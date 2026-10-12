/**
 * CloudSalud Copiloto ESE - Frontend Application Logic (Suite 360)
 * Integración de Riesgos en Auditorías, Catálogo 360, Los 5 Pilares,
 * Navegación Multinivel, Chat Copiloto, Voz (Speech-to-Text), Chart.js y WhatsApp.
 */

const API_BASE = window.location.origin && window.location.origin.startsWith("http") 
  ? `${window.location.origin}/api` 
  : "/api";

// Estado de la aplicación
const state = {
  currentRole: "GERENTE_GENERAL",
  currentTab: "copilot", // 'copilot' | 'audit-risks' | 'catalog' | 'pillars' | 'roadmap' | 'whatsapp'
  isRecording: false,
  chartInstances: {}
};

// Elementos DOM principales
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const voiceBtn = document.getElementById("voice-btn");
const voiceIndicator = document.getElementById("voice-indicator");
const roleSelect = document.getElementById("role-select");
const activeRoleBadge = document.getElementById("active-role-badge");
const executionTimeLabel = document.getElementById("execution-time-label");

// Vistas
const viewCopilot = document.getElementById("view-copilot");
const viewAuditRisks = document.getElementById("view-audit-risks");
const viewCatalog = document.getElementById("view-catalog");
const viewImplementation = document.getElementById("view-implementation");
const viewPillars = document.getElementById("view-pillars");
const viewRoadmap = document.getElementById("view-roadmap");
const viewWhatsapp = document.getElementById("view-whatsapp");

// WhatsApp Elements
const waMessages = document.getElementById("wa-messages");
const waInput = document.getElementById("wa-input");
const waVoiceBtn = document.getElementById("wa-voice-btn");

// Audit Modal Elements
const openAuditBtn = document.getElementById("open-audit-btn");
const closeAuditBtn = document.getElementById("close-audit-btn");
const auditModal = document.getElementById("audit-modal");
const auditTableBody = document.getElementById("audit-table-body");

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
  initEventListeners();
  fetchDashboardKPIs();
  initVoiceRecognition();
  initImplementationModule();
});

function initEventListeners() {
  // Cambio de Rol (RBAC)
  roleSelect.addEventListener("change", (e) => {
    state.currentRole = e.target.value;
    if (activeRoleBadge) {
      activeRoleBadge.textContent = state.currentRole;
    }
    appendSystemNotice(`Rol activo cambiado a: **${state.currentRole}**. Los permisos de acceso a finanzas y datos clínicos se han actualizado.`);
  });

  // Envío de mensaje en Dashboard
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;
    sendMessage(query, false, "Dashboard Web");
    chatInput.value = "";
  });

  // Envío en WhatsApp Simulator
  waInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      const q = waInput.value.trim();
      if (!q) return;
      sendMessage(q, false, "WhatsApp Business API (Texto)", true);
      waInput.value = "";
    }
  });

  // Botón rápido de Briefing Matutino
  const briefingBtn = document.getElementById("trigger-briefing-btn");
  if (briefingBtn) {
    briefingBtn.addEventListener("click", () => {
      switchMainTab("copilot");
      sendMessage("Briefing Matutino", false, "Dashboard Web");
    });
  }

  // Action chips
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".quick-chip");
    if (chip) {
      const prompt = chip.getAttribute("data-prompt");
      if (prompt) {
        switchMainTab("copilot");
        sendMessage(prompt, false, "Dashboard Web");
      }
    }
  });

  // Limpiar Chat
  const clearBtn = document.getElementById("clear-chat-btn");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      chatMessages.innerHTML = `
        <div class="text-center py-6 text-xs text-slate-400 font-medium">
          Historial de conversación reiniciado.
        </div>
      `;
    });
  }

  // Modal de Auditoría
  openAuditBtn.addEventListener("click", openAuditModal);
  closeAuditBtn.addEventListener("click", () => auditModal.classList.add("hidden"));
}

// Navegación principal por pestañas (7 pestañas)
function switchMainTab(tab) {
  state.currentTab = tab;

  // Ocultar todas las vistas
  viewCopilot.classList.add("hidden");
  if (viewAuditRisks) viewAuditRisks.classList.add("hidden");
  if (viewCatalog) viewCatalog.classList.add("hidden");
  if (viewImplementation) viewImplementation.classList.add("hidden");
  viewPillars.classList.add("hidden");
  viewRoadmap.classList.add("hidden");
  viewWhatsapp.classList.add("hidden");

  // Mostrar la vista seleccionada
  if (tab === "copilot") {
    viewCopilot.classList.remove("hidden");
  } else if (tab === "audit-risks") {
    if (viewAuditRisks) viewAuditRisks.classList.remove("hidden");
  } else if (tab === "catalog") {
    if (viewCatalog) viewCatalog.classList.remove("hidden");
  } else if (tab === "implementation") {
    if (viewImplementation) viewImplementation.classList.remove("hidden");
  } else if (tab === "pillars") {
    viewPillars.classList.remove("hidden");
  } else if (tab === "roadmap") {
    viewRoadmap.classList.remove("hidden");
  } else if (tab === "whatsapp") {
    viewWhatsapp.classList.remove("hidden");
  }

  // Actualizar estilos de los botones en el nav (Azul Marino #0F172A & Teal #0D9488)
  const tabButtons = {
    copilot: document.getElementById("tab-btn-copilot"),
    "audit-risks": document.getElementById("tab-btn-audit-risks"),
    catalog: document.getElementById("tab-btn-catalog"),
    implementation: document.getElementById("tab-btn-implementation"),
    pillars: document.getElementById("tab-btn-pillars"),
    roadmap: document.getElementById("tab-btn-roadmap"),
    whatsapp: document.getElementById("tab-btn-whatsapp")
  };

  Object.keys(tabButtons).forEach(key => {
    const btn = tabButtons[key];
    if (!btn) return;
    if (key === tab) {
      btn.className = "main-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 bg-[#0D9488] text-white shadow-sm transition";
    } else {
      btn.className = "main-tab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 text-slate-300 hover:text-white hover:bg-slate-800 transition";
    }
  });

  lucide.createIcons();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Probar caso de uso de un pilar o módulo en el Copiloto
function triggerPillarTest(prompt) {
  switchMainTab("copilot");
  setTimeout(() => {
    sendMessage(prompt, false, "Dashboard Web");
  }, 200);
}

// Cargar métricas en tiempo real del hospital
async function fetchDashboardKPIs() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) return;
    const data = await res.json();

    const urgEl = document.getElementById("kpi-urg-pct");
    if (urgEl) urgEl.textContent = `${data.urgencias_ocupacion_pct}%`;
    const urgSub = document.getElementById("kpi-urg-sub");
    if (urgSub) urgSub.textContent = `${data.urgencias_ocupadas} / ${data.urgencias_total} camas`;
    const uciEl = document.getElementById("kpi-uci-libres");
    if (uciEl) uciEl.textContent = data.camas_uci_libres;
    
    const m90 = data.cartera_mayor_90_cop;
    const cartEl = document.getElementById("kpi-cartera-m90");
    if (cartEl) cartEl.textContent = m90 >= 1e9 ? `$${(m90 / 1e9).toFixed(1)} mil M` : `$${(m90 / 1e6).toFixed(0)} M`;
    
    const glosas = data.glosas_pendientes_cop;
    const glosEl = document.getElementById("kpi-glosas");
    if (glosEl) glosEl.textContent = `$${(glosas / 1e6).toFixed(1)} M`;
    const eqEl = document.getElementById("kpi-equipos");
    if (eqEl) eqEl.textContent = data.alertas_biomedicas_count;
    const retEl = document.getElementById("kpi-rethus");
    if (retEl) retEl.textContent = data.rethus_por_renovar_count;
  } catch (err) {
    console.error("Error al cargar KPIs del dashboard:", err);
  }
}

