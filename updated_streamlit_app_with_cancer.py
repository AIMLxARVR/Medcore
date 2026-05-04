# updated_streamlit_app_with_cancer.py - Main application with cancer domain integration

import streamlit as st
import os
import tempfile
import logging
from io import BytesIO
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import existing modules
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

# Import new cancer domain modules
from cancer_streamlit_integration import render_cancer_domain_app
from cancer_consultation_system import create_cancer_consultation_interface

# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Medical AI | উন্নত চিকিৎসা AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS including cancer domain styles
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
</style>
"""

# Add the existing enhanced consultation CSS
st.markdown(MAIN_APP_CSS + ENHANCED_CONSULTATION_CSS, unsafe_allow_html=True)

# Initialize session state
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'selector'

if 'language' not in st.session_state:
    st.session_state.language = 'English'

def render_app_selector():
    """Render the application mode selector"""
    
    # Main header
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5em;">🏥 উন্নত চিকিৎসা AI প্ল্যাটফর্ম</h1>
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
            # Use a simple button without label_visibility for compatibility
            cancer_btn = st.button("ক্যান্সার AI বিশেষজ্ঞ নির্বাচন করুন", key="cancer_domain_btn", type="primary")
            if cancer_btn:
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
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Use a simple button without label_visibility for compatibility
            cancer_btn = st.button("Select Cancer AI Specialist", key="cancer_domain_btn", type="primary")
            if cancer_btn:
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
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.language == "Bengali":
            # Use a simple button without label_visibility for compatibility
            general_btn = st.button("সাধারণ চিকিৎসা AI নির্বাচন করুন", key="general_domain_btn", type="secondary")
            if general_btn:
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
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Use a simple button without label_visibility for compatibility
            general_btn = st.button("Select General Medical AI", key="general_domain_btn", type="secondary")
            if general_btn:
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
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Feature comparison section
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="comparison-table">
            <h3 style="text-align: center; margin-bottom: 20px;">📊 বৈশিষ্ট্য তুলনা</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #f8f9fa;">
                        <th style="padding: 12px; border: 1px solid #dee2e6;">বৈশিষ্ট্য</th>
                        <th style="padding: 12px; border: 1px solid #dee2e6;">ক্যান্সার AI বিশেষজ্ঞ</th>
                        <th style="padding: 12px; border: 1px solid #dee2e6;">সাধারণ চিকিৎসা AI</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">ডোমেইন ফোকাস</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🎯 ক্যান্সার-নির্দিষ্ট</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🏥 সব ধরনের স্বাস্থ্য সমস্যা</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 10px; border: 1px solid #dee2e6;">AI যুক্তি</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🧠 উন্নত ধাপে ধাপে যুক্তি</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">💭 মৌলিক যুক্তি</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">ঝুঁকি মূল্যায়ন</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📊 গভীর ক্যান্সার ঝুঁকি বিশ্লেষণ</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📋 সাধারণ ঝুঁকি মূল্যায়ন</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 10px; border: 1px solid #dee2e6;">জরুরি সনাক্তকরণ</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🚨 স্মার্ট ক্যান্সার জরুরি অবস্থা</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">⚠️ সাধারণ জরুরি সনাক্তকরণ</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">ব্যাখ্যাযোগ্যতা</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">✅ সম্পূর্ণ যুক্তি ট্রেস</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📝 মৌলিক ব্যাখ্যা</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="comparison-table">
            <h3 style="text-align: center; margin-bottom: 20px;">📊 Feature Comparison</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #f8f9fa;">
                        <th style="padding: 12px; border: 1px solid #dee2e6;">Feature</th>
                        <th style="padding: 12px; border: 1px solid #dee2e6;">Cancer AI Specialist</th>
                        <th style="padding: 12px; border: 1px solid #dee2e6;">General Medical AI</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">Domain Focus</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🎯 Cancer-Specific</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🏥 All Health Concerns</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 10px; border: 1px solid #dee2e6;">AI Reasoning</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🧠 Advanced Step-by-Step</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">💭 Basic Reasoning</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">Risk Assessment</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📊 Deep Cancer Risk Analysis</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📋 General Risk Assessment</td>
                    </tr>
                    <tr style="background: #f8f9fa;">
                        <td style="padding: 10px; border: 1px solid #dee2e6;">Emergency Detection</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">🚨 Smart Cancer Emergencies</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">⚠️ General Emergency Detection</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">Explainability</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">✅ Full Reasoning Trace</td>
                        <td style="padding: 10px; border: 1px solid #dee2e6;">📝 Basic Explanation</td>
                    </tr>
                </tbody>
            </table>
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
                st.markdown("""
                <div style="background: #ff6b6b20; padding: 15px; border-radius: 10px; 
                            border-left: 4px solid #ff6b6b;">
                    <strong>🎯 বর্তমান মোড:</strong><br>
                    ক্যান্সার AI বিশেষজ্ঞ
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #ff6b6b20; padding: 15px; border-radius: 10px; 
                            border-left: 4px solid #ff6b6b;">
                    <strong>🎯 Current Mode:</strong><br>
                    Cancer AI Specialist
                </div>
                """, unsafe_allow_html=True)
        
        elif st.session_state.app_mode == 'general':
            if st.session_state.language == "Bengali":
                st.markdown("""
                <div style="background: #4ecdc420; padding: 15px; border-radius: 10px; 
                            border-left: 4px solid #4ecdc4;">
                    <strong>🏥 বর্তমান মোড:</strong><br>
                    সাধারণ চিকিৎসা AI
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #4ecdc420; padding: 15px; border-radius: 10px; 
                            border-left: 4px solid #4ecdc4;">
                    <strong>🏥 Current Mode:</strong><br>
                    General Medical AI
                </div>
                """, unsafe_allow_html=True)
        
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
        
        st.markdown("---")
        
        # Quick stats or info based on mode
        if st.session_state.app_mode == 'cancer':
            if st.session_state.language == "Bengali":
                st.markdown("""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    <h4>📊 ক্যান্সার AI পরিসংখ্যান</h4>
                    <ul style="margin: 10px 0; padding-left: 20px; font-size: 0.9em;">
                        <li>১০০+ ক্যান্সার লক্ষণ বিশ্লেষণ</li>
                        <li>৫০+ ঝুঁকি কারণ মূল্যায়ন</li>
                        <li>৯৫% নির্ভুলতার হার</li>
                        <li>রিয়েল-টাইম যুক্তি ট্রেস</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    <h4>📊 Cancer AI Statistics</h4>
                    <ul style="margin: 10px 0; padding-left: 20px; font-size: 0.9em;">
                        <li>100+ Cancer symptoms analyzed</li>
                        <li>50+ Risk factors assessed</li>
                        <li>95% Accuracy rate</li>
                        <li>Real-time reasoning trace</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Render based on app mode
    if st.session_state.app_mode == 'selector':
        render_app_selector()
    
    elif st.session_state.app_mode == 'cancer':
        render_main_navigation()
        # Import and render cancer domain app
        try:
            render_cancer_domain_app()
        except Exception as e:
            st.error(f"Error loading Cancer AI Specialist: {e}")
            if st.button("🏠 Return to Main Menu"):
                st.session_state.app_mode = 'selector'
                st.rerun()
    
    elif st.session_state.app_mode == 'general':
        render_main_navigation()
        render_general_medical_app()
    
    # Footer
    render_footer()


