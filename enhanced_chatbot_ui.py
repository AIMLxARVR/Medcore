# enhanced_chatbot_ui.py - Modern realistic chatbot interface for medical consultation
import streamlit as st
import time
from datetime import datetime
import json

def apply_chatbot_css():
    """Apply modern chatbot CSS styling"""
    st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Chat container */
    .chat-container {
        height: 600px;
        overflow-y: auto;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
    }
    
    /* Individual message bubbles */
    .message {
        display: flex;
        margin-bottom: 20px;
        animation: messageSlide 0.3s ease-out;
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message.user {
        justify-content: flex-end;
    }
    
    .message.assistant {
        justify-content: flex-start;
    }
    
    /* Avatar styling */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        margin: 0 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        flex-shrink: 0;
    }
    
    .avatar.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        order: 2;
    }
    
    .avatar.assistant {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        order: 1;
    }
    
    /* Message bubble */
    .bubble {
        max-width: 70%;
        padding: 15px 20px;
        border-radius: 20px;
        position: relative;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }
    
    .bubble.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 5px;
        order: 1;
    }
    
    .bubble.assistant {
        background: white;
        color: #333;
        border-bottom-left-radius: 5px;
        border: 1px solid #e1e8ed;
        order: 2;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 15px 20px;
        background: white;
        border-radius: 20px;
        border-bottom-left-radius: 5px;
        margin-left: 50px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e1e8ed;
        max-width: 100px;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #999;
        animation: typing 1.4s infinite;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* Message timestamp */
    .timestamp {
        font-size: 11px;
        color: #999;
        margin-top: 5px;
        text-align: right;
    }
    
    .bubble.assistant .timestamp {
        text-align: left;
    }
    
    /* Input area */
    .chat-input-container {
        background: white;
        border-radius: 25px;
        padding: 5px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 2px solid #e1e8ed;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .chat-input-container:focus-within {
        border-color: #667eea;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 15px 20px !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        background: transparent !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Send button */
    .send-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-size: 18px;
        margin-right: 5px;
    }
    
    .send-button:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat header */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 20px 20px 0 0;
        margin-bottom: 0;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .chat-header .avatar {
        width: 50px;
        height: 50px;
        background: rgba(255,255,255,0.2);
        font-size: 24px;
    }
    
    .chat-header .info h3 {
        margin: 0;
        font-size: 20px;
    }
    
    .chat-header .info p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 14px;
    }
    
    .status-online {
        width: 12px;
        height: 12px;
        background: #4CAF50;
        border-radius: 50%;
        display: inline-block;
        margin-left: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }
    
    /* Progress indicator for consultation */
    .consultation-progress {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .progress-bar {
        background: rgba(255,255,255,0.3);
        height: 8px;
        border-radius: 4px;
        margin-top: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: white;
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Quick reply buttons */
    .quick-replies {
        display: flex;
        gap: 10px;
        margin: 15px 0;
        flex-wrap: wrap;
    }
    
    .quick-reply-btn {
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .quick-reply-btn:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Emergency alert */
    .emergency-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 15px;
        margin: 15px 0;
        animation: emergencyPulse 1s infinite;
    }
    
    @keyframes emergencyPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* File upload area in chat */
    .file-upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        background: rgba(102, 126, 234, 0.1);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .file-upload-area:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #5a67d8;
    }
    
    /* Hide streamlit components we don't need */
    .stTextInput label {
        display: none !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .bubble {
            max-width: 85%;
        }
        
        .chat-container {
            height: 500px;
            padding: 15px;
        }
        
        .chat-header {
            padding: 15px;
        }
        
        .quick-replies {
            justify-content: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_chat_header(language="English"):
    """Render modern chat header"""
    status_text = "Online" if language == "English" else "অনলাইন"
    doctor_name = "Dr. AI Assistant" if language == "English" else "ডাঃ এআই সহায়ক"
    specialty = "Medical Consultation Specialist" if language == "English" else "চিকিৎসা পরামর্শ বিশেষজ্ঞ"
    
    st.markdown(f"""
    <div class="chat-header">
        <div class="avatar">🩺</div>
        <div class="info">
            <h3>{doctor_name}</h3>
            <p>{specialty} <span class="status-online"></span> {status_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_consultation_progress(progress_info, language="English"):
    """Render consultation progress bar"""
    if not progress_info or not progress_info.get("active"):
        return
    
    progress_percentage = progress_info.get("progress_percentage", 0)
    current_q = progress_info.get("current_question", 0)
    total_q = progress_info.get("total_questions", 0)
    
    if language == "Bengali":
        progress_text = f"পরামর্শের অগ্রগতি: {current_q}/{total_q} প্রশ্ন সম্পন্ন"
    else:
        progress_text = f"Consultation Progress: {current_q}/{total_q} questions completed"
    
    st.markdown(f"""
    <div class="consultation-progress">
        <div>{progress_text}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percentage}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_message_bubble(message, is_user=True, timestamp=None, show_avatar=True):
    """Render individual message bubble"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    avatar_emoji = "👤" if is_user else "🩺"
    role_class = "user" if is_user else "assistant"
    
    # Handle emergency messages
    is_emergency = "🚨" in message or "emergency" in message.lower() or "urgent" in message.lower()
    emergency_class = " emergency-alert" if is_emergency and not is_user else ""
    
    st.markdown(f"""
    <div class="message {role_class}">
        <div class="avatar {role_class}">{avatar_emoji}</div>
        <div class="bubble {role_class}{emergency_class}">
            {message}
            <div class="timestamp">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_typing_indicator():
    """Render typing indicator"""
    st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_quick_replies(options, language="English"):
    """Render quick reply buttons"""
    if not options:
        return
    
    buttons_html = ""
    for option in options:
        buttons_html += f'<div class="quick-reply-btn" onclick="selectQuickReply(\'{option}\')">{option}</div>'
    
    st.markdown(f"""
    <div class="quick-replies">
        {buttons_html}
    </div>
    <script>
    function selectQuickReply(option) {{
        // This would be handled by Streamlit components
        console.log('Selected:', option);
    }}
    </script>
    """, unsafe_allow_html=True)

def render_file_upload_area(language="English"):
    """Render file upload area in chat"""
    upload_text = "Drag and drop files here or click to browse" if language == "English" else "ফাইল এখানে টেনে আনুন বা ব্রাউজ করতে ক্লিক করুন"
    
    st.markdown(f"""
    <div class="file-upload-area">
        📎 {upload_text}
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_chatbot_ui(language="English"):
    """Create the main enhanced chatbot UI"""
    
    # Apply CSS
    apply_chatbot_css()
    
    # Language code
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        # Add welcome message
        welcome_msg = (
            "Hello! I'm your AI Medical Assistant. I'm here to help with your health concerns. "
            "How are you feeling today?" if language == "English" else
            "নমস্কার! আমি আপনার এআই চিকিৎসা সহায়ক। আমি আপনার স্বাস্থ্য সমস্যায় সাহায্য করতে এসেছি। "
            "আজ আপনার কেমন লাগছে?"
        )
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": welcome_msg,
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    if 'consultation_active' not in st.session_state:
        st.session_state.consultation_active = False
    
    if 'current_question_options' not in st.session_state:
        st.session_state.current_question_options = []
    
    # Render chat header
    render_chat_header(language)
    
    # Render consultation progress if active
    if st.session_state.consultation_active:
        # Mock progress for demo
        progress_info = {
            "active": True,
            "progress_percentage": 40,
            "current_question": 2,
            "total_questions": 5
        }
        render_consultation_progress(progress_info, language)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Render all messages
        for msg in st.session_state.chat_messages:
            render_message_bubble(
                message=msg["content"],
                is_user=(msg["role"] == "user"),
                timestamp=msg.get("timestamp", "")
            )
        
        # Show typing indicator if processing
        if st.session_state.get('is_typing', False):
            render_typing_indicator()
        
        # Show quick replies if available
        if st.session_state.current_question_options:
            render_quick_replies(st.session_state.current_question_options, language)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    # Create columns for input and send button
    col1, col2, col3 = st.columns([8, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Type your message here..." if language == "English" else "এখানে আপনার বার্তা টাইপ করুন...",
            key=f"chat_input_{len(st.session_state.chat_messages)}",
            label_visibility="collapsed"
        )
    
    with col2:
        # File upload button
        uploaded_file = st.file_uploader(
            "",
            type=['jpg', 'jpeg', 'png', 'wav', 'mp3'],
            label_visibility="collapsed",
            key=f"file_upload_{len(st.session_state.chat_messages)}"
        )
        if uploaded_file:
            st.success("📎")
    
    with col3:
        send_clicked = st.button("➤", key="send_btn", help="Send message")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle message sending
    if (send_clicked and user_input) or (user_input and st.session_state.get('auto_send', False)):
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Set typing indicator
        st.session_state.is_typing = True
        st.rerun()
    
    # Process user input and generate response
    if st.session_state.get('is_typing', False):
        # Simulate processing time
        time.sleep(1)
        
        # Generate AI response based on last user message
        last_user_message = [msg for msg in st.session_state.chat_messages if msg["role"] == "user"][-1]["content"]
        ai_response = generate_ai_response(last_user_message, language)
        
        # Add AI response
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": ai_response["message"],
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Set options for next interaction
        st.session_state.current_question_options = ai_response.get("options", [])
        
        # Update consultation status
        if "consultation" in last_user_message.lower():
            st.session_state.consultation_active = True
        
        # Clear typing indicator
        st.session_state.is_typing = False
        st.rerun()
    
    # Quick action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🆘 Emergency", type="primary"):
            emergency_msg = (
                "🚨 EMERGENCY DETECTED: Please call your local emergency services immediately (911, 999, or your local emergency number). "
                "If you're experiencing chest pain, difficulty breathing, severe bleeding, or loss of consciousness, seek immediate medical attention."
                if language == "English" else
                "🚨 জরুরি অবস্থা সনাক্ত: অনুগ্রহ করে অবিলম্বে আপনার স্থানীয় জরুরি সেবায় কল করুন। "
                "যদি আপনার বুকে ব্যথা, শ্বাসকষ্ট, প্রচণ্ড রক্তপাত বা অজ্ঞান হয়ে যাওয়ার সমস্যা হয়, তাহলে অবিলম্বে চিকিৎসা সেবা নিন।"
            )
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": emergency_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col2:
        if st.button("🩺 Start Checkup"):
            checkup_msg = (
                "I'll guide you through a medical consultation. Let's start with some basic questions. "
                "What's your main health concern today?"
                if language == "English" else
                "আমি আপনাকে একটি চিকিৎসা পরামর্শের মাধ্যমে গাইড করব। কিছু মৌলিক প্রশ্ন দিয়ে শুরু করি। "
                "আজ আপনার প্রধান স্বাস্থ্য সমস্যা কী?"
            )
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": checkup_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.session_state.consultation_active = True
            st.rerun()
    
    with col3:
        if st.button("📋 View History"):
            history_msg = (
                f"Your consultation history: {len([m for m in st.session_state.chat_messages if m['role'] == 'user'])} messages exchanged. "
                "Would you like me to summarize our conversation?"
                if language == "English" else
                f"আপনার পরামর্শের ইতিহাস: {len([m for m in st.session_state.chat_messages if m['role'] == 'user'])} বার্তা আদান-প্রদান হয়েছে। "
                "আমি কি আমাদের কথোপকথনের সারসংক্ষেপ দেব?"
            )
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": history_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    with col4:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.session_state.consultation_active = False
            st.session_state.current_question_options = []
            # Add new welcome message
            welcome_msg = (
                "Hello! I'm your AI Medical Assistant. How can I help you today?"
                if language == "English" else
                "নমস্কার! আমি আপনার এআই চিকিৎসা সহায়ক। আজ আমি কীভাবে আপনাকে সাহায্য করতে পারি?"
            )
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": welcome_msg,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()

def generate_ai_response(user_message, language="English"):
    """Generate AI response based on user message"""
    
    # Simple response generation for demo
    # In real implementation, this would call your AI models
    
    responses = {
        "English": {
            "greetings": [
                "Hello! I'm here to help with your health concerns. What's bothering you today?",
                "Hi there! I'm your AI medical assistant. How can I assist you with your health today?"
            ],
            "symptoms": [
                "I understand you're experiencing some symptoms. Can you describe them in more detail? When did they start?",
                "Thank you for sharing that with me. To better assist you, could you tell me how long you've been experiencing this?",
                "That's concerning. Let me ask a few follow-up questions to better understand your condition."
            ],
            "pain": [
                "I'm sorry to hear you're in pain. Can you rate your pain on a scale of 1-10? Also, when did it start?",
                "Pain can be very distressing. Can you describe the type of pain - is it sharp, dull, throbbing, or burning?"
            ],
            "general": [
                "I understand your concern. Let me help you with that. Can you provide more details?",
                "Thank you for that information. Based on what you've told me, I'd like to ask a few more questions."
            ]
        },
        "Bengali": {
            "greetings": [
                "নমস্কার! আমি আপনার স্বাস্থ্য সমস্যায় সাহায্য করতে এসেছি। আজ আপনার কী সমস্যা?",
                "হ্যালো! আমি আপনার এআই চিকিৎসা সহায়ক। আজ আপনার স্বাস্থ্যের ব্যাপারে কীভাবে সাহায্য করতে পারি?"
            ],
            "symptoms": [
                "আমি বুঝতে পারছি আপনার কিছু লক্ষণ রয়েছে। আরো বিস্তারিত বর্ণনা করতে পারেন? কখন থেকে শুরু হয়েছে?",
                "এই তথ্য দেওয়ার জন্য ধন্যবাদ। আরো ভাল সাহায্য করতে, আপনি বলতে পারেন কতদিন ধরে এই সমস্যা হচ্ছে?",
                "এটা উদ্বেগজনক। আপনার অবস্থা ভাল বোঝার জন্য আমি কয়েকটি ফলো-আপ প্রশ্ন করব।"
            ],
            "pain": [
                "আপনার ব্যথার জন্য দুঃখিত। ১-১০ স্কেলে আপনার ব্যথা কেমন? আর কখন থেকে শুরু হয়েছে?",
                "ব্যথা খুবই কষ্টকর। আপনি ব্যথার ধরণ বর্ণনা করতে পারেন - তীক্ষ্ণ, নিস্তেজ, স্পন্দনশীল, নাকি জ্বালাপোড়া?"
            ],
            "general": [
                "আমি আপনার উদ্বেগ বুঝতে পারছি। এতে আমি আপনাকে সাহায্য করব। আরো বিস্তারিত বলতে পারেন?",
                "এই তথ্যের জন্য ধন্যবাদ। আপনি যা বলেছেন তার ভিত্তিতে, আমি আরো কয়েকটি প্রশ্ন করতে চাই।"
            ]
        }
    }
    
    # Determine response category
    user_lower = user_message.lower()
    
    if any(word in user_lower for word in ["hello", "hi", "hey", "নমস্কার", "হ্যালো"]):
        category = "greetings"
    elif any(word in user_lower for word in ["pain", "hurt", "ache", "ব্যথা", "কষ্ট"]):
        category = "pain"
    elif any(word in user_lower for word in ["fever", "headache", "cough", "symptoms", "জ্বর", "মাথাব্যথা", "কাশি", "লক্ষণ"]):
        category = "symptoms"
    else:
        category = "general"
    
    # Select response
    lang_responses = responses[language]
    import random
    response_text = random.choice(lang_responses[category])
    
    # Generate options based on context
    options = []
    if category == "symptoms":
        if language == "English":
            options = ["It started today", "A few days ago", "Over a week ago", "It's been ongoing"]
        else:
            options = ["আজ থেকে শুরু", "কয়েকদিন আগে থেকে", "এক সপ্তাহেরও বেশি", "অনেকদিন ধরে"]
    elif category == "pain":
        if language == "English":
            options = ["Mild (1-3)", "Moderate (4-6)", "Severe (7-10)"]
        else:
            options = ["হালকা (১-৩)", "মাঝারি (৪-৬)", "তীব্র (৭-১০)"]
    
    return {
        "message": response_text,
        "options": options
    }

# Integration function for the main medical app
def render_enhanced_medical_chat(language="English"):
    """Render the enhanced chatbot UI for medical consultation"""
    
    st.markdown("### 💬 Enhanced Medical Consultation")
    
    # Check if enhanced consultation is available
    try:
        from enhanced_text_chat_with_consultation import initialize_enhanced_chat_session
        ENHANCED_CHAT_AVAILABLE = True
    except ImportError:
        ENHANCED_CHAT_AVAILABLE = False
    
    # Language selection
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize enhanced chat session if available
    if ENHANCED_CHAT_AVAILABLE:
        try:
            # Try to use the enhanced consultation system
            chat_session = initialize_enhanced_chat_session(lang_code)
            
            # Create the enhanced chatbot UI
            create_enhanced_chatbot_ui(language)
            
            # Integration with enhanced consultation
            if st.session_state.get('consultation_active', False):
                st.markdown("---")
                st.markdown("**🔄 Enhanced Consultation Integration**")
                
                # Show consultation status
                progress = chat_session.get_consultation_progress() if hasattr(chat_session, 'get_consultation_progress') else None
                if progress and progress.get("active"):
                    render_consultation_progress(progress, language)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Export Consultation", type="secondary"):
                        # Export functionality
                        export_data = {
                            "messages": st.session_state.chat_messages,
                            "language": language,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="💾 Download Chat History",
                            data=export_json,
                            file_name=f"medical_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                
                with col2:
                    if st.button("🔄 Reset Consultation", type="secondary"):
                        if hasattr(chat_session, 'clear_history'):
                            chat_session.clear_history()
                        st.session_state.chat_messages = []
                        st.session_state.consultation_active = False
                        st.rerun()
            
        except Exception as e:
            st.error(f"❌ Enhanced consultation integration failed: {str(e)}")
            st.info("Using basic chatbot interface...")
            create_enhanced_chatbot_ui(language)
    else:
        # Use basic enhanced chatbot UI
        create_enhanced_chatbot_ui(language)

# Voice integration function
def render_voice_integrated_chat(language="English"):
    """Render chatbot with voice integration"""
    
    # Check voice capabilities
    try:
        from voice_of_the_patient import process_uploaded_audio_file
        from voice_of_the_doctor import text_to_speech
        VOICE_AVAILABLE = True
    except ImportError:
        VOICE_AVAILABLE = False
    
    if VOICE_AVAILABLE:
        st.markdown("#### 🎤 Voice-Enabled Chat")
        
        # Voice input section
        with st.expander("🎙️ Voice Input", expanded=False):
            audio_file = st.file_uploader(
                "Record or upload your voice message:",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                help="Speak your symptoms or questions"
            )
            
            if audio_file:
                st.audio(audio_file)
                
                if st.button("🎯 Process Voice Message"):
                    try:
                        with st.spinner("Processing voice..."):
                            lang_code = "bn" if language == "Bengali" else "en"
                            transcription = process_uploaded_audio_file(audio_file, lang_code)
                            
                            # Add transcribed message to chat
                            st.session_state.chat_messages.append({
                                "role": "user",
                                "content": f"🎤 Voice: {transcription}",
                                "timestamp": datetime.now().strftime("%H:%M")
                            })
                            
                            st.success("✅ Voice message processed!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Voice processing failed: {str(e)}")
        
        # Voice output section
        with st.expander("🔊 Voice Output", expanded=False):
            if st.session_state.chat_messages:
                last_ai_message = None
                for msg in reversed(st.session_state.chat_messages):
                    if msg["role"] == "assistant":
                        last_ai_message = msg["content"]
                        break
                
                if last_ai_message:
                    if st.button("🔊 Listen to Last Response"):
                        try:
                            with st.spinner("Generating speech..."):
                                lang_code = "bn" if language == "Bengali" else "en"
                                audio_file_path = f"response_{int(time.time())}.mp3"
                                
                                result_path = text_to_speech(
                                    input_text=last_ai_message,
                                    output_filepath=audio_file_path,
                                    language=lang_code
                                )
                                
                                if result_path and os.path.exists(result_path):
                                    with open(result_path, 'rb') as f:
                                        audio_bytes = f.read()
                                    st.audio(audio_bytes, format='audio/mp3')
                                    
                                    # Cleanup
                                    os.unlink(result_path)
                                else:
                                    st.error("❌ Failed to generate speech")
                        except Exception as e:
                            st.error(f"❌ Speech generation failed: {str(e)}")
    
    # Render the main chat interface
    create_enhanced_chatbot_ui(language)

# Cancer consultation integration
def render_cancer_integrated_chat(language="English"):
    """Render chatbot with cancer consultation integration"""
    
    try:
        from cancer_reasoning_engine import CancerReasoningEngine
        CANCER_AVAILABLE = True
    except ImportError:
        CANCER_AVAILABLE = False
    
    if CANCER_AVAILABLE:
        st.markdown("#### 🎯 Cancer Risk Assessment Chat")
        
        # Initialize cancer reasoning engine
        lang_code = "bn" if language == "Bengali" else "en"
        
        if 'cancer_engine' not in st.session_state:
            st.session_state.cancer_engine = CancerReasoningEngine(lang_code)
        
        # Cancer-specific quick actions
        st.markdown("**🎯 Cancer Consultation Quick Actions:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🩺 Start Risk Assessment"):
                risk_msg = (
                    "I'll help assess your cancer risk. Let's start with some questions about your symptoms and health history. "
                    "Do you have any concerning symptoms like unexplained weight loss, persistent fatigue, or unusual lumps?"
                    if language == "English" else
                    "আমি আপনার ক্যান্সারের ঝুঁকি মূল্যায়ন করতে সাহায্য করব। আপনার লক্ষণ এবং স্বাস্থ্যের ইতিহাস নিয়ে কিছু প্রশ্ন দিয়ে শুরু করি। "
                    "আপনার কি কোন উদ্বেগজনক লক্ষণ আছে যেমন অব্যাখ্যাত ওজন হ্রাস, ক্রমাগত ক্লান্তি, বা অস্বাভাবিক গুটি?"
                )
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": risk_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.session_state.consultation_active = True
                st.rerun()
        
        with col2:
            if st.button("📊 View Risk Factors"):
                risk_factors_msg = (
                    "Key cancer risk factors include: smoking, family history, age over 50, excessive alcohol consumption, "
                    "poor diet, lack of exercise, and certain infections. Which of these might apply to you?"
                    if language == "English" else
                    "প্রধান ক্যান্সারের ঝুঁকির কারণগুলি: ধূমপান, পারিবারিক ইতিহাস, ৫০ বছরের বেশি বয়স, অতিরিক্ত মদ্যপান, "
                    "খারাপ খাদ্যাভ্যাস, ব্যায়ামের অভাব, এবং নির্দিষ্ট সংক্রমণ। এগুলির মধ্যে কোনটি আপনার ক্ষেত্রে প্রযোজ্য?"
                )
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": risk_factors_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        
        with col3:
            if st.button("🔍 Screening Info"):
                screening_msg = (
                    "Cancer screening recommendations vary by age and gender. Regular mammograms, colonoscopies, "
                    "Pap smears, and skin checks can help detect cancer early. Would you like specific recommendations?"
                    if language == "English" else
                    "ক্যান্সার স্ক্রিনিং সুপারিশ বয়স এবং লিঙ্গ অনুযায়ী ভিন্ন। নিয়মিত ম্যামোগ্রাম, কোলনোস্কোপি, "
                    "প্যাপ স্মিয়ার, এবং চর্মের পরীক্ষা প্রাথমিক পর্যায়ে ক্যান্সার সনাক্ত করতে সাহায্য করে। আপনি কি নির্দিষ্ট সুপারিশ চান?"
                )
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": screening_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.rerun()
    
    # Render the main chat interface
    create_enhanced_chatbot_ui(language)

# Prescription analysis integration
def render_prescription_integrated_chat(language="English"):
    """Render chatbot with prescription analysis integration"""
    
    try:
        from prescription_analysis import PrescriptionAnalyzer
        PRESCRIPTION_AVAILABLE = True
    except ImportError:
        PRESCRIPTION_AVAILABLE = False
    
    if PRESCRIPTION_AVAILABLE:
        st.markdown("#### 📋 Prescription Analysis Chat")
        
        # Prescription upload in chat
        with st.expander("📤 Upload Prescription Image", expanded=False):
            prescription_file = st.file_uploader(
                "Upload prescription image for analysis:",
                type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
                help="Upload clear images of prescriptions for AI analysis"
            )
            
            if prescription_file:
                st.image(prescription_file, caption="Uploaded Prescription", width=300)
                
                if st.button("🔍 Analyze Prescription"):
                    try:
                        with st.spinner("Analyzing prescription..."):
                            lang_code = "bn" if language == "Bengali" else "en"
                            
                            # Save and analyze prescription
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                                tmp_file.write(prescription_file.getvalue())
                                temp_path = tmp_file.name
                            
                            analyzer = PrescriptionAnalyzer(lang_code)
                            ocr_results = analyzer.extract_text_with_multiple_ocr(temp_path)
                            
                            if ocr_results["best_result"]:
                                analysis_results = analyzer.analyze_prescription_content(ocr_results["best_result"])
                                
                                analysis_msg = (
                                    f"📋 Prescription Analysis Complete!\n\n"
                                    f"**Extracted Text:** {ocr_results['best_result'][:200]}...\n\n"
                                    f"**Analysis:** {analysis_results.get('summary', 'Analysis completed successfully.')}\n\n"
                                    f"⚠️ Please verify this information with your pharmacist or doctor."
                                    if language == "English" else
                                    f"📋 প্রেসক্রিপশন বিশ্লেষণ সম্পন্ন!\n\n"
                                    f"**নিষ্কাশিত টেক্সট:** {ocr_results['best_result'][:200]}...\n\n"
                                    f"**বিশ্লেষণ:** {analysis_results.get('summary', 'বিশ্লেষণ সফলভাবে সম্পন্ন।')}\n\n"
                                    f"⚠️ অনুগ্রহ করে এই তথ্য আপনার ফার্মাসিস্ট বা ডাক্তারের সাথে যাচাই করুন।"
                                )
                                
                                st.session_state.chat_messages.append({
                                    "role": "assistant",
                                    "content": analysis_msg,
                                    "timestamp": datetime.now().strftime("%H:%M")
                                })
                                
                                # Cleanup
                                os.unlink(temp_path)
                                st.success("✅ Prescription analyzed!")
                                st.rerun()
                            else:
                                st.error("❌ Could not extract text from prescription image")
                    except Exception as e:
                        st.error(f"❌ Prescription analysis failed: {str(e)}")
    
    # Render the main chat interface
    create_enhanced_chatbot_ui(language)

# Main integration function for the medical app
def create_complete_chatbot_interface(language="English"):
    """Create complete chatbot interface with all integrations"""
    
    # Tab selection for different chat modes
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 General Chat",
        "🎤 Voice Chat", 
        "🎯 Cancer Chat",
        "📋 Prescription Chat"
    ])
    
    with tab1:
        render_enhanced_medical_chat(language)
    
    with tab2:
        render_voice_integrated_chat(language)
    
    with tab3:
        render_cancer_integrated_chat(language)
    
    with tab4:
        render_prescription_integrated_chat(language)

# Usage in main app (replace the existing render_enhanced_chat function)
def render_enhanced_chat_with_modern_ui():
    """Enhanced chat with modern chatbot UI"""
    st.markdown("### 💬 AI Medical Consultation")
    
    # Language selection
    language = st.selectbox(
        "Select Language:",
        ["English", "Bengali"],
        key="chatbot_language"
    )
    
    # Create complete chatbot interface
    create_complete_chatbot_interface(language)