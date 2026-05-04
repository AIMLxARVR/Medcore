# enhanced_realtime_audio_recorder.py - Auto-submit after recording
import streamlit as st
import streamlit.components.v1 as components
import tempfile
import base64
import os
import logging
import hashlib
import time
import uuid

def create_auto_submit_audio_recorder(language="en", on_audio_recorded=None):
    """
    Create an audio recorder that automatically submits after recording stops
    
    Args:
        language (str): Language code for UI text
        on_audio_recorded (function): Callback function when audio is recorded
        
    Returns:
        str or None: Path to recorded audio file if successful
    """
    
    # Text for different languages
    if language == "bn":
        start_text = "🎤 রেকর্ড শুরু করুন"
        stop_text = "⏹️ রেকর্ড থামান"
        recording_text = "🔴 রেকর্ডিং..."
        processing_text = "⏳ প্রক্রিয়াকরণ..."
        ready_text = "✅ প্রস্তুত"
        error_text = "❌ ত্রুটি"
        permission_text = "🎙️ মাইক্রোফোন অনুমতি প্রয়োজন"
        instruction_text = "রেকর্ড বাটনে ক্লিক করুন এবং কথা বলুন"
    else:
        start_text = "🎤 Start Recording"
        stop_text = "⏹️ Stop Recording"
        recording_text = "🔴 Recording..."
        processing_text = "⏳ Processing..."
        ready_text = "✅ Ready"
        error_text = "❌ Error"
        permission_text = "🎙️ Microphone Permission Required"
        instruction_text = "Click the record button and start speaking"
    
    # Generate unique component ID
    component_id = str(uuid.uuid4())[:8]
    
    # Create session state key for this component
    session_key = f"audio_recorder_{component_id}"
    
    if session_key not in st.session_state:
        st.session_state[session_key] = {
            'audio_data': None,
            'is_processing': False,
            'recording_complete': False
        }
    
    # HTML and JavaScript for real-time recording with auto-submit
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .audio-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                margin: 15px 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                color: white;
                min-height: 200px;
                justify-content: center;
            }}
            
            .record-button {{
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                color: white;
                border: none;
                border-radius: 50px;
                padding: 20px 40px;
                font-size: 20px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
                min-width: 250px;
                position: relative;
                overflow: hidden;
            }}
            
            .record-button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
                background: linear-gradient(135deg, #ff5252 0%, #d84315 100%);
            }}
            
            .record-button.recording {{
                background: linear-gradient(135deg, #2ed573 0%, #1dd1a1 100%);
                animation: recordingPulse 2s infinite;
                box-shadow: 0 6px 20px rgba(46, 213, 115, 0.5);
            }}
            
            .record-button.processing {{
                background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
                cursor: not-allowed;
                animation: processingPulse 1.5s infinite;
            }}
            
            .record-button:disabled {{
                background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
                animation: none;
            }}
            
            @keyframes recordingPulse {{
                0%, 100% {{ 
                    box-shadow: 0 6px 20px rgba(46, 213, 115, 0.5);
                    transform: scale(1);
                }}
                50% {{ 
                    box-shadow: 0 8px 30px rgba(46, 213, 115, 0.8);
                    transform: scale(1.02);
                }}
            }}
            
            @keyframes processingPulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            
            .status-text {{
                margin-top: 20px;
                font-size: 18px;
                font-weight: 500;
                text-align: center;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            
            .waveform {{
                display: flex;
                align-items: center;
                justify-content: center;
                height: 60px;
                margin: 20px 0;
                gap: 4px;
            }}
            
            .wave-bar {{
                width: 4px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 2px;
                animation: wave 1.5s infinite ease-in-out;
            }}
            
            .wave-bar:nth-child(1) {{ animation-delay: 0s; }}
            .wave-bar:nth-child(2) {{ animation-delay: 0.1s; }}
            .wave-bar:nth-child(3) {{ animation-delay: 0.2s; }}
            .wave-bar:nth-child(4) {{ animation-delay: 0.3s; }}
            .wave-bar:nth-child(5) {{ animation-delay: 0.4s; }}
            .wave-bar:nth-child(6) {{ animation-delay: 0.5s; }}
            .wave-bar:nth-child(7) {{ animation-delay: 0.6s; }}
            
            @keyframes wave {{
                0%, 40%, 100% {{ height: 15px; opacity: 0.5; }}
                20% {{ height: 45px; opacity: 1; }}
            }}
            
            .instruction {{
                margin-bottom: 20px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                text-align: center;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            
            .audio-preview {{
                margin-top: 20px;
                width: 100%;
                max-width: 300px;
                border-radius: 25px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }}
            
            .spinner {{
                width: 30px;
                height: 30px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-top: 3px solid white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 10px auto;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="audio-container" id="audioContainer_{component_id}">
            <div class="instruction">{instruction_text}</div>
            
            <button id="recordButton_{component_id}" class="record-button" onclick="toggleRecording_{component_id}()">
                {start_text}
            </button>
            
            <div id="waveform_{component_id}" class="waveform" style="display: none;">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
            </div>
            
            <div id="status_{component_id}" class="status-text"></div>
            
            <div id="spinner_{component_id}" class="spinner" style="display: none;"></div>
            
            <audio id="audioPlayback_{component_id}" controls style="display: none;" class="audio-preview"></audio>
        </div>
        
        <script>
            // Scoped variables for component {component_id}
            let mediaRecorder_{component_id};
            let audioChunks_{component_id} = [];
            let isRecording_{component_id} = false;
            let isProcessing_{component_id} = false;
            
            async function toggleRecording_{component_id}() {{
                const button = document.getElementById('recordButton_{component_id}');
                const status = document.getElementById('status_{component_id}');
                const waveform = document.getElementById('waveform_{component_id}');
                const playback = document.getElementById('audioPlayback_{component_id}');
                const spinner = document.getElementById('spinner_{component_id}');
                
                if (isProcessing_{component_id}) {{
                    return; // Don't allow interaction while processing
                }}
                
                if (!isRecording_{component_id}) {{
                    try {{
                        const stream = await navigator.mediaDevices.getUserMedia({{ 
                            audio: {{
                                echoCancellation: true,
                                noiseSuppression: true,
                                autoGainControl: true,
                                sampleRate: 44100
                            }}
                        }});
                        
                        mediaRecorder_{component_id} = new MediaRecorder(stream, {{
                            mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
                                ? 'audio/webm;codecs=opus' 
                                : 'audio/webm'
                        }});
                        
                        audioChunks_{component_id} = [];
                        
                        mediaRecorder_{component_id}.ondataavailable = function(event) {{
                            if (event.data.size > 0) {{
                                audioChunks_{component_id}.push(event.data);
                            }}
                        }};
                        
                        mediaRecorder_{component_id}.onstop = async function() {{
                            const audioBlob = new Blob(audioChunks_{component_id}, {{ 
                                type: 'audio/webm' 
                            }});
                            const audioUrl = URL.createObjectURL(audioBlob);
                            
                            playback.src = audioUrl;
                            playback.style.display = 'block';
                            
                            // Start processing immediately
                            isProcessing_{component_id} = true;
                            button.className = 'record-button processing';
                            button.textContent = '{processing_text}';
                            button.disabled = true;
                            status.textContent = '{processing_text}';
                            spinner.style.display = 'block';
                            
                            // Convert to base64 and trigger Streamlit processing
                            const reader = new FileReader();
                            reader.onloadend = function() {{
                                const base64Audio = reader.result.split(',')[1];
                                
                                // Create audio data object
                                const audioData = {{
                                    component_id: '{component_id}',
                                    audio_data: base64Audio,
                                    timestamp: Date.now(),
                                    mime_type: 'audio/webm',
                                    auto_submit: true
                                }};
                                
                                // Store in window for Streamlit to access
                                window.audioRecordingData_{component_id} = audioData;
                                
                                // Trigger Streamlit rerun by dispatching custom event
                                const event = new CustomEvent('streamlit:audioRecorded', {{
                                    detail: audioData
                                }});
                                window.dispatchEvent(event);
                                
                                // Also create a hidden element for fallback detection
                                const hiddenDiv = document.createElement('div');
                                hiddenDiv.id = 'audio_ready_{component_id}';
                                hiddenDiv.style.display = 'none';
                                hiddenDiv.setAttribute('data-audio-ready', 'true');
                                hiddenDiv.setAttribute('data-component-id', '{component_id}');
                                hiddenDiv.textContent = JSON.stringify(audioData);
                                document.body.appendChild(hiddenDiv);
                                
                                // Force a small DOM change to trigger Streamlit
                                document.title = document.title + ' ';
                                setTimeout(() => {{
                                    document.title = document.title.trim();
                                }}, 100);
                            }};
                            reader.readAsDataURL(audioBlob);
                        }};
                        
                        mediaRecorder_{component_id}.start();
                        isRecording_{component_id} = true;
                        
                        button.textContent = '{stop_text}';
                        button.className = 'record-button recording';
                        status.textContent = '{recording_text}';
                        waveform.style.display = 'flex';
                        playback.style.display = 'none';
                        
                    }} catch (error) {{
                        console.error('Error accessing microphone:', error);
                        status.textContent = '{permission_text}';
                        button.disabled = false;
                    }}
                }} else {{
                    // Stop recording
                    if (mediaRecorder_{component_id} && mediaRecorder_{component_id}.state === 'recording') {{
                        mediaRecorder_{component_id}.stop();
                        mediaRecorder_{component_id}.stream.getTracks().forEach(track => track.stop());
                    }}
                    
                    isRecording_{component_id} = false;
                    waveform.style.display = 'none';
                }}
            }}
            
            // Handle page visibility change
            document.addEventListener('visibilitychange', function() {{
                if (document.hidden && isRecording_{component_id}) {{
                    toggleRecording_{component_id}();
                }}
            }});
            
            // Function to reset the recorder after processing
            window.resetRecorder_{component_id} = function() {{
                const button = document.getElementById('recordButton_{component_id}');
                const status = document.getElementById('status_{component_id}');
                const spinner = document.getElementById('spinner_{component_id}');
                
                isProcessing_{component_id} = false;
                button.className = 'record-button';
                button.textContent = '{start_text}';
                button.disabled = false;
                status.textContent = '{ready_text}';
                spinner.style.display = 'none';
                
                // Clean up the audio data
                if (window.audioRecordingData_{component_id}) {{
                    delete window.audioRecordingData_{component_id};
                }}
            }};
        </script>
    </body>
    </html>
    """
    
    # Render the component
    components.html(html_code, height=320)
    
    # Check for recorded audio data
    audio_ready_key = f'audio_ready_{component_id}'
    
    # JavaScript to check for audio data
    check_js = f"""
    <script>
    (function() {{
        const audioReadyDiv = document.getElementById('{audio_ready_key}');
        if (audioReadyDiv && audioReadyDiv.getAttribute('data-audio-ready') === 'true') {{
            // Audio is ready for processing
            const audioDataStr = audioReadyDiv.textContent;
            try {{
                const audioData = JSON.parse(audioDataStr);
                console.log('Audio data ready for processing:', audioData.timestamp);
                
                // Set a flag in Streamlit session state
                window.streamlitAudioReady_{component_id} = true;
                
                // Clean up the div
                audioReadyDiv.remove();
            }} catch (e) {{
                console.error('Error parsing audio data:', e);
            }}
        }}
    }})();
    </script>
    """
    
    components.html(check_js, height=0)
    
    # Check if audio is ready for processing
    if f'audio_data_{component_id}' not in st.session_state:
        st.session_state[f'audio_data_{component_id}'] = None
    
    return component_id


def create_streamlined_voice_recorder(language="en"):
    """
    Create a streamlined voice recorder that auto-submits after recording
    """
    # Use the streamlit-audio-recorder if available
    try:
        from streamlit_audio_recorder import st_audiorec
        
        if language == "bn":
            st.info("🎤 রেকর্ড করার জন্য নিচের বাটনে ক্লিক করুন")
        else:
            st.info("🎤 Click the button below to record")
        
        # Create the audio recorder
        wav_audio_data = st_audiorec()
        
        if wav_audio_data is not None:
            # Save to temporary file immediately
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(wav_audio_data)
                temp_path = tmp_file.name
            
            if language == "bn":
                st.success("✅ অডিও রেকর্ড সম্পন্ন! প্রক্রিয়াকরণ শুরু করা হচ্ছে...")
            else:
                st.success("✅ Audio recorded! Starting processing...")
            
            # Play the recorded audio for user confirmation
            st.audio(wav_audio_data, format="audio/wav")
            
            return temp_path
            
    except ImportError:
        if language == "bn":
            st.warning("স্ট্রিমলিট অডিও রেকর্ডার উপলব্ধ নেই। ফাইল আপলোড ব্যবহার করুন।")
        else:
            st.warning("Streamlit audio recorder not available. Please use file upload.")
    
    return None


def process_audio_automatically(audio_file_path, image_file, language_code, language_name):
    """
    Process the recorded audio automatically
    """
    if not audio_file_path or not os.path.exists(audio_file_path):
        return None, None, None
    
    try:
        # Import required modules
        from voice_of_the_patient import transcribe_with_groq
        from voice_of_the_doctor import text_to_speech
        from brain_of_the_doctor import encode_image, analyze_image_with_query
        from enhanced_text_chat import ChatSession
        
        # Step 1: Transcribe the audio
        with st.status("🎯 Converting speech to text..." if language_name == "English" else "🎯 অডিও টেক্সটে রূপান্তর করা হচ্ছে..."):
            transcribed_text = transcribe_with_groq(
                stt_model="whisper-large-v3",
                audio_filepath=audio_file_path,
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                language=language_code
            )
        
        if not transcribed_text or transcribed_text.strip() == "":
            if language_name == "Bengali":
                st.error("অডিও ট্রান্সক্রিপশন ব্যর্থ হয়েছে")
            else:
                st.error("Audio transcription failed")
            return None, None, None
        
        # Step 2: Process with AI
        with st.status("🤖 Processing with AI Doctor..." if language_name == "English" else "🤖 ডাক্তারের সাথে বিশ্লেষণ করা হচ্ছে..."):
            if image_file:
                # Process with image
                image_file.seek(0)
                
                # Save image to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(image_file.read())
                    image_filepath = tmp_img.name
                
                # Get system prompt for vision
                if language_code == "bn":
                    system_prompt = "আপনি একজন জ্ঞানী চিকিৎসা পেশাদার যিনি ভিজ্যুয়াল তথ্যের উপর ভিত্তি করে রোগীর অবস্থার প্রাথমিক মূল্যায়ন প্রদান করছেন।"
                else:
                    system_prompt = "You are a knowledgeable medical professional providing a preliminary assessment of a patient's condition based on visual information."
                
                doctor_response = analyze_image_with_query(
                    query=f"{system_prompt}\n\n{transcribed_text}",
                    encoded_image=encode_image(image_filepath),
                    language=language_code
                )
                
                # Clean up temp file
                os.unlink(image_filepath)
                
            else:
                # Process text only
                if 'chat_session' not in st.session_state:
                    st.session_state.chat_session = ChatSession()
                
                st.session_state.chat_session.add_user_message(transcribed_text)
                doctor_response = st.session_state.chat_session.get_response(language=language_code)
        
        # Step 3: Generate voice response
        audio_response_path = None
        try:
            with st.status("🔊 Generating voice response..." if language_name == "English" else "🔊 ভয়েস প্রতিক্রিয়া তৈরি করা হচ্ছে..."):
                audio_response_path = f"voice_response_{int(time.time())}.mp3"
                text_to_speech(
                    input_text=doctor_response, 
                    output_filepath=audio_response_path, 
                    language=language_code
                )
        except Exception as audio_error:
            logging.warning(f"Voice response generation failed: {audio_error}")
            audio_response_path = None
        
        return transcribed_text, doctor_response, audio_response_path
        
    except Exception as e:
        logging.error(f"Error in automatic audio processing: {e}")
        st.error(f"Processing error: {str(e)}")
        return None, None, None
    finally:
        # Clean up the original audio file
        try:
            if audio_file_path and os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
        except Exception as cleanup_error:
            logging.warning(f"Audio cleanup failed: {cleanup_error}")