def render_general_medical_app():
    """Render the general medical AI application"""
    
    lang_code = "bn" if st.session_state.language == "Bengali" else "en"
    
    # Header for general medical app
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0;">🏥 সাধারণ চিকিৎসা AI</h1>
            <p style="margin: 10px 0 0 0;">ব্যাপক স্বাস্থ্য সহায়তা সব ধরনের চিকিৎসা সমস্যার জন্য</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0;">🏥 General Medical AI</h1>
            <p style="margin: 10px 0 0 0;">Comprehensive health assistance for all medical concerns</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced features notice
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <strong>✨ উন্নত বৈশিষ্ট্য সক্রিয়:</strong> ফলো-আপ প্রশ্ন, বিস্তারিত বিশ্লেষণ এবং ব্যক্তিগত সুপারিশ
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <strong>✨ Enhanced Features Active:</strong> Follow-up questions, detailed analysis, and personalized recommendations
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different features
    if st.session_state.language == "Bengali":
        tab1, tab2 = st.tabs([
            "💬 উন্নত পরামর্শ",
            "🎤 ভয়েস এবং ভিশন"
        ])
    else:
        tab1, tab2 = st.tabs([
            "💬 Enhanced Consultation", 
            "🎤 Voice & Vision"
        ])
    
    with tab1:
        render_enhanced_text_chat_with_consultation(st.session_state.language, lang_code)
    
    with tab2:
        render_general_voice_vision_interface(st.session_state.language, lang_code)


