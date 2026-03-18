import streamlit as st
from openai import OpenAI
import subprocess, re, socket, json

st.set_page_config(
    page_title="Contract Analyzer",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@300;400&family=Lato:wght@300;400;700&display=swap');

:root {
    --bg:          #FAFAF8;
    --surface:     #FFFFFF;
    --border:      #E8E5DF;
    --text:        #1C1C1A;
    --muted:       #7A7A75;
    --accent:      #5C4A32;
    --red-bg:      #FDF2F2;
    --red-bd:      #E53E3E;
    --amber-bg:    #FFFBF0;
    --amber-bd:    #D97706;
    --green-bg:    #F0FDF6;
    --green-bd:    #16A34A;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Lato', sans-serif;
    color: var(--text);
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }

.main .block-container {
    max-width: 700px !important;
    margin: 0 auto !important;
    padding: 5rem 1.5rem 8rem !important;
}

/* Disclaimer banner */
.disclaimer-banner {
    background: #FFFBF0;
    border: 1px solid #D97706;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}
.disclaimer-content {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
}
.disclaimer-icon { font-size: 1rem; margin-top: 0.1rem; }
.disclaimer-text {
    font-size: 0.82rem;
    font-weight: 300;
    color: #92400E;
    line-height: 1.6;
}
.disclaimer-text b { font-weight: 700; }
.dismiss-btn {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #D97706;
    cursor: pointer;
    background: none;
    border: none;
    padding: 0;
    white-space: nowrap;
    margin-top: 0.1rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.dismiss-btn:hover { opacity: 0.6; }

/* Nav */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 5rem;
}
.nav-brand {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
}
.nav-pill {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
}

/* Hero */
.hero { margin-bottom: 3.5rem; }
.hero h1 {
    font-family: 'Lora', serif;
    font-size: 2.5rem;
    font-weight: 400;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 1rem;
}
.hero h1 em { font-style: italic; color: var(--accent); }
.hero p {
    font-size: 1rem;
    font-weight: 300;
    color: var(--muted);
    line-height: 1.7;
}

/* Upload */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 8px !important;
    padding: 2rem 1.5rem !important;
}
[data-testid="stFileUploader"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--accent) !important;
}
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] p {
    font-size: 0.85rem !important;
    color: var(--muted) !important;
    font-weight: 300 !important;
}

/* Button */
.stButton > button {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: var(--text) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.75 !important; }

.rule { border: none; border-top: 1px solid var(--border); margin: 3rem 0; }

/* Risk banner */
.risk-banner {
    border-radius: 8px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 3rem;
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
}
.risk-banner.high   { background: var(--red-bg);   border-left: 4px solid var(--red-bd);   }
.risk-banner.medium { background: var(--amber-bg); border-left: 4px solid var(--amber-bd); }
.risk-banner.low    { background: var(--green-bg); border-left: 4px solid var(--green-bd); }
.risk-icon { font-size: 1.5rem; }
.risk-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.risk-banner.high   .risk-label { color: var(--red-bd);   }
.risk-banner.medium .risk-label { color: var(--amber-bd); }
.risk-banner.low    .risk-label { color: var(--green-bd); }
.risk-text {
    font-family: 'Lora', serif;
    font-size: 1rem;
    line-height: 1.55;
    color: var(--text);
}

/* Section */
.section { margin-bottom: 3rem; }
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* Summary */
.summary-text {
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    line-height: 1.8;
    color: var(--text);
}

