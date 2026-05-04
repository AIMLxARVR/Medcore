# complete_medical_ai_app_with_cancer_prescription.py - Full integration with ALL modules
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

# Import all modules with comprehensive error handling
try:
    from brain_of_the_doctor import encode_image, analyze_image_with_query
    BRAIN_MODULE_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import brain_of_the_doctor: {e}")
    BRAIN_MODULE_AVAILABLE = False

try:
    from voice_of_the_patient import transcribe_with_groq, process_uploaded_audio_file, validate_audio_file
    VOICE_INPUT_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import voice_of_the_patient: {e}")
    VOICE_INPUT_AVAILABLE = False

try:
    from voice_of_the_doctor import text_to_speech
    VOICE_OUTPUT_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import voice_of_the_doctor: {e}")
    VOICE_OUTPUT_AVAILABLE = False

try:
    from enhanced_text_chat_with_consultation import (
        render_enhanced_text_chat_with_consultation,
        reset_enhanced_chat_session,
        export_consultation_history,
        initialize_enhanced_chat_session
    )
    ENHANCED_CHAT_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import enhanced consultation: {e}")
    ENHANCED_CHAT_AVAILABLE = False

try:
    from medical_imaging_analysis import MedicalImagingAnalysisSystem
    MEDICAL_IMAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import medical imaging analysis: {e}")
    MEDICAL_IMAGING_AVAILABLE = False

try:
    from enhanced_medical_consultation import EnhancedChatSession
    CONSULTATION_SESSION_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import consultation session: {e}")
    CONSULTATION_SESSION_AVAILABLE = False

# ===== NEW: Cancer modules =====
try:
    from cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel
    CANCER_REASONING_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import cancer_reasoning_engine: {e}")
    CANCER_REASONING_AVAILABLE = False

try:
    from enhanced_cancer_consultation_system import (
        create_enhanced_cancer_consultation_interface,
        EnhancedCancerConsultationSession
    )
    CANCER_CONSULTATION_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import enhanced_cancer_consultation_system: {e}")
    CANCER_CONSULTATION_AVAILABLE = False

# ===== NEW: Prescription analysis =====
try:
    from prescription_analysis import PrescriptionAnalyzer, create_prescription_analysis_interface
    PRESCRIPTION_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.error(f"Failed to import prescription_analysis: {e}")
    PRESCRIPTION_ANALYSIS_AVAILABLE = False

# Define harmonized color scheme
COLORS = {
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',    # Medical burgundy
    'accent': '#F18F01',       # Warm orange
    'success': '#C73E1D',      # Medical red
    'background': '#F5F7FA',   # Light gray-blue
    'text': '#2C3E50',         # Dark blue-gray
    'light': '#E8F4FD',       # Very light blue
    'dark': '#1A252F',        # Dark navy
    'cancer': '#FF6B6B',      # Cancer red
    'prescription': '#4CAF50'  # Prescription green
}