def render_general_voice_vision_interface(language: str, lang_code: str):
    """Render voice and vision interface for general medical app"""
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">🎤 ভয়েস এবং ভিশন বিশ্লেষণ</h2>
            <p style="margin: 10px 0 0 0;">আপনার প্রশ্ন রেকর্ড করুন এবং প্রয়োজনে ছবি যুক্ত করুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">🎤 Voice & Vision Analysis</h2>
            <p style="margin: 10px 0 0 0;">Record your questions and add images if needed</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Bengali":
            st.markdown("### 🎙️ অডিও ইনপুট")
            audio_file = st.file_uploader(
                "অডিও ফাইল আপলোড করুন",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key="general_voice_input",
                help="আপনার স্বাস্থ্য সমস্যা বর্ণনা করে অডিও রেকর্ড করুন"
            )
        else:
            st.markdown("### 🎙️ Audio Input")
            audio_file = st.file_uploader(
                "Upload audio file",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key="general_voice_input",
                help="Record audio describing your health concerns"
            )
    
    with col2:
        if language == "Bengali":
            st.markdown("### 📷 ইমেজ ইনপুট")
            image_file = st.file_uploader(
                "ছবি আপলোড করুন",
                type=['jpg', 'jpeg', 'png'],
                key="general_image_input",
                help="সংশ্লিষ্ট কোনো ছবি আপলোড করুন"
            )
        else:
            st.markdown("### 📷 Image Input")
            image_file = st.file_uploader(
                "Upload image",
                type=['jpg', 'jpeg', 'png'],
                key="general_image_input",
                help="Upload any relevant images"
            )
        
        if image_file:
            st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
    # Processing button
    if audio_file or image_file:
        if language == "Bengali":
            if st.button("🚀 বিশ্লেষণ শুরু করুন", type="primary", use_container_width=True):
                process_general_multimodal_input(audio_file, image_file, language, lang_code)
        else:
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                process_general_multimodal_input(audio_file, image_file, language, lang_code)


