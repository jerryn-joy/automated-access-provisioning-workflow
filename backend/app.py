from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI(title="Self-Service Access Portal API")

# Demo manager directory
MANAGER_MAP: Dict[str, str] = {
    "jerrynjoy.jj@gmail.com": "jerrynjoy.jj@gmail.com",
    "bob@company-demo.com": "manager.it@company-demo.com",
    "charlie@company-demo.com": "manager.projects@company-demo.com",
}

# Demo resource-to-group mapping
RESOURCE_GROUP_MAP: Dict[str, str] = {
    "Lizenz für Analyse-Software": "grp_analysis_software",
    "Zugriff auf Projekt-Marketing-SharePoint": "grp_marketing_sharepoint",
    "Zugriff auf internes Wiki-Editoren": "grp_internal_wiki_editors",
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
    manager_email = MANAGER_MAP.get(user_email.lower())
    if not manager_email:
        raise HTTPException(status_code=404, detail="Manager not found for this user")
    return {
        "user_email": user_email.lower(),
        "manager_email": manager_email
    }

@app.post("/api/provision-access")
def provision_access(payload: ProvisionRequest):
    group_name = RESOURCE_GROUP_MAP.get(payload.resource)
    if not group_name:
        raise HTTPException(status_code=400, detail="Unknown resource")

    # Simulated provisioning result
    return {
        "success": True,
        "request_id": payload.request_id,
        "user_email": payload.user_email,
        "group_name": group_name,
        "message": f"User added to group {group_name}"
    }
