"""
Remote Area Health Info Agent — Streamlit Chat UI
Health guidance, hospital finder, and emergency contacts for remote/hilly regions.
"""
import streamlit as st
import os
from agent.core import HealthAgent

# Page config
st.set_page_config(
    page_title="🏥 Seva Doctor — Health Info Agent",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .emergency-banner {
        background: linear-gradient(90deg, #d32f2f, #f44336);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.1rem;
    }
    .emergency-banner a { color: #fff; font-weight: bold; }
    .main-header {
        background: linear-gradient(90deg, #1565c0, #42a5f5);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .feature-card {
        background: #e3f2fd;
        border-left: 4px solid #1976d2;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .emergency-card {
        background: #ffebee;
        border-left: 4px solid #d32f2f;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "messages" not in st.session_state:
        st.session_state.messages = []


def sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/hospital-3.png", width=64)
        st.title("🏥 Seva Doctor")
        st.caption("Health info for remote regions")

        st.divider()

        # Emergency numbers (always visible)
        st.markdown("""
        <div class="emergency-card">
            <b>🚨 Emergency Numbers</b><br>
            <b>108</b> — Ambulance<br>
            <b>102</b> — Health Helpline<br>
            <b>112</b> — All Emergencies<br>
            <b>100</b> — Police<br>
            <b>1091</b> — Women Helpline
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # API Key input
        st.subheader("🔑 API Key")
        api_key = st.text_input(
            "OpenAI or Groq API Key",
            type="password",
            placeholder="sk-... or gsk_...",
            help="Get free Groq API key at console.groq.com",
        )

        provider = st.selectbox("Provider", ["groq", "openai"])

        if api_key and st.session_state.agent is None:
            st.session_state.agent = HealthAgent(api_key=api_key, provider=provider)
            st.success("✅ Agent ready!")

        st.divider()

        # Quick actions
        st.subheader("⚡ Quick Questions")
        quick_qs = [
            "बुखार आ रहा है, क्या करूं?",
            "Ladakh में nearest hospital कहाँ है?",
            "I have chest pain, what should I do?",
            "My child has dengue symptoms",
            "Sikkim में altitude sickness से कैसे बचें?",
            "Ayushman card kaise banwayen?",
        ]
        for q in quick_qs:
            if st.button(q, use_container_width=True, key=f"q_{q[:20]}"):
                st.session_state.pending_message = q
                st.rerun()

        st.divider()
        st.caption("Built for GSSoC 2026 — Agents for India Track")
        st.caption("By [Nawang Dorjay](https://github.com/nawangdorjay)")


def main():
    init_session_state()
    sidebar()

    # Emergency banner
    st.markdown("""
    <div class="emergency-banner">
        🚨 <b>Emergency?</b> Call <b>108</b> (Ambulance) or <b>102</b> (Health Helpline) immediately!
        &nbsp;&nbsp;|&nbsp;&nbsp; <b>112</b> for all emergencies
    </div>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Seva Doctor</h1>
        <p style="font-size:1.1rem; margin:0;">Health Information Agent for Remote & Hilly Regions of India</p>
        <p style="font-size:0.9rem; margin:0.5rem 0 0 0; opacity:0.9;">
            Health guidance • Hospital finder • Emergency contacts • Altitude health • Govt schemes
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards (when no messages)
    if not st.session_state.messages:
        cols = st.columns(3)
        features = [
            ("💊 Health Guidance", "First-aid advice for fever, diarrhea, burns, injuries. What to do and when to see a doctor."),
            ("🏥 Hospital Finder", "Find nearest hospitals, PHCs, and health centres with phone numbers and services."),
            ("🚨 Emergency Contacts", "State-wise emergency numbers — ambulance, police, women helpline, child helpline."),
            ("🏔️ Altitude Health", "AMS prevention and treatment for Ladakh, Spiti, Sikkim, Uttarakhand."),
            ("🏛️ Health Schemes", "Ayushman Bharat, Jan Aushadhi, JSY — free treatment and cheap medicines."),
            ("🦠 Disease Info", "Dengue, malaria, TB, typhoid — symptoms, prevention, when to seek help."),
        ]
        for i, (title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <b>{title}</b><br>
                    <span style="font-size:0.9rem; color:#555;">{desc}</span>
                </div>
                """, unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Pending message
    prompt = None
    if "pending_message" in st.session_state:
        prompt = st.session_state.pending_message
        del st.session_state.pending_message

    # Chat input
    if not prompt:
        prompt = st.chat_input("अपनी स्वास्थ्य समस्या बताएं... Describe your health concern...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not st.session_state.agent:
            error_msg = "⚠️ Please enter your API key in the sidebar. For emergencies, call 108 now."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.warning(error_msg)
            return

        with st.chat_message("assistant"):
            with st.spinner("🏥 Thinking..."):
                response = st.session_state.agent.process_query(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer
    st.divider()
    st.caption(
        "⚠️ **Disclaimer:** This is an information agent, not a doctor. "
        "For any serious health concern, please visit a qualified medical professional. "
        "In emergencies, call 108 immediately."
    )


if __name__ == "__main__":
    main()
