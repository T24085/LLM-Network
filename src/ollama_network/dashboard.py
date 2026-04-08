from __future__ import annotations

import json

from .branding import load_logo_data_url


_DEFAULT_FIREBASE_CONFIG = {
    "apiKey": "",
    "authDomain": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
}


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Network Control Room</title>
  <style>
    :root{--bg:#efe8db;--panel:#fcf9f4;--line:rgba(23,33,38,.12);--text:#172126;--muted:#5d6b73;--teal:#0a8f83;--deep:#0d5e5a;--signal:#f26a3d;--ink:#181e2b}
    *{box-sizing:border-box} body{margin:0;padding:16px;font-family:Segoe UI,Aptos,sans-serif;background:var(--bg);color:var(--text)}
    button,input,select,textarea{font:inherit} button{cursor:pointer}
    .shell{max-width:1480px;margin:0 auto;display:grid;gap:16px}
    .card{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 14px 36px rgba(23,33,38,.06)}
    .hero{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:start;background:linear-gradient(135deg,var(--deep),var(--teal));color:#fff}
    .hero-brand{display:flex;gap:18px;align-items:flex-start}
    .hero-logo{width:110px;max-width:24vw;height:auto;display:block;filter:drop-shadow(0 12px 24px rgba(0,0,0,.18))}
    .hero-copy{display:grid;gap:8px}
    .actions,.chips{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
    .grid{display:grid;grid-template-columns:minmax(0,1fr);gap:16px;align-items:start}
    .stack{display:grid;gap:16px}
    .two{display:grid;grid-template-columns:repeat(2,minmax(220px,1fr));gap:12px}
    .three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
    label{display:grid;gap:6px;font-size:.8rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#45545b}
    input,textarea,select{width:100%;padding:11px 12px;border:1px solid rgba(23,33,38,.14);border-radius:12px;background:#fff;color:var(--text)}
    input[readonly]{background:#f0eeea} textarea{min-height:120px;resize:vertical}
    .button{border:0;border-radius:999px;padding:10px 16px;font-weight:600}
    .primary{background:var(--teal);color:#fff}.secondary{background:#e7e1d7;color:var(--text)}.signal{background:var(--signal);color:#fff}
    .chip{padding:6px 10px;border-radius:999px;background:rgba(10,143,131,.1);color:var(--deep);font-size:.84rem}.warn{background:rgba(242,106,61,.12);color:#a84625}
    .status{min-height:22px;color:var(--muted)} .error{color:#a5331c}.ok{color:var(--deep)}
    .hidden{display:none!important} .subtle{font-size:.84rem;color:var(--muted)} h1,h2,h3{line-height:1.05} h2{margin:0 0 14px}
    pre{margin:0;padding:14px;border-radius:14px;background:var(--ink);color:#e9f2f2;overflow:auto;max-height:420px;min-height:120px;font-size:.82rem;line-height:1.55}
    .model-list,.admin-jobs,.account-list,.prompt-history{display:grid;gap:10px}
    .artifact-list{display:grid;gap:10px}
    .stats-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .stats-card{padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .stats-card strong{display:block;font-size:1.15rem}
    .stats-card span{display:block;color:var(--muted);font-size:.82rem;margin-top:4px}
    .history-shell{display:grid;gap:14px}
    .conversation-card{padding:0;overflow:hidden}
    .conversation-card details{border:none;background:transparent;padding:0}
    .conversation-card summary{list-style:none;cursor:pointer;padding:14px 16px}
    .conversation-card summary::-webkit-details-marker{display:none}
    .conversation-head{display:grid;gap:8px}
    .conversation-head-top{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
    .conversation-head-copy{display:grid;gap:6px}
    .conversation-actions{display:flex;flex-wrap:wrap;gap:8px}
    .conversation-body{display:grid;gap:12px;padding:0 16px 16px}
    .conversation-message-list{display:grid;gap:10px}
    .conversation-message{padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .conversation-message.user{border-color:rgba(10,143,131,.18);background:rgba(10,143,131,.04)}
    .conversation-message.assistant{border-color:rgba(23,33,38,.08)}
    .conversation-message pre{margin-top:8px;max-height:220px;min-height:0}
    .conversation-section-title{display:flex;justify-content:space-between;gap:12px;align-items:flex-end}
    .archived-shell{display:grid;gap:10px}
    .archived-shell details{padding:0}
    .archived-shell summary{padding:14px 16px}
    .artifact-card{padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .artifact-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:8px}
    .artifact-head strong{font-size:.95rem}
    .artifact-meta{font-size:.8rem;color:var(--muted)}
    .artifact-preview{max-height:260px;min-height:96px}
    .row,.job-card,.account-item{padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .job-card-queued{border-color:rgba(242,106,61,.45);background:linear-gradient(180deg,rgba(242,106,61,.09),rgba(255,255,255,.98));box-shadow:0 10px 22px rgba(242,106,61,.08)}
    .job-card-assigned{border-color:rgba(10,143,131,.4);background:linear-gradient(180deg,rgba(10,143,131,.10),rgba(255,255,255,.98));box-shadow:0 10px 22px rgba(10,143,131,.08)}
    .job-card-completed{border-color:rgba(15,106,84,.22);background:linear-gradient(180deg,rgba(15,106,84,.05),rgba(255,255,255,.98))}
    .job-card-failed{border-color:rgba(191,74,43,.28);background:linear-gradient(180deg,rgba(191,74,43,.07),rgba(255,255,255,.98))}
    .job-card-canceled{border-color:rgba(108,117,125,.22);background:linear-gradient(180deg,rgba(108,117,125,.06),rgba(255,255,255,.98))}
    .job-status-banner{display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:999px;font-size:.8rem;font-weight:700}
    .job-status-banner.queued{background:rgba(242,106,61,.14);color:#b24a24}
    .job-status-banner.assigned{background:rgba(10,143,131,.14);color:var(--deep)}
    .job-status-banner.completed{background:rgba(15,106,84,.12);color:#0c5a47}
    .job-status-banner.failed{background:rgba(191,74,43,.14);color:#a34528}
    .job-status-banner.canceled{background:rgba(108,117,125,.14);color:#5e666d}
    .row{display:flex;justify-content:space-between;gap:14px;align-items:flex-start}.row-head{display:grid;gap:2px}
    .checkline{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .checkline input{width:auto;margin-top:2px}
    .job-card h3,.account-item h3{margin:0 0 8px;font-size:1rem}
    .job-card p,.account-item p{margin:0;color:var(--muted);line-height:1.5}
    .job-meta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
    .workspace-head{display:grid;gap:12px;align-items:start;margin-bottom:0}
    .elastic-tabs{position:relative;display:inline-flex;align-items:center;padding:4px;background:#fff;border-radius:999px;box-shadow:0 10px 26px rgba(23,33,38,.08);border:1px solid rgba(23,33,38,.08);overflow:hidden}
    .elastic-selector{position:absolute;left:4px;top:4px;bottom:4px;width:0;border-radius:999px;background:linear-gradient(135deg,#0a8f83 0%,#0d5e5a 100%);transition:left .45s cubic-bezier(0.68,-0.55,0.265,1.55),width .45s cubic-bezier(0.68,-0.55,0.265,1.55),opacity .2s ease;box-shadow:0 10px 24px rgba(10,143,131,.22);opacity:0}
    .workspace-tabs{align-self:start}
    .workspace-tab,.admin-job-tab{position:relative;z-index:1;border:none;border-radius:999px;padding:11px 16px;background:transparent;color:var(--muted);font-weight:700;letter-spacing:.01em;transition:color .3s ease}
    .workspace-tab.active,.admin-job-tab.active{color:var(--deep)}
    .elastic-tabs.ready .elastic-selector{opacity:1}
    .elastic-tabs[data-highlight='true'] .workspace-tab.active,.elastic-tabs[data-highlight='true'] .admin-job-tab.active{color:#fff}
    .workspace-frame{border:none;border-radius:0;background:transparent;padding:18px 0 0;margin-top:0}
    .tab-panel{display:grid;gap:16px}
    .tab-panel[hidden]{display:none}
    .job-meta-strip{display:grid;gap:6px;padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:#fff}
    .admin-jobs-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end}
    .admin-job-tabs{display:inline-flex}
    .job-card details{border:none;padding:0;background:transparent}
    .job-card summary{list-style:none;cursor:pointer}
    .job-card summary::-webkit-details-marker{display:none}
    .job-summary{display:grid;gap:8px}
    .job-summary-top{display:flex;justify-content:space-between;gap:14px;align-items:flex-start}
    .job-summary-copy{display:grid;gap:6px}
    .job-collapse{color:var(--muted);font-size:.84rem;font-weight:700}
    .job-body{display:grid;gap:10px;padding-top:10px}
    .drawer-shell{position:fixed;inset:0;display:none;z-index:50}
    .drawer-shell.open{display:block}
    .drawer-backdrop{position:absolute;inset:0;background:rgba(10,16,22,.22);backdrop-filter:blur(2px)}
    .drawer{position:absolute;right:0;top:0;height:100%;width:min(560px,94vw);background:var(--panel);border-left:1px solid var(--line);box-shadow:-24px 0 48px rgba(23,33,38,.18);padding:22px;display:grid;gap:14px;transform:translateX(100%);transition:transform .22s ease}
    .drawer-shell.open .drawer{transform:translateX(0)}
    .drawer-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
    .drawer-body{display:grid;gap:14px;overflow:auto;padding-right:4px}
    .floating-rail{position:fixed;right:22px;top:50%;transform:translateY(-50%);display:grid;gap:10px;z-index:30}
    .rail-button{border:1px solid var(--line);border-radius:999px;padding:10px 16px;background:var(--panel);box-shadow:0 12px 28px rgba(23,33,38,.12)}
    details{border:1px solid var(--line);border-radius:16px;background:#fff;padding:14px}
    summary{cursor:pointer;font-weight:700;color:var(--text)}
    @media (max-width:1120px){.hero,.grid,.two,.three,.stats-grid{grid-template-columns:1fr}.row,.workspace-head{flex-direction:column}}
  </style>
</head>
<body>
  <div class="shell">
    <section class="card hero">
      <div class="hero-brand">
        <img src="__LOGO_DATA_URL__" alt="LLM Network logo" class="hero-logo">
        <div class="hero-copy">
          <div style="text-transform:uppercase;letter-spacing:.18em;font-size:12px;opacity:.8">LLM Network</div>
          <h1 style="margin:0;font-size:clamp(2rem,3vw,3.2rem)">LLM Network Control Room</h1>
          <p style="margin:0;max-width:64ch">Sign in with Google to unlock your bound network account, submit jobs, inspect outputs, and operate local workers. Admin accounts can optionally let their local worker service the full queue, including their own prompts.</p>
        </div>
      </div>
      <div class="actions">
        <div id="session-pill" class="chip">Sign in required</div>
        <button id="sign-in" class="button primary">Sign in with Google</button>
        <button id="sign-out" class="button secondary hidden">Sign out</button>
        <button id="refresh-all" class="button secondary">Refresh network</button>
      </div>
    </section>

    <section id="auth-panel" class="card">
      <div class="chips">
        <span class="chip">Google login required</span>
        <span class="chip">Firebase token verified</span>
        <span class="chip">Stable network identity</span>
      </div>
      <p>Project: <strong id="auth-project">llm-network</strong></p>
      <p>Your Google account is bound to one stable network user id on first login. Admin accounts also unlock the queue override for local worker testing.</p>
      <div class="actions">
        <button id="sign-in-panel" class="button primary">Continue with Google</button>
      </div>
      <div id="auth-status" class="status">Waiting for sign-in.</div>
    </section>

    <div id="dashboard-shell" class="hidden stack">
      <section class="card">
        <div class="chips">
          <span class="chip">Queue <strong id="metric-queue" style="margin-left:6px">0</strong></span>
          <span class="chip">Workers <strong id="metric-workers" style="margin-left:6px">0</strong></span>
          <span class="chip">Users <strong id="metric-users" style="margin-left:6px">0</strong></span>
          <span id="admin-pill" class="chip hidden">Admin session</span>
        </div>
      </section>

      <section id="admin-panel" class="card hidden">
        <div class="actions" style="justify-content:space-between">
          <div>
            <h2>Admin Console</h2>
            <div class="subtle">Review accounts, inspect queued and completed jobs, and adjust credits. The worker override below only activates when you explicitly turn it on for your worker.</div>
          </div>
          <button id="admin-refresh" class="button primary">Refresh admin data</button>
        </div>
        <div class="three">
          <label>User account<select id="admin-credit-user"></select></label>
          <label>Credit adjustment<input id="admin-credit-amount" type="number" step="1" value="100"></label>
          <label>Reason<input id="admin-credit-note" value="manual admin credit grant"></label>
        </div>
        <div class="actions">
          <button id="admin-adjust-credits" class="button signal">Apply adjustment</button>
        </div>
        <div id="admin-status" class="status"></div>
        <div id="admin-summary" class="chips"></div>
        <div class="admin-jobs-head">
          <div>
            <h3 style="margin:0">Jobs</h3>
            <div class="subtle">Filter queued and completed work, then expand only the items you want to inspect.</div>
          </div>
          <div class="admin-job-tabs elastic-tabs" role="tablist" aria-label="Admin job filters" data-elastic-tabs="admin-jobs">
            <div class="elastic-selector"></div>
            <button id="admin-job-tab-all" class="admin-job-tab active" data-admin-job-tab="all" role="tab" aria-selected="true">All</button>
            <button id="admin-job-tab-queued" class="admin-job-tab" data-admin-job-tab="queued" role="tab" aria-selected="false">Queued</button>
            <button id="admin-job-tab-completed" class="admin-job-tab" data-admin-job-tab="completed" role="tab" aria-selected="false">Completed</button>
          </div>
        </div>
        <div id="admin-jobs" class="admin-jobs"></div>
      </section>

      <div class="grid">
        <div class="stack">
          <section class="card">
            <div class="workspace-head">
              <div>
                <h2>Workspace</h2>
                <div class="subtle">Switch between submitting prompts to the network and running your local worker. The noisy diagnostics stay in the side panels.</div>
              </div>
              <div class="workspace-tabs elastic-tabs" role="tablist" aria-label="Workspace sections" data-elastic-tabs="workspace">
                <div class="elastic-selector"></div>
                <button id="tab-network" class="workspace-tab active" data-workspace-tab="network" role="tab" aria-selected="true" aria-controls="tab-panel-network">Use the network</button>
                <button id="tab-worker" class="workspace-tab" data-workspace-tab="worker" role="tab" aria-selected="false" aria-controls="tab-panel-worker" tabindex="-1">Operate a worker</button>
              </div>
            </div>

            <div class="workspace-frame">
            <div id="tab-panel-network" class="tab-panel" role="tabpanel" aria-labelledby="tab-network">
              <h3 style="margin:0">Use the network</h3>
            <div class="two">
              <label>Network user ID<input id="user-id" readonly></label>
              <label>Balance<input id="user-balance" readonly></label>
            </div>
            <div class="actions">
              <button id="refresh-user" class="button secondary">Refresh balance</button>
              <button id="load-models" class="button secondary">Refresh network options</button>
              <button id="open-network-drawer" class="button secondary">Open network panel</button>
            </div>
            <div id="user-status" class="status"></div>
            <div id="local-detection-summary" class="chips"></div>
            <div class="two">
              <label>Conversation<select id="conversation-select"></select></label>
              <label>Conversation controls<div class="actions"><button id="new-conversation" class="button secondary" type="button">Start new conversation</button><button id="refresh-conversations" class="button secondary" type="button">Refresh conversations</button></div></label>
            </div>
            <details>
              <summary>Current conversation</summary>
              <div style="height:12px"></div>
              <div id="conversation-meta" class="subtle">No conversation selected.</div>
              <div style="height:10px"></div>
              <div id="conversation-thread" class="conversation-message-list"></div>
            </details>
            <details>
              <summary>Advanced model availability</summary>
              <div style="height:12px"></div>
              <div class="subtle" style="margin-bottom:12px">You usually do not need this list. The network can stay on <code>auto</code> unless you want to force a specific model.</div>
              <div id="model-list" class="model-list"></div>
            </details>
            <label>Prompt<textarea id="job-prompt" placeholder="Summarize the design tradeoffs of a reciprocal local-only GPU network."></textarea></label>
            <div class="two">
              <label>Requester ID<input id="job-user-id" readonly></label>
              <label>Model<select id="job-model"></select></label>
              <label>Max output tokens<input id="job-max-output" type="number" min="1" value="350"></label>
              <label>Prompt tokens override<input id="job-prompt-tokens" type="number" min="1" placeholder="Optional"></label>
            </div>
            <div class="actions">
              <button id="submit-job" class="button signal">Submit job</button>
              <button id="refresh-job" class="button secondary">Refresh tracked job</button>
              <button id="open-job-drawer" class="button secondary">Open job panel</button>
            </div>
            <div id="job-status" class="status"></div>
            <div id="job-meta-summary" class="job-meta-strip subtle hidden"></div>
            <div id="job-artifact-actions" class="actions hidden">
              <button id="create-artifacts" class="button secondary">Create files</button>
              <button id="download-artifacts" class="button secondary">Download zip</button>
            </div>
            <div id="job-artifacts" class="artifact-list hidden"></div>
            <details id="job-raw-output" class="hidden">
              <summary>Raw model output</summary>
              <div style="height:10px"></div>
              <pre id="job-answer">No tracked response yet.</pre>
            </details>
            <details id="prompt-history-wrap" open>
              <summary>Conversation history</summary>
              <div style="height:12px"></div>
              <div class="conversation-section-title">
                <div>
                  <h3 style="margin:0">Saved conversations</h3>
                  <div class="subtle">Server-side history for this account. Expanding a thread shows the full prompt and response trail, not browser-only state.</div>
                </div>
                <button id="refresh-history" class="button secondary">Refresh history</button>
              </div>
              <div style="height:12px"></div>
              <div id="prompt-history" class="history-shell"></div>
              <div id="archived-history" class="archived-shell"></div>
            </details>
            </div>

            <div id="tab-panel-worker" class="tab-panel hidden" hidden role="tabpanel" aria-labelledby="tab-worker">
            <h3 style="margin:0">Operate a worker</h3>
            <div id="worker-detection-summary" class="chips"></div>
            <div class="two">
              <label>Worker ID<input id="worker-id" readonly></label>
              <label>Owner user ID<input id="worker-owner" readonly></label>
              <label>GPU name<input id="worker-gpu" readonly></label>
              <label>Dedicated VRAM GB<input id="worker-vram" readonly></label>
              <label>Host RAM GB<input id="worker-system-ram" readonly></label>
              <label>Approved local models<input id="worker-models" readonly></label>
              <label>Estimated throughput<input id="worker-throughput" readonly></label>
              <label>Poll interval seconds<input id="worker-poll-interval" type="number" min="0.5" step="0.5" value="2"></label>
            </div>
            <div id="worker-excluded-models" class="job-meta-strip subtle hidden"></div>
            <div id="admin-override-wrap" class="hidden">
              <label class="checkline" style="text-transform:none;letter-spacing:0;color:var(--text);font-size:.94rem;font-weight:600">
                <input id="worker-admin-override" type="checkbox">
                <span>
                  Allow this admin worker to claim any queued prompt, including my own.
                  <div class="subtle">Use this when you want to inspect how prompts resolve for users or preview your own prompts through the same worker path.</div>
                </span>
              </label>
            </div>
            <div class="subtle">Standard workers only pick up jobs from other users. If you queue your own prompt and your worker has the same owner id, it will stay queued unless admin self-serve is enabled.</div>
            <div class="actions">
              <button id="start-worker" class="button primary">Start worker</button>
              <button id="stop-worker" class="button secondary">Stop worker</button>
              <button id="run-worker-once" class="button secondary">Run one cycle now</button>
              <button id="open-worker-drawer" class="button secondary">Open worker panel</button>
            </div>
            <div id="worker-status" class="status"></div>
            <div id="worker-queue-status" class="job-meta-strip subtle hidden"></div>
            </div>
            </div>
          </section>
        </div>

        <div class="stack hidden">
          <section class="card"><h2>Network Snapshot</h2><pre id="network-json">{}</pre></section>
          <section class="card"><h2>Tracked Job</h2><pre id="job-answer">No tracked response yet.</pre><div style="height:10px"></div><pre id="job-json">{}</pre></section>
          <section class="card"><h2>Local Worker Loop</h2><pre id="local-worker-json">{}</pre></section>
        </div>
      </div>
    </div>
  </div>

  <div id="floating-rail" class="floating-rail hidden">
    <button class="rail-button" data-drawer-target="network">Network</button>
    <button class="rail-button" data-drawer-target="job">Job</button>
    <button class="rail-button" data-drawer-target="worker">Worker</button>
    <button class="rail-button" data-drawer-target="worker-stats">Worker Stats</button>
  </div>

  <div id="drawer-shell" class="drawer-shell">
    <div id="drawer-backdrop" class="drawer-backdrop"></div>
    <aside class="drawer">
      <div class="drawer-head">
        <div>
          <div id="drawer-eyebrow" class="subtle">Diagnostics</div>
          <h2 id="drawer-title" style="margin:4px 0 0">Panel</h2>
        </div>
        <button id="drawer-close" class="button secondary">Close</button>
      </div>
      <div id="drawer-body" class="drawer-body"></div>
    </aside>
  </div>

  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-app.js";
    import { GoogleAuthProvider, getAuth, onAuthStateChanged, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-auth.js";

    const FIREBASE_CONFIG = __FIREBASE_CONFIG__;
    const firebaseApp = initializeApp(FIREBASE_CONFIG);
    const auth = getAuth(firebaseApp);
    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({ prompt: "select_account" });

    const state = { authUser: null, session: null, lastJobId: "", trackedJob: null, pollHandle: null, activeDrawer: "", activeWorkspace: "network", activeAdminJobTab: "all", activeConversationId: "", conversationCache: {}, workerStats: null };
    const el = (id) => document.getElementById(id);
    const DRAWER_PANELS = {
      network: { eyebrow: "Network", title: "Network Snapshot", render: () => `<pre>${escapeHtml(el("network-json").textContent)}</pre>` },
      job: { eyebrow: "Jobs", title: "Tracked Job", render: () => `${el("job-meta-summary").classList.contains("hidden") ? "" : `<div class="job-meta-strip subtle">${escapeHtml(el("job-meta-summary").textContent)}</div>`}${el("job-artifacts").classList.contains("hidden") ? "" : `<div class="artifact-list">${el("job-artifacts").innerHTML}</div>`}${el("job-raw-output").classList.contains("hidden") ? "" : `<details open><summary>Raw model output</summary><div style="height:10px"></div><pre>${escapeHtml(el("job-answer").textContent)}</pre></details>`}<pre>${escapeHtml(el("job-json").textContent)}</pre>` },
      worker: { eyebrow: "Workers", title: "Local Worker Loop", render: () => `<pre>${escapeHtml(el("local-worker-json").textContent)}</pre>` },
      "worker-stats": { eyebrow: "Workers", title: "Worker Stats", render: () => workerStatsMarkup(state.workerStats) },
    };

    async function getIdToken(forceRefresh = false) { return state.authUser ? state.authUser.getIdToken(forceRefresh) : ""; }
    async function api(path, options = {}) {
      const headers = new Headers(options.headers || {});
      if (options.body !== undefined && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
      const token = await getIdToken(false);
      if (token) headers.set("Authorization", `Bearer ${token}`);
      let response = await fetch(path, { ...options, headers });
      if (response.status === 401 && state.authUser) {
        const refreshed = await getIdToken(true);
        if (refreshed) {
          headers.set("Authorization", `Bearer ${refreshed}`);
          response = await fetch(path, { ...options, headers });
        }
      }
      const isJson = response.headers.get("content-type")?.includes("application/json");
      const payload = isJson ? await response.json() : {};
      if (!response.ok) throw new Error(payload.error || `Request failed with ${response.status}`);
      return payload;
    }
    async function apiBlob(path) {
      const headers = new Headers();
      const token = await getIdToken(false);
      if (token) headers.set("Authorization", `Bearer ${token}`);
      let response = await fetch(path, { headers });
      if (response.status === 401 && state.authUser) {
        const refreshed = await getIdToken(true);
        if (refreshed) {
          headers.set("Authorization", `Bearer ${refreshed}`);
          response = await fetch(path, { headers });
        }
      }
      if (!response.ok) {
        const isJson = response.headers.get("content-type")?.includes("application/json");
        const payload = isJson ? await response.json() : {};
        throw new Error(payload.error || `Request failed with ${response.status}`);
      }
      return {
        blob: await response.blob(),
        disposition: response.headers.get("Content-Disposition") || "",
      };
    }

    function setStatus(id, message, kind = "ok") { const node = el(id); node.textContent = message; node.className = `status ${kind}`; }
    function writeJson(id, payload) { el(id).textContent = JSON.stringify(payload, null, 2); if (state.activeDrawer) renderDrawer(); }
    function parseCsv(text) { return String(text || "").split(",").map((part) => part.trim()).filter(Boolean); }
    function parseThroughput(text) { return parseCsv(text).reduce((acc, entry) => { const [model, value] = entry.split("="); if (model && value) acc[model.trim()] = Number(value.trim()); return acc; }, {}); }
    function chip(label, kind = "") { const node = document.createElement("span"); node.className = `chip ${kind}`.trim(); node.textContent = label; return node; }
    function escapeHtml(value) { return String(value || "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;"); }
    function formatTimestamp(unix) {
      const numeric = Number(unix || 0);
      if (!numeric) return "";
      return new Date(numeric * 1000).toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
    }
    function jobOutcomeLabel(status) {
      if (status === "failed") return "Failed";
      if (status === "assigned") return "Running";
      if (status === "canceled") return "Canceled";
      return "Completed";
    }
    function adminJobStatusClass(status) {
      if (status === "queued") return "queued";
      if (status === "assigned") return "assigned";
      if (status === "failed") return "failed";
      if (status === "canceled") return "canceled";
      return "completed";
    }
    function adminJobBanner(status) {
      if (status === "queued") return `<span class="job-status-banner queued">Queued and waiting</span>`;
      if (status === "assigned") return `<span class="job-status-banner assigned">Currently running</span>`;
      if (status === "failed") return `<span class="job-status-banner failed">Run failed</span>`;
      if (status === "canceled") return `<span class="job-status-banner canceled">Canceled</span>`;
      return `<span class="job-status-banner completed">Completed</span>`;
    }
    function adminJobSortTime(job) {
      if (state.activeAdminJobTab === "queued") return Number(job?.submitted_at_unix || 0);
      if (state.activeAdminJobTab === "completed") return Number(job?.completed_at_unix || job?.submitted_at_unix || 0);
      return Number(job?.completed_at_unix || job?.assigned_at_unix || job?.submitted_at_unix || 0);
    }
    function isSelfServedJob(job) {
      return Boolean(job?.assigned_worker_id && job?.requester_user_id && job.assigned_worker_id === job.requester_user_id && Number(job?.refunded_credits || 0) >= Number(job?.reserved_credits || 0));
    }
    function billingParts(job) {
      const parts = [];
      const promptTokens = Number(job?.prompt_tokens_used || 0);
      const outputTokens = Number(job?.output_tokens_used || job?.result?.output_tokens || 0);
      const billedTokens = Number(job?.billed_tokens || 0);
      const reserved = Number(job?.reserved_credits || 0);
      const actual = Number(job?.actual_credits || 0);
      const refunded = Number(job?.refunded_credits || 0);
      const workerEarned = Number(job?.worker_earned_credits || 0);
      const platformFee = Number(job?.platform_fee_credits || 0);
      if (promptTokens) parts.push(`Prompt ${promptTokens} tok`);
      if (outputTokens) parts.push(`Output ${outputTokens} tok`);
      if (billedTokens) parts.push(`Billed ${billedTokens} tok`);
      if (reserved || actual || refunded || job?.status === "completed") parts.push(`Reserved ${reserved} cr`);
      if (actual || job?.status === "completed") parts.push(`Final ${actual} cr`);
      if (refunded) parts.push(`Refund ${refunded} cr`);
      if (workerEarned) parts.push(`Worker +${workerEarned} cr`);
      if (platformFee) parts.push(`Platform +${platformFee} cr`);
      if (isSelfServedJob(job)) parts.push("Self-served preview refunded");
      return parts;
    }
    async function syncWalletDisplay() {
      if (!state.session?.user_id) return;
      try {
        const payload = await api(`/users/${encodeURIComponent(state.session.user_id)}`);
        el("user-balance").value = String(payload.wallet?.available_credits ?? payload.balance ?? "");
      } catch (_error) {
      }
    }
    function renderJobMeta(payload) {
      const lines = [];
      const submitted = formatTimestamp(payload?.submitted_at_unix);
      const assigned = formatTimestamp(payload?.assigned_at_unix);
      const completed = formatTimestamp(payload?.completed_at_unix);
      if (submitted) lines.push(`Submitted ${submitted}`);
      if (assigned) lines.push(`Assigned ${assigned}`);
      if (completed) lines.push(`${jobOutcomeLabel(payload?.status)} ${completed}`);
      if (payload?.assigned_worker_id) lines.push(`Worker ${payload.assigned_worker_id}`);
      lines.push(...billingParts(payload || {}));
      const summary = el("job-meta-summary");
      summary.textContent = lines.join(" | ");
      summary.classList.toggle("hidden", lines.length === 0);
    }
    function renderWorkerQueueState(payload) {
      const node = el("worker-queue-status");
      if (!payload) {
        node.textContent = "";
        node.classList.add("hidden");
        return;
      }
      const parts = [];
      if (payload.summary) parts.push(payload.summary);
      if (payload.queued_jobs !== undefined) parts.push(`Visible queued jobs: ${payload.queued_jobs}`);
      if (payload.compatible_jobs !== undefined) parts.push(`Compatible now: ${payload.compatible_jobs}`);
      if (Array.isArray(payload.blocked_examples) && payload.blocked_examples.length) {
        const first = payload.blocked_examples[0];
        parts.push(`Example blocked job ${first.job_id}: ${first.reason}`);
      }
      node.textContent = parts.join(" | ");
      node.classList.toggle("hidden", parts.length === 0);
    }
    function renderExcludedModels(items) {
      const node = el("worker-excluded-models");
      const models = Array.isArray(items) ? items : [];
      if (!models.length) {
        node.textContent = "";
        node.classList.add("hidden");
        return;
      }
      node.textContent = models.map((item) => `${item.tag}: ${item.reason}`).join(" | ");
      node.classList.remove("hidden");
    }
    function updateElasticTabs(container) {
      if (!container) return;
      const selector = container.querySelector(".elastic-selector");
      const active = container.querySelector(".active");
      if (!selector || !active) return;
      const width = Math.round(active.getBoundingClientRect().width || active.offsetWidth || 0);
      if (width <= 8) {
        selector.style.width = "0px";
        container.classList.remove("ready");
        container.dataset.highlight = "false";
        requestAnimationFrame(() => {
          const retryWidth = Math.round(active.getBoundingClientRect().width || active.offsetWidth || 0);
          if (retryWidth > 8) updateElasticTabs(container);
        });
        return;
      }
      selector.style.left = `${active.offsetLeft}px`;
      selector.style.width = `${width}px`;
      container.classList.add("ready");
      container.dataset.highlight = "true";
    }
    function refreshElasticTabs() {
      document.querySelectorAll("[data-elastic-tabs]").forEach((container) => updateElasticTabs(container));
    }
    function renderConversationMessages(container, messages) {
      container.innerHTML = "";
      const list = Array.isArray(messages) ? messages : [];
      if (!list.length) {
        const empty = document.createElement("div");
        empty.className = "row";
        empty.innerHTML = "<div class='row-head'><strong>No saved messages yet</strong><span class='subtle'>This conversation will fill in as prompts and responses are stored.</span></div>";
        container.appendChild(empty);
        return;
      }
      list.forEach((message) => {
        const card = document.createElement("div");
        const role = String(message.role || "message").toLowerCase();
        card.className = `conversation-message ${role === "user" ? "user" : "assistant"}`;
        const meta = document.createElement("div");
        meta.className = "job-meta";
        meta.appendChild(chip(role === "user" ? "User" : "Assistant"));
        if (message.status) meta.appendChild(chip(String(message.status)));
        if (message.job_id) meta.appendChild(chip(String(message.job_id)));
        const stamped = formatTimestamp(message.timestamp_unix);
        if (stamped) meta.appendChild(chip(stamped));
        const content = String(message.content || "").trim();
        const body = content.includes("\\n") || content.length > 220
          ? document.createElement("pre")
          : document.createElement("p");
        body.textContent = content || "(empty message)";
        card.appendChild(meta);
        card.appendChild(body);
        container.appendChild(card);
      });
    }
    function conversationPreview(conversation) {
      const preview = String(conversation?.last_message_preview || "").trim();
      if (!preview) return "No replies stored yet.";
      return preview.length > 120 ? `${preview.slice(0, 120)}...` : preview;
    }
    async function ensureConversationDetail(conversationId) {
      if (!conversationId) return { messages: [] };
      if (state.conversationCache[conversationId]) return state.conversationCache[conversationId];
      const payload = await api(`/conversations/${encodeURIComponent(conversationId)}`);
      state.conversationCache[conversationId] = payload;
      return payload;
    }
    function renderConversationCard(conversation, archived = false) {
      const conversationId = String(conversation?.conversation_id || "");
      const card = document.createElement("div");
      card.className = `job-card conversation-card ${archived ? "job-card-canceled" : "job-card-completed"}`;
      const details = document.createElement("details");
      details.open = !archived && state.activeConversationId === conversationId;
      const summary = document.createElement("summary");
      const updated = formatTimestamp(conversation.updated_at_unix);
      const created = formatTimestamp(conversation.created_at_unix);
      summary.innerHTML = `<div class="conversation-head"><div class="conversation-head-top"><div class="conversation-head-copy"><div class="job-meta">${archived ? '<span class="chip warn">Archived</span>' : ""}<span class="chip">${escapeHtml(`${conversation.message_count || 0} messages`)}</span>${updated ? `<span class="chip">${escapeHtml(`Updated ${updated}`)}</span>` : ""}</div><strong>${escapeHtml(conversation.title || conversationId)}</strong><span class="subtle">${escapeHtml(conversationPreview(conversation))}</span>${created ? `<span class="subtle">Started ${escapeHtml(created)}</span>` : ""}</div><span class="job-collapse">${details.open ? "Hide thread" : "Show thread"}</span></div></div>`;
      const body = document.createElement("div");
      body.className = "conversation-body";
      const actions = document.createElement("div");
      actions.className = "conversation-actions";
      if (!archived) {
        const useButton = document.createElement("button");
        useButton.className = "button secondary";
        useButton.textContent = "Use this conversation";
        useButton.addEventListener("click", () => loadConversation(conversationId).catch((error) => setStatus("job-status", error.message, "error")));
        const archiveButton = document.createElement("button");
        archiveButton.className = "button secondary";
        archiveButton.textContent = "Archive";
        archiveButton.addEventListener("click", () => archiveConversation(conversationId).catch((error) => setStatus("job-status", error.message, "error")));
        actions.appendChild(useButton);
        actions.appendChild(archiveButton);
      } else {
        const restoreButton = document.createElement("button");
        restoreButton.className = "button secondary";
        restoreButton.textContent = "Restore";
        restoreButton.addEventListener("click", () => restoreConversation(conversationId).catch((error) => setStatus("job-status", error.message, "error")));
        actions.appendChild(restoreButton);
      }
      const transcript = document.createElement("div");
      transcript.className = "conversation-message-list";
      const loadThread = async () => {
        const payload = await ensureConversationDetail(conversationId);
        renderConversationMessages(transcript, payload.messages || []);
      };
      details.addEventListener("toggle", () => {
        const label = summary.querySelector(".job-collapse");
        if (label) label.textContent = details.open ? "Hide thread" : "Show thread";
        if (details.open) loadThread().catch((error) => setStatus("job-status", error.message, "error"));
      });
      body.appendChild(actions);
      body.appendChild(transcript);
      details.appendChild(summary);
      details.appendChild(body);
      card.appendChild(details);
      if (details.open) {
        queueMicrotask(() => loadThread().catch((error) => setStatus("job-status", error.message, "error")));
      }
      return card;
    }
    function renderPromptHistory(payload) {
      const wrap = el("prompt-history");
      const archivedWrap = el("archived-history");
      wrap.innerHTML = "";
      archivedWrap.innerHTML = "";
      const conversations = payload?.conversations || [];
      const archived = payload?.archived_conversations || [];
      if (!conversations.length && !archived.length) {
        const empty = document.createElement("div");
        empty.className = "row";
        empty.innerHTML = "<div class='row-head'><strong>No saved conversations yet</strong><span class='subtle'>Once you submit prompts, the full conversation transcript will persist here on the server.</span></div>";
        wrap.appendChild(empty);
        return;
      }
      conversations.forEach((conversation) => wrap.appendChild(renderConversationCard(conversation, false)));
      if (archived.length) {
        const details = document.createElement("details");
        const summary = document.createElement("summary");
        summary.textContent = `Archived conversations (${archived.length})`;
        details.appendChild(summary);
        const list = document.createElement("div");
        list.className = "history-shell";
        archived.forEach((conversation) => list.appendChild(renderConversationCard(conversation, true)));
        details.appendChild(document.createElement("div")).style.height = "12px";
        details.appendChild(list);
        archivedWrap.appendChild(details);
      }
    }
    function renderConversationDetail(payload) {
      if (payload?.conversation_id) {
        state.conversationCache[payload.conversation_id] = payload;
      }
      if (!payload?.conversation_id) {
        el("conversation-meta").textContent = "No conversation selected.";
        renderConversationMessages(el("conversation-thread"), []);
        return;
      }
      const count = Array.isArray(payload.messages) ? payload.messages.length : 0;
      const updated = formatTimestamp(payload.updated_at_unix);
      const archived = payload.is_archived ? " | Archived" : "";
      el("conversation-meta").textContent = `${payload.title || payload.conversation_id} | ${count} messages${updated ? ` | Updated ${updated}` : ""}${archived}`;
      renderConversationMessages(el("conversation-thread"), payload.messages || []);
    }
    function renderConversationList(payload) {
      const select = el("conversation-select");
      select.innerHTML = "";
      const blank = document.createElement("option");
      blank.value = "";
      blank.textContent = "Start a new conversation";
      select.appendChild(blank);
      (payload?.conversations || []).forEach((conversation) => {
        const option = document.createElement("option");
        option.value = conversation.conversation_id;
        option.textContent = `${conversation.title || conversation.conversation_id} (${conversation.message_count})`;
        select.appendChild(option);
      });
      if (state.activeConversationId && Array.from(select.options).some((option) => option.value === state.activeConversationId)) {
        select.value = state.activeConversationId;
      } else {
        state.activeConversationId = "";
        select.value = "";
      }
    }
    async function refreshConversations() {
      const payload = await api("/conversations");
      renderPromptHistory(payload);
      renderConversationList(payload);
      if (state.activeConversationId) {
        await loadConversation(state.activeConversationId);
      } else {
        renderConversationDetail({ messages: [] });
      }
    }
    async function loadConversation(conversationId) {
      state.activeConversationId = conversationId || "";
      if (!state.activeConversationId) {
        renderConversationDetail({ messages: [] });
        el("conversation-select").value = "";
        return;
      }
      const payload = await api(`/conversations/${encodeURIComponent(state.activeConversationId)}`);
      renderConversationDetail(payload);
      el("conversation-select").value = state.activeConversationId;
    }
    async function archiveConversation(conversationId) {
      const payload = await api(`/conversations/${encodeURIComponent(conversationId)}/archive`, { method: "POST", body: JSON.stringify({}) });
      state.conversationCache[conversationId] = payload;
      if (state.activeConversationId === conversationId) startNewConversation();
      setStatus("job-status", `Archived ${payload.title || payload.conversation_id}.`, "ok");
      await refreshConversations();
    }
    async function restoreConversation(conversationId) {
      const payload = await api(`/conversations/${encodeURIComponent(conversationId)}/restore`, { method: "POST", body: JSON.stringify({}) });
      state.conversationCache[conversationId] = payload;
      setStatus("job-status", `Restored ${payload.title || payload.conversation_id}.`, "ok");
      await refreshConversations();
    }
    function startNewConversation() {
      state.activeConversationId = "";
      el("conversation-select").value = "";
      renderConversationDetail({ messages: [] });
    }
    function setWorkspaceTab(name) {
      state.activeWorkspace = name;
      ["network", "worker"].forEach((tabName) => {
        const active = tabName === name;
        const tab = el(`tab-${tabName}`);
        const panel = el(`tab-panel-${tabName}`);
        tab.classList.toggle("active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
        tab.tabIndex = active ? 0 : -1;
        panel.classList.toggle("hidden", !active);
        panel.hidden = !active;
      });
      updateElasticTabs(document.querySelector('[data-elastic-tabs="workspace"]'));
    }
    function artifactSummary(artifact) {
      const lines = String(artifact?.content || "").split("\\n").length;
      return `${artifact.language || "text"} | ${lines} lines`;
    }
    function renderArtifactList(container, artifacts, jobId, statusTarget, includeActions = true) {
      container.innerHTML = "";
      const list = Array.isArray(artifacts) ? artifacts : [];
      if (!list.length) {
        container.classList.add("hidden");
        return;
      }
      list.forEach((artifact) => {
        const card = document.createElement("div");
        card.className = "artifact-card";
        const head = document.createElement("div");
        head.className = "artifact-head";
        head.innerHTML = `<strong>${escapeHtml(artifact.path)}</strong><span class="artifact-meta">${escapeHtml(artifactSummary(artifact))}</span>`;
        const preview = document.createElement("pre");
        preview.className = "artifact-preview";
        preview.textContent = artifact.content || "";
        card.appendChild(head);
        card.appendChild(preview);
        container.appendChild(card);
      });
      if (!includeActions) {
        container.classList.remove("hidden");
        return;
      }
      const actions = document.createElement("div");
      actions.className = "actions";
      const createButton = document.createElement("button");
      createButton.className = "button secondary";
      createButton.textContent = "Create files";
      createButton.addEventListener("click", () => createArtifacts(jobId, statusTarget).catch((error) => setStatus(statusTarget, error.message, "error")));
      const downloadButton = document.createElement("button");
      downloadButton.className = "button secondary";
      downloadButton.textContent = "Download zip";
      downloadButton.addEventListener("click", () => downloadArtifacts(jobId, statusTarget).catch((error) => setStatus(statusTarget, error.message, "error")));
      actions.appendChild(createButton);
      actions.appendChild(downloadButton);
      container.appendChild(actions);
      container.classList.remove("hidden");
    }
    function setAdminJobTab(name) {
      state.activeAdminJobTab = name;
      ["all", "queued", "completed"].forEach((tabName) => {
        const active = tabName === name;
        const tab = el(`admin-job-tab-${tabName}`);
        if (!tab) return;
        tab.classList.toggle("active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
      });
      updateElasticTabs(document.querySelector('[data-elastic-tabs="admin-jobs"]'));
    }
    function toggleDashboard(unlocked) { el("dashboard-shell").classList.toggle("hidden", !unlocked); el("auth-panel").classList.toggle("hidden", unlocked); el("sign-in").classList.toggle("hidden", unlocked); el("sign-out").classList.toggle("hidden", !unlocked); }
    function setAdminVisible(visible) { el("admin-panel").classList.toggle("hidden", !visible); el("admin-pill").classList.toggle("hidden", !visible); el("admin-override-wrap").classList.toggle("hidden", !visible); }
    function setRailVisible(visible) { el("floating-rail").classList.toggle("hidden", !visible); }
    function workerStatsMarkup(payload) {
      if (!payload?.worker) {
        return `<div class="row"><div class="row-head"><strong>No worker stats yet</strong><span class="subtle">Start a worker or refresh the worker panel first.</span></div></div>`;
      }
      const summary = payload.summary || {};
      const recentJobs = Array.isArray(payload.recent_jobs) ? payload.recent_jobs : [];
      const topModels = Array.isArray(payload.top_models) ? payload.top_models : [];
      const loop = payload.local_loop || {};
      const tiles = [
        ["Completed jobs", summary.completed_jobs || 0],
        ["Failed jobs", summary.failed_jobs || 0],
        ["Credits earned", summary.credits_earned || 0],
        ["Requester credits charged", summary.credits_charged_to_requesters || 0],
        ["Billed tokens", summary.billed_tokens || 0],
        ["Average latency", `${Number(summary.avg_latency_seconds || 0).toFixed(2)}s`],
        ["External jobs", summary.external_jobs || 0],
        ["Self-served jobs", summary.self_served_jobs || 0],
      ];
      const tileMarkup = tiles.map(([label, value]) => `<div class="stats-card"><strong>${escapeHtml(String(value))}</strong><span>${escapeHtml(String(label))}</span></div>`).join("");
      const modelsMarkup = topModels.length
        ? topModels.map((item) => `<span class="chip">${escapeHtml(`${item.model_tag} · ${item.jobs} jobs`)}</span>`).join("")
        : `<span class="subtle">No completed model history yet.</span>`;
      const jobsMarkup = recentJobs.length
        ? recentJobs.map((job) => {
            const when = formatTimestamp(job.completed_at_unix || job.assigned_at_unix || job.submitted_at_unix);
            return `<div class="job-card job-card-${adminJobStatusClass(job.status)}"><div class="job-meta"><span class="chip">${escapeHtml(job.status || "")}</span><span class="chip">${escapeHtml(job.resolved_model_tag || job.model_tag || "")}</span></div><strong>${escapeHtml(job.job_id || "")}</strong><p>${escapeHtml(job.prompt || "")}</p><p class="subtle">${escapeHtml([when ? `Updated ${when}` : "", ...billingParts(job)].filter(Boolean).join(" | ") || "No billing data yet.")}</p></div>`;
          }).join("")
        : `<div class="row"><div class="row-head"><strong>No jobs served yet</strong><span class="subtle">Once this worker completes jobs, the history will appear here.</span></div></div>`;
      return `
        <div class="stack">
          <div class="stats-grid">${tileMarkup}</div>
          <div class="job-meta-strip subtle">
            Worker ${escapeHtml(payload.worker.worker_id || "")} | Owner ${escapeHtml(payload.worker.owner_user_id || "")}${summary.last_completed_at_unix ? ` | Last completed ${escapeHtml(formatTimestamp(summary.last_completed_at_unix))}` : ""}${loop.jobs_completed !== undefined ? ` | Local loop completed ${escapeHtml(String(loop.jobs_completed))}` : ""}
          </div>
          <section class="card" style="padding:16px">
            <h3 style="margin:0 0 10px">Top served models</h3>
            <div class="chips">${modelsMarkup}</div>
          </section>
          <section class="card" style="padding:16px">
            <h3 style="margin:0 0 10px">Recent worker jobs</h3>
            <div class="stack">${jobsMarkup}</div>
          </section>
        </div>
      `;
    }
    function renderDrawer() {
      const panel = DRAWER_PANELS[state.activeDrawer];
      if (!panel) { el("drawer-shell").classList.remove("open"); return; }
      el("drawer-eyebrow").textContent = panel.eyebrow;
      el("drawer-title").textContent = panel.title;
      el("drawer-body").innerHTML = panel.render();
      el("drawer-shell").classList.add("open");
    }
    async function refreshWorkerStats() {
      const workerId = el("worker-id").value.trim();
      if (!workerId) {
        state.workerStats = null;
        if (state.activeDrawer === "worker-stats") renderDrawer();
        return;
      }
      state.workerStats = await api(`/workers/${encodeURIComponent(workerId)}/stats`);
      if (state.activeDrawer === "worker-stats") renderDrawer();
    }
    function openDrawer(name) { state.activeDrawer = name; renderDrawer(); if (name === "worker-stats") refreshWorkerStats().catch((error) => setStatus("worker-status", error.message, "error")); }
    function closeDrawer() { state.activeDrawer = ""; renderDrawer(); }
    function renderSessionPill() { el("session-pill").textContent = state.session ? `${state.session.display_name || state.session.email || state.session.user_id} | ${state.session.user_id}` : "Sign in required"; }
    function showGlobalError(error) { const message = error?.message || String(error); ["auth-status","user-status","job-status","worker-status","admin-status"].forEach((id) => setStatus(id, message, "error")); }

    function renderTrackedJob(payload) {
      state.trackedJob = payload || null;
      writeJson("job-json", payload);
      renderJobMeta(payload || {});
      const answer = payload?.result?.output_text?.trim();
      const errorMessage = payload?.result?.error_message?.trim();
      const rawOutput = answer || (errorMessage ? `Worker error: ${errorMessage}` : payload?.status ? `Tracked job is ${payload.status}.` : "No tracked response yet.");
      const artifacts = payload?.artifacts || [];
      el("job-answer").textContent = rawOutput;
      el("job-raw-output").classList.toggle("hidden", !rawOutput);
      el("job-artifact-actions").classList.toggle("hidden", !artifacts.length);
      renderArtifactList(el("job-artifacts"), artifacts, payload?.job_id || state.lastJobId || "", "job-status", false);
      if (state.activeDrawer === "job") renderDrawer();
    }
    async function refreshPromptHistory() {
      await refreshConversations();
    }

    async function fetchSession() {
      const payload = await api("/auth/session");
      state.session = payload;
      renderSessionPill();
      el("user-id").value = payload.user_id || "";
      el("job-user-id").value = payload.user_id || "";
      el("worker-id").value = payload.user_id || "";
      el("worker-owner").value = payload.user_id || "";
      el("user-balance").value = String(payload.wallet?.available_credits ?? payload.balance ?? "");
      setAdminVisible(Boolean(payload.is_admin));
      setStatus("auth-status", payload.issued ? `Signed in. Created network account ${payload.user_id}.` : `Signed in. Using network account ${payload.user_id}.`, "ok");
      setStatus("user-status", `Authenticated as ${payload.display_name || payload.email || payload.user_id}. Balance: ${Number(payload.balance).toFixed(4)} credits.`, "ok");
      return payload;
    }

    async function refreshModels() {
      const payload = await api("/models");
      const list = el("model-list");
      const select = el("job-model");
      const summary = el("local-detection-summary");
      list.innerHTML = ""; select.innerHTML = ""; summary.innerHTML = "";
      ["auto","good","better","best"].forEach((value) => { const option = document.createElement("option"); option.value = value; option.textContent = value; select.appendChild(option); });
      if (payload.local_detection?.ollama_available) {
        summary.appendChild(chip("Ollama detected"));
        summary.appendChild(chip(`${payload.local_detection.approved_local_models.length} approved local`));
      } else summary.appendChild(chip(payload.local_detection?.error || "Ollama not detected", "warn"));
      payload.models.forEach((model) => {
        const row = document.createElement("div");
        row.className = "row";
        row.innerHTML = `<div class="row-head"><strong>${model.tag}</strong><span class="subtle">${model.min_vram_gb} GB minimum</span></div><div class="subtle">${model.family} | ${model.runtime} | ${model.installed_locally ? "installed on server host" : "not installed locally"}</div>`;
        list.appendChild(row);
        const option = document.createElement("option");
        option.value = model.tag;
        option.textContent = `${model.tag} - exact`;
        select.appendChild(option);
      });
      if ((payload.local_detection?.approved_local_models || []).includes("glm4:9b")) {
        select.value = "glm4:9b";
      }
    }

    async function refreshWorkerContext() {
      const payload = await api("/worker-context");
      const summary = el("worker-detection-summary");
      summary.innerHTML = "";
      el("worker-id").value = payload.suggested_worker_id || el("worker-id").value;
      el("worker-owner").value = payload.suggested_owner_user_id || el("worker-owner").value;
      el("worker-gpu").value = payload.suggested_gpu_name || "";
      el("worker-vram").value = payload.suggested_vram_gb || "";
      el("worker-system-ram").value = payload.suggested_system_ram_gb || "";
      el("worker-models").value = (payload.suggested_installed_models || []).join(", ");
      el("worker-throughput").value = Object.entries(payload.suggested_benchmark_tokens_per_second || {}).map(([model, value]) => `${model}=${value}`).join(", ");
      renderExcludedModels(payload.excluded_local_models || []);
      summary.appendChild(chip(payload.hardware_detection?.detected ? "GPU detected" : payload.hardware_detection?.error || "GPU not detected", payload.hardware_detection?.detected ? "" : "warn"));
      summary.appendChild(chip((payload.suggested_installed_models || []).length ? `${payload.suggested_installed_models.length} approved local models` : "No approved local models ready", (payload.suggested_installed_models || []).length ? "" : "warn"));
      await refreshWorkerStats();
    }

    async function refreshNetwork() {
      const payload = await api("/network");
      writeJson("network-json", payload);
      writeJson("local-worker-json", payload.local_workers || {});
      el("metric-queue").textContent = payload.queued_jobs.length;
      el("metric-workers").textContent = Object.keys(payload.workers).length;
      el("metric-users").textContent = payload.user_count;
      const currentWorker = payload.local_workers?.[el("worker-id").value.trim()];
      if (currentWorker) {
        renderWorkerQueueState({
          summary: currentWorker.last_idle_reason || currentWorker.last_queue_summary || "",
          queued_jobs: currentWorker.visible_queued_jobs,
          compatible_jobs: currentWorker.compatible_queued_jobs,
        });
      }
      await refreshWorkerStats();
      return payload;
    }

    async function refreshTrackedJob() {
      if (!state.lastJobId) { renderTrackedJob({}); setStatus("job-status", "No tracked job yet.", "ok"); return; }
      const payload = await api(`/jobs/${state.lastJobId}`);
      renderTrackedJob(payload);
      if (payload.conversation) {
        state.activeConversationId = payload.conversation.conversation_id || state.activeConversationId;
        renderConversationDetail(payload.conversation);
      }
      await syncWalletDisplay();
      setStatus("job-status", `Tracked job ${payload.job_id} is ${payload.status}.`, "ok");
    }

    function renderAdminOverview(payload) {
      const summary = el("admin-summary");
      const select = el("admin-credit-user");
      const jobs = el("admin-jobs");
      summary.innerHTML = ""; select.innerHTML = ""; jobs.innerHTML = "";
      summary.appendChild(chip(`${payload.summary.online_workers} online workers`));
      summary.appendChild(chip(`${payload.summary.queued_jobs} queued jobs`));
      summary.appendChild(chip(`${payload.summary.known_network_users} users`));
      (payload.users || []).forEach((user) => {
        const option = document.createElement("option");
        option.value = user.user_id;
        option.textContent = `${user.user_id} | ${user.wallet.available_credits} credits`;
        select.appendChild(option);
      });
      const filteredJobs = (payload.jobs || []).filter((job) => {
        if (state.activeAdminJobTab === "queued") return ["queued", "assigned"].includes(job.status);
        if (state.activeAdminJobTab === "completed") return ["completed", "failed", "canceled"].includes(job.status);
        return true;
      }).sort((left, right) => {
        const rightTime = adminJobSortTime(right);
        const leftTime = adminJobSortTime(left);
        if (rightTime !== leftTime) return rightTime - leftTime;
        return String(right.job_id || "").localeCompare(String(left.job_id || ""));
      }).slice(0, 12);
      filteredJobs.forEach((job) => {
        const card = document.createElement("div");
        const statusClass = adminJobStatusClass(job.status);
        card.className = `job-card job-card-${statusClass}`;
        const output = job.result?.output_text?.trim() || job.result?.error_message?.trim() || "No result yet.";
        const meta = document.createElement("div");
        meta.className = "job-meta";
        [job.status, job.requester_user_id, job.model_tag].forEach((label) => meta.appendChild(chip(String(label || ""))));
        const timeline = document.createElement("p");
        timeline.textContent = [
          formatTimestamp(job.submitted_at_unix) ? `Submitted ${formatTimestamp(job.submitted_at_unix)}` : "",
          formatTimestamp(job.assigned_at_unix) ? `Assigned ${formatTimestamp(job.assigned_at_unix)}` : "",
          formatTimestamp(job.completed_at_unix) ? `${jobOutcomeLabel(job.status)} ${formatTimestamp(job.completed_at_unix)}` : "",
          ...billingParts(job),
        ].filter(Boolean).join(" | ") || "Timestamps pending.";
        const details = document.createElement("details");
        details.open = ["queued", "assigned"].includes(job.status);
        const summaryRow = document.createElement("summary");
        const previewPrompt = job.prompt.length > 72 ? `${job.prompt.slice(0, 72)}...` : job.prompt;
        const banner = adminJobBanner(job.status);
        summaryRow.innerHTML = `<div class="job-summary"><div class="job-summary-top"><div class="job-summary-copy">${banner}<div class="job-meta">${meta.innerHTML}</div><strong>${job.job_id}</strong><span class="subtle">${timeline.textContent}</span><span class="subtle">Prompt preview: ${escapeHtml(previewPrompt)}</span></div><span class="job-collapse">${details.open ? "Hide details" : "Show details"}</span></div></div>`;
        details.addEventListener("toggle", () => {
          const label = summaryRow.querySelector(".job-collapse");
          if (label) label.textContent = details.open ? "Hide details" : "Show details";
        });
        const body = document.createElement("div");
        body.className = "job-body";
        const prompt = document.createElement("p");
        prompt.textContent = `Prompt: ${job.prompt}`;
        const result = document.createElement("p");
        result.textContent = job.artifacts?.length ? `Generated ${job.artifacts.length} file artifact(s).` : `Output: ${output}`;
        body.appendChild(prompt);
        body.appendChild(result);
        if (job.artifacts?.length) {
          const artifactWrap = document.createElement("div");
          artifactWrap.className = "artifact-list";
          renderArtifactList(artifactWrap, job.artifacts, job.job_id, "admin-status");
          body.appendChild(artifactWrap);
        }
        if (job.status === "queued") {
          const actions = document.createElement("div");
          actions.className = "actions";
          const reroute = document.createElement("button");
          reroute.className = "button secondary";
          reroute.textContent = "Reroute to auto";
          reroute.addEventListener("click", () => adminRerouteJob(job.job_id, "auto").catch((error) => setStatus("admin-status", error.message, "error")));
          const cancel = document.createElement("button");
          cancel.className = "button secondary";
          cancel.textContent = "Cancel queued job";
          cancel.addEventListener("click", () => adminCancelJob(job.job_id).catch((error) => setStatus("admin-status", error.message, "error")));
          actions.appendChild(reroute);
          actions.appendChild(cancel);
          body.appendChild(actions);
        }
        details.appendChild(summaryRow);
        details.appendChild(body);
        card.appendChild(details);
        jobs.appendChild(card);
      });
      if (!filteredJobs.length) {
        const empty = document.createElement("div");
        empty.className = "row";
        empty.innerHTML = `<div class="row-head"><strong>No ${state.activeAdminJobTab === "all" ? "" : state.activeAdminJobTab + " "}jobs to show</strong><span class="subtle">Switch tabs or refresh admin data.</span></div>`;
        jobs.appendChild(empty);
      }
    }

    async function refreshAdminOverview() {
      if (!state.session?.is_admin) return;
      const payload = await api("/admin/overview");
      renderAdminOverview(payload);
      setStatus("admin-status", `Loaded admin overview for ${payload.actor_email}.`, "ok");
    }

    async function refreshUser() {
      const userId = el("user-id").value.trim();
      const payload = await api(`/users/${encodeURIComponent(userId)}`);
      el("user-balance").value = String(payload.wallet?.available_credits ?? payload.balance ?? "");
      setStatus("user-status", `Loaded ${payload.user_id}. Balance: ${Number(payload.balance).toFixed(4)} credits.`, "ok");
    }

    async function submitJob() {
      const body = { requester_user_id: el("job-user-id").value.trim(), model_tag: el("job-model").value, prompt: el("job-prompt").value, max_output_tokens: Number(el("job-max-output").value || 0) };
      if (state.activeConversationId) body.conversation_id = state.activeConversationId;
      const promptTokens = el("job-prompt-tokens").value.trim();
      if (promptTokens) body.prompt_tokens = Number(promptTokens);
      const payload = await api("/jobs", { method: "POST", body: JSON.stringify(body) });
      state.lastJobId = payload.job_id;
      state.activeConversationId = payload.conversation_id || state.activeConversationId;
      renderTrackedJob(payload);
      if (payload.conversation) renderConversationDetail(payload.conversation);
      setWorkspaceTab("network");
      openDrawer("job");
      setStatus("job-status", `Queued ${payload.job_id} with ${payload.reserved_credits} reserved credits.`, "ok");
      await syncWalletDisplay();
      await refreshNetwork();
      await refreshPromptHistory();
      if (state.session?.is_admin) await refreshAdminOverview();
    }

    function allowAdminSelfServe() { return Boolean(state.session?.is_admin && el("worker-admin-override").checked); }

    async function startWorker() {
      const payload = await api("/workers/start-local", {
        method: "POST",
        body: JSON.stringify({
          worker_id: el("worker-id").value.trim(),
          owner_user_id: el("worker-owner").value.trim(),
          gpu_name: el("worker-gpu").value.trim(),
          vram_gb: Number(el("worker-vram").value || 0),
          installed_models: parseCsv(el("worker-models").value),
          benchmark_tokens_per_second: parseThroughput(el("worker-throughput").value),
          poll_interval_seconds: Number(el("worker-poll-interval").value || 2),
          runtime: "ollama",
          allows_cloud_fallback: false,
          allow_admin_self_serve: allowAdminSelfServe(),
        }),
      });
      writeJson("local-worker-json", payload.loop || {});
      renderWorkerQueueState(payload.queue || null);
      const adminNote = payload.loop?.allow_admin_self_serve
        ? " Admin override is active, so this worker can also claim your own queued jobs."
        : " This worker will only claim jobs from other users.";
      setWorkspaceTab("worker");
      openDrawer("worker");
      setStatus("worker-status", `Worker ${payload.worker.worker_id} is polling locally in the background.${adminNote}`, "ok");
      await refreshNetwork();
    }

    async function stopWorker() {
      const workerId = el("worker-id").value.trim();
      const payload = await api(`/workers/${encodeURIComponent(workerId)}/stop-local`, { method: "POST", body: JSON.stringify({}) });
      writeJson("local-worker-json", payload.loop || {});
      setStatus("worker-status", `Worker ${workerId} was stopped.`, "ok");
      await refreshNetwork();
    }

    async function runWorkerOnce() {
      const workerId = el("worker-id").value.trim();
      const payload = await api(`/workers/${encodeURIComponent(workerId)}/run-once`, {
        method: "POST",
        body: JSON.stringify({ allow_admin_self_serve: allowAdminSelfServe() }),
      });
      if (!payload.job) {
        renderWorkerQueueState(payload.queue || null);
        setStatus("worker-status", payload.queue?.summary || "No matching queued job was available for this worker.", "ok");
        return;
      }
      state.lastJobId = payload.job.job_id;
      renderTrackedJob(payload.job);
      setWorkspaceTab("worker");
      openDrawer("job");
      setStatus("worker-status", `Worker ${workerId} completed ${payload.job.job_id}. ${billingParts(payload.job).join(" | ")}`, "ok");
      await syncWalletDisplay();
      await refreshNetwork();
      await refreshPromptHistory();
      if (state.session?.is_admin) await refreshAdminOverview();
    }

    async function adjustCredits() {
      const userId = el("admin-credit-user").value;
      const payload = await api(`/admin/users/${encodeURIComponent(userId)}/credits`, {
        method: "POST",
        body: JSON.stringify({ amount: Number(el("admin-credit-amount").value || 0), note: el("admin-credit-note").value }),
      });
      setStatus("admin-status", `Adjusted ${payload.user_id} by ${payload.amount} credits.`, "ok");
      await refreshAdminOverview();
      if (userId === state.session?.user_id) await refreshUser();
    }
    async function createArtifacts(jobId, statusTarget = "job-status") {
      const payload = await api(`/jobs/${encodeURIComponent(jobId)}/artifacts/create`, { method: "POST", body: JSON.stringify({}) });
      setStatus(statusTarget, `Created ${payload.files.length} file(s) in ${payload.export_dir}.`, "ok");
    }
    async function downloadArtifacts(jobId, statusTarget = "job-status") {
      const response = await apiBlob(`/jobs/${encodeURIComponent(jobId)}/artifacts/download`);
      const url = URL.createObjectURL(response.blob);
      const anchor = document.createElement("a");
      const filenameMatch = /filename=\"?([^\";]+)\"?/.exec(response.disposition || "");
      anchor.href = url;
      anchor.download = filenameMatch?.[1] || `${jobId}-artifacts.zip`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
      setStatus(statusTarget, `Downloaded ${anchor.download}.`, "ok");
    }
    async function adminCancelJob(jobId) {
      const payload = await api(`/admin/jobs/${encodeURIComponent(jobId)}/cancel`, {
        method: "POST",
        body: JSON.stringify({ note: "Canceled from dashboard admin console" }),
      });
      setStatus("admin-status", `Canceled ${payload.job.job_id}.`, "ok");
      await refreshAdminOverview();
      await refreshNetwork();
      await refreshPromptHistory();
      if (state.lastJobId === jobId) renderTrackedJob(payload.job);
    }
    async function adminRerouteJob(jobId, modelTag) {
      const payload = await api(`/admin/jobs/${encodeURIComponent(jobId)}/reroute`, {
        method: "POST",
        body: JSON.stringify({ model_tag: modelTag }),
      });
      setStatus("admin-status", `Rerouted ${payload.job.job_id} to ${payload.job.model_tag}.`, "ok");
      await refreshAdminOverview();
      await refreshNetwork();
      await refreshPromptHistory();
      if (state.lastJobId === jobId) renderTrackedJob(payload.job);
    }

    function stopPolling() { if (state.pollHandle) { clearInterval(state.pollHandle); state.pollHandle = null; } }
    function ensurePolling() { if (state.pollHandle) return; state.pollHandle = setInterval(() => { if (!state.authUser) return; refreshNetwork().catch(() => {}); if (state.lastJobId) refreshTrackedJob().catch(() => {}); }, 4000); }
    async function signIn() { setStatus("auth-status", "Opening Google sign-in...", "ok"); await signInWithPopup(auth, provider); }
    async function signOutCurrent() { await signOut(auth); }

    function bind() {
      el("auth-project").textContent = FIREBASE_CONFIG.projectId || "unconfigured";
      el("sign-in").addEventListener("click", () => signIn().catch(showGlobalError));
      el("sign-in-panel").addEventListener("click", () => signIn().catch(showGlobalError));
      el("sign-out").addEventListener("click", () => signOutCurrent().catch(showGlobalError));
      el("refresh-all").addEventListener("click", () => Promise.all([refreshNetwork(), refreshTrackedJob(), refreshPromptHistory(), refreshAdminOverview()]).catch(showGlobalError));
      el("refresh-user").addEventListener("click", () => refreshUser().catch(showGlobalError));
      el("load-models").addEventListener("click", () => Promise.all([refreshModels(), refreshWorkerContext()]).catch(showGlobalError));
      el("submit-job").addEventListener("click", () => submitJob().catch((error) => setStatus("job-status", error.message, "error")));
      el("refresh-job").addEventListener("click", () => refreshTrackedJob().catch((error) => setStatus("job-status", error.message, "error")));
      el("create-artifacts").addEventListener("click", () => createArtifacts(state.lastJobId).catch((error) => setStatus("job-status", error.message, "error")));
      el("download-artifacts").addEventListener("click", () => downloadArtifacts(state.lastJobId).catch((error) => setStatus("job-status", error.message, "error")));
      el("refresh-history").addEventListener("click", () => refreshPromptHistory().catch((error) => setStatus("job-status", error.message, "error")));
      el("refresh-conversations").addEventListener("click", () => refreshConversations().catch((error) => setStatus("job-status", error.message, "error")));
      el("new-conversation").addEventListener("click", () => startNewConversation());
      el("conversation-select").addEventListener("change", (event) => loadConversation(event.target.value).catch((error) => setStatus("job-status", error.message, "error")));
      el("start-worker").addEventListener("click", () => startWorker().catch((error) => setStatus("worker-status", error.message, "error")));
      el("stop-worker").addEventListener("click", () => stopWorker().catch((error) => setStatus("worker-status", error.message, "error")));
      el("run-worker-once").addEventListener("click", () => runWorkerOnce().catch((error) => setStatus("worker-status", error.message, "error")));
      el("admin-refresh").addEventListener("click", () => refreshAdminOverview().catch((error) => setStatus("admin-status", error.message, "error")));
      el("admin-adjust-credits").addEventListener("click", () => adjustCredits().catch((error) => setStatus("admin-status", error.message, "error")));
      document.querySelectorAll("[data-admin-job-tab]").forEach((node) => node.addEventListener("click", () => { setAdminJobTab(node.dataset.adminJobTab); refreshAdminOverview().catch((error) => setStatus("admin-status", error.message, "error")); }));
      el("open-network-drawer").addEventListener("click", () => openDrawer("network"));
      el("open-job-drawer").addEventListener("click", () => openDrawer("job"));
      el("open-worker-drawer").addEventListener("click", () => openDrawer("worker"));
      document.querySelectorAll("[data-workspace-tab]").forEach((node) => node.addEventListener("click", () => setWorkspaceTab(node.dataset.workspaceTab)));
      el("drawer-close").addEventListener("click", () => closeDrawer());
      el("drawer-backdrop").addEventListener("click", () => closeDrawer());
      document.querySelectorAll("[data-drawer-target]").forEach((node) => node.addEventListener("click", () => openDrawer(node.dataset.drawerTarget)));
      document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeDrawer(); });
      window.addEventListener("resize", () => refreshElasticTabs());
    }

    async function handleAuthenticatedSession() {
      toggleDashboard(true);
      setRailVisible(true);
      await fetchSession();
      await refreshModels();
      await refreshWorkerContext();
      await refreshNetwork();
      await refreshPromptHistory();
      if (state.session?.is_admin) await refreshAdminOverview();
      if (state.lastJobId) await refreshTrackedJob(); else renderTrackedJob({});
      requestAnimationFrame(() => refreshElasticTabs());
      setTimeout(() => refreshElasticTabs(), 120);
      ensurePolling();
    }

    function resetSignedOutState() {
      stopPolling();
      state.session = null; state.lastJobId = ""; state.trackedJob = null; state.activeConversationId = ""; state.conversationCache = {};
      ["user-id","user-balance","job-user-id","worker-id","worker-owner","worker-gpu","worker-vram","worker-system-ram","worker-models","worker-throughput"].forEach((id) => { const node = el(id); if (node) node.value = ""; });
      closeDrawer(); setRailVisible(false); toggleDashboard(false); setAdminVisible(false); setWorkspaceTab("network"); renderSessionPill(); renderTrackedJob({}); renderPromptHistory({ conversations: [], archived_conversations: [] }); renderConversationList({ conversations: [] }); renderConversationDetail({ messages: [] }); renderWorkerQueueState(null); writeJson("network-json", {}); writeJson("local-worker-json", {}); setStatus("auth-status", "Waiting for sign-in.", "ok");
    }

    bind();
    setWorkspaceTab("network");
    setAdminJobTab("all");
    requestAnimationFrame(() => refreshElasticTabs());
    onAuthStateChanged(auth, async (user) => {
      state.authUser = user;
      renderSessionPill();
      if (!user) { resetSignedOutState(); return; }
      try { await handleAuthenticatedSession(); } catch (error) { toggleDashboard(false); showGlobalError(error); }
    });
  </script>
</body>
</html>
"""


def render_dashboard_html(firebase_client_config: dict[str, str] | None = None) -> str:
    config = dict(_DEFAULT_FIREBASE_CONFIG)
    if firebase_client_config:
        config.update(firebase_client_config)
    html = HTML.replace("__FIREBASE_CONFIG__", json.dumps(config))
    return html.replace("__LOGO_DATA_URL__", load_logo_data_url())
