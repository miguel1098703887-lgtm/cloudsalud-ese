"""
CloudSalud Suite 360 - Catálogo Maestro de Items para Implementar
Estructura detallada de 32 ítems técnicos, operativos y regulatorios para blindar a las
E.S.E. e IPS en Colombia ante auditorías de Secretarías de Salud (Res. 3100) y EPS,
así como desplegar los 8 servicios de CloudSalud 360.
"""

from typing import List, Dict, Any

IMPLEMENTATION_ITEMS: List[Dict[str, Any]] = [
    # =========================================================================
    # EJE 1: MITIGACIÓN DE LOS 5 PUNTOS CRÍTICOS EN AUDITORÍAS (Res. 3100 & EPS)
    # =========================================================================
    
    # --- ÁREA 1: Talento Humano y Legalidad del Personal (RETHUS y Contratación) ---
    {
        "id": "IMP-TH-01",
        "codigo": "TH-01",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Talento Humano (RETHUS)",
        "titulo": "Conector Automatizado y Webhook de Validación RETHUS MinSalud",
        "especificacion": "Sincronización diaria automatizada contra el Registro Único Nacional de Talento Humano en Salud (RETHUS). Detecta de inmediato profesionales ejerciendo con tarjeta suspendida o en trámite.",
        "normativa": "Ley 1164 de 2007 (Art. 18) y Resolución 3100 de 2019 (Estándar Talento Humano)",
        "entregable": "Servicio de consulta batch y webhook que bloquea agenda médica si el RETHUS no está activo.",
        "prioridad": "CRÍTICA",
        "impacto": "Evita investigaciones penales/disciplinarias y cierre automático del servicio por ejercicio ilegal.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Qué profesionales asistenciales tienen pendiente o en trámite su inscripción en el ReTHUS?"
    },
    {
        "id": "IMP-TH-02",
        "codigo": "TH-02",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Talento Humano (RETHUS)",
        "titulo": "Motor Proactivo de Vencimientos de Contratos, Pólizas y Carné de Vacunación",
        "especificacion": "Sistema de notificaciones tempranas a 45, 30 y 10 días de vencimiento para contratos asistenciales (OPS/Planta), pólizas de responsabilidad civil médica y esquemas de bioseguridad (Hepatitis B, Tétanos, Varicela).",
        "normativa": "Resolución 3100 de 2019 (Criterios de Habilitación de Personal Asistencial)",
        "entregable": "Tablero semafórico de alertas preventivas y notificaciones push/WhatsApp al líder de Talento Humano.",
        "prioridad": "ALTA",
        "impacto": "Previene hallazgos por personal con pólizas de responsabilidad o contratos vencidos durante turnos.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cuáles son los contratos asistenciales y pólizas que vencen en los próximos 30 días?"
    },
    {
        "id": "IMP-TH-03",
        "codigo": "TH-03",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Talento Humano (RETHUS)",
        "titulo": "Auditoría Cruzada de Planillas PILA (Seguridad Social) para Pagos OPS",
        "especificacion": "Módulo de validación de pago de aportes a salud, pensión y ARL (Riesgo V hospitalario). Bloqueo automático de órdenes de pago a contratistas si no se acredita el pago de PILA del periodo correspondiente.",
        "normativa": "Ley 1438 de 2011 (Formalización laboral y protección social) y Estatuto Anticorrupción",
        "entregable": "Validador algorítmico de soportes PILA previo al desembolso de cuentas de cobro de honorarios.",
        "prioridad": "CRÍTICA",
        "impacto": "Protege a la ESE de demandas laborales por relaciones de trabajo precarias y sanciones de la UGPP.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cómo audita CloudSalud los soportes de seguridad social PILA en contratos de prestación de servicios?"
    },
    {
        "id": "IMP-TH-04",
        "codigo": "TH-04",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Talento Humano (RETHUS)",
        "titulo": "Bóveda Criptográfica y Validación de Convalidación de Títulos Extranjeros",
        "especificacion": "Repositorio cifrado de diplomas, actas de grado y resoluciones de convalidación del Ministerio de Educación Nacional para profesionales extranjeros o con posgrados en el exterior, junto con cursos obligatorios (ACLS, BLS, Res. 459/Violencia Sexual).",
        "normativa": "Decreto 1075 de 2015 y Resolución 3100 de 2019",
        "entregable": "Expediente digital auditado con hash de verificación e indicador de vigencia de cursos mandatarios.",
        "prioridad": "ALTA",
        "impacto": "Blindaje ante sanciones de Secretarías de Salud por títulos no convalidados o cursos asistenciales vencidos.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Qué requisitos de cursos obligatorios de habilitación (ACLS, Código Blanco) exige la Resolución 3100?"
    },

    # --- ÁREA 2: Parque Biomédico e Infraestructura (Trazabilidad y Metrología) ---
    {
        "id": "IMP-BM-01",
        "codigo": "BM-01",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Parque Biomédico",
        "titulo": "Hojas de Vida Biomédicas Digitales con Marcación QR de Piso",
        "especificacion": "Generación digital estandarizada de hojas de vida de equipos médicos bajo formato INVIMA y Res. 3100. Adhesión de sticker físico con código QR dinámico en cada equipo (incubadoras, bombas, monitores, rayos X, desfibriladores).",
        "normativa": "Resolución 3100 de 2019 (Estándar Dotación e Infraestructura) y Decreto 4725 de 2005",
        "entregable": "Plataforma web/móvil que permite al auditor escanear el QR del equipo y ver instantáneamente su historial.",
        "prioridad": "CRÍTICA",
        "impacto": "Elimina el hallazgo por ausencia de 'papel regulatorio' u hojas de vida desactualizadas.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "Muéstrame la hoja de vida biomédica y estado del desfibrilador de Urgencias."
    },
    {
        "id": "IMP-BM-02",
        "codigo": "BM-02",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Parque Biomédico",
        "titulo": "Cronograma Automatizado de Mantenimientos Preventivos y Correctivos",
        "especificacion": "Algoritmo de cálculo de frecuencias de mantenimiento preventivo basado en horas de operación, criticidad clínica y recomendaciones del fabricante, con generación automática de órdenes técnicas.",
        "normativa": "Resolución 3100 de 2019 (Mantenimiento preventivo periódico obligatorio)",
        "entregable": "Módulo de calendario con alertas anticipadas a la Jefatura de Biomédica y Gerencia Hospitalaria.",
        "prioridad": "ALTA",
        "impacto": "Evita paradas imprevistas de servicios críticos (cirugía, urgencias, imagenología) y no conformidades.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cuáles son los mantenimientos biomédicos preventivos programados para este mes?"
    },
    {
        "id": "IMP-BM-03",
        "codigo": "BM-03",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Parque Biomédico",
        "titulo": "Repositorio de Metrología y Certificados de Calibración Acreditados ONAC",
        "especificacion": "Trazabilidad de calibración metrológica realizada por laboratorios autorizados o con patrones trazables a ONAC. Almacenamiento digital de curvas de calibración e incertidumbres.",
        "normativa": "Resolución 3100 de 2019 y Guía Rápida de Metrología Biomédica MinSalud",
        "entregable": "Repositorio con cálculo automático de días restantes de validez y alertas semafóricas antes de 30 días.",
        "prioridad": "CRÍTICA",
        "impacto": "Evita el sellamiento inmediato y decomiso preventivo de equipos de soporte vital por falta de calibración.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Qué desfibriladores y monitores de signos vitales tienen calibración metrológica próxima a vencer?"
    },
    {
        "id": "IMP-BM-04",
        "codigo": "BM-04",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Parque Biomédico",
        "titulo": "Protocolo Digital de Sellamiento Preventivo y Bloqueo de Disponibilidad",
        "especificacion": "Cuando un equipo biomédico supera la fecha límite de calibración o presenta falla metrológica, el software lo marca automáticamente como 'NO CONFORME / FUERA DE SERVICIO' bloqueando su asignación asistencial.",
        "normativa": "Resolución 3100 de 2019 (Seguridad del Paciente y Dotación)",
        "entregable": "Módulo de cuarentena biomédica digital con registro de aislamiento físico de equipo.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza que ningún paciente sea atendido con un equipo descalibrado, salvando vidas y responsabilidad legal.",
        "estado": "En Curso",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cómo opera el bloqueo preventivo de equipos biomédicos sin calibración vigente?"
    },

    # --- ÁREA 3: Protocolos Clínicos Obsoletos o Inexistentes (Desalineación Normativa) ---
    {
        "id": "IMP-PC-01",
        "codigo": "PC-01",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Protocolos Clínicos",
        "titulo": "Curaduría y Repositorio Cloud de Guías de Práctica Clínica (GPC)",
        "especificacion": "Estandarización y depuración de guías institucionales copiadas o caducas. Adopción formal de las Guías de Práctica Clínica vigentes avaladas por el Ministerio de Salud y Protección Social.",
        "normativa": "Resolución 3100 de 2019 (Procesos Prioritarios Asistenciales) y Guía Metodológica MinSalud",
        "entregable": "Repositorio cloud indexado semánticamente con firmas de adopción formal por Comité Técnico Científico.",
        "prioridad": "ALTA",
        "impacto": "Blindaje frente al hallazgo de 'guías desactualizadas' o discordantes con la evidencia científica nacional.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "Muéstrame el protocolo de lavado de manos actualizado para enviarlo a la auditoría."
    },
    {
        "id": "IMP-PC-02",
        "codigo": "PC-02",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Protocolos Clínicos",
        "titulo": "Copiloto Clínico en Turno para Respuestas Inmediatas (< 3 Segundos)",
        "especificacion": "Módulo de consulta rápida en terminal o móvil para el médico en turno, estructurado para responder al instante la conducta exacta ante Código Azul (Reanimación), Código Rojo/Obstétrico (Hemorragia) y Código Sepsis.",
        "normativa": "Resolución 3100 de 2019 (Capacitación y Adherencia del Personal en Turno)",
        "entregable": "Motor de búsqueda con diagramas de flujo interactivos y dosificación de fármacos de reanimación.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza que cuando el auditor interrogue al médico de turno, este responda con exactitud el protocolo aprobado.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cuál es el protocolo institucional para manejo de Código Rojo Obstétrico en urgencias?"
    },
    {
        "id": "IMP-PC-03",
        "codigo": "PC-03",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Protocolos Clínicos",
        "titulo": "Micro-evaluaciones y Monitoreo de Adherencia Clínica (PAMEC)",
        "especificacion": "Sistema de micro-quizzes de 3 preguntas al inicio de turnos asistenciales para medir conocimiento del personal sobre protocolos de seguridad del paciente, eventos adversos y bioseguridad, con certificación de lectura.",
        "normativa": "Decreto 780 de 2016 y Lineamientos PAMEC (Programa de Auditoría para el Mejoramiento de la Calidad)",
        "entregable": "Panel de porcentaje de adherencia clínica por servicio con trazabilidad de firma de inducción del personal.",
        "prioridad": "ALTA",
        "impacto": "Sustenta documentalmente ante la Secretaría de Salud el cumplimiento del estándar PAMEC de calidad.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuáles son las metas PAMEC y el nivel de adherencia a protocolos clínicos en el hospital?"
    },
    {
        "id": "IMP-PC-04",
        "codigo": "PC-04",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Protocolos Clínicos",
        "titulo": "Control de Versiones y Alertas de Renovación Bienal de Protocolos",
        "especificacion": "Mecanismo de gobernanza documental con alertas automáticas cuando un protocolo, manual o guía clínica cumple 24 meses sin revisión o cuando MinSalud expide una nueva directriz vinculante.",
        "normativa": "Resolución 3100 de 2019 (Vigencia y Actualización Documental)",
        "entregable": "Historial de versiones con control de cambios, firmas de aprobación de Comité y fecha límite de vigencia.",
        "prioridad": "OPERATIVA",
        "impacto": "Evita la obsolescencia inadvertida de manuales asistenciales y de soporte.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Qué protocolos asistenciales tienen más de 2 años sin actualización en el repositorio?"
    },

    # --- ÁREA 4: Historia Clínica y Calidad del Registro (Origen de las Glosas) ---
    {
        "id": "IMP-HC-01",
        "codigo": "HC-01",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Historia Clínica y Glosas",
        "titulo": "Formatos Estructurados de Rutas de Atención (Resolución 3280 de 2018)",
        "especificacion": "Plantillas clínicas digitales guiadas para Promoción y Mantenimiento de la Salud (PYM) por curso de vida: Primera Infancia, Infancia, Adolescencia, Juventud, Adultez, Vejez y Materno Perinatal, sin permitir campos vacíos.",
        "normativa": "Resolución 3280 de 2018 (Adopción de Lineamientos RIAS) y Resolución 839 de 2017",
        "entregable": "Módulos de registro clínico con escalas automáticas (Tanner, Escala Abreviada de Desarrollo, Framingham).",
        "prioridad": "CRÍTICA",
        "impacto": "Elimina el 90% de las glosas de EPS por registros clínicos incompletos en consulta externa y prevención.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cómo mitigar las glosas por calidad de historia clínica mediante formatos PYM de la Resolución 3280?"
    },
    {
        "id": "IMP-HC-02",
        "codigo": "HC-02",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Historia Clínica y Glosas",
        "titulo": "Pre-auditoría Algorítmica Concurrente de Cuentas Médicas",
        "especificacion": "Motor validador que examina la historia clínica antes de facturar a la EPS: valida oportunidad de notas (< 12 horas), concordancia entre CIE-10 y procedimientos CUPS, justificación de estancia y órdenes médicas.",
        "normativa": "Decreto 441 de 2022 (Régimen de Glosas y Devoluciones de Facturación en Salud)",
        "entregable": "Score de riesgo de glosa por factura y reporte previo para corrección por el médico tratante.",
        "prioridad": "CRÍTICA",
        "impacto": "Recupera hasta el 15% del flujo de caja de la ESE al interceptar las causas de glosa antes del radicado.",
        "estado": "Implementado",
        "tiempo_estimado": "3 semanas",
        "copilot_prompt": "Genera un resumen de los motivos principales de glosas y facturas devueltas de este mes."
    },
    {
        "id": "IMP-HC-03",
        "codigo": "HC-03",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Historia Clínica y Glosas",
        "titulo": "Firma Digital Avanzada y Estampado Cronológico Certificado",
        "especificacion": "Implementación de firma digital criptográfica con certificado emitido por entidad acreditada ONAC y sello de tiempo (timestamping), blindando la inmutabilidad de cada evolución médica y epicrisis.",
        "normativa": "Ley 527 de 1999 (Comercio Electrónico y Firmas Digitales) y Resolución 1995 de 1999",
        "entregable": "Módulo de firma con verificación biométrica o token seguro para todo el cuerpo asistencial.",
        "prioridad": "ALTA",
        "impacto": "Plena validez probatoria ante jueces, Supersalud y Secretarías; nulidad de glosas por 'falta de firma'.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Qué validez jurídica y técnica tienen las firmas digitales en historias clínicas según la Ley 527?"
    },
    {
        "id": "IMP-HC-04",
        "codigo": "HC-04",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Historia Clínica y Glosas",
        "titulo": "Motor de Conciliación Automática de Glosas bajo Decreto 441 de 2022",
        "especificacion": "Generador estructurado de respuestas a objeciones de EPS aplicando los plazos perentorios del Decreto 441: cálculo automático de plazos de respuesta, tipificación de causales injustificadas y memoriales de conciliación.",
        "normativa": "Decreto 441 de 2022 y Circular Única de la Superintendencia Nacional de Salud",
        "entregable": "Módulo de gestión de cartera objetada con cronómetro de vencimiento de términos legales de la EPS.",
        "prioridad": "ALTA",
        "impacto": "Acelera el recaudo de cartera mayor a 90 días y evita la caducidad de objeciones frente a las EPS.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿A cuánto asciende la cartera mayor a 90 días con la Nueva EPS y cómo aplicar el Decreto 441?"
    },

    # --- ÁREA 5: Gestión de Medicamentos, Insumos y Dispositivos (Semáforo de Vencimientos) ---
    {
        "id": "IMP-FA-01",
        "codigo": "FA-01",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Farmacia y Carro Paro",
        "titulo": "Semáforo Dinámico FEFO (First Expired, First Out) y Lectura Datamatrix",
        "especificacion": "Control sistematizado de inventarios farmacéuticos: clasificación semafórica automática (Rojo < 30 días, Amarillo 31-90 días, Verde > 90 días) con lectura de código bidimensional Datamatrix en recepción y dispensación.",
        "normativa": "Resolución 3100 de 2019 (Estándar Medicamentos y Dispositivos) y Res. 1403 de 2007",
        "entregable": "Módulo de rotación prioritaria que sugiere transferencias inmediatas de medicamentos a áreas de alto consumo.",
        "prioridad": "CRÍTICA",
        "impacto": "Elimina pérdidas por vencimiento en farmacia y evita decomisos durante visitas de inspección sanitaria.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "Alerta de semáforo de vencimientos en carro de paro y farmacia de urgencias."
    },
    {
        "id": "IMP-FA-02",
        "codigo": "FA-02",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Farmacia y Carro Paro",
        "titulo": "Checklist Digital de Turno del Carro de Paro de Urgencias y Quirófano",
        "especificacion": "Lista de chequeo digital obligatoria por cambio de turno mediante código QR del precinto. Verifica insumos vitales: Adrenalina, Amiodarona, Atropina, laringoscopios, guías de intubación y tubos endotraqueales.",
        "normativa": "Resolución 3100 de 2019 (Dotación y Dotación en Reanimación y Soporte Vital)",
        "entregable": "App móvil de verificación en piso con firma digital de la Enfermera Jefe y precinto electrónico.",
        "prioridad": "CRÍTICA",
        "impacto": "Evita el cierre temporal del servicio de Urgencias por hallar un medicamento vencido en el carro de paro.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cuáles son los medicamentos e insumos obligatorios del carro de paro según la Resolución 3100?"
    },
    {
        "id": "IMP-FA-03",
        "codigo": "FA-03",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Farmacia y Carro Paro",
        "titulo": "Telemetría IoT Continua de Cadena de Frío (2°C a 8°C)",
        "especificacion": "Integración de sensores inalámbricos en refrigeradores de vacunas, insulinas y hemoderivados. Registro continuo sin intervención manual con alertas inmediatas por WhatsApp/SMS ante oscilaciones térmicas.",
        "normativa": "Resolución 3100 de 2019 y Manual de Cadena de Frío PAI (MinSalud)",
        "entregable": "Tablero de temperatura en tiempo real y descarga automática de gráficas termohigrométricas para el auditor.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza la efectividad biológica de vacunas y previene la pérdida patrimonial por descarte de biológicos.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuál es el protocolo de cadena de frío y temperatura exigido para vacunas y biológicos?"
    },
    {
        "id": "IMP-FA-04",
        "codigo": "FA-04",
        "eje": "PUNTOS_CRITICOS",
        "categoria": "Farmacia y Carro Paro",
        "titulo": "Módulo de Bajas Técnicas, Cuarentena y Tecno/Farmacovigilancia INVIMA",
        "especificacion": "Gestión digital de productos averiados, retirados del mercado o con reporte de alerta sanitaria del INVIMA. Generación de actas de desnaturalización ambiental y reportes al Programa Nacional de Farmacovigilancia.",
        "normativa": "Resolución 1403 de 2007 y Decretos de Tecnovigilancia y Farmacovigilancia",
        "entregable": "Módulo de cuarentena virtual que bloquea la dispensación y emite el reporte oficial al INVIMA.",
        "prioridad": "ALTA",
        "impacto": "Cumplimiento estricto del estándar de seguridad en la administración de fármacos y dispositivos médicos.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cómo se gestiona el reporte de tecnovigilancia y farmacovigilancia ante el INVIMA en CloudSalud?"
    },

    # =========================================================================
    # EJE 2: DESPLIEGUE DEL CATÁLOGO DE SERVICIOS CLOUDSALUD 360 (8 Módulos)
    # =========================================================================
    
    # --- MÓDULO 1: Gestión Integral de Inventarios, Activos e Infraestructura ---
    {
        "id": "IMP-CAT-01",
        "codigo": "CAT-01",
        "eje": "CATALOGO_360",
        "categoria": "1. Inventarios y Activos",
        "titulo": "Inventario Físico Georreferenciado y Control de Flota de Ambulancias (TAB/TAM)",
        "especificacion": "Mapeo digital de activos fijos hospitalarios por bloque, piso y consultorio. Bitácora telemática de ambulancias con seguimiento GPS, control de revisiones técnico-mecánicas y habilitación de transporte asistencial.",
        "normativa": "Resolución 3100 de 2019 (Servicio de Transporte Asistencial de Pacientes)",
        "entregable": "Plano digital interactivo con ubicación de equipos y estado de habilitación vehicular.",
        "prioridad": "ALTA",
        "impacto": "Control total del patrimonio de la ESE y respuesta oportuna en traslados asistenciales.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Qué activos biomédicos están registrados en Urgencias y cuál es su estado?"
    },

    # --- MÓDULO 2: Curaduría y Actualización de Protocolos Institucionales ---
    {
        "id": "IMP-CAT-02",
        "codigo": "CAT-02",
        "eje": "CATALOGO_360",
        "categoria": "2. Curaduría Documental",
        "titulo": "Gestor Documental Normativo con Aprobación por Comité y Control de Cambios",
        "especificacion": "Flujo de trabajo para redacción, revisión médica, aprobación por Comité de Calidad y publicación de protocolos clínicos, consentimientos informados y manuales de bioseguridad.",
        "normativa": "Sistema Obligatorio de Garantía de Calidad en Salud (SOGCS) - Decreto 780 de 2016",
        "entregable": "Repositorio con firma electrónica de los miembros del Comité y marcas de agua de estado (Vigente / Obsoleto).",
        "prioridad": "ALTA",
        "impacto": "Garantiza que ningún médico consulte documentos no autorizados institucionalmente.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cómo se tramita la aprobación de un nuevo protocolo asistencial en CloudSalud?"
    },

    # --- MÓDULO 3: Mantenimiento Preventivo, Correctivo y Metrología ---
    {
        "id": "IMP-CAT-03",
        "codigo": "CAT-03",
        "eje": "CATALOGO_360",
        "categoria": "3. Mantenimiento y Metrología",
        "titulo": "Generador Móvil de Órdenes de Trabajo (OT) Biomédicas con Firma de Conformidad",
        "especificacion": "Aplicación para técnicos e ingenieros biomédicos que permite registrar repuestos utilizados, costo de la intervención, adjuntar fotografías de antes/después y captura de firma de recibido por el jefe del servicio.",
        "normativa": "Resolución 3100 de 2019 (Evidencia documental de mantenimiento técnico)",
        "entregable": "Módulo OT móvil con actualización en tiempo real de la hoja de vida del equipo.",
        "prioridad": "ALTA",
        "impacto": "Trazabilidad exacta del gasto de mantenimiento y soporte ante auditorías técnicas.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuáles son las órdenes de trabajo de mantenimiento correctivo abiertas en cirugía?"
    },

    # --- MÓDULO 4: Gestión Inteligente de Talento Humano ---
    {
        "id": "IMP-CAT-04",
        "codigo": "CAT-04",
        "eje": "CATALOGO_360",
        "categoria": "4. Talento Humano Inteligente",
        "titulo": "Matriz de Suficiencia de Personal Asistencial y Planificación de Turnos",
        "especificacion": "Cálculo de ratios normativos de personal médico, enfermería y auxiliares por cama habilitada según complejidad (Urgencias, Hospitalización, UCI). Detección de sobrecarga o déficit en turnos.",
        "normativa": "Resolución 3100 de 2019 (Criterios de Dotación de Talento Humano)",
        "entregable": "Tablero de malla de turnos con semáforo de suficiencia de talento humano en tiempo real.",
        "prioridad": "ALTA",
        "impacto": "Evita sanciones por operar servicios asistenciales con personal insuficiente o sobrecargado.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuál es la relación de enfermeras por cama en el servicio de Urgencias y UCI?"
    },

    # --- MÓDULO 5: Formatos PYM (Res. 3280) para Calidad Asistencial ---
    {
        "id": "IMP-CAT-05",
        "codigo": "CAT-05",
        "eje": "CATALOGO_360",
        "categoria": "5. Formatos PYM Res. 3280",
        "titulo": "Integrador RIPS JSON Interoperable (Resolución 2275 de 2023) con Soportes PYM",
        "especificacion": "Generación del formato estándar RIPS en estructura JSON con validación en el mecanismo único del Ministerio de Salud, ligando automáticamente los soportes clínicos obligatorios de PYM para erradicar devoluciones.",
        "normativa": "Resolución 2275 de 2023 (Adopción de Campos RIPS en estructura JSON) y Res. 3280",
        "entregable": "Validador previo de estructura RIPS JSON con validación cruzada CUPS-CIE10-Valor pactado.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza la radicación exitosa de facturas electrónicas de salud sin reprocesos ni glosas técnicas.",
        "estado": "Implementado",
        "tiempo_estimado": "3 semanas",
        "copilot_prompt": "¿Cómo se valida la generación de RIPS JSON bajo Resolución 2275 en CloudSalud?"
    },

    # --- MÓDULO 6: Control de Actividades Operativas y Logísticas ---
    {
        "id": "IMP-CAT-06",
        "codigo": "CAT-06",
        "eje": "CATALOGO_360",
        "categoria": "6. Logística y Saneamiento",
        "titulo": "Libro Digital RESPEL (Residuos Peligrosos) y Control de Desinfección de Tanques",
        "especificacion": "Registro electrónico del formulario RH1 de generación de residuos biosanitarios, cortopunzantes, anatomopatológicos y químicos. Control de cronogramas de lavado y desinfección de tanques de agua potable y fumigación.",
        "normativa": "Resolución 3100 de 2019 (Estándar Infraestructura y Saneamiento) y Decreto 351 de 2014",
        "entregable": "Libro de registro digital certificado con pesaje diario y manifiestos de transporte ambiental.",
        "prioridad": "ALTA",
        "impacto": "Blindaje ante auditorías ambientales de Secretarías de Salud y Corporaciones Autónomas Regionales (CAR).",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cuál es el estado de saneamiento ambiental y residuos hospitalarios RESPEL en las sedes?"
    },

    # --- MÓDULO 7: Digitalización Documental y Trazabilidad (Cero Papel) ---
    {
        "id": "IMP-CAT-07",
        "codigo": "CAT-07",
        "eje": "CATALOGO_360",
        "categoria": "7. Trazabilidad Cero Papel",
        "titulo": "Captura de Firma Biométrica en Tabletas para Actas de Entrega y Recepción",
        "especificacion": "Digitalización de actas de entrega y recepción de turno médico, inventario de insumos, entrega de dotación a funcionarios y compromisos de comités institucionales con firma en tableta y geolocalización.",
        "normativa": "Ley 527 de 1999 y Directiva Presidencial de Gobierno Digital Cero Papel",
        "entregable": "Generador de actas PDF/A con firma biométrica estampada y código de verificación web.",
        "prioridad": "OPERATIVA",
        "impacto": "Ahorro de costos en papelería, eliminación del extravío de documentos y respaldo probatorio.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cómo funciona el módulo de actas con firma digital y trazabilidad jurídica?"
    },

    # --- MÓDULO 8: Dashboards y Reportes Gerenciales a un Clic ---
    {
        "id": "IMP-CAT-08",
        "codigo": "CAT-08",
        "eje": "CATALOGO_360",
        "categoria": "8. Dashboards y Reportes",
        "titulo": "Generador Automático de Informes para Junta Directiva y Visitas de Habilitación",
        "especificacion": "Consolidación en 1 clic del informe ejecutivo trimestral y anual del Plan de Gestión del Gerente (Res. 408 de 2018), así como del expediente probatorio previo a la visita de Habilitación de la Secretaría de Salud.",
        "normativa": "Resolución 408 de 2018 (Evaluación de Gerentes de ESE) y Resolución 3100 de 2019",
        "entregable": "Dossier ejecutivo en PDF y Excel estructurado según los 7 estándares de habilitación.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza la calificación satisfactoria del Gerente y reduce el tiempo de preparación de auditorías de 3 semanas a 10 minutos.",
        "estado": "Implementado",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "Genera el informe ejecutivo de cumplimiento de estándares para la Junta Directiva."
    },

    # --- COMPONENTES TRANSVERSALES DE INTEGRACIÓN ---
    {
        "id": "IMP-CAT-09",
        "codigo": "CAT-09",
        "eje": "CATALOGO_360",
        "categoria": "6. Logística y Saneamiento",
        "titulo": "Conector Multisede Unificado para Redes Integradas de Salud (Centros y Puestos)",
        "especificacion": "Sincronización de datos entre el hospital sede principal y puestos de salud periféricos/rurales, permitiendo trazabilidad de inventarios biomédicos, fármacos y personal en una única consola gerencial.",
        "normativa": "Ley 1438 de 2011 (Redes Integradas de Servicios de Salud - RISS)",
        "entregable": "Módulo de gestión multisede con balance independiente y consolidado.",
        "prioridad": "ALTA",
        "impacto": "Control integral de sedes descentralizadas que suelen ser las más descuidadas en auditorías.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuál es la ocupación y estado de insumos en los centros de salud periféricos de la red?"
    },
    {
        "id": "IMP-CAT-10",
        "codigo": "CAT-10",
        "eje": "CATALOGO_360",
        "categoria": "4. Talento Humano Inteligente",
        "titulo": "Auditor Financiero de Contratos de Prestación de Servicios vs. Producción Asistencial",
        "especificacion": "Módulo de cruce entre el valor pagado por contratos de prestación de servicios asistenciales y las consultas, cirugías o procedimientos efectivamente registrados en la historia clínica (Rendimiento por Hora Médica).",
        "normativa": "Ley 1438 de 2011 y Estatuto de Contratación de las ESE",
        "entregable": "Tablero de costo-efectividad de personal asistencial y control de desbalance financiero.",
        "prioridad": "ALTA",
        "impacto": "Optimiza el presupuesto de talento humano y previene hallazgos fiscales de la Contraloría.",
        "estado": "En Curso",
        "tiempo_estimado": "2 semanas",
        "copilot_prompt": "¿Cuál es la relación de producción asistencial frente al costo de contratos OPS este mes?"
    },
    {
        "id": "IMP-CAT-11",
        "codigo": "CAT-11",
        "eje": "CATALOGO_360",
        "categoria": "8. Dashboards y Reportes",
        "titulo": "Integración Omnicanal de Notificaciones de Gerencia por WhatsApp Business API",
        "especificacion": "Envío automático de alertas críticas (ocupación > 95%, vencimientos inminentes, insumos agotados) y despacho del Briefing Matutino diario de las 6:30 a.m. al teléfono móvil del Gerente y Subgerentes.",
        "normativa": "Gobierno Digital y Comunicación Estratégica Directiva",
        "entregable": "Bot conversacional oficial con comandos ejecutivos y recepción de notas de voz transcribibles.",
        "prioridad": "ALTA",
        "impacto": "Permite al Gerente tomar decisiones estratégicas al instante mientras recorre las instalaciones o asiste a reuniones.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "Briefing Matutino"
    },
    {
        "id": "IMP-CAT-12",
        "codigo": "CAT-12",
        "eje": "CATALOGO_360",
        "categoria": "8. Dashboards y Reportes",
        "titulo": "Bitácora Inalterable de Auditoría Forense (Contraloría y Supersalud)",
        "especificacion": "Registro inmutable en base de datos con estampado SHA-256 de todas las consultas realizadas en el sistema, modificaciones de datos, descargas de reportes y accesos por rol (RBAC), preparado para peritajes judiciales.",
        "normativa": "Ley 1581 de 2012 (Protección de Datos Personales) y Circular Externa Supersalud",
        "entregable": "Visor de logs auditables con exportación certificada para entes de control fiscal y disciplinario.",
        "prioridad": "CRÍTICA",
        "impacto": "Garantiza la máxima transparencia administrativa y exime a la dirección de responsabilidades indebidas.",
        "estado": "Implementado",
        "tiempo_estimado": "1 semana",
        "copilot_prompt": "¿Cómo garantiza CloudSalud la inalterabilidad de los registros de auditoría forense?"
    }
]

