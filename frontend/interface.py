"""Banking AI Agent — Premium Dark Mode Streamlit Chat Interface."""

import os
import json
import streamlit as st
import requests

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Banking AI Agent",
    page_icon="🏦",
    layout="wide",
)

# ---- INJECT PREMIUM CUSTOM CSS (FORCING DARK MODE & AESTHETICS) ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography & Colors */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }
    
    /* Background Force Dark Mode */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d1527 0%, #03050a 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    /* Sidebar Premium Style */
    section[data-testid="stSidebar"] {
        background-color: #05080e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding-top: 2rem !important;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Chat Message Bubbles Design */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -4px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* User Chat Bubble */
    [data-testid="stChatMessage"][data-test-role="user"] {
        background-color: rgba(30, 41, 59, 0.45) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
    }
    
    /* Assistant Chat Bubble */
    [data-testid="stChatMessage"][data-test-role="assistant"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
    }

    /* Streamlit Expander styling */
    .conda-expander, [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        margin-top: 10px !important;
    }
    
    /* Text input bar */
    div[data-testid="stChatInput"] {
        border-radius: 12px !important;
        background-color: #0b101c !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 -10px 25px -5px rgba(0,0,0,0.4) !important;
    }
    
    /* Custom Header Styles */
    .title-gradient {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.85rem;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
        letter-spacing: -0.04em;
    }
    
    .subtitle-light {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 25px;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.06) !important;
        margin: 20px 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_backend_health():
    """Check if the backend API is healthy."""
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None


def get_backend_config():
    """Get the backend configuration."""
    try:
        resp = requests.get(f"{API_BASE_URL}/config", timeout=5)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None


def display_workflow_details(data: dict):
    """Display the structured workflow details nicely inside custom HTML cards."""
    intent_info = data.get("intent", {})
    intent_name = intent_info.get("intent", "N/A")
    confidence = intent_info.get("confidence", 0.0)
    intent_reason = intent_info.get("reason", "N/A")
    
    priority = data.get("priority", "N/A").lower()
    routed_to = data.get("routed_to", "N/A")
    validated = data.get("validation_passed", False)
    next_action = data.get("next_action", "N/A")
    
    # Priority Color Mapping & Glow styling
    priority_colors = {
        "critical": {"bg": "rgba(244, 63, 94, 0.15)", "border": "rgba(244, 63, 94, 0.35)", "text": "#f43f5e", "glow": "0 0 15px rgba(244, 63, 94, 0.25)", "label": "🚨 CRITICAL"},
        "high": {"bg": "rgba(249, 115, 22, 0.15)", "border": "rgba(249, 115, 22, 0.35)", "text": "#f97316", "glow": "0 0 15px rgba(249, 115, 22, 0.25)", "label": "🔥 HIGH"},
        "medium": {"bg": "rgba(234, 179, 8, 0.15)", "border": "rgba(234, 179, 8, 0.35)", "text": "#eab308", "glow": "0 0 15px rgba(234, 179, 8, 0.25)", "label": "⚡ MEDIUM"},
        "low": {"bg": "rgba(16, 185, 129, 0.15)", "border": "rgba(16, 185, 129, 0.35)", "text": "#10b981", "glow": "0 0 15px rgba(16, 185, 129, 0.25)", "label": "🟢 LOW"},
    }
    
    p_style = priority_colors.get(
        priority, 
        {"bg": "rgba(148, 163, 184, 0.15)", "border": "rgba(148, 163, 184, 0.35)", "text": "#94a3b8", "glow": "none", "label": f"⚪ {priority.upper()}"}
    )
    
    # Validation status styling
    v_style = (
        {"color": "#10b981", "bg": "rgba(16, 185, 129, 0.12)", "border": "rgba(16, 185, 129, 0.25)", "label": "✅ PASSED", "glow": "0 0 12px rgba(16, 185, 129, 0.2)"}
        if validated else
        {"color": "#f43f5e", "bg": "rgba(244, 63, 94, 0.12)", "border": "rgba(244, 63, 94, 0.25)", "label": "❌ FAILED", "glow": "0 0 12px rgba(244, 63, 94, 0.2)"}
    )

    # 3-Column Premium HTML Grid Rendering (Left-aligned to prevent Markdown indentation bug)
    st.markdown(
        f"""<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 10px; margin-bottom: 20px;">
<div style="background: rgba(30, 41, 59, 0.35); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.06); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
<div style="font-size: 0.75rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">🎯 INTENT RECOGNITION</div>
<div style="font-size: 1.3rem; font-weight: 800; color: #38bdf8; margin: 8px 0; font-family: 'Outfit', sans-serif;">{intent_name}</div>
<div style="font-size: 0.85rem; color: #cbd5e1; display: flex; align-items: center; justify-content: space-between;">
<span>Confidence:</span>
<span style="font-weight: 800; color: #10b981; font-size: 1rem;">{confidence:.0%}</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; margin-top: 8px; overflow: hidden;">
<div style="width: {confidence * 100}%; height: 100%; background: linear-gradient(90deg, #38bdf8, #10b981); border-radius: 3px;"></div>
</div>
</div>
<div style="background: {p_style['bg']}; padding: 18px; border-radius: 12px; border: 1px solid {p_style['border']}; box-shadow: {p_style['glow']};">
<div style="font-size: 0.75rem; color: #cbd5e1; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">⚡ URGENCY & ROUTING</div>
<div style="font-size: 1.3rem; font-weight: 800; color: {p_style['text']}; margin: 8px 0; font-family: 'Outfit', sans-serif;">{p_style['label']}</div>
<div style="font-size: 0.85rem; color: #cbd5e1; display: flex; align-items: center; justify-content: space-between;">
<span>Routed To:</span>
<span style="font-weight: 800; color: #f8fafc; background: rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 6px;">{routed_to}</span>
</div>
</div>
<div style="background: {v_style['bg']}; padding: 18px; border-radius: 12px; border: 1px solid {v_style['border']}; box-shadow: {v_style['glow']};">
<div style="font-size: 0.75rem; color: #cbd5e1; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">🛡️ SAFEGUARD & NEXT ACTION</div>
<div style="font-size: 1.3rem; font-weight: 800; color: {v_style['color']}; margin: 8px 0; font-family: 'Outfit', sans-serif;">{v_style['label']}</div>
<div style="font-size: 0.85rem; color: #cbd5e1; display: flex; align-items: center; justify-content: space-between;">
<span>Next Action:</span>
<span style="font-weight: 800; color: #c084fc;">{next_action}</span>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Intent reason container
    if intent_reason and intent_reason != "N/A":
        st.markdown(
            f"""<div style="background: rgba(30, 41, 59, 0.2); border-left: 4px solid #38bdf8; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 16px; font-size: 0.9rem;">
<span style="font-weight: 700; color: #38bdf8;">🧠 Intent Classification Rationale:</span><br/>
<span style="color: #cbd5e1; font-style: italic;">"{intent_reason}"</span>
</div>""",
            unsafe_allow_html=True
        )

    # Policy info container
    policy = data.get("policy")
    if policy:
        st.markdown(
            f"""<div style="background: rgba(139, 92, 246, 0.05); border: 1px dashed rgba(139, 92, 246, 0.25); padding: 16px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
<div style="display: flex; align-items: center; margin-bottom: 8px;">
<span style="font-size: 1.2rem; margin-right: 8px;">📋</span>
<span style="font-size: 0.95rem; font-weight: 800; color: #c084fc; letter-spacing: 0.02em; font-family: 'Outfit', sans-serif;">BANKING POLICY REFERENCE [{policy.get('policy_id', 'N/A')}]</span>
</div>
<div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 6px;">{policy.get('title', 'N/A')}</div>
<div style="font-size: 0.88rem; color: #94a3b8; line-height: 1.5; background: rgba(0,0,0,0.15); padding: 12px; border-radius: 8px;">{policy.get('content', 'N/A')}</div>
</div>""",
            unsafe_allow_html=True
        )

    # Missing info container
    missing = data.get("missing_info")
    if missing:
        st.markdown(
            f"""<div style="background: rgba(234, 179, 8, 0.08); border-left: 4px solid #eab308; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 16px; font-size: 0.9rem;">
<span style="font-weight: 700; color: #eab308;">⚠️ Prompting Missing Parameters:</span><br/>
<span style="color: #cbd5e1;">The user needs to provide: <strong>{missing}</strong></span>
</div>""",
            unsafe_allow_html=True
        )


# ---- SIDEBAR DESIGN ----
with st.sidebar:
    # App Logo / Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">🏦</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #f8fafc; font-family: 'Outfit', sans-serif; letter-spacing: -0.02em;">BANKING AI AGENT</div>
            <div style="font-size: 0.8rem; color: #64748b;">Enterprise NLP Solutions</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<hr/>", unsafe_allow_html=True)

    # System Status with glowing bullets
    st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 12px;'>📡 SYSTEM HEALTH</h3>", unsafe_allow_html=True)
    health = check_backend_health()
    if health:
        st.markdown(
            """
            <div style="
                display: flex; 
                align-items: center; 
                background: rgba(16, 185, 129, 0.08); 
                padding: 10px 14px; 
                border-radius: 10px; 
                border: 1px solid rgba(16, 185, 129, 0.2);
                margin-bottom: 15px;
            ">
                <div style="
                    width: 10px; 
                    height: 10px; 
                    background-color: #10b981; 
                    border-radius: 50%; 
                    margin-right: 12px;
                    box-shadow: 0 0 8px #10b981;
                    animation: pulse 2s infinite;
                "></div>
                <span style="color: #10b981; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.02em;">API GATEWAY: ONLINE</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                display: flex; 
                align-items: center; 
                background: rgba(239, 68, 68, 0.08); 
                padding: 10px 14px; 
                border-radius: 10px; 
                border: 1px solid rgba(239, 68, 68, 0.2);
                margin-bottom: 15px;
            ">
                <div style="
                    width: 10px; 
                    height: 10px; 
                    background-color: #ef4444; 
                    border-radius: 50%; 
                    margin-right: 12px;
                    box-shadow: 0 0 8px #ef4444;
                "></div>
                <span style="color: #ef4444; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.02em;">API GATEWAY: OFFLINE</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Configuration formatted beautifully
    config = get_backend_config()
    if config:
        st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 12px;'>⚙️ CONFIGURATION</h3>", unsafe_allow_html=True)
        for k, v in config.items():
            label = k.replace("_", " ").upper()
            st.markdown(
                f"""
                <div style="
                    display: flex; 
                    flex-direction: column;
                    background: rgba(255,255,255,0.015); 
                    padding: 8px 12px; 
                    border-radius: 8px; 
                    margin-bottom: 6px;
                    border: 1px solid rgba(255,255,255,0.03);
                ">
                    <span style="color: #64748b; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.03em;">{label}</span>
                    <span style="color: #38bdf8; font-size: 0.82rem; font-weight: 600; margin-top: 2px; word-break: break-all;">{v}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # About Section
    st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 8px;'>ℹ️ PLATFORM DETAILS</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.45; text-align: justify;">
            This system runs on an enterprise microservice architecture:
            <ul style="margin-left: -15px; margin-top: 6px;">
                <li><strong>API Gateway</strong> (FastAPI) orchestrating the workflow pipelines.</li>
                <li><strong>Intent Service</strong> (gRPC) classifying Banking77 intents.</li>
                <li><strong>Ollama</strong> driving the generative responses.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- MAIN CHAT AREA ----
st.markdown("<h1 class='title-gradient'>💬 Banking Customer Service</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-light'>Ask anything about fees, balances, loan requirements, or card freezing.</p>", unsafe_allow_html=True)
st.markdown("<hr/>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(msg["content"])
            if msg.get("details"):
                with st.expander("📊 Workflow Analytics", expanded=False):
                    display_workflow_details(msg["details"])
        else:
            st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Type your banking question here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Process with backend
    with st.chat_message("assistant"):
        with st.spinner("🤖 Orchestrator processing agentic nodes..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/run-agent",
                    json={"message": user_input},
                    timeout=180,
                )

                if response.status_code == 200:
                    data = response.json()
                    draft = data.get("draft_response", "I could not generate a response.")

                    # Show draft response
                    st.markdown(draft)

                    # Show workflow details
                    with st.expander("📊 Workflow Analytics", expanded=True):
                        display_workflow_details(data)

                    with st.expander("🔍 Diagnostics (Raw JSON)", expanded=False):
                        st.json(data)

                    # Save to history
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": draft,
                            "details": data,
                        }
                    )
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"❌ {error_msg}"}
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "🔌 Cannot connect to the backend. Is it running? "
                    f"Check: {API_BASE_URL}/health"
                )
            except requests.exceptions.Timeout:
                st.error(
                    "⏱️ Request timed out. The agent may be processing a complex request."
                )
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
