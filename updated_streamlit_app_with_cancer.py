# streamlit_app_fixed.py - Cloud deployment optimized version
import streamlit as st
import os
import tempfile
import logging
from io import BytesIO
import time

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
        initialize_enhanced_chat_session,
        ENHANCED_CONSULTATION_CSS
    )
except ImportError as e:
    logging.error(f"Failed to import enhanced consultation: {e}")
    def render_enhanced_text_chat_with_consultation(*args, **kwargs):
        st.error("Enhanced consultation not available")
    def reset_enhanced_chat_session(*args, **kwargs):
        pass
    def export_consultation_history(*args, **kwargs):
        return "{}", "consultation.json"
    def initialize_enhanced_chat_session(*args, **kwargs):
        return None
    ENHANCED_CONSULTATION_CSS = ""

# Import new cancer domain modules with error handling
try:
    from updated_cancer_streamlit_integration import render_enhanced_cancer_domain_app
except ImportError as e:
    logging.error(f"Failed to import cancer modules: {e}")
    def render_enhanced_cancer_domain_app():
        st.error("Cancer domain not available")

try:
    from enhanced_cancer_consultation_system import create_enhanced_cancer_consultation_interface
except ImportError as e:
    logging.error(f"Failed to import cancer consultation: {e}")
    def create_enhanced_cancer_consultation_interface(*args, **kwargs):
        st.error("Cancer consultation not available")

# Import prescription analysis module with error handling
try:
    from prescription_analysis import create_prescription_analysis_interface
except ImportError:
    try:
        from prescription_analysis import create_prescription_analysis_interface
    except ImportError as e:
        logging.error(f"Failed to import prescription analysis: {e}")
        def create_prescription_analysis_interface(*args, **kwargs):
            st.error("Prescription analysis not available")

