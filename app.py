import streamlit as st
import streamlit.components.v1 as components
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Alan-Nexus | Developer Control Plane",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #090d16;
        color: #f3f4f6;
    }
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .log-box {
        background-color: #030712;
        border: 1px solid #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        height: 350px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

if "logs" not in st.session_state:
    st.session_state.logs = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

BACKEND_URL = "http://localhost:8000/api/nexus/voice"

def log_event(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"time": timestamp, "msg": message, "level": level})

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("Alan-Nexus")
    st.caption("Open-Source Multi-Agent Middleware")
    
    st.divider()
    st.subheader("⚙️ Session Controls")
    session_id = st.text_input("Active Thread ID", value="session_demo_101")
    model_name = st.selectbox("LLM Inference Engine", ["openai/gpt-oss-20b"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2)
    
    st.divider()
    if st.button("Clear Session Memory", use_container_width=True):
        st.session_state.logs = []
        st.session_state.chat_history = []
        st.session_state.show_settings = False
        log_event("Session checkpointer memory reset.", "WARN")
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size: 11px; color: #6b7280;'>OpenFire Hackathon 2026 • Alan-Nexus Engine v2.0</p>", unsafe_allow_html=True)

st.title("⚡ Alan-Nexus Developer Control Plane")
st.markdown("Replacing rigid cloud-bound JavaScript intents with stateful **LangGraph + Groq** Python workflows.")


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><p style="font-size: 11px; color: #9ca3af; text-transform: uppercase; font-weight: 600;">FastAPI Bridge</p><p style="font-size: 16px; color: #4ade80; font-weight: 500; margin-top: 4px;">🟢 Online (localhost:8000)</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p style="font-size: 11px; color: #9ca3af; text-transform: uppercase; font-weight: 600;">Active Model</p><p style="font-size: 16px; color: #c084fc; font-weight: 500; margin-top: 4px;">{model_name}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><p style="font-size: 11px; color: #9ca3af; text-transform: uppercase; font-weight: 600;">Agent Architecture</p><p style="font-size: 16px; color: #60a5fa; font-weight: 500; margin-top: 4px;">LangGraph Stateful</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><p style="font-size: 11px; color: #9ca3af; text-transform: uppercase; font-weight: 600;">Thread ID</p><p style="font-size: 16px; color: #fbbf24; font-weight: 500; margin-top: 4px;">{session_id}</p></div>', unsafe_allow_html=True)

st.write("")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("🎤 Voice & Audio Console")
    
    mic_component_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: #111827; color: #f3f4f6; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px; border: 1px solid #1f2937; border-radius: 8px; }
            #micBtn { background-color: #4f46e5; color: white; border: none; width: 65px; height: 65px; border-radius: 50%; font-size: 24px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s; display: flex; align-items: center; justify-content: center; }
            #micBtn:hover { background-color: #4338ca; }
            #micStatus { color: #9ca3af; font-size: 13px; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <button id="micBtn" onclick="toggleListening()">🎙️</button>
        <p id="micStatus">Click microphone to speak</p>

        <script>
            let recognition = null;
            let isListening = false;
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (SpeechRecognition) {
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    isListening = true;
                    document.getElementById('micBtn').style.backgroundColor = '#dc2626';
                    document.getElementById('micStatus').innerText = "Listening... Speak now";
                };

                recognition.onresult = async function(event) {
                    const transcript = event.results[0][0].transcript;
                    document.getElementById('micStatus').innerText = "Processing: " + transcript;
                    
                    try {
                        const res = await fetch("http://localhost:8000/api/nexus/voice", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                user_input: transcript,
                                session_id: "session_demo_101",
                                context: { source: "streamlit_mic_widget" }
                            })
                        });
                        
                        if (res.ok) {
                            const data = await res.json();
                            document.getElementById('micStatus').innerText = "Done! Response spoken.";
                            
                            if ('speechSynthesis' in window) {
                                window.speechSynthesis.cancel();
                                const utterance = new SpeechSynthesisUtterance(data.spoken_text);
                                window.speechSynthesis.speak(utterance);
                            }
                        } else {
                            document.getElementById('micStatus').innerText = "Backend error.";
                        }
                    } catch(e) {
                        document.getElementById('micStatus').innerText = "Connection failed.";
                    }
                    
                    setTimeout(() => { resetMic(); }, 2500);
                };

                recognition.onerror = function(event) {
                    document.getElementById('micStatus').innerText = "Error: " + event.error;
                    resetMic();
                };

                recognition.onend = function() {
                    if (isListening) resetMic();
                };
            } else {
                document.getElementById('micStatus').innerText = "Speech Recognition requires Google Chrome.";
            }

            function toggleListening() {
                if (!recognition) return;
                if (isListening) {
                    recognition.stop();
                    resetMic();
                } else {
                    try { recognition.start(); } catch(e) { recognition.stop(); resetMic(); }
                }
            }

            function resetMic() {
                isListening = false;
                document.getElementById('micBtn').style.backgroundColor = '#4f46e5';
                document.getElementById('micStatus').innerText = "Click microphone to speak";
            }
        </script>
    </body>
    </html>
    """
    
    components.html(mic_component_code, height=140)
    
    st.write("")
    st.subheader("⌨️ Command Input Box")
    
    user_input = st.text_input("Enter or speak command:", value="", placeholder="e.g., Open settings for me.")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        send_clicked = st.button("🚀 Execute Pipeline", type="primary", use_container_width=True)
    with col_b2:
        clear_clicked = st.button("Clear Log", use_container_width=True)
        if clear_clicked:
            st.session_state.logs = []
            st.session_state.show_settings = False
            st.rerun()

    if send_clicked and user_input:
        log_event(f"Incoming command for session '{session_id}': '{user_input}'", "INFO")
        try:
            payload = {
                "user_input": user_input,
                "session_id": session_id,
                "context": {"source": "streamlit_control_plane", "temperature": temperature}
            }
            res = requests.post(BACKEND_URL, json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()
                spoken_text = data.get('spoken_text', 'Done.')
                intent = data.get('intent', 'GENERAL_QA')
                json_payload = data.get('json_payload', {})
                
                log_event(f"Intent classified: [{intent}]", "SUCCESS")
                log_event(f"Spoken response synthesized: '{spoken_text}'", "SUCCESS")
                if json_payload:
                    log_event(f"Action Payload: {json.dumps(json_payload)}", "PAYLOAD")
                
                st.session_state.chat_history.append({
                    "user": user_input,
                    "response": spoken_text,
                    "intent": intent,
                    "payload": json_payload
                })
                
                if "setting" in user_input.lower() or "NAVIGATE" in str(json_payload) or "DYNAMIC_ACTION" in intent:
                    st.session_state.show_settings = True
                
                speech_script = f"""
                <script>
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance("{spoken_text}");
                        window.speechSynthesis.speak(utterance);
                    }}
                </script>
                """
                components.html(speech_script, height=0)
                st.rerun()
            else:
                log_event(f"Server error status {res.status_code}", "ERROR")
        except Exception as e:
                log_event(f"Connection error: {str(e)}", "ERROR")

    st.subheader("💬 Active Conversation Memory")
    chat_container = st.container(height=230)
    with chat_container:
        if not st.session_state.chat_history:
            st.info("No active conversation turns recorded in this thread yet.")
        else:
            for chat in reversed(st.session_state.chat_history):
                st.markdown(f"**User:** {chat['user']}")
                st.markdown(f"**Nexus Agent [{chat['intent']}]:** {chat['response']}")
                if chat['payload']:
                    st.json(chat['payload'])
                st.divider()

with right_col:
    st.subheader("📊 Real-Time Event Stream & JSON Log")
    
    log_html = "<div class='log-box'>"
    if not st.session_state.logs:
        log_html += "<span style='color: #6b7280;'>[System] Waiting for backend events... Click microphone or send text.</span>"
    else:
        for log in st.session_state.logs:
            color = "#4ade80"
            if log["level"] == "ERROR": color = "#f87171"
            elif log["level"] == "WARN": color = "#fbbf24"
            elif log["level"] == "PAYLOAD": color = "#c084fc"
            
            log_html += f"<div style='margin-bottom: 6px;'><span style='color: #6b7280;'>[{log['time']}]</span> <span style='color: {color}; font-weight: bold;'>[{log['level']}]</span> {log['msg']}</div>"
    log_html += "</div>"
    
    st.markdown(log_html, unsafe_allow_html=True)

# Render Settings Panel if triggered via voice/text command
if st.session_state.show_settings:
    with st.expander("⚙️ Alan-Nexus Active System Settings (Triggered via Voice Action)", expanded=True):
        st.success("Settings panel successfully opened via multi-agent action payload!")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.text_input("System Endpoint", value="http://localhost:8000")
            st.slider("Max Token Limit", 256, 2048, 1024)
        with col_s2:
            st.selectbox("Security Level", ["High (PII Redacted)", "Standard"])
            if st.button("Close Settings Panel"):
                st.session_state.show_settings = False
                st.rerun()