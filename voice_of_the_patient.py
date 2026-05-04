# voice_of_the_patient_fixed.py - Cloud-friendly speech-to-text with Groq
import os
import logging
import tempfile
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Remove PyAudio dependency - not needed for cloud deployment
def record_audio(duration=10, sample_rate=44100, output_filename="recorded_audio.wav"):
    """
    This function is deprecated for cloud deployment.
    Use file upload instead.
    """
    logging.warning("record_audio() is not available in cloud deployment. Use file upload instead.")
    return None

def transcribe_with_groq(audio_filepath, GROQ_API_KEY=None, stt_model="whisper-large-v3", language="en"):
    """
    Transcribe audio file using Groq's speech-to-text API
    
    Args:
        audio_filepath (str): Path to the audio file
        GROQ_API_KEY (str): Groq API key (optional, will use env var if not provided)
        stt_model (str): Speech-to-text model to use
        language (str): Language code for transcription
        
    Returns:
        str: Transcribed text or error message
    """
    
    # Use provided API key or environment variable
    api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        error_msg = ("API key না পাওয়া গেছে। অনুগ্রহ করে GROQ_API_KEY সেট করুন।" 
                    if language == "bn" else 
                    "API key not found. Please set GROQ_API_KEY.")
        logging.error(error_msg)
        return error_msg
    
    if not os.path.exists(audio_filepath):
        error_msg = ("অডিও ফাইল পাওয়া যায়নি।" 
                    if language == "bn" else 
                    "Audio file not found.")
        logging.error(f"Audio file not found: {audio_filepath}")
        return error_msg
    
    try:
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Open and transcribe the audio file
        with open(audio_filepath, "rb") as file:
            # Create transcription request
            transcription = client.audio.transcriptions.create(
                file=file,
                model=stt_model,
                language=language if language != "bn" else "bn",  # Groq supports Bengali
                response_format="text"
            )
            
            # Extract transcribed text
            transcribed_text = transcription
            
            if isinstance(transcribed_text, str) and transcribed_text.strip():
                logging.info(f"Transcription successful: {len(transcribed_text)} characters")
                return transcribed_text.strip()
            else:
                error_msg = ("ট্রান্সক্রিপশন খালি বা ব্যর্থ হয়েছে।" 
                            if language == "bn" else 
                            "Transcription returned empty or failed.")
                logging.warning(error_msg)
                return error_msg
                
    except Exception as e:
        error_msg = (f"ট্রান্সক্রিপশনে ত্রুটি: {str(e)}" 
                    if language == "bn" else 
                    f"Transcription error: {str(e)}")
        logging.error(f"Groq transcription failed: {e}")
        return error_msg

def process_uploaded_audio_file(uploaded_file, language="en"):
    """
    Process an uploaded audio file and return transcription
    
    Args:
        uploaded_file: Streamlit uploaded file object
        language (str): Language code for transcription
        
    Returns:
        str: Transcribed text or error message
    """
    
    if uploaded_file is None:
        return ("কোন ফাইল আপলোড করা হয়নি।" 
                if language == "bn" else 
                "No file uploaded.")
    
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
        
        # Transcribe the audio
        transcription = transcribe_with_groq(
            audio_filepath=temp_path,
            GROQ_API_KEY=GROQ_API_KEY,
            stt_model="whisper-large-v3",
            language=language
        )
        
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except Exception as cleanup_error:
            logging.warning(f"Failed to cleanup temp file: {cleanup_error}")
        
        return transcription
        
    except Exception as e:
        error_msg = (f"ফাইল প্রক্রিয়াকরণে ত্রুটি: {str(e)}" 
                    if language == "bn" else 
                    f"File processing error: {str(e)}")
        logging.error(f"Audio file processing failed: {e}")
        return error_msg

def get_supported_audio_formats():
    """
    Get list of supported audio formats for cloud deployment
    
    Returns:
        list: Supported audio file extensions
    """
    return ['wav', 'mp3', 'ogg', 'm4a', 'flac', 'webm']

def validate_audio_file(uploaded_file, max_size_mb=25):
    """
    Validate uploaded audio file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_size_mb (int): Maximum file size in MB
        
    Returns:
        tuple: (is_valid, error_message)
    """
    
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    supported_formats = get_supported_audio_formats()
    
    if file_extension not in supported_formats:
        return False, f"Unsupported format. Supported: {', '.join(supported_formats)}"
    
    # Check file size
    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File too large. Maximum size: {max_size_mb}MB"
    
    return True, "Valid audio file"

# Cloud-friendly audio recording instructions
def display_audio_recording_instructions(language="en"):
    """
    Display instructions for audio recording in cloud environment
    """
    import streamlit as st
    
    if language == "bn":
        st.info("""
        📱 **অডিও রেকর্ডিং নির্দেশনা:**
        
        1. আপনার ফোন বা কম্পিউটারে অডিও রেকর্ড করুন
        2. ফাইলটি সেভ করুন (WAV, MP3, M4A ফরম্যাটে)
        3. নিচের আপলোড বাটনে ক্লিক করে ফাইলটি আপলোড করুন
        4. সর্বোচ্চ ফাইল সাইজ: ২৫ MB
        
        📝 **টিপস:**
        - শান্ত পরিবেশে রেকর্ড করুন
        - মাইক্রোফোনের কাছে স্পষ্ট করে কথা বলুন
        - ব্যাকগ্রাউন্ড শব্দ এড়িয়ে চলুন
        """)
    else:
        st.info("""
        📱 **Audio Recording Instructions:**
        
        1. Record audio on your phone or computer
        2. Save the file (in WAV, MP3, M4A format)
        3. Click the upload button below to upload the file
        4. Maximum file size: 25 MB
        
        📝 **Tips:**
        - Record in a quiet environment
        - Speak clearly close to the microphone
        - Avoid background noise
        """)

# Alternative transcription function for different audio formats
def transcribe_audio_with_format_conversion(audio_filepath, target_format="wav", language="en"):
    """
    Transcribe audio with automatic format conversion if needed
    
    Args:
        audio_filepath (str): Path to audio file
        target_format (str): Target format for transcription
        language (str): Language code
        
    Returns:
        str: Transcribed text
    """
    
    # For cloud deployment, we'll rely on Groq's built-in format support
    # Groq Whisper can handle multiple audio formats directly
    return transcribe_with_groq(
        audio_filepath=audio_filepath,
        GROQ_API_KEY=GROQ_API_KEY,
        stt_model="whisper-large-v3",
        language=language
    )