"""
CloudSalud Copiloto ESE - Role-Based Access Control (RBAC)
Seguridad de accesos según la estructura orgánica hospitalaria colombiana.
"""

from enum import Enum
from typing import Dict, List, Tuple

class UserRole(str, Enum):
    GERENTE_GENERAL = "GERENTE_GENERAL"
    SUBGERENTE_CIENTIFICO = "SUBGERENTE_CIENTIFICO"
    DIRECTOR_FINANCIERO = "DIRECTOR_FINANCIERO"

# Matriz de permisos por módulo funcional
PERMISSIONS: Dict[UserRole, List[str]] = {
    UserRole.GERENTE_GENERAL: [
        "HABILITACION_CALIDAD",
        "FINANCIERO_CARTERA",
        "FINANCIERO_GLOSAS",
        "FINANCIERO_PRESUPUESTO",
        "OPERATIVO_CAMAS",
        "OPERATIVO_FARMACIA",
        "TALENTO_HUMANO",
        "EQUIPOS_BIOMEDICOS",
        "BRIEFING_ESTRATEGICO",
        "AUDITORIA_LOGS"
    ],
    UserRole.SUBGERENTE_CIENTIFICO: [
        "HABILITACION_CALIDAD",
        "OPERATIVO_CAMAS",
        "OPERATIVO_FARMACIA",
        "TALENTO_HUMANO",
        "EQUIPOS_BIOMEDICOS",
        "BRIEFING_ESTRATEGICO"
        # Bloqueado: Finanzas, Cartera, Glosas, Presupuesto ESE, Auditoría
    ],
    UserRole.DIRECTOR_FINANCIERO: [
        "FINANCIERO_CARTERA",
        "FINANCIERO_GLOSAS",
        "FINANCIERO_PRESUPUESTO",
        "HABILITACION_CALIDAD",
        "BRIEFING_ESTRATEGICO"
        # Bloqueado: Ocupación clínica detallada, Talento humano individual, Auditoría
    ]
}

def verify_permission(role: str, module_requested: str) -> Tuple[bool, str]:
    """
    Verifica si el rol tiene permiso para consultar el módulo solicitado.
    """
    try:
        user_role = UserRole(role)
    except ValueError:
        return False, f"Rol no reconocido en el sistema ESE: '{role}'"

    allowed_modules = PERMISSIONS.get(user_role, [])
    
    if module_requested in allowed_modules:
        return True, "Acceso concedido"

    # Mensajes institucionales de denegación según rol
    if user_role == UserRole.SUBGERENTE_CIENTIFICO and "FINANCIERO" in module_requested:
        return False, (
            "🔒 **Acceso Restringido por Política de Control Interno:**\n"
            "El perfil de **Subgerencia Científica** no cuenta con autorización para visualizar saldos de cartera, glosas o ejecución presupuestal global. "
            "Esta información está reservada para el despacho del **Gerente General** y la **Dirección Financiera** de la E.S.E."
        )
    elif user_role == UserRole.DIRECTOR_FINANCIERO and "OPERATIVO_CAMAS" in module_requested:
        return False, (
            "🔒 **Acceso Restringido:**\n"
            "El perfil de **Dirección Financiera** tiene restringido el acceso al monitoreo en tiempo real de camas clínicas individuales y triages asistenciales. "
            "Consulte con la Subgerencia Científica o solicite habilitación al Gerente."
        )
    
    return False, f"🔒 El rol '{user_role.value}' no tiene permisos para acceder a la dimensión '{module_requested}'."
