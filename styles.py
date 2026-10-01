import gradio as gr

# -------------------------
# Theme: fonts + base colors for Gradio's own components
# -------------------------

THEME = gr.themes.Soft(
    primary_hue="neutral",
    secondary_hue="neutral",
    neutral_hue="neutral",
    # One font everywhere: Schibsted Grotesk (a sturdy news-style sans)
    font=[gr.themes.GoogleFont("Schibsted Grotesk", weights=(400, 500, 600, 700, 800)), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="#ffffff",
    body_text_color="#111111",
    body_text_color_subdued="#555555",
    block_background_fill="#ffffff",
    block_border_width="0px",
    block_shadow="none",
    border_color_primary="#e5e5e5",
    color_accent="#111111",
    color_accent_soft="#f2f2f2",
    input_background_fill="#ffffff",
    button_primary_background_fill="#111111",
    button_primary_background_fill_hover="#333333",
    button_primary_text_color="#ffffff",
)


# -------------------------
# CSS: layout and look of the page
# -------------------------

CSS = """
:root {
  /* Neutrals */
  --surface: #ffffff;       /* page, chat card, bot messages */
  --line: #e5e5e5;          /* borders and dividers */
  --soft: #f5f5f5;          /* location button, chips, user messages */
  --soft-line: #e0e0e0;

  /* Text */
  --ink: #111111;           /* main text      (18.9:1 on white) */
  --muted: #555555;         /* secondary text  (7.5:1 on white) */
  --faint: #767676;         /* placeholder     (4.5:1 on white) */

  /* Actions: black buttons with white text */
  --action: #111111;
  --action-hover: #333333;
  --action-disabled: #d4d4d4;

  /* Highlight colour: used sparingly so it stands out */
  --yellow: #ffd23f;        /* black text on it = 14:1 */
  --yellow-hover: #f5c518;
  --yellow-soft: #fff6d1;

  --heading: 'Schibsted Grotesk', ui-sans-serif, system-ui, sans-serif;
  --focus: 0 0 0 3px rgba(0, 0, 0, 0.2);
}

::selection { background: var(--yellow); color: var(--ink); }

/* Page width and background. The page fills the window; the chat card stretches to fill what's left */
body, .gradio-container { background: var(--surface) !important; }
.gradio-container .app { max-width: 1172px !important; height: 100vh; margin: 0 auto !important; padding: 12px 16px 24px !important; }
footer { display: none !important; }

/* Hidden box that stores "lat,lon" */
#user_location { display: none !important; }

/* ---------- Header: status | title | button ---------- */
#topbar {
  display: grid !important; grid-template-columns: 1fr auto 1fr; align-items: center;
  gap: 16px; padding: 4px 0 10px; flex-grow: 0 !important;
}
#topbar > * { min-width: 0 !important; }
#topbar > .block { padding: 0 !important; }
#peek_btn { justify-self: end; }

.eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }

.title-block { display: flex; align-items: center; gap: 12px; }
.title-block .mascot { width: 46px; }
.title-block .eyebrow { margin: 0 0 2px; }
.title-block h1 {
  font-family: var(--heading); font-size: 28px; line-height: 1.05; font-weight: 800; letter-spacing: -0.03em;
  color: var(--ink); margin: 0;
}
.title-block h1 span {
  color: var(--ink); padding: 0 4px; margin: 0 -2px;
  background: linear-gradient(transparent 48%, var(--yellow) 48%, var(--yellow) 84%, transparent 84%);
}

#peek_btn {
  flex: 0 0 auto !important; min-width: 0 !important; width: auto !important;
  background: var(--soft) !important; color: var(--ink) !important;
  border: 1px solid var(--soft-line) !important; border-radius: 10px !important;
  font-weight: 600 !important; font-size: 13px !important; padding: 8px 16px !important;
  box-shadow: none !important;
}
#peek_btn:hover { background: var(--yellow-soft) !important; border-color: var(--yellow-hover) !important; }

/* While the browser is finding the location */
#peek_btn.locating {
  background: var(--yellow-soft) !important; border-color: var(--ink) !important;
  cursor: progress !important; animation: breathe 1.2s ease-in-out infinite;
}
@keyframes breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(0.97); } }
#peek_btn::before {
  content: ""; width: 16px; height: 16px; margin-right: 8px; background: currentColor;
  -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z'/><circle cx='12' cy='10' r='2.5'/></svg>") center / contain no-repeat;
          mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z'/><circle cx='12' cy='10' r='2.5'/></svg>") center / contain no-repeat;
}

.status { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); }
.status .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--faint); flex: 0 0 auto; }
.status.on { color: var(--ink); }
.status.on .dot { background: var(--yellow); box-shadow: 0 0 0 1.5px var(--ink); }

.mascot { animation: bob 4s ease-in-out infinite; }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@media (prefers-reduced-motion: reduce) { .mascot { animation: none; } }

/* ---------- Chat card ---------- */
#chat_card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 18px;
  overflow: hidden; gap: 0 !important; padding: 0 !important;
  flex: 1 1 0 !important; min-height: 0;
}
#chat_card > .block { padding: 0 !important; }
#chat_card .prose { margin: 0 !important; }
.chat-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 22px; border-bottom: 1px solid var(--line);
}
.agent { display: flex; align-items: center; gap: 10px; }
.agent-icon {
  width: 30px; height: 30px; border-radius: 8px; background: var(--yellow-soft);
  display: grid; place-items: center; color: var(--action);
}
.agent-name { font-family: var(--heading); font-weight: 700; font-size: 15px; color: var(--ink); line-height: 1.2; }
.agent-tag { font-size: 11px; color: var(--muted); }
.ready { font-size: 11px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
.ready::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--yellow); box-shadow: 0 0 0 1.5px var(--ink); }

/* Chat messages area */
#chatbot { flex: 1 1 0 !important; min-height: 0 !important; height: auto !important; border: none !important; border-radius: 0 !important; background: var(--surface) !important; }
#chatbot .bubble-wrap { background: var(--surface) !important; }
#chatbot .message.user { background: var(--soft) !important; border-color: var(--soft-line) !important; }
#chatbot .message.bot { background: var(--surface) !important; border-color: var(--line) !important; }
#chatbot .prose { opacity: 1 !important; }  /* Gradio fades message text to 80% by default */
#chatbot a { color: var(--action); font-weight: 600; }

/* Google Maps links become a yellow pill with a filled pin */
#chatbot a[href*="google.com/maps"] {
  display: inline-flex; align-items: center; gap: 6px; vertical-align: middle;
  margin: 2px 0; padding: 6px 14px 6px 10px; border-radius: 999px;
  background: var(--yellow); color: var(--ink) !important; font-size: 13px; font-weight: 700;
  text-decoration: none !important; box-shadow: none;
  transition: transform 0.15s ease, background 0.15s ease;
}
#chatbot a[href*="google.com/maps"]:hover { background: var(--yellow-hover); transform: translateY(-1px); }
#chatbot a[href*="google.com/maps"]::before {
  content: ""; width: 14px; height: 14px; flex: 0 0 auto; background: currentColor;
  -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='black' fill-rule='evenodd' d='M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 4.5a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5z'/></svg>") center / contain no-repeat;
          mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='black' fill-rule='evenodd' d='M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 4.5a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5z'/></svg>") center / contain no-repeat;
}
#chatbot a[href*="google.com/maps"].popping { animation: squish 0.35s ease; }
@keyframes squish { 0% { transform: scale(1); } 40% { transform: scale(0.92); } 100% { transform: scale(1); } }

/* Little pin bubbles that pop out of the link when it's clicked */
.pin-pop {
  position: fixed; z-index: 9999; pointer-events: none;
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--yellow); border: 2px solid var(--ink);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  opacity: 0; animation: pinpop 0.8s cubic-bezier(0.2, 0.8, 0.3, 1) forwards;
}
.pin-pop::after {
  content: ""; position: absolute; inset: 3px; background: var(--ink);
  -webkit-mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='black' fill-rule='evenodd' d='M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 4.5a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5z'/></svg>") center / contain no-repeat;
          mask: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='black' fill-rule='evenodd' d='M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 4.5a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5z'/></svg>") center / contain no-repeat;
}
/* Black version, used while we wait for the user's location */
.pin-pop.dark { background: var(--ink); border-color: #ffffff; }
.pin-pop.dark::after { background: #ffffff; }

@keyframes pinpop {
  0%   { opacity: 0; transform: translate(0, 0) scale(0.3); }
  25%  { opacity: 1; }
  60%  { opacity: 1; transform: translate(var(--dx), var(--dy)) scale(1); }
  100% { opacity: 0; transform: translate(var(--dx), calc(var(--dy) - 10px)) scale(0.9); }
}

/* Empty-state text */
.ph { text-align: center; }
.ph .eyebrow { margin-bottom: 10px; }
.ph-title { font-family: var(--heading); font-size: 24px; color: var(--ink); margin: 0; font-weight: 700; letter-spacing: -0.02em; }

/* Example chips */
#chatbot .placeholder-content { justify-content: center !important; }
#chatbot .placeholder { flex: 0 0 auto !important; height: auto !important; }
#chatbot .examples {
  display: flex !important; flex-wrap: wrap; justify-content: center; gap: 8px;
  margin: 0 auto !important; padding: 14px 16px 0 !important; max-width: 100% !important;
}
#chatbot .example {
  width: auto !important; flex: 0 0 auto !important;
  padding: 8px 14px !important; border-radius: 999px !important; min-height: 0 !important;
  background: var(--soft) !important; border: 1px solid var(--soft-line) !important;
  color: var(--ink) !important; font-size: 12px !important;
}
#chatbot .example:hover { background: var(--yellow-soft) !important; border-color: var(--yellow-hover) !important; transform: none !important; }

/* Input row */
#chat_card .form, #chat_input { border: none !important; box-shadow: none !important; background: var(--surface) !important; }
#chat_input { border-top: 1px solid var(--line) !important; border-radius: 0 !important; padding: 10px 14px 10px 20px !important; }
#chat_input textarea { font-size: 14px !important; background: transparent !important; box-shadow: none !important; border: none !important; }
#chat_input textarea::placeholder { color: var(--faint); }
#chat_input .submit-button {
  width: 34px !important; height: 34px !important; min-width: 34px !important; border-radius: 50% !important;
  background: var(--action) !important; color: #fff !important; border: none !important;
}
#chat_input .submit-button:hover:not(:disabled) { background: var(--action-hover) !important; }
#chat_input .submit-button:disabled { background: var(--action-disabled) !important; }

/* Keyboard focus: a clear ring on everything you can tab to */
#peek_btn:focus-visible, #chatbot .example:focus-visible, #chat_input .submit-button:focus-visible,
#chatbot a:focus-visible { outline: none !important; box-shadow: var(--focus) !important; }
#chat_input:focus-within { background: #fafafa !important; }

/* Gradio's small copy/share/delete icons: quiet until hovered */
#chatbot .icon-button, #chatbot .icon-button-wrapper button { color: var(--faint) !important; }
#chatbot .icon-button:hover, #chatbot .icon-button-wrapper button:hover { color: var(--action) !important; }

/* ---------- Phone width: title on top, status + button underneath ---------- */
@media (max-width: 720px) {
  #topbar { grid-template-columns: 1fr auto; grid-template-areas: "title title" "status button"; row-gap: 10px; }
  #title_box { grid-area: title; justify-self: center; }
  #status_box { grid-area: status; }
  #peek_btn { grid-area: button; padding: 8px 12px !important; }
  .title-block h1 { font-size: 22px; }
  #chatbot .example { flex: 0 1 auto !important; }
}
"""


# -------------------------
# HTML pieces
# -------------------------

def status_html(shared):
    """Small line under the top bar that shows whether location is shared."""
    if shared:
        return '<div class="status on"><span class="dot"></span>Location shared. Searching near you.</div>'
    return '<div class="status"><span class="dot"></span>Location stays private until you choose to share it.</div>'


MASCOT_SVG = """
<svg class="mascot" viewBox="0 0 120 130" aria-hidden="true">
  <ellipse cx="60" cy="104" rx="32" ry="22" fill="#e5e5e5" stroke="#111111" stroke-width="2.5"/>
  <ellipse cx="60" cy="82" rx="33" ry="6" fill="#ffd23f" stroke="#111111" stroke-width="2"/>
  <circle cx="60" cy="56" r="28" fill="#ffffff" stroke="#111111" stroke-width="2.5"/>
  <circle cx="51" cy="60" r="2.2" fill="#111111"/>
  <circle cx="69" cy="60" r="2.2" fill="#111111"/>
  <path d="M55 68 q5 4 10 0" fill="none" stroke="#111111" stroke-width="2" stroke-linecap="round"/>
  <path d="M34 38 q26 -26 52 0 z" fill="#555555" stroke="#111111" stroke-width="2.5" stroke-linejoin="round"/>
  <ellipse cx="62" cy="38" rx="36" ry="6" fill="#555555" stroke="#111111" stroke-width="2.5"/>
  <circle cx="68" cy="22" r="3.5" fill="#ffd23f" stroke="#111111" stroke-width="1.5"/>
</svg>
"""

TITLE_HTML = f"""
<div class="title-block">
  {MASCOT_SVG}
  <div>
    <p class="eyebrow">Your little local guide</p>
    <h1>Find Me <span>Something</span></h1>
  </div>
</div>
"""

CHAT_HEAD_HTML = """
<div class="chat-head">
  <div class="agent">
    <div class="agent-icon">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>
      </svg>
    </div>
    <div>
      <div class="agent-name">Peekaboo</div>
      <div class="agent-tag">your finding friend</div>
    </div>
  </div>
  <div class="ready">ready</div>
</div>
"""

# Shown inside the chat before the first message
CHAT_PLACEHOLDER = """
<div class="ph">
  <p class="eyebrow">A good place to start</p>
  <p class="ph-title">What would you like to find?</p>
</div>
"""


# Added to the page's <head>, so the browser runs it as soon as the page opens:
# 1. keeps the page in light mode so the colors above always look right
# 2. when a Google Maps link is clicked, pops little pin bubbles out of it,
#    then opens Google Maps in a new tab
PAGE_HEAD = """
<script>
(() => {
  const url = new URL(window.location);
  if (url.searchParams.get("__theme") !== "light") {
    url.searchParams.set("__theme", "light");
    window.location.href = url.href;
    return;
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest('#chatbot a[href*="google.com/maps"]');
    if (!link) return;

    event.preventDefault();
    event.stopPropagation();

    // Skip the animation for people who prefer less motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      window.open(link.href, "_blank", "noopener");
      return;
    }

    const box = link.getBoundingClientRect();
    const bubbles = [[-26, -34, 0], [0, -48, 70], [26, -34, 140]];  // [x, y, delay]

    bubbles.forEach(([dx, dy, delay]) => {
      const bubble = document.createElement("span");
      bubble.className = "pin-pop";
      bubble.style.left = (box.left + box.width / 2 - 12) + "px";
      bubble.style.top = (box.top) + "px";
      bubble.style.setProperty("--dx", dx + "px");
      bubble.style.setProperty("--dy", dy + "px");
      bubble.style.animationDelay = delay + "ms";
      document.body.appendChild(bubble);
      setTimeout(() => bubble.remove(), 1000 + delay);
    });

    link.classList.add("popping");
    setTimeout(() => {
      link.classList.remove("popping");
      window.open(link.href, "_blank", "noopener");
    }, 450);
  }, true);
})();
</script>
"""


# Runs when the "Let me peek nearby" button is clicked: the browser shows its
# permission popup, and whatever this returns ("lat,lon" or "") goes into the hidden box.
LOCATION_JS = """
() => new Promise((resolve) => {
  if (!navigator.geolocation) {
    alert("Your browser doesn't support location sharing.");
    return resolve("");
  }

  const button = document.getElementById("peek_btn");
  const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Pop three black pin bubbles out of the bottom of the button
  const popBubbles = () => {
    if (!button || calm) return;
    const box = button.getBoundingClientRect();
    const bubbles = [[-30, 40, 0], [0, 54, 90], [30, 40, 180]];  // [x, y, delay]

    bubbles.forEach(([dx, dy, delay]) => {
      const bubble = document.createElement("span");
      bubble.className = "pin-pop dark";
      bubble.style.left = (box.left + box.width / 2 - 12) + "px";
      bubble.style.top = (box.top + box.height / 2 - 12) + "px";
      bubble.style.setProperty("--dx", dx + "px");
      bubble.style.setProperty("--dy", dy + "px");
      bubble.style.animationDelay = delay + "ms";
      document.body.appendChild(bubble);
      setTimeout(() => bubble.remove(), 1000 + delay);
    });
  };

  // Keep popping until the browser gives us the location (or fails)
  popBubbles();
  const loop = setInterval(popBubbles, 900);
  if (button) button.classList.add("locating");

  const finish = (value) => {
    clearInterval(loop);
    if (button) button.classList.remove("locating");
    resolve(value);
  };

  navigator.geolocation.getCurrentPosition(
    (pos) => finish(`${pos.coords.latitude},${pos.coords.longitude}`),
    (err) => {
      finish("");
      alert("Couldn't get your location: " + err.message +
            "\\nIf you blocked it before, click the icon left of the address bar and allow Location.");
    },
    { timeout: 20000 }  // give up after 20 seconds so the bubbles don't run forever
  );
})
"""
