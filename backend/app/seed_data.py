"""
CloudSalud Copiloto ESE - Seed Data Script
Genera datos realistas y representativos de una ESE Hospital Nivel II en Colombia.
"""

from app.database import get_connection, init_db

def seed_database():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Limpiar tablas previas
    tables = [
        "camas_hospitalarias", "cartera_eps", "glosas_facturacion",
        "equipos_biomedicos", "talento_humano", "presupuesto_rubros",
        "inventario_farmacia", "auditoria_consultas"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")

    # 1. Camas Hospitalarias
    # Total Urgencias: 35 camas (33 ocupadas = 94.3% ocupación)
    # UCI Adultos: 15 camas (12 ocupadas, 3 disponibles = 80% ocupación)
    # UCI Neonatal: 8 camas (7 ocupadas, 1 disponible = 87.5% ocupación)
    # Hospitalización: 50 camas (42 ocupadas = 84% ocupación)
    camas = []
    
    # Urgencias
    for i in range(1, 36):
        cod = f"URG-{i:02d}"
        if i <= 33:
            estado = "Ocupada"
            # 5 pacientes en triage 2 con más de 4 horas esperando cama de piso
            triage = "Triage 2" if i <= 15 else ("Triage 1" if i <= 20 else "Triage 3")
            horas = 4.8 if i in [3, 7, 12, 14] else (2.5 if i < 15 else 1.2)
            motivo = "Síndrome coronario / Dolor torácico" if i % 3 == 0 else "Infección respiratoria aguda / Trauma"
        else:
            estado = "Disponible"
            triage = None
            horas = 0.0
            motivo = None
        camas.append((cod, "Urgencias Adultos", estado, triage, horas, motivo))

    # UCI Adultos
    for i in range(1, 16):
        cod = f"UCIA-{i:02d}"
        estado = "Ocupada" if i <= 12 else "Disponible"
        camas.append((cod, "UCI Adultos", estado, "Triage 1" if estado == "Ocupada" else None, 18.0 if estado == "Ocupada" else 0.0, "Postoperatorio cardiovascular / Sepsis severa" if estado == "Ocupada" else None))

    # UCI Neonatal
    for i in range(1, 9):
        cod = f"UCIN-{i:02d}"
        estado = "Ocupada" if i <= 7 else "Disponible"
        camas.append((cod, "UCI Neonatal", estado, "Triage 1" if estado == "Ocupada" else None, 36.0 if estado == "Ocupada" else 0.0, "Prematurez extrema / Dificultad respiratoria neonatal" if estado == "Ocupada" else None))

    # Hospitalización Cirugía
    for i in range(1, 51):
        cod = f"HOSP-{i:02d}"
        estado = "Ocupada" if i <= 42 else ("Mantenimiento / Desinfección" if i == 43 else "Disponible")
        camas.append((cod, "Hospitalización Cirugía", estado, None, 48.0 if estado == "Ocupada" else 0.0, "Recuperación postquirúrgica apendicectomía/colecistectomía" if estado == "Ocupada" else None))

    cursor.executemany("""
    INSERT INTO camas_hospitalarias (codigo_cama, servicio, estado, triage, tiempo_espera_horas, motivo_ingreso_agregado)
    VALUES (?, ?, ?, ?, ?, ?);
    """, camas)

    # 2. Cartera por EPS (Valores en Millones de COP expresados en números completos)
    # Nueva EPS: Mayor de 90 días = $2.480.000.000 (91-180: 1.150M + 181-360: 890M + >360: 440M)
    cartera = [
        ("Nueva EPS", "EPS037", "Contributivo y Subsidiado", 850000000, 1420000000, 1150000000, 890000000, 440000000, 4750000000),
        ("Sanitas EPS (En Intervención)", "EPS005", "Contributivo", 420000000, 780000000, 620000000, 310000000, 190000000, 2320000000),
        ("Coosalud EPS", "ESS024", "Subsidiado", 310000000, 520000000, 430000000, 280000000, 120000000, 1660000000),
        ("Savia Salud EPS (En Intervención)", "ESS118", "Subsidiado", 210000000, 390000000, 340000000, 260000000, 180000000, 1380000000),
        ("Salud Total EPS", "EPS002", "Contributivo", 380000000, 410000000, 210000000, 95000000, 45000000, 1140000000),
        ("Asmet Salud EPS (En Liquidación)", "ESS062", "Subsidiado", 0, 45000000, 110000000, 290000000, 680000000, 1125000000),
        ("Fondo ADRES (Giro Directo / SOAT sin póliza)", "ADRES01", "Público", 650000000, 320000000, 180000000, 90000000, 30000000, 1270000000)
    ]
    cursor.executemany("""
    INSERT INTO cartera_eps (eps_nombre, codigo_eps, regimen, corriente, dias_31_90, dias_91_180, dias_181_360, mayor_360, total_cartera)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, cartera)

    # 3. Glosas de Facturación (Mes en curso)
    glosas = [
        ("RAD-2026-0891", "Nueva EPS", "GL-01 Pertinencia Médica", "Estancia en UCI Adultos objetada por falta de registro de escala APACHE II al ingreso", 185000000, 62000000, "2026-09-25", 8, "Pendiente Respuesta"),
        ("RAD-2026-0892", "Nueva EPS", "GL-02 Soporte Incompleto", "Falta firma digital en orden médica de tomografía computarizada", 42000000, 14500000, "2026-09-28", 11, "Pendiente Respuesta"),
        ("RAD-2026-0904", "Sanitas EPS", "GL-03 Tarifas y Manuales", "Divergencia entre manual tarifario SOAT 2026 pactado en nota técnica vs liquidación", 95000000, 28000000, "2026-10-02", 15, "Pendiente Respuesta"),
        ("RAD-2026-0915", "Coosalud EPS", "GL-01 Pertinencia Médica", "Procedimiento quirúrgico de osteosíntesis sin autorización previa expresa de la ERP", 78000000, 41000000, "2026-09-22", 5, "Pendiente Respuesta"),
        ("RAD-2026-0920", "Nueva EPS", "GL-04 Medicamentos No PBS", "Soporte de fórmula MIPRES sin diligenciamiento de junta médica previa", 63000000, 31000000, "2026-09-30", 13, "Pendiente Respuesta"),
        ("RAD-2026-0840", "Salud Total EPS", "GL-02 Soporte Incompleto", "Falta epicrisis hospitalaria escaneada en formato interoperable RIPS", 34000000, 8500000, "2026-09-15", 0, "Conciliada")
    ]
    cursor.executemany("""
    INSERT INTO glosas_facturacion (numero_radicado, eps_nombre, codigo_glosa, concepto_glosa, valor_facturado, valor_glosado, fecha_notificacion, dias_habiles_respuesta, estado_glosa)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, glosas)

    # 4. Equipos Biomédicos y Metrología (Res. 3100 Estándar Dotación)
    # Incluye los 5 desfibriladores de Urgencias que vencen en 15 días y 1 ventilador en 7 días
    equipos = [
        ("BIO-DF-01", "Desfibrilador Bifásico con Marcapasos Externo", "Mindray BeneHeart D3", "Urgencias Sala Reanimación", "2025-10-27", "2026-10-27", 15, "Operativo", "Clase IIb"),
        ("BIO-DF-02", "Desfibrilador Bifásico con Marcapasos Externo", "Mindray BeneHeart D3", "Urgencias Trauma Shock", "2025-10-27", "2026-10-27", 15, "Operativo", "Clase IIb"),
        ("BIO-DF-03", "Desfibrilador Bifásico con Marcapasos Externo", "Philips HeartStart XL+", "Urgencias Observación Hombres", "2025-10-27", "2026-10-27", 15, "Operativo", "Clase IIb"),
        ("BIO-DF-04", "Desfibrilador Bifásico con Marcapasos Externo", "Philips HeartStart XL+", "Urgencias Observación Mujeres", "2025-10-27", "2026-10-27", 15, "Operativo", "Clase IIb"),
        ("BIO-DF-05", "Desfibrilador Bifásico con Marcapasos Externo", "Zoll R Series Plus", "Urgencias Triage / Procedimientos", "2025-10-27", "2026-10-27", 15, "Operativo", "Clase IIb"),
        ("BIO-VM-04", "Ventilador Mecánico Neonatal de Alta Frecuencia", "Dräger Babylog VN500", "UCI Neonatal Cuna 3", "2025-10-19", "2026-10-19", 7, "Operativo", "Clase III"),
        ("BIO-VM-01", "Ventilador Mecánico Adultos", "Hamilton-C3", "UCI Adultos Cama 1", "2026-03-10", "2027-03-10", 149, "Operativo", "Clase III"),
        ("BIO-BI-12", "Bomba de Infusión Volumétrica", "B. Braun Infusomat Space", "Urgencias Adultos", "2026-04-05", "2027-04-05", 175, "Operativo", "Clase IIb"),
        ("BIO-MS-08", "Monitor de Signos Vitales Multiparamétrico", "Edan iM80", "Quirófano 1", "2026-02-14", "2027-02-14", 125, "Operativo", "Clase IIb"),
        ("BIO-MQ-02", "Máquina de Anestesia con Vaporizador", "Datex Ohmeda Aespire", "Quirófano 2", "2025-11-05", "2026-11-05", 24, "Mantenimiento Preventivo", "Clase III")
    ]
    cursor.executemany("""
    INSERT INTO equipos_biomedicos (codigo_activo, nombre_equipo, marca_modelo, servicio_ubicacion, fecha_ultima_calibracion, fecha_vencimiento_calibracion, dias_para_vencer, estado_operativo, clasificacion_riesgo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, equipos)

    # 5. Talento Humano y ReTHUS (Res. 3100)
    # Incluye los 3 médicos con ReTHUS por renovar y pólizas
    talento = [
        ("TH-2011", "Médico General Urgencias", "Urgencias Adultos", "Por Renovar", "2026-10-25", "Vencida", -2, "Contrato Prestación de Servicios"),
        ("TH-2015", "Médico General Urgencias", "Urgencias Adultos", "Por Renovar", "2026-10-28", "Vigente", 16, "Contrato Prestación de Servicios"),
        ("TH-2044", "Médico Especialista Pediatría", "Urgencias Pediátricas", "Por Renovar", "2026-10-30", "Vigente", 18, "Planta Permanente"),
        ("TH-1082", "Médico Especialista Neonatología", "UCI Neonatal", "Vigente", "2028-04-15", "Vigente", 180, "Planta Permanente"),
        ("TH-1090", "Médico Especialista Cuidados Intensivos", "UCI Adultos", "Vigente", "2027-11-12", "Vigente", 240, "Planta Permanente"),
        ("TH-3051", "Enfermera Jefe Coordinadora UCI", "UCI Adultos", "Vigente", "2027-08-20", "Vigente", 310, "Planta Permanente"),
        ("TH-3092", "Enfermera Jefe Asistencial", "Urgencias Adultos", "Vigente", "2028-01-10", "Vigente", 120, "Planta Permanente"),
        ("TH-4011", "Químico Farmacéutico", "Farmacia Central Hospitalaria", "Vigente", "2029-05-18", "Vigente", 400, "Planta Permanente")
    ]
    cursor.executemany("""
    INSERT INTO talento_humano (id_personal_anonimizado, perfil_profesional, servicio_asignado, registro_rethus_estado, fecha_vencimiento_rethus, poliza_responsabilidad_medica, dias_vencimiento_poliza, tipo_vinculacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, talento)

    # 6. Presupuesto ESE (En pesos colombianos)
    # Material Médico-Quirúrgico al 91.8% de ejecución (Alerta de agotamiento presupuestal)
    presupuesto = [
        ("RUB-201", "Material Médico-Quirúrgico e Insumos Hospitalarios", 1800000000, 1850000000, 1698300000, 1540000000, 151700000, 91.8),
        ("RUB-202", "Medicamentos Esenciales y Sueros", 2400000000, 2400000000, 2040000000, 1880000000, 360000000, 85.0),
        ("RUB-203", "Suministro de Oxígeno Medicinal y Gases", 650000000, 720000000, 560000000, 510000000, 160000000, 77.8),
        ("RUB-204", "Mantenimiento Preventivo y Metrología Biomédica", 420000000, 420000000, 310000000, 275000000, 110000000, 73.8),
        ("RUB-101", "Servicios Personales de Planta (Nómina Asistencial/Admin)", 7800000000, 7800000000, 6100000000, 5950000000, 1700000000, 78.2),
        ("RUB-305", "Servicios de Alimentación y Nutrición de Pacientes", 580000000, 580000000, 440000000, 410000000, 140000000, 75.9)
    ]
    cursor.executemany("""
    INSERT INTO presupuesto_rubros (codigo_rubro, nombre_rubro, apropiacion_inicial, apropiacion_vigente, comprometido, ejecutado_giro, saldo_disponible, porcentaje_ejecucion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, presupuesto)

    # 7. Inventario Farmacia e Insumos Vitales
    farmacia = [
        ("CUM-0012-1", "Adrenalina (Epinefrina) 1mg/1ml Ampolla", "Solución Inyectable", 1, 18, 50, 2, "Riesgo Desabastecimiento Crítico"),
        ("CUM-0034-2", "Catéter Venoso Central Trilumen Pediátrico 4 Fr", "Dispositivo Médico", 1, 4, 15, 3, "Riesgo Desabastecimiento Crítico"),
        ("CUM-0045-8", "Tubo Endotraqueal con Neumotaponador No. 7.5", "Dispositivo Médico", 0, 12, 30, 4, "Alerta Temprana"),
        ("CUM-0089-3", "Norepinefrina 4mg/4ml Ampolla", "Solución Inyectable", 1, 65, 40, 14, "Normal"),
        ("CUM-0112-9", "Lactato de Ringer Bolsa 500ml", "Solución Parenteral", 0, 420, 150, 18, "Normal"),
        ("CUM-0220-4", "Fentanilo 0.5mg/10ml Ampolla", "Solución Inyectable", 1, 85, 30, 22, "Normal"),
        ("CUM-0315-7", "Meropenem 1g Polvo para Inyección", "Polvo Liofilizado", 0, 110, 35, 16, "Normal")
    ]
    cursor.executemany("""
    INSERT INTO inventario_farmacia (codigo_cum, nombre_medicamento, forma_farmaceutica, es_vital_no_disponible, stock_actual, stock_minimo_seguridad, dias_autonomia_consumo, estado_alerta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, farmacia)

    conn.commit()
    conn.close()
    print("Base de datos de Hospital San Rafael E.S.E. poblada exitosamente con datos representativos.")

if __name__ == "__main__":
    seed_database()
