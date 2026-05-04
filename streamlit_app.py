# updated_streamlit_app.py - Main application with enhanced medical consultation
import streamlit as st
import os
import tempfile
import logging
from io import BytesIO
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import modules for different features
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech
from enhanced_text_chat_with_consultation import (
    render_enhanced_text_chat_with_consultation,
    reset_enhanced_chat_session,
    export_consultation_history,
    initialize_enhanced_chat_session,
    ENHANCED_CONSULTATION_CSS
)

# Configure Streamlit page
st.set_page_config(
    page_title="Labaid GPT / ল্যাবএইড জিপিটি",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI (including consultation styles)
st.markdown("""
<style>
    /* Main chat container styling */
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

    /* Follow-up question styling */
    .follow-up-message {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        color: #2e7d32;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        margin-right: 20%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4caf50;
        animation: slideInLeft 0.3s ease-out;
    }

    /* Emergency alert styling */
    .emergency-alert {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        color: #c62828;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 2px solid #f44336;
        box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3); }
        50% { box-shadow: 0 6px 16px rgba(244, 67, 54, 0.5); }
        100% { box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3); }
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
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }

    /* Consultation progress indicators */
    .consultation-progress {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
        animation: fadeIn 0.5s ease-in;
    }

    /* Quick consultation button styling */
    .quick-consultation-btn {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border: 2px solid #9c27b0;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .quick-consultation-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(156, 39, 176, 0.3);
        background: linear-gradient(135deg, #e1bee7 0%, #ce93d8 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for enhanced features
if 'language' not in st.session_state:
    st.session_state.language = 'English'

if 'enhanced_features_enabled' not in st.session_state:
    st.session_state.enhanced_features_enabled = True

# Helper functions for voice and vision (keeping existing functionality)
def get_unique_filename(prefix="audio", suffix=".mp3"):
    """Generate a unique filename to avoid caching issues"""
    import time
    import random
    timestamp = int(time.time())
    random_num = random.randint(1000, 9999)
    return f"{prefix}_{timestamp}_{random_num}{suffix}"

def process_voice_vision(audio_file, image_file, language="en"):
    """Process voice input and optional image (existing functionality)"""
    if audio_file is None:
        if language == "bn":
            return "কোন অডিও রেকর্ড করা হয়নি", "অনুগ্রহ করে আপনার প্রশ্ন রেকর্ড করুন", None
        else:
            return "No audio recorded", "Please record your question", None
    
    try:
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_file.read())
            audio_filepath = tmp_audio.name
        
        # Transcribe the audio
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3",
            language=language
        )
        
        # Handle the image input if provided
        if image_file is not None:
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(image_file.read())
                image_filepath = tmp_img.name
            
            # For voice+vision, use enhanced consultation
            chat_session = initialize_enhanced_chat_session(language)
            
            # Combine transcribed text with image analysis instruction
            combined_query = f"{speech_to_text_output}\n\nI have also uploaded an image for you to analyze."
            
            doctor_response = analyze_image_with_query(
                query=combined_query, 
                encoded_image=encode_image(image_filepath),
                language=language
            )
            
            # Clean up temp file
            os.unlink(image_filepath)
        else:
            # If no image, process through enhanced consultation
            chat_session = initialize_enhanced_chat_session(language)
            from enhanced_text_chat_with_consultation import process_consultation_message
            doctor_response = process_consultation_message(chat_session, speech_to_text_output)
        
        # Generate voice response
        output_filepath = get_unique_filename("voice_vision_response")
        text_to_speech(input_text=doctor_response, output_filepath=output_filepath, language=language)
        
        # Clean up temp audio file
        os.unlink(audio_filepath)
        
        return speech_to_text_output, doctor_response, output_filepath
    
    except Exception as e:
        logging.error(f"Error in process_voice_vision: {e}")
        if language == "bn":
            return f"অডিও প্রক্রিয়াকরণে ত্রুটি: {str(e)}", "একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।", None
        else:
            return f"Error processing audio: {str(e)}", "An error occurred. Please try again.", None

# Main App
def main():
    # Sidebar for settings and controls
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">⚙️ Enhanced Settings / উন্নত সেটিংস</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selector
        language_options = ["English", "Bengali"]
        selected_language = st.radio(
            "🌐 Language / ভাষা",
            language_options,
            index=0 if st.session_state.language == "English" else 1
        )
        
        # Update session state when language changes
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()
        
        # Convert to language code
        lang_code = "bn" if selected_language == "Bengali" else "en"
        
        st.markdown("---")
        
        # Enhanced features toggle
        st.markdown("### 🚀 Enhanced Features")
        
        enhanced_consultation = st.checkbox(
            "🔍 AI Medical Consultation" if selected_language == "English" else "🔍 AI চিকিৎসা পরামর্শ",
            value=True,
            help="Enable detailed follow-up questions and comprehensive analysis" if selected_language == "English" 
                 else "বিস্তারিত ফলো-আপ প্রশ্ন এবং ব্যাপক বিশ্লেষণ সক্রিয় করুন"
        )
        
        st.session_state.enhanced_features_enabled = enhanced_consultation
        
        st.markdown("---")
        
        # Feature info
        if selected_language == "Bengali":
            feature_info = """
            <div class="feature-card">
                <h4>🚀 নতুন বৈশিষ্ট্য</h4>
                <ul>
                    <li>🔍 উন্নত চিকিৎসা পরামর্শ</li>
                    <li>📋 ফলো-আপ প্রশ্ন সিস্টেম</li>
                    <li>📊 ব্যাপক লক্ষণ বিশ্লেষণ</li>
                    <li>🎯 স্মার্ট রোগ নির্ণয় সহায়তা</li>
                    <li>🚨 জরুরি অবস্থা সনাক্তকরণ</li>
                    <li>📈 পরামর্শ অগ্রগতি ট্র্যাকিং</li>
                </ul>
            </div>
            """
        else:
            feature_info = """
            <div class="feature-card">
                <h4>🚀 New Features</h4>
                <ul>
                    <li>🔍 AI medical consultation</li>
                    <li>📋 Follow-up question system</li>
                    <li>📊 Comprehensive symptom analysis</li>
                    <li>🎯 Smart diagnostic assistance</li>
                    <li>🚨 Emergency situation detection</li>
                    <li>📈 Consultation progress tracking</li>
                </ul>
            </div>
            """
        
        st.markdown(feature_info, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Control buttons
        if selected_language == "Bengali":
            if st.button("🗑️ চ্যাট রিসেট করুন", type="secondary", use_container_width=True):
                reset_enhanced_chat_session(lang_code)
                st.success("চ্যাট রিসেট সম্পন্ন!")
                time.sleep(1)
                st.rerun()
        else:
            if st.button("🗑️ Reset Chat", type="secondary", use_container_width=True):
                reset_enhanced_chat_session(lang_code)
                st.success("Chat reset completed!")
                time.sleep(1)
                st.rerun()
        
        # Export consultation button
        chat_session = initialize_enhanced_chat_session(lang_code)
        if chat_session.history:
            if selected_language == "Bengali":
                if st.button("📥 পরামর্শ ডাউনলোড করুন", use_container_width=True):
                    json_data, filename = export_consultation_history(chat_session, lang_code)
                    st.download_button(
                        label="💾 ডাউনলোড ফাইল",
                        data=json_data,
                        file_name=filename,
                        mime="application/json"
                    )
            else:
                if st.button("📥 Export Consultation", use_container_width=True):
                    json_data, filename = export_consultation_history(chat_session, lang_code)
                    st.download_button(
                        label="💾 Download File",
                        data=json_data,
                        file_name=filename,
                        mime="application/json"
                    )
        
        # Disclaimer
        st.markdown("---")
        if selected_language == "Bengali":
            disclaimer_text = """
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; border-left: 4px solid #ffc107;">
                <small><strong>⚠️ গুরুত্বপূর্ণ দাবিত্যাগ:</strong> 
                <br>• এই উন্নত AI ডাক্তার বিস্তারিত পরামর্শ প্রদান করে
                <br>• জরুরি অবস্থায় তাৎক্ষণিক চিকিৎসা সেবা নিন
                <br>• চূড়ান্ত রোগ নির্ণয়ের জন্য পেশাদার ডাক্তারের পরামর্শ নিন
                <br>• এটি প্রাথমিক স্ক্রিনিং এবং গাইডেন্সের জন্য</small>
            </div>
            """
        else:
            disclaimer_text = """
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; border-left: 4px solid #ffc107;">
                <small><strong>⚠️ Important Disclaimer:</strong> 
                <br>• This enhanced AI Doctor provides detailed consultations
                <br>• Seek immediate medical care for emergencies
                <br>• Consult professional healthcare providers for final diagnosis
                <br>• This is for preliminary screening and guidance</small>
            </div>
            """
        
        st.markdown(disclaimer_text, unsafe_allow_html=True)

    # Main content area
    if selected_language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1>🏥 ল্যাবএইড জিপিটি</h1>
            <p>বিস্তারিত ফলো-আপ প্রশ্ন সহ আমাদের উন্নত এআই ডাক্তারের সাথে পরামর্শ নিন</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show feature highlight
        if st.session_state.enhanced_features_enabled:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                        color: #2e7d32; padding: 15px; border-radius: 10px; margin: 15px 0; 
                        border-left: 4px solid #4caf50;">
                <strong>🔍 উন্নত পরামর্শ সক্রিয়:</strong> আমি আপনার সমস্যা ভালভাবে বুঝতে বিস্তারিত প্রশ্ন করব এবং ব্যাপক বিশ্লেষণ প্রদান করব।
            </div>
            """, unsafe_allow_html=True)
        
        # Create tabs for Bengali
        if st.session_state.enhanced_features_enabled:
            tab1, tab2 = st.tabs(["💬 চিকিৎসা পরামর্শ", "🎤 ভয়েস এবং দৃষ্টি"])
            
            with tab1:
                render_enhanced_text_chat_with_consultation(selected_language, lang_code)
            
            with tab2:
                render_voice_vision_interface(selected_language, lang_code)
        else:
            # Fallback to basic interface
            tab1, tab2 = st.tabs(["💬 টেক্সট চ্যাট", "🎤 ভয়েস এবং দৃষ্টি"])
            
            with tab1:
                st.info("উন্নত বৈশিষ্ট্য সক্রিয় করতে সাইডবার ব্যবহার করুন।")
            
            with tab2:
                render_voice_vision_interface(selected_language, lang_code)
    
    else:  # English interface
        st.markdown("""
        <div class="main-header">
            <h1>🏥 Labaid GPT</h1>
            <p>Get comprehensive medical consultation with detailed follow-up questions from our enhanced AI Doctor</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show feature highlight
        if st.session_state.enhanced_features_enabled:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                        color: #2e7d32; padding: 15px; border-radius: 10px; margin: 15px 0; 
                        border-left: 4px solid #4caf50;">
                <strong>🔍 Enhanced Consultation Active:</strong> I'll ask detailed follow-up questions to better understand your condition and provide comprehensive analysis.
            </div>
            """, unsafe_allow_html=True)
        
        # Create tabs for English
        if st.session_state.enhanced_features_enabled:
            tab1, tab2 = st.tabs(["💬 AI Medical Consultation", "🎤 Voice & Vision"])
            
            with tab1:
                render_enhanced_text_chat_with_consultation(selected_language, lang_code)
            
            with tab2:
                render_voice_vision_interface(selected_language, lang_code)
        else:
            # Fallback to basic interface
            tab1, tab2 = st.tabs(["💬 Text Chat", "🎤 Voice & Vision"])
            
            with tab1:
                st.info("Enable enhanced features using the sidebar.")
            
            with tab2:
                render_voice_vision_interface(selected_language, lang_code)


def render_voice_vision_interface(language, lang_code):
    """Render the voice and vision interface"""
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div class="feature-card">
            <h2>🎤 ভয়েস এবং দৃষ্টি</h2>
            <p>আপনার প্রশ্ন রেকর্ড করুন এবং প্রয়োজনে একটি ছবি যুক্ত করুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-card">
            <h2>🎤 Voice & Vision</h2>
            <p>Record your questions and optionally add an image for analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create two columns for recording and image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎙️ {} </h3>
        </div>
        """.format("অডিও রেকর্ডিং" if language == "Bengali" else "Audio Recording"), 
        unsafe_allow_html=True)
        
        # Audio recorder (you can integrate your existing audio recorder here)
        if language == "Bengali":
            audio_file = st.file_uploader(
                "একটি অডিও ফাইল আপলোড করুন",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key=f"voice_vision_audio_{lang_code}",
                help="আপনার প্রশ্ন রেকর্ড করে আপলোড করুন"
            )
        else:
            audio_file = st.file_uploader(
                "Upload an audio file",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key=f"voice_vision_audio_{lang_code}",
                help="Record and upload your question"
            )
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📷 {} </h3>
        </div>
        """.format("ছবি যুক্ত করুন (ঐচ্ছিক)" if language == "Bengali" else "Add Image (Optional)"), 
        unsafe_allow_html=True)
        
        # Image upload
        if language == "Bengali":
            image_file = st.file_uploader(
                "একটি ছবি আপলোড করুন",
                type=['jpg', 'jpeg', 'png'],
                key=f"voice_vision_image_{lang_code}",
                help="ডাক্তারের সাথে ছবি বিশ্লেষণের জন্য"
            )
        else:
            image_file = st.file_uploader(
                "Upload an image for analysis",
                type=['jpg', 'jpeg', 'png'],
                key=f"voice_vision_image_{lang_code}",
                help="Upload an image for the doctor to analyze"
            )
        
        if image_file:
            st.image(image_file, caption="Uploaded Image" if language == "English" else "আপলোড করা ছবি", 
                    use_column_width=True)
    
    # Submit button and processing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if language == "Bengali":
            submit_button = st.button(
                "🚀 প্রশ্ন জমা দিন", 
                key=f"submit_voice_vision_{lang_code}",
                type="primary", 
                use_container_width=True,
                disabled=not audio_file
            )
        else:
            submit_button = st.button(
                "🚀 Submit Question", 
                key=f"submit_voice_vision_{lang_code}",
                type="primary", 
                use_container_width=True,
                disabled=not audio_file
            )
    
    # Process the submission
    if submit_button and audio_file:
        # Processing indicator
        if language == "Bengali":
            with st.spinner("🎯 আপনার প্রশ্ন প্রক্রিয়া করা হচ্ছে..."):
                transcribed_text, doctor_response, audio_response_path = process_voice_vision(
                    audio_file, image_file, lang_code
                )
        else:
            with st.spinner("🎯 Processing your question..."):
                transcribed_text, doctor_response, audio_response_path = process_voice_vision(
                    audio_file, image_file, lang_code
                )
        
        # Display results
        if transcribed_text and doctor_response:
            # Display what user said
            if language == "Bengali":
                st.markdown("""
                <div class="feature-card">
                    <h4>👤 আপনি যা বলেছেন:</h4>
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; font-style: italic;">
                        "{}"
                    </div>
                </div>
                """.format(transcribed_text), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="feature-card">
                    <h4>👤 What you said:</h4>
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; font-style: italic;">
                        "{}"
                    </div>
                </div>
                """.format(transcribed_text), unsafe_allow_html=True)
            
            # Display doctor's response
            if language == "Bengali":
                st.markdown("""
                <div class="feature-card">
                    <h4>🏥 ডাক্তারের উত্তর:</h4>
                    <div style="background: #f3e5f5; padding: 15px; border-radius: 10px;">
                        {}
                    </div>
                </div>
                """.format(doctor_response.replace('\n', '<br>')), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="feature-card">
                    <h4>🏥 Doctor's Response:</h4>
                    <div style="background: #f3e5f5; padding: 15px; border-radius: 10px;">
                        {}
                    </div>
                </div>
                """.format(doctor_response.replace('\n', '<br>')), unsafe_allow_html=True)
            
            # Audio response
            if audio_response_path and os.path.exists(audio_response_path):
                if language == "Bengali":
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🔊 ডাক্তারের ভয়েস প্রতিক্রিয়া:</h4>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="feature-card">
                        <h4>🔊 Doctor's Voice Response:</h4>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.audio(audio_response_path, format="audio/mp3")


if __name__ == "__main__":
    main()