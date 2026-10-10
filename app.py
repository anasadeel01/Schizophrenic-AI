"""The Schizophrenic AI — light, polished Streamlit frontend.

Run from the project directory:
    streamlit run app.py

Uses the existing answer(prompt) function from schizo.py.
"""
import html
import streamlit as st
import streamlit.components.v1 as components

from schizo import answer

st.set_page_config(
    page_title="Schizophrenic AI | Explore Perspectives",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Visual system ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
      --ink: #17213b;
      --muted: #66728b;
      --purple: #6558d9;
      --blue: #4d7df2;
      --line: #e4e9f4;
      --surface: rgba(255,255,255,.84);
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] {
      color: var(--ink);
      background:
        radial-gradient(ellipse at 5% 3%, rgba(153, 171, 255, .26), transparent 32%),
        radial-gradient(ellipse at 92% 13%, rgba(123, 222, 218, .22), transparent 29%),
        radial-gradient(ellipse at 50% 75%, rgba(222, 218, 255, .18), transparent 38%),
        #f7f9fe;
    }
    [data-testid="stHeader"] { background: rgba(247,249,254,.72); }
    [data-testid="stMain"] { background: transparent; }
    .block-container { max-width: 1160px; padding-top: 1.15rem; padding-bottom: 3.5rem; }
    #MainMenu, footer { visibility: hidden; }

    .topbar {
      display:flex; align-items:center; justify-content:space-between; gap:16px;
      padding: 10px 0 19px; border-bottom:1px solid rgba(113,129,166,.18);
    }
    .brand { display:flex; align-items:center; gap:11px; color:#202b48; font-weight:800; font-size:13px; letter-spacing:.08em; }
    .brand-mark {
      display:grid; place-items:center; width:39px; height:39px; border-radius:14px;
      color:white; font-size:20px; background:linear-gradient(135deg,#8176f1,#5d77e9 65%,#54c9ce);
      box-shadow:0 8px 20px rgba(99,105,220,.23);
    }
    .top-pill {
      display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid #e1e7f3;
      border-radius:999px; background:rgba(255,255,255,.7); color:#64718b;
      font-size:11px; font-weight:700; letter-spacing:.035em;
    }
    .live-dot { width:7px; height:7px; border-radius:50%; background:#39b98a; box-shadow:0 0 0 4px rgba(57,185,138,.12); }
    .hero-kicker {
      display:inline-flex; gap:8px; align-items:center; padding:7px 11px; border-radius:999px;
      color:#5b56bc; background:#eeedff; border:1px solid #e2e0ff;
      font-size:10px; font-weight:800; letter-spacing:.11em; text-transform:uppercase;
    }
    .hero-title {
      font-family:'Space Grotesk',sans-serif; font-size:clamp(42px,5.5vw,69px); line-height:1.04;
      letter-spacing:-.065em; color:#1a2542; font-weight:700; margin:19px 0 16px;
    }
    .hero-title .accent {
      background:linear-gradient(100deg,#6558d9,#4e82e8 58%,#27aeb3);
      color:transparent; -webkit-background-clip:text; background-clip:text;
    }
    .hero-copy { color:#64718a; max-width:525px; font-size:15px; line-height:1.85; margin-bottom:20px; }
    .feature-row { display:flex; flex-wrap:wrap; gap:9px; margin-top:19px; }
    .feature-chip {
      display:inline-flex; align-items:center; gap:7px; padding:9px 12px; border-radius:12px;
      background:rgba(255,255,255,.78); border:1px solid #e4e9f5; color:#45526e;
      font-size:11px; font-weight:700; box-shadow:0 3px 10px rgba(38,57,97,.025);
      transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
    }
    .feature-chip:hover { transform:translateY(-3px); box-shadow:0 9px 22px rgba(63,77,143,.11); border-color:#c8ccfa; }
    .section-eyebrow { margin:28px 0 11px; color:#747fa0; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }
    .panel-heading { color:#1c2845; font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:21px; letter-spacing:-.035em; }
    .panel-subheading { color:#738099; font-size:12px; line-height:1.65; margin:4px 0 17px; }
    [data-testid="stVerticalBlockBorderWrapper"] {
      background:rgba(255,255,255,.78); border:1px solid rgba(219,226,241,.94);
      border-radius:22px; box-shadow:0 12px 35px rgba(44,62,110,.055);
      transition:box-shadow .25s ease, transform .25s ease, border-color .25s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
      box-shadow:0 17px 42px rgba(44,62,110,.085); border-color:#d4dcf4;
    }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
      color:#1d2947!important; background:#fbfcff!important; border:1px solid #dce3f1!important;
      border-radius:13px!important; caret-color:#6558d9!important;
    }
    [data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color:#96a0b5!important; }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
      border-color:#8d86ed!important; box-shadow:0 0 0 3px rgba(111,99,221,.12)!important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
      background:#fbfcff!important; border-color:#dce3f1!important; border-radius:12px!important; color:#25314f!important;
    }
    div.stButton > button, div.stFormSubmitButton > button, div.stDownloadButton > button {
      border:1px solid transparent; border-radius:13px; min-height:45px;
      background:linear-gradient(100deg,#6e62e5,#5a75e6 62%,#39b9c0);
      color:white!important; font-weight:800; box-shadow:0 7px 16px rgba(93,101,216,.18);
      transition:transform .2s ease, box-shadow .2s ease, filter .2s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover, div.stDownloadButton > button:hover {
      transform:translateY(-2px); box-shadow:0 12px 23px rgba(93,101,216,.25); filter:saturate(1.12);
    }
    div.stButton > button:active, div.stFormSubmitButton > button:active { transform:translateY(0) scale(.99); }
    [data-testid="stChatMessage"] {
      background:rgba(255,255,255,.88); border:1px solid #e1e7f3; border-radius:17px;
      padding:15px 17px; box-shadow:0 5px 18px rgba(36,54,99,.035);
      animation:rise-in .35s ease both;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { color:#293652; line-height:1.8; }
    [data-testid="stCaptionContainer"], .stCaption { color:#6d7a94!important; }
    [data-testid="stMarkdownContainer"] p { color:inherit; }
    [data-testid="stAlert"] { border-radius:14px; }
    .response-note { padding:12px 14px; border-radius:12px; background:#f0f4ff; border:1px solid #e1e8ff; color:#586782; font-size:12px; line-height:1.65; }
    .footer-note { text-align:center; color:#8792aa; font-size:10px; letter-spacing:.08em; margin-top:34px; }
    @keyframes rise-in { from {opacity:0; transform:translateY(8px)} to {opacity:1; transform:translateY(0)} }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation:none!important; transition:none!important; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topbar">
      <div class="brand"><span class="brand-mark">🎭</span><span>SCHIZOPHRENIC AI</span></div>
      <div class="top-pill"><span class="live-dot"></span> AI PERSONA EXPERIMENT</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero ----------
hero, visual = st.columns([1.08, .92], gap="large")
with hero:
    st.markdown(
        """
        <div style="padding-top:23px">
          <div class="hero-kicker">✦ A different kind of AI conversation</div>
          <h1 class="hero-title">One question.<br><span class="accent">Many perspectives.</span></h1>
          <p class="hero-copy">Explore how a generative model responds through an unpredictable persona. Ask a question, discover an unexpected perspective, and save the ideas that stay with you.</p>
          <div class="feature-row">
            <span class="feature-chip">✧ Dynamic personas</span>
            <span class="feature-chip">◎ Interactive experience</span>
            <span class="feature-chip">↗ Save your conversation</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with visual:
    components.html(
        r"""
        <div id="scene-wrap" style="height:365px;position:relative;overflow:hidden;border-radius:25px;background:radial-gradient(ellipse at 50% 48%,#eef0ff 0%,#f6f8ff 48%,#fbfdff 100%);border:1px solid #d9e2f5;box-shadow:0 16px 40px rgba(70,88,150,.09);perspective:900px;">
          <div style="position:absolute;left:20px;top:18px;color:#7b87a4;font:700 10px 'DM Sans',sans-serif;letter-spacing:1.6px;z-index:5">NEURAL FIELD <span style="color:#a6add0">/ 001</span></div>
          <div style="position:absolute;right:20px;bottom:18px;color:#8591aa;font:700 9px 'DM Sans',sans-serif;letter-spacing:1.5px;z-index:5">THINK BEYOND THE EXPECTED</div>
          <div id="orb-stage" style="position:absolute;inset:0;display:grid;place-items:center;transform-style:preserve-3d;">
            <div class="halo"></div>
            <div class="orbit orbit-one"><span class="satellite sat-one"></span></div>
            <div class="orbit orbit-two"><span class="satellite sat-two"></span></div>
            <div class="orbit orbit-three"></div>
            <div class="orb">
              <div class="orb-shine"></div><div class="orb-line line-a"></div><div class="orb-line line-b"></div>
            </div>
            <div class="spark spark-a"></div><div class="spark spark-b"></div><div class="spark spark-c"></div>
            <div class="spark spark-d"></div><div class="spark spark-e"></div><div class="spark spark-f"></div>
          </div>
        </div>
        <style>
          *{box-sizing:border-box}
          #orb-stage{transition:transform .25s ease-out}
          .halo{position:absolute;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(137,133,247,.23),rgba(110,204,226,.12) 43%,transparent 70%);filter:blur(4px);animation:haloPulse 4s ease-in-out infinite}
          .orb{position:absolute;width:154px;height:154px;border-radius:50%;overflow:hidden;transform:translateZ(45px);background:radial-gradient(circle at 29% 22%,#ffffff 0%,#d8d9ff 10%,#a3a4f5 28%,#8179e9 49%,#696bd5 68%,#5f92d8 83%,#83dce0 100%);box-shadow:inset -17px -19px 35px rgba(54,65,153,.29),inset 9px 8px 19px rgba(255,255,255,.88),0 22px 38px rgba(101,103,213,.25),0 0 48px rgba(127,141,241,.2);animation:orbFloat 5s ease-in-out infinite}
          .orb:after{content:"";position:absolute;inset:0;border-radius:50%;background:linear-gradient(135deg,rgba(255,255,255,.46),transparent 35%,rgba(87,105,203,.13) 75%,rgba(255,255,255,.13));}
          .orb-shine{position:absolute;left:24px;top:18px;width:52px;height:26px;border-radius:50%;background:rgba(255,255,255,.72);filter:blur(9px);transform:rotate(-38deg);z-index:2}
          .orb-line{position:absolute;z-index:1;border:1px solid rgba(255,255,255,.28);border-radius:50%;width:220px;height:80px;left:-32px;top:37px;transform:rotate(-36deg)}
          .line-b{transform:rotate(53deg);width:185px;height:105px;left:-15px;top:20px;border-color:rgba(81,218,223,.4)}
          .orbit{position:absolute;border:1.5px solid rgba(116,132,225,.65);border-radius:50%;transform-style:preserve-3d}
          .orbit-one{width:220px;height:220px;transform:rotateX(67deg) rotateZ(-24deg);animation:spinOne 9s linear infinite}
          .orbit-two{width:255px;height:180px;transform:rotateX(68deg) rotateY(28deg) rotateZ(25deg);border-color:rgba(75,190,204,.7);animation:spinTwo 11s linear infinite}
          .orbit-three{width:205px;height:205px;border:1px dashed rgba(145,151,225,.43);transform:rotateY(68deg) rotateZ(-18deg);animation:spinThree 16s linear infinite}
          .satellite{position:absolute;width:12px;height:12px;border-radius:50%;display:block;box-shadow:0 0 15px currentColor}
          .sat-one{background:#64cdd2;color:#64cdd2;left:15%;top:12%}
          .sat-two{background:#9284f0;color:#9284f0;right:8%;bottom:19%;width:9px;height:9px}
          .spark{position:absolute;width:5px;height:5px;border-radius:50%;background:#9aa3f4;box-shadow:0 0 12px rgba(114,128,232,.8);animation:twinkle 2.7s ease-in-out infinite}
          .spark-a{left:23%;top:31%}.spark-b{right:24%;top:28%;animation-delay:.5s}.spark-c{left:28%;bottom:27%;animation-delay:1s}.spark-d{right:20%;bottom:31%;animation-delay:1.4s}.spark-e{left:50%;top:23%;width:3px;height:3px;animation-delay:.8s}.spark-f{right:34%;top:68%;width:4px;height:4px;animation-delay:1.8s}
          @keyframes orbFloat{0%,100%{transform:translateY(0) translateZ(45px)}50%{transform:translateY(-10px) translateZ(45px)}}
          @keyframes spinOne{from{transform:rotateX(67deg) rotateZ(-24deg)}to{transform:rotateX(67deg) rotateZ(336deg)}}
          @keyframes spinTwo{from{transform:rotateX(68deg) rotateY(28deg) rotateZ(25deg)}to{transform:rotateX(68deg) rotateY(28deg) rotateZ(-335deg)}}
          @keyframes spinThree{from{transform:rotateY(68deg) rotateZ(-18deg)}to{transform:rotateY(68deg) rotateZ(342deg)}}
          @keyframes haloPulse{0%,100%{transform:scale(.9);opacity:.65}50%{transform:scale(1.12);opacity:1}}
          @keyframes twinkle{0%,100%{opacity:.35;transform:scale(.75)}50%{opacity:1;transform:scale(1.5)}}
          @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}
        </style>
        <script>
        (() => {
          const wrap=document.getElementById('scene-wrap'), stage=document.getElementById('orb-stage');
          wrap.addEventListener('pointermove',e=>{
            const r=wrap.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
            stage.style.transform=`rotateX(${-y*8}deg) rotateY(${x*9}deg)`;
          });
          wrap.addEventListener('pointerleave',()=>stage.style.transform='rotateX(0deg) rotateY(0deg)');
        })();
        </script>
        """,
        height=375,
        scrolling=False,
    )

st.markdown('<div class="section-eyebrow">01 &nbsp; / &nbsp; Conversation workspace</div>', unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<div class="panel-heading">What would you like to explore?</div><div class="panel-subheading">Choose a topic to get started, or write a question in your own words.</div>', unsafe_allow_html=True)

    starters = [
        "Choose a suggested question…",
        "What will cities look like in 2050?",
        "How should humanity respond to climate change?",
        "What do you think about electric cars?",
        "Tell me about the future of healthcare.",
        "Could artificial intelligence ever become conscious?",
    ]
    if "draft_prompt" not in st.session_state:
        st.session_state.draft_prompt = ""
    selected = st.selectbox("Suggested questions", starters, label_visibility="collapsed", key="starter_select")
    if selected != starters[0]:
        st.session_state.draft_prompt = selected

    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_input(
            "Your question",
            value=st.session_state.draft_prompt,
            placeholder="Type a question or idea here…",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("✦  Generate perspective", use_container_width=True)

    if submitted:
        st.session_state.draft_prompt = ""
        if not prompt.strip():
            st.warning("Enter a question first, and your AI conversation can begin.")
        elif st.session_state.get("request_count", 0) >= 15:
            st.warning("You've reached the 15-request demo limit for this session.")
        else:
            st.session_state.request_count = st.session_state.get("request_count", 0) + 1
            st.session_state.setdefault("history", []).append(("user", prompt.strip()))
            with st.spinner("Exploring a new perspective…"):
                try:
                    result = answer(prompt.strip())
                    response, persona = result if isinstance(result, tuple) else (result, None)
                    response = str(response)
                except Exception as exc:
                    error_text = str(exc)
                    if "429" in error_text or "quota" in error_text.lower() or "RESOURCE_EXHAUSTED" in error_text:
                        response = (
                            "The AI provider's request quota is currently exhausted, so I couldn't generate a response. "
                            "Your frontend is working correctly. Please wait for the quota to reset or configure an API provider "
                            "with available quota, then try again."
                        )
                    else:
                        response = f"Generation failed: {error_text}"
                    persona = None
            st.session_state.history.append(("assistant", response))
            st.session_state.last_persona = persona

# ---------- Conversation history ----------
if st.session_state.get("history"):
    st.markdown('<div class="section-eyebrow">02 &nbsp; / &nbsp; Conversation</div>', unsafe_allow_html=True)
    for index, (role, message) in enumerate(st.session_state.history):
        avatar = "🤖" if role == "assistant" else "🧑"
        with st.chat_message(role, avatar=avatar):
            st.markdown(html.escape(message).replace("\n", "  \n"), unsafe_allow_html=False)

    if st.session_state.history[-1][0] == "assistant":
        with st.expander("View generation details"):
            st.write("Persona:", st.session_state.get("last_persona") or "Not available")

    user_messages = [m for r, m in st.session_state.history if r == "user"]
    col_download, col_clear = st.columns([1, 1])
    with col_download:
        if user_messages:
            st.download_button(
                "↓  Download conversation",
                data="\n\n".join(f"{r.upper()}: {m}" for r, m in st.session_state.history),
                file_name="schizophrenic_ai_conversation.txt",
                mime="text/plain",
                use_container_width=True,
            )
    with col_clear:
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.history = []
            st.session_state.request_count = 0
            st.session_state.last_persona = None
            st.rerun()

st.markdown(
    '<div class="footer-note">SCHIZOPHRENIC AI &nbsp; · &nbsp; GENERATIVE PERSONA EXPERIMENT &nbsp; · &nbsp; EXPERIMENTAL SYSTEM</div>',
    unsafe_allow_html=True,
)
