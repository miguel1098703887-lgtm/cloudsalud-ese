"""
CloudSalud Copiloto ESE - Dashboard KPI API Endpoint
Retorna las métricas consolidadas en tiempo real del hospital para la vista ejecutiva.
"""

from fastapi import APIRouter
from app.database import get_connection

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # Ocupación Urgencias
    cursor.execute("""
    SELECT COUNT(*) as total, SUM(CASE WHEN estado = 'Ocupada' THEN 1 ELSE 0 END) as ocupadas
    FROM camas_hospitalarias WHERE servicio = 'Urgencias Adultos';
    """)
    urg = cursor.fetchone()
    urg_pct = round((urg["ocupadas"] / urg["total"] * 100), 1) if urg["total"] > 0 else 0

    # Camas UCI libres (Adultos + Neonatal)
    cursor.execute("""
    SELECT SUM(CASE WHEN estado = 'Disponible' THEN 1 ELSE 0 END) as libres
    FROM camas_hospitalarias WHERE servicio IN ('UCI Adultos', 'UCI Neonatal');
    """)
    uci_libres = cursor.fetchone()["libres"] or 0

    # Cartera total y >90 días
    cursor.execute("""
    SELECT SUM(total_cartera) as total,
           SUM(dias_91_180 + dias_181_360 + mayor_360) as mayor_90
    FROM cartera_eps;
    """)
    cart = cursor.fetchone()
    total_cartera = cart["total"] or 0
    cartera_m90 = cart["mayor_90"] or 0

    # Glosas pendientes
    cursor.execute("SELECT SUM(valor_glosado) as glosas FROM glosas_facturacion WHERE estado_glosa = 'Pendiente Respuesta';")
    total_glosas = cursor.fetchone()["glosas"] or 0

    # Equipos con calibración próxima (<30d)
    cursor.execute("SELECT COUNT(*) as equipos FROM equipos_biomedicos WHERE dias_para_vencer <= 30;")
    equipos_alerta = cursor.fetchone()["equipos"]

    # ReTHUS pendientes
    cursor.execute("SELECT COUNT(*) as rethus FROM talento_humano WHERE registro_rethus_estado != 'Vigente';")
    rethus_alerta = cursor.fetchone()["rethus"]

    # Insumos críticos
    cursor.execute("SELECT COUNT(*) as insumos FROM inventario_farmacia WHERE dias_autonomia_consumo <= 3;")
    insumos_criticos = cursor.fetchone()["insumos"]

    conn.close()

    return {
        "hospital_nombre": "Hospital San Rafael E.S.E. - Nivel II",
        "municipio": "Facatativá / Cundinamarca",
        "urgencias_ocupacion_pct": urg_pct,
        "urgencias_ocupadas": urg["ocupadas"],
        "urgencias_total": urg["total"],
        "camas_uci_libres": uci_libres,
        "cartera_total_cop": total_cartera,
        "cartera_mayor_90_cop": cartera_m90,
        "glosas_pendientes_cop": total_glosas,
        "alertas_biomedicas_count": equipos_alerta,
        "rethus_por_renovar_count": rethus_alerta,
        "farmacia_critica_count": insumos_criticos
    }
