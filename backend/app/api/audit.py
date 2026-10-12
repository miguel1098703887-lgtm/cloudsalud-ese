"""
CloudSalud Copiloto ESE - Audit Log Inspection API
Permite consultar el registro inalterable de auditoría para revisiones de Contraloría, Procuraduría o Control Interno.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from app.security.audit_logger import get_recent_audit_logs
from app.security.rbac import verify_permission, UserRole

router = APIRouter(prefix="/api/audit", tags=["Auditoría y Trazabilidad"])

@router.get("/logs")
def view_audit_logs(role: str = "GERENTE_GENERAL", limit: int = Query(50, le=100)):
    allowed, msg = verify_permission(role, "AUDITORIA_LOGS")
    if not allowed:
        raise HTTPException(status_code=403, detail=msg)
    
    logs = get_recent_audit_logs(limit)
    return {
        "status": "success",
        "total_registros": len(logs),
        "logs": logs
    }
