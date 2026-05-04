# audio_recorder.py - Cloud-friendly audio recording component for Streamlit
import streamlit as st
import tempfile
import os
import time
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Audio recorder - removed streamlit-audio-recorder dependency
AUDIO_RECORDER_AVAILABLE = False

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
    
    # Method 1: File upload only (since streamlit-audio-recorder is not available)
    st.info("🎙️ Please record audio on your device and upload the file below.")
    
    # File upload method as primary method
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
        
        # File upload only approach (streamlit-audio-recorder not available)
        st.info("🎙️ Please record audio on your device and upload the file here.")
        
        uploaded_file_tab1 = st.file_uploader(
            "Audio file (from recording tab)",
            type=['wav', 'mp3', 'ogg', 'm4a', 'flac'],
            key=f"audio_record_tab_{language}"
        )
        
        if uploaded_file_tab1 is not None:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file_tab1.getvalue())
                return tmp_file.name
    
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
    
    st.sidebar.warning("⚠️ Audio Recording: File Upload Only")
    st.sidebar.info("💡 Record audio on your device and upload the file")