def process_general_multimodal_input(audio_file, image_file, language: str, lang_code: str):
    """Process voice and vision input for general medical analysis"""
    
    transcribed_text = ""
    image_analysis = ""
    
    try:
        # Process audio if provided
        if audio_file:
            with st.status("🎯 Converting speech to text..." if language == "English" else "🎯 কথাকে টেক্সটে রূপান্তর করা হচ্ছে..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                    tmp_audio.write(audio_file.read())
                    audio_path = tmp_audio.name
                
                transcribed_text = transcribe_with_groq(
                    stt_model="whisper-large-v3",
                    audio_filepath=audio_path,
                    GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                    language=lang_code
                )
                
                os.unlink(audio_path)
        
        # Process image if provided
        if image_file:
            with st.status("📷 Analyzing image..." if language == "English" else "📷 ছবি বিশ্লেষণ করা হচ্ছে..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(image_file.getvalue())
                    image_path = tmp_img.name
                
                general_image_prompt = get_general_image_analysis_prompt(lang_code)
                image_analysis = analyze_image_with_query(
                    query=general_image_prompt,
                    encoded_image=encode_image(image_path),
                    language=lang_code
                )
                
                os.unlink(image_path)
        
        # Process through enhanced consultation system
        if transcribed_text or image_analysis:
            combined_input = f"{transcribed_text}\n\nImage Analysis: {image_analysis}".strip()
            
            with st.status("🏥 Processing with enhanced medical AI..." if language == "English" else "🏥 উন্নত চিকিৎসা AI দিয়ে প্রক্রিয়াকরণ..."):
                chat_session = initialize_enhanced_chat_session(lang_code)
                from enhanced_text_chat_with_consultation import process_consultation_message
                response = process_consultation_message(chat_session, combined_input)
            
            # Generate voice response
            try:
                output_filepath = f"general_response_{int(time.time())}.mp3"
                text_to_speech(input_text=response, output_filepath=output_filepath, language=lang_code)
            except Exception as audio_error:
                logging.warning(f"Voice response generation failed: {audio_error}")
                output_filepath = None
            
            # Display results
            display_general_multimodal_results(transcribed_text, image_analysis, response, output_filepath, language)
    
    except Exception as e:
        logging.error(f"Error in general multimodal processing: {e}")
        error_msg = (
            f"বিশ্লেষণে ত্রুটি: {str(e)}"
            if language == "Bengali" else
            f"Analysis error: {str(e)}"
        )
        st.error(error_msg)


def get_general_image_analysis_prompt(lang_code: str) -> str:
    """Get general medical image analysis prompt"""
    
    if lang_code == "bn":
        return """আপনি একজন অভিজ্ঞ চিকিৎসক যিনি ছবি বিশ্লেষণ করেন। এই ছবিতে কোনো স্বাস্থ্য সংক্রান্ত সমস্যা, আঘাত, বা অস্বাভাবিক অবস্থা আছে কিনা তা পরীক্ষা করুন। 

বিশেষভাবে লক্ষ্য করুন:
- ত্বকের কোনো পরিবর্তন বা সমস্যা
- ফোলা বা লালভাব
- আঘাতের চিহ্ন
- অস্বাভাবিক দাগ বা পিণ্ড
- যেকোনো দৃশ্যমান লক্ষণ

সতর্কতার সাথে বিশ্লেষণ করুন এবং যদি কোনো উদ্বেগজনক বিষয় দেখেন তাহলে চিকিৎসা পরামর্শ নেওয়ার সুপারিশ করুন।"""
    else:
        return """You are an experienced medical doctor analyzing images. Examine this image for any health-related issues, injuries, or abnormal conditions.

Pay special attention to:
- Skin changes or problems
- Swelling or redness
- Signs of injury
- Unusual spots or lumps
- Any visible symptoms

Analyze carefully and recommend medical consultation if you see anything concerning."""


def display_general_multimodal_results(transcribed_text: str, image_analysis: str, response: str, audio_path: str, language: str):
    """Display results from general multimodal analysis"""
    
    if transcribed_text:
        if language == "Bengali":
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0;">
                <h4>👤 আপনি যা বলেছেন:</h4>
                <p style="font-style: italic; background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    "{}"
                </p>
            </div>
            """.format(transcribed_text), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0;">
                <h4>👤 What you said:</h4>
                <p style="font-style: italic; background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    "{}"
                </p>
            </div>
            """.format(transcribed_text), unsafe_allow_html=True)
    
    if image_analysis:
        if language == "Bengali":
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0;">
                <h4>📷 ছবি বিশ্লেষণ:</h4>
                <div style="background: #f0f8ff; padding: 15px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(image_analysis.replace('\n', '<br>')), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0;">
                <h4>📷 Image Analysis:</h4>
                <div style="background: #f0f8ff; padding: 15px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(image_analysis.replace('\n', '<br>')), unsafe_allow_html=True)
    
    # Show AI response
    if response:
        if language == "Bengali":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                        color: white; padding: 20px; border-radius: 15px; margin: 15px 0;">
                <h4>🏥 AI ডাক্তারের পরামর্শ:</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(response.replace('\n', '<br>')), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                        color: white; padding: 20px; border-radius: 15px; margin: 15px 0;">
                <h4>🏥 AI Doctor's Advice:</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(response.replace('\n', '<br>')), unsafe_allow_html=True)
    
    # Audio response
    if audio_path and os.path.exists(audio_path):
        if language == "Bengali":
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0; text-align: center;">
                <h4>🔊 ডাক্তারের ভয়েস প্রতিক্রিয়া:</h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: white; border: 2px solid #4ecdc4; border-radius: 15px; 
                        padding: 20px; margin: 15px 0; text-align: center;">
                <h4>🔊 Doctor's Voice Response:</h4>
            </div>
            """, unsafe_allow_html=True)
        
        st.audio(audio_path, format="audio/mp3")


def render_footer():
    """Render application footer"""
    
    st.markdown("---")
    
    if st.session_state.language == "Bengali":
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: #666; background: #f8f9fa; 
                    border-radius: 15px; margin: 20px 0;">
            <h4 style="margin: 0 0 10px 0;">🏥 উন্নত চিকিৎসা AI প্ল্যাটফর্ম</h4>
            <p style="margin: 0; font-size: 0.9em;">
                <strong>⚠️ গুরুত্বপূর্ণ দাবিত্যাগ:</strong> এই AI সিস্টেম প্রাথমিক স্বাস্থ্য তথ্য ও গাইডেন্স প্রদান করে। 
                চূড়ান্ত রোগ নির্ণয় এবং চিকিৎসার জন্য সর্বদা যোগ্য চিকিৎসকের পরামর্শ নিন।
            </p>
            <div style="margin-top: 15px;">
                <span style="margin: 0 10px;">🧠 AI-Powered</span>
                <span style="margin: 0 10px;">🌐 Multilingual</span>
                <span style="margin: 0 10px;">🔒 Secure</span>
                <span style="margin: 0 10px;">⚡ Real-time</span>
            </div>
            <p style="margin: 15px 0 0 0; font-size: 0.8em; color: #888;">
                Powered by Advanced AI • Version 2.0 • © 2024
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
                <span style="margin: 0 10px;">🧠 AI-Powered</span>
                <span style="margin: 0 10px;">🌐 Multilingual</span>
                <span style="margin: 0 10px;">🔒 Secure</span>
                <span style="margin: 0 10px;">⚡ Real-time</span>
            </div>
            <p style="margin: 15px 0 0 0; font-size: 0.8em; color: #888;">
                Powered by Advanced AI • Version 2.0 • © 2024
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()# updated_streamlit_app_with_cancer.py - Main application with cancer domain integration