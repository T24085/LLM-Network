from __future__ import annotations


DASHBOARD_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Network Control Room</title>
  <style>
    :root {
      --bg: #efe8db;
      --panel: rgba(252, 249, 244, 0.9);
      --panel-strong: rgba(255, 255, 255, 0.72);
      --ink: #172126;
      --muted: #5d6b73;
      --line: rgba(23, 33, 38, 0.12);
      --accent: #0a8f83;
      --accent-deep: #0d5e5a;
      --signal: #f26a3d;
      --shadow: 0 22px 80px rgba(11, 29, 37, 0.1);
      --radius: 26px;
    }

    * { box-sizing: border-box; }

    html { color-scheme: light; }

    body {
      margin: 0;
      min-height: 100vh;
      padding: clamp(10px, 1vw, 18px);
      font-family: "Segoe UI Variable", "Aptos", "Trebuchet MS", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(10, 143, 131, 0.14), transparent 26%),
        radial-gradient(circle at top right, rgba(242, 106, 61, 0.12), transparent 28%),
        linear-gradient(180deg, #f7f3eb 0%, #eee6da 52%, #e8e0d2 100%);
    }

    .shell {
      width: min(1880px, 100%);
      margin: 0 auto;
      padding: clamp(14px, 1vw, 20px);
      border: 1px solid rgba(255, 255, 255, 0.55);
      border-radius: 36px;
      background: rgba(255, 255, 255, 0.48);
      backdrop-filter: blur(18px);
      box-shadow: var(--shadow);
    }

    .topbar {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
      gap: 18px 22px;
      padding: clamp(20px, 1.6vw, 28px);
      border-radius: 30px;
      background:
        linear-gradient(135deg, rgba(9, 99, 93, 0.96), rgba(10, 143, 131, 0.88)),
        linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0));
      color: #f7fbfb;
      overflow: hidden;
      position: relative;
      border: 1px solid rgba(247, 251, 251, 0.12);
    }

    .topbar::after {
      content: "";
      position: absolute;
      inset: auto -6% -58% 54%;
      height: 280px;
      background: radial-gradient(circle, rgba(255,255,255,0.22), transparent 64%);
      transform: rotate(-8deg);
      pointer-events: none;
    }

    .header-copy,
    .topbar-actions {
      position: relative;
      z-index: 1;
    }

    .eyebrow {
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 12px;
      opacity: 0.8;
      margin-bottom: 12px;
    }

    h1 {
      margin: 0;
      max-width: none;
      font-size: clamp(2.2rem, 3.4vw, 3.6rem);
      line-height: 0.98;
      font-weight: 760;
    }

    .topbar p {
      max-width: 62ch;
      font-size: 0.98rem;
      line-height: 1.6;
      color: rgba(247, 251, 251, 0.84);
      margin: 12px 0 0;
    }

    .topbar-actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      align-content: start;
      gap: 10px;
    }

    .summary-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .metric {
      padding: 16px 18px;
      border-radius: 22px;
      background: var(--panel-strong);
      border: 1px solid var(--line);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.48);
      min-height: 108px;
      display: grid;
      align-content: start;
      gap: 10px;
      transform: translateY(14px);
      opacity: 0;
      animation: rise 600ms ease forwards;
    }

    .metric:nth-child(2) { animation-delay: 80ms; }
    .metric:nth-child(3) { animation-delay: 160ms; }
    .metric:nth-child(4) { animation-delay: 240ms; }

    .metric label {
      display: block;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      opacity: 0.68;
    }

    .metric strong {
      font-size: clamp(1.6rem, 2.3vw, 2.4rem);
      line-height: 1;
    }

    .metric-copy {
      font-size: 0.92rem;
      line-height: 1.5;
      color: var(--muted);
    }

    .metric .pulse {
      color: var(--accent-deep);
    }

    .workspace {
      display: grid;
      grid-template-columns: minmax(0, 1.18fr) minmax(360px, 0.82fr);
      gap: 20px;
      margin-top: 16px;
      align-items: start;
    }

    .stack {
      display: grid;
      gap: 16px;
      min-width: 0;
      align-content: start;
    }

    .inspector-stack {
      position: sticky;
      top: 14px;
      align-self: start;
    }

    .workspace > *,
    .split > *,
    .field-grid > * {
      min-width: 0;
    }

    section {
      padding: 22px;
      border-radius: var(--radius);
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.45);
      min-width: 0;
      overflow: hidden;
    }

    section h2 {
      margin: 0 0 6px;
      font-size: 1.2rem;
      line-height: 1.2;
    }

    section p {
      margin: 0 0 16px;
      color: var(--muted);
      line-height: 1.55;
      max-width: 72ch;
    }

    .split {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 0.78fr);
      gap: 12px;
      align-items: start;
    }

    .field-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    label.field {
      display: grid;
      gap: 7px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--ink);
    }

    input, textarea, select {
      width: 100%;
      border: 1px solid rgba(23, 33, 38, 0.14);
      border-radius: 16px;
      background: rgba(255,255,255,0.86);
      color: var(--ink);
      padding: 12px 14px;
      font: inherit;
      transition: border-color 160ms ease, transform 160ms ease, box-shadow 160ms ease;
    }

    textarea {
      resize: vertical;
      min-height: 140px;
    }

    input:focus, textarea:focus, select:focus {
      outline: none;
      border-color: rgba(10, 143, 131, 0.62);
      box-shadow: 0 0 0 4px rgba(10, 143, 131, 0.12);
      transform: translateY(-1px);
    }

    input[readonly] {
      background: rgba(23, 33, 38, 0.05);
      color: rgba(23, 33, 38, 0.86);
      cursor: default;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }

    button {
      appearance: none;
      border: 0;
      border-radius: 999px;
      padding: 12px 18px;
      font: inherit;
      font-weight: 680;
      cursor: pointer;
      transition: transform 160ms ease, box-shadow 160ms ease, opacity 160ms ease;
    }

    button:hover { transform: translateY(-1px); }
    button.primary {
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-deep) 100%);
      color: white;
      box-shadow: 0 14px 28px rgba(10, 143, 131, 0.22);
    }

    button.secondary {
      background: rgba(23, 33, 38, 0.06);
      color: var(--ink);
    }

    .topbar .secondary {
      background: rgba(247, 251, 251, 0.12);
      color: #f7fbfb;
      border: 1px solid rgba(247, 251, 251, 0.14);
    }

    button.signal {
      background: linear-gradient(135deg, #f26a3d 0%, #dc5a2f 100%);
      color: white;
      box-shadow: 0 14px 28px rgba(242, 106, 61, 0.18);
    }

    .subtle {
      font-size: 0.88rem;
      color: var(--muted);
    }

    .subtle-wrap {
      font-size: 0.88rem;
      color: var(--muted);
      line-height: 1.5;
      overflow-wrap: anywhere;
    }

    .chipline {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 14px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(10, 143, 131, 0.1);
      color: var(--accent-deep);
      font-size: 0.82rem;
      font-weight: 650;
    }

    .chip.warn {
      background: rgba(242, 106, 61, 0.12);
      color: #a84625;
    }

    .chip.dim {
      background: rgba(23, 33, 38, 0.08);
      color: var(--muted);
    }

    .worker-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .list {
      display: grid;
      gap: 12px;
    }

    .row {
      display: grid;
      gap: 4px;
      padding: 12px 0;
      border-top: 1px solid var(--line);
    }

    .row:first-child { border-top: 0; padding-top: 0; }

    .row-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      flex-wrap: wrap;
    }

    .code {
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: 0.88rem;
      word-break: break-word;
    }

    pre {
      margin: 0;
      padding: 16px;
      border-radius: 20px;
      background: rgba(24, 30, 43, 0.96);
      color: #e9f2f2;
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: 0.83rem;
      line-height: 1.55;
      overflow: auto;
      max-width: 100%;
      min-height: 180px;
      max-height: 380px;
    }

    .status {
      margin-top: 12px;
      min-height: 24px;
      font-size: 0.92rem;
      color: var(--muted);
    }

    .status.error { color: #a5331c; }
    .status.ok { color: var(--accent-deep); }

    .pulse {
      position: relative;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: rgba(247, 251, 251, 0.9);
      font-size: 0.88rem;
    }

    .pulse::before {
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #9ef5e5;
      box-shadow: 0 0 0 0 rgba(158, 245, 229, 0.8);
      animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(158, 245, 229, 0.8); }
      70% { box-shadow: 0 0 0 14px rgba(158, 245, 229, 0); }
      100% { box-shadow: 0 0 0 0 rgba(158, 245, 229, 0); }
    }

    @keyframes rise {
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    @media (max-width: 1480px) {
      .split {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 1320px) {
      .topbar {
        grid-template-columns: 1fr;
      }

      .workspace {
        grid-template-columns: minmax(0, 1fr);
      }

      .inspector-stack {
        position: static;
      }
    }

    @media (max-width: 1080px) {
      .summary-strip,
      .workspace,
      .split {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 720px) {
      body {
        padding: 8px;
      }

      .shell {
        padding: 10px;
        border-radius: 24px;
      }

      .topbar,
      section,
      .metric {
        border-radius: 22px;
        padding: 16px;
      }

      .topbar-actions {
        justify-content: flex-start;
      }

      .field-grid {
        grid-template-columns: 1fr;
      }

      .worker-grid {
        grid-template-columns: 1fr;
      }

      h1 {
        font-size: clamp(2rem, 11vw, 2.8rem);
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="header-copy">
        <div class="eyebrow">LLM Network</div>
        <h1>Local inference network control room</h1>
        <p>Issue user IDs, submit jobs, register worker nodes, and inspect the live coordinator state from one operator surface.</p>
      </div>
      <div class="topbar-actions">
        <button class="primary" id="refresh-all">Refresh network</button>
        <button class="secondary" id="load-models">Reload models</button>
        <button class="secondary" id="build-cli">Build CLI pack</button>
      </div>
    </header>

    <div class="summary-strip">
      <div class="metric">
        <label>Queue depth</label>
        <strong id="metric-queue">0</strong>
        <div class="metric-copy">Jobs waiting for a compatible worker claim.</div>
      </div>
      <div class="metric">
        <label>Workers online</label>
        <strong id="metric-workers">0</strong>
        <div class="metric-copy">Registered nodes visible to the local coordinator.</div>
      </div>
      <div class="metric">
        <label>Tracked users</label>
        <strong id="metric-users">0</strong>
        <div class="metric-copy">Issued identities with credit and job history on record.</div>
      </div>
      <div class="metric">
        <label>Coordinator</label>
        <strong>Connected</strong>
        <div class="pulse">Dashboard connected to local coordinator</div>
      </div>
    </div>

    <main class="workspace">
      <div class="stack">
        <section>
          <h2>Use the network</h2>
          <p>Issue an opaque identifier once, keep it private, and use that ID any time you reconnect to the network.</p>
          <div class="split">
            <div>
              <div class="chipline">
                  <span class="chip">Opaque identity</span>
                  <span class="chip">Public jobs only</span>
              </div>
              <div class="field-grid">
                <label class="field">
                  Issued user ID
                  <input id="user-id" placeholder="usr_...">
                </label>
                <label class="field">
                  Starting credits
                  <input id="user-credits" type="number" min="0" step="0.1" value="5">
                </label>
              </div>
              <div class="actions">
                <button class="primary" id="issue-user">Issue ID</button>
                <button class="secondary" id="fetch-user">Lookup ID</button>
              </div>
              <div class="status" id="user-status"></div>
            </div>
            <div>
              <div class="subtle">Approved models and local detection</div>
              <div class="chipline" id="local-detection-summary"></div>
              <div class="list" id="model-list"></div>
              <div style="height: 12px"></div>
              <div class="subtle">Detected local Ollama models on this server host</div>
              <pre id="local-model-json">[]</pre>
            </div>
          </div>
          <div style="height: 18px"></div>
          <label class="field">
            Prompt
            <textarea id="job-prompt" placeholder="Summarize the design tradeoffs of a reciprocal local-only GPU network."></textarea>
          </label>
          <div class="field-grid" style="margin-top: 12px">
            <label class="field">
              Requester ID
              <input id="job-user-id" placeholder="usr_...">
            </label>
            <label class="field">
              Quality or model
              <select id="job-model"></select>
            </label>
            <label class="field">
              Max output tokens
              <input id="job-max-output" type="number" min="1" value="350">
            </label>
            <label class="field">
              Prompt tokens override
              <input id="job-prompt-tokens" type="number" min="1" placeholder="Optional">
            </label>
          </div>
          <div class="actions">
            <button class="signal" id="submit-job">Submit job</button>
            <button class="secondary" id="refresh-job">Refresh tracked job</button>
          </div>
          <div class="status" id="job-status"></div>
        </section>

        <section>
          <h2>Operate a worker</h2>
          <p>For the local demo, the dashboard uses your issued ID plus this machine's detected GPU and approved local Ollama models. Click Start worker and the server will register it and keep polling the queue in the background on this same machine.</p>
          <div class="chipline" id="worker-detection-summary"></div>
          <div class="worker-grid">
            <label class="field">
              Worker ID
              <input id="worker-id" placeholder="Issued user ID" readonly>
            </label>
            <label class="field">
              Owner user ID
              <input id="worker-owner" placeholder="Issued user ID" readonly>
            </label>
            <label class="field">
              GPU name
              <input id="worker-gpu" placeholder="Detected from this machine" readonly>
            </label>
            <label class="field">
              VRAM GB
              <input id="worker-vram" type="number" min="1" step="0.5" value="0" readonly>
            </label>
            <label class="field">
              Approved local models
              <input id="worker-models" placeholder="Detected approved local models" readonly>
            </label>
            <label class="field">
              Estimated throughput
              <input id="worker-throughput" placeholder="Auto-estimated for detected models" readonly>
            </label>
            <label class="field">
              Poll interval seconds
              <input id="worker-poll-interval" type="number" min="0.5" step="0.5" value="2">
            </label>
          </div>
          <div class="actions">
            <button class="primary" id="start-worker">Start worker</button>
            <button class="secondary" id="stop-worker">Stop worker</button>
          </div>
          <div class="subtle">This same-machine worker loop is the simplest way to test the network locally. For multi-machine use, run the standalone worker daemon instead.</div>
          <div class="subtle-wrap" id="worker-model-hint">Detected local models will populate here when available.</div>
          <div class="status" id="worker-status"></div>
        </section>

        <section>
          <h2>CLI control pack</h2>
          <p>Generate PowerShell commands from the current dashboard values. The browser cannot execute local terminal commands directly, so this gives terminal-first users a one-click command bundle instead.</p>
          <div class="actions">
            <button class="primary" id="build-cli-pack">Generate commands</button>
            <button class="secondary" id="copy-cli-pack">Copy commands</button>
          </div>
          <div class="status" id="cli-status"></div>
          <pre id="cli-json"># CLI commands will appear here.</pre>
        </section>
      </div>

      <div class="stack inspector-stack">
        <section>
          <h2>Network Snapshot</h2>
          <p>Live ledger and worker state from the local coordinator.</p>
          <pre id="network-json">{}</pre>
        </section>

        <section>
          <h2>Tracked Job</h2>
          <p>The last job you submitted or refreshed.</p>
          <div class="subtle">AI response</div>
          <pre id="job-answer">No tracked response yet.</pre>
          <div style="height: 12px"></div>
          <div class="subtle">Raw job record</div>
          <pre id="job-json">{}</pre>
        </section>

        <section>
          <h2>Local Worker Loop</h2>
          <p>Status for the background worker running on the same machine as this server.</p>
          <pre id="local-worker-json">{}</pre>
        </section>
      </div>
    </main>
  </div>

  <script>
    const state = {
      lastJobId: "",
      models: [],
      localDetection: null,
      currentUserId: "",
      workerContext: null,
    };

    const el = (id) => document.getElementById(id);

    async function api(path, options = {}) {
      const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
      const isJson = response.headers.get("content-type")?.includes("application/json");
      const payload = isJson ? await response.json() : {};
      if (!response.ok) {
        throw new Error(payload.error || `Request failed with ${response.status}`);
      }
      return payload;
    }

    function parseCsv(text) {
      return text.split(",").map((part) => part.trim()).filter(Boolean);
    }

    function parseThroughput(text) {
      return parseCsv(text).reduce((acc, entry) => {
        const [model, value] = entry.split("=");
        if (model && value) acc[model.trim()] = Number(value.trim());
        return acc;
      }, {});
    }

    function setStatus(id, message, kind = "ok") {
      const node = el(id);
      node.textContent = message;
      node.className = `status ${kind}`;
    }

    function writeJson(id, payload) {
      el(id).textContent = JSON.stringify(payload, null, 2);
    }

    function renderTrackedJob(payload) {
      writeJson("job-json", payload);
      const answer = payload?.result?.output_text?.trim();
      const errorMessage = payload?.result?.error_message?.trim();
      if (answer) {
        el("job-answer").textContent = answer;
      } else if (errorMessage) {
        el("job-answer").textContent = `Worker error: ${errorMessage}`;
      } else if (payload?.status === "queued" || payload?.status === "assigned") {
        el("job-answer").textContent = "Waiting for a worker response.";
      } else {
        el("job-answer").textContent = "No tracked response yet.";
      }
    }

    function renderWorkerContext(payload) {
      state.workerContext = payload || {};
      const summary = el("worker-detection-summary");
      summary.innerHTML = "";
      const workerId = payload?.suggested_worker_id || state.currentUserId || "";
      const ownerUserId = payload?.suggested_owner_user_id || state.currentUserId || "";
      const gpuName = payload?.suggested_gpu_name || "";
      const vramGb = Number(payload?.suggested_vram_gb || 0);
      const models = payload?.suggested_installed_models || [];
      const throughput = payload?.suggested_benchmark_tokens_per_second || {};

      if (workerId) {
        el("worker-id").value = workerId;
      }
      if (ownerUserId) {
        el("worker-owner").value = ownerUserId;
      }
      el("worker-gpu").value = gpuName;
      el("worker-vram").value = vramGb > 0 ? String(vramGb) : "";
      el("worker-models").value = models.join(", ");
      el("worker-throughput").value = Object.entries(throughput)
        .map(([model, value]) => `${model}=${value}`)
        .join(", ");

      if (payload?.hardware_detection?.detected) {
        summary.appendChild(buildChip(`GPU detected`, "ok"));
        summary.appendChild(buildChip(`${gpuName || "GPU"}${vramGb ? ` - ${vramGb} GB` : ""}`, "dim"));
      } else {
        summary.appendChild(buildChip(payload?.hardware_detection?.error || "GPU not detected", "warn"));
      }
      if (models.length) {
        summary.appendChild(buildChip(`${models.length} approved local models`, "ok"));
      } else {
        summary.appendChild(buildChip("No approved local models ready", "warn"));
      }
    }

    function syncIdentityFields(userId) {
      const value = String(userId || "").trim();
      if (!value) {
        return;
      }
      el("user-id").value = value;
      el("job-user-id").value = value;
      el("worker-owner").value = value;
      el("worker-id").value = value;
      state.currentUserId = value;
      localStorage.setItem("ollama_network_user_id", value);
      if (state.workerContext) {
        state.workerContext.suggested_worker_id = value;
        state.workerContext.suggested_owner_user_id = value;
      }
    }

    function shellQuote(value) {
      const text = String(value ?? "");
      return `"${text.replace(/"/g, '\\"')}"`;
    }

    async function refreshModels() {
      const payload = await api("/models");
      state.models = payload.models;
      state.localDetection = payload.local_detection;
      const list = el("model-list");
      const select = el("job-model");
      const summary = el("local-detection-summary");
      const localPre = el("local-model-json");
      list.innerHTML = "";
      select.innerHTML = "";
      summary.innerHTML = "";
      localPre.textContent = JSON.stringify(payload.local_detection?.detected_models || [], null, 2);

      [
        { value: "auto", label: "Auto - strongest installed on the worker" },
        { value: "good", label: "Good - lower-cost local model" },
        { value: "better", label: "Better - stronger local model" },
        { value: "best", label: "Best - premium local model" },
      ].forEach((item) => {
        const option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.label;
        select.appendChild(option);
      });

      if (payload.local_detection?.ollama_available) {
        const approvedCount = payload.local_detection.approved_local_models.length;
        const allCount = payload.local_detection.detected_models.length;
        summary.appendChild(buildChip(`Ollama detected on server host`, "ok"));
        summary.appendChild(buildChip(`${approvedCount} approved local`, approvedCount ? "ok" : "warn"));
        summary.appendChild(buildChip(`${allCount} total local`, "dim"));
      } else {
        summary.appendChild(buildChip(payload.local_detection?.error || "Ollama not detected", "warn"));
      }

      payload.models.forEach((model) => {
        const row = document.createElement("div");
        row.className = "row";
        const installLabel = model.installed_locally ? "installed on server host" : "not installed locally";
        row.innerHTML = `
          <div class="row-head">
            <strong>${model.tag}</strong>
            <span class="subtle">${model.min_vram_gb} GB minimum</span>
          </div>
          <div class="subtle">${model.family} family · ${model.runtime} · ${installLabel}</div>
        `;
        list.appendChild(row);
        const option = document.createElement("option");
        option.value = model.tag;
        option.textContent = `${model.tag} - exact`;
        select.appendChild(option);
      });

      const approvedLocal = payload.local_detection?.approved_local_models || [];
      const detectedModels = payload.local_detection?.detected_models || [];
      if (approvedLocal.length) {
        el("worker-models").value = approvedLocal.join(", ");
        el("worker-model-hint").textContent = `Detected approved local models on the API server host: ${approvedLocal.join(", ")}.`;
        if (!el("job-model").value) {
          el("job-model").value = "auto";
        }
      } else if (detectedModels.length) {
        el("worker-models").value = "";
        el("worker-model-hint").textContent = `Local Ollama models were detected, but none are in the approved network catalog: ${detectedModels.join(", ")}.`;
      } else {
        el("worker-model-hint").textContent = "No local Ollama models detected on the API server host yet.";
      }
    }

    async function refreshWorkerContext() {
      const payload = await api("/worker-context");
      if (state.currentUserId) {
        payload.suggested_worker_id = state.currentUserId;
        payload.suggested_owner_user_id = state.currentUserId;
      }
      renderWorkerContext(payload);
    }

    function buildChip(label, kind) {
      const chip = document.createElement("span");
      chip.className = `chip ${kind === "warn" ? "warn" : kind === "dim" ? "dim" : ""}`.trim();
      chip.textContent = label;
      return chip;
    }

    async function refreshNetwork() {
      const payload = await api("/network");
      writeJson("network-json", payload);
      writeJson("local-worker-json", payload.local_workers || {});
      el("metric-queue").textContent = payload.queued_jobs.length;
      el("metric-workers").textContent = Object.keys(payload.workers).length;
      el("metric-users").textContent = payload.user_count;
      return payload;
    }

    async function refreshTrackedJob() {
      if (!state.lastJobId) {
        setStatus("job-status", "No tracked job yet.", "ok");
        el("job-answer").textContent = "No tracked response yet.";
        return;
      }
      const payload = await api(`/jobs/${state.lastJobId}`);
      renderTrackedJob(payload);
      setStatus("job-status", `Tracked job ${payload.job_id} is ${payload.status}.`, "ok");
    }

    async function registerUser() {
      const payload = await api("/users/issue", {
        method: "POST",
        body: JSON.stringify({
          starting_credits: Number(el("user-credits").value || 0),
        }),
      });
      syncIdentityFields(payload.user_id);
      await refreshWorkerContext();
      setStatus("user-status", `Issued ${payload.user_id}. Balance: ${Number(payload.balance).toFixed(4)} credits. Save this identifier.`, "ok");
      await refreshNetwork();
    }

    async function fetchUser() {
      const userId = el("user-id").value.trim();
      const payload = await api(`/users/${encodeURIComponent(userId)}`);
      syncIdentityFields(payload.user_id);
      await refreshWorkerContext();
      setStatus("user-status", `Loaded ${payload.user_id}. Balance: ${Number(payload.balance).toFixed(4)} credits.`, "ok");
    }

    async function hydrateIdentity() {
      const payload = await api("/identity-context");
      const stored = localStorage.getItem("ollama_network_user_id");
      const selected = stored || payload.auto_selected_user_id || payload.last_active_user_id || "";
      if (!selected) {
        return;
      }
      syncIdentityFields(selected);
      await refreshWorkerContext();
      try {
        const user = await api(`/users/${encodeURIComponent(selected)}`);
        setStatus("user-status", `Loaded ${user.user_id}. Balance: ${Number(user.balance).toFixed(4)} credits.`, "ok");
      } catch (_error) {
        setStatus("user-status", `Stored ID ${selected} was not found on this server yet.`, "error");
      }
    }

    async function submitJob() {
      const body = {
        requester_user_id: el("job-user-id").value.trim(),
        model_tag: el("job-model").value,
        prompt: el("job-prompt").value,
        max_output_tokens: Number(el("job-max-output").value || 0),
      };
      const promptTokens = el("job-prompt-tokens").value.trim();
      if (promptTokens) body.prompt_tokens = Number(promptTokens);
      const payload = await api("/jobs", {
        method: "POST",
        body: JSON.stringify(body),
      });
      state.lastJobId = payload.job_id;
      renderTrackedJob(payload);
      setStatus("job-status", `Queued ${payload.job_id} with ${payload.reserved_credits} reserved credits.`, "ok");
      await refreshNetwork();
    }

    async function startWorker() {
      const ownerUserId = state.currentUserId || el("worker-owner").value.trim() || el("user-id").value.trim();
      if (!ownerUserId) {
        throw new Error("Issue or load a user ID first so the worker has an owner.");
      }
      const workerId = ownerUserId;
      const gpuName = el("worker-gpu").value.trim();
      const installedModels = parseCsv(el("worker-models").value);
      const throughput = parseThroughput(el("worker-throughput").value);
      if (!gpuName) {
        throw new Error("No GPU was detected on this machine yet.");
      }
      if (!installedModels.length) {
        throw new Error("No approved local Ollama models were detected for this machine.");
      }
      el("worker-owner").value = ownerUserId;
      el("worker-id").value = workerId;
      const payload = await api("/workers/start-local", {
        method: "POST",
        body: JSON.stringify({
          worker_id: workerId,
          owner_user_id: ownerUserId,
          gpu_name: gpuName,
          vram_gb: Number(el("worker-vram").value || 0),
          installed_models: installedModels,
          benchmark_tokens_per_second: throughput,
          poll_interval_seconds: Number(el("worker-poll-interval").value || 2),
          runtime: "ollama",
          allows_cloud_fallback: false,
        }),
      });
      writeJson("local-worker-json", payload.loop || {});
      setStatus("worker-status", `Worker ${payload.worker.worker_id} is polling locally in the background.`, "ok");
      await refreshNetwork();
    }

    async function stopWorker() {
      const workerId = el("worker-id").value.trim() || el("worker-owner").value.trim() || state.currentUserId || el("user-id").value.trim();
      if (!workerId) {
        throw new Error("Load a user ID first so the dashboard knows which worker to stop.");
      }
      el("worker-id").value = workerId;
      const payload = await api(`/workers/${encodeURIComponent(workerId)}/stop-local`, {
        method: "POST",
        body: JSON.stringify({}),
      });
      writeJson("local-worker-json", payload.loop || {});
      setStatus("worker-status", `Worker ${workerId} was stopped.`, "ok");
      await refreshNetwork();
    }

    function buildCliPack() {
      const origin = window.location.origin;
      const userId = el("user-id").value.trim() || "usr_your_id_here";
      const requesterId = el("job-user-id").value.trim() || userId || "usr_your_id_here";
      const startingCredits = Number(el("user-credits").value || 0);
      const modelTag = el("job-model").value || "auto";
      const prompt = el("job-prompt").value.trim() || "Summarize the network state.";
      const maxOutput = Number(el("job-max-output").value || 0);
      const promptTokens = el("job-prompt-tokens").value.trim();
      const workerId = el("worker-id").value.trim() || state.currentUserId || userId || "usr_your_id_here";
      const workerOwner = el("worker-owner").value.trim() || state.currentUserId || "usr_your_id_here";
      const gpuName = el("worker-gpu").value.trim() || "Detected GPU";
      const vramGb = Number(el("worker-vram").value || 0);
      const models = parseCsv(el("worker-models").value);
      const modelArgs = (models.length ? models : [modelTag]).map((item) => `--model ${shellQuote(item)}`).join(" ");
      const throughputArgs = parseCsv(el("worker-throughput").value).map((item) => `--tps ${shellQuote(item)}`).join(" ");
      const promptTokenArg = promptTokens ? ` --prompt-tokens ${promptTokens}` : "";

        const commands = [
          `$env:PYTHONPATH='src'; python -m ollama_network.server --host 127.0.0.1 --port ${window.location.port || 8000}`,
          `$env:PYTHONPATH='src'; python -m ollama_network.cli --server-url ${shellQuote(origin)} issue-user --starting-credits ${startingCredits}`,
          `# Save the issued user_id from the command above and reuse it on future sessions`,
          `$env:PYTHONPATH='src'; python -m ollama_network.cli --server-url ${shellQuote(origin)} user --user-id ${shellQuote(userId)}`,
          `$env:PYTHONPATH='src'; python -m ollama_network.cli --server-url ${shellQuote(origin)} register-worker --worker-id ${shellQuote(workerId)} --owner-user-id ${shellQuote(workerOwner)} --gpu-name ${shellQuote(gpuName)} --vram-gb ${vramGb} ${modelArgs}${throughputArgs ? ` ${throughputArgs}` : ""}`,
          `$env:PYTHONPATH='src'; python -m ollama_network.cli --server-url ${shellQuote(origin)} submit-job --requester-user-id ${shellQuote(requesterId)} --model-tag ${shellQuote(modelTag)} --prompt ${shellQuote(prompt)} --max-output-tokens ${maxOutput}${promptTokenArg}`,
            `$env:PYTHONPATH='src'; python -m ollama_network.worker_daemon --server-url ${shellQuote(origin)} --worker-id ${shellQuote(workerId)} --owner-user-id ${shellQuote(workerOwner)} --gpu-name ${shellQuote(gpuName)} --vram-gb ${vramGb} ${modelArgs}${throughputArgs ? ` ${throughputArgs}` : ""} --poll-interval ${Number(el("worker-poll-interval").value || 2)}`,
            `$env:PYTHONPATH='src'; python -m ollama_network.cli --server-url ${shellQuote(origin)} network`,
          ];

      el("cli-json").textContent = commands.join("\\n\\n");
      setStatus("cli-status", "CLI command pack generated from the current form values.", "ok");
      return commands.join("\\n\\n");
    }

    async function copyCliPack() {
      const text = buildCliPack();
      await navigator.clipboard.writeText(text);
      setStatus("cli-status", "CLI command pack copied to the clipboard.", "ok");
    }

    function bind() {
      el("refresh-all").addEventListener("click", () => refreshNetwork().catch(showGlobalError));
      el("load-models").addEventListener("click", () => Promise.all([refreshModels(), refreshWorkerContext()]).catch(showGlobalError));
      el("build-cli").addEventListener("click", () => {
        buildCliPack();
        document.getElementById("cli-json").scrollIntoView({ behavior: "smooth", block: "start" });
      });
      el("issue-user").addEventListener("click", () => registerUser().catch((error) => setStatus("user-status", error.message, "error")));
      el("fetch-user").addEventListener("click", () => fetchUser().catch((error) => setStatus("user-status", error.message, "error")));
      el("submit-job").addEventListener("click", () => submitJob().catch((error) => setStatus("job-status", error.message, "error")));
      el("refresh-job").addEventListener("click", () => refreshTrackedJob().catch((error) => setStatus("job-status", error.message, "error")));
      el("start-worker").addEventListener("click", () => startWorker().catch((error) => setStatus("worker-status", error.message, "error")));
      el("stop-worker").addEventListener("click", () => stopWorker().catch((error) => setStatus("worker-status", error.message, "error")));
      el("build-cli-pack").addEventListener("click", () => buildCliPack());
      el("copy-cli-pack").addEventListener("click", () => copyCliPack().catch((error) => setStatus("cli-status", error.message, "error")));
    }

    function showGlobalError(error) {
      setStatus("user-status", error.message, "error");
      setStatus("job-status", error.message, "error");
      setStatus("worker-status", error.message, "error");
      setStatus("cli-status", error.message, "error");
    }

    async function boot() {
      bind();
      await refreshModels();
      await hydrateIdentity();
      await refreshWorkerContext();
      await refreshNetwork();
      renderTrackedJob({});
      writeJson("local-worker-json", {});
      buildCliPack();
      setInterval(() => {
        refreshNetwork().catch(() => {});
        if (state.lastJobId) {
          refreshTrackedJob().catch(() => {});
        }
      }, 4000);
    }

    boot().catch(showGlobalError);
  </script>
</body>
</html>
"""

