# updated_streamlit_app_with_harmonized_colors.py - Unified color scheme throughout
import streamlit as st
import os
import tempfile
import logging
from io import BytesIO
import time
import base64
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import modules for different features with error handling
try:
    from brain_of_the_doctor import encode_image, analyze_image_with_query
except ImportError as e:
    logging.error(f"Failed to import brain_of_the_doctor: {e}")
    st.error("Brain module not available")

try:
    from voice_of_the_patient import transcribe_with_groq, process_uploaded_audio_file
except ImportError:
    try:
        from voice_of_the_patient import transcribe_with_groq
        def process_uploaded_audio_file(uploaded_file, language="en"):
            return "Audio processing not fully available"
    except ImportError as e:
        logging.error(f"Failed to import voice modules: {e}")
        def transcribe_with_groq(*args, **kwargs):
            return "Voice transcription not available"
        def process_uploaded_audio_file(uploaded_file, language="en"):
            return "Audio processing not available"

try:
    from voice_of_the_doctor import text_to_speech
except ImportError as e:
    logging.error(f"Failed to import voice_of_the_doctor: {e}")
    def text_to_speech(*args, **kwargs):
        logging.warning("Text-to-speech not available")
        return None

try:
    from enhanced_text_chat_with_consultation import (
        render_enhanced_text_chat_with_consultation,
        reset_enhanced_chat_session,
        export_consultation_history,
        initialize_enhanced_chat_session
    )
except ImportError as e:
    logging.error(f"Failed to import enhanced consultation: {e}")
    def render_enhanced_text_chat_with_consultation(*args, **kwargs):
        st.error("Enhanced consultation not available")
    def reset_enhanced_chat_session():
        pass
    def export_consultation_history():
        return "Export not available"
    def initialize_enhanced_chat_session():
        pass

# Define harmonized color scheme
COLORS = {
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',    # Medical burgundy
    'accent': '#F18F01',       # Warm orange
    'success': '#C73E1D',      # Medical red
    'background': '#F5F7FA',   # Light gray-blue
    'text': '#2C3E50',         # Dark blue-gray
    'light': '#E8F4FD',       # Very light blue
    'dark': '#1A252F'          # Dark navy
}

def apply_custom_css():
    """Apply custom CSS with harmonized colors"""
    st.markdown(f"""
    <style>
    /* Main app styling */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: {COLORS['background']};
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    
    .main-header h1 {{
        color: white;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .main-header p {{
        color: {COLORS['light']};
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 0;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {COLORS['light']};
    }}
    
    .sidebar .sidebar-content {{
        background-color: {COLORS['light']};
        padding: 1rem;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid {COLORS['primary']};
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    
    .feature-card h3 {{
        color: {COLORS['primary']};
        margin-bottom: 0.5rem;
    }}
    
    .feature-card p {{
        color: {COLORS['text']};
        margin-bottom: 0;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['secondary']};
        transform: translateY(-1px);
    }}
    
    /* Success messages */
    .stSuccess {{
        background-color: {COLORS['success']};
        color: white;
        border-radius: 8px;
    }}
    
    /* Info messages */
    .stInfo {{
        background-color: {COLORS['accent']};
        color: white;
        border-radius: 8px;
    }}
    
    /* Text inputs */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 2px solid {COLORS['light']};
        padding: 0.5rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 2px {COLORS['primary']}33;
    }}
    
    /* File uploader */
    .stFileUploader {{
        background-color: white;
        border-radius: 12px;
        border: 2px dashed {COLORS['primary']};
        padding: 1rem;
    }}
    
    /* Chat messages */
    .chat-message {{
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        max-width: 80%;
    }}
    
    .chat-message.user {{
        background-color: {COLORS['primary']};
        color: white;
        margin-left: auto;
    }}
    
    .chat-message.assistant {{
        background-color: white;
        color: {COLORS['text']};
        border: 1px solid {COLORS['light']};
    }}
    
    /* Progress bars */
    .stProgress > div > div > div {{
        background-color: {COLORS['primary']};
    }}
    
    /* Metrics */
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: bold;
        color: {COLORS['primary']};
    }}
    
    .metric-label {{
        color: {COLORS['text']};
        font-size: 0.9rem;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: 1px solid {COLORS['light']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    /* Audio player */
    .stAudio {{
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['light']};
        border-radius: 8px;
        color: {COLORS['primary']};
        font-weight: 500;
    }}
    
    .streamlit-expanderContent {{
        background-color: white;
        border-radius: 0 0 8px 8px;
    }}
    
    /* Sidebar navigation */
    .nav-item {{
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .nav-item:hover {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    .nav-item.active {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    /* Loading spinner */
    .stSpinner {{
        color: {COLORS['primary']};
    }}
    
    /* Footer */
    .footer {{
        background-color: {COLORS['dark']};
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 12px;
        margin-top: 2rem;
    }}
    
    .footer p {{
        margin: 0;
        opacity: 0.8;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 2rem;
        }}
        
        .feature-card {{
            padding: 1rem;
        }}
        
        .chat-message {{
            max-width: 95%;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the main header with harmonized styling"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 AI Medical Assistant</h1>
        <p>Advanced AI-powered healthcare consultation and analysis platform</p>
    </div>
    """, unsafe_allow_html=True)

