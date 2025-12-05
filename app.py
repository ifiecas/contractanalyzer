import streamlit as st
import requests
from pypdf import PdfReader
from docx import Document
import io

# Modern Professional Theme Configuration
st.set_page_config(
    page_title="Contract Analyzer Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional look
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2E3440;
        --secondary-color: #5E81AC;
        --accent-color: #88C0D0;
        --success-color: #A3BE8C;
        --warning-color: #EBCB8B;
        --danger-color: #BF616A;
        --bg-color: #ECEFF4;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2E3440 0%, #3B4252 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        color: #ECEFF4;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .main-subtitle {
        color: #88C0D0;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2E3440;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #ECEFF4;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #5E81AC 0%, #81A1C1 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #81A1C1 0%, #5E81AC 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #E5E9F0;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        color: #2E3440;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #5E81AC 0%, #81A1C1 100%);
        color: white;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #5E81AC;
    }
    
    .feature-title {
        color: #2E3440;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-text {
        color: #4C566A;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Status indicators */
    .status-connected {
        color: #A3BE8C;
        font-weight: 600;
    }
    
    .status-error {
        color: #BF616A;
        font-weight: 600;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #E5E9F0;
        border-radius: 8px;
        font-weight: 600;
        color: #2E3440;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #E5E9F0;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E5E9F0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">⚖️ Contract Analyzer Pro</div>
    <div class="main-subtitle">🔒 Private AI-Powered Contract Analysis | 100% Local & Secure</div>
</div>
""", unsafe_allow_html=True)

# Foundry Local API endpoint - CORRECTED
FOUNDRY_API = "http://127.0.0.1:50390/v1/chat/completions"
MODEL_NAME = "qwen2.5-0.5b-instruct-generic-gpu:4"

# Function to call Foundry Local API
def call_foundry_api(prompt):
    try:
        response = requests.post(
            FOUNDRY_API,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        # Extract content from the response
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "No response from model"
    except requests.exceptions.HTTPError as e:
        return f"❌ API Error: {e}\n\nResponse: {response.text if response else 'No response'}"
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nMake sure the model is loaded with: foundry model load qwen2.5-0.5b"

# Function to extract text from PDF
def extract_pdf_text(file):
    try:
        pdf = PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to extract text from DOCX
def extract_docx_text(file):
    try:
        doc = Document(io.BytesIO(file.read()))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

# Function to analyze contract
def analyze_contract(contract_text, analysis_type):
    contract_snippet = contract_text[:3500]
    
    prompts = {
        "risks": f"""Analyze this contract and identify potential risks and concerning clauses. Focus on:
- Non-compete clauses
- Liability terms
- Termination conditions
- Auto-renewal terms
- Hidden fees
- One-sided terms

Contract:
{contract_snippet}

List the top 5-7 risks clearly and concisely:""",
        
        "questions": f"""Based on this contract, generate important questions to ask a lawyer before signing. Focus on:
- Ambiguous terms needing clarification
- Areas for negotiation
- Missing protections
- Unusual provisions

Contract:
{contract_snippet}

Generate 7-10 specific, actionable questions:""",
        
        "benefits": f"""Analyze this contract and explain the benefits and rights you receive. Include:
- Your rights and entitlements
- What you're getting from this agreement
- Protections in your favor
- Payment or compensation terms

Contract:
{contract_snippet}

List your key benefits clearly:""",
        
        "summary": f"""Translate this contract into plain English. Explain:
- Main purpose and who the parties are
- Key obligations for each party
- Important terms and conditions
- Duration and how to terminate

Contract:
{contract_snippet}

Provide a clear, easy-to-understand summary:"""
    }
    
    return call_foundry_api(prompts[analysis_type])

# Test API connection
def test_api_connection():
    try:
        response = requests.post(
            FOUNDRY_API,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            },
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

# Sidebar
with st.sidebar:
    st.markdown("### 📁 Upload Document")
    
    # API Status
    if test_api_connection():
        st.markdown('<p class="status-connected">● Connected to Foundry Local</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-error">● Not Connected</p>', unsafe_allow_html=True)
        st.warning("⚠️ Model not loaded!\n\nRun: `foundry model load qwen2.5-0.5b`")
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Choose a contract file",
        type=["pdf", "docx"],
        help="Your document is processed locally and never leaves your computer"
    )
    
    st.markdown("---")
    
    st.markdown("### 🔒 Privacy First")
    st.caption("✓ 100% local processing")
    st.caption("✓ No cloud uploads")
    st.caption("✓ No data retention")
    st.caption("✓ Completely private")
    
    st.markdown("---")
    
    st.markdown("### 🤖 AI Model")
    st.caption(f"Model: qwen2.5-0.5b")
    st.caption("Provider: Foundry Local")
    
    with st.expander("⚙️ Settings"):
        st.code(f"API: {FOUNDRY_API}")
        st.code(f"Model: {MODEL_NAME}")
        st.code(f"Status: {'Online' if test_api_connection() else 'Offline'}")

# Main content
if uploaded_file:
    # Extract text
    with st.spinner("📖 Reading document..."):
        if uploaded_file.name.endswith(".pdf"):
            contract_text = extract_pdf_text(uploaded_file)
        else:
            contract_text = extract_docx_text(uploaded_file)
    
    if contract_text and not contract_text.startswith("Error"):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.success(f"✅ **{uploaded_file.name}** loaded successfully")
        with col2:
            st.info(f"📊 {len(contract_text):,} characters")
        
        # Preview
        with st.expander("📄 Document Preview"):
            st.text_area("First 2000 characters", contract_text[:2000], height=200, disabled=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🚨 Risk Assessment",
            "❓ Questions for Lawyer",
            "✅ Your Benefits",
            "📋 Plain English"
        ])
        
        with tab1:
            st.markdown("#### 🚨 Identify Potential Risks")
            st.caption("Analyze concerning clauses and unfavorable terms")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("▶️ Analyze Risks", key="risks_btn", use_container_width=True):
                with st.spinner("🔍 Analyzing... Please wait (may take 30-60 seconds)"):
                    result = analyze_contract(contract_text, "risks")
                    st.markdown("---")
                    st.markdown(result)
        
        with tab2:
            st.markdown("#### ❓ Questions for Your Attorney")
            st.caption("Important questions to discuss before signing")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("▶️ Generate Questions", key="questions_btn", use_container_width=True):
                with st.spinner("🔍 Generating questions..."):
                    result = analyze_contract(contract_text, "questions")
                    st.markdown("---")
                    st.markdown(result)
        
        with tab3:
            st.markdown("#### ✅ Your Rights & Benefits")
            st.caption("What you're getting from this agreement")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("▶️ Analyze Benefits", key="benefits_btn", use_container_width=True):
                with st.spinner("🔍 Analyzing benefits..."):
                    result = analyze_contract(contract_text, "benefits")
                    st.markdown("---")
                    st.markdown(result)
        
        with tab4:
            st.markdown("#### 📋 Simple Summary")
            st.caption("Contract explained in plain language")
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("▶️ Create Summary", key="summary_btn", use_container_width=True):
                with st.spinner("🔍 Summarizing..."):
                    result = analyze_contract(contract_text, "summary")
                    st.markdown("---")
                    st.markdown(result)
    else:
        st.error(contract_text)

else:
    # Welcome screen with feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🚨 Risk Assessment</div>
            <div class="feature-text">
                Identify concerning clauses, hidden fees, and unfavorable terms 
                that could put you at risk.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">✅ Benefits Analysis</div>
            <div class="feature-text">
                Understand your rights, entitlements, and what you're gaining 
                from the agreement.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">❓ Legal Questions</div>
            <div class="feature-text">
                Generate specific questions to ask your attorney before signing 
                any contract.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📋 Plain English</div>
            <div class="feature-text">
                Translate complex legal language into simple, understandable 
                terms anyone can grasp.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use cases
    st.markdown("### 💼 Perfect For")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 Employment**")
        st.caption("• Job offers")
        st.caption("• Promotion letters")
        st.caption("• Severance packages")
    
    with col2:
        st.markdown("**🏢 Business**")
        st.caption("• Service agreements")
        st.caption("• Vendor contracts")
        st.caption("• Partnership deals")
    
    with col3:
        st.markdown("**🏠 Personal**")
        st.caption("• Rental leases")
        st.caption("• Purchase agreements")
        st.caption("• NDAs")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    # Legal disclaimer
    st.warning("""
    **⚖️ Important Legal Disclaimer**
    
    This tool provides AI-assisted contract analysis to help you better understand 
    legal documents. However, it does **not** constitute legal advice and cannot 
    replace consultation with a qualified attorney. Always seek professional legal 
    counsel for important contracts and legal matters.
    """)

# Footer
st.sidebar.divider()
st.sidebar.caption("🔒 Powered by Foundry Local")
st.sidebar.caption(f"⚡ qwen2.5-0.5b (GPU-accelerated)")
st.sidebar.caption("⚖️ Not legal advice")