def get_implementation_summary() -> Dict[str, Any]:
    """Calcula estadísticas consolidadas del plan de implementación."""
    total = len(IMPLEMENTATION_ITEMS)
    implementados = sum(1 for item in IMPLEMENTATION_ITEMS if item["estado"] == "Implementado")
    en_curso = sum(1 for item in IMPLEMENTATION_ITEMS if item["estado"] == "En Curso")
    pendientes = sum(1 for item in IMPLEMENTATION_ITEMS if item["estado"] == "Pendiente")
    
    criticos = sum(1 for item in IMPLEMENTATION_ITEMS if item["prioridad"] == "CRÍTICA")
    criticos_blindados = sum(1 for item in IMPLEMENTATION_ITEMS if item["prioridad"] == "CRÍTICA" and item["estado"] == "Implementado")

    porcentaje_avance = round((implementados / total) * 100, 1) if total > 0 else 0
    porcentaje_blindaje_critico = round((criticos_blindados / criticos) * 100, 1) if criticos > 0 else 0

    return {
        "total_items": total,
        "implementados": implementados,
        "en_curso": en_curso,
        "pendientes": pendientes,
        "porcentaje_avance": porcentaje_avance,
        "total_criticos": criticos,
        "criticos_blindados": criticos_blindados,
        "porcentaje_blindaje_critico": porcentaje_blindaje_critico,
        "puntos_criticos_count": sum(1 for item in IMPLEMENTATION_ITEMS if item["eje"] == "PUNTOS_CRITICOS"),
        "catalogo_360_count": sum(1 for item in IMPLEMENTATION_ITEMS if item["eje"] == "CATALOGO_360")
    }
