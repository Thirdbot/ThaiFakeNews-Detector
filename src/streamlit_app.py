import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
ENDPOINT_URL = os.environ.get("HF_ENDPOINT_URL")

st.set_page_config(
    page_title="Thai Fake News Detector",
    page_icon="🔍",
    layout="centered",
)

# ── Premium Dark Theme CSS with Animations ────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #000000;
        --bg-secondary: #0a0a0a;
        --bg-card: #111111;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --text-primary: #ffffff;
        --text-secondary: #a1a1aa;
        --text-muted: #52525b;
        --border-color: rgba(255, 255, 255, 0.08);
        --glow-purple: rgba(139, 92, 246, 0.4);
    }
    
    *:not([data-testid="stIconMaterial"]) {
        font-family: 'Noto Sans Thai', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Main Background with Animated Gradient */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139, 92, 246, 0.15), transparent),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(236, 72, 153, 0.1), transparent),
            radial-gradient(ellipse 40% 30% at 0% 100%, rgba(6, 182, 212, 0.08), transparent);
        min-height: 100vh;
    }
    
    /* Floating Orbs Animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.06) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.04) 0%, transparent 50%);
        animation: floatOrbs 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes floatOrbs {
        0%, 100% { 
            background-position: 0% 0%, 100% 100%, 50% 50%;
            opacity: 0.6;
        }
        25% { 
            background-position: 30% 70%, 70% 30%, 20% 80%;
            opacity: 0.8;
        }
        50% { 
            background-position: 100% 50%, 0% 50%, 80% 20%;
            opacity: 1;
        }
        75% { 
            background-position: 70% 30%, 30% 70%, 50% 50%;
            opacity: 0.7;
        }
    }
    
    /* Grid Lines Background */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Title with Shimmer Effect */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(
            90deg, 
            #ffffff 0%, 
            #8b5cf6 25%, 
            #ec4899 50%, 
            #8b5cf6 75%, 
            #ffffff 100%
        );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite;
        filter: drop-shadow(0 0 30px var(--glow-purple));
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Subtitle with Fade Animation */
    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        opacity: 0;
        animation: fadeSlideUp 0.8s ease forwards 0.3s;
    }
    
    @keyframes fadeSlideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Glass Card Style */
    .glass-card {
        background: linear-gradient(
            135deg,
            rgba(17, 17, 17, 0.8) 0%,
            rgba(17, 17, 17, 0.6) 100%
        );
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        animation: cardAppear 0.6s ease forwards;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.03),
            transparent
        );
        animation: cardShine 4s ease-in-out infinite;
    }
    
    @keyframes cardShine {
        0%, 100% { left: -100%; }
        50% { left: 100%; }
    }
    
    @keyframes cardAppear {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--accent-purple), var(--accent-pink));
        border-radius: 4px 0 0 4px;
    }
    
    .info-box p {
        color: var(--text-secondary);
        margin: 0;
        line-height: 1.8;
        font-size: 0.95rem;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #0a0a0a 100%) !important;
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 2rem 1rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 2.5rem;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 10px 40px rgba(139, 92, 246, 0.3); }
        50% { transform: scale(1.05); box-shadow: 0 15px 50px rgba(139, 92, 246, 0.4); }
    }
    
    .sidebar-title {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }
    
    .sidebar-subtitle {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    /* Sidebar Link Cards */
    .link-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 0.875rem 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-decoration: none;
    }
    
    .link-card:hover {
        background: rgba(139, 92, 246, 0.1);
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateX(4px);
    }
    
    .link-card .icon {
        width: 36px;
        height: 36px;
        background: rgba(139, 92, 246, 0.15);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    
    .link-card .text {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .link-card:hover .text {
        color: var(--text-primary);
    }
    
    .link-card a {
        color: inherit !important;
        text-decoration: none !important;
    }
    
    /* Stats Card */
    .stats-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
        border: 1px solid rgba(6, 182, 212, 0.15);
        border-radius: 16px;
        padding: 1.25rem;
        margin-top: 1.5rem;
    }
    
    .stats-card .stat-label {
        color: var(--accent-cyan);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .stats-card .stat-value {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .stats-card .stat-desc {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(17, 17, 17, 0.9) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15), 0 0 30px rgba(139, 92, 246, 0.1) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    .stTextArea label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Secondary Button */
    div[data-testid="column"]:last-child .stButton > button {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: none !important;
    }
    
    div[data-testid="column"]:last-child .stButton > button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: none !important;
    }
    
    /* Result Cards */
    .result-card {
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: resultAppear 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes resultAppear {
        0% {
            opacity: 0;
            transform: scale(0.8) translateY(20px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .result-real {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 78, 59, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 0 60px rgba(16, 185, 129, 0.15);
    }
    
    .result-fake {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(127, 29, 29, 0.2) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        box-shadow: 0 0 60px rgba(239, 68, 68, 0.15);
    }
    
    .result-unknown {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(120, 53, 15, 0.2) 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 0 60px rgba(251, 191, 36, 0.15);
    }
    
    .result-icon-wrapper {
        width: 100px;
        height: 100px;
        margin: 0 auto 1.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        animation: iconBounce 0.8s ease forwards 0.3s;
        opacity: 0;
    }
    
    .result-real .result-icon-wrapper {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(16, 185, 129, 0.1));
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.3);
    }
    
    .result-fake .result-icon-wrapper {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(239, 68, 68, 0.1));
        box-shadow: 0 0 40px rgba(239, 68, 68, 0.3);
    }
    
    .result-unknown .result-icon-wrapper {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.3), rgba(251, 191, 36, 0.1));
        box-shadow: 0 0 40px rgba(251, 191, 36, 0.3);
    }
    
    @keyframes iconBounce {
        0% { opacity: 0; transform: scale(0.3); }
        50% { transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .result-real .result-title { color: var(--accent-green); }
    .result-fake .result-title { color: var(--accent-red); }
    .result-unknown .result-title { color: #fbbf24; }
    
    .result-desc {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Loading Animation */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .loading-dots {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 1.5rem;
    }
    
    .loading-dot {
        width: 14px;
        height: 14px;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
        border-radius: 50%;
        animation: dotPulse 1.4s ease-in-out infinite;
    }
    
    .loading-dot:nth-child(1) { animation-delay: 0s; }
    .loading-dot:nth-child(2) { animation-delay: 0.15s; }
    .loading-dot:nth-child(3) { animation-delay: 0.3s; }
    
    @keyframes dotPulse {
        0%, 80%, 100% { 
            transform: scale(0.6);
            opacity: 0.4;
        }
        40% { 
            transform: scale(1.2);
            opacity: 1;
        }
    }
    
    .loading-text {
        color: var(--accent-purple);
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), rgba(139, 92, 246, 0.3), var(--border-color), transparent);
        margin: 2.5rem 0;
        position: relative;
    }
    
    .divider::after {
        content: '';
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 8px;
        height: 8px;
        background: var(--accent-purple);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--accent-purple);
    }
    
    /* Section Title */
    .section-title {
        text-align: center;
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] details summary {
        background: rgba(17, 17, 17, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        list-style: none !important;
    }

    [data-testid="stExpander"] details[open] summary {
        border-radius: 12px 12px 0 0 !important;
    }

    /* Hide default arrow */
    [data-testid="stExpander"] details summary::-webkit-details-marker,
    [data-testid="stExpander"] details summary::marker {
        display: none !important;
        content: '' !important;
    }

    [data-testid="stExpander"] details summary svg {
        fill: var(--text-muted) !important;
    }

    .streamlit-expanderContent,
    [data-testid="stExpander"] details > div {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid var(--border-color) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
    }
    
    .footer p {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin: 0.25rem 0;
    }
    
    .footer-brand {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
        color: var(--text-muted);
        font-size: 0.85rem;
    }
    
    .footer-brand span {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-purple), var(--accent-pink));
        border-radius: 4px;
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
    }
    
    div[data-testid="stAlert"] {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.2) !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🛡️</div>
        <h2 class="sidebar-title">Thai Fake News</h2>
        <p class="sidebar-subtitle">AI Detection System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color: #8b5cf6; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">Project Links</p>
    
    <a href="https://huggingface.co/spaces/thirdExec/thai_fakenews_detector" target="_blank" style="text-decoration: none;">
        <div class="link-card">
            <div class="icon">🤗</div>
            <span class="text">HF Space</span>
        </div>
    </a>
    
    <a href="https://github.com/Thirdbot/FineTuneSloth" target="_blank" style="text-decoration: none;">
        <div class="link-card">
            <div class="icon">💻</div>
            <span class="text">Training Code</span>
        </div>
    </a>
    
    <a href="https://huggingface.co/thirdExec/Qwen2.5-1.5B-Instruct-ThaiFakeNews-bnb-4bit" target="_blank" style="text-decoration: none;">
        <div class="link-card">
            <div class="icon">🧠</div>
            <span class="text">Model</span>
        </div>
    </a>
    
    <a href="https://huggingface.co/datasets/EXt1/Thai-True-Fake-News" target="_blank" style="text-decoration: none;">
        <div class="link-card">
            <div class="icon">📊</div>
            <span class="text">Dataset</span>
        </div>
    </a>
    
    <div class="stats-card">
        <div class="stat-label">Training Dataset</div>
        <div class="stat-value">6,004</div>
        <div class="stat-desc">Thai news articles (2017-2024)<br>from Antifakenewscenter Thailand</div>
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">ตรวจสอบข่าวปลอม</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Thai Fake News Detector · Powered by Qwen2.5-1.5B</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <p>
        โมเดลนี้ใช้ <strong style="color: #8b5cf6;">Qwen2.5-1.5B</strong> ที่ผ่านการ fine-tune 
        บนชุดข้อมูลข่าวภาษาไทย 6,004 บทความ เพื่อจำแนกว่าข่าวนั้นเป็น 
        <strong style="color: #10b981;">ข่าวจริง</strong> หรือ 
        <strong style="color: #ef4444;">ข่าวปลอม</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
if "news_input" not in st.session_state:
    st.session_state.news_input = ""

news_input = st.text_area(
    "ใส่หัวข้อข่าวหรือเนื้อหาข่าวที่ต้องการตรวจสอบ",
    placeholder="เช่น: รัฐบาลแจกเงินคนละ 10,000 บาท ผ่านแอปเป๋าตัง",
    height=160,
    key="news_input",
)

run = st.button("ตรวจสอบข่าว", type="primary", use_container_width=True)

# ── Inference ─────────────────────────────────────────────────────────────────
if run:
    if not news_input.strip():
        st.warning("กรุณาใส่ข้อความข่าวก่อนตรวจสอบ")
    else:
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
        <div class="loading-container">
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
            <p class="loading-text">กำลังวิเคราะห์ข่าว...</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            client = InferenceClient(base_url=ENDPOINT_URL, token=os.environ.get("HF_TOKEN"))

            response = client.text_generation(
                news_input.strip(),
                max_new_tokens=20,
                temperature=0.05,
                do_sample=True,
            )
            
            loading_placeholder.empty()

            generated = response.split("### Response:")[-1].strip()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">ผลการตรวจสอบ</div>', unsafe_allow_html=True)

            if "จริง" in generated:
                st.markdown("""
                <div class="result-card result-real">
                    <div class="result-icon-wrapper">✓</div>
                    <h2 class="result-title">ข่าวจริง</h2>
                    <p class="result-desc">โมเดลประเมินว่าข่าวนี้มีแนวโน้มเป็น <strong>ข่าวจริง</strong></p>
                </div>
                """, unsafe_allow_html=True)
            elif "ปลอม" in generated:
                st.markdown("""
                <div class="result-card result-fake">
                    <div class="result-icon-wrapper">✗</div>
                    <h2 class="result-title">ข่าวปลอม</h2>
                    <p class="result-desc">โมเดลประเมินว่าข่าวนี้มีแนวโน้มเป็น <strong>ข่าวปลอม</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card result-unknown">
                    <div class="result-icon-wrapper">?</div>
                    <h2 class="result-title">ไม่สามารถวิเคราะห์ได้</h2>
                    <p class="result-desc">โมเดลไม่สามารถระบุได้ว่าเป็นข่าวจริงหรือข่าวปลอม</p>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("ดูผลลัพธ์ดิบจากโมเดล"):
                st.code(response, language=None)

        except Exception as exc:
            loading_placeholder.empty()
            st.error(f"เกิดข้อผิดพลาด: {exc}")
            st.markdown("""
            <div class="info-box" style="border-color: rgba(239, 68, 68, 0.3); background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(127, 29, 29, 0.05) 100%);">
                <p style="color: #fbbf24; font-weight: 600; margin-bottom: 0.75rem;">แนวทางแก้ไข:</p>
                <p style="color: #a1a1aa;">
                    • ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต<br>
                    • โมเดลอาจยังไม่พร้อมใช้งานผ่าน Inference API<br>
                    • ลองเปิด <a href="https://huggingface.co/spaces/thirdExec/thai_fakenews_detector" style="color: #8b5cf6;">HF Space</a> แทน
                </p>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>ผลการตรวจสอบจากโมเดล AI อาจไม่ถูกต้องเสมอไป</p>
    <p>กรุณายืนยันจากแหล่งข่าวที่น่าเชื่อถือก่อนเผยแพร่ต่อ</p>
    <div class="footer-brand">
        Made with <span>Thai Fake News Detection Team</span>
    </div>
</div>
""", unsafe_allow_html=True)
