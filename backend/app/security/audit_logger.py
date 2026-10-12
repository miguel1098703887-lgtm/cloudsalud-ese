"""
CloudSalud Copiloto ESE - Immutable Audit Logger
Registro de auditoría conforme a la Ley 1474 de 2011 (Estatuto Anticorrupción) y Circular Única de la Supersalud.
"""

import time
from typing import Optional
from app.database import get_connection

def log_audit_event(
    canal: str,
    rol_usuario: str,
    id_usuario: str,
    pregunta_original: str,
    pregunta_anonimizada: str,
    modulo_invocado: str,
    sql_ejecutado: Optional[str],
    tiempo_respuesta_ms: float
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO auditoria_consultas (
            canal, rol_usuario, id_usuario, pregunta_original,
            pregunta_anonimizada, modulo_invocado, sql_ejecutado,
            tiempo_respuesta_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            canal, rol_usuario, id_usuario, pregunta_original,
            pregunta_anonimizada, modulo_invocado, sql_ejecutado,
            tiempo_respuesta_ms
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR AUDITORÍA]: No se pudo registrar el log: {e}")

def get_recent_audit_logs(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, timestamp, canal, rol_usuario, id_usuario,
           pregunta_anonimizada, modulo_invocado, sql_ejecutado, tiempo_respuesta_ms
    FROM auditoria_consultas
    ORDER BY id DESC
    LIMIT ?;
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
