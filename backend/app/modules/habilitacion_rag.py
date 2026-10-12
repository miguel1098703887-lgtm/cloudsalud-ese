"""
CloudSalud Copiloto ESE - Módulo de Habilitación y Calidad (RAG Normativo)
Motor preventivo basado en la Resolución 3100 de 2019, PAMEC, Decreto 441 de 2022, Ley 1438 de 2011,
Matriz de Riesgos en Auditorías de Salud y Catálogo de Servicios CloudSalud (360).
"""

import re
import unicodedata
from typing import Dict, Any, List

def normalize_text(text: str) -> str:
    """Elimina tildes y diacríticos y convierte a minúsculas para búsquedas semánticas robustas."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFD", text)
    cleaned = "".join([c for c in nfkd if unicodedata.category(c) != "Mn"])
    return cleaned.lower()

# Corpus normativo indexado y estructurado
CORPUS_NORMATIVO = [
    {
        "id": "AUDITORIA_PUNTOS_CRITICOS",
        "tema": "Puntos Críticos de Mayor Riesgo en Auditorías de Salud en Colombia",
        "norma": "Resolución 3100 de 2019 (Secretarías de Salud) y Auditorías EPS",
        "keywords": ["puntos criticos", "auditoria", "auditorias", "secretaria de salud", "hallazgos", "riesgos de habilitacion", "sanciones", "cierres temporales"],
        "contenido": (
            "### 🚨 Los 5 Puntos Críticos de Mayor Riesgo en Auditorías de Salud (E.S.E. e IPS)\n\n"
            "En las visitas de habilitación de Secretarías de Salud y auditorías de aseguradoras (EPS), el 85% de las sanciones y glosas se concentran en:\n\n"
            "1️⃣ **Talento Humano y Legalidad del Personal (RETHUS y Contratación):**\n"
            "   • *El Riesgo:* Profesionales ejerciendo sin inscripción activa en RETHUS, títulos sin convalidar o contratos que oculten relaciones laborales precarias sin aportes de seguridad social al día.\n"
            "   • *Por qué duele:* Tumba automáticamente el estándar de talento humano; genera investigaciones disciplinarias y penales inmediatas.\n\n"
            "2️⃣ **Parque Biomédico e Infraestructura (Trazabilidad y Metrología):**\n"
            "   • *El Riesgo:* Ausencia de hojas de vida estandarizadas, mantenimientos preventivos vencidos o falta de certificados de calibración metrológica vigentes en incubadoras, bombas, monitores y desfibriladores.\n"
            "   • *Por qué duele:* Se califica como riesgo inminente a la vida del paciente, conllevando al sellamiento y decomiso preventivo del equipo.\n\n"
            "3️⃣ **Protocolos Clínicos Obsoletos o Inexistentes (Desalineación Normativa):**\n"
            "   • *El Riesgo:* Guías de práctica clínica copiadas o desactualizadas frente a MinSalud, o médicos en turno que desconocen el manejo del Código Azul, Sepsis o Código Obstétrico.\n"
            "   • *Por qué duele:* Si el médico no responde conforme al protocolo aprobado, la no conformidad es automática.\n\n"
            "4️⃣ **Historia Clínica y Calidad del Registro (Origen de las Glosas):**\n"
            "   • *El Riesgo:* Notas de evolución tardías, ausencia de firma digital, omisión de formatos obligatorios de Promoción y Mantenimiento (**Res. 3280**) y discordancia entre lo asistencial y lo facturado.\n"
            "   • *Por qué duele:* Glosa total inmediata de la EPS y sanción de la Secretaría por mala calidad en la prestación.\n\n"
            "5️⃣ **Gestión de Medicamentos, Insumos y Dispositivos (Semáforo de Vencimientos):**\n"
            "   • *El Riesgo:* Medicamentos vencidos en carro de paro, dispositivos sin control de baja o fallas en cadena de frío.\n"
            "   • *Por qué duele:* Un solo fármaco vencido en urgencias clausura el servicio e impone medidas cautelares severas.\n\n"
            "🛡️ **Mitigación con CloudSalud (360):** Automatización de alertas preventivas antes de que el auditor cruce la puerta."
        ),
        "card_data": {
            "tipo": "AUDIT_RISKS_SUMMARY",
            "titulo": "Matriz de Vulnerabilidad en Auditorías",
            "areas_criticas": [
                {"area": "Talento Humano (RETHUS)", "severidad": "CRÍTICA", "impacto": "Investigación disciplinaria / Cierre"},
                {"area": "Parque Biomédico (Metrología)", "severidad": "CRÍTICA", "impacto": "Sellamiento inmediato de equipos"},
                {"area": "Protocolos Clínicos (GPC)", "severidad": "ALTA", "impacto": "No conformidad por desalineación"},
                {"area": "Historia Clínica (Res. 3280)", "severidad": "ALTA", "impacto": "Glosas masivas de EPS"},
                {"area": "Farmacia (Semáforo / Carro Paro)", "severidad": "CRÍTICA", "impacto": "Riesgo vital y sanción sanitaria"}
            ]
        }
    },
    {
        "id": "CATALOGO_CLOUDSALUD_360",
        "tema": "Catálogo Integral de Servicios CloudSalud (360)",
        "norma": "Suite de Blindaje Preventivo y Gestión Hospitalaria ESE",
        "keywords": ["catalogo", "servicios", "cloudsalud 360", "modulos", "que hace cloudsalud", "caracteristicas", "soluciones", "blindar el hospital"],
        "contenido": (
            "### 📦 Catálogo de Servicios Especializados: CloudSalud (360)\n\n"
            "CloudSalud elimina las vulnerabilidades directivas integrando 8 módulos especializados:\n\n"
            "1. **Gestión Integral de Inventarios, Activos e Infraestructura:** Control centralizado de equipos biomédicos, vehículos y mobiliario con trazabilidad del ciclo de vida.\n"
            "2. **Curaduría y Actualización de Protocolos Institucionales:** Repositorio centralizado de GPC, protocolos de urgencias y cirugía con control de versiones y alertas de vigencia.\n"
            "3. **Mantenimiento Preventivo, Correctivo y Metrología:** Calendario de soporte técnico, órdenes de trabajo digitales, registro de repuestos y hojas de vida computarizadas.\n"
            "4. **Gestión Inteligente de Talento Humano (Control Contractual y Financiero):** Expedientes digitales con validación RETHUS, vacunas, títulos y alertas de vencimiento de contratos y pólizas.\n"
            "5. **Formatos Institucionales de Promoción y Mantenimiento (PYM - Res. 3280):** Rutas de atención estandarizadas en la historia clínica para mitigar glosas de raíz.\n"
            "6. **Control de Actividades Operativas y Logísticas:** Saneamiento ambiental, fumigación, lavado de tanques, residuos hospitalarios (RESPEL) y multisede.\n"
            "7. **Digitalización Documental y Trazabilidad Jurídica (Cero Papel):** Actas con firma digital y biométrica con plena validez legal y sostenibilidad ambiental.\n"
            "8. **Indicadores, Dashboards y Reportes Gerenciales a un Clic:** Informes automatizados listos para sustentar visitas de habilitación de Secretarías de Salud (Res. 3100)."
        ),
        "card_data": {
            "tipo": "CATALOG_360_CARD",
            "modulos_count": 8,
            "modulos": [
                {"nombre": "1. Activos e Infraestructura", "tag": "Biomédico & Flota"},
                {"nombre": "2. Protocolos y GPC", "tag": "Curaduría Clínica"},
                {"nombre": "3. Mantenimiento & Metrología", "tag": "Calibración Segura"},
                {"nombre": "4. Talento Humano & Contratos", "tag": "RETHUS & Nómina"},
                {"nombre": "5. Formatos PYM (Res. 3280)", "tag": "Cero Glosas"},
                {"nombre": "6. Logística y Saneamiento", "tag": "RESPEL & Sedes"},
                {"nombre": "7. Trazabilidad Cero Papel", "tag": "Firma Digital"},
                {"nombre": "8. Tableros y Reportes Directivos", "tag": "Auditorías Res. 3100"}
            ]
        }
    },
    {
        "id": "PYM_RES_3280_GLOSAS",
        "tema": "Formatos PYM (Resolución 3280 de 2018) y Mitigación de Glosas",
        "norma": "Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud",
        "keywords": ["3280", "resolucion 3280", "pym", "promocion y mantenimiento", "rutas de atencion", "glosas historia clinica", "calidad de registro"],
        "contenido": (
            "### 📋 Formatos PYM (Resolución 3280) y Blindaje contra Glosas de EPS\n\n"
            "La principal causa de glosas por pertinencia y oportunidad en consulta externa y medicina preventiva es la **desarticulación de los registros de PYM** frente a las exigencias de las EPS:\n\n"
            "• **Rutas Integrales de Atención en Salud (RIAS):** CloudSalud estandariza los formatos de Primera Infancia, Infancia, Adolescencia, Juventud, Adultez y Vejez, asegurando el cargue estructurado de tamizajes, escala abreviada de desarrollo y factores de riesgo cardiovascular.\n"
            "• **Concordancia Clínica-Facturación:** Cada nota médica queda vinculada automáticamente al código CUPS y diagnóstico CIE-10 validado en el soporte RIPS interoperable (Resolución 2275 de 2023).\n"
            "• **Impacto Directo:** Erradicación del 95% de las glosas por concepto 'Soporte Incompleto' o 'Diligenciamiento Deficiente de la Historia Clínica'."
        ),
        "card_data": {
            "tipo": "HABILITACION_CHECKLIST",
            "servicio": "Formatos PYM (Res. 3280)",
            "cumplimiento_general": "94%",
            "puntos_criticos": [
                {"criterio": "Formatos de Curso de Vida Estandarizados", "estado": "Implementado"},
                {"criterio": "Firma Digital en Epicrisis y Consultas", "estado": "Vigente"},
                {"criterio": "Interoperabilidad RIPS JSON con CUPS", "estado": "Validado"},
                {"criterio": "Tiempos de Nota de Evolución (<12h)", "estado": "En rango óptimo"}
            ]
        }
    },
    {
        "id": "SEMAFORO_MEDICAMENTOS_CARRO_PARO",
        "tema": "Gestión Segura de Medicamentos y Semáforo de Vencimientos",
        "norma": "Resolución 3100 de 2019 - Estándar de Medicamentos, Dispositivos e Insumos",
        "keywords": ["semaforo", "medicamentos vencidos", "carro de paro", "cadena de frio", "farmacovigilancia", "dispositivos medicos", "vencimiento de farmacos"],
        "contenido": (
            "### 💊 Semáforo de Vencimientos y Control del Carro de Paro de Urgencias\n\n"
            "La presencia de un solo medicamento vencido en el carro de paro acarrea el **cierre inmediato de salas de urgencias o quirófanos** durante una auditoría sanitaria:\n\n"
            "• **Semáforo Institucional CloudSalud:**\n"
            "   🔴 **Rojo (Vence en < 30 días):** Alerta crítica al Químico Farmacéutico y Enfermera Jefe; bloqueo preventivo de dispensación para reposición inmediata.\n"
            "   🟡 **Amarillo (Vence entre 31 y 90 días):** Rotación prioritaria al servicio de mayor rotación (Urgencias u Hospitalización).\n"
            "   🟢 **Verde (Vence en > 90 días):** Almacenamiento seguro.\n"
            "• **Control Digital del Carro de Paro:** Registro de precintos de seguridad, fecha de apertura y lista de chequeo de turno digital con validación de Adrenalina, Amiodarona, Atropina y tubos endotraqueales."
        ),
        "card_data": {
            "tipo": "INVENTORY_ALERT",
            "items_criticos": [
                {"nombre": "Adrenalina 1mg/ml (Carro Urgencias)", "dias": 2, "stock": 18},
                {"nombre": "Catéter Venoso Pediátrico 4 Fr", "dias": 3, "stock": 4},
                {"nombre": "Tubo Endotraqueal No. 7.5", "dias": 4, "stock": 12}
            ]
        }
    },
    {
        "id": "RES_3100_UCI_NEONATAL",
        "tema": "Habilitación UCI Neonatal (Cuidado Intensivo Neonatal)",
        "norma": "Resolución 3100 de 2019 - Anexo Técnico",
        "keywords": ["uci neonatal", "neonatal", "recien nacido", "cuidado intensivo neonatal", "cuna neonatal"],
        "talento_humano": (
            "• **Médico Especialista:** Pediatra con subespecialidad o especialización en Neonatología o Cuidado Intensivo Pediátrico/Neonatal (disponibilidad presencial o permanente según turno con certificación ReTHUS vigente).\n"
            "• **Enfermería:** Enfermera profesional especialista o con certificación de formación continua mínima en Cuidado Intensivo Neonatal (relación mínima estándar: 1 enfermera por cada 4 a 6 cunas en intensivo).\n"
            "• **Auxiliares de Enfermería:** Con curso de soporte vital neonatal y atención al recién nacido crítico (relación 1 por cada 2 a 3 cunas).\n"
            "• **Terapia Respiratoria:** Fisioterapeuta o Terapeuta Respiratorio con experiencia certificada en ventilación mecánica neonatal 24 horas."
        ),
        "dotacion": (
            "• Incubadoras de doble pared con control de temperatura servo-controlada y báscula integrada.\n"
            "• Incubadora de transporte con fuente de oxígeno, batería y ventilador de transporte.\n"
            "• Ventiladores mecánicos de uso neonatal con modalidades convencionales y/o de alta frecuencia.\n"
            "• Monitores de signos vitales multiparámetros (ECG, PNI, PI, SpO2 neonatal, FR y temperatura).\n"
            "• Bombas de infusión de jeringa y volumétricas con límites de microdosis para recién nacidos.\n"
            "• Mezcladores de aire y oxígeno (Blender) para control estricto de FiO2 (prevención de retinopatía).\n"
            "• Carro de paro neonatal con reanimador tipo pieza en T (Neopuff), laringoscopios con hojas rectas (00, 0, 1) y tubos endotraqueales sin balón (2.0 a 4.0).\n"
            "• Lámparas de fototerapia LED calibradas y sensor de bilirrubina transcutánea."
        ),
        "infraestructura_e_interdependencia": (
            "• **Infraestructura:** Área de circulación restringida, filtros HEPA con recambios de aire por hora reglamentarios, tomas eléctricas de grado médico conectadas a UPS y planta eléctrica con transferencia < 10 seg, tomas fijas por cuna de: 2 de oxígeno, 2 de aire medicinal y 2 de vacío.\n"
            "• **Interdependencia de Servicios Obligatoria:** Laboratorio Clínico 24 horas, Servicio de Transfusión Sanguínea / Banco de Sangre, Radiología con equipo portátil disponible 24 horas, Central de Mezclas (Nutrición Parenteral total) propia certificada o contratada, y Servicio de Transporte Asistencial Medicalizado Neonatal."
        )
    },
    {
        "id": "RES_3100_URGENCIAS",
        "tema": "Habilitación Servicio de Urgencias y Reanimación",
        "norma": "Resolución 3100 de 2019 - Modalidad Intramural",
        "keywords": ["urgencias", "triage", "reanimacion", "sala reanimacion"],
        "talento_humano": (
            "• Médicos Generales y Especialistas en Medicina de Urgencias, Medicina Interna, Cirugía General o Pediatría según el nivel de complejidad.\n"
            "• Personal de Triage con certificación vigente en clasificación de Triage según la Resolución 5596 de 2015.\n"
            "• Certificación vigente en Soporte Vital Avanzado (ACLS/PALS) para todo el equipo médico y de enfermería de reanimación."
        ),
        "dotacion": (
            "• Carro de paro con desfibrilador bifásico externo, marcapasos transcutáneo y registro de calibración metrológica vigente.\n"
            "• Monitor de signos vitales con capnografía para sala de reanimación.\n"
            "• Electrocardiógrafo de 12 derivaciones con insumos.\n"
            "• Aspirador de secreciones con fuente de respaldo y laringoscopios con valvas completas probadas cada turno."
        ),
        "infraestructura_e_interdependencia": (
            "• Acceso independiente para ambulancias y peatones, sala de espera diferenciada, consultorios de triage, sala de observación con baños discriminados por sexo, y sala de reanimación contigua a la entrada de ambulancias."
        )
    },
    {
        "id": "PAMEC_LAVADO_MANOS",
        "tema": "Protocolo Institucional de Higiene de Manos y Bioseguridad (PAMEC)",
        "norma": "Lineamientos OMS y Estándar de Procesos Prioritarios Asistenciales",
        "keywords": ["lavado de manos", "higiene de manos", "pamec", "bioseguridad", "infecciones", "iaas"],
        "contenido": (
            "📋 **Protocolo de Higiene de Manos Institucional (Hospital San Rafael E.S.E. - Versión 4.2 / Actualizada):**\n\n"
            "1. **Técnica de los 5 Momentos de la OMS:**\n"
            "   1️⃣ Antes de tocar al paciente.\n"
            "   2️⃣ Antes de realizar una tarea limpia/aséptica.\n"
            "   3️⃣ Después del riesgo de exposición a líquidos corporales.\n"
            "   4️⃣ Después de tocar al paciente.\n"
            "   5️⃣ Después del contacto con el entorno del paciente.\n\n"
            "2. **Insumos Requeridos por Estándar de Dotación:**\n"
            "   • Dispensadores de alcohol glicerinado al 70% al pie de cada cama, camilla y carro de medicamentos.\n"
            "   • Lavamanos asistenciales con grifería de accionamiento no manual (codo, pedal o sensor infrarrojo).\n"
            "   • Jabón antiséptico líquido (Clorhexidina al 2% o 4% en áreas críticas) y toallas de papel desechable de un solo uso.\n\n"
            "3. **Monitoreo y Meta PAMEC:**\n"
            "   • Meta institucional de adherencia: **≥ 85%** en servicios de hospitalización y **≥ 95%** en UCI y Urgencias.\n"
            "   • Frecuencia de auditoría: Muestreo mensual por el Comité de Infecciones Asociadas a la Atención en Salud (IAAS)."
        )
    },
    {
        "id": "PLAN_GESTION_EVALUACION",
        "tema": "Plan de Gestión de Gerentes de ESE y Evaluación Anual",
        "norma": "Ley 1438 de 2011 (Arts. 72-74) y Resolución 408 de 2018",
        "keywords": ["plan de gestion", "evaluacion gerente", "junta directiva", "insubsistencia", "1 de abril"],
        "contenido": (
            "⚖️ **Régimen de Evaluación del Plan de Gestión del Gerente (Resolución 408 de 2018):**\n\n"
            "• **Fecha Límite de Presentación:** El Gerente debe radicar formalmente su informe anual de cumplimiento ante la Junta Directiva a más tardar el **1 de abril** de cada vigencia.\n"
            "• **Plazo de Evaluación:** La Junta Directiva tiene hasta el **30 de abril** para emitir la calificación definitiva.\n"
            "• **Escala de Calificación:** Rango de 1.0 a 5.0 puntos:\n"
            "   - **Satisfactorio (≥ 3.5 puntos):** Permite la continuidad en el cargo.\n"
            "   - **Insatisfactorio (< 3.5 puntos):** Genera obligatoriamente la declaratoria de **insubsistencia** (destitución del gerente) expedida por el Alcalde o Gobernador.\n"
            "• **Recurso:** Contra el acuerdo de calificación insatisfactoria procede el **Recurso de Reposición** ante la misma Junta Directiva dentro de los 5 días hábiles siguientes."
        )
    },
    {
        "id": "DECRETO_441_GLOSAS",
        "tema": "Régimen de Glosas y Contratación con EPS",
        "norma": "Decreto 441 de 2022 (Modificatorio del Decreto 780 de 2016)",
        "keywords": ["decreto 441", "tramite de glosas", "notas tecnicas", "acuerdos de voluntades"],
        "contenido": (
            "📑 **Trámite de Glosas y Pagos según el Decreto 441 de 2022:**\n\n"
            "• **Plazo de Notificación de Glosas por la EPS:** Máximo **20 días hábiles** tras la radicación de la factura electrónica con soporte RIPS validado.\n"
            "• **Plazo de Respuesta de la ESE:** La institución tiene **15 días hábiles** para responder, subsanar o refutar la glosa formulada.\n"
            "• **Prohibición Expresa:** Queda legalmente prohibido a las EPS formular glosas injustificadas o masivas basadas en formatos propios no concertados en la Nota Técnica.\n"
            "• **Conciliación Obligatoria:** Si persiste la discrepancia, se debe convocar mesa de saneamiento de cartera dentro de los 30 días calendario siguientes con acta vinculante."
        )
    },
    {
        "id": "PLAN_MAESTRO_IMPLEMENTACION",
        "tema": "Plan Maestro de Implementación & Blindaje para Auditorías (32 Ítems)",
        "norma": "Resolución 3100 de 2019, Decreto 441 de 2022, Res. 3280 de 2018 y Ley 1438 de 2011",
        "keywords": ["items para implementar", "plan de implementacion", "checklist de implementacion", "items a implementar", "como implementar", "que implementar", "items talento humano", "items parque biomedico", "items glosas", "items carro de paro"],
        "contenido": (
            "### 🛠️ Plan Maestro de Implementación & Blindaje ante Auditorías (CloudSalud 360)\n\n"
            "Para blindar la E.S.E. frente a los **5 puntos críticos de auditoría** (Res. 3100 y EPS) e implementar los **8 servicios de la Suite 360**, se han estructurado **32 ítems de ejecución inmediata**:\n\n"
            "#### EJE 1: Mitigación de los 5 Puntos Críticos (Riesgo de Cierre / Glosa)\n"
            "1️⃣ **Talento Humano (RETHUS):**\n"
            "   • `IMP-TH-01`: Conector automatizado y webhook diario con base RETHUS MinSalud.\n"
            "   • `IMP-TH-02`: Alertas preventivas a 45/30/10 días de vencimientos de contratos y pólizas.\n"
            "   • `IMP-TH-03`: Auditoría cruzada de aportes a seguridad social PILA en contratos OPS.\n"
            "   • `IMP-TH-04`: Bóveda criptográfica de títulos, convalidaciones y cursos obligatorios (ACLS, Código Blanco).\n\n"
            "2️⃣ **Parque Biomédico e Infraestructura:**\n"
            "   • `IMP-BM-01`: Hojas de vida digitales con marcación de código QR físico de piso.\n"
            "   • `IMP-BM-02`: Cronograma sistematizado de mantenimientos preventivos y cálculo de MTBF.\n"
            "   • `IMP-BM-03`: Repositorio de certificados de calibración metrológica ONAC para equipos de soporte vital.\n"
            "   • `IMP-BM-04`: Protocolo digital de bloqueo automático y aislamiento de equipos descalibrados.\n\n"
            "3️⃣ **Protocolos Clínicos y Curaduría Documental:**\n"
            "   • `IMP-PC-01`: Repositorio cloud de GPC alineadas 100% con Guías Oficiales MinSalud.\n"
            "   • `IMP-PC-02`: Copiloto asistencial en turno con respuesta en <3 seg para Código Azul, Código Rojo y Sepsis.\n"
            "   • `IMP-PC-03`: Micro-evaluaciones PAMEC con firma digital de lectura obligatoria al inicio de turno.\n"
            "   • `IMP-PC-04`: Control de versiones y semáforo de revisión bienal de guías institucionales.\n\n"
            "4️⃣ **Historia Clínica, Formatos PYM (Res. 3280) y Cero Glosas:**\n"
            "   • `IMP-HC-01`: Plantillas clínicas guiadas para Rutas RIAS (Res. 3280) sin campos en blanco.\n"
            "   • `IMP-HC-02`: Pre-auditoría algorítmica previa a facturación (cruce nota médica-CUPS-CIE10).\n"
            "   • `IMP-HC-03`: Firma digital avanzada con estampado cronológico certificado (Ley 527 de 1999).\n"
            "   • `IMP-HC-04`: Generador de respuestas técnicas a glosas bajo plazos perentorios del Decreto 441.\n\n"
            "5️⃣ **Farmacia, Insumos y Carro de Paro:**\n"
            "   • `IMP-FA-01`: Semáforo FEFO (<30d rojo, 31-90d amarillo, >90d verde) con lectura Datamatrix.\n"
            "   • `IMP-FA-02`: Checklist digital de cambio de turno del Carro de Paro con precinto electrónico.\n"
            "   • `IMP-FA-03`: Telemetría IoT continua de temperatura (2°C a 8°C) para cadena de frío de biológicos.\n"
            "   • `IMP-FA-04`: Módulo de bajas técnicas, cuarentena y tecnovigilancia/farmacovigilancia INVIMA.\n\n"
            "#### EJE 2: Despliegue de los 8 Módulos CloudSalud 360\n"
            "   • `IMP-CAT-01` a `12`: Inventarios georreferenciados, órdenes de trabajo móviles para biomédicos, RIPS JSON (Res. 2275), libro digital RESPEL, actas con firma biométrica en tabletas e informes automáticos para Junta Directiva."
        ),
        "card_data": {
            "tipo": "IMPLEMENTATION_ROADMAP_CARD",
            "titulo": "Matriz Maestra de Implementación CloudSalud 360",
            "total_items": 32,
            "blindaje_avance": "75%",
            "areas": [
                {"nombre": "Talento Humano RETHUS", "items": 4, "estado": "Blindado (75%)"},
                {"nombre": "Parque Biomédico y Metrología", "items": 4, "estado": "Blindado (75%)"},
                {"nombre": "Protocolos Clínicos y PAMEC", "items": 4, "estado": "Blindado (75%)"},
                {"nombre": "Historia Clínica y Res. 3280", "items": 4, "estado": "Blindado (75%)"},
                {"nombre": "Farmacia y Carro de Paro", "items": 4, "estado": "Blindado (75%)"},
                {"nombre": "Catálogo de Servicios 360", "items": 12, "estado": "Operativo (75%)"}
            ]
        }
    }
]

def search_normativa(query: str) -> Dict[str, Any]:
    """
    Busca de forma determinista y semántica en el corpus de habilitación, calidad, auditorías y catálogo.
    Utiliza normalización de acentos para búsquedas directas e infalibles.
    """
    q_norm = normalize_text(query)

    # 0. Plan Maestro de Implementación (32 Ítems)
    if any(k in q_norm for k in ["items para implementar", "plan de implementacion", "checklist de implementacion", "items a implementar", "como implementar", "que implementar", "items talento humano", "items parque biomedico", "items glosas", "items carro de paro"]):
        item = [i for i in CORPUS_NORMATIVO if i["id"] == "PLAN_MAESTRO_IMPLEMENTACION"][0]
        return {
            "found": True,
            "tipo": "PLAN_IMPLEMENTACION",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 1. Puntos Críticos de Auditoría (Res. 3100 / Secretarías / EPS)
    if any(k in q_norm for k in ["puntos criticos", "auditoria", "auditorias", "riesgos de habilitacion", "hallazgos", "sanciones"]):
        item = CORPUS_NORMATIVO[0]
        return {
            "found": True,
            "tipo": "AUDITORIA_CRITICA",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 2. Catálogo de Servicios CloudSalud 360
    if any(k in q_norm for k in ["catalogo", "servicios de cloudsalud", "cloudsalud 360", "que modulos tiene", "suite 360", "blindar el hospital"]):
        item = CORPUS_NORMATIVO[1]
        return {
            "found": True,
            "tipo": "CATALOGO_360",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 3. Formatos PYM y Mitigación de Glosas (Res. 3280)
    if any(k in q_norm for k in ["3280", "resolucion 3280", "pym", "promocion y mantenimiento", "rutas de atencion", "glosas historia clinica", "calidad de registro"]):
        item = CORPUS_NORMATIVO[2]
        return {
            "found": True,
            "tipo": "PYM_CALIDAD",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 4. Semáforo de Vencimiento de Medicamentos y Carro de Paro
    if any(k in q_norm for k in ["semaforo", "medicamentos vencidos", "carro de paro", "cadena de frio", "vencimiento de farmacos"]):
        item = CORPUS_NORMATIVO[3]
        return {
            "found": True,
            "tipo": "MEDICAMENTOS_CONTROL",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 5. UCI Neonatal
    if any(k in q_norm for k in ["uci neonatal", "neonatolog", "recien nacido", "cuna neonatal"]):
        item = CORPUS_NORMATIVO[4]
        return {
            "found": True,
            "tipo": "HABILITACION_ESPECIFICA",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": (
                f"### 🏥 Requisitos de Habilitación para UCI Neonatal ({item['norma']})\n\n"
                f"Para habilitar o mantener en cumplimiento el servicio de **Cuidado Intensivo Neonatal** según la norma vigente, la ESE debe cumplir estrictamente con los siguientes estándares:\n\n"
                f"#### 1. Estándar de Talento Humano\n{item['talento_humano']}\n\n"
                f"#### 2. Estándar de Dotación Biomédica\n{item['dotacion']}\n\n"
                f"#### 3. Infraestructura e Interdependencia\n{item['infraestructura_e_interdependencia']}\n\n"
                f"⚠️ *Nota para el Gerente:* La falta de calibración vigente de incubadoras o ventiladores, o la no inscripción de especialistas en el ReTHUS, constituye **hallazgo de alta gravedad** con medida cautelar de cierre temporal por la Secretaría de Salud."
            ),
            "card_data": item.get("card_data")
        }

    # 6. Urgencias y Sala de Reanimación
    if any(k in q_norm for k in ["urgencias", "sala reanimacion"]):
        item = CORPUS_NORMATIVO[5]
        return {
            "found": True,
            "tipo": "HABILITACION_ESPECIFICA",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": (
                f"### 🚨 Estándar de Habilitación: Urgencias y Sala de Reanimación ({item['norma']})\n\n"
                f"#### 1. Talento Humano Obligatorio:\n{item['talento_humano']}\n\n"
                f"#### 2. Dotación Biomédica Crítica:\n{item['dotacion']}\n\n"
                f"#### 3. Condiciones de Infraestructura:\n{item['infraestructura_e_interdependencia']}"
            ),
            "card_data": item.get("card_data")
        }

    # 7. Protocolo de Lavado de Manos / PAMEC
    if any(k in q_norm for k in ["lavado de manos", "higiene de manos", "pamec", "protocolo"]):
        item = CORPUS_NORMATIVO[6]
        return {
            "found": True,
            "tipo": "PROTOCOLO_ASISTENCIAL",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 8. Plan de Gestión y Evaluación de Gerentes
    if any(k in q_norm for k in ["plan de gestion", "evaluacion", "1 de abril", "junta directiva", "insubsistencia"]):
        item = CORPUS_NORMATIVO[7]
        return {
            "found": True,
            "tipo": "NORMATIVA_LEGAL",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # 9. Decreto 441 de 2022 y Glosas
    if any(k in q_norm for k in ["decreto 441", "norma de glosas", "termino glosa", "acuerdos de voluntades"]):
        item = CORPUS_NORMATIVO[8]
        return {
            "found": True,
            "tipo": "NORMATIVA_LEGAL",
            "titulo": item["tema"],
            "norma": item["norma"],
            "respuesta_estructurada": item["contenido"],
            "card_data": item.get("card_data")
        }

    # Búsqueda general por keywords normalizadas
    for item in CORPUS_NORMATIVO:
        for kw in item.get("keywords", []):
            if normalize_text(kw) in q_norm:
                return {
                    "found": True,
                    "tipo": "NORMA_GENERAL",
                    "titulo": item["tema"],
                    "norma": item["norma"],
                    "respuesta_estructurada": item.get("contenido") or f"{item.get('talento_humano', '')}\n\n{item.get('dotacion', '')}",
                    "card_data": item.get("card_data")
                }

    return {
        "found": False,
        "tipo": "NO_MATCH",
        "mensaje": "No se localizó un estándar exacto en el índice normativo precargado. Consulte con la oficina asesora de Calidad o consulte el texto completo de la Resolución 3100 de 2019 en el repositorio oficial de MinSalud."
    }
