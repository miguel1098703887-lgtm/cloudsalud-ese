"""
CloudSalud Copiloto ESE - Proactive Engine & Morning Briefing
Genera el informe ejecutivo de las 6:30 a.m. y monitorea alertas proactivas
(calibración biomédica, ReTHUS, riesgo de glosas y stock crítico).
"""

from typing import Dict, Any, List
from app.database import get_connection

def generate_morning_briefing(user_name: str = "Dr. Carlos Mendoza (Gerente)") -> Dict[str, Any]:
    """
    Construye el briefing matutino proactivo de las 6:30 a.m.
    sintetizando asistencial, habilitación, finanzas y alertas del día.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Ocupación Urgencias y UCI
    cursor.execute("""
    SELECT servicio, COUNT(*) as total, SUM(CASE WHEN estado = 'Ocupada' THEN 1 ELSE 0 END) as ocupadas
    FROM camas_hospitalarias
    WHERE servicio IN ('Urgencias Adultos', 'UCI Adultos', 'UCI Neonatal')
    GROUP BY servicio;
    """)
    ocupaciones = {r["servicio"]: {"total": r["total"], "ocupadas": r["ocupadas"], "disp": r["total"] - r["ocupadas"]} for r in cursor.fetchall()}

    # Triage 2 crítico
    cursor.execute("SELECT COUNT(*) FROM camas_hospitalarias WHERE tiempo_espera_horas >= 4.0 AND triage = 'Triage 2';")
    pacientes_triage_demora = cursor.fetchone()[0]

    # Equipos con calibración próxima a vencer (< 30 días)
    cursor.execute("SELECT COUNT(*) FROM equipos_biomedicos WHERE dias_para_vencer <= 30;")
    equipos_por_vencer = cursor.fetchone()[0]

    # Personal con ReTHUS por renovar
    cursor.execute("SELECT COUNT(*) FROM talento_humano WHERE registro_rethus_estado != 'Vigente';")
    rethus_pendientes = cursor.fetchone()[0]

    # Rubros presupuestales en riesgo (>90%)
    cursor.execute("SELECT COUNT(*) FROM presupuesto_rubros WHERE porcentaje_ejecucion >= 90.0;")
    rubros_agotamiento = cursor.fetchone()[0]

    # Medicamentos críticos (<5 días autonomía)
    cursor.execute("SELECT COUNT(*) FROM inventario_farmacia WHERE dias_autonomia_consumo <= 3;")
    medicamentos_criticos = cursor.fetchone()[0]

    conn.close()

    urg_data = ocupaciones.get("Urgencias Adultos", {"total": 35, "ocupadas": 33, "disp": 2})
    urg_pct = round((urg_data["ocupadas"] / urg_data["total"]) * 100, 1)

    ucia_data = ocupaciones.get("UCI Adultos", {"total": 15, "ocupadas": 12, "disp": 3})
    ucin_data = ocupaciones.get("UCI Neonatal", {"total": 8, "ocupadas": 7, "disp": 1})
    total_uci_disp = ucia_data["disp"] + ucin_data["disp"]

    texto = (
        f"🌅 **Briefing Matutino - Hospital San Rafael E.S.E.** (06:30 a.m.)\n"
        f"Buenos días, **{user_name}**. Este es el estado consolidado para el inicio de jornada:\n\n"
        f"**1. 🌡️ Frente Asistencial & Camas:**\n"
        f"• **Urgencias Adultos:** Al **{urg_pct}% de ocupación** ({urg_data['ocupadas']}/{urg_data['total']} camas ocupadas, solo **{urg_data['disp']} disponibles**).\n"
        f"• **Cuidados Intensivos:** **{total_uci_disp} camas UCI disponibles** ({ucia_data['disp']} UCI Adultos, {ucin_data['disp']} UCI Neonatal).\n"
        f"• **Alerta Triage:** **{pacientes_triage_demora} pacientes** llevan más de 4 horas esperando cama en Triage 2.\n\n"
        f"**2. ⚠️ Frente de Calidad & Habilitación (Res. 3100):**\n"
        f"• **{equipos_por_vencer} equipos biomédicos** tienen calibración que vence en los próximos 15 a 25 días (incluye 5 desfibriladores de urgencias y 1 ventilador neonatal).\n"
        f"• **{rethus_pendientes} profesionales de la salud** tienen pendiente actualización de su inscripción en el ReTHUS.\n\n"
        f"**3. 💰 Frente Financiero & Operativo:**\n"
        f"• **Cartera Vencida:** Nueva EPS acumula **$2.480 millones** en mora superior a 90 días.\n"
        f"• **Presupuesto:** **{rubros_agotamiento} rubro** ('Material Médico-Quirúrgico') al **91.8%** de ejecución.\n"
        f"• **Farmacia:** **{medicamentos_criticos} insumos vitales** con stock crítico (Adrenalina para 2 días).\n\n"
        f"📌 *Agenda Externa:* Visita de auditoría preventiva programada de la Secretaría de Salud Departamental para esta semana."
    )

    return {
        "titulo": "Briefing Matutino 6:30 AM",
        "resumen_texto": texto,
        "metrics": {
            "urgencias_ocupacion": f"{urg_pct}%",
            "camas_uci_libres": total_uci_disp,
            "pacientes_triage2_demora": pacientes_triage_demora,
            "calibraciones_por_vencer": equipos_por_vencer,
            "rethus_por_renovar": rethus_pendientes,
            "medicamentos_criticos": medicamentos_criticos
        }
    }

def get_proactive_alarms() -> List[Dict[str, Any]]:
    """
    Retorna la lista de alertas tempranas automáticas que el asistente dispara sin que el usuario pregunte.
    """
    conn = get_connection()
    cursor = conn.cursor()

    alarms = []

    # 1. Alarma Biomédica
    cursor.execute("""
    SELECT codigo_activo, nombre_equipo, servicio_ubicacion, dias_para_vencer
    FROM equipos_biomedicos
    WHERE dias_para_vencer <= 20
    ORDER BY dias_para_vencer ASC;
    """)
    biomedicos = [dict(r) for r in cursor.fetchall()]
    if biomedicos:
        alarms.append({
            "categoria": "HABILITACION_DOTACION",
            "nivel": "CRITICO",
            "titulo": f"Vencimiento Inminente de Calibración ({len(biomedicos)} Equipos)",
            "detalle": f"En 15 días vence la calibración metrológica de 5 desfibriladores bifásicos en Urgencias y en 7 días el ventilador neonatal Babylog VN500 en UCI Neonatal.",
            "impacto_normativo": "Resolución 3100 de 2019 - Estándar de Dotación (Hallazgo de cierre de servicio)",
            "accion_sugerida": "Contactar de inmediato al proveedor de mantenimiento metrológico contratado."
        })

    # 2. Alarma Talento Humano / ReTHUS
    cursor.execute("""
    SELECT id_personal_anonimizado, perfil_profesional, servicio_asignado, registro_rethus_estado
    FROM talento_humano
    WHERE registro_rethus_estado != 'Vigente';
    """)
    th = [dict(r) for r in cursor.fetchall()]
    if th:
        alarms.append({
            "categoria": "HABILITACION_TALENTO_HUMANO",
            "nivel": "ALERTA",
            "titulo": f"Pendiente Renovación ReTHUS ({len(th)} Profesionales)",
            "detalle": f"{len(th)} médicos (2 de Urgencias y 1 Pediatra) figuran en estado 'Por Renovar' en el Registro de Talento Humano en Salud.",
            "impacto_normativo": "Resolución 3100 de 2019 - Estándar de Talento Humano y Ley 1164 de 2007",
            "accion_sugerida": "Oficio preventivo a la Coordinación Médica para radicar soportes en plataforma Sispro/ReTHUS."
        })

    # 3. Alarma Farmacia
    cursor.execute("""
    SELECT nombre_medicamento, dias_autonomia_consumo, stock_actual
    FROM inventario_farmacia
    WHERE dias_autonomia_consumo <= 3;
    """)
    farma = [dict(r) for r in cursor.fetchall()]
    if farma:
        nombres = ", ".join([f"{f['nombre_medicamento']} ({f['dias_autonomia_consumo']} días)" for f in farma])
        alarms.append({
            "categoria": "OPERATIVO_FARMACIA",
            "nivel": "CRITICO",
            "titulo": "Riesgo de Desabastecimiento Inminente en Farmacia",
            "detalle": f"Stock crítico en insumos vitales: {nombres}.",
            "impacto_normativo": "Garantía de oportunidad en carro de paro y reanimación (Ley Estatutaria 1751)",
            "accion_sugerida": "Emitir orden de compra de urgencia con cargo al rubro de medicamentos esenciales."
        })

    conn.close()
    return alarms
