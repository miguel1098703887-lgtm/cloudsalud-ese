"""
CloudSalud Copiloto ESE - Chat & Voice API Endpoint
Orquestador inteligente que integra Sanitización (Ley 1581), RBAC, RAG Normativo, Text-to-SQL y Auditoría.
"""

import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.security.sanitizer import sanitize_query, format_privacy_notice
from app.security.rbac import verify_permission, UserRole
from app.security.audit_logger import log_audit_event
from app.modules.habilitacion_rag import search_normativa
from app.modules.text_to_sql import process_query_analytics
from app.modules.proactive_engine import generate_morning_briefing, get_proactive_alarms

router = APIRouter(prefix="/api", tags=["Chat & Copiloto"])

class ChatRequest(BaseModel):
    query: str
    role: str = "GERENTE_GENERAL"
    channel: str = "Dashboard Web"
    user_id: str = "DIR-001"
    is_voice: bool = False

class ChatResponse(BaseModel):
    response_text: str
    card: Optional[Dict[str, Any]] = None
    suggested_pills: List[str]
    anonymized_query: str
    had_privacy_redactions: bool
    module_used: str
    sql_executed: Optional[str] = None
    execution_time_ms: float

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(request: ChatRequest):
    start_time = time.time()
    raw_query = request.query.strip()
    role = request.role
    channel = request.channel if not request.is_voice else "WhatsApp Business API (Nota de Voz)"
    user_id = request.user_id

    # 1. Sanitización de datos sensibles de salud (Ley 1581 / Habeas Data)
    sanitized_q, had_redactions, redactions_list = sanitize_query(raw_query)
    q_lower = sanitized_q.lower()

    # Valores por defecto
    module_used = "DESCONOCIDO"
    sql_executed = None
    card_data = None
    response_text = ""
    suggested_pills = [
        "🌅 Briefing Matutino",
        "⚠️ Alertas Habilitación",
        "💰 Cartera Nueva EPS",
        "🌡️ Ocupación Urgencias y UCI"
    ]

    # 2. Manejo de Disparadores Proactivos Rápidos (Briefing / Alertas)
    if any(k in q_lower for k in ["briefing", "buenos dias", "resumen de inicio", "informe matutino"]):
        # Verificar permiso
        allowed, msg = verify_permission(role, "BRIEFING_ESTRATEGICO")
        if not allowed:
            response_text = msg
            module_used = "RBAC_DENIED"
        else:
            briefing = generate_morning_briefing()
            response_text = briefing["resumen_texto"]
            card_data = {
                "tipo": "BRIEFING_SUMMARY",
                "metrics": briefing["metrics"]
            }
            module_used = "PROACTIVE_BRIEFING"
            suggested_pills = [
                "⚠️ Ver Alertas de Habilitación",
                "💰 Detalle Cartera Nueva EPS",
                "⏱️ Pacientes Triage 2 > 4h",
                "💊 Stock Insumos Farmacia"
            ]

    elif any(k in q_lower for k in ["alertas habilitacion", "vencimientos", "calibracion", "rethus vencido"]):
        allowed, msg = verify_permission(role, "HABILITACION_CALIDAD")
        if not allowed:
            response_text = msg
            module_used = "RBAC_DENIED"
        else:
            alarms = get_proactive_alarms()
            module_used = "PROACTIVE_ALARMS"
            lineas = []
            for a in alarms:
                lineas.append(
                    f"### 🔔 {a['titulo']} [{a['nivel']}]\n"
                    f"• **Detalle:** {a['detalle']}\n"
                    f"• **Marco Normativo:** *{a['impacto_normativo']}*\n"
                    f"• **Acción Recomendada:** {a['accion_sugerida']}"
                )
            response_text = (
                "## ⚠️ Tablero de Alertas Tempranas de Habilitación y Operación\n\n"
                "El copiloto ha detectado los siguientes eventos críticos con impacto regulatorio inminente:\n\n"
                + "\n\n---\n\n".join(lineas)
            )
            card_data = {
                "tipo": "PROACTIVE_ALARMS_LIST",
                "total_alertas": len(alarms),
                "alertas": alarms
            }
            suggested_pills = [
                "🏥 Requisitos Habilitar UCI Neonatal",
                "📋 Protocolo Lavado de Manos PAMEC",
                "📊 Ejecución Presupuestal Rubros"
            ]

    else:
        # 3. Detectar si corresponde a módulo Financiero
        is_financial = any(k in q_lower for k in ["cartera", "glosa", "presupuesto", "rubro", "factura"])
        if is_financial:
            # RBAC Check
            allowed, msg = verify_permission(role, "FINANCIERO_CARTERA")
            if not allowed:
                response_text = msg
                module_used = "RBAC_DENIED"
            else:
                sql_res = process_query_analytics(sanitized_q)
                if sql_res["matched"]:
                    response_text = sql_res["text"]
                    card_data = sql_res.get("card")
                    sql_executed = sql_res.get("sql")
                    module_used = "TEXT_TO_SQL_FINANCIERO"
                else:
                    response_text = "No logré estructurar una consulta financiera para esa solicitud. Intente con: '¿A cuánto asciende la cartera con Nueva EPS?' o 'Resumen de glosas'."

        # 4. Detectar si corresponde a módulo Operativo / Camas / Triage / Farmacia
        elif any(k in q_lower for k in ["ocupacion", "camas", "triage", "4 horas", "farmacia", "desabastecimiento", "stock"]):
            allowed, msg = verify_permission(role, "OPERATIVO_CAMAS")
            if not allowed:
                response_text = msg
                module_used = "RBAC_DENIED"
            else:
                sql_res = process_query_analytics(sanitized_q)
                if sql_res["matched"]:
                    response_text = sql_res["text"]
                    card_data = sql_res.get("card")
                    sql_executed = sql_res.get("sql")
                    module_used = "TEXT_TO_SQL_OPERATIVO"
                else:
                    response_text = "No logré consultar los datos operativos en vivo. Puede preguntar por: 'Ocupación de Urgencias y UCI' o 'Pacientes en Triage 2 más de 4 horas'."

        # 5. RAG Normativo de Habilitación y Calidad (Res. 3100, PAMEC, Ley 1438)
        else:
            rag_res = search_normativa(sanitized_q)
            if rag_res["found"]:
                response_text = rag_res["respuesta_estructurada"]
                card_data = rag_res.get("card_data")
                module_used = "RAG_HABILITACION"
            else:
                # Fallback con Text-to-SQL por si hay términos analíticos
                sql_res = process_query_analytics(sanitized_q)
                if sql_res["matched"]:
                    response_text = sql_res["text"]
                    card_data = sql_res.get("card")
                    sql_executed = sql_res.get("sql")
                    module_used = "TEXT_TO_SQL_FALLBACK"
                else:
                    response_text = (
                        "Soy el **Copiloto Gerencial de CloudSalud para ESE**.\n\n"
                        "Puedo apoyarle estratégicamente en:\n"
                        "1. **Habilitación y Calidad (Res. 3100 / PAMEC):** Consulte requisitos para UCI Neonatal, Urgencias, o soporte documental.\n"
                        "2. **Finanzas y Glosas:** Cartera >90 días con EPS, glosas pendientes y ejecución presupuestal.\n"
                        "3. **Operación Asistencial en Tiempo Real:** Ocupación de camas, esperas en Triage 2 y stock de farmacia.\n\n"
                        "Seleccione una acción rápida o escriba/dicte su inquietud."
                    )
                    module_used = "GENERAL_GUIDE"

    # 6. Agregar aviso legal de Habeas Data si se anonimizó algo
    if had_redactions:
        response_text += format_privacy_notice(redactions_list)

    execution_time = round((time.time() - start_time) * 1000, 2)

    # 7. Registrar evento en log de auditoría inalterable
    log_audit_event(
        canal=channel,
        rol_usuario=role,
        id_usuario=user_id,
        pregunta_original=raw_query,
        pregunta_anonimizada=sanitized_q,
        modulo_invocado=module_used,
        sql_ejecutado=sql_executed,
        tiempo_respuesta_ms=execution_time
    )

    return ChatResponse(
        response_text=response_text,
        card=card_data,
        suggested_pills=suggested_pills,
        anonymized_query=sanitized_q,
        had_privacy_redactions=had_redactions,
        module_used=module_used,
        sql_executed=sql_executed,
        execution_time_ms=execution_time
    )