// Envío de consulta al Copiloto
async function sendMessage(query, isVoice = false, channel = "Dashboard Web", isWhatsApp = false) {
  appendUserMessage(query, isVoice, isWhatsApp);
  const loaderId = appendLoadingIndicator(isWhatsApp);

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        role: state.currentRole,
        channel: channel,
        user_id: "DIR-001",
        is_voice: isVoice
      })
    });

    const data = await response.json();
    removeLoadingIndicator(loaderId);

    if (executionTimeLabel) {
      executionTimeLabel.textContent = `Respuesta en ${data.execution_time_ms} ms (${data.module_used})`;
    }

    appendBotMessage(data, isWhatsApp);

  } catch (error) {
    removeLoadingIndicator(loaderId);
    appendBotErrorMessage("Error de conexión con el backend de CloudSalud. Verifique que el servicio esté activo.", isWhatsApp);
  }
}

function appendUserMessage(text, isVoice, isWhatsApp) {
  if (isWhatsApp) {
    const bubble = document.createElement("div");
    bubble.className = "bg-[#d9fdd3] text-[#111b21] p-2.5 rounded-xl rounded-tr-sm self-end ml-auto max-w-[85%] shadow-xs text-xs border border-[#c1f3b8]";
    bubble.innerHTML = `
      <p class="flex items-center space-x-1.5 font-medium">
        ${isVoice ? '<i data-lucide="mic" class="w-3.5 h-3.5 text-[#008069]"></i>' : ''}
        <span>${escapeHtml(text)}</span>
      </p>
      <span class="block text-right text-[9px] text-slate-500 mt-0.5">Ahora ✓✓</span>
    `;
    waMessages.appendChild(bubble);
    waMessages.scrollTop = waMessages.scrollHeight;
    lucide.createIcons();
    return;
  }

  const msgDiv = document.createElement("div");
  msgDiv.className = "flex items-start justify-end space-x-3";
  msgDiv.innerHTML = `
    <div class="bg-sky-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-[80%] text-xs shadow-sm">
      <div class="flex items-center space-x-1.5 mb-0.5 opacity-90 text-[10px] font-medium">
        ${isVoice ? '<i data-lucide="mic" class="w-3 h-3"></i><span>Nota de voz transcripta</span>' : '<span>Consulta Gerencial</span>'}
      </div>
      <p class="leading-relaxed font-medium">${escapeHtml(text)}</p>
    </div>
    <div class="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 flex items-center justify-center shrink-0">
      <i data-lucide="user" class="w-4 h-4 text-sky-700"></i>
    </div>
  `;
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  lucide.createIcons();
}