# Configure Streamlit page
st.set_page_config(
    page_title="LABAID GPT | ল্যাবএইড জিপিটি",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS including cancer domain styles and prescription analysis
MAIN_APP_CSS = """
<style>
    /* Main application styling */
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .app-selector {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.3);
    }
    
    .feature-comparison {
        background: white;
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .domain-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        cursor: pointer;
        transition: transform 0.3s ease;
        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
    }
    
    .domain-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
    
    .cancer-domain-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
    }
    
    .cancer-domain-card:hover {
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    .general-domain-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
    }
    
    .general-domain-card:hover {
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
    
    .feature-list {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #007bff;
    }
    
    .comparison-table {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .new-badge {
        background: #ff4757;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .beta-badge {
        background: #ffa726;
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        margin-left: 10px;
    }
    
    /* Chat container styling */
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        margin-left: 20%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        margin-right: 20%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }

    /* Input area styling */
    .input-container {
        background: white;
        border-radius: 25px;
        padding: 10px 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .input-container:focus-within {
        border-color: #667eea;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.2);
    }
    
    /* Chat statistics */
    .chat-stats {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    
    /* Animations */
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Error message styling */
    .error-banner {
        background: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    
    .warning-banner {
        background: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
</style>
"""

# Add the existing enhanced consultation CSS
st.markdown(MAIN_APP_CSS + ENHANCED_CONSULTATION_CSS, unsafe_allow_html=True)

# Initialize session state
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'selector'

if 'language' not in st.session_state:
    st.session_state.language = 'English'

def check_api_key():
    """Check if required API keys are available"""
    groq_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_key:
        if st.session_state.language == "Bengali":
            st.error("""
            ⚠️ **API কী প্রয়োজন**: এই অ্যাপ্লিকেশনটি ব্যবহার করতে GROQ_API_KEY প্রয়োজন।
            
            **সেটআপ নির্দেশনা:**
            1. [Groq Console](https://console.groq.com) এ যান
            2. একটি বিনামূল্যে অ্যাকাউন্ট তৈরি করুন
            3. API কী জেনারেট করুন
            4. Streamlit Cloud এ Environment Variables এ GROQ_API_KEY সেট করুন
            """)
        else:
            st.error("""
            ⚠️ **API Key Required**: This application requires a GROQ_API_KEY to function.
            
            **Setup Instructions:**
            1. Go to [Groq Console](https://console.groq.com)
            2. Create a free account
            3. Generate an API key
            4. Set GROQ_API_KEY in Streamlit Cloud Environment Variables
            """)
        return False
    return True

def render_app_selector():
    """Render the application mode selector"""
    
    # Check API key first
    if not check_api_key():
        st.stop()
    
    # Main header
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5em;">🏥 ল্যাবএইড জিপিটি</h1>
            <p style="margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.9;">
                বিশ্বমানের AI চিকিৎসা সহায়তা - সাধারণ এবং বিশেষায়িত ডোমেইন
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5em;">🏥 LABAID GPT</h1>
            <p style="margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.9;">
                World-class AI medical assistance - General and Specialized Domains
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Language selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        language_options = ["English", "Bengali"]
        selected_language = st.radio(
            "🌐 Language / ভাষা",
            language_options,
            index=0 if st.session_state.language == "English" else 1,
            horizontal=True
        )
        
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()
    
    # Domain selection
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="app-selector">
            <h2 style="margin: 0 0 15px 0;">🎯 আপনার চিকিৎসা ডোমেইন নির্বাচন করুন</h2>
            <p style="margin: 0; opacity: 0.9;">বিশেষায়িত বা সাধারণ চিকিৎসা সহায়তা বেছে নিন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="app-selector">
            <h2 style="margin: 0 0 15px 0;">🎯 Choose Your Medical Domain</h2>
            <p style="margin: 0; opacity: 0.9;">Select specialized or general medical assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Domain cards
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == "Bengali":
            if st.button("🎯 ক্যান্সার AI বিশেষজ্ঞ", key="cancer_domain_btn", type="primary", use_container_width=True):
                st.session_state.app_mode = 'cancer'
                st.rerun()
            
            st.markdown("""
            <div class="domain-card cancer-domain-card">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🎯</div>
                    <h3 style="margin: 0 0 10px 0;">ক্যান্সার AI বিশেষজ্ঞ<span class="new-badge">নতুন</span></h3>
                    <p style="margin: 0; opacity: 0.9;">উন্নত যুক্তি ও বিশ্লেষণ সহ ক্যান্সার-নির্দিষ্ট পরামর্শ</p>
                </div>
                <div class="feature-list" style="margin-top: 20px; background: rgba(255,255,255,0.1);">
                    <h4 style="margin: 0 0 10px 0; color: white;">🌟 বিশেষ বৈশিষ্ট্য:</h4>
                    <ul style="margin: 0; color: white; opacity: 0.9;">
                        <li>স্মার্ট লক্ষণ বিশ্লেষণ</li>
                        <li>ঝুঁকি কারণ মূল্যায়ন</li>
                        <li>AI যুক্তি ব্যাখ্যা</li>
                        <li>জরুরি অবস্থা সনাক্তকরণ</li>
                        <li>ব্যক্তিগত সুপারিশ</li>
                        <li>প্রেসক্রিপশন বিশ্লেষণ</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🎯 Cancer AI Specialist", key="cancer_domain_btn", type="primary", use_container_width=True):
                st.session_state.app_mode = 'cancer'
                st.rerun()
            
            st.markdown("""
            <div class="domain-card cancer-domain-card">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🎯</div>
                    <h3 style="margin: 0 0 10px 0;">Cancer AI Specialist<span class="new-badge">NEW</span></h3>
                    <p style="margin: 0; opacity: 0.9;">Cancer-specific consultation with advanced reasoning & analysis</p>
                </div>
                <div class="feature-list" style="margin-top: 20px; background: rgba(255,255,255,0.1);">
                    <h4 style="margin: 0 0 10px 0; color: white;">🌟 Special Features:</h4>
                    <ul style="margin: 0; color: white; opacity: 0.9;">
                        <li>Smart Symptom Analysis</li>
                        <li>Risk Factor Assessment</li>
                        <li>AI Reasoning Explanation</li>
                        <li>Emergency Detection</li>
                        <li>Personalized Recommendations</li>
                        <li>Prescription Analysis</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.language == "Bengali":
            if st.button("🏥 সাধারণ চিকিৎসা AI", key="general_domain_btn", type="secondary", use_container_width=True):
                st.session_state.app_mode = 'general'
                st.rerun()
            
            st.markdown("""
            <div class="domain-card general-domain-card">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🏥</div>
                    <h3 style="margin: 0 0 10px 0;">সাধারণ চিকিৎসা AI</h3>
                    <p style="margin: 0; opacity: 0.9;">সব ধরনের স্বাস্থ্য সমস্যার জন্য ব্যাপক চিকিৎসা সহায়তা</p>
                </div>
                <div class="feature-list" style="margin-top: 20px; background: rgba(255,255,255,0.1);">
                    <h4 style="margin: 0 0 10px 0; color: white;">🌟 মূল বৈশিষ্ট্য:</h4>
                    <ul style="margin: 0; color: white; opacity: 0.9;">
                        <li>ভয়েস + ভিশন বিশ্লেষণ</li>
                        <li>উন্নত পরামর্শ সিস্টেম</li>
                        <li>ফলো-আপ প্রশ্ন</li>
                        <li>বহুভাষিক সহায়তা</li>
                        <li>রিয়েল-টাইম প্রতিক্রিয়া</li>
                        <li>প্রেসক্রিপশন বিশ্লেষণ</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🏥 General Medical AI", key="general_domain_btn", type="secondary", use_container_width=True):
                st.session_state.app_mode = 'general'
                st.rerun()
            
            st.markdown("""
            <div class="domain-card general-domain-card">
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 15px;">🏥</div>
                    <h3 style="margin: 0 0 10px 0;">General Medical AI</h3>
                    <p style="margin: 0; opacity: 0.9;">Comprehensive medical assistance for all health concerns</p>
                </div>
                <div class="feature-list" style="margin-top: 20px; background: rgba(255,255,255,0.1);">
                    <h4 style="margin: 0 0 10px 0; color: white;">🌟 Core Features:</h4>
                    <ul style="margin: 0; color: white; opacity: 0.9;">
                        <li>Voice + Vision Analysis</li>
                        <li>Enhanced Consultation System</li>
                        <li>Follow-up Questions</li>
                        <li>Multilingual Support</li>
                        <li>Real-time Responses</li>
                        <li>Prescription Analysis</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_main_navigation():
    """Render navigation for the selected app mode"""
    
    # Sidebar navigation
    with st.sidebar:
        if st.session_state.language == "Bengali":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin: 0;">🧭 নেভিগেশন</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="margin: 0;">🧭 Navigation</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Back to selector button
        if st.session_state.language == "Bengali":
            if st.button("🏠 মূল মেনুতে ফিরুন", use_container_width=True):
                st.session_state.app_mode = 'selector'
                st.rerun()
        else:
            if st.button("🏠 Back to Main Menu", use_container_width=True):
                st.session_state.app_mode = 'selector'
                st.rerun()
        
        st.markdown("---")
        
        # Current mode indicator
        if st.session_state.app_mode == 'cancer':
            if st.session_state.language == "Bengali":
                st.success("🎯 বর্তমান: ক্যান্সার AI বিশেষজ্ঞ")
            else:
                st.success("🎯 Current: Cancer AI Specialist")
        
        elif st.session_state.app_mode == 'general':
            if st.session_state.language == "Bengali":
                st.success("🏥 বর্তমান: সাধারণ চিকিৎসা AI")
            else:
                st.success("🏥 Current: General Medical AI")
        
        st.markdown("---")
        
        # Language switcher
        language_options = ["English", "Bengali"]
        selected_language = st.radio(
            "🌐 Language / ভাষা",
            language_options,
            index=0 if st.session_state.language == "English" else 1
        )
        
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()


def render_general_medical_app():
    """Enhanced general medical app with cloud-optimized features"""
    
    lang_code = "bn" if st.session_state.language == "Bengali" else "en"
    
    # Header
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1>🏥 সাধারণ চিকিৎসা AI</h1>
            <p>ব্যাপক স্বাস্থ্য সহায়তা - এখন ক্লাউড-অপ্টিমাইজড</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1>🏥 LABAID GPT</h1>
            <p>Comprehensive health assistance - Now cloud-optimized</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different features
    if st.session_state.language == "Bengali":
        tab1, tab2, tab3 = st.tabs([
            "💬 AI পরামর্শ",
            "🎤 ভয়েস এবং ইমেজ",
            "📋 প্রেসক্রিপশন বিশ্লেষণ"
        ])
    else:
        tab1, tab2, tab3 = st.tabs([
            "💬 AI Consultation", 
            "🎤 Voice & Image",
            "📋 Prescription Analysis"
        ])
    
    with tab1:
        try:
            render_enhanced_text_chat_with_consultation(st.session_state.language, lang_code)
        except Exception as e:
            st.error(f"Consultation feature error: {e}")
            render_basic_chat_interface(lang_code)
    
    with tab2:
        render_voice_image_interface(lang_code)
    
    with tab3:
        create_prescription_analysis_interface(st.session_state.language)


def render_basic_chat_interface(lang_code):
    """Basic chat interface as fallback"""
    
    if lang_code == "bn":
        st.markdown("### 💬 মৌলিক চ্যাট ইন্টারফেস")
        st.info("উন্নত পরামর্শ বৈশিষ্ট্য লোড হচ্ছে না। মৌলিক চ্যাট ব্যবহার করুন।")
        
        user_input = st.text_area("আপনার প্রশ্ন লিখুন:", placeholder="যেমন: আমার মাথা ব্যথা করছে")
        
        if st.button("প্রশ্ন জমা দিন"):
            if user_input:
                st.write("**আপনি:** " + user_input)
                st.write("**ডাক্তার:** দুঃখিত, উন্নত বৈশিষ্ট্যগুলি বর্তমানে উপলব্ধ নেই। অনুগ্রহ করে পেশাদার চিকিৎসা সহায়তা নিন।")
    else:
        st.markdown("### 💬 Basic Chat Interface")
        st.info("Enhanced consultation features are not loading. Using basic chat.")
        
        user_input = st.text_area("Your question:", placeholder="e.g., I have a headache")
        
        if st.button("Submit Question"):
            if user_input:
                st.write("**You:** " + user_input)
                st.write("**Doctor:** Sorry, enhanced features are currently not available. Please seek professional medical assistance.")


def render_voice_image_interface(lang_code):
    """Cloud-optimized voice and image interface"""
    
    if st.session_state.language == "Bengali":
        st.markdown("### 🎤 ভয়েস এবং ইমেজ বিশ্লেষণ")
    else:
        st.markdown("### 🎤 Voice & Image Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == "Bengali":
            st.markdown("#### 🎙️ অডিও আপলোড")
            audio_file = st.file_uploader(
                "অডিও ফাইল আপলোড করুন",
                type=['wav', 'mp3', 'ogg', 'm4a', 'flac'],
                help="আপনার প্রশ্ন রেকর্ড করে আপলোড করুন"
            )
        else:
            st.markdown("#### 🎙️ Audio Upload")
            audio_file = st.file_uploader(
                "Upload audio file",
                type=['wav', 'mp3', 'ogg', 'm4a', 'flac'],
                help="Record and upload your question"
            )
    
    with col2:
        if st.session_state.language == "Bengali":
            st.markdown("#### 📷 ইমেজ আপলোড")
            image_file = st.file_uploader(
                "ছবি আপলোড করুন",
                type=['jpg', 'jpeg', 'png'],
                help="সংশ্লিষ্ট ছবি আপলোড করুন"
            )
        else:
            st.markdown("#### 📷 Image Upload")
            image_file = st.file_uploader(
                "Upload image",
                type=['jpg', 'jpeg', 'png'],
                help="Upload relevant images"
            )
        
        if image_file:
            st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
    # Process button
    if audio_file or image_file:
        if st.session_state.language == "Bengali":
            if st.button("🚀 বিশ্লেষণ শুরু করুন", type="primary", use_container_width=True):
                process_multimodal_input(audio_file, image_file, lang_code)
        else:
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                process_multimodal_input(audio_file, image_file, lang_code)


def process_multimodal_input(audio_file, image_file, lang_code):
    """Process audio and image inputs with cloud-friendly approach"""
    
    transcribed_text = ""
    image_analysis = ""
    
    try:
        # Process audio if provided
        if audio_file:
            with st.status("🎯 Converting speech to text..." if lang_code == "en" else "🎯 কথাকে টেক্সটে রূপান্তর করা হচ্ছে..."):
                transcribed_text = process_uploaded_audio_file(audio_file, lang_code)
        
        # Process image if provided
        if image_file:
            with st.status("📷 Analyzing image..." if lang_code == "en" else "📷 ছবি বিশ্লেষণ করা হচ্ছে..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                        tmp_img.write(image_file.getvalue())
                        image_path = tmp_img.name
                    
                    prompt = get_general_image_prompt(lang_code)
                    image_analysis = analyze_image_with_query(
                        query=prompt,
                        encoded_image=encode_image(image_path),
                        language=lang_code
                    )
                    
                    os.unlink(image_path)
                except Exception as e:
                    image_analysis = f"Image analysis failed: {e}"
        
        # Display results
        display_multimodal_results(transcribed_text, image_analysis, lang_code)
        
    except Exception as e:
        logging.error(f"Multimodal processing failed: {e}")
        error_msg = f"প্রক্রিয়াকরণে ত্রুটি: {str(e)}" if lang_code == "bn" else f"Processing error: {str(e)}"
        st.error(error_msg)


def get_general_image_prompt(lang_code):
    """Get general medical image analysis prompt"""
    if lang_code == "bn":
        return """আপনি একজন অভিজ্ঞ চিকিৎসক। এই ছবিতে কোনো স্বাস্থ্য সংক্রান্ত সমস্যা আছে কিনা বিশ্লেষণ করুন।
        
        বিশেষভাবে লক্ষ্য করুন:
        - ত্বকের কোনো সমস্যা
        - ফোলা বা লালভাব
        - আঘাতের চিহ্ন
        - অস্বাভাবিক দাগ
        
        সতর্কতার সাথে বিশ্লেষণ করুন এবং চিকিৎসা পরামর্শের সুপারিশ করুন।"""
    else:
        return """You are an experienced medical doctor. Analyze this image for any health-related issues.
        
        Pay attention to:
        - Skin problems
        - Swelling or redness
        - Signs of injury
        - Unusual spots
        
        Analyze carefully and recommend medical consultation if needed."""


def display_multimodal_results(transcribed_text, image_analysis, lang_code):
    """Display results from multimodal analysis"""
    
    if transcribed_text:
        if lang_code == "bn":
            st.markdown(f"### 👤 আপনি যা বলেছেন:\n*{transcribed_text}*")
        else:
            st.markdown(f"### 👤 What you said:\n*{transcribed_text}*")
    
    if image_analysis:
        if lang_code == "bn":
            st.markdown(f"### 📷 ছবি বিশ্লেষণ:\n{image_analysis}")
        else:
            st.markdown(f"### 📷 Image Analysis:\n{image_analysis}")
    
    if transcribed_text or image_analysis:
        if lang_code == "bn":
            st.success("✅ বিশ্লেষণ সম্পন্ন! আরও বিস্তারিত পরামর্শের জন্য একজন চিকিৎসকের সাথে যোগাযোগ করুন।")
        else:
            st.success("✅ Analysis complete! Contact a healthcare provider for detailed consultation.")


def render_cancer_domain_app():
    """Render cancer domain app with error handling"""
    try:
        render_enhanced_cancer_domain_app()
    except Exception as e:
        logging.error(f"Cancer domain error: {e}")
        
        if st.session_state.language == "Bengali":
            st.error("ক্যান্সার AI বিশেষজ্ঞ লোড করতে সমস্যা হচ্ছে।")
            st.markdown("""
            ### 🎯 ক্যান্সার AI বিশেষজ্ঞ (সীমিত মোড)
            
            দুঃখিত, সম্পূর্ণ ক্যান্সার বিশেষজ্ঞ বৈশিষ্ট্য বর্তমানে উপলব্ধ নেই।
            
            **বিকল্প বিকল্প:**
            - সাধারণ চিকিৎসা AI ব্যবহার করুন
            - প্রেসক্রিপশন বিশ্লেষণ বৈশিষ্ট্য ব্যবহার করুন
            - পেশাদার অনকোলজিস্টের সাথে পরামর্শ করুন
            """)
        else:
            st.error("Cancer AI Specialist failed to load.")
            st.markdown("""
            ### 🎯 Cancer AI Specialist (Limited Mode)
            
            Sorry, the full cancer specialist features are currently not available.
            
            **Alternative Options:**
            - Use General Medical AI
            - Use Prescription Analysis feature
            - Consult with professional oncologists
            """)
        
        # Fallback: render basic cancer information
        create_basic_cancer_interface()


def create_basic_cancer_interface():
    """Basic cancer information interface as fallback"""
    
    if st.session_state.language == "Bengali":
        st.markdown("""
        ### 📋 মৌলিক ক্যান্সার তথ্য
        
        **গুরুত্বপূর্ণ লক্ষণ:**
        - দীর্ঘস্থায়ী কাশি (৩ সপ্তাহের বেশি)
        - অব্যাখ্যাত ওজন হ্রাস
        - অস্বাভাবিক গাঁট বা পিণ্ড
        - অস্বাভাবিক রক্তপাত
        - ত্বকের পরিবর্তন
        
        **ঝুঁকির কারণ:**
        - ধূমপান
        - পারিবারিক ইতিহাস
        - বয়স (৫০+)
        - অতিরিক্ত রোদে থাকা
        
        ⚠️ **গুরুত্বপূর্ণ:** কোনো উদ্বেগজনক লক্ষণ দেখলে অবিলম্বে একজন অনকোলজিস্টের সাথে পরামর্শ করুন।
        """)
        
        user_input = st.text_area("আপনার লক্ষণ বা প্রশ্ন লিখুন:")
        if st.button("পরামর্শ পান"):
            if user_input:
                st.info("মৌলিক পরামর্শ: অনুগ্রহ করে একজন যোগ্য অনকোলজিস্টের সাথে পরামর্শ করুন।")
    else:
        st.markdown("""
        ### 📋 Basic Cancer Information
        
        **Important Symptoms:**
        - Persistent cough (>3 weeks)
        - Unexplained weight loss
        - Unusual lumps or masses
        - Unusual bleeding
        - Skin changes
        
        **Risk Factors:**
        - Smoking
        - Family history
        - Age (50+)
        - Excessive sun exposure
        
        ⚠️ **Important:** If you have any concerning symptoms, consult an oncologist immediately.
        """)
        
        user_input = st.text_area("Describe your symptoms or questions:")
        if st.button("Get Advice"):
            if user_input:
                st.info("Basic advice: Please consult with a qualified oncologist for proper evaluation.")


def render_footer():
    """Render application footer"""
    
    st.markdown("---")
    
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: #666; background: #f8f9fa; 
                    border-radius: 15px; margin: 20px 0;">
            <h4 style="margin: 0 0 10px 0;">🏥 ল্যাবএইড জিপিটি</h4>
            <p style="margin: 0; font-size: 0.9em;">
                <strong>⚠️ গুরুত্বপূর্ণ দাবিত্যাগ:</strong> এই AI সিস্টেম প্রাথমিক স্বাস্থ্য তথ্য ও গাইডেন্স প্রদান করে। 
                চূড়ান্ত রোগ নির্ণয় এবং চিকিৎসার জন্য সর্বদা যোগ্য চিকিৎসকের পরামর্শ নিন।
            </p>
            <div style="margin-top: 15px;">
                <span style="margin: 0 10px;">☁️ Cloud-Optimized</span>
                <span style="margin: 0 10px;">🌐 Multilingual</span>
                <span style="margin: 0 10px;">🔒 Secure</span>
                <span style="margin: 0 10px;">⚡ Real-time</span>
            </div>
            <p style="margin: 15px 0 0 0; font-size: 0.8em; color: #888;">
                Powered by Groq & Advanced AI • Cloud Version • © 2024
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: #666; background: #f8f9fa; 
                    border-radius: 15px; margin: 20px 0;">
            <h4 style="margin: 0 0 10px 0;">🏥 LABAID GPT</h4>
            <p style="margin: 0; font-size: 0.9em;">
                <strong>⚠️ Important Disclaimer:</strong> This AI system provides preliminary health information and guidance. 
                Always consult qualified healthcare providers for definitive diagnosis and treatment.
            </p>
            <div style="margin-top: 15px;">
                <span style="margin: 0 10px;">☁️ Cloud-Optimized</span>
                <span style="margin: 0 10px;">🌐 Multilingual</span>
                <span style="margin: 0 10px;">🔒 Secure</span>
                <span style="margin: 0 10px;">⚡ Real-time</span>
            </div>
            <p style="margin: 15px 0 0 0; font-size: 0.8em; color: #888;">
                Powered by Groq & Advanced AI • Cloud Version • © 2024
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function with error handling"""
    
    try:
        # Render based on app mode
        if st.session_state.app_mode == 'selector':
            render_app_selector()
        
        elif st.session_state.app_mode == 'cancer':
            render_main_navigation()
            render_cancer_domain_app()
        
        elif st.session_state.app_mode == 'general':
            render_main_navigation()
            render_general_medical_app()
        
        # Footer
        render_footer()
        
    except Exception as e:
        logging.error(f"Main app error: {e}")
        
        if st.session_state.language == "Bengali":
            st.error(f"""
            অ্যাপ্লিকেশনে ত্রুটি ঘটেছে: {str(e)}
            
            **সমাধানের চেষ্টা করুন:**
            1. পেজ রিফ্রেশ করুন
            2. ব্রাউজার ক্যাশ ক্লিয়ার করুন
            3. API কী সঠিকভাবে সেট করা আছে কিনা পরীক্ষা করুন
            """)
        else:
            st.error(f"""
            Application error occurred: {str(e)}
            
            **Try these solutions:**
            1. Refresh the page
            2. Clear browser cache
            3. Check if API keys are properly set
            """)
        
        # Fallback: Show basic interface
        if st.button("🔄 Reset Application" if st.session_state.language == "English" else "🔄 অ্যাপ্লিকেশন রিসেট করুন"):
            st.session_state.app_mode = 'selector'
            st.rerun()


if __name__ == "__main__":
    main()