-- ============================================================================
-- CLOUDSALUD 360 - ESQUEMA DE BASE DE DATOS RELACIONAL EN POSTGRESQL (v15+)
-- Normativa: Resolución 3100/2019 (Habilitación MinSalud), Decreto 4725/2005 (INVIMA),
-- Decreto 441/2022 (Glosas EPS), Ley 1474/2011 (Anticorrupción), Ley 1581/2012 (Habeas Data)
-- ============================================================================

-- Extensión para generación de UUIDs y funciones criptográficas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Creación de esquemas lógicos organizacionales
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS activos;
CREATE SCHEMA IF NOT EXISTS talento_humano;
CREATE SCHEMA IF NOT EXISTS modulos;
CREATE SCHEMA IF NOT EXISTS auditoria;

-- ============================================================================
-- 1. TIPOS ENUMERADOS (ENUMS) DEL NEGOCIO HOSPITALARIO
-- ============================================================================

CREATE TYPE activos.tipo_riesgo_biomedico AS ENUM (
    'CLASE_I',       -- Bajo Riesgo (ej. fonendoscopios, básculas)
    'CLASE_IIA',     -- Riesgo Moderado (ej. monitores de signos, bombas de infusión)
    'CLASE_IIB',     -- Alto Riesgo (ej. ventiladores mecánicos, desfibriladores, rayos X)
    'CLASE_III'      -- Muy Alto Riesgo / Soporte de Vida (ej. marcapasos, máquinas de anestesia)
);

CREATE TYPE activos.estado_operativo_activo AS ENUM (
    'OPERATIVO',
    'EN_MANTENIMIENTO',
    'FUERA_DE_SERVICIO',
    'EN_CALIBRACION',
    'DADO_DE_BAJA'
);

CREATE TYPE activos.tipo_mantenimiento AS ENUM (
    'PREVENTIVO',
    'CORRECTIVO',
    'CALIBRACION_METROLOGICA',
    'CALIFICACION_VALIDACION',
    'INSTALACION_CAPACITACION'
);

CREATE TYPE talento_humano.estado_rethus AS ENUM (
    'ACTIVO',
    'EN_TRAMITE',
    'VENCIDO',
    'SUSPENDIDO',
    'NO_REGISTRADO'
);

CREATE TYPE talento_humano.tipo_vinculacion AS ENUM (
    'PLANTA_PERMANENTE',
    'PRESTACION_SERVICIOS_OPS',
    'AGREMIACION_SINDICAL',
    'CONVENIO_DOCENCIA_SERVICIO'
);

CREATE TYPE auditoria.severidad_hallazgo AS ENUM (
    'CRITICA',       -- Cierre temporal de servicio o medida cautelar inmediata
    'MAYOR',         -- Hallazgo que afecta el estándar de habilitación
    'MENOR',         -- Oportunidad de mejora / hallazgo documental subsanable
    'OBSERVACION'    -- Recomendación preventiva
);

CREATE TYPE auditoria.estado_glosa AS ENUM (
    'NOTIFICADA',
    'EN_REVISION_AUDITORIA',
    'CONTESTADA_JUSTIFICADA',
    'ACEPTADA_PARCIAL',
    'CONCILIADA_SUPERSALUD',
    'VENCIDA_PERENTORIA'
);

-- ============================================================================
-- 2. ESQUEMA CORE: INSTITUCIÓN PRESTADORA, SEDES Y ROLES (RBAC)
-- ============================================================================

CREATE TABLE core.institucion_prestadora (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo_habilitacion_reps VARCHAR(12) NOT NULL UNIQUE, -- Código asignado por MinSalud
    nit VARCHAR(20) NOT NULL UNIQUE,
    razon_social VARCHAR(255) NOT NULL,
    naturaleza_juridica VARCHAR(50) NOT NULL DEFAULT 'E.S.E.', -- ESE Pública o IPS Privada
    nivel_complejidad SMALLINT NOT NULL CHECK (nivel_complejidad BETWEEN 1 AND 4),
    departamento VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono_contacto VARCHAR(50),
    email_gerencia VARCHAR(150) NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core.sedes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institucion_id UUID NOT NULL REFERENCES core.institucion_prestadora(id) ON DELETE RESTRICT,
    codigo_sede VARCHAR(4) NOT NULL, -- Ej: 01 (Sede Principal), 02 (Puesto de Salud)
    nombre_sede VARCHAR(150) NOT NULL,
    es_principal BOOLEAN NOT NULL DEFAULT FALSE,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    responsable_sede VARCHAR(150),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_institucion_sede UNIQUE (institucion_id, codigo_sede)
);

