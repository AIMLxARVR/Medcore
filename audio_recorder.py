# audio_recorder.py - Cloud-friendly audio recording component for Streamlit
import streamlit as st
import tempfile
import os
import time
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Try to import audio recording libraries with graceful fallbacks
try:
    from streamlit_audio_recorder import st_audiorec
    AUDIO_RECORDER_AVAILABLE = True
    logging.info("streamlit-audio-recorder is available")
except ImportError:
    AUDIO_RECORDER_AVAILABLE = False
    logging.warning("streamlit-audio-recorder not available")

# Remove PyAudio dependency for cloud deployment
PYAUDIO_AVAILABLE = False

def create_audio_recorder(language="en"):
    """
    Create an audio recorder component optimized for cloud deployment
    
    Args:
        language (str): Language code for UI text
        
    Returns:
        bytes or None: Audio data if recorded successfully
    """
    
    # Text for different languages
    if language == "bn":
        record_text = "🎤 রেকর্ড করুন"
        upload_text = "অথবা অডিও ফাইল আপলোড করুন"
        instruction_text = "নিচের বাটনে ক্লিক করে আপনার প্রশ্ন রেকর্ড করুন"
    else:
        record_text = "🎤 Record"
        upload_text = "Or upload an audio file"
        instruction_text = "Click the button below to record your question"
    
    st.write(instruction_text)
    
    # Method 1: Try streamlit-audio-recorder (Cloud-friendly)
    if AUDIO_RECORDER_AVAILABLE:
        try:
            wav_audio_data = st_audiorec()
            
            if wav_audio_data is not None:
                st.success("✅ Audio recorded successfully!")
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(wav_audio_data)
                    tmp_file_path = tmp_file.name
                
                # Let user play back the recording
                st.audio(wav_audio_data, format="audio/wav")
                
                return tmp_file_path
                
        except Exception as e:
            st.error(f"Audio recorder error: {e}")
            logging.error(f"Audio recorder error: {e}")
    
    # Method 2: File upload as primary method for cloud deployment
    else:
        st.info("🎙️ Please use the file upload option below to upload your recorded audio.")
    
    # File upload method
    st.write("---")
    st.write(upload_text)
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'ogg', 'm4a', 'flac'],
        help="Upload your recorded question"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
        return tmp_file_path
    
    return None


def create_simple_audio_input(language="en"):
    """
    Create a simple audio input optimized for cloud deployment
    """
    
    # Text for different languages
    if language == "bn":
        tab1_text = "🎤 রেকর্ড করুন"
        tab2_text = "📁 ফাইল আপলোড"
        record_instruction = "নিচের রেকর্ডার ব্যবহার করুন:"
        upload_instruction = "একটি অডিও ফাইল বেছে নিন:"
    else:
        tab1_text = "🎤 Record Audio"
        tab2_text = "📁 Upload File"
        record_instruction = "Use the recorder below:"
        upload_instruction = "Choose an audio file:"
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs([tab1_text, tab2_text])
    
    with tab1:
        st.write(record_instruction)
        
        # Try to use streamlit-audio-recorder if available
        if AUDIO_RECORDER_AVAILABLE:
            try:
                wav_audio_data = st_audiorec()
                
                if wav_audio_data is not None:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(wav_audio_data)
                        return tmp_file.name
                        
            except Exception as e:
                st.error(f"Recording error: {e}")
                logging.error(f"Recording error: {e}")
        else:
            st.info("🎙️ Audio recording requires additional setup. Please use the file upload tab.")
    
    with tab2:
        st.write(upload_instruction)
        
        uploaded_file = st.file_uploader(
            "Audio file",
            type=['wav', 'mp3', 'ogg', 'm4a', 'flac'],
            key=f"audio_upload_{language}"
        )
        
        if uploaded_file is not None:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                return tmp_file.name
    
    return None


def display_audio_recorder_status():
    """Display the status of audio recording capabilities"""
    
    st.sidebar.markdown("### 🎵 Audio Status")
    
    if AUDIO_RECORDER_AVAILABLE:
        st.sidebar.success("✅ Audio Recording Available")
    else:
        st.sidebar.warning("⚠️ Audio Recording: File Upload Only")
        st.sidebar.info("💡 Record audio on your device and upload the file")