def apply_custom_css():
    """Apply comprehensive custom CSS"""
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
    
    /* Cancer-specific styling */
    .cancer-header {{
        background: linear-gradient(135deg, {COLORS['cancer']} 0%, #ee5a24 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        text-align: center;
    }}
    
    .cancer-card {{
        background: white;
        border: 2px solid {COLORS['cancer']};
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
        border-left: 6px solid {COLORS['cancer']};
    }}
    
    .risk-indicator-low {{
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    
    .risk-indicator-moderate {{
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    
    .risk-indicator-high {{
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    
    .risk-indicator-critical {{
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
        100% {{ opacity: 1; }}
    }}
    
    /* Prescription-specific styling */
    .prescription-header {{
        background: linear-gradient(135deg, {COLORS['prescription']} 0%, #45a049 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }}
    
    .prescription-card {{
        background: white;
        border: 2px solid {COLORS['prescription']};
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        border-left: 6px solid {COLORS['prescription']};
    }}
    
    /* Progress indicators */
    .progress-indicator {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
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
    
    /* Status indicators */
    .status-available {{
        color: #4caf50;
        font-weight: bold;
    }}
    
    .status-unavailable {{
        color: #f44336;
        font-weight: bold;
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
    
    /* Analysis results */
    .analysis-result {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['accent']};
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['secondary']};
        transform: translateY(-1px);
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
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🏥 LABAID GPT</h1>
        <p>Complete AI-powered healthcare platform with cancer screening & prescription analysis</p>
    </div>
    """, unsafe_allow_html=True)

def get_system_status():
    """Get comprehensive system status for all modules"""
    return {
        "Brain Analysis": BRAIN_MODULE_AVAILABLE,
        "Voice Input": VOICE_INPUT_AVAILABLE,
        "Voice Output": VOICE_OUTPUT_AVAILABLE,
        "Enhanced Chat": ENHANCED_CHAT_AVAILABLE,
        "Medical Imaging": MEDICAL_IMAGING_AVAILABLE,
        "Consultation Session": CONSULTATION_SESSION_AVAILABLE,
        "Cancer Reasoning": CANCER_REASONING_AVAILABLE,
        "Cancer Consultation": CANCER_CONSULTATION_AVAILABLE,
        "Prescription Analysis": PRESCRIPTION_ANALYSIS_AVAILABLE
    }

def render_system_status():
    """Render comprehensive system status dashboard"""
    st.markdown("## 🔧 System Status")
    
    status = get_system_status()
    
    col1, col2, col3 = st.columns(3)
    
    for i, (module, available) in enumerate(status.items()):
        col_idx = i % 3
        col = [col1, col2, col3][col_idx]
        
        with col:
            if available:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="status-available">✅ {module}</div>
                    <div class="metric-label">Available</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="status-unavailable">❌ {module}</div>
                    <div class="metric-label">Needs Setup</div>
                </div>
                """, unsafe_allow_html=True)

def render_feature_overview():
    """Render comprehensive feature overview cards"""
    st.markdown("## 🎯 Available Features")
    
    col1, col2 = st.columns(2)
    
    with col1:

        # Voice Input
        personalise_care_plan = "✅ Ready" if VOICE_INPUT_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎤 Health Risk Assessment and Personalise Care Plan</h3>
            <p>Convert patient voice recordings to text for documentation</p>
            <small>Status: {personalise_care_plan}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Cancer Consultation
        cancer_status = "✅ Ready" if CANCER_CONSULTATION_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎯 Cancer Consultation</h3>
            <p>Advanced cancer risk assessment with AI reasoning engine</p>
            <small>Status: {cancer_status}</small>
        </div>
        """, unsafe_allow_html=True)


        # Brain Analysis
        brain_status = "✅ Ready" if BRAIN_MODULE_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>🧠 Medical Image Analysis</h3>
            <p>Upload medical images for AI-powered analysis and diagnosis assistance</p>
            <small>Status: {brain_status}</small>
        </div>
        """, unsafe_allow_html=True)
        

    
    with col2:

        # Enhanced Chat
        chat_status = "✅ Ready" if ENHANCED_CHAT_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>💬 AI Doctor Consultation</h3>
            <p>Comprehensive chat interface with consultation history</p>
            <small>Status: {chat_status}</small>
        </div>
        """, unsafe_allow_html=True)

        # # Voice Output
        # voice_output_status = "✅ Ready" if VOICE_OUTPUT_AVAILABLE else "⚠️ Setup Required"
        # st.markdown(f"""
        # <div class="feature-card">
        #     <h3>🔊 Text-to-Speech</h3>
        #     <p>Convert medical reports and responses to audio format</p>
        #     <small>Status: {voice_output_status}</small>
        # </div>
        # """, unsafe_allow_html=True)

        # Voice Input
        voice_input_status = "✅ Ready" if VOICE_INPUT_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎤 Voice Transcription</h3>
            <p>Convert patient voice recordings to text for documentation</p>
            <small>Status: {voice_input_status}</small>
        </div>
        """, unsafe_allow_html=True)
        
        
        # Prescription Analysis
        prescription_status = "✅ Ready" if PRESCRIPTION_ANALYSIS_AVAILABLE else "⚠️ Setup Required"
        st.markdown(f"""
        <div class="feature-card">
            <h3>📋 Prescription Analysis</h3>
            <p>OCR and AI analysis of prescription images with safety checks</p>
            <small>Status: {prescription_status}</small>
        </div>
        """, unsafe_allow_html=True)

def render_image_analysis():
    """Render functional image analysis interface"""
    st.markdown("### 🧠 AI Brain - Medical Image Analysis")
    
    if not BRAIN_MODULE_AVAILABLE:
        st.error("🚫 Brain module not available. Please check brain_of_the_doctor.py")
        return
    
    # Check API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ GROQ_API_KEY not found. Please set your API key.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Upload Medical Image**")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload medical images for AI analysis",
            key="brain_image_upload"
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Medical Image", use_column_width=True)
            
            st.markdown("**Image Details:**")
            st.write(f"- **Filename:** {uploaded_file.name}")
            st.write(f"- **Size:** {uploaded_file.size} bytes")
            st.write(f"- **Type:** {uploaded_file.type}")
    
    with col2:
        st.markdown("**Analysis Settings**")
        
        # Language selection
        language = st.selectbox(
            "Select Language:",
            ["English", "Bengali"],
            help="Choose the language for analysis",
            key="brain_language"
        )
        lang_code = "en" if language == "English" else "bn"
        
        # Analysis type selection
        if MEDICAL_IMAGING_AVAILABLE:
            analysis_type = st.selectbox(
                "Analysis Type:",
                ["General Analysis", "Ophthalmology", "Cardiology", "Orthopedics"],
                help="Choose specialized analysis type",
                key="brain_analysis_type"
            )
        
        query = st.text_area(
            "Analysis Query:",
            placeholder="e.g., 'Analyze this X-ray for potential abnormalities'",
            height=100,
            key="brain_query"
        )
        
        if st.button("🔍 Analyze Image", type="primary", key="brain_analyze"):
            if uploaded_file is not None and query:
                try:
                    with st.spinner("Analyzing image..."):
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_path = tmp_file.name
                        
                        # Encode image
                        encoded_image = encode_image(temp_path)
                        
                        # Perform analysis
                        if MEDICAL_IMAGING_AVAILABLE and analysis_type != "General Analysis":
                            # Use specialized analysis
                            imaging_system = MedicalImagingAnalysisSystem(lang_code)
                            specialist_map = {
                                "Ophthalmology": "ophthalmology",
                                "Cardiology": "cardiology", 
                                "Orthopedics": "orthopedics"
                            }
                            specialist = imaging_system.specialists[specialist_map[analysis_type]]
                            result = specialist.analyze_image(temp_path)
                        else:
                            # Use general analysis
                            result = analyze_image_with_query(
                                query=query,
                                encoded_image=encoded_image,
                                language=lang_code
                            )
                        
                        # Clean up temp file
                        os.unlink(temp_path)
                        
                        # Display results
                        st.success("✅ Analysis completed!")
                        st.markdown("### 📋 AI Analysis Results")
                        st.markdown(f"""
                        <div class="analysis-result">
                            {result}
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    logging.error(f"Image analysis error: {e}")
            else:
                st.warning("⚠️ Please upload an image and enter a query.")

def render_voice_features():
    """Render functional voice processing features"""
    st.markdown("### 🎤 Voice Processing")
    
    # Check API keys
    groq_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_key:
        st.warning("⚠️ GROQ_API_KEY not found. Please set your API key for voice features.")
    
    tab1, tab2 = st.tabs(["📝 Speech to Text", "🔊 Text to Speech"])
    
    with tab1:
        st.markdown("**Patient Voice Transcription**")
        
        if not VOICE_INPUT_AVAILABLE:
            st.error("🚫 Voice input module not available. Check voice_of_the_patient.py")
            return
        
        # Language selection
        language = st.selectbox(
            "Select language:",
            ["English", "Bengali", "Spanish", "French", "German"],
            key="transcription_language"
        )
        
        lang_codes = {
            "English": "en", "Bengali": "bn", "Spanish": "es", 
            "French": "fr", "German": "de"
        }
        lang_code = lang_codes[language]
        
        # Audio file upload
        audio_file = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'ogg', 'flac', 'm4a'],
            help="Upload patient voice recordings for transcription",
            key="voice_audio_upload"
        )
        
        if audio_file is not None:
            # Validate audio file
            is_valid, message = validate_audio_file(audio_file)
            
            if is_valid:
                st.success(f"✅ {message}")
                st.audio(audio_file, format='audio/wav')
                
                if st.button("🎯 Transcribe Audio", type="primary", key="transcribe_btn"):
                    if groq_key:
                        try:
                            with st.spinner("Transcribing audio..."):
                                transcription = process_uploaded_audio_file(audio_file, lang_code)
                            
                            st.success("✅ Transcription completed!")
                            st.markdown("### 📝 Transcribed Text")
                            st.markdown(f"""
                            <div class="analysis-result">
                                {transcription}
                            </div>
                            """, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Transcription failed: {str(e)}")
                    else:
                        st.error("❌ GROQ API key required for transcription")
            else:
                st.error(f"❌ {message}")
    
    with tab2:
        st.markdown("**Convert Text to Speech**")
        
        if not VOICE_OUTPUT_AVAILABLE:
            st.error("🚫 Voice output module not available. Check voice_of_the_doctor.py")
            return
        
        # Language selection for TTS
        tts_language = st.selectbox(
            "Select language:",
            ["English", "Bengali"],
            key="tts_language"
        )
        tts_lang_code = "en" if tts_language == "English" else "bn"
        
        text_input = st.text_area(
            "Enter text to convert to speech:",
            placeholder="Enter medical report or consultation notes...",
            height=150,
            key="tts_text_input"
        )
        
        if st.button("🔊 Generate Speech", type="primary", key="tts_btn"):
            if text_input:
                try:
                    with st.spinner("Generating speech..."):
                        # Generate unique filename
                        audio_filename = f"tts_output_{int(time.time())}.mp3"
                        
                        # Generate speech
                        result_path = text_to_speech(
                            input_text=text_input,
                            output_filepath=audio_filename,
                            language=tts_lang_code
                        )
                        
                        if result_path and os.path.exists(result_path):
                            st.success("✅ Speech generated successfully!")
                            
                            # Play the generated audio
                            with open(result_path, 'rb') as audio_file:
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format='audio/mp3')
                            
                            # Clean up
                            os.unlink(result_path)
                        else:
                            st.error("❌ Failed to generate speech")
                            
                except Exception as e:
                    st.error(f"❌ Speech generation failed: {str(e)}")
            else:
                st.warning("⚠️ Please enter some text to convert.")

def render_enhanced_chat():
    """Render enhanced chat consultation interface"""
    st.markdown("### 💬 Enhanced Medical Consultation")
    
    if not ENHANCED_CHAT_AVAILABLE:
        st.error("🚫 Enhanced chat module not available. Check enhanced_text_chat_with_consultation.py")
        render_basic_chat()
        return
    
    # Language selection
    language = st.selectbox(
        "Select Language:",
        ["English", "Bengali"],
        key="chat_language"
    )
    lang_code = "en" if language == "English" else "bn"
    
    # Use the enhanced chat module
    try:
        render_enhanced_text_chat_with_consultation(language, lang_code)
    except Exception as e:
        st.error(f"❌ Enhanced chat failed: {str(e)}")
        st.info("Falling back to basic chat...")
        render_basic_chat()

def render_cancer_consultation():
    """Render cancer consultation interface"""
    st.markdown("### 🎯 Cancer Risk Assessment & Consultation")
    
    if not CANCER_CONSULTATION_AVAILABLE:
        st.error("🚫 Cancer consultation module not available. Check enhanced_cancer_consultation_system.py")
        render_basic_cancer_info()
        return
    
    # Language selection
    language = st.selectbox(
        "Select Language:",
        ["English", "Bengali"],
        key="cancer_language"
    )
    
    # Use the enhanced cancer consultation module
    try:
        create_enhanced_cancer_consultation_interface(language)
    except Exception as e:
        st.error(f"❌ Cancer consultation failed: {str(e)}")
        logging.error(f"Cancer consultation error: {e}")
        render_basic_cancer_info()

def render_basic_cancer_info():
    """Basic cancer information fallback"""
    st.markdown("""
    <div class="cancer-header">
        <h1>🎯 Cancer Information</h1>
        <p>Basic cancer information and guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ Advanced cancer consultation features are not available.")
    
    st.markdown("""
    **Important Cancer Warning Signs:**
    - Unexplained weight loss
    - Persistent fatigue
    - Changes in bowel or bladder habits
    - Unusual bleeding or discharge
    - Persistent cough or hoarseness
    - Changes in skin moles
    - Difficulty swallowing
    - Persistent pain
    
    **🚨 Please consult with an oncologist or healthcare provider immediately if you experience any of these symptoms.**
    """)

def render_prescription_analysis():
    """Render prescription analysis interface"""
    st.markdown("### 📋 Prescription Analysis")
    
    if not PRESCRIPTION_ANALYSIS_AVAILABLE:
        st.error("🚫 Prescription analysis module not available. Check prescription_analysis.py")
        render_basic_prescription_info()
        return
    
    # Language selection
    language = st.selectbox(
        "Select Language:",
        ["English", "Bengali"],
        key="prescription_language"
    )
    
    # Use the prescription analysis module
    try:
        create_prescription_analysis_interface(language)
    except Exception as e:
        st.error(f"❌ Prescription analysis failed: {str(e)}")
        logging.error(f"Prescription analysis error: {e}")
        render_basic_prescription_info()

def render_basic_prescription_info():
    """Basic prescription information fallback"""
    st.markdown("""
    <div class="prescription-header">
        <h1>📋 Prescription Information</h1>
        <p>Basic prescription guidance and safety tips</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ Advanced prescription analysis features are not available.")
    
    st.markdown("""
    **Prescription Safety Tips:**
    - Always follow dosage instructions exactly
    - Take medications at prescribed times
    - Complete the full course of antibiotics
    - Store medications properly
    - Check expiration dates
    - Report side effects to your doctor
    - Don't share medications with others
    - Keep a list of all medications for emergencies
    
    **🚨 Always consult your pharmacist or doctor if you have questions about your prescription.**
    """)

def render_basic_chat():
    """Basic chat fallback"""
    st.markdown("**Basic Chat Interface**")
    
    # Initialize basic chat history
    if 'basic_chat_history' not in st.session_state:
        st.session_state.basic_chat_history = []
    
    # Display chat history
    for message in st.session_state.basic_chat_history:
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
            placeholder="Describe your symptoms...",
            key="basic_chat_input"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", key="basic_send")
    
    if send_button and user_input:
        # Add user message
        st.session_state.basic_chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Generate basic response
        response = f"Thank you for your question about: '{user_input}'. For a basic response, I recommend consulting with a healthcare professional for proper medical advice."
        
        st.session_state.basic_chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", key="clear_basic_chat"):
        st.session_state.basic_chat_history = []
        st.rerun()

def render_settings():
    """Render comprehensive application settings"""
    st.markdown("### ⚙️ Settings & Configuration")
    
    with st.expander("🔑 API Configuration"):
        st.markdown("**API Keys Setup**")
        
        # Groq API Key
        groq_key = st.text_input(
            "Groq API Key:",
            type="password",
            help="Required for voice transcription, image analysis, and cancer consultation",
            placeholder="gsk_..."
        )
        
        # ElevenLabs API Key (optional)
        elevenlabs_key = st.text_input(
            "ElevenLabs API Key (Optional):",
            type="password",
            help="For enhanced text-to-speech quality",
            placeholder="sk_..."
        )
        
        if st.button("💾 Save API Keys"):
            if groq_key:
                os.environ['GROQ_API_KEY'] = groq_key
                st.success("✅ Groq API key saved!")
            if elevenlabs_key:
                os.environ['ELEVENLABS_API_KEY'] = elevenlabs_key
                st.success("✅ ElevenLabs API key saved!")
    
    with st.expander("🎛️ Application Settings"):
        st.markdown("**General Settings**")
        
        # Default language
        default_language = st.selectbox(
            "Default Language:",
            ["English", "Bengali"],
            help="Set your preferred default language"
        )
        
        # Enable/disable features
        st.markdown("**Feature Settings**")
        enable_voice = st.checkbox("Enable Voice Features", value=True)
        enable_cancer = st.checkbox("Enable Cancer Consultation", value=True)
        enable_prescription = st.checkbox("Enable Prescription Analysis", value=True)
        
        # Safety settings
        st.markdown("**Safety Settings**")
        show_disclaimers = st.checkbox("Show Medical Disclaimers", value=True)
        emergency_detection = st.checkbox("Enable Emergency Detection", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved successfully!")
    
    with st.expander("📊 System Information"):
        st.markdown("**Comprehensive Module Status**")
        render_system_status()
        
        st.markdown("**Environment Information**")
        st.code(f"""
Python Version: {os.sys.version}
Streamlit Version: {st.__version__}
Current Working Directory: {os.getcwd()}

Available Environment Variables:
- GROQ_API_KEY: {'✅ Set' if os.environ.get('GROQ_API_KEY') else '❌ Not Set'}
- ELEVENLABS_API_KEY: {'✅ Set' if os.environ.get('ELEVENLABS_API_KEY') else '❌ Not Set'}

Module Status Summary:
- Core Modules: {sum([BRAIN_MODULE_AVAILABLE, VOICE_INPUT_AVAILABLE, VOICE_OUTPUT_AVAILABLE])}/3
- Enhanced Features: {sum([ENHANCED_CHAT_AVAILABLE, MEDICAL_IMAGING_AVAILABLE, CONSULTATION_SESSION_AVAILABLE])}/3
- Specialized Modules: {sum([CANCER_REASONING_AVAILABLE, CANCER_CONSULTATION_AVAILABLE, PRESCRIPTION_ANALYSIS_AVAILABLE])}/3
        """)
    
    with st.expander("🔧 Troubleshooting"):
        st.markdown("**Common Issues & Solutions**")
        
        st.markdown("""
        **Module Import Errors:**
        - Ensure all Python files are in the same directory
        - Check for typos in module names
        - Verify all dependencies are installed
        
        **API Issues:**
        - Verify GROQ_API_KEY is set correctly
        - Check internet connection
        - Ensure API key has sufficient credits
        
        **Voice Processing Issues:**
        - Check audio file format (WAV, MP3, OGG supported)
        - Ensure file size is under 25MB
        - Verify Groq API key is set
        
        **Cancer/Prescription Analysis Issues:**
        - Check if respective modules are imported correctly
        - Verify Groq API key is configured
        - Ensure image files are clear and readable
        """)
        
        if st.button("🔄 Reload All Modules"):
            st.info("🔄 Reloading application...")
            st.rerun()

def main():
    """Main application function with comprehensive features"""
    # Set page configuration
    st.set_page_config(
        page_title="Labaid GPT - Powered by LABAID AI",
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
    
    # System status in sidebar
    status = get_system_status()
    available_count = sum(status.values())
    total_count = len(status)
    
    st.sidebar.markdown(f"""
    **System Status:** {available_count}/{total_count} modules ready
    """)
    
    # Progress bar for system readiness
    progress = available_count / total_count
    st.sidebar.progress(progress)
    
    # Enhanced navigation with new features
    page = st.sidebar.selectbox(
        "Select Feature:",
        [
            "🏠 Home",
            "🧠 Medical Image Analysis",
            "🎤 Voice Processing", 
            "💬 AI Doctor Consultation",
            "🎯 Cancer Consultation",  # NEW
            "📋 Prescription Analysis",  # NEW
            "⚙️ Settings"
        ]
    )
    
    # Main content area
    if page == "🏠 Home":
        render_feature_overview()
        
        # Enhanced quick stats
        st.markdown("## 📊 System Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{available_count}/{total_count}</div>
                <div class="metric-label">Modules Ready</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            api_status = "✅" if os.environ.get('GROQ_API_KEY') else "❌"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{api_status}</div>
                <div class="metric-label">API Status</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            advanced_features = sum([CANCER_CONSULTATION_AVAILABLE, PRESCRIPTION_ANALYSIS_AVAILABLE])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{advanced_features}/2</div>
                <div class="metric-label">Advanced Features</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🔒</div>
                <div class="metric-label">Secure & Safe</div>
            </div>
            """, unsafe_allow_html=True)
        
        # # Quick access to new features
        # st.markdown("## 🚀 Quick Access")
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     if st.button("🎯 Start Cancer Risk Assessment", type="primary", use_container_width=True):
        #         st.session_state.page_redirect = "🎯 Cancer Consultation"
        #         st.rerun()
        
        # with col2:
        #     if st.button("📋 Analyze Prescription", type="primary", use_container_width=True):
        #         st.session_state.page_redirect = "📋 Prescription Analysis"
        #         st.rerun()
    
    elif page == "🧠 Medical Image Analysis":
        render_image_analysis()
    
    elif page == "🎤 Voice Processing":
        render_voice_features()
    
    elif page == "💬 AI Doctor Consultation":
        render_enhanced_chat()
    
    elif page == "🎯 Cancer Consultation":
        render_cancer_consultation()
    
    elif page == "📋 Prescription Analysis":
        render_prescription_analysis()
    
    elif page == "⚙️ Settings":
        render_settings()
    
    # Handle page redirects
    if hasattr(st.session_state, 'page_redirect'):
        if st.session_state.page_redirect == "🎯 Cancer Consultation":
            render_cancer_consultation()
        elif st.session_state.page_redirect == "📋 Prescription Analysis":
            render_prescription_analysis()
        del st.session_state.page_redirect
    
    # Footer with enhanced information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🏥 <strong>LABAID GPT</strong> - Powered By LABAID AI (A Sister Concern of LABAID GROUP)<br>
        General Medical Consultation| Cancer Screening | Prescription Analysis | Voice Processing<br>
        <small>⚠️ Always consult healthcare professionals for medical advice. This is a preliminary screening tool.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🆕 New Features")
    st.sidebar.markdown("- 🎯 Cancer Risk Assessment")
    st.sidebar.markdown("- 📋 Prescription OCR Analysis")
    st.sidebar.markdown("- 🧠 Advanced AI Reasoning")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Resources")
    st.sidebar.markdown("- [Setup Guide](#)")
    st.sidebar.markdown("- [API Documentation](#)")
    st.sidebar.markdown("- [Medical Disclaimers](#)")
    st.sidebar.markdown("- [Emergency Contacts](#)")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Important")
    st.sidebar.markdown("""
    <small style='color: #666;'>
    This AI assistant provides preliminary information only. 
    Always consult qualified healthcare providers for medical decisions.
    In emergencies, contact your local emergency services immediately.
    </small>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()