CREATE TABLE core.usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institucion_id UUID NOT NULL REFERENCES core.institucion_prestadora(id) ON DELETE RESTRICT,
    numero_documento VARCHAR(20) NOT NULL UNIQUE,
    tipo_documento VARCHAR(10) NOT NULL DEFAULT 'CC',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo_institucional VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN ('GERENTE_GENERAL', 'SUBGERENTE_CIENTIFICO', 'DIRECTOR_FINANCIERO', 'LIDER_CALIDAD', 'INGENIERO_BIOMEDICO', 'AUDITOR_MEDICO')),
    telefono_movil VARCHAR(20),
    canal_preferido VARCHAR(20) DEFAULT 'WEB' CHECK (canal_preferido IN ('WEB', 'WHATSAPP', 'AMBOS')),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_acceso TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 3. ESQUEMA MÓDULOS: CATÁLOGO CLOUDSALUD 360 Y SERVICIOS REPS
-- ============================================================================

CREATE TABLE modulos.catalogo_servicios_360 (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo_modulo VARCHAR(20) NOT NULL UNIQUE, -- Ej: MOD-01-ACTIVOS, MOD-02-GPC, etc.
    nombre VARCHAR(150) NOT NULL,
    eje_estrategico VARCHAR(100) NOT NULL, -- Habilitación, Financiero, Operaciones, Jurídico
    descripcion TEXT NOT NULL,
    version_actual VARCHAR(10) NOT NULL DEFAULT '2.0.0',
    impacto_auditoria TEXT NOT NULL,
    estado_activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modulos.servicios_habilitados_reps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sede_id UUID NOT NULL REFERENCES core.sedes(id) ON DELETE RESTRICT,
    codigo_servicio_reps VARCHAR(10) NOT NULL, -- Ej: 301 (Urgencias), 312 (UCI Neonatal)
    nombre_servicio VARCHAR(150) NOT NULL,
    grupo_servicio VARCHAR(100) NOT NULL, -- Consulta Externa, Urgencias, Internación, Quirúrgicos
    complejidad_servicio SMALLINT NOT NULL CHECK (complejidad_servicio BETWEEN 1 AND 3),
    resolucion_habilitacion VARCHAR(50),
    fecha_radicacion_novedad DATE,
    fecha_vencimiento_distintivo DATE NOT NULL,
    capacidad_instalada_camas INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_sede_servicio UNIQUE (sede_id, codigo_servicio_reps)
);

-- ============================================================================
-- 4. ESQUEMA ACTIVOS: HOJAS DE VIDA BIOMÉDICA, METROLOGÍA Y MANTENIMIENTOS
-- ============================================================================