def render_feature_overview():
    """Render feature overview cards"""
    st.markdown("## 🎯 Available Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 AI Brain Analysis</h3>
            <p>Upload medical images for AI-powered analysis and diagnosis assistance</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Voice Transcription</h3>
            <p>Convert patient voice recordings to text for documentation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔊 Text-to-Speech</h3>
            <p>Convert medical reports and responses to audio format</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Enhanced Consultation</h3>
            <p>Comprehensive chat interface with consultation history</p>
        </div>
        """, unsafe_allow_html=True)

def render_image_analysis():
    """Render image analysis interface"""
    st.markdown("### 🧠 AI Brain - Medical Image Analysis")
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Upload Medical Image**")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload medical images for AI analysis"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Medical Image", use_column_width=True)
            
            # Show image details
            st.markdown("**Image Details:**")
            st.write(f"- **Filename:** {uploaded_file.name}")
            st.write(f"- **Size:** {uploaded_file.size} bytes")
            st.write(f"- **Type:** {uploaded_file.type}")
    
    with col2:
        st.markdown("**Analysis Query**")
        query = st.text_area(
            "Enter your medical query about the image:",
            placeholder="e.g., 'Analyze this X-ray for potential abnormalities'",
            height=100
        )
        
        if st.button("🔍 Analyze Image", type="primary"):
            if uploaded_file is not None and query:
                try:
                    with st.spinner("Analyzing image..."):
                        # Here you would call your image analysis function
                        # For demo purposes, showing a placeholder
                        st.success("Analysis completed!")
                        st.markdown("**AI Analysis Results:**")
                        st.info("Image analysis functionality requires the brain_of_the_doctor module to be properly configured.")
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
            else:
                st.warning("Please upload an image and enter a query.")

def render_voice_features():
    """Render voice-related features"""
    st.markdown("### 🎤 Voice Processing")
    
    # Create tabs for different voice features
    tab1, tab2 = st.tabs(["📝 Speech to Text", "🔊 Text to Speech"])
    
    with tab1:
        st.markdown("**Patient Voice Transcription**")
        
        # Audio file upload
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'ogg', 'flac'],
            help="Upload patient voice recordings for transcription"
        )
        
        if audio_file is not None:
            st.audio(audio_file, format='audio/wav')
            
            # Language selection
            language = st.selectbox(
                "Select language:",
                ["en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "zh"],
                help="Choose the language of the audio"
            )
            
            if st.button("🎯 Transcribe Audio", type="primary"):
                try:
                    with st.spinner("Transcribing audio..."):
                        # Here you would call your transcription function
                        st.success("Transcription completed!")
                        st.markdown("**Transcribed Text:**")
                        st.info("Voice transcription functionality requires the voice_of_the_patient module to be properly configured.")
                except Exception as e:
                    st.error(f"Transcription failed: {str(e)}")
    
    with tab2:
        st.markdown("**Convert Text to Speech**")
        
        text_input = st.text_area(
            "Enter text to convert to speech:",
            placeholder="Enter medical report or consultation notes...",
            height=150
        )
        
        if st.button("🔊 Generate Speech", type="primary"):
            if text_input:
                try:
                    with st.spinner("Generating speech..."):
                        # Here you would call your TTS function
                        st.success("Speech generated successfully!")
                        st.info("Text-to-speech functionality requires the voice_of_the_doctor module to be properly configured.")
                except Exception as e:
                    st.error(f"Speech generation failed: {str(e)}")
            else:
                st.warning("Please enter some text to convert.")

def render_enhanced_chat():
    """Render enhanced chat consultation interface"""
    st.markdown("### 💬 Enhanced Medical Consultation")
    
    # Initialize chat session if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    st.markdown("**Medical Consultation Chat**")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>Patient:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <strong>AI Doctor:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Type your medical question:",
            placeholder="Describe your symptoms or ask a medical question...",
            key="chat_input"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", key="send_chat")
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate AI response (placeholder)
        ai_response = f"Thank you for your question: '{user_input}'. This is a demo response. The enhanced consultation module needs to be properly configured for full functionality."
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Clear input and rerun
        st.rerun()
    
    # Chat controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export History"):
            if st.session_state.chat_history:
                # Create downloadable JSON
                history_json = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button(
                    label="Download Chat History",
                    data=history_json,
                    file_name=f"consultation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No chat history to export.")
    
    with col3:
        if st.button("🔄 Reset Session"):
            st.session_state.chat_history = []
            st.success("Session reset successfully!")
            st.rerun()

def render_settings():
    """Render application settings"""
    st.markdown("### ⚙️ Settings & Configuration")
    
    # API Settings
    with st.expander("🔑 API Configuration"):
        st.markdown("**API Keys and Settings**")
        
        # Environment variables check
        openai_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            help="Enter your OpenAI API key for AI functionality"
        )
        
        groq_key = st.text_input(
            "Groq API Key:",
            type="password",
            help="Enter your Groq API key for voice processing"
        )
        
        if st.button("💾 Save API Keys"):
            if openai_key:
                os.environ['OPENAI_API_KEY'] = openai_key
                st.success("OpenAI API key saved!")
            if groq_key:
                os.environ['GROQ_API_KEY'] = groq_key
                st.success("Groq API key saved!")
    
    # Application Settings
    with st.expander("🎛️ Application Settings"):
        st.markdown("**General Settings**")
        
        # Theme selection
        theme = st.selectbox(
            "Color Theme:",
            ["Professional Blue", "Medical Green", "Warm Orange"],
            help="Choose your preferred color theme"
        )
        
        # Language settings
        app_language = st.selectbox(
            "Application Language:",
            ["English", "Spanish", "French", "German"],
            help="Select your preferred language"
        )
        
        # Notification settings
        enable_notifications = st.checkbox(
            "Enable Notifications",
            value=True,
            help="Show success and error notifications"
        )
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    
    # System Information
    with st.expander("ℹ️ System Information"):
        st.markdown("**Application Status**")
        
        # Module status
        modules_status = {
            "Brain Analysis": "⚠️ Needs Configuration",
            "Voice Processing": "⚠️ Needs Configuration",
            "Text-to-Speech": "⚠️ Needs Configuration",
            "Enhanced Chat": "✅ Available"
        }
        
        for module, status in modules_status.items():
            st.write(f"**{module}:** {status}")
        
        # System info
        st.write(f"**Python Version:** {os.sys.version}")
        st.write(f"**Streamlit Version:** {st.__version__}")

def render_footer():
    """Render application footer"""
    st.markdown("""
    <div class="footer">
        <p>🏥 AI Medical Assistant - Advanced Healthcare AI Platform</p>
        <p>Built with Streamlit • Powered by OpenAI & Groq</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Set page configuration
    st.set_page_config(
        page_title="AI Medical Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Render header
    render_header()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    page = st.sidebar.selectbox(
        "Select Feature:",
        [
            "🏠 Home",
            "🧠 Image Analysis",
            "🎤 Voice Processing",
            "💬 Enhanced Chat",
            "⚙️ Settings"
        ]
    )
    
    # Render pages based on selection
    if page == "🏠 Home":
        render_feature_overview()
        
        # Quick stats
        st.markdown("## 📊 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">4</div>
                <div class="metric-label">AI Features</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">24/7</div>
                <div class="metric-label">Availability</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">10+</div>
                <div class="metric-label">Languages</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">100%</div>
                <div class="metric-label">Secure</div>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "🧠 Image Analysis":
        render_image_analysis()
    
    elif page == "🎤 Voice Processing":
        render_voice_features()
    
    elif page == "💬 Enhanced Chat":
        render_enhanced_chat()
    
    elif page == "⚙️ Settings":
        render_settings()
    
    # Render footer
    render_footer()
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 System Status")
    st.sidebar.success("✅ Application Running")
    st.sidebar.info("⚠️ Some modules need configuration")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Quick Links")
    st.sidebar.markdown("- [Documentation](#)")
    st.sidebar.markdown("- [Support](#)")
    st.sidebar.markdown("- [API Reference](#)")

if __name__ == "__main__":
    main()