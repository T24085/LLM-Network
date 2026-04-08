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
  <title>LLM Network</title>
  <meta name="description" content="Public landing page and dashboard entry for the LLM Network.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root{--bg:#071018;--panel:#102634;--line:rgba(255,255,255,.1);--text:#edf4ef;--muted:#a7bcc2;--aqua:#63dbc9;--gold:#f2c772;--shadow:0 24px 70px rgba(0,0,0,.28)}
    *{box-sizing:border-box} html{scroll-behavior:smooth}
    body{margin:0;background:radial-gradient(circle at top left,rgba(99,219,201,.13),transparent 28%),linear-gradient(180deg,#071018,#0b141d);color:var(--text);font-family:"Instrument Sans","Segoe UI",sans-serif}
    a{color:inherit;text-decoration:none} button{font:inherit} .container{max-width:1360px;margin:0 auto}
    .hero{min-height:100svh;padding:24px;display:grid;align-items:start}
    .topbar,.metric-grid,.story,.pricing,.faq,.final{display:grid;gap:16px}
    .topbar{grid-template-columns:1fr auto;align-items:center}
    .brand{display:flex;align-items:center;gap:14px}
    .brand-logo{width:58px;height:58px;object-fit:contain;display:block;filter:drop-shadow(0 10px 18px rgba(0,0,0,.18))}
    .brand strong,.section h2,.price,.display{font-family:"Space Grotesk","Segoe UI",sans-serif}
    .brand span,.nav a,.lede,.fine,.faq p,.plan p,.story p,.feature-list li,.section p{color:var(--muted)}
    .brand span{display:block;font-size:.82rem;letter-spacing:.1em;text-transform:uppercase}
    .nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:12px 18px}
    .nav a{font-size:.95rem}
    .hero-grid{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(540px,.98fr);gap:48px;align-items:center;min-height:calc(100svh - 88px)}
    .hero-grid > *,.two-col > *{min-width:0}
    .eyebrow{display:inline-flex;align-items:center;gap:10px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.04);font-size:.82rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
    .eyebrow::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--aqua);box-shadow:0 0 14px rgba(99,219,201,.5)}
    .display{margin:18px 0 16px;max-width:9ch;font-size:clamp(3.4rem,8vw,6.2rem);line-height:.93;letter-spacing:-.05em}
    .lede{max-width:34rem;font-size:1.06rem;line-height:1.7}
    .cta-row,.signal-row{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
    .cta-row{justify-content:flex-start;margin:28px 0 16px}
    .button{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 20px;border-radius:999px;border:1px solid transparent;cursor:pointer;transition:transform .18s ease}
    .button:hover{transform:translateY(-1px)}
    .button-primary{background:linear-gradient(135deg,var(--aqua),#28abb6);color:#071018;font-weight:700}
    .button-secondary{background:rgba(255,255,255,.03);border-color:var(--line);color:var(--text)}
    .pill{display:inline-flex;align-items:center;gap:10px;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.04)}
    .pill::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--gold)}
    .poster{position:relative;min-height:660px;border:1px solid var(--line);border-radius:32px;background:radial-gradient(circle at 60% 45%,rgba(99,219,201,.16),transparent 20%),linear-gradient(160deg,rgba(12,29,40,.92),rgba(7,16,24,.82));box-shadow:var(--shadow);overflow:hidden}
    .poster::before,.poster::after{content:"";position:absolute;border:1px solid rgba(255,255,255,.08);border-radius:50%}
    .poster::before{inset:10%}.poster::after{inset:20%}
    .core{position:absolute;left:50%;top:45%;width:170px;height:170px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(242,199,114,.95),rgba(242,199,114,.18) 34%,transparent 62%)}
    .poster-logo{position:absolute;left:50%;top:33%;width:min(360px,62%);transform:translateX(-50%);opacity:.92;filter:drop-shadow(0 18px 28px rgba(0,0,0,.28))}
    .node,.terminal,.summary,.panel,.plan,.faq-item,.story-item{border:1px solid var(--line);background:rgba(255,255,255,.03);box-shadow:var(--shadow)}
    .node{position:absolute;z-index:2;max-width:210px;padding:12px 14px;border-radius:18px;backdrop-filter:blur(10px)} .node small{display:block;color:#91e1d6;text-transform:uppercase;letter-spacing:.06em;font-size:.7rem} .node span{display:block;color:var(--muted);font-size:.82rem;margin-top:4px}
    .n1{top:12%;right:7%}.n2{top:38%;right:9%}.n3{left:7%;bottom:26%}.n4{left:9%;top:20%}
    .poster-floor{position:absolute;left:24px;right:24px;bottom:24px;z-index:1;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(220px,.85fr);gap:14px;align-items:stretch}
    .terminal,.summary{min-width:0;padding:16px 18px;border-radius:22px}
    .terminal code,.summary code{display:block;white-space:pre-wrap;overflow-wrap:anywhere;color:#c9f0eb;font:inherit;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.78rem;line-height:1.55}
    main{padding:0 24px 84px}
    .section{padding:92px 0;border-top:1px solid var(--line)}
    .section-head{max-width:760px;margin-bottom:32px}
    .label{color:var(--gold);font-size:.82rem;letter-spacing:.14em;text-transform:uppercase}
    .section h2{margin:10px 0 12px;font-size:clamp(2rem,4vw,3.5rem);line-height:1.02;letter-spacing:-.04em}
    .section p{margin:0;line-height:1.7}
    .panel{border-radius:28px;overflow:hidden}
    .two-col{display:grid;grid-template-columns:1.05fr .95fr}
    .feature-copy,.dashboard-preview{padding:32px}
    .feature-list{margin:0;padding:0;list-style:none;display:grid;gap:16px}
    .feature-list li{padding-bottom:16px;border-bottom:1px solid var(--line);line-height:1.6}
    .metric-grid{grid-template-columns:repeat(2,minmax(0,1fr));margin:18px 0}
    .metric{padding:15px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.03)}
    .metric strong{display:block;font-size:1.5rem}
    .rail{display:grid;gap:10px;padding-top:14px;border-top:1px solid var(--line)}
    .rail div{display:flex;justify-content:space-between;gap:12px}
    .pricing,.story,.faq{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
    .pricing{align-items:start}
    .plan,.story-item,.faq-item{padding:26px;border-radius:28px}
    .plan.featured{background:linear-gradient(180deg,rgba(99,219,201,.14),rgba(255,255,255,.03));transform:translateY(-8px)}
    .plan-kicker{color:var(--gold);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}
    .plan h3,.story-item h3,.faq-item h3{margin:10px 0 10px;font-size:1.14rem}
    .price{margin:0 0 12px;font-size:clamp(2.4rem,4vw,3.2rem);letter-spacing:-.04em}
    .price span{font-size:1rem;font-family:"Instrument Sans","Segoe UI",sans-serif;color:var(--muted)}
    .plan ul{margin:0 0 22px;padding:0;list-style:none;display:grid;gap:10px}
    .plan li{position:relative;padding-left:18px;line-height:1.5}
    .plan li::before{content:"";position:absolute;left:0;top:.55em;width:8px;height:8px;border-radius:50%;background:var(--aqua)}
    .story-item strong{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;background:rgba(242,199,114,.14);color:var(--gold);font-family:"Space Grotesk","Segoe UI",sans-serif}
    .final{grid-template-columns:1fr auto;align-items:end;padding:34px;border:1px solid var(--line);border-radius:34px;background:linear-gradient(135deg,rgba(99,219,201,.16),rgba(255,255,255,.03))}
    footer{padding:20px 24px 36px;color:var(--muted)} .footer-row{max-width:1180px;margin:0 auto;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:18px}
    @media (max-width:1240px){.hero-grid{grid-template-columns:1fr}.poster{max-width:760px;width:100%;justify-self:center}.n2{top:56%;right:8%}.n3{bottom:24%}}
    @media (max-width:1040px){.two-col,.final{grid-template-columns:1fr}.plan.featured{transform:none}}
    @media (max-width:720px){.hero,main,footer{padding-inline:18px}.topbar{grid-template-columns:1fr}.nav{justify-content:flex-start}.display{font-size:clamp(3rem,18vw,4.3rem)}.poster{min-height:560px}.poster-floor,.metric-grid{grid-template-columns:1fr}.button{width:100%}.node{max-width:170px}.n1{right:4%}.n2{top:52%;right:4%}.n3{left:4%;bottom:28%}.n4{left:4%}}
  </style>
</head>
<body>
  <section class="hero">
    <div class="container">
      <header class="topbar">
        <div class="brand">
          <img src="__LOGO_DATA_URL__" alt="LLM Network logo" class="brand-logo">
          <div>
            <strong>LLM Network</strong>
            <span>Local inference exchange</span>
          </div>
        </div>
        <nav class="nav" aria-label="Primary">
          <a href="#why">Why it works</a>
          <a href="#pricing">Pricing</a>
          <a href="#faq">FAQ</a>
          <a data-dashboard-link href="./dashboard">Dashboard</a>
        </nav>
      </header>

      <div class="hero-grid">
        <div>
          <div class="eyebrow">Verified workers. Shared credits. Google login.</div>
          <h1 class="display">Run the network from one front door.</h1>
          <p class="lede">Everything for the LLM Network lives here: the product story, pricing, credit economics, and the direct path into the main dashboard where users sign in, submit jobs, and operate local workers.</p>
          <div class="cta-row">
            <button id="hero-sign-in" class="button button-primary" type="button">Sign in with Google</button>
            <a class="button button-secondary" data-dashboard-link href="./dashboard">Open dashboard</a>
            <a class="button button-secondary" href="#pricing">See pricing</a>
          </div>
          <div class="signal-row">
            <div id="session-pill" class="pill">Checking session status</div>
            <div id="auth-status" class="fine">First sign-in can bootstrap a stable network identity with launch credits.</div>
          </div>
        </div>

        <div class="poster" aria-hidden="true">
          <div class="core"></div>
          <img src="__LOGO_DATA_URL__" alt="" class="poster-logo">
          <div class="node n1"><small>Dashboard</small><strong>Control Room</strong><span>Wallet, queue, workers, CLI pack</span></div>
          <div class="node n2"><small>Worker</small><strong>RTX 4090 Local Node</strong><span>Approved Ollama models with verified throughput</span></div>
          <div class="node n3"><small>Usage</small><strong>Prompt Dispatch</strong><span>Reserve credits, route jobs, collect results</span></div>
          <div class="node n4"><small>Identity</small><strong>Google Bound Account</strong><span>One stable network id across sessions</span></div>
          <div class="poster-floor">
            <div class="terminal"><code>python -m ollama_network.server --host 127.0.0.1 --port 8000

python -m ollama_network.cli --server-url http://127.0.0.1:8000 submit-job --model-tag qwen3:4b --prompt "Summarize the worker protocol."</code></div>
            <div class="summary"><code>Queue depth: 12 active jobs
Connected workers: 48 verified
Credit exchange: $1 = 100 credits
Launch credit: 5 bootstrap credits</code></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <main>
    <div class="container">
      <section id="why" class="section">
        <div class="section-head">
          <div class="label">Find Everything Fast</div>
          <h2>A public front page for discovery, with the real operator surface one click away.</h2>
          <p>The landing page explains the network clearly, anchors pricing to credits, and sends users straight into the authenticated dashboard instead of making them hunt for the product surface.</p>
        </div>
        <div class="panel two-col">
          <div class="feature-copy">
            <ul class="feature-list">
              <li><strong>Google login opens the same network identity every time.</strong><br>The dashboard binds one stable user id to the Google account on first sign-in and reuses it later.</li>
              <li><strong>Approved local Ollama models are visible in one place.</strong><br>Users can inspect models, queue work, and see how jobs move across the network.</li>
              <li><strong>Worker operations stay inside the same control room.</strong><br>Operators can start a local worker loop, review hardware detection, and export CLI commands without leaving the UI.</li>
              <li><strong>Pricing is expressed in credits, not vague tiers.</strong><br>The page makes launch credits and wallet top-ups obvious before the user signs in.</li>
            </ul>
          </div>
          <div class="dashboard-preview">
            <div class="pill">Main control room</div>
            <div class="metric-grid">
              <div class="metric"><strong>5.0</strong><span>Bootstrap credits at first sign-in</span></div>
              <div class="metric"><strong>4s</strong><span>Auto refresh rhythm for network state</span></div>
              <div class="metric"><strong>1</strong><span>Stable user identity per Google account</span></div>
              <div class="metric"><strong>0</strong><span>Cloud fallback in the worker runtime</span></div>
            </div>
            <div class="rail">
              <div><span>Sign in</span><strong>Google popup</strong></div>
              <div><span>Wallet</span><strong>Credits, pending, earned, spent</strong></div>
              <div><span>Workers</span><strong>Detected GPU + approved models</strong></div>
              <div><span>CLI pack</span><strong>Copy exact commands from the UI</strong></div>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" class="section">
        <div class="section-head">
          <div class="label">Pricing</div>
          <h2>Start free, buy credits directly, or bring a full worker fleet.</h2>
          <p>The credit model is intentionally simple. New users can launch without paying first, power users can top up linearly, and labs can roll in multiple verified workers under custom operations.</p>
        </div>
        <div class="pricing">
          <article class="plan">
            <div class="plan-kicker">Launch</div>
            <h3>Explorer</h3>
            <div class="price">$0 <span>to start</span></div>
            <p>For first-time users who want to sign in, inspect the network, and submit initial jobs from the dashboard.</p>
            <ul>
              <li>5 bootstrap credits on first authenticated session</li>
              <li>Google sign-in and stable network user id</li>
              <li>Dashboard access, model browser, and queue visibility</li>
              <li>Best for evaluation, demos, and first prompts</li>
            </ul>
            <button class="button button-secondary" type="button" data-sign-in>Launch free</button>
          </article>

          <article class="plan featured">
            <div class="plan-kicker">Most direct</div>
            <h3>Operator Credits</h3>
            <div class="price">$1 <span>= 100 credits</span></div>
            <p>Top up only what you need, then spend credits on jobs or earn them back by serving work from your own local node.</p>
            <ul>
              <li>Linear top-up model with no forced subscription</li>
              <li>Ideal for recurring prompting and worker payouts</li>
              <li>Uses the same wallet and ledger already exposed by the service</li>
              <li>Keeps product pricing grounded in the existing backend</li>
            </ul>
            <a class="button button-primary" data-dashboard-link href="./dashboard">Open wallet in dashboard</a>
          </article>

          <article class="plan">
            <div class="plan-kicker">Scale</div>
            <h3>Fleet</h3>
            <div class="price">Custom <span>lab rollout</span></div>
            <p>For teams that want coordinated worker onboarding, curated model approvals, and a tighter operating loop around local-only inference.</p>
            <ul>
              <li>Multi-worker operations and benchmark baselining</li>
              <li>Policy tuning around approved models and routing</li>
              <li>Useful when one machine is no longer enough</li>
              <li>Leaves room for a future enterprise layer without changing the core ledger</li>
            </ul>
            <a class="button button-secondary" href="#faq">Review rollout notes</a>
          </article>
        </div>
      </section>

      <section class="section">
        <div class="section-head">
          <div class="label">Workflow</div>
          <h2>From sign-in to worker revenue in three moves.</h2>
          <p>The page explains the whole operating loop without burying the actual action surface behind docs or scattered links.</p>
        </div>
        <div class="story">
          <article class="story-item"><strong>1</strong><h3>Enter through the landing page</h3><p>Review what the network does, see how credits work, and authenticate directly from the hero without guessing where the dashboard lives.</p></article>
          <article class="story-item"><strong>2</strong><h3>Use the dashboard as the source of truth</h3><p>Submit jobs, inspect balances, load approved models, and copy the exact CLI pack needed to automate the same actions outside the browser.</p></article>
          <article class="story-item"><strong>3</strong><h3>Turn local hardware into network supply</h3><p>Start a same-machine local worker loop, publish verified throughput, and earn credits when public jobs land on your node.</p></article>
        </div>
      </section>

      <section id="faq" class="section">
        <div class="section-head">
          <div class="label">FAQ</div>
          <h2>Clear answers before users hit the control room.</h2>
          <p>The landing page now covers the questions people usually ask before they commit to a workflow or spend credits.</p>
        </div>
        <div class="faq">
          <article class="faq-item"><h3>Do I have to pay before I can see the dashboard?</h3><p>No. The page routes users into the dashboard with Google sign-in, and new authenticated sessions can receive bootstrap credits so they can start without a purchase.</p></article>
          <article class="faq-item"><h3>How are credits priced?</h3><p>The current exchange is straight-line pricing: one US dollar adds one hundred credits to the wallet. That maps directly to the existing purchase flow in the service layer.</p></article>
          <article class="faq-item"><h3>Is this tied to cloud inference?</h3><p>No. The product position and the worker tooling stay local-only. The dashboard and copy both reinforce that the network is built around approved Ollama workers without cloud fallback.</p></article>
          <article class="faq-item"><h3>Where do I manage workers and CLI commands?</h3><p>Inside the main dashboard. The landing page is now the public discovery surface, while `/dashboard` remains the operator surface for authenticated usage, worker control, and CLI generation.</p></article>
        </div>
      </section>

      <section class="section">
        <div class="final">
          <div>
            <div class="label">Open The Network</div>
            <h2>Start here, then move straight into the main control room.</h2>
            <p>Review pricing, sign in with Google, and continue into the dashboard to submit work and run local nodes.</p>
          </div>
          <div class="cta-row" style="margin:0">
            <button class="button button-primary" type="button" data-sign-in>Sign in and continue</button>
            <a class="button button-secondary" data-dashboard-link href="./dashboard">Go to dashboard</a>
          </div>
        </div>
      </section>
    </div>
  </main>

  <footer>
    <div class="footer-row">
      <span>LLM Network homepage and dashboard entry</span>
      <span>Local-only Ollama inference coordination</span>
    </div>
  </footer>

  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-app.js";
    import { GoogleAuthProvider, getAuth, onAuthStateChanged, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-auth.js";

    const FIREBASE_CONFIG = __FIREBASE_CONFIG__;
    const authReady = Boolean(FIREBASE_CONFIG.apiKey && FIREBASE_CONFIG.projectId);
    const dashboardUrl = new URL("./dashboard", window.location.href).toString();
    const sessionPill = document.getElementById("session-pill");
    const authStatus = document.getElementById("auth-status");
    const signInButtons = [...document.querySelectorAll("[data-sign-in]"), document.getElementById("hero-sign-in")].filter(Boolean);
    const dashboardLinks = [...document.querySelectorAll("[data-dashboard-link]")];
    let auth = null;
    let provider = null;

    function setAuthMessage(pill, message) {
      sessionPill.textContent = pill;
      authStatus.textContent = message;
    }

    function toggleButtons(disabled, label) {
      signInButtons.forEach((button) => {
        button.disabled = disabled;
        if (label) button.textContent = label;
      });
    }

    async function handleSignIn() {
      if (!auth || !provider) {
        setAuthMessage("Firebase not configured", "Add Firebase web keys to enable browser sign-in, or open /dashboard after configuration.");
        return;
      }
      try {
        toggleButtons(true, "Opening Google...");
        setAuthMessage("Opening sign-in", "Completing Google authentication.");
        await signInWithPopup(auth, provider);
        setAuthMessage("Signed in", "Redirecting to the main dashboard.");
        window.location.href = dashboardUrl;
      } catch (error) {
        const message = error?.message || String(error);
        setAuthMessage("Sign-in failed", message);
        toggleButtons(false, "Sign in with Google");
      }
    }

    function bind() {
      signInButtons.forEach((button) => button.addEventListener("click", handleSignIn));
      dashboardLinks.forEach((link) => { link.href = dashboardUrl; });
    }

    function bootAuth() {
      if (!authReady) {
        setAuthMessage("Firebase not configured", "Sign-in is disabled until the Firebase client config is present.");
        toggleButtons(true, "Login unavailable");
        return;
      }

      const app = initializeApp(FIREBASE_CONFIG);
      auth = getAuth(app);
      provider = new GoogleAuthProvider();
      provider.setCustomParameters({ prompt: "select_account" });

      onAuthStateChanged(auth, (user) => {
        if (!user) {
          setAuthMessage("Ready for sign-in", "Open the dashboard or sign in here to continue with your bound network account.");
          toggleButtons(false, "Sign in with Google");
          return;
        }
        const name = user.displayName || user.email || "Signed-in user";
        setAuthMessage("Session detected", `Continue to the dashboard as ${name}.`);
        signInButtons.forEach((button) => { button.textContent = "Continue to dashboard"; });
      });
    }

    bind();
    bootAuth();
  </script>
</body>
</html>
"""


def render_landing_html(firebase_client_config: dict[str, str] | None = None) -> str:
    config = dict(_DEFAULT_FIREBASE_CONFIG)
    if firebase_client_config:
        config.update(firebase_client_config)
    html = HTML.replace("__FIREBASE_CONFIG__", json.dumps(config))
    return html.replace("__LOGO_DATA_URL__", load_logo_data_url())