CREATE TABLE activos.hoja_vida_biomedica (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sede_id UUID NOT NULL REFERENCES core.sedes(id) ON DELETE RESTRICT,
    servicio_id UUID NOT NULL REFERENCES modulos.servicios_habilitados_reps(id) ON DELETE RESTRICT,
    codigo_inventario_placa VARCHAR(50) NOT NULL UNIQUE, -- Número de placa institucional
    nombre_equipo VARCHAR(150) NOT NULL, -- Ej: Desfibrilador Bifásico, Monitor de Signos
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    serie VARCHAR(100) NOT NULL,
    registro_sanitario_invima VARCHAR(100) NOT NULL, -- Obligatorio Res. 3100
    clasificacion_riesgo activos.tipo_riesgo_biomedico NOT NULL,
    tecnologia_predominante VARCHAR(100) NOT NULL, -- Electrónica, Hidráulica, Óptica, etc.
    ubicacion_especifica VARCHAR(150) NOT NULL, -- Ej: Urgencias - Box Trauma 1
    es_carro_paro BOOLEAN NOT NULL DEFAULT FALSE,
    fuente_alimentacion VARCHAR(50) DEFAULT '110V_AC_BATERIA',
    vida_util_anos SMALLINT NOT NULL DEFAULT 5,
    ano_fabricacion SMALLINT NOT NULL,
    fecha_adquisicion DATE NOT NULL,
    valor_compra_cop NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    periodicidad_mantenimiento_meses SMALLINT NOT NULL DEFAULT 6,
    periodicidad_calibracion_meses SMALLINT NOT NULL DEFAULT 12,
    estado_operativo activos.estado_operativo_activo NOT NULL DEFAULT 'OPERATIVO',
    manual_operacion_url VARCHAR(500),
    guia_rapida_url VARCHAR(500),
    metadata JSONB, -- Almacena variables técnicas específicas (potencia, rango joules, etc.)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE activos.metrologia_calibracion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activo_id UUID NOT NULL REFERENCES activos.hoja_vida_biomedica(id) ON DELETE RESTRICT,
    numero_certificado VARCHAR(100) NOT NULL UNIQUE,
    laboratorio_metrologico VARCHAR(200) NOT NULL,
    acreditacion_onac_numero VARCHAR(100), -- Si aplica acreditación ONAC
    fecha_calibracion DATE NOT NULL,
    fecha_proximo_vencimiento DATE NOT NULL,
    resultado_metrologico VARCHAR(50) NOT NULL CHECK (resultado_metrologico IN ('CONFORME', 'NO_CONFORME', 'CONFORME_CON_RESTRICCION')),
    error_maximo_detectado VARCHAR(100),
    incertidumbre_medicion VARCHAR(100),
    url_certificado_digital VARCHAR(500) NOT NULL, -- Soporte inalterable en PDF
    calibrador_responsable VARCHAR(150) NOT NULL,
    tarjeta_profesional_calibrador VARCHAR(50),
    observaciones_tecnicas TEXT,
    activo_vigente BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE activos.ordenes_mantenimiento (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activo_id UUID NOT NULL REFERENCES activos.hoja_vida_biomedica(id) ON DELETE RESTRICT,
    codigo_orden VARCHAR(50) NOT NULL UNIQUE,
    tipo_mantenimiento activos.tipo_mantenimiento NOT NULL,
    fecha_programada DATE NOT NULL,
    fecha_ejecucion DATE,
    descripcion_falla_solicitud TEXT,
    procedimientos_realizados TEXT,
    repuestos_utilizados JSONB, -- Lista estructurada de repuestos y códigos
    costo_mano_obra_cop NUMERIC(12,2) DEFAULT 0.00,
    costo_repuestos_cop NUMERIC(12,2) DEFAULT 0.00,
    costo_total_cop NUMERIC(12,2) GENERATED ALWAYS AS (costo_mano_obra_cop + costo_repuestos_cop) STORED,
    empresa_prestadora_servicio VARCHAR(200) NOT NULL,
    tecnico_ingeniero_responsable VARCHAR(150) NOT NULL,
    firma_tecnico_url VARCHAR(500),
    recibido_por_personal_asistencial VARCHAR(150) NOT NULL,
    cargo_recibe VARCHAR(100) NOT NULL,
    firma_recibido_url VARCHAR(500),
    satisfaccion_servicio SMALLINT CHECK (satisfaccion_servicio BETWEEN 1 AND 5),
    estado_orden VARCHAR(30) DEFAULT 'COMPLETADA' CHECK (estado_orden IN ('PROGRAMADA', 'EN_PROCESO', 'COMPLETADA', 'CANCELADA')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE activos.infraestructura_critica (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sede_id UUID NOT NULL REFERENCES core.sedes(id) ON DELETE RESTRICT,
    tipo_activo VARCHAR(100) NOT NULL, -- 'PLANTA_ELECTRICA', 'CENTRAL_OXIGENO', 'AIRE_QUIRORANOS', 'AUTOCLAVE'
    codigo_infraestructura VARCHAR(50) NOT NULL UNIQUE,
    capacidad_nominal VARCHAR(100) NOT NULL, -- Ej: '250 kVA', '1500 gal/min'
    autonomia_horas NUMERIC(6,2), -- Ej: 72 horas para planta eléctrica
    ubicacion VARCHAR(150) NOT NULL,
    fecha_ultima_prueba_transferencia DATE,
    fecha_proxima_prueba_transferencia DATE,
    resultado_ultima_prueba VARCHAR(50),
    certificado_retie_url VARCHAR(500),
    estado_operativo VARCHAR(50) DEFAULT 'OPTIMO',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5. ESQUEMA TALENTO HUMANO: RETHUS, CONTRATOS Y SEGURIDAD SOCIAL
-- ============================================================================

CREATE TABLE talento_humano.profesionales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institucion_id UUID NOT NULL REFERENCES core.institucion_prestadora(id) ON DELETE RESTRICT,
    numero_identificacion VARCHAR(20) NOT NULL UNIQUE,
    tipo_identificacion VARCHAR(10) NOT NULL DEFAULT 'CC',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    profesion_base VARCHAR(100) NOT NULL, -- Medicina, Enfermería, Fisioterapia, etc.
    especialidad VARCHAR(150), -- Pediatría, Anestesiología, Cuidado Intensivo, etc.
    numero_tarjeta_profesional VARCHAR(50) NOT NULL,
    entidad_emisora_tarjeta VARCHAR(100) DEFAULT 'Colegio Médico Colombiano',
    titulo_convalidado_men BOOLEAN NOT NULL DEFAULT FALSE,
    resolucion_convalidacion VARCHAR(100), -- Obligatorio si estudió en el extranjero
    correo_personal VARCHAR(150),
    celular VARCHAR(30),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE talento_humano.registro_rethus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profesional_id UUID NOT NULL REFERENCES talento_humano.profesionales(id) ON DELETE CASCADE,
    numero_registro_rethus VARCHAR(50) NOT NULL UNIQUE,
    fecha_inscripcion DATE NOT NULL,
    fecha_ultima_verificacion DATE NOT NULL DEFAULT CURRENT_DATE,
    estado_rethus talento_humano.estado_rethus NOT NULL DEFAULT 'ACTIVO',
    codigo_verificacion_minsalud VARCHAR(100),
    soporte_rethus_pdf_url VARCHAR(500),
    observaciones TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE talento_humano.contratos_vinculaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profesional_id UUID NOT NULL REFERENCES talento_humano.profesionales(id) ON DELETE RESTRICT,
    sede_id UUID NOT NULL REFERENCES core.sedes(id) ON DELETE RESTRICT,
    servicio_asignado_id UUID NOT NULL REFERENCES modulos.servicios_habilitados_reps(id) ON DELETE RESTRICT,
    numero_contrato VARCHAR(50) NOT NULL UNIQUE,
    tipo_vinculacion talento_humano.tipo_vinculacion NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_terminacion DATE NOT NULL,
    honorarios_mensuales_cop NUMERIC(12,2) NOT NULL,
    aseguradora_poliza_rcm VARCHAR(150) NOT NULL, -- Responsabilidad Civil Médica
    numero_poliza_rcm VARCHAR(100) NOT NULL,
    vigencia_poliza_desde DATE NOT NULL,
    vigencia_poliza_hasta DATE NOT NULL,
    monto_amparo_rcm_cop NUMERIC(15,2) NOT NULL DEFAULT 500000000.00,
    estado_seguridad_social VARCHAR(50) NOT NULL DEFAULT 'AL_DIA' CHECK (estado_seguridad_social IN ('AL_DIA', 'PENDIENTE_PLANILLA', 'EN_MORA')),
    soporte_contrato_pdf_url VARCHAR(500),
    soporte_poliza_pdf_url VARCHAR(500),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 6. ESQUEMA AUDITORÍA: LOG INALTERABLE, HALLAZGOS Y GLOSAS (DEC. 441)
-- ============================================================================

CREATE TABLE auditoria.audit_trail (
    id BIGSERIAL PRIMARY KEY,
    transaction_uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id UUID REFERENCES core.usuarios(id) ON DELETE SET NULL,
    rol_ejecutor VARCHAR(50) NOT NULL,
    canal_origen VARCHAR(50) NOT NULL, -- 'WEB_DASHBOARD', 'WHATSAPP_API', 'PROACTIVE_CRON'
    direccion_ip INET,
    modulo_consultado VARCHAR(100) NOT NULL,
    consulta_sanitizada TEXT NOT NULL, -- Texto sin cédulas ni nombres de pacientes (Ley 1581)
    sql_generado TEXT,
    tiempo_respuesta_ms INT NOT NULL,
    filas_afectadas INT DEFAULT 0,
    checksum_sha256 VARCHAR(64) NOT NULL -- Hash SHA-256 encadenado para inmutabilidad legal
);

-- Trigger de Inmutabilidad Absoluta en Audit Trail (Imposible alterar o borrar registros)
CREATE OR REPLACE FUNCTION auditoria.fn_proteger_audit_trail()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Operación denegada: La tabla auditoria.audit_trail es estrictamente inalterable bajo el Estatuto Anticorrupción (Ley 1474 de 2011) y la Ley 1581 de 2012.';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_bloquear_modificacion_audit_trail
BEFORE UPDATE OR DELETE ON auditoria.audit_trail
FOR EACH ROW EXECUTE FUNCTION auditoria.fn_proteger_audit_trail();

CREATE TABLE auditoria.hallazgos_habilitacion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sede_id UUID NOT NULL REFERENCES core.sedes(id) ON DELETE RESTRICT,
    servicio_id UUID REFERENCES modulos.servicios_habilitados_reps(id) ON DELETE SET NULL,
    codigo_estandar_res3100 VARCHAR(50) NOT NULL, -- Ej: 'EST-TH-01', 'EST-DOT-03', 'EST-MED-05'
    nombre_estandar VARCHAR(100) NOT NULL, -- Talento Humano, Dotación, Medicamentos, Procesos
    criterio_evaluado TEXT NOT NULL,
    descripcion_hallazgo TEXT NOT NULL,
    severidad auditoria.severidad_hallazgo NOT NULL,
    medida_preventiva_inmediata TEXT NOT NULL,
    plan_mejoramiento_pamec TEXT NOT NULL,
    fecha_identificacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_limite_subsanacion DATE NOT NULL,
    responsable_subsanacion VARCHAR(150) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'ABIERTO' CHECK (estado IN ('ABIERTO', 'EN_SUBSANACION', 'SUBSANADO_VALIDADO', 'VENCIDO')),
    evidencia_cierre_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auditoria.glosas_aseguradores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institucion_id UUID NOT NULL REFERENCES core.institucion_prestadora(id) ON DELETE RESTRICT,
    nombre_eps VARCHAR(150) NOT NULL, -- Nueva EPS, Sanitas, Salud Total, etc.
    nit_eps VARCHAR(20) NOT NULL,
    numero_factura VARCHAR(50) NOT NULL,
    fecha_factura DATE NOT NULL,
    valor_facturado_cop NUMERIC(15,2) NOT NULL,
    valor_glosado_cop NUMERIC(15,2) NOT NULL,
    codigo_glosa_supersalud VARCHAR(20) NOT NULL, -- Codificación oficial de glosas
    descripcion_glosa TEXT NOT NULL,
    fecha_notificacion_glosa DATE NOT NULL,
    -- Plazo perentorio de 15 días hábiles según Decreto 441 de 2022
    fecha_vencimiento_respuesta DATE NOT NULL,
    estado_glosa auditoria.estado_glosa NOT NULL DEFAULT 'NOTIFICADA',
    respuesta_juridica_radicada TEXT,
    fecha_radicacion_respuesta DATE,
    radicado_salida VARCHAR(50),
    recuperado_cop NUMERIC(15,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auditoria.autodiagnosticos_express (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institucion_id UUID NOT NULL REFERENCES core.institucion_prestadora(id) ON DELETE RESTRICT,
    ejecutado_por_usuario_id UUID REFERENCES core.usuarios(id) ON DELETE SET NULL,
    fecha_ejecucion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    indice_blindaje_score NUMERIC(5,2) NOT NULL, -- Porcentaje 0.00 a 100.00%
    total_items_evaluados SMALLINT NOT NULL DEFAULT 32,
    total_implementados SMALLINT NOT NULL,
    total_en_despliegue SMALLINT NOT NULL,
    total_pendientes SMALLINT NOT NULL,
    vulnerabilidades_criticas_detectadas SMALLINT NOT NULL,
    resumen_hallazgos_json JSONB NOT NULL,
    plan_accion_recomendado_json JSONB NOT NULL,
    tiempo_computo_ms INT NOT NULL
);

-- ============================================================================
-- 7. ÍNDICES DE RENDIMIENTO Y VISTAS ESTRATÉGICAS
-- ============================================================================

-- Índices B-Tree en llaves foráneas y campos temporales críticos
CREATE INDEX idx_biomedica_servicio ON activos.hoja_vida_biomedica(servicio_id);
CREATE INDEX idx_biomedica_riesgo ON activos.hoja_vida_biomedica(clasificacion_riesgo);
CREATE INDEX idx_metrologia_vencimiento ON activos.metrologia_calibracion(fecha_proximo_vencimiento);
CREATE INDEX idx_metrologia_activo ON activos.metrologia_calibracion(activo_id);
CREATE INDEX idx_contratos_fechas ON talento_humano.contratos_vinculaciones(fecha_terminacion, vigencia_poliza_hasta);
CREATE INDEX idx_rethus_estado ON talento_humano.registro_rethus(estado_rethus);
CREATE INDEX idx_audit_timestamp ON auditoria.audit_trail(timestamp DESC);
CREATE INDEX idx_glosas_eps_vencimiento ON auditoria.glosas_aseguradores(nombre_eps, fecha_vencimiento_respuesta);

-- Índices GIN para consultas estructuradas en JSONB y texto
CREATE INDEX idx_audit_json_metadata ON activos.hoja_vida_biomedica USING gin(metadata);
CREATE INDEX idx_autodiag_findings_json ON auditoria.autodiagnosticos_express USING gin(resumen_hallazgos_json);

-- VISTA 1: Semáforo de Equipos Biomédicos Próximos a Vencer Calibración (< 30 días)
CREATE OR REPLACE VIEW activos.vw_alertas_biomedicas_vencimiento AS
SELECT 
    b.id AS activo_id,
    b.codigo_inventario_placa,
    b.nombre_equipo,
    b.marca,
    b.modelo,
    b.serie,
    b.clasificacion_riesgo,
    s.nombre_servicio,
    b.ubicacion_especifica,
    m.numero_certificado,
    m.fecha_proximo_vencimiento,
    (m.fecha_proximo_vencimiento - CURRENT_DATE) AS dias_para_vencer,
    CASE 
        WHEN m.fecha_proximo_vencimiento < CURRENT_DATE THEN 'VENCIDO_CRITICO'
        WHEN (m.fecha_proximo_vencimiento - CURRENT_DATE) <= 15 THEN 'ALERTA_INMEDIATA'
        WHEN (m.fecha_proximo_vencimiento - CURRENT_DATE) <= 30 THEN 'ALERTA_PREVENTIVA'
        ELSE 'OPTIMO'
    END AS semaforo_riesgo
FROM activos.hoja_vida_biomedica b
JOIN modulos.servicios_habilitados_reps s ON b.servicio_id = s.id
JOIN activos.metrologia_calibracion m ON b.id = m.activo_id AND m.activo_vigente = TRUE
WHERE (m.fecha_proximo_vencimiento - CURRENT_DATE) <= 30
ORDER BY m.fecha_proximo_vencimiento ASC;

-- VISTA 2: Semáforo de Talento Humano en Riesgo de Habilitación (RETHUS / Póliza)
CREATE OR REPLACE VIEW talento_humano.vw_alertas_personal_habilitacion AS
SELECT 
    p.id AS profesional_id,
    p.tipo_identificacion,
    p.numero_identificacion,
    p.nombres || ' ' || p.apellidos AS nombre_completo,
    p.profesion_base,
    p.especialidad,
    r.estado_rethus,
    c.numero_contrato,
    c.fecha_terminacion AS fecha_terminacion_contrato,
    c.vigencia_poliza_hasta AS fecha_vencimiento_poliza,
    c.estado_seguridad_social,
    CASE 
        WHEN r.estado_rethus != 'ACTIVO' THEN 'RETHUS_NO_ACTIVO_CRITICO'
        WHEN c.vigencia_poliza_hasta < CURRENT_DATE THEN 'POLIZA_VENCIDA_CRITICO'
        WHEN (c.vigencia_poliza_hasta - CURRENT_DATE) <= 15 THEN 'POLIZA_POR_VENCER'
        WHEN c.estado_seguridad_social != 'AL_DIA' THEN 'SEGURIDAD_SOCIAL_PENDIENTE'
        ELSE 'CONFORME'
    END AS estado_riesgo_auditoria
FROM talento_humano.profesionales p
LEFT JOIN talento_humano.registro_rethus r ON p.id = r.profesional_id
LEFT JOIN talento_humano.contratos_vinculaciones c ON p.id = c.profesional_id AND c.activo = TRUE
WHERE r.estado_rethus != 'ACTIVO' 
   OR c.vigencia_poliza_hasta <= (CURRENT_DATE + INTERVAL '30 days')
   OR c.estado_seguridad_social != 'AL_DIA';
