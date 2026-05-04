# enhanced_text_chat_with_consultation.py - Updated text chat with medical consultation
import os
import logging
import streamlit as st
import tempfile
import time
from enhanced_medical_consultation import (
    EnhancedChatSession, 
    process_consultation_message, 
    get_consultation_status_display
)
from voice_of_the_doctor import text_to_speech

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Helper functions for the consultation system
def initialize_enhanced_chat_session(language="en"):
    """Initialize enhanced chat session in Streamlit session state"""
    session_key = f'enhanced_chat_session_{language}'
    
    if session_key not in st.session_state:
        st.session_state[session_key] = EnhancedChatSession(language)
    
    return st.session_state[session_key]


def display_consultation_progress(chat_session, language="en"):
    """Display consultation progress in the UI"""
    status_display = get_consultation_status_display(chat_session, language)
    
    if status_display:
        progress_info = chat_session.get_consultation_progress()
        
        # Create a progress bar
        if progress_info["active"] and progress_info["stage"] == "gathering_info":
            progress_percentage = progress_info["questions_completed"] / progress_info["total_questions"]
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                        border-left: 4px solid #2196f3;">
                {}
            </div>
            """.format(status_display), unsafe_allow_html=True)
            
            # Progress bar
            st.progress(progress_percentage)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                        border-left: 4px solid #ff9800;">
                {}
            </div>
            """.format(status_display), unsafe_allow_html=True)


