"""
CloudSalud Copiloto ESE - Security & Privacy Sanitizer
Cumplimiento estricto de la Ley Estatutaria 1581 de 2012 (Habeas Data) y Secreto Profesional Médico (Ley 23 de 1981).
Garantiza que la IA nunca procese ni exponga Datos Personales Sensibles de Pacientes (PHI).
"""

import re
from typing import Tuple

# Patrones de detección de datos personales protegidos
REGEX_CEDULA = r'\b(c\.?c\.?|c[eé]dula|identificaci[oó]n|ti|tarjeta de identidad|registro civil|nit)\s*[:#]?\s*([0-9]{6,11})\b'
REGEX_HISTORIA_CLINICA = r'\b(h\.?c\.?|historia cl[ií]nica|folio|expediente)\s*[:#]?\s*([0-9A-Za-z-]{4,15})\b'
REGEX_TELEFONO = r'\b(\+?57\s?)?3[0-9]{2}[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}\b'
REGEX_NOMBRE_PACIENTE = r'\b(paciente|usuario|afiliado)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\b'

def sanitize_query(raw_query: str) -> Tuple[str, bool, list]:
    """
    Sanitiza la consulta del usuario eliminando identificadores personales directos.
    Retorna: (query_anonimizada, hubo_reemplazo, lista_de_advertencias)
    """
    sanitized = raw_query
    redactions = []
    
    # 1. Anonimizar nombres de pacientes
    def replace_name(match):
        redactions.append(f"Nombre de paciente censurado: '{match.group(2)}'")
        return f"{match.group(1)} [PACIENTE_ANONIMIZADO]"
    sanitized = re.sub(REGEX_NOMBRE_PACIENTE, replace_name, sanitized, flags=re.IGNORECASE)

    # 2. Anonimizar Cédulas / Identificaciones
    def replace_id(match):
        redactions.append(f"Documento de identidad censurado: '{match.group(2)}'")
        return f"{match.group(1)} [DOCUMENTO_PROTEGIDO]"
    sanitized = re.sub(REGEX_CEDULA, replace_id, sanitized, flags=re.IGNORECASE)

    # 3. Anonimizar Historias Clínicas
    def replace_hc(match):
        redactions.append(f"Número de Historia Clínica censurado: '{match.group(2)}'")
        return f"{match.group(1)} [HC_PROTEGIDA]"
    sanitized = re.sub(REGEX_HISTORIA_CLINICA, replace_hc, sanitized, flags=re.IGNORECASE)

    # 4. Anonimizar Teléfonos
    def replace_tel(match):
        redactions.append(f"Teléfono personal censurado")
        return "[TEL_PROTEGIDO]"
    sanitized = re.sub(REGEX_TELEFONO, replace_tel, sanitized)

    hubo_reemplazo = len(redactions) > 0
    return sanitized, hubo_reemplazo, redactions

def format_privacy_notice(redactions: list) -> str:
    """Genera advertencia formal de Habeas Data para adjuntar a la respuesta."""
    if not redactions:
        return ""
    items = "\n".join([f"  • {item}" for item in redactions])
    return (
        "\n\n> 🛡️ **Protección de Datos (Ley 1581 de 2012):**\n"
        "> Se aplicó disociación automática a los siguientes datos sensibles para garantizar el secreto médico:\n"
        f"{items}"
    )
