"""
CloudSalud Copiloto ESE - Database Engine
Configuración y esquema de base de datos relacional para Hospital San Rafael E.S.E.
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path(__file__).resolve().parent.parent / "cloudsalud_ese.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Camas y Ocupación Hospitalaria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS camas_hospitalarias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_cama TEXT UNIQUE NOT NULL,
        servicio TEXT NOT NULL, -- 'Urgencias Adultos', 'UCI Adultos', 'UCI Neonatal', 'Hospitalización Cirugía', 'Gineco-Obstetricia'
        estado TEXT NOT NULL,   -- 'Ocupada', 'Disponible', 'Mantenimiento / Desinfección'
        triage TEXT,            -- 'Triage 1', 'Triage 2', 'Triage 3', NULL
        tiempo_espera_horas REAL DEFAULT 0,
        motivo_ingreso_agregado TEXT, -- Ley 1581: datos agregados/patología sindrómica
        fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Cartera por EPS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cartera_eps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eps_nombre TEXT UNIQUE NOT NULL,
        codigo_eps TEXT NOT NULL,
        regimen TEXT NOT NULL, -- 'Contributivo', 'Subsidiado'
        corriente REAL NOT NULL,
        dias_31_90 REAL NOT NULL,
        dias_91_180 REAL NOT NULL,
        dias_181_360 REAL NOT NULL,
        mayor_360 REAL NOT NULL,
        total_cartera REAL NOT NULL,
        estado_auditoria TEXT DEFAULT 'Activo'
    );
    """)

    # 3. Glosas de Facturación (Decreto 441 de 2022)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS glosas_facturacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_radicado TEXT NOT NULL,
        eps_nombre TEXT NOT NULL,
        codigo_glosa TEXT NOT NULL, -- Ej: 'GL-01 Pertinencia Médica', 'GL-02 Soporte Incompleto', 'GL-03 Tarifas'
        concepto_glosa TEXT NOT NULL,
        valor_facturado REAL NOT NULL,
        valor_glosado REAL NOT NULL,
        fecha_notificacion DATE NOT NULL,
        dias_habiles_respuesta INTEGER NOT NULL, -- Plazo legal: 20 días hábiles
        estado_glosa TEXT NOT NULL -- 'Pendiente Respuesta', 'Conciliada', 'Aceptada ESE', 'Ratificada EPS'
    );
    """)

    # 4. Equipos Biomédicos y Metrología (Res. 3100/2019 Estándar Dotación)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos_biomedicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_activo TEXT UNIQUE NOT NULL,
        nombre_equipo TEXT NOT NULL,
        marca_modelo TEXT NOT NULL,
        servicio_ubicacion TEXT NOT NULL, -- 'Urgencias Sala Reanimación', 'UCI Neonatal', 'Quirófano 1'
        fecha_ultima_calibracion DATE NOT NULL,
        fecha_vencimiento_calibracion DATE NOT NULL,
        dias_para_vencer INTEGER NOT NULL,
        estado_operativo TEXT NOT NULL, -- 'Operativo', 'Mantenimiento Preventivo', 'Fuera de Servicio'
        clasificacion_riesgo TEXT NOT NULL -- 'Clase I', 'Clase IIa', 'Clase IIb', 'Clase III'
    );
    """)

    # 5. Talento Humano y ReTHUS (Res. 3100/2019 Estándar Talento Humano)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS talento_humano (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_personal_anonimizado TEXT UNIQUE NOT NULL, -- Ley 1581: TH-2041
        perfil_profesional TEXT NOT NULL,             -- 'Médico Especialista Neonatología', 'Médico General Urgencias', 'Enfermera Jefe UCI'
        servicio_asignado TEXT NOT NULL,
        registro_rethus_estado TEXT NOT NULL,         -- 'Vigente', 'Vencido', 'En Trámite de Renovación'
        fecha_vencimiento_rethus DATE,
        poliza_responsabilidad_medica TEXT NOT NULL,  -- 'Vigente', 'Vencida'
        dias_vencimiento_poliza INTEGER NOT NULL,
        tipo_vinculacion TEXT NOT NULL                -- 'Planta Permanente', 'Contrato Prestación de Servicios'
    );
    """)

    # 6. Ejecución Presupuestal ESE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS presupuesto_rubros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_rubro TEXT UNIQUE NOT NULL,
        nombre_rubro TEXT NOT NULL,
        apropiacion_inicial REAL NOT NULL,
        apropiacion_vigente REAL NOT NULL,
        comprometido REAL NOT NULL,
        ejecutado_giro REAL NOT NULL,
        saldo_disponible REAL NOT NULL,
        porcentaje_ejecucion REAL NOT NULL
    );
    """)

    # 7. Inventario Crítico Farmacia e Insumos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario_farmacia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_cum TEXT UNIQUE NOT NULL,
        nombre_medicamento TEXT NOT NULL,
        forma_farmaceutica TEXT NOT NULL,
        es_vital_no_disponible BOOLEAN DEFAULT 0,
        stock_actual INTEGER NOT NULL,
        stock_minimo_seguridad INTEGER NOT NULL,
        dias_autonomia_consumo INTEGER NOT NULL,
        estado_alerta TEXT NOT NULL -- 'Normal', 'Alerta Temprana', 'Riesgo Desabastecimiento Crítico'
    );
    """)

    # 8. Registro de Auditoría y Trazabilidad (Contraloría / Supersalud / Ley 1581)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auditoria_consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        canal TEXT NOT NULL,          -- 'Dashboard Web', 'WhatsApp Business API (Voz/Texto)'
        rol_usuario TEXT NOT NULL,    -- 'GERENTE_GENERAL', 'SUBGERENTE_CIENTIFICO', 'DIRECTOR_FINANCIERO'
        id_usuario TEXT NOT NULL,
        pregunta_original TEXT NOT NULL,
        pregunta_anonimizada TEXT NOT NULL,
        modulo_invocado TEXT NOT NULL, -- 'RAG_HABILITACION', 'TEXT_TO_SQL', 'PROACTIVE_BRIEFING'
        sql_ejecutado TEXT,
        tiempo_respuesta_ms REAL NOT NULL
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Base de datos inicializada en: {DB_PATH}")