function appendLoadingIndicator(isWhatsApp) {
  const id = "loader-" + Date.now();
  if (isWhatsApp) {
    const loader = document.createElement("div");
    loader.id = id;
    loader.className = "bg-white text-slate-500 p-2.5 rounded-xl text-xs max-w-[60%] flex items-center space-x-2 border border-slate-200 shadow-2xs";
    loader.innerHTML = `<span class="animate-pulse font-medium">Escribiendo...</span>`;
    waMessages.appendChild(loader);
    waMessages.scrollTop = waMessages.scrollHeight;
    return id;
  }

  const loader = document.createElement("div");
  loader.id = id;
  loader.className = "flex items-start space-x-3";
  loader.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center shrink-0 text-white shadow-sm">
      <i data-lucide="activity" class="w-4 h-4"></i>
    </div>
    <div class="bg-slate-50 border border-slate-200 rounded-2xl rounded-tl-sm px-4 py-3 text-xs text-slate-600 flex items-center space-x-2 shadow-2xs font-medium">
      <div class="flex space-x-1">
        <div class="w-1.5 h-1.5 bg-sky-600 rounded-full animate-bounce"></div>
        <div class="w-1.5 h-1.5 bg-sky-600 rounded-full animate-bounce [animation-delay:0.2s]"></div>
        <div class="w-1.5 h-1.5 bg-sky-600 rounded-full animate-bounce [animation-delay:0.4s]"></div>
      </div>
      <span>Consultando RAG Normativo y bases de datos de la E.S.E...</span>
    </div>
  `;
  chatMessages.appendChild(loader);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  lucide.createIcons();
  return id;
}

function removeLoadingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function appendBotMessage(data, isWhatsApp) {
  if (isWhatsApp) {
    const bubble = document.createElement("div");
    bubble.className = "bg-white p-3 rounded-xl rounded-tl-sm border border-slate-200 shadow-2xs max-w-[90%] text-slate-800 text-xs";
    bubble.innerHTML = `
      <div class="text-[10px] text-[#008069] font-bold mb-1 flex items-center space-x-1">
        <i data-lucide="shield" class="w-3 h-3"></i>
        <span>CloudSalud Copiloto ESE</span>
      </div>
      <div class="leading-relaxed whitespace-pre-wrap text-slate-700 font-normal">${formatMarkdown(data.response_text)}</div>
      <span class="block text-right text-[9px] text-slate-400 mt-1">Ahora ✓✓</span>
    `;
    waMessages.appendChild(bubble);
    waMessages.scrollTop = waMessages.scrollHeight;
    lucide.createIcons();
    return;
  }

  const msgDiv = document.createElement("div");
  msgDiv.className = "flex items-start space-x-3";

  const chartId = "chart-" + Date.now();

  let cardHtml = "";
  if (data.card) {
    cardHtml = generateCardHtml(data.card, chartId);
  }

  let pillsHtml = "";
  if (data.suggested_pills && data.suggested_pills.length > 0) {
    pillsHtml = `
      <div class="mt-3 pt-2.5 border-t border-slate-200 flex flex-wrap gap-1.5">
        ${data.suggested_pills.map(p => `
          <button class="quick-chip bg-white hover:bg-sky-50 text-sky-700 border border-slate-200 rounded-lg px-2.5 py-1 text-[11px] font-semibold transition shadow-2xs" data-prompt="${escapeHtml(p)}">
            ${escapeHtml(p)}
          </button>
        `).join("")}
      </div>
    `;
  }

  let traceBadge = "";
  if (data.sql_executed) {
    traceBadge = `
      <div class="mt-2 text-[10px] font-mono text-emerald-800 bg-emerald-50 border border-emerald-200 rounded-lg px-2.5 py-1.5">
        <strong>SQL Auditado:</strong> ${escapeHtml(data.sql_executed.substring(0, 110))}...
      </div>
    `;
  }

  msgDiv.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center shrink-0 shadow-sm text-white">
      <i data-lucide="bot" class="w-5 h-5"></i>
    </div>
    <div class="bg-slate-50 border border-slate-200 rounded-2xl rounded-tl-sm p-4 max-w-[85%] text-xs text-slate-700 leading-relaxed shadow-xs">
      <div class="prose-salud">${formatMarkdown(data.response_text)}</div>
      ${cardHtml}
      ${traceBadge}
      ${pillsHtml}
    </div>
  `;

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  lucide.createIcons();

  if (data.card) {
    renderChart(data.card, chartId);
  }
}

function appendSystemNotice(text) {
  const notice = document.createElement("div");
  notice.className = "flex justify-center my-2";
  notice.innerHTML = `
    <div class="bg-amber-50 text-amber-900 border border-amber-200 rounded-xl px-3.5 py-1.5 text-[11px] flex items-center space-x-2 font-medium shadow-2xs">
      <i data-lucide="info" class="w-3.5 h-3.5 text-amber-600"></i>
      <span>${formatMarkdown(text)}</span>
    </div>
  `;
  chatMessages.appendChild(notice);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  lucide.createIcons();
}

