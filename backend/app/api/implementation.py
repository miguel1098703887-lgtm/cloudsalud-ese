"""
CloudSalud Copiloto ESE - API de Plan de Implementación & Blindaje de Auditorías
Permite consultar, filtrar y actualizar el estado de los 32 ítems de implementación.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.modules.implementation_items import IMPLEMENTATION_ITEMS, get_implementation_summary
from app.database import get_connection

router = APIRouter(prefix="/api/implementation", tags=["Plan de Implementación"])

class StatusUpdateRequest(BaseModel):
    estado: str  # "Implementado", "En Curso", "Pendiente"

@router.get("/items")
def list_implementation_items(categoria: Optional[str] = None, prioridad: Optional[str] = None, eje: Optional[str] = None):
    """Retorna la lista completa de ítems para implementar junto con el resumen ejecutivo."""
    items = IMPLEMENTATION_ITEMS
    if categoria:
        items = [i for i in items if i["categoria"].lower() == categoria.lower()]
    if prioridad:
        items = [i for i in items if i["prioridad"].lower() == prioridad.lower()]
    if eje:
        items = [i for i in items if i["eje"].lower() == eje.lower()]

    summary = get_implementation_summary()
    return {
        "summary": summary,
        "items": items
    }

@router.post("/toggle/{item_id}")
def update_item_status(item_id: str, payload: StatusUpdateRequest):
    """Actualiza interactivamente el estado de un ítem para implementar."""
    valid_states = ["Implementado", "En Curso", "Pendiente"]
    if payload.estado not in valid_states:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Opciones: {valid_states}")

    target = None
    for item in IMPLEMENTATION_ITEMS:
        if item["id"] == item_id or item["codigo"] == item_id:
            item["estado"] = payload.estado
            target = item
            break

    if not target:
        raise HTTPException(status_code=404, detail="Ítem de implementación no encontrado.")

    return {
        "success": True,
        "updated_item": target,
        "new_summary": get_implementation_summary()
    }

@router.post("/autodiagnosis")
def run_live_autodiagnosis():
    """
    Ejecuta un autodiagnóstico en tiempo real cruzando la base de datos de la E.S.E.
    con los ítems de implementación de los 5 puntos críticos.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Talento Humano / ReTHUS
    cursor.execute("SELECT COUNT(*) as alert_count FROM talento_humano WHERE registro_rethus_estado != 'Vigente';")
    rethus_alerts = cursor.fetchone()["alert_count"]

    # 2. Parque Biomédico
    cursor.execute("SELECT COUNT(*) as alert_count FROM equipos_biomedicos WHERE dias_para_vencer <= 30;")
    biomed_alerts = cursor.fetchone()["alert_count"]

    # 3. Farmacia / Carro de Paro
    cursor.execute("SELECT COUNT(*) as alert_count FROM inventario_farmacia WHERE dias_autonomia_consumo <= 3;")
    farmacia_alerts = cursor.fetchone()["alert_count"]

    # 4. Glosas
    cursor.execute("SELECT COUNT(*) as count, SUM(valor_glosado) as total FROM glosas_facturacion WHERE estado_glosa = 'Pendiente Respuesta';")
    glosas_row = cursor.fetchone()
    glosas_count = glosas_row["count"] or 0
    glosas_total = glosas_row["total"] or 0

    conn.close()

    findings = []
    if rethus_alerts > 0:
        findings.append({
            "area": "Talento Humano (RETHUS)",
            "codigo_item": "TH-01",
            "severidad": "CRÍTICA",
            "hallazgo": f"Se detectaron {rethus_alerts} profesionales asistenciales con inscripción en ReTHUS vencida o en trámite.",
            "accion_recomendada": "Activar el conector automático RETHUS (IMP-TH-01) y emitir alerta de renovación."
        })
    if biomed_alerts > 0:
        findings.append({
            "area": "Parque Biomédico (Metrología)",
            "codigo_item": "BM-03",
            "severidad": "CRÍTICA",
            "hallazgo": f"{biomed_alerts} equipos de soporte vital (incluyendo desfibriladores de urgencias) vencen calibración en menos de 30 días.",
            "accion_recomendada": "Generar orden técnica urgente en módulo de Metrología (IMP-BM-03) para evitar sellamiento preventivo."
        })
    if farmacia_alerts > 0:
        findings.append({
            "area": "Farmacia y Carro de Paro",
            "codigo_item": "FA-02",
            "severidad": "CRÍTICA",
            "hallazgo": f"{farmacia_alerts} insumos del carro de paro tienen autonomía crítica menor a 3 días.",
            "accion_recomendada": "Ejecutar checklist de cambio de turno digital (IMP-FA-02) y reposición inmediata con químico farmacéutico."
        })
    if glosas_count > 0:
        findings.append({
            "area": "Historia Clínica y Glosas",
            "codigo_item": "HC-02",
            "severidad": "ALTA",
            "hallazgo": f"{glosas_count} facturas objetadas por EPS que suman ${round(glosas_total/1e6, 1)}M pendientes de respuesta bajo Decreto 441.",
            "accion_recomendada": "Activar pre-auditoría algorítmica de historias clínicas (IMP-HC-02) y formatos de la Res. 3280."
        })

    summary = get_implementation_summary()

    return {
        "status": "Autodiagnóstico ejecutado exitosamente",
        "hospital": "Hospital San Rafael E.S.E. - Nivel II",
        "indice_blindaje_actual": f"{summary['porcentaje_avance']}%",
        "total_hallazgos_preventivos": len(findings),
        "hallazgos": findings,
        "resumen_implementacion": summary
    }
