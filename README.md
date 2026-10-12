# CloudSalud - Copiloto Gerencial y Estratégico para Hospitales Públicos (E.S.E.) en Colombia

CloudSalud es una plataforma y copiloto de inteligencia artificial diseñado a la medida de los gerentes y directores de las **Empresas Sociales del Estado (E.S.E.)** en Colombia.

Lejos de ser un simple chatbot de preguntas frecuentes, CloudSalud actúa como un **Copiloto Estratégico, Proactivo y Analítico** que fusiona:
1. **RAG Normativo determinista** para Habilitación y Calidad (Resolución 3100 de 2019, PAMEC, Ley 1438 de 2011).
2. **Text-to-SQL analítico en tiempo real** para finanzas, cartera, glosas (Decreto 441 de 2022), urgencias y farmacia, garantizando **cero alucinaciones contables**.
3. **Omnicanalidad y Voz**: Dashboard gerencial web y simulador de WhatsApp Business API con notas de voz (Speech-to-Text).
4. **Seguridad y Cumplimiento Normativo (Ley 1581 de 2012)**: Anonimización automática de datos sensibles de salud (PHI), control de acceso basado en roles (RBAC) y registro inalterable de auditoría para entes de control (Contraloría y Supersalud).

---

## 🏛️ Cobertura de los 5 Pilares de Diseño

### 1. Casos de Uso Core (El "Cerebro")
* **Módulo de Habilitación y Calidad:** 
  - Auditor preventivo con requisitos exactos de la **Resolución 3100 de 2019** (UCI Neonatal, Urgencias, Quirófanos).
  - Alertas automáticas de vencimiento de calibración metrológica biomédica (desfibriladores, ventiladores) y registros ReTHUS de médicos asistenciales.
  - Soporte documental de guías clínicas y protocolos PAMEC (ej. higiene de manos según los 5 momentos OMS).
* **Módulo Financiero y Supervivencia:**
  - Consulta matemática exacta de cartera vencida por asegurador (ej. Nueva EPS >90 días).
  - Resumen y motivos de glosas con plazos perentorios de respuesta (Decreto 441 de 2022).
  - Alertas de agotamiento en rubros de gasto (Material Médico-Quirúrgico al 91.8%).
* **Módulo Operativo y Asistencial en Vivo:**
  - Termómetro hospitalario de ocupación en Urgencias y camas UCI.
  - Detección de demoras críticas en Triage 2 (>4 horas).
  - Monitoreo de stock mínimo de seguridad en medicamentos vitales (Adrenalina, catéteres centrales).

### 2. Experiencia de Usuario (UX) y Accesibilidad
* **Briefing Matutino Proactivo (06:30 a.m.):** Resumen diario integral que cruza asistencial, habilitación, finanzas y agenda externa antes de iniciar la jornada.
* **Omnicanalidad y Voz (Speech-to-Text):** Permite dictar notas de voz desde el móvil o el navegador, transcribiendo y procesando instantáneamente la consulta.
* **Tarjetas Visuales y Action Pills:** Gráficos dinámicos interactivos (Chart.js) de cartera, glosas y ocupación incrustados en la conversación, junto a botones de acción rápida para eliminar el síndrome de pantalla en blanco.

### 3. Arquitectura Tecnológica
```
[ Usuario (Web / WhatsApp API / Voz) ]
               │
               ▼
[ Sanitizador Ley 1581 (Disociación PHI) ]
               │
               ▼
[ Control de Accesos RBAC (Gerente / Subgerente / Dir. Financiero) ]
               │
       ┌───────┴───────────────────────────┐
       ▼                                   ▼
[ RAG Normativo ]                  [ Text-to-SQL Engine ]
• Res. 3100/2019 (Habilitación)    • Cartera EPS & Glosas
• Dec. 441/2022 (Acuerdos/Glosas)  • Ocupación de Camas
• Ley 1438 / Res. 408 (Plan Gest.) • Presupuesto ESE
• PAMEC & Protocolos Clínicos      • Farmacia e Insumos
       │                                   │
       └───────┬───────────────────────────┘
               ▼
[ Logger Inalterable de Auditoría (Ley 1474 / Supersalud) ]
               │
               ▼
[ Respuesta Estructurada + Tarjetas Visuales (Chart.js) ]
```