/* Parties */
.party { padding: 1rem 0; border-bottom: 1px solid var(--border); }
.party:last-child { border-bottom: none; }
.party-name { font-size: 0.9rem; font-weight: 700; color: var(--text); margin-bottom: 0.1rem; }
.party-role {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--accent);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.party-obligations { font-size: 0.88rem; font-weight: 300; color: #3A3A38; line-height: 1.65; }

/* Terms */
.term { display: grid; grid-template-columns: 160px 1fr; gap: 1.25rem; padding: 0.85rem 0; border-bottom: 1px solid var(--border); align-items: baseline; }
.term:last-child { border-bottom: none; }
.term-name { font-size: 0.85rem; font-weight: 700; color: var(--text); }
.term-detail { font-size: 0.88rem; font-weight: 300; color: #3A3A38; line-height: 1.65; }

/* Flags */
.flag { border-radius: 6px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; }
.flag.high   { background: var(--red-bg);   border-left: 3px solid var(--red-bd);   }
.flag.medium { background: var(--amber-bg); border-left: 3px solid var(--amber-bd); }
.flag.low    { background: var(--green-bg); border-left: 3px solid var(--green-bd); }
.flag-severity {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.flag.high   .flag-severity { color: var(--red-bd);   }
.flag.medium .flag-severity { color: var(--amber-bd); }
.flag.low    .flag-severity { color: var(--green-bd); }
.flag-issue { font-size: 0.9rem; font-weight: 700; color: var(--text); margin-bottom: 0.2rem; }
.flag-clause { font-family: 'IBM Plex Mono', monospace; font-size: 0.73rem; color: var(--muted); margin-bottom: 0.4rem; }
.flag-suggestion { font-size: 0.85rem; font-weight: 300; color: #3A3A38; line-height: 1.6; }
.flag-suggestion b { font-weight: 700; color: var(--text); }

/* Data rows */
.data-row { display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border); gap: 1rem; }
.data-row:last-child { border-bottom: none; }
.data-label { font-size: 0.88rem; font-weight: 300; color: var(--muted); }
.data-value { font-size: 0.88rem; font-weight: 700; color: var(--text); text-align: right; }

/* Recommendation */
.rec-box { background: var(--text); border-radius: 8px; padding: 1.75rem 2rem; margin-bottom: 3rem; }
.rec-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #888882;
    margin-bottom: 0.75rem;
}
.rec-text { font-family: 'Lora', serif; font-size: 1.05rem; line-height: 1.75; color: var(--bg); }

/* Questions */
.question { display: flex; gap: 1rem; padding: 0.9rem 0; border-bottom: 1px solid var(--border); align-items: flex-start; }
.question:last-child { border-bottom: none; }
.q-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    color: var(--accent);
    min-width: 22px;
    margin-top: 0.15rem;
}
.q-text { font-size: 0.9rem; font-weight: 400; color: var(--text); line-height: 1.6; }

/* Footer */
.footer { margin-top: 5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; }
.footer span { font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# ── Port detection ─────────────────────────────────────────────────────────────
def find_foundry_port():
    try:
        result = subprocess.run(["foundry", "service", "status"], capture_output=True, text=True, timeout=5)
        match = re.search(r'http://127\.0\.0\.1:(\d+)', result.stdout + result.stderr)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    for port in [52657, 50934, 51000, 51234, 52000]:
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=0.5)
            s.close()
            return port
        except Exception:
            continue
    return 50934

@st.cache_resource
def get_client():
    port = find_foundry_port()
    return OpenAI(base_url=f"http://127.0.0.1:{port}/v1", api_key="foundry"), port

SYSTEM_PROMPT = """You are a contract analyst helping everyday people understand contracts before signing.

Analyze the contract and respond ONLY with a valid JSON object — no markdown, no extra text, just raw JSON:

{
  "risk_level": "high|medium|low",
  "risk_summary": "One clear sentence summarising the overall risk",
  "summary": "2-3 plain-English sentences: what is this contract, who are the parties, what is the main purpose",
  "parties": [
    {"name": "Party name", "role": "e.g. Employer / Employee / Landlord / Tenant", "obligations": "Plain English: what they must do"}
  ],
  "key_terms": [
    {"term": "Legal term or clause name", "detail": "Plain English explanation relevant to the signer"}
  ],
  "red_flags": [
    {"severity": "high|medium|low", "issue": "Short title", "clause": "Brief quote or clause reference", "suggestion": "What to negotiate or watch out for"}
  ],
  "key_dates": [{"label": "What this date is", "value": "Date or duration"}],
  "key_numbers": [{"label": "What this figure is", "value": "Amount or figure"}],
  "recommendation": "2-3 sentences: sign as-is, negotiate, or avoid — and the most important reason",
  "questions_to_ask": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]
}

Be specific, plain, and focus on what matters most to someone signing this for the first time. Return ONLY valid JSON."""

MODEL = "Phi-4-mini-instruct-generic-gpu:5"

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
    <span class="nav-brand">◈ Contract Analyzer</span>
    <div style="display:flex;align-items:center;gap:0.5rem;">
        <span class="nav-pill">Local · Private · Offline</span>
        <span class="nav-pill">🤖 Phi-4-mini</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Dismissible disclaimer banner ──────────────────────────────────────────────
if "disclaimer_dismissed" not in st.session_state:
    st.session_state.disclaimer_dismissed = False

if not st.session_state.disclaimer_dismissed:
    col1, col2 = st.columns([10, 1])
    with col1:
        st.markdown("""
        <div style="background:#FFFBF0;border:1px solid #D97706;border-radius:8px;padding:1rem 1.25rem;margin-bottom:0.5rem;display:flex;gap:0.75rem;align-items:flex-start;">
            <span style="font-size:1rem;margin-top:0.1rem;">⚠️</span>
            <span style="font-size:0.82rem;font-weight:300;color:#92400E;line-height:1.6;">
                <b>Not legal advice.</b> This tool helps you understand what you're reading — think of it as a smart friend who read the contract first. Always consult a qualified legal professional before signing anything important.
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("✕", key="dismiss_disclaimer"):
            st.session_state.disclaimer_dismissed = True
            st.rerun()

st.markdown("""
<div class="hero">
    <h1>Understand what<br>you're <em>signing.</em></h1>
    <p>Upload your contract for a plain-English breakdown — fully offline. Nothing leaves your device.</p>
</div>
""", unsafe_allow_html=True)

try:
    import fitz
    file_types = ["pdf", "txt", "md"]
except ImportError:
    file_types = ["txt", "md"]

uploaded_file = st.file_uploader("Upload your contract", type=file_types, label_visibility="collapsed")

contract_text = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        try:
            import fitz
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            contract_text = "".join(page.get_text() for page in doc)
            num_pages = len(doc)
            doc.close()
            st.success(f"✓ {uploaded_file.name}  ·  {num_pages} page{'s' if num_pages != 1 else ''}")
        except Exception as e:
            st.error(f"Could not read PDF: {e}")
    else:
        contract_text = uploaded_file.read().decode("utf-8")
        st.success(f"✓ {uploaded_file.name}")

st.markdown("<br>", unsafe_allow_html=True)
analyze = st.button("Analyze →")

# ── Output ─────────────────────────────────────────────────────────────────────
if analyze:
    if not contract_text.strip():
        st.warning("Please upload a contract file first.")
    else:
        st.markdown('<hr class="rule">', unsafe_allow_html=True)
        client, port = get_client()

        with st.spinner("Reading your contract..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Analyze this contract:\n\n{contract_text}"}
                    ],
                    temperature=0.2,
                    max_tokens=2048,
                )
                raw = response.choices[0].message.content
                raw = re.sub(r'^```json\s*', '', raw.strip())
                raw = re.sub(r'^```\s*', '', raw.strip())
                raw = re.sub(r'\s*```$', '', raw.strip())
                data = json.loads(raw)

                risk = data.get("risk_level", "medium").lower()
                icons  = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                labels = {"high": "High Risk — Review carefully before signing", "medium": "Medium Risk — Some points to clarify first", "low": "Low Risk — Looks reasonable"}

                st.markdown(f"""
                <div class="risk-banner {risk}">
                    <div class="risk-icon">{icons.get(risk,'🟡')}</div>
                    <div>
                        <div class="risk-label">{labels.get(risk,'')}</div>
                        <div class="risk-text">{data.get('risk_summary','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                # What is this contract
                st.markdown(f"""
                <div class="section">
                    <div class="section-label">What is this contract</div>
                    <div class="summary-text">{data.get('summary','')}</div>
                </div>""", unsafe_allow_html=True)

                # Who is involved
                parties = data.get("parties", [])
                if parties:
                    p_html = "".join([f"""<div class="party">
                        <div class="party-name">{p.get('name','')}</div>
                        <div class="party-role">{p.get('role','')}</div>
                        <div class="party-obligations">{p.get('obligations','')}</div>
                    </div>""" for p in parties])
                    st.markdown(f"""<div class="section"><div class="section-label">Who is involved</div>{p_html}</div>""", unsafe_allow_html=True)

                # Red flags
                flags = data.get("red_flags", [])
                if flags:
                    f_html = "".join([f"""<div class="flag {f.get('severity','medium').lower()}">
                        <div class="flag-severity">{f.get('severity','').upper()} RISK</div>
                        <div class="flag-issue">{f.get('issue','')}</div>
                        <div class="flag-clause">{f.get('clause','')}</div>
                        <div class="flag-suggestion"><b>What to do:</b> {f.get('suggestion','')}</div>
                    </div>""" for f in flags])
                    st.markdown(f"""<div class="section"><div class="section-label">Red flags</div>{f_html}</div>""", unsafe_allow_html=True)

                # Terms explained
                terms = data.get("key_terms", [])
                if terms:
                    t_html = "".join([f"""<div class="term">
                        <div class="term-name">{t.get('term','')}</div>
                        <div class="term-detail">{t.get('detail','')}</div>
                    </div>""" for t in terms])
                    st.markdown(f"""<div class="section"><div class="section-label">Terms explained</div>{t_html}</div>""", unsafe_allow_html=True)

                # Dates & numbers
                dates   = data.get("key_dates", [])
                numbers = data.get("key_numbers", [])
                all_data = [(d.get('label',''), d.get('value','')) for d in dates + numbers]
                if all_data:
                    rows = "".join([f"""<div class="data-row">
                        <div class="data-label">{label}</div>
                        <div class="data-value">{value}</div>
                    </div>""" for label, value in all_data])
                    st.markdown(f"""<div class="section"><div class="section-label">Key dates & numbers</div>{rows}</div>""", unsafe_allow_html=True)

                # Recommendation
                st.markdown(f"""
                <div class="rec-box">
                    <div class="rec-label">Recommendation</div>
                    <div class="rec-text">{data.get('recommendation','')}</div>
                </div>""", unsafe_allow_html=True)

                # Questions to ask
                questions = data.get("questions_to_ask", [])
                if questions:
                    q_html = "".join([f"""<div class="question">
                        <div class="q-num">0{i+1}</div>
                        <div class="q-text">{q}</div>
                    </div>""" for i, q in enumerate(questions)])
                    st.markdown(f"""<div class="section"><div class="section-label">Ask before you sign</div>{q_html}</div>""", unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.markdown(f"""<div class="section"><div class="section-label">Analysis</div><div class="summary-text">{raw}</div></div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Could not connect to Foundry Local. Make sure it's running: `foundry model run phi-4-mini`\n\nError: {str(e)}")

st.markdown("""
<div class="footer">
    <span>All analysis runs locally</span>
    <span>Powered by Foundry Local</span>
</div>""", unsafe_allow_html=True)
