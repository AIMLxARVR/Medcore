# audio_recorder.py - Real-time audio recording component for Streamlit
import streamlit as st
import tempfile
import os
import time
from io import BytesIO
import numpy as np

# Try to import audio recording libraries
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False
    st.warning("streamlit-webrtc not installed. Install with: pip install streamlit-webrtc")

try:
    from streamlit_audio_recorder import st_audiorec
    AUDIO_RECORDER_AVAILABLE = True
except ImportError:
    AUDIO_RECORDER_AVAILABLE = False

try:
    import pyaudio
    import wave
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

def create_audio_recorder(language="en"):
    """
    Create an audio recorder component based on available libraries
    
    Args:
        language (str): Language code for UI text
        
    Returns:
        bytes or None: Audio data if recorded successfully
    """
    
    # Text for different languages
    if language == "bn":
        record_text = "🎤 রেকর্ড করুন"
        stop_text = "⏹️ থামান"
        recording_text = "🔴 রেকর্ডিং চলছে..."
        upload_text = "অথবা অডিও ফাইল আপলোড করুন"
        no_audio_text = "কোন অডিও রেকর্ড করা হয়নি"
        instruction_text = "নিচের বাটনে ক্লিক করে আপনার প্রশ্ন রেকর্ড করুন"
    else:
        record_text = "🎤 Record"
        stop_text = "⏹️ Stop"
        recording_text = "🔴 Recording..."
        upload_text = "Or upload an audio file"
        no_audio_text = "No audio recorded"
        instruction_text = "Click the button below to record your question"
    
    st.write(instruction_text)
    
    # Method 1: Try streamlit-audio-recorder (Recommended)
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
    
    # Method 2: Browser-based recording with JavaScript (Fallback)
    else:
        st.info("🎙️ Real-time recording not available. Please use file upload below.")
    
    # Method 3: File upload as fallback
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


def create_browser_audio_recorder(language="en"):
    """
    Create a browser-based audio recorder using HTML5 and JavaScript
    """
    
    # Text for different languages
    if language == "bn":
        record_text = "🎤 রেকর্ড শুরু করুন"
        stop_text = "⏹️ রেকর্ড থামান"
        download_text = "📥 ডাউনলোড করুন"
        recording_text = "🔴 রেকর্ডিং..."
        status_recording = "রেকর্ডিং চলছে..."
        status_completed = "রেকর্ডিং সম্পন্ন!"
        error_prefix = "ত্রুটি: "
    else:
        record_text = "🎤 Start Recording"
        stop_text = "⏹️ Stop Recording"
        download_text = "📥 Download Recording"
        recording_text = "🔴 Recording..."
        status_recording = "Recording in progress..."
        status_completed = "Recording completed!"
        error_prefix = "Error: "
    
    # HTML and JavaScript for browser-based recording
    html_code = f"""
    <div id="audio-recorder">
        <button id="recordButton" onclick="toggleRecording()">{record_text}</button>
        <button id="stopButton" onclick="stopRecording()" disabled>{stop_text}</button>
        <button id="downloadButton" onclick="downloadRecording()" disabled>{download_text}</button>
        
        <div id="status"></div>
        <audio id="audioPlayback" controls style="display:none; margin-top: 10px;"></audio>
    </div>
    
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    
    async function toggleRecording() {{
        if (!isRecording) {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.ondataavailable = function(event) {{
                    audioChunks.push(event.data);
                }};
                
                mediaRecorder.onstop = function() {{
                    const audioBlob = new Blob(audioChunks, {{ type: 'audio/wav' }});
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    document.getElementById('audioPlayback').src = audioUrl;
                    document.getElementById('audioPlayback').style.display = 'block';
                    document.getElementById('downloadButton').disabled = false;
                    
                    // Create download link
                    const downloadLink = document.createElement('a');
                    downloadLink.href = audioUrl;
                    downloadLink.download = 'recorded_audio.wav';
                    downloadLink.id = 'hiddenDownloadLink';
                    document.body.appendChild(downloadLink);
                }};
                
                mediaRecorder.start();
                isRecording = true;
                
                document.getElementById('recordButton').textContent = '{recording_text}';
                document.getElementById('recordButton').disabled = true;
                document.getElementById('stopButton').disabled = false;
                document.getElementById('status').textContent = '{status_recording}';
                
            }} catch (error) {{
                document.getElementById('status').textContent = '{error_prefix}' + error.message;
            }}
        }}
    }}
    
    function stopRecording() {{
        if (mediaRecorder && isRecording) {{
            mediaRecorder.stop();
            isRecording = false;
            
            // Stop all tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            
            document.getElementById('recordButton').textContent = '{record_text}';
            document.getElementById('recordButton').disabled = false;
            document.getElementById('stopButton').disabled = true;
            document.getElementById('status').textContent = '{status_completed}';
            
            audioChunks = [];
        }}
    }}
    
    function downloadRecording() {{
        const downloadLink = document.getElementById('hiddenDownloadLink');
        if (downloadLink) {{
            downloadLink.click();
        }}
    }}
    </script>
    
    <style>
    #audio-recorder {{
        padding: 20px;
        border: 2px dashed #ccc;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }}
    
    #audio-recorder button {{
        margin: 5px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }}
    
    #recordButton {{
        background-color: #ff4444;
        color: white;
    }}
    
    #stopButton {{
        background-color: #666;
        color: white;
    }}
    
    #downloadButton {{
        background-color: #4CAF50;
        color: white;
    }}
    
    #status {{
        margin-top: 10px;
        font-weight: bold;
    }}
    </style>
    """
    
    # Display the HTML component
    st.components.v1.html(html_code, height=250)
    
    # Note for users
    if language == "bn":
        st.info("📝 **নোট**: রেকর্ডিং সম্পন্ন হলে 'ডাউনলোড করুন' বাটনে ক্লিক করে ফাইল ডাউনলোড করুন, তারপর নিচে আপলোড করুন।")
    else:
        st.info("📝 **Note**: After recording, click 'Download Recording' to save the file, then upload it below.")


def create_simple_audio_input(language="en"):
    """
    Create a simple audio input with both recording and upload options
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
                
        # Fallback to browser-based recorder
        else:
            create_browser_audio_recorder(language)
    
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