### 4. Seguridad y Cumplimiento
* **Anonimización Automática (Ley 1581 de 2012):** Detección y censura de nombres de pacientes, números de cédula, folios de historia clínica y teléfonos. El sistema entrega únicamente información agregada.
* **Control de Accesos Basado en Roles (RBAC):**
  - `GERENTE_GENERAL`: Acceso total (Finanzas, Calidad, Asistencial, Auditoría).
  - `SUBGERENTE_CIENTIFICO`: Asistencial, Habilitación y Camas; finanzas bloqueadas.
  - `DIRECTOR_FINANCIERO`: Cartera, Glosas y Presupuesto; datos clínicos detallados restringidos.
* **Trazabilidad Inalterable:** Registro por consulta con hora, rol, canal, consulta anonimizada, SQL ejecutado y tiempo de respuesta en milisegundos.

---

## 🚀 Puesta en Marcha Rápida

### 1. Requisitos Previos
* Python 3.10+
* FastAPI y Uvicorn (`pip install fastapi uvicorn`)

### 2. Iniciar el Servidor de CloudSalud
Desde la carpeta raíz del proyecto:
```powershell
cd C:\Users\migue\.gemini\antigravity\scratch\cloudsalud\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Acceso al Dashboard
Abra su navegador web en:
👉 **`http://localhost:8000/`**

### 4. Acceso Público por Internet (En Vivo)
Para compartir la aplicación inmediatamente con cualquier persona en el mundo sin necesidad de configurar servidores:
* **URL Pública en Vivo:** `https://few-dancers-repeat.loca.lt`
* **Contraseña / IP de Acceso (si la solicita en la primera apertura):** `38.172.222.22`

*(El túnel conecta de forma segura con el servidor local mediante HTTPS).*

### 5. Despliegue Permanente 24/7 en la Nube (Render / Railway)

#### A. Subir a GitHub
```bash
git remote add origin https://github.com/TU_USUARIO/cloudsalud-ese.git
git branch -M main
git push -u origin main
```

#### B. Desplegar en Render.com (Gratuito)
1. Inicie sesión en [Render.com](https://render.com/).
2. Haga clic en **New + > Web Service** y conecte su repositorio de GitHub.
3. Configure los campos:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir backend`
4. Haga clic en **Deploy Web Service**. Render generará automáticamente un enlace HTTPS permanente (ej. `https://cloudsalud-ese.onrender.com`).

#### C. Despliegue con Docker
```bash
docker build -t cloudsalud-ese .
docker run -p 8000:8000 cloudsalud-ese
```

### 6. Ejecución de Pruebas Unitarias
```powershell
cd backend
python tests/test_copilot.py
```
*(8 pruebas unitarias aprobadas: Sanitizador, RBAC, RAG Habilitación, Text-to-SQL Cartera, Termómetro Camas, Briefing Matutino, Alertas Proactivas y Matriz de 32 Items).*

---

## 📋 Hoja de Ruta de Fases (Roadmap)

* [x] **Fase 1: El Oráculo Normativo:** Carga de estándares de la Resolución 3100 de 2019, PAMEC y Ley 1438 de 2011.
* [x] **Fase 2: El Asistente de Alertas Proactivas:** Conexión a mantenimiento biomédico (calibraciones metrológicas) y ReTHUS para disparar avisos antes del vencimiento.
* [x] **Fase 3: El Analista Financiero y Operativo:** Motor Text-to-SQL para cartera EPS, glosas (Decreto 441 de 2022), urgencias y farmacia.
* [x] **Fase 3.5: Matriz de 32 Items de Implementación y Diagnóstico Express:** Escaneo algorítmico y autodiagnóstico en vivo.
* [ ] **Fase 4: Modelo Predictivo y Alertas Epidemiológicas:** Predicción de picos de infección respiratoria (IRA) y cálculo de sobrecosto por días de estancia prolongada.

