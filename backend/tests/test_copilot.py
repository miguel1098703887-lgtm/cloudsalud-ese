"""
Test Suite para CloudSalud Copiloto ESE
Verifica de punta a punta: Sanitización Ley 1581, RBAC, RAG Normativo, Text-to-SQL y Briefing Matutino.
"""

import unittest
import sys
from pathlib import Path

# Agregar directorio backend al sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import init_db
from app.seed_data import seed_database
from app.security.sanitizer import sanitize_query
from app.security.rbac import verify_permission, UserRole
from app.modules.habilitacion_rag import search_normativa
from app.modules.text_to_sql import process_query_analytics
from app.modules.proactive_engine import generate_morning_briefing, get_proactive_alarms

class TestCloudSalud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_database()

    def test_01_sanitizer_ley1581(self):
        """Verifica que se anonimicen cédulas y nombres de pacientes."""
        raw = "El paciente Juan Carlos Gómez con cédula 1024567890 tiene dengue en urgencias"
        sanitized, redacted, items = sanitize_query(raw)
        self.assertTrue(redacted)
        self.assertNotIn("1024567890", sanitized)
        self.assertNotIn("Juan Carlos Gómez", sanitized)
        self.assertIn("[PACIENTE_ANONIMIZADO]", sanitized)
        self.assertIn("[DOCUMENTO_PROTEGIDO]", sanitized)

    def test_02_rbac_permissions(self):
        """Verifica que Subgerencia Científica no pueda ver finanzas, pero sí camas."""
        # Subgerente científico intentando ver cartera
        allowed, msg = verify_permission("SUBGERENTE_CIENTIFICO", "FINANCIERO_CARTERA")
        self.assertFalse(allowed)
        self.assertIn("Acceso Restringido", msg)

        # Gerente General sí puede
        allowed_g, _ = verify_permission("GERENTE_GENERAL", "FINANCIERO_CARTERA")
        self.assertTrue(allowed_g)

    def test_03_rag_habilitacion_uci_neonatal(self):
        """Verifica respuesta normativa de Res. 3100 para UCI Neonatal."""
        res = search_normativa("¿Qué requisitos nos faltan para habilitar una UCI neonatal?")
        self.assertTrue(res["found"])
        self.assertIn("Resolución 3100 de 2019", res["norma"])
        self.assertIn("Neonatología", res["respuesta_estructurada"])
        self.assertIn("Incubadoras de doble pared", res["respuesta_estructurada"])

    def test_04_text_to_sql_cartera_nueva_eps(self):
        """Verifica consulta matemática exacta de cartera con Nueva EPS."""
        res = process_query_analytics("¿A cuánto asciende la cartera mayor a 90 días con la Nueva EPS?")
        self.assertTrue(res["matched"])
        self.assertIn("Nueva EPS", res["text"])
        self.assertIsNotNone(res["card"])
        self.assertEqual(res["card"]["tipo"], "CHART_CARTERA")

    def test_05_text_to_sql_ocupacion_urgencias(self):
        """Verifica cálculo en tiempo real del termómetro hospitalario."""
        res = process_query_analytics("¿Cuál es el porcentaje de ocupación de Urgencias y UCI?")
        self.assertTrue(res["matched"])
        self.assertIn("Urgencias Adultos", res["text"])
        self.assertIn("UCI Adultos", res["text"])

    def test_06_morning_briefing(self):
        """Verifica generación completa del briefing matutino de las 6:30 am."""
        briefing = generate_morning_briefing("Dr. Carlos Mendoza")
        self.assertIn("Briefing Matutino", briefing["titulo"])
        self.assertIn("Urgencias Adultos", briefing["resumen_texto"])
        self.assertIn("urgencias_ocupacion", briefing["metrics"])

    def test_07_proactive_alarms(self):
        """Verifica la detección automática de los 5 desfibriladores y ReTHUS."""
        alarms = get_proactive_alarms()
        self.assertGreaterEqual(len(alarms), 2)
        categorias = [a["categoria"] for a in alarms]
        self.assertIn("HABILITACION_DOTACION", categorias)
        self.assertIn("HABILITACION_TALENTO_HUMANO", categorias)

    def test_08_implementation_items(self):
        """Verifica la consulta y estructura del Plan Maestro de Implementación (32 ítems)."""
        from app.modules.implementation_items import IMPLEMENTATION_ITEMS, get_implementation_summary
        self.assertEqual(len(IMPLEMENTATION_ITEMS), 32)
        summary = get_implementation_summary()
        self.assertEqual(summary["total_items"], 32)
        self.assertGreaterEqual(summary["porcentaje_avance"], 50.0)

        # Prueba en RAG
        rag_res = search_normativa("¿Cuáles son los items para implementar en el hospital?")
        self.assertTrue(rag_res["found"])
        self.assertIn("Plan Maestro de Implementación", rag_res["titulo"])
        self.assertEqual(rag_res["card_data"]["tipo"], "IMPLEMENTATION_ROADMAP_CARD")

if __name__ == "__main__":
    unittest.main()