function appendBotErrorMessage(errorText, isWhatsApp) {
  if (isWhatsApp) {
    const bubble = document.createElement("div");
    bubble.className = "bg-rose-50 text-rose-800 p-2.5 rounded-xl border border-rose-200 text-xs";
    bubble.textContent = errorText;
    waMessages.appendChild(bubble);
    return;
  }
  const msgDiv = document.createElement("div");
  msgDiv.className = "flex items-start space-x-3";
  msgDiv.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-rose-600 flex items-center justify-center shrink-0 text-white">
      <i data-lucide="alert-triangle" class="w-4 h-4"></i>
    </div>
    <div class="bg-rose-50 border border-rose-200 rounded-2xl rounded-tl-sm p-3.5 text-xs text-rose-800 font-medium">
      ${escapeHtml(errorText)}
    </div>
  `;
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  lucide.createIcons();
}

function generateCardHtml(card, chartId) {
  if (card.tipo === "CHART_CARTERA" || card.tipo === "CHART_GLOSAS") {
    return `
      <div class="mt-3 p-3.5 bg-white border border-slate-200 rounded-xl shadow-2xs">
        <h4 class="text-xs font-bold text-slate-800 mb-2">${escapeHtml(card.titulo)}</h4>
        <div class="h-44 relative">
          <canvas id="${chartId}"></canvas>
        </div>
      </div>
    `;
  } else if (card.tipo === "CHART_OCUPACION") {
    return `
      <div class="mt-3 p-3.5 bg-white border border-slate-200 rounded-xl shadow-2xs">
        <h4 class="text-xs font-bold text-slate-800 mb-2">${escapeHtml(card.titulo)}</h4>
        <div class="h-48 relative">
          <canvas id="${chartId}"></canvas>
        </div>
      </div>
    `;
  } else if (card.tipo === "AUDIT_RISKS_SUMMARY") {
    return `
      <div class="mt-3 p-3.5 bg-white border border-rose-200 rounded-xl shadow-2xs">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-xs font-bold text-rose-800">${escapeHtml(card.titulo)}</h4>
          <span class="text-[10px] bg-rose-100 text-rose-800 px-2 py-0.5 rounded-full font-bold">Res. 3100 / EPS</span>
        </div>
        <div class="space-y-1.5">
          ${card.areas_criticas.map(a => `
            <div class="flex items-center justify-between text-[11px] p-2 bg-slate-50 border border-slate-100 rounded-lg">
              <span class="text-slate-800 font-semibold">${escapeHtml(a.area)}</span>
              <div class="flex items-center space-x-2">
                <span class="text-[10px] text-slate-500">${escapeHtml(a.impacto)}</span>
                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded ${a.severidad === 'CRÍTICA' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}">${a.severidad}</span>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } else if (card.tipo === "CATALOG_360_CARD") {
    return `
      <div class="mt-3 p-3.5 bg-white border border-emerald-200 rounded-xl shadow-2xs">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-xs font-bold text-emerald-800">Suite CloudSalud (360) - 8 Módulos</h4>
          <span class="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-bold">Blindaje Preventivo</span>
        </div>
        <div class="grid grid-cols-2 gap-2 mt-2">
          ${card.modulos.map(m => `
            <div class="p-2 bg-slate-50 border border-slate-100 rounded-lg">
              <p class="text-[11px] font-bold text-slate-800">${escapeHtml(m.nombre)}</p>
              <span class="text-[9px] text-sky-700 font-semibold">${escapeHtml(m.tag)}</span>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } else if (card.tipo === "HABILITACION_CHECKLIST") {
    return `
      <div class="mt-3 p-3.5 bg-white border border-slate-200 rounded-xl shadow-2xs">
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-xs font-bold text-emerald-800">Verificación de Habilitación: ${escapeHtml(card.servicio)}</h4>
          <span class="text-[10px] bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full font-bold">Cumplimiento: ${card.cumplimiento_general}</span>
        </div>
        <div class="space-y-1.5">
          ${card.puntos_criticos.map(p => `
            <div class="flex items-center justify-between text-[11px] p-2 bg-slate-50 border border-slate-100 rounded-lg">
              <span class="text-slate-700 font-medium">${escapeHtml(p.criterio)}</span>
              <span class="font-bold ${p.estado.includes('Crítico') ? 'text-red-600' : (p.estado.includes('Alerta') ? 'text-amber-600' : 'text-emerald-700')}">${escapeHtml(p.estado)}</span>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } else if (card.tipo === "PROACTIVE_ALARMS_LIST") {
    return `
      <div class="mt-3 space-y-2">
        ${card.alertas.map(a => `
          <div class="p-3 bg-white border ${a.nivel === 'CRITICO' ? 'border-red-200 bg-red-50/20' : 'border-amber-200 bg-amber-50/20'} rounded-xl shadow-2xs">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs ${a.nivel === 'CRITICO' ? 'text-red-700' : 'text-amber-700'}">${escapeHtml(a.titulo)}</span>
              <span class="text-[9px] uppercase px-2 py-0.5 rounded font-extrabold ${a.nivel === 'CRITICO' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}">${a.nivel}</span>
            </div>
            <p class="text-[11px] text-slate-700 mt-1">${escapeHtml(a.detalle)}</p>
            <div class="mt-2 text-[10px] text-sky-800 font-semibold flex items-center space-x-1">
              <i data-lucide="check-circle" class="w-3.5 h-3.5 text-sky-600"></i>
              <span>Acción sugerida: ${escapeHtml(a.accion_sugerida)}</span>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  } else if (card.tipo === "IMPLEMENTATION_ROADMAP_CARD") {
    return `
      <div class="mt-3 p-4 bg-white border border-emerald-200 rounded-2xl shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <h4 class="text-xs font-bold text-[#0F172A]">${escapeHtml(card.titulo)}</h4>
          </div>
          <span class="text-[10px] bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full font-bold">Blindaje: ${escapeHtml(card.blindaje_avance)}</span>
        </div>
        <div class="grid grid-cols-2 gap-2 mb-3">
          ${card.areas.map(a => `
            <div class="p-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl flex items-center justify-between">
              <span class="text-[11px] font-semibold text-[#0F172A]">${escapeHtml(a.nombre)}</span>
              <span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">${escapeHtml(a.estado)}</span>
            </div>
          `).join("")}
        </div>
        <button class="w-full py-2 bg-[#0D9488] hover:bg-[#0F766E] text-white text-xs font-semibold rounded-xl transition" onclick="switchMainTab('implementation')">
          Abrir Matriz Completa de 32 Items →
        </button>
      </div>
    `;
  }
  return "";
}

function renderChart(card, chartId) {
  const canvas = document.getElementById(chartId);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const darkGrayText = "#334155";

  if (card.tipo === "CHART_CARTERA") {
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: card.labels,
        datasets: [{
          data: card.data,
          backgroundColor: ["#10b981", "#0284c7", "#f59e0b", "#f97316", "#ef4444"],
          borderWidth: 2,
          borderColor: "#ffffff"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
            labels: { color: darkGrayText, font: { size: 10, weight: "bold" } }
          }
        }
      }
    });
  } else if (card.tipo === "CHART_GLOSAS") {
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: card.labels,
        datasets: [{
          label: "Valor Glosado (COP)",
          data: card.data,
          backgroundColor: "#e11d48",
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { 
            grid: { color: "#f1f5f9" },
            ticks: { color: darkGrayText, font: { size: 9, weight: "bold" } } 
          },
          y: { 
            grid: { color: "#f1f5f9" },
            ticks: { color: darkGrayText, font: { size: 9 } } 
          }
        }
      }
    });
  } else if (card.tipo === "CHART_OCUPACION") {
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: card.servicios,
        datasets: [{
          label: "Ocupación (%)",
          data: card.ocupacion,
          backgroundColor: card.ocupacion.map(v => v >= 90 ? "#dc2626" : (v >= 80 ? "#d97706" : "#059669")),
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { 
            max: 100, 
            grid: { color: "#f1f5f9" },
            ticks: { color: darkGrayText, font: { size: 9, weight: "bold" } } 
          },
          y: { 
            grid: { color: "#f1f5f9" },
            ticks: { color: darkGrayText, font: { size: 9, weight: "bold" } } 
          }
        }
      }
    });
  }
}

function initVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (!SpeechRecognition) {
    if (voiceBtn) voiceBtn.addEventListener("click", () => simulateVoiceNote());
    if (waVoiceBtn) waVoiceBtn.addEventListener("click", () => simulateVoiceNote(true));
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "es-CO";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    state.isRecording = true;
    voiceIndicator.classList.remove("hidden");
    voiceBtn.classList.add("bg-red-50", "text-red-600", "border-red-300");
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    chatInput.value = transcript;
    sendMessage(transcript, true, "Dashboard Web (Voz)");
  };

  recognition.onerror = () => {
    simulateVoiceNote();
  };

  recognition.onend = () => {
    state.isRecording = false;
    voiceIndicator.classList.add("hidden");
    voiceBtn.classList.remove("bg-red-50", "text-red-600", "border-red-300");
  };

  if (voiceBtn) {
    voiceBtn.addEventListener("click", () => {
      if (state.isRecording) {
        recognition.stop();
      } else {
        recognition.start();
      }
    });
  }

  if (waVoiceBtn) {
    waVoiceBtn.addEventListener("click", () => {
      simulateVoiceNote(true);
    });
  }
}

function simulateVoiceNote(isWhatsApp = false) {
  const simulatedVoiceQueries = [
    "¿Cuáles son los 5 puntos críticos donde las ESE e IPS acumulan mayor riesgo en auditorías de habilitación y EPS?",
    "Muéstrame el catálogo completo de servicios de CloudSalud 360",
    "¿A cuánto asciende la cartera mayor a 90 días con la Nueva EPS?",
    "¿Qué requisitos de talento humano o dotación nos faltan para habilitar una UCI neonatal?",
    "Genera un resumen de los motivos principales de glosas de este mes"
  ];
  const query = simulatedVoiceQueries[Math.floor(Math.random() * simulatedVoiceQueries.length)];
  
  if (isWhatsApp) {
    sendMessage(query, true, "WhatsApp Business API (Nota de Voz)", true);
  } else {
    chatInput.value = query;
    sendMessage(query, true, "Dashboard Web (Nota de Voz)");
  }
}

async function openAuditModal() {
  auditModal.classList.remove("hidden");
  auditTableBody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-slate-400">Cargando registros...</td></tr>`;

  try {
    const res = await fetch(`${API_BASE}/audit/logs?role=${state.currentRole}`);
    if (!res.ok) {
      const err = await res.json();
      auditTableBody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-rose-600 font-semibold">${escapeHtml(err.detail || "Acceso denegado")}</td></tr>`;
      return;
    }

    const data = await res.json();
    if (!data.logs || data.logs.length === 0) {
      auditTableBody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-slate-400">No hay registros de auditoría aún.</td></tr>`;
      return;
    }

    auditTableBody.innerHTML = data.logs.map(log => `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 text-slate-500 text-[10px] font-mono">${log.timestamp.split("T")[1] || log.timestamp}</td>
        <td class="py-2.5 px-3 font-bold text-[10px] text-sky-700">${escapeHtml(log.rol_usuario)}</td>
        <td class="py-2.5 px-3 text-slate-600 text-[10px] font-medium">${escapeHtml(log.canal)}</td>
        <td class="py-2.5 px-3 text-slate-800 text-xs font-semibold">${escapeHtml(log.pregunta_anonimizada)}</td>
        <td class="py-2.5 px-3 text-slate-500 text-[10px] font-medium">${escapeHtml(log.modulo_invocado)}</td>
        <td class="py-2.5 px-3 text-emerald-700 text-[9px] font-mono font-medium">${log.sql_ejecutado ? escapeHtml(log.sql_ejecutado.substring(0, 45)) + '...' : 'N/A'}</td>
        <td class="py-2.5 px-3 text-right text-slate-600 text-[10px] font-semibold">${log.tiempo_respuesta_ms} ms</td>
      </tr>
    `).join("");

  } catch (err) {
    auditTableBody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-rose-600">Error al cargar registros.</td></tr>`;
  }
}

function formatMarkdown(text) {
  if (!text) return "";
  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h3>$1</h3>')
    .replace(/^# (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>');
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/* =========================================================================
   MÓDULO: PLAN MAESTRO DE IMPLEMENTACIÓN & BLINDAJE DE AUDITORÍAS (32 ÍTEMS)
   ========================================================================= */

let allImplementationItems = [];
let currentImplFilter = "all";
let currentImplSearch = "";

async function initImplementationModule() {
  const container = document.getElementById("impl-items-container");
  if (!container) return;

  // Escuchar Autodiagnóstico en Vivo
  const autoDiagBtn = document.getElementById("btn-run-autodiagnosis");
  if (autoDiagBtn) {
    autoDiagBtn.addEventListener("click", runAutodiagnosis);
  }

  // Escuchar Exportar CSV
  const exportCsvBtn = document.getElementById("btn-export-csv");
  if (exportCsvBtn) {
    exportCsvBtn.addEventListener("click", exportImplementationCSV);
  }

  // Cerrar Banner Autodiagnóstico
  const closeDiagBtn = document.getElementById("close-autodiag-btn");
  if (closeDiagBtn) {
    closeDiagBtn.addEventListener("click", () => {
      document.getElementById("autodiagnosis-banner").classList.add("hidden");
    });
  }

  // Escuchar Búsqueda en Vivo
  const searchInput = document.getElementById("impl-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentImplSearch = e.target.value.toLowerCase().trim();
      renderImplementationItems();
    });
  }

  // Escuchar Filtros por Eje / Prioridad
  const filterBtns = document.querySelectorAll(".impl-filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => {
        b.className = "impl-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#F8FAFC] text-[#334155] hover:bg-slate-100 border border-[#E2E8F0] transition";
      });
      btn.className = "impl-filter-btn px-3 py-1.5 rounded-lg text-xs font-bold bg-[#0F172A] text-white transition shadow-sm";
      currentImplFilter = btn.getAttribute("data-filter");
      renderImplementationItems();
    });
  });

  await loadImplementationData();
}

async function loadImplementationData() {
  try {
    const res = await fetch(`${API_BASE}/implementation/items`);
    if (!res.ok) throw new Error("Error al obtener ítems");
    const data = await res.json();
    allImplementationItems = data.items || [];
    updateImplementationKPIs(data.summary);
    renderImplementationItems();
  } catch (err) {
    console.error("Error al cargar ítems de implementación:", err);
  }
}

function updateImplementationKPIs(summary) {
  if (!summary) return;
  
  const scoreEl = document.getElementById("stat-shield-score");
  if (scoreEl) scoreEl.textContent = `${summary.porcentaje_avance}%`;

  const barEl = document.getElementById("stat-progress-bar");
  if (barEl) barEl.style.width = `${summary.porcentaje_avance}%`;

  const impEl = document.getElementById("stat-implemented-count");
  if (impEl) impEl.textContent = summary.implementados;

  const progEl = document.getElementById("stat-inprogress-count");
  if (progEl) progEl.textContent = summary.en_curso;

  const pendEl = document.getElementById("stat-pending-count");
  if (pendEl) pendEl.textContent = summary.pendientes;

  const critEl = document.getElementById("stat-critical-ratio");
  if (critEl) critEl.textContent = `${summary.criticos_blindados} / ${summary.total_criticos}`;
}

function renderImplementationItems() {
  const container = document.getElementById("impl-items-container");
  if (!container) return;

  // Filtrado
  const filtered = allImplementationItems.filter(item => {
    // Filtro por categoría / eje
    let matchesFilter = true;
    if (currentImplFilter === "PUNTOS_CRITICOS") {
      matchesFilter = item.eje === "PUNTOS_CRITICOS";
    } else if (currentImplFilter === "CATALOGO_360") {
      matchesFilter = item.eje === "CATALOGO_360";
    } else if (currentImplFilter === "CRITICA") {
      matchesFilter = item.prioridad === "CRÍTICA";
    }

    // Filtro por texto
    let matchesSearch = true;
    if (currentImplSearch) {
      const q = currentImplSearch;
      matchesSearch = (
        item.codigo.toLowerCase().includes(q) ||
        item.titulo.toLowerCase().includes(q) ||
        item.categoria.toLowerCase().includes(q) ||
        item.normativa.toLowerCase().includes(q) ||
        item.especificacion.toLowerCase().includes(q) ||
        item.entregable.toLowerCase().includes(q)
      );
    }

    return matchesFilter && matchesSearch;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 text-center bg-white border border-[#E2E8F0] rounded-2xl">
        <i data-lucide="inbox" class="w-8 h-8 text-slate-300 mx-auto mb-2"></i>
        <p class="text-xs text-slate-500 font-medium">No se encontraron ítems de implementación con los criterios seleccionados.</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  container.innerHTML = filtered.map(item => {
    // Prioridad visual
    let priorityBadge = "";
    if (item.prioridad === "CRÍTICA") {
      priorityBadge = `<span class="bg-amber-100 text-[#B45309] text-[9px] font-extrabold uppercase px-2 py-0.5 rounded-full border border-amber-200">🚨 Crítica (Riesgo Cierre/Glosa)</span>`;
    } else if (item.prioridad === "ALTA") {
      priorityBadge = `<span class="bg-slate-100 text-[#334155] text-[9px] font-bold uppercase px-2 py-0.5 rounded-full border border-slate-200">Alta (Habilitación)</span>`;
    } else {
      priorityBadge = `<span class="bg-slate-50 text-slate-500 text-[9px] font-medium uppercase px-2 py-0.5 rounded-full border border-slate-100">Operativa</span>`;
    }

    // Borde según estado
    let borderClass = "border-[#E2E8F0]";
    if (item.estado === "Implementado") borderClass = "border-emerald-200 bg-white hover:border-emerald-400";
    else if (item.estado === "En Curso") borderClass = "border-amber-200 bg-white hover:border-amber-400";
    else borderClass = "border-slate-200 bg-white hover:border-slate-300";

    return `
      <div class="border ${borderClass} rounded-2xl p-5 shadow-sm hover:shadow transition flex flex-col justify-between">
        <div>
          <!-- Header de Tarjeta -->
          <div class="flex items-center justify-between gap-2 mb-2">
            <div class="flex items-center space-x-2">
              <span class="font-heading font-extrabold text-xs px-2 py-0.5 rounded-lg bg-[#0F172A] text-white">${escapeHtml(item.codigo)}</span>
              <span class="text-[11px] font-bold text-[#0D9488]">${escapeHtml(item.categoria)}</span>
            </div>
            ${priorityBadge}
          </div>

          <!-- Título -->
          <h3 class="font-heading text-xs font-bold text-[#0F172A] mb-2 leading-snug">
            ${escapeHtml(item.titulo)}
          </h3>

          <!-- Cuerpo de la Especificación -->
          <div class="space-y-2 text-xs text-[#334155]">
            <div class="p-2.5 bg-[#F8FAFC] rounded-xl border border-[#E2E8F0]">
              <strong class="text-[#0F172A] block mb-0.5 text-[10px] uppercase font-bold tracking-wide">⚙️ Especificación Técnica:</strong>
              <p class="text-[11px] leading-relaxed">${escapeHtml(item.especificacion)}</p>
            </div>

            <div class="p-2.5 bg-emerald-50/50 rounded-xl border border-emerald-100">
              <strong class="text-[#0F766E] block mb-0.5 text-[10px] uppercase font-bold tracking-wide">📦 Entregable CloudSalud:</strong>
              <p class="text-[11px] leading-relaxed text-[#115E59]">${escapeHtml(item.entregable)}</p>
            </div>

            <div class="flex flex-wrap gap-1 text-[10px]">
              <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md font-mono">⚖️ ${escapeHtml(item.normativa)}</span>
            </div>

            <p class="text-[10px] text-slate-500 italic mt-1">
              <strong>Impacto:</strong> ${escapeHtml(item.impacto)}
            </p>
          </div>
        </div>

        <!-- Footer: Selector de Estado Interactivo y Botón Copiloto -->
        <div class="mt-4 pt-3 border-t border-[#F1F5F9] flex items-center justify-between gap-2">
          
          <select 
            onchange="updateItemStatusFromUI('${item.id}', this.value)"
            class="text-[11px] font-bold px-2.5 py-1.5 rounded-lg border focus:outline-none cursor-pointer transition ${
              item.estado === 'Implementado' ? 'bg-emerald-50 text-emerald-800 border-emerald-300' :
              (item.estado === 'En Curso' ? 'bg-amber-50 text-[#B45309] border-amber-300' : 'bg-slate-50 text-slate-600 border-slate-300')
            }"
          >
            <option value="Implementado" ${item.estado === 'Implementado' ? 'selected' : ''}>🟢 Implementado</option>
            <option value="En Curso" ${item.estado === 'En Curso' ? 'selected' : ''}>🟡 En Despliegue</option>
            <option value="Pendiente" ${item.estado === 'Pendiente' ? 'selected' : ''}>⚪ Pendiente</option>
          </select>

          <button 
            onclick="triggerPillarTest('${escapeHtml(item.copilot_prompt).replace(/'/g, "\\'")}')" 
            class="px-2.5 py-1.5 bg-[#F8FAFC] hover:bg-teal-50 text-[#0F766E] text-[11px] font-semibold rounded-lg border border-[#E2E8F0] transition flex items-center space-x-1"
            title="Consultar este ítem directamente con el Copiloto de IA"
          >
            <i data-lucide="bot" class="w-3 h-3 text-[#0D9488]"></i>
            <span>Probar</span>
          </button>

        </div>
      </div>
    `;
  }).join("");

  lucide.createIcons();
}

async function updateItemStatusFromUI(itemId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/implementation/toggle/${itemId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ estado: newStatus })
    });
    if (!res.ok) throw new Error("Fallo al actualizar estado");
    const data = await res.json();
    
    // Actualizar localmente
    const target = allImplementationItems.find(i => i.id === itemId);
    if (target) target.estado = newStatus;

    updateImplementationKPIs(data.new_summary);
    renderImplementationItems();
  } catch (err) {
    console.error("Error al actualizar estado del ítem:", err);
    alert("No se pudo actualizar el estado del ítem en el servidor.");
  }
}

async function runAutodiagnosis() {
  const banner = document.getElementById("autodiagnosis-banner");
  const findingsList = document.getElementById("autodiag-findings-list");
  if (!banner || !findingsList) return;

  findingsList.innerHTML = `<p class="text-xs text-slate-500 animate-pulse">Escaneando bases de datos de talento humano, biomédica, farmacia y glosas...</p>`;
  banner.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE}/implementation/autodiagnosis`, { method: "POST" });
    if (!res.ok) throw new Error("Error al ejecutar autodiagnóstico");
    const data = await res.json();

    if (!data.hallazgos || data.hallazgos.length === 0) {
      findingsList.innerHTML = `
        <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 font-semibold">
          ✅ Sin vulnerabilidades críticas inmediatas detectadas en la base de datos del hospital.
        </div>
      `;
    } else {
      findingsList.innerHTML = data.hallazgos.map(h => `
        <div class="p-3 bg-white border border-amber-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-2 shadow-2xs">
          <div>
            <div class="flex items-center space-x-2">
              <span class="text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded ${h.severidad === 'CRÍTICA' ? 'bg-amber-100 text-[#B45309]' : 'bg-slate-100 text-slate-700'}">${h.severidad}</span>
              <strong class="text-xs text-[#0F172A]">${escapeHtml(h.area)} (Ítem ${h.codigo_item})</strong>
            </div>
            <p class="text-xs text-[#334155] mt-1">${escapeHtml(h.hallazgo)}</p>
            <p class="text-[11px] text-[#0F766E] font-medium mt-0.5"><strong>Plan de Acción:</strong> ${escapeHtml(h.accion_recomendada)}</p>
          </div>
          <button class="px-3 py-1.5 bg-[#0D9488] hover:bg-[#0F766E] text-white text-xs font-semibold rounded-lg shrink-0 transition" onclick="triggerPillarTest('Alerta en ${escapeHtml(h.area)}: ¿Cómo subsanar de inmediato?')">
            Subsanar con IA →
          </button>
        </div>
      `).join("");
    }

    if (data.resumen_implementacion) {
      updateImplementationKPIs(data.resumen_implementacion);
    }
    lucide.createIcons();

  } catch (err) {
    findingsList.innerHTML = `<p class="text-xs text-rose-600 font-bold">Error de conexión al ejecutar el autodiagnóstico.</p>`;
  }
}

function exportImplementationCSV() {
  if (!allImplementationItems || allImplementationItems.length === 0) {
    alert("No hay ítems cargados para exportar.");
    return;
  }

  const headers = ["Codigo", "Eje", "Categoria", "Titulo", "Prioridad", "Estado", "Normativa", "Especificacion_Tecnica", "Entregable_CloudSalud", "Impacto_Auditoria"];
  const rows = allImplementationItems.map(item => [
    `"${item.codigo}"`,
    `"${item.eje}"`,
    `"${item.categoria}"`,
    `"${item.titulo.replace(/"/g, '""')}"`,
    `"${item.prioridad}"`,
    `"${item.estado}"`,
    `"${item.normativa.replace(/"/g, '""')}"`,
    `"${item.especificacion.replace(/"/g, '""')}"`,
    `"${item.entregable.replace(/"/g, '""')}"`,
    `"${item.impacto.replace(/"/g, '""')}"`
  ]);

  const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\r\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `Matriz_Implementacion_CloudSalud360_${new Date().toISOString().split("T")[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ==========================================
// MODAL CONTROLLERS & GLOBAL TOAST
// ==========================================

let toastTimeout = null;

function showToast(message) {
  const toast = document.getElementById("global-toast");
  const msgEl = document.getElementById("global-toast-msg");
  if (!toast || !msgEl) return;

  msgEl.textContent = message;
  toast.classList.remove("hidden");
  
  // Transición suave
  setTimeout(() => {
    toast.classList.remove("opacity-0", "translate-y-2");
    toast.classList.add("opacity-100", "translate-y-0");
  }, 10);

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("opacity-100", "translate-y-0");
    toast.classList.add("opacity-0", "translate-y-2");
    setTimeout(() => toast.classList.add("hidden"), 300);
  }, 3500);
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("hidden");
}

function showHospitalQuickStatus() {
  const modal = document.getElementById("quick-status-modal");
  if (modal) {
    modal.classList.remove("hidden");
    lucide.createIcons();
  }
}

function showRoleModal() {
  const modal = document.getElementById("role-modal");
  if (modal) {
    modal.classList.remove("hidden");
    lucide.createIcons();
  }
}

function showHabeasDataModal() {
  const modal = document.getElementById("privacy-modal");
  if (modal) {
    modal.classList.remove("hidden");
    lucide.createIcons();
  }
}

function showCopilotInfoModal() {
  const modal = document.getElementById("copilot-info-modal");
  if (modal) {
    modal.classList.remove("hidden");
    lucide.createIcons();
  }
}

// Filtro interactivo desde las tarjetas KPI superiores de Implementación
function filterImplFromCard(filterVal) {
  switchMainTab("implementation");
  currentImplFilter = filterVal;

  const filterBtns = document.querySelectorAll(".impl-filter-btn");
  filterBtns.forEach(btn => {
    if (btn.getAttribute("data-filter") === filterVal) {
      btn.className = "impl-filter-btn px-3 py-1.5 rounded-lg text-xs font-bold bg-[#0F172A] text-white transition shadow-sm";
    } else {
      btn.className = "impl-filter-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-[#F8FAFC] text-[#334155] hover:bg-slate-100 border border-[#E2E8F0] transition";
    }
  });

  renderImplementationItems();
  const label = filterVal === 'all' ? 'todos los 32 ítems' : (filterVal === 'CRITICA' ? 'ítems Críticos' : `ítems ${filterVal}`);
  showToast(`Filtrando matriz por: ${label}`);
}

// ==========================================
// WHATSAPP BUSINESS API CONTROLLERS
// ==========================================

function toggleWAMenu() {
  const menu = document.getElementById("wa-dropdown-menu");
  if (menu) {
    menu.classList.toggle("hidden");
    lucide.createIcons();
  }
}

// Cerrar menú de WhatsApp si se hace click fuera
document.addEventListener("click", (e) => {
  const menu = document.getElementById("wa-dropdown-menu");
  const btn = document.getElementById("wa-menu-btn");
  if (menu && !menu.classList.contains("hidden")) {
    if (!menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.add("hidden");
    }
  }
});

function sendWAMorningBriefing() {
  switchMainTab("whatsapp");
  sendMessage("Briefing Matutino", false, "WhatsApp Business API", true);
  showToast("Reenviando Briefing Matutino por WhatsApp...");
}

function clearWAMessages() {
  if (!waMessages) return;
  waMessages.innerHTML = `
    <div class="bg-white p-3 rounded-xl rounded-tl-sm border border-slate-200 shadow-sm max-w-[90%] text-[#334155]">
      <p class="text-[#0F766E] font-bold text-[11px] mb-1 font-heading">🌅 Asistente CloudSalud ESE</p>
      <p class="text-[11px] leading-relaxed text-[#334155]">
        Canal de mensajería cifrado listo. Puede enviar consultas directas, audios o adjuntar evidencias clínicas.
      </p>
      <span class="block text-right text-[9px] text-[#64748B] mt-1 tabular-numbers">Listo ✓✓</span>
    </div>
  `;
  showToast("Historial de WhatsApp reiniciado.");
}

function simulateWAAttachment() {
  const simulatedFiles = [
    { name: "Certificado_Calibracion_Desfibriladores_2026.pdf", size: "2.4 MB", prompt: "He recibido el certificado de calibración de los 5 desfibriladores de urgencias. ¿Cumple con la norma técnica de Habilitación Res. 3100?" },
    { name: "Contrato_Prestacion_Servicios_Medicos.pdf", size: "1.1 MB", prompt: "¿Qué cláusulas de seguridad social y RETHUS son obligatorias en los contratos de prestación de servicios asistenciales para pasar la auditoría?" },
    { name: "Soporte_Glosa_NuevaEPS_Res441.pdf", size: "3.8 MB", prompt: "Adjunto el acta de glosas de Nueva EPS por $2.480M. ¿Cuáles son los términos perentorios del Decreto 441 de 2022 para responder?" }
  ];

  const file = simulatedFiles[Math.floor(Math.random() * simulatedFiles.length)];

  const bubble = document.createElement("div");
  bubble.className = "bg-[#d9fdd3] text-[#111b21] p-3 rounded-xl rounded-tr-sm self-end ml-auto max-w-[85%] shadow-xs text-xs border border-[#c1f3b8]";
  bubble.innerHTML = `
    <div class="flex items-center space-x-2.5 p-2 bg-white/80 rounded-lg border border-[#b2e2a8] mb-1.5">
      <div class="w-8 h-8 rounded-lg bg-teal-100 text-[#0F766E] flex items-center justify-center font-bold text-xs shrink-0">
        PDF
      </div>
      <div class="overflow-hidden">
        <p class="font-bold text-[11px] truncate text-[#0F172A]">${escapeHtml(file.name)}</p>
        <span class="text-[9px] text-slate-500">${file.size} • Documento cargado</span>
      </div>
    </div>
    <p class="font-medium text-[11px]">${escapeHtml(file.prompt)}</p>
    <span class="block text-right text-[9px] text-slate-500 mt-1">Ahora ✓✓</span>
  `;
  waMessages.appendChild(bubble);
  waMessages.scrollTop = waMessages.scrollHeight;

  showToast(`Adjuntando documento: ${file.name}`);

  setTimeout(() => {
    sendMessage(file.prompt, false, "WhatsApp Business API (Adjunto)", true);
  }, 400);
}