def render_enhanced_text_chat_with_consultation(language="English", lang_code="en"):
    """Render the enhanced text chat interface with medical consultation"""
    
    # Initialize enhanced chat session
    chat_session = initialize_enhanced_chat_session(lang_code)
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1>💬 চিকিৎসা পরামর্শ</h1>
            <p>আমাদের এআই ডাক্তারের সাথে বিস্তারিত পরামর্শ নিন - ফলো-আপ প্রশ্ন সহ</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1>💬 AI Medical Consultation</h1>
            <p>Get detailed consultation with our AI Doctor - including follow-up questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display consultation progress if active
    display_consultation_progress(chat_session, lang_code)
    
    # Chat statistics
    display_enhanced_chat_stats(chat_session, lang_code)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history with enhanced styling
    if chat_session.history:
        for i, message in enumerate(chat_session.history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 {language == "Bengali" and "আপনি" or "You"}:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Check if this is a follow-up question
                is_follow_up = "📋" in message["content"] and ("Question" in message["content"] or "প্রশ্ন" in message["content"])
                
                message_class = "follow-up-message" if is_follow_up else "assistant-message"
                
                st.markdown(f"""
                <div class="{message_class}">
                    <strong>🏥 {language == "Bengali" and "ডাক্তার" or "Doctor"}:</strong><br>
                    {message["content"].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Audio player if available and it's a comprehensive response
                if not is_follow_up and len(message["content"]) > 200:
                    # Generate audio for longer responses
                    audio_key = f"audio_response_{i}_{len(message['content'])}"
                    if audio_key not in st.session_state:
                        try:
                            audio_file_path = f"enhanced_response_{i}_{int(time.time())}.mp3"
                            text_to_speech(
                                input_text=message["content"][:500],  # Limit for audio
                                output_filepath=audio_file_path, 
                                language=lang_code
                            )
                            if os.path.exists(audio_file_path):
                                st.session_state[audio_key] = audio_file_path
                        except Exception as e:
                            logging.warning(f"Audio generation failed: {e}")
                    
                    if audio_key in st.session_state and os.path.exists(st.session_state[audio_key]):
                        st.audio(st.session_state[audio_key], format="audio/mp3")
    else:
        # Welcome message for empty chat
        if language == "Bengali":
            welcome_msg = """
            <div class="assistant-message">
                <strong>🏥 ডাক্তার:</strong><br>
                নমস্কার! আমি আপনার এআই চিকিৎসক। আপনার স্বাস্থ্য সংক্রান্ত যেকোনো সমস্যার কথা বলুন, আমি বিস্তারিত প্রশ্ন করে সঠিক পরামর্শ দেওয়ার চেষ্টা করব।
                
                🔍 <strong>নতুন বৈশিষ্ট্য</strong>: আমি আপনার সমস্যা ভালভাবে বুঝতে ফলো-আপ প্রশ্ন করব এবং তারপর বিস্তারিত বিশ্লেষণ ও পরামর্শ দেব।
            </div>
            """
        else:
            welcome_msg = """
            <div class="assistant-message">
                <strong>🏥 Doctor:</strong><br>
                Hello! I'm your AI Doctor. Tell me about any health concerns you have, and I'll ask detailed follow-up questions to provide you with accurate guidance.
                
                🔍 <strong>Enhanced Feature</strong>: I'll ask follow-up questions to better understand your condition and then provide comprehensive analysis and recommendations.
            </div>
            """
        st.markdown(welcome_msg, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([6, 2, 1])
    
    with col1:
        # Dynamic placeholder based on consultation status
        progress = chat_session.get_consultation_progress()
        
        if progress["active"] and progress["stage"] == "gathering_info":
            if language == "Bengali":
                placeholder_text = "ডাক্তারের প্রশ্নের উত্তর দিন..."
                label_text = "💭 আপনার উত্তর এখানে টাইপ করুন..."
            else:
                placeholder_text = "Answer the doctor's question..."
                label_text = "💭 Type your answer here..."
        else:
            if language == "Bengali":
                placeholder_text = "যেমন: আমার মাথা ব্যথা করছে এবং জ্বর আছে"
                label_text = "💭 আপনার স্বাস্থ্য সমস্যার কথা বলুন..."
            else:
                placeholder_text = "e.g., I have a headache and fever"
                label_text = "💭 Describe your health concern..."
        
        user_input = st.text_area(
            label_text,
            key=f"enhanced_chat_input_{lang_code}_{len(chat_session.history)}",
            placeholder=placeholder_text,
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        if language == "Bengali":
            chat_image = st.file_uploader(
                "📷 ছবি যুক্ত করুন",
                type=['jpg', 'jpeg', 'png'],
                key=f"enhanced_chat_image_{lang_code}_{len(chat_session.history)}",
                help="প্রয়োজনে একটি ছবি আপলোড করুন"
            )
        else:
            chat_image = st.file_uploader(
                "📷 Add Image",
                type=['jpg', 'jpeg', 'png'],
                key=f"enhanced_chat_image_{lang_code}_{len(chat_session.history)}",
                help="Upload an image if needed"
            )
    
    with col3:
        if language == "Bengali":
            send_button = st.button(
                "📤 পাঠান", 
                key=f"send_enhanced_chat_{lang_code}_{len(chat_session.history)}", 
                type="primary", 
                use_container_width=True
            )
        else:
            send_button = st.button(
                "📤 Send", 
                key=f"send_enhanced_chat_{lang_code}_{len(chat_session.history)}", 
                type="primary", 
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced quick questions based on consultation status
    if not chat_session.in_consultation:
        display_enhanced_quick_questions(chat_session, language, lang_code)
    
    # Process message
    if (send_button or user_input) and user_input and user_input.strip():
        with st.spinner("🤔 Processing your message..." if language == "English" else "🤔 আপনার বার্তা প্রক্রিয়া করা হচ্ছে..."):
            try:
                # Process the message through the consultation system
                if chat_image:
                    # For now, handle image with regular text processing
                    # You can extend this to include image analysis in consultation
                    response = process_consultation_message(chat_session, user_input)
                else:
                    response = process_consultation_message(chat_session, user_input)
                
                # Rerun to show the new message
                st.rerun()
                
            except Exception as e:
                logging.error(f"Error processing enhanced message: {e}")
                if language == "Bengali":
                    st.error(f"একটি ত্রুটি ঘটেছে: {str(e)}")
                else:
                    st.error(f"An error occurred: {str(e)}")
    
    elif send_button and not user_input.strip():
        if language == "Bengali":
            st.warning("⚠️ অনুগ্রহ করে একটি বার্তা টাইপ করুন।")
        else:
            st.warning("⚠️ Please type a message.")


def display_enhanced_quick_questions(chat_session, language, lang_code):
    """Display enhanced quick questions for starting consultations"""
    
    if language == "Bengali":
        st.markdown("### 🔥 দ্রুত পরামর্শ শুরু করুন")
        quick_questions = [
            "আমার জ্বর এবং মাথা ব্যথা",
            "পেটে ব্যথা ও অস্বস্তি", 
            "কাশি ও গলা ব্যথা",
            "ত্বকে সমস্যা"
        ]
        col_headers = ["জ্বর ও ব্যথা", "পেটের সমস্যা", "শ্বাসযন্ত্র", "ত্বক সমস্যা"]
    else:
        st.markdown("### 🔥 Start Quick Consultation")
        quick_questions = [
            "I have fever and headache",
            "Stomach pain and discomfort",
            "Cough and sore throat", 
            "Skin problems"
        ]
        col_headers = ["Fever & Pain", "Digestive", "Respiratory", "Skin Issues"]
    
    # Display quick question buttons
    cols = st.columns(4)
    for i, (question, header) in enumerate(zip(quick_questions, col_headers)):
        with cols[i]:
            st.markdown(f"**{header}**")
            if st.button(question, key=f"enhanced_quick_{i}_{lang_code}_{len(chat_session.history)}", use_container_width=True):
                # Process the quick question through consultation system
                with st.spinner("Starting consultation..." if language == "English" else "পরামর্শ শুরু করা হচ্ছে..."):
                    try:
                        response = process_consultation_message(chat_session, question)
                        st.rerun()
                    except Exception as e:
                        logging.error(f"Error with quick question: {e}")
                        st.error(f"Error: {e}")


def display_enhanced_chat_stats(chat_session, lang_code):
    """Display enhanced chat statistics including consultation info"""
    
    total_messages = len(chat_session.history)
    user_messages = len([msg for msg in chat_session.history if msg["role"] == "user"])
    assistant_messages = len([msg for msg in chat_session.history if msg["role"] == "assistant"])
    
    progress = chat_session.get_consultation_progress()
    
    if lang_code == "bn":
        if progress["active"]:
            stats_text = f"""📊 সক্রিয় পরামর্শ | 💬 {total_messages} বার্তা | 
                           📋 {progress["questions_completed"]}/{progress["total_questions"]} প্রশ্ন সম্পন্ন"""
        else:
            stats_text = f"📊 চ্যাট পরিসংখ্যান: {total_messages} মোট বার্তা | {user_messages} ব্যবহারকারী | {assistant_messages} ডাক্তার"
    else:
        if progress["active"]:
            stats_text = f"""📊 Active Consultation | 💬 {total_messages} Messages | 
                           📋 {progress["questions_completed"]}/{progress["total_questions"]} Questions Completed"""
        else:
            stats_text = f"📊 Chat Stats: {total_messages} Total Messages | {user_messages} User | {assistant_messages} Doctor"
    
    if total_messages > 0:
        st.markdown(f'<div class="chat-stats">{stats_text}</div>', unsafe_allow_html=True)


def reset_enhanced_chat_session(lang_code):
    """Reset the enhanced chat session"""
    session_key = f'enhanced_chat_session_{lang_code}'
    
    if session_key in st.session_state:
        st.session_state[session_key].clear_history()
    
    # Clear any cached audio files
    for key in list(st.session_state.keys()):
        if key.startswith("audio_response_"):
            try:
                if os.path.exists(st.session_state[key]):
                    os.unlink(st.session_state[key])
                del st.session_state[key]
            except:
                pass


def export_consultation_history(chat_session, language="en"):
    """Export consultation history with structured format"""
    import json
    from datetime import datetime
    
    # Get consultation progress
    progress = chat_session.get_consultation_progress()
    
    # Create export data
    export_data = {
        "export_date": datetime.now().isoformat(),
        "language": language,
        "consultation_active": progress.get("active", False),
        "consultation_stage": progress.get("stage", "none"),
        "chief_complaint": progress.get("chief_complaint", ""),
        "total_messages": len(chat_session.history),
        "conversation": []
    }
    
    for i, message in enumerate(chat_session.history):
        export_data["conversation"].append({
            "message_id": i + 1,
            "role": message["role"],
            "content": message["content"],
            "timestamp": datetime.now().isoformat(),
            "is_follow_up": "📋" in message["content"] if message["role"] == "assistant" else False
        })
    
    # Convert to JSON string
    json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    # Create download button
    filename = f"medical_consultation_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    return json_string, filename


# CSS for enhanced consultation UI
ENHANCED_CONSULTATION_CSS = """
<style>
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

/* Consultation progress styling */
.consultation-progress {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #2196f3;
    animation: fadeIn 0.5s ease-in;
}

/* Enhanced user message for answers */
.user-answer-message {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    color: #e65100;
    padding: 15px 20px;
    border-radius: 20px 20px 5px 20px;
    margin: 10px 0;
    margin-left: 20%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-right: 4px solid #ff9800;
    animation: slideInRight 0.3s ease-out;
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

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Quick consultation buttons */
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
"""