from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Self-Service Access Portal API")

# Demo manager directory
MANAGER_MAP: Dict[str, str] = {
    "jerryn.c.joy@gmail.com": "jerrynjoy.jj@gmail.com",
    "jerryn.joy@hyfindr.com": "jerrynjoy.jj@gmail.com",
    "jerrynjoy.jj@gmail.com": "jerrynjoy.jj@gmail.com",
}

# Resource-to-group mapping (MUST match frontend values exactly)
RESOURCE_GROUP_MAP: Dict[str, str] = {
    "License for Analysis Software": "grp_analysis_software",
    "Access to Project Marketing SharePoint": "grp_marketing_sharepoint",
    "Access to Internal Wiki Editors": "grp_internal_wiki_editors",
}

class ProvisionRequest(BaseModel):
    request_id: str
    user_email: EmailStr
    resource: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/manager/{user_email}")
def get_manager(user_email: str):
    user_email = user_email.lower()
    logger.info(f"[REQUEST] Manager lookup for: {user_email}")

    manager_email = MANAGER_MAP.get(user_email)
    if not manager_email:
        logger.warning(f"[ERROR] No manager found for: {user_email}")
        raise HTTPException(status_code=404, detail="Manager not found for this user")

    logger.info(f"[RESPONSE] Manager found: {manager_email}")

    return {
        "user_email": user_email,
        "manager_email": manager_email
    }

@app.post("/api/provision-access")
def provision_access(payload: ProvisionRequest):
    logger.info(f"[REQUEST] Provisioning request: {payload}")

    group_name = RESOURCE_GROUP_MAP.get(payload.resource)
    if not group_name:
        logger.error(f"[ERROR] Unknown resource: {payload.resource}")
        raise HTTPException(status_code=400, detail="Unknown resource")

    # Simulated provisioning
    logger.info(f"[ACTION] Adding {payload.user_email} to group {group_name}")

    logger.info(f"[RESPONSE] Provisioning successful for {payload.user_email}")

    return {
        "success": True,
        "request_id": payload.request_id,
        "user_email": payload.user_email,
        "group_name": group_name,
        "message": f"User added to group {group_name}"
    }
