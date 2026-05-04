# updated_cancer_streamlit_integration.py - Integration with enhanced user-friendly consultation

import streamlit as st
import os
import tempfile
import logging
from datetime import datetime
import json

# Import the enhanced cancer consultation modules
from enhanced_cancer_consultation_system import (
    create_enhanced_cancer_consultation_interface,
    EnhancedCancerConsultationSession
)
from cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel

# Import existing modules for compatibility
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def render_enhanced_cancer_domain_app():
    """Main function to render the enhanced cancer domain app"""
    
    # Custom CSS for enhanced cancer domain
    st.markdown("""
    <style>
    /* Enhanced cancer domain specific styling */
    .cancer-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        text-align: center;
    }
    
    .questionnaire-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.3);
    }
    
    .question-card {
        background: white;
        border: 2px solid #ff6b6b;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
        border-left: 6px solid #ff6b6b;
    }
    
    .progress-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    
    .results-summary {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
    }
    
    .risk-indicator-low {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .risk-indicator-moderate {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .risk-indicator-high {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .recommendation-card {
        background: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0;
    }
    
    .emergency-alert {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        color: #c62828;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #f44336;
        box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3); }
        50% { box-shadow: 0 6px 16px rgba(244, 67, 54, 0.5); }
        100% { box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3); }
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        color: #2e7d32;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 4px solid #4caf50;
    }
    
    .ai-reasoning-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling for questionnaire */
    .stRadio > div {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        border-color: #ff6b6b;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border: 2px solid #ff6b6b;
        border-radius: 10px;
        font-size: 16px;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Language selection
    if 'enhanced_cancer_app_language' not in st.session_state:
        st.session_state.enhanced_cancer_app_language = 'English'
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("""
        <div class="cancer-header" style="padding: 15px; margin-bottom: 15px;">
            <h3 style="margin: 0;">⚙️ Enhanced Cancer AI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selector
        language_options = ["English", "Bengali"]
        selected_language = st.radio(
            "🌐 Language / ভাষা",
            language_options,
            index=0 if st.session_state.enhanced_cancer_app_language == "English" else 1,
            key="enhanced_cancer_language_selector"
        )
        
        if selected_language != st.session_state.enhanced_cancer_app_language:
            st.session_state.enhanced_cancer_app_language = selected_language
            st.rerun()
        
        st.markdown("---")
        
        # Feature description
        if selected_language == "Bengali":
            st.markdown("""
            <div style="background: #e8f5e8; padding: 15px; border-radius: 10px;">
                <h4>🎯 নতুন বৈশিষ্ট্য</h4>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>🎯 সহজ হ্যাঁ/না প্রশ্ন</li>
                    <li>📊 মাল্টিপল চয়েস প্রশ্ন</li>
                    <li>⏱️ দ্রুত পরামর্শ</li>
                    <li>🧠 স্মার্ট বিশ্লেষণ</li>
                    <li>📋 ব্যক্তিগত সুপারিশ</li>
                    <li>🚨 জরুরি সনাক্তকরণ</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #e8f5e8; padding: 15px; border-radius: 10px;">
                <h4>🎯 New Features</h4>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>🎯 Simple Yes/No questions</li>
                    <li>📊 Multiple choice questions</li>
                    <li>⏱️ Quick consultation</li>
                    <li>🧠 Smart analysis</li>
                    <li>📋 Personalized recommendations</li>
                    <li>🚨 Emergency detection</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistics
        if selected_language == "Bengali":
            st.markdown("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                <h4>📊 পরিসংখ্যান</h4>
                <ul style="margin: 10px 0; padding-left: 20px; font-size: 0.9em;">
                    <li>১৮টি স্মার্ট প্রশ্ন</li>
                    <li>৫-১০ মিনিট সময়</li>
                    <li>৯৫%+ নির্ভুলতা</li>
                    <li>তাৎক্ষণিক ফলাফল</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                <h4>📊 Statistics</h4>
                <ul style="margin: 10px 0; padding-left: 20px; font-size: 0.9em;">
                    <li>18 Smart questions</li>
                    <li>5-10 minutes duration</li>
                    <li>95%+ accuracy</li>
                    <li>Instant results</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Main app header
    if selected_language == "Bengali":
        st.markdown("""
        <div class="cancer-header">
            <h1 style="margin: 0; font-size: 2.5em;">🎯 উন্নত ক্যান্সার AI বিশেষজ্ঞ</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
                ব্যবহারকারী-বান্ধব প্রশ্নোত্তর সহ স্মার্ট ক্যান্সার ঝুঁকি মূল্যায়ন
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="cancer-header">
            <h1 style="margin: 0; font-size: 2.5em;">🎯 Enhanced AI Cancer Specialist</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">
                Smart cancer risk assessment with user-friendly questionnaire
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature highlights
    if selected_language == "Bengali":
        st.markdown("""
        <div class="feature-highlight">
            <h3 style="margin: 0 0 15px 0;">🌟 নতুন ও উন্নত বৈশিষ্ট্য</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">🎯</div>
                    <div><strong>সহজ প্রশ্ন</strong></div>
                    <div style="font-size: 0.9em;">হ্যাঁ/না প্রশ্ন</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">⏱️</div>
                    <div><strong>দ্রুত</strong></div>
                    <div style="font-size: 0.9em;">৫-১০ মিনিট</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">🧠</div>
                    <div><strong>স্মার্ট AI</strong></div>
                    <div style="font-size: 0.9em;">উন্নত বিশ্লেষণ</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">📋</div>
                    <div><strong>ব্যক্তিগত</strong></div>
                    <div style="font-size: 0.9em;">কাস্টম সুপারিশ</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-highlight">
            <h3 style="margin: 0 0 15px 0;">🌟 New & Enhanced Features</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">🎯</div>
                    <div><strong>Simple Questions</strong></div>
                    <div style="font-size: 0.9em;">Yes/No format</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">⏱️</div>
                    <div><strong>Quick</strong></div>
                    <div style="font-size: 0.9em;">5-10 minutes</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">🧠</div>
                    <div><strong>Smart AI</strong></div>
                    <div style="font-size: 0.9em;">Advanced analysis</div>
                </div>
                <div style="text-align: center; margin: 10px;">
                    <div style="font-size: 2em;">📋</div>
                    <div><strong>Personal</strong></div>
                    <div style="font-size: 0.9em;">Custom recommendations</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main application tabs
    if selected_language == "Bengali":
        tab1, tab2, tab3= st.tabs([
            "🎯 স্মার্ট পরামর্শ",
            "🎤 ভয়েস + ভিশন", 
            "📊 দ্রুত ঝুঁকি চেক",
        ])
    else:
        tab1, tab2, tab3 = st.tabs([
            "🎯 Smart Consultation",
            "🎤 Voice + Vision",
            "📊 Risk Check", 
        ])
    
    # Tab 1: Enhanced Cancer Consultation
    with tab1:
        create_enhanced_cancer_consultation_interface(selected_language)
    
    # Tab 2: Voice + Vision Cancer Analysis
    with tab2:
        render_enhanced_cancer_voice_vision_interface(selected_language)
    
    # Tab 3: Quick Risk Calculator
    with tab3:
        render_quick_risk_assessment(selected_language)
    
    # # Tab 4: AI Reasoning Viewer
    # with tab4:
    #     render_enhanced_reasoning_viewer(selected_language)


def render_enhanced_cancer_voice_vision_interface(language: str):
    """Render enhanced voice and vision interface for cancer domain"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    if language == "Bengali":
        st.markdown("""
        <div class="questionnaire-card">
            <h2 style="margin: 0;">🎤 ক্যান্সার-নির্দিষ্ট ভয়েস এবং ইমেজ বিশ্লেষণ</h2>
            <p style="margin: 10px 0 0 0;">আপনার উপসর্গ বর্ণনা করুন এবং প্রয়োজনে ছবি যুক্ত করুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="questionnaire-card">
            <h2 style="margin: 0;">🎤 Cancer-Specific Voice and Image Analysis</h2>
            <p style="margin: 10px 0 0 0;">Describe your symptoms and add images if needed</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Bengali":
            st.markdown("### 🎙️ অডিও ইনপুট")
            audio_file = st.file_uploader(
                "অডিও ফাইল আপলোড করুন",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key="enhanced_cancer_voice_input",
                help="আপনার উপসর্গ বর্ণনা করে অডিও রেকর্ড করুন"
            )
        else:
            st.markdown("### 🎙️ Audio Input")
            audio_file = st.file_uploader(
                "Upload audio file",
                type=['wav', 'mp3', 'ogg', 'm4a'],
                key="enhanced_cancer_voice_input",
                help="Record audio describing your symptoms"
            )
    
    with col2:
        if language == "Bengali":
            st.markdown("### 📷 ইমেজ ইনপুট")
            image_file = st.file_uploader(
                "ছবি আপলোড করুন",
                type=['jpg', 'jpeg', 'png'],
                key="enhanced_cancer_image_input",
                help="সংশ্লিষ্ট কোনো ছবি আপলোড করুন"
            )
        else:
            st.markdown("### 📷 Image Input")
            image_file = st.file_uploader(
                "Upload image",
                type=['jpg', 'jpeg', 'png'],
                key="enhanced_cancer_image_input",
                help="Upload any relevant images"
            )
        
        if image_file:
            st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
    # Processing section
    if audio_file or image_file:
        if language == "Bengali":
            if st.button("🚀 উন্নত ক্যান্সার বিশ্লেষণ শুরু করুন", type="primary", use_container_width=True):
                process_enhanced_cancer_multimodal_input(audio_file, image_file, language)
        else:
            if st.button("🚀 Start Enhanced Cancer Analysis", type="primary", use_container_width=True):
                process_enhanced_cancer_multimodal_input(audio_file, image_file, language)


def render_quick_risk_assessment(language: str):
    """Render the original advanced cancer risk calculator with detailed factor analysis"""
    
    if language == "Bengali":
        st.markdown("""
        <div class="ai-reasoning-card">
            <h2 style="margin: 0;">📊 উন্নত ক্যান্সার ঝুঁকি ক্যালকুলেটর</h2>
            <p style="margin: 10px 0 0 0;">আপনার ব্যক্তিগত ঝুঁকি কারণ বিশ্লেষণ করুন এবং বিস্তারিত মূল্যায়ন পান</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ai-reasoning-card">
            <h2 style="margin: 0;">📊 Advanced Cancer Risk Calculator</h2>
            <p style="margin: 10px 0 0 0;">Analyze your personal risk factors and get detailed assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk factor inputs - THESE ARE THE DYNAMIC INPUTS
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Bengali":
            st.markdown("### 👤 ব্যক্তিগত তথ্য")
            age = st.slider("বয়স", 18, 100, 40, key="cancer_risk_age_slider")
            gender = st.selectbox("লিঙ্গ", ["পুরুষ", "মহিলা", "অন্যান্য"], key="cancer_risk_gender_select")
            smoking = st.selectbox("ধূমপানের অবস্থা", ["কখনো করিনি", "অতীতে করেছি", "বর্তমানে করি"], key="cancer_risk_smoking_select")
            alcohol = st.selectbox("মদ্যপানের অভ্যাস", ["না", "মাঝে মাঝে", "নিয়মিত", "অতিরিক্ত"], key="cancer_risk_alcohol_select")
        else:
            st.markdown("### 👤 Personal Information")
            age = st.slider("Age", 18, 100, 40, key="cancer_risk_age_slider")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="cancer_risk_gender_select")
            smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"], key="cancer_risk_smoking_select")
            alcohol = st.selectbox("Alcohol Consumption", ["None", "Occasional", "Regular", "Heavy"], key="cancer_risk_alcohol_select")
    
    with col2:
        if language == "Bengali":
            st.markdown("### 🧬 ঝুঁকি কারণসমূহ")
            family_history = st.multiselect("পারিবারিক ক্যান্সারের ইতিহাস", 
                                          ["স্তন ক্যান্সার", "ফুসফুস ক্যান্সার", "কোলোরেক্টাল ক্যান্সার", "প্রোস্টেট ক্যান্সার"],
                                          key="cancer_risk_family_history_select")
            diet_quality = st.selectbox("খাদ্যের মান", ["খুব ভাল", "ভাল", "গড়", "খারাপ"], key="cancer_risk_diet_select")
            exercise = st.selectbox("ব্যায়ামের অভ্যাস", ["নিয়মিত", "মাঝে মাঝে", "কদাচিৎ", "না"], key="cancer_risk_exercise_select")
            sun_exposure = st.selectbox("রোদে থাকার পরিমাণ", ["কম", "মধ্যম", "বেশি", "অতিরিক্ত"], key="cancer_risk_sun_select")
        else:
            st.markdown("### 🧬 Risk Factors")
            family_history = st.multiselect("Family Cancer History", 
                                          ["Breast Cancer", "Lung Cancer", "Colorectal Cancer", "Prostate Cancer"],
                                          key="cancer_risk_family_history_select")
            diet_quality = st.selectbox("Diet Quality", ["Excellent", "Good", "Average", "Poor"], key="cancer_risk_diet_select")
            exercise = st.selectbox("Exercise Habits", ["Regular", "Occasional", "Rare", "None"], key="cancer_risk_exercise_select")
            sun_exposure = st.selectbox("Sun Exposure", ["Low", "Moderate", "High", "Excessive"], key="cancer_risk_sun_select")
    
    # Calculate risk button
    if language == "Bengali":
        if st.button("🧮 বিস্তারিত ঝুঁকি বিশ্লেষণ করুন", type="primary", use_container_width=True, key="cancer_risk_calculate_btn"):
            calculate_and_display_cancer_risk(age, gender, smoking, alcohol, family_history, 
                                            diet_quality, exercise, sun_exposure, language, True)
    else:
        if st.button("🧮 Calculate Detailed Risk Analysis", type="primary", use_container_width=True, key="cancer_risk_calculate_btn"):
            calculate_and_display_cancer_risk(age, gender, smoking, alcohol, family_history, 
                                            diet_quality, exercise, sun_exposure, language, True)


def calculate_and_display_cancer_risk(age, gender, smoking, alcohol, family_history, diet_quality, exercise, sun_exposure, language, risk_visualization):
    """Calculate and display cancer risk assessment with detailed factor analysis using DYNAMIC user inputs"""
    
    # Initialize reasoning engine
    lang_code = "bn" if language == "Bengali" else "en"
    reasoning_engine = CancerReasoningEngine(lang_code)
    
    # Convert DYNAMIC inputs to risk factors format - THIS IS THE KEY FIX
    patient_data = {
        "age": age,  # Using actual slider value
        "gender": convert_gender_input(gender, language),  # Convert properly
        "smoking": convert_smoking_input(smoking, language),  # Convert properly
        "heavy_drinking": convert_alcohol_input(alcohol, language),  # Convert properly
        "family_history_cancer": len(family_history) > 0,  # Based on actual selection
        "poor_diet": convert_diet_input(diet_quality, language),  # Convert properly
        "no_exercise": convert_exercise_input(exercise, language),  # Convert properly
        "excessive_sun_exposure": convert_sun_input(sun_exposure, language)  # Convert properly
    }
    
    # Run risk assessment with DYNAMIC data
    with st.spinner("Calculating risk..." if language == "English" else "ঝুঁকি গণনা করা হচ্ছে..."):
        risk_assessment = reasoning_engine.assess_risk_factors(patient_data)
    
    # Display enhanced risk analysis with DYNAMIC inputs
    display_enhanced_risk_analysis(age, gender, smoking, alcohol, family_history, 
                                 diet_quality, exercise, sun_exposure, 
                                 risk_assessment, language, risk_visualization)
    
    # Show detailed risk breakdown
    display_detailed_risk_breakdown(risk_assessment, reasoning_engine, language)


# Helper functions to convert user inputs properly
def convert_gender_input(gender, language):
    """Convert gender input to standard format"""
    if language == "Bengali":
        return "male" if gender == "পুরুষ" else "female" if gender == "মহিলা" else "other"
    else:
        return gender.lower()

def convert_smoking_input(smoking, language):
    """Convert smoking input to boolean"""
    if language == "Bengali":
        return smoking == "বর্তমানে করি"
    else:
        return smoking == "Current"

def convert_alcohol_input(alcohol, language):
    """Convert alcohol input to boolean for heavy drinking"""
    if language == "Bengali":
        return alcohol == "অতিরিক্ত"
    else:
        return alcohol == "Heavy"

def convert_diet_input(diet_quality, language):
    """Convert diet input to boolean for poor diet"""
    if language == "Bengali":
        return diet_quality == "খারাপ"
    else:
        return diet_quality == "Poor"

def convert_exercise_input(exercise, language):
    """Convert exercise input to boolean for no exercise"""
    if language == "Bengali":
        return exercise == "না"
    else:
        return exercise == "None"

def convert_sun_input(sun_exposure, language):
    """Convert sun exposure input to boolean for excessive exposure"""
    if language == "Bengali":
        return sun_exposure == "অতিরিক্ত"
    else:
        return sun_exposure == "Excessive"

def display_enhanced_risk_analysis(age, gender, smoking, alcohol, family_history, diet_quality, exercise, sun_exposure, risk_assessment, language, risk_visualization):
    """Display comprehensive factor-by-factor risk analysis with PROPER TABLE RENDERING"""
    
    if language == "Bengali":
        st.markdown("## 🧠 **ঝুঁকি মূল্যায়ন বিশ্লেষণ**")
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1976d2;">🧠 ঝুঁকি মূল্যায়ন পদ্ধতি</h4>
            <p style="margin: 5px 0;">প্রতিটি কারণ এভাবে মূল্যায়ন করা হয়:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li><strong>সুরক্ষামূলক (↓ ঝুঁকি কমায়)</strong>: যেমন ধূমপান না করা, নিয়মিত ব্যায়াম</li>
                <li><strong>নিরপেক্ষ (↔)</strong>: যেমন ৪০ বছর বয়স (মাঝারি পর্যায়)</li>
                <li><strong>ঝুঁকি বৃদ্ধিকারী (↑ ঝুঁকি বাড়ায়)</strong>: যেমন পারিবারিক ইতিহাস, অতিরিক্ত রোদ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("## 🧠 **Risk Assessment Analysis**")
        
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1976d2;">🧠 Risk Assessment Heuristics</h4>
            <p style="margin: 5px 0;">Each factor can be rated as:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li><strong>Protective (↓ Risk)</strong>: e.g., no smoking, regular exercise</li>
                <li><strong>Neutral (↔)</strong>: e.g., age 40 (moderate range)</li>
                <li><strong>Risk-enhancing (↑ Risk)</strong>: e.g., family history, high sun exposure</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Factor-by-factor analysis using DYNAMIC inputs
    if language == "Bengali":
        st.markdown("### 🔍 **কারণ-ভিত্তিক বিশ্লেষণ:**")
    else:
        st.markdown("### 🔍 **Factor-by-Factor Analysis:**")
    
    # Create analysis table with DYNAMIC data
    factors_analysis = analyze_individual_factors(age, gender, smoking, alcohol, family_history, 
                                                diet_quality, exercise, sun_exposure, language)
    
    # Display analysis table with PROPER rendering
    display_factors_table_streamlit(factors_analysis, language)
    
    # Calculate overall risk level
    overall_risk = calculate_overall_risk_level(factors_analysis)
    
    # Display final evaluation
    display_final_risk_evaluation(overall_risk, factors_analysis, language)
    
    # Show traditional risk visualization if enabled
    if risk_visualization:
        st.markdown("---")
        display_risk_visualization(risk_assessment, language)

def display_factors_table_streamlit(factors_analysis, language):
    """Display the factors analysis using Streamlit's native table rendering - FIXES HTML TAG DISPLAY ISSUE"""
    
    # Prepare data for Streamlit table
    table_data = []
    
    for factor in factors_analysis:
        table_data.append({
            "Risk Symbol" if language == "English" else "ঝুঁকি": factor["symbol"],
            "Factor" if language == "English" else "কারণ": factor["factor"],
            "Risk Assessment" if language == "English" else "ঝুঁকি মূল্যায়ন": factor["note"]
        })
    
    # Display as Streamlit dataframe with custom styling
    import pandas as pd
    df = pd.DataFrame(table_data)
    
    # Apply conditional formatting based on risk levels
    def style_risk_row(row):
        factor_info = factors_analysis[row.name]
        risk_level = factor_info["risk_level"]
        
        if risk_level == "protective":
            return ['background-color: #e8f5e9'] * len(row)
        elif risk_level == "neutral":
            return ['background-color: #f5f5f5'] * len(row)
        elif risk_level == "mild_risk":
            return ['background-color: #fff3e0'] * len(row)
        elif risk_level in ["risk", "high_risk"]:
            return ['background-color: #ffebee'] * len(row)
        else:
            return [''] * len(row)
    
    # Display styled dataframe
    styled_df = df.style.apply(style_risk_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Add legend
    if language == "Bengali":
        st.markdown("""
        <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 10px;">
            <h5>চিহ্ন ব্যাখ্যা:</h5>
            <p><strong>↓</strong> = সুরক্ষামূলক (ঝুঁকি কমায়) | <strong>↔</strong> = নিরপেক্ষ | <strong>↗</strong> = সামান্য ঝুঁকি | <strong>↑</strong> = ঝুঁকি বৃদ্ধি | <strong>↑↑</strong> = উচ্চ ঝুঁকি</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 10px;">
            <h5>Symbol Legend:</h5>
            <p><strong>↓</strong> = Protective (reduces risk) | <strong>↔</strong> = Neutral | <strong>↗</strong> = Mild risk | <strong>↑</strong> = Risk increase | <strong>↑↑</strong> = High risk</p>
        </div>
        """, unsafe_allow_html=True)

def analyze_individual_factors(age, gender, smoking, alcohol, family_history, diet_quality, exercise, sun_exposure, language):
    """Analyze each risk factor individually using DYNAMIC inputs"""
    
    factors = []
    
    # Age analysis - USING DYNAMIC AGE
    if age < 30:
        age_risk = "protective"
        age_symbol = "↓"
        age_note = "Young age provides natural protection" if language == "English" else "অল্প বয়স প্রাকৃতিক সুরক্ষা প্রদান করে"
    elif age < 50:
        age_risk = "neutral"
        age_symbol = "↔"
        age_note = "Moderate risk starts to increase gradually" if language == "English" else "ঝুঁকি ধীরে ধীরে বাড়তে শুরু করে"
    elif age < 65:
        age_risk = "mild_risk"
        age_symbol = "↗"
        age_note = "Age-related risk becomes more significant" if language == "English" else "বয়স-সংক্রান্ত ঝুঁকি আরো গুরুত্বপূর্ণ হয়ে ওঠে"
    else:
        age_risk = "risk"
        age_symbol = "↑"
        age_note = "Higher age significantly increases cancer risk" if language == "English" else "বেশি বয়স ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে বাড়ায়"
    
    factors.append({
        "factor": f"Age {age}" if language == "English" else f"বয়স {age}",
        "risk_level": age_risk,
        "symbol": age_symbol,
        "note": age_note
    })
    
    # Continue with all other factors using DYNAMIC inputs...
    # Gender analysis - USING DYNAMIC GENDER
    if language == "English":
        gender_text = gender
        if gender.lower() == "male":
            gender_risk = "mild_risk"
            gender_symbol = "↗"
            gender_note = "Males generally have slightly higher incidence for several cancers"
        elif gender.lower() == "female":
            gender_risk = "neutral"
            gender_symbol = "↔"
            gender_note = "Gender-specific risks vary by cancer type"
        else:
            gender_risk = "neutral"
            gender_symbol = "↔"
            gender_note = "Gender-specific risk assessment requires individual evaluation"
    else:
        gender_text = gender
        if gender == "পুরুষ":
            gender_risk = "mild_risk"
            gender_symbol = "↗"
            gender_note = "পুরুষদের সাধারণত কয়েকটি ক্যান্সারের ঝুঁকি সামান্য বেশি"
        elif gender == "মহিলা":
            gender_risk = "neutral"
            gender_symbol = "↔"
            gender_note = "লিঙ্গ-নির্দিষ্ট ঝুঁকি ক্যান্সারের ধরন অনুযায়ী ভিন্ন"
        else:
            gender_risk = "neutral"
            gender_symbol = "↔"
            gender_note = "লিঙ্গ-নির্দিষ্ট ঝুঁকি মূল্যায়নে ব্যক্তিগত পর্যালোচনা প্রয়োজন"
    
    factors.append({
        "factor": f"Gender: {gender_text}" if language == "English" else f"লিঙ্গ: {gender_text}",
        "risk_level": gender_risk,
        "symbol": gender_symbol,
        "note": gender_note
    })
    
    # Smoking analysis - USING DYNAMIC SMOKING INPUT
    if language == "English":
        smoking_options = {"Never": "never", "Former": "former", "Current": "current"}
        smoking_key = smoking_options.get(smoking, "never")
        
        if smoking_key == "never":
            smoking_risk = "protective"
            smoking_symbol = "↓"
            smoking_note = "Major risk reducer. No smoking is one of the strongest protective factors"
        elif smoking_key == "former":
            smoking_risk = "mild_risk"
            smoking_symbol = "↗"
            smoking_note = "Former smoking still carries some residual risk, but much lower than current"
        else:
            smoking_risk = "high_risk"
            smoking_symbol = "↑↑"
            smoking_note = "Current smoking dramatically increases risk for multiple cancers"
    else:
        smoking_bn_options = {"কখনো করিনি": "never", "অতীতে করেছি": "former", "বর্তমানে করি": "current"}
        smoking_key = smoking_bn_options.get(smoking, "never")
        
        if smoking_key == "never":
            smoking_risk = "protective"
            smoking_symbol = "↓"
            smoking_note = "প্রধান ঝুঁকি হ্রাসকারী। ধূমপান না করা সবচেয়ে শক্তিশালী সুরক্ষামূলক কারণ"
        elif smoking_key == "former":
            smoking_risk = "mild_risk"
            smoking_symbol = "↗"
            smoking_note = "পূর্বের ধূমপানে এখনো কিছু ঝুঁকি থাকে, তবে বর্তমান ধূমপানের চেয়ে অনেক কম"
        else:
            smoking_risk = "high_risk"
            smoking_symbol = "↑↑"
            smoking_note = "বর্তমান ধূমপান একাধিক ক্যান্সারের ঝুঁকি নাটকীয়ভাবে বাড়ায়"
    
    factors.append({
        "factor": f"Smoking: {smoking}" if language == "English" else f"ধূমপান: {smoking}",
        "risk_level": smoking_risk,
        "symbol": smoking_symbol,
        "note": smoking_note
    })
    
    # Alcohol analysis - USING DYNAMIC ALCOHOL INPUT
    if language == "English":
        alcohol_options = {"None": "none", "Occasional": "occasional", "Regular": "regular", "Heavy": "heavy"}
        alcohol_key = alcohol_options.get(alcohol, "none")
        
        if alcohol_key == "none":
            alcohol_risk = "protective"
            alcohol_symbol = "↓"
            alcohol_note = "No alcohol consumption is protective against several cancers"
        elif alcohol_key == "occasional":
            alcohol_risk = "neutral"
            alcohol_symbol = "↔"
            alcohol_note = "Light drinking has minimal impact on cancer risk"
        elif alcohol_key == "regular":
            alcohol_risk = "mild_risk"
            alcohol_symbol = "↗"
            alcohol_note = "Regular consumption moderately increases risk"
        else:
            alcohol_risk = "risk"
            alcohol_symbol = "↑"
            alcohol_note = "Heavy drinking significantly increases risk for liver, breast, and other cancers"
    else:
        alcohol_bn_options = {"না": "none", "মাঝে মাঝে": "occasional", "নিয়মিত": "regular", "অতিরিক্ত": "heavy"}
        alcohol_key = alcohol_bn_options.get(alcohol, "none")
        
        if alcohol_key == "none":
            alcohol_risk = "protective"
            alcohol_symbol = "↓"
            alcohol_note = "মদ্যপান না করা কয়েকটি ক্যান্সারের বিরুদ্ধে সুরক্ষামূলক"
        elif alcohol_key == "occasional":
            alcohol_risk = "neutral"
            alcohol_symbol = "↔"
            alcohol_note = "হালকা মদ্যপানে ক্যান্সারের ঝুঁকিতে ন্যূনতম প্রভাব"
        elif alcohol_key == "regular":
            alcohol_risk = "mild_risk"
            alcohol_symbol = "↗"
            alcohol_note = "নিয়মিত সেবন মাঝারি মাত্রায় ঝুঁকি বাড়ায়"
        else:
            alcohol_risk = "risk"
            alcohol_symbol = "↑"
            alcohol_note = "অতিরিক্ত মদ্যপান লিভার, স্তন এবং অন্যান্য ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে বাড়ায়"
    
    factors.append({
        "factor": f"Alcohol: {alcohol}" if language == "English" else f"মদ্যপান: {alcohol}",
        "risk_level": alcohol_risk,
        "symbol": alcohol_symbol,
        "note": alcohol_note
    })
    
    # Family history analysis - USING DYNAMIC FAMILY HISTORY INPUT
    if len(family_history) == 0:
        fh_risk = "protective"
        fh_symbol = "↓"
        fh_note = "No inherited predisposition suspected" if language == "English" else "কোন বংশগত প্রবণতা সন্দেহ নেই"
    elif len(family_history) == 1:
        fh_risk = "mild_risk"
        fh_symbol = "↗"
        fh_note = f"One family cancer history increases vigilance for {family_history[0]}" if language == "English" else f"একটি পারিবারিক ক্যান্সার ইতিহাস {family_history[0]} এর জন্য সতর্কতা বাড়ায়"
    else:
        fh_risk = "risk"
        fh_symbol = "↑"
        fh_note = f"Multiple family cancers suggest possible genetic predisposition" if language == "English" else "একাধিক পারিবারিক ক্যান্সার সম্ভাব্য জেনেটিক প্রবণতা নির্দেশ করে"
    
    factors.append({
        "factor": f"Family History: {', '.join(family_history) if family_history else 'None'}" if language == "English" else f"পারিবারিক ইতিহাস: {', '.join(family_history) if family_history else 'নেই'}",
        "risk_level": fh_risk,
        "symbol": fh_symbol,
        "note": fh_note
    })
    
    # Diet analysis - USING DYNAMIC DIET INPUT
    if language == "English":
        diet_options = {"Excellent": "excellent", "Good": "good", "Average": "average", "Poor": "poor"}
        diet_key = diet_options.get(diet_quality, "average")
        
        if diet_key == "excellent":
            diet_risk = "protective"
            diet_symbol = "↓"
            diet_note = "Excellent diet strongly supports cancer prevention"
        elif diet_key == "good":
            diet_risk = "protective"
            diet_symbol = "↓"
            diet_note = "Good diet supports prevention of colon, prostate, and other cancers"
        elif diet_key == "average":
            diet_risk = "neutral"
            diet_symbol = "↔"
            diet_note = "Average diet provides moderate protection"
        else:
            diet_risk = "risk"
            diet_symbol = "↑"
            diet_note = "Poor diet increases risk for multiple cancer types"
    else:
        diet_bn_options = {"খুব ভাল": "excellent", "ভাল": "good", "গড়": "average", "খারাপ": "poor"}
        diet_key = diet_bn_options.get(diet_quality, "average")
        
        if diet_key == "excellent":
            diet_risk = "protective"
            diet_symbol = "↓"
            diet_note = "চমৎকার খাদ্যাভ্যাস ক্যান্সার প্রতিরোধে দৃঢ়ভাবে সহায়তা করে"
        elif diet_key == "good":
            diet_risk = "protective"
            diet_symbol = "↓"
            diet_note = "ভাল খাদ্যাভ্যাস কোলন, প্রোস্টেট এবং অন্যান্য ক্যান্সার প্রতিরোধে সহায়তা করে"
        elif diet_key == "average":
            diet_risk = "neutral"
            diet_symbol = "↔"
            diet_note = "গড় খাদ্যাভ্যাস মাঝারি সুরক্ষা প্রদান করে"
        else:
            diet_risk = "risk"
            diet_symbol = "↑"
            diet_note = "খারাপ খাদ্যাভ্যাস একাধিক ক্যান্সারের ঝুঁকি বাড়ায়"
    
    factors.append({
        "factor": f"Diet: {diet_quality}" if language == "English" else f"খাদ্যাভ্যাস: {diet_quality}",
        "risk_level": diet_risk,
        "symbol": diet_symbol,
        "note": diet_note
    })
    
    # Exercise analysis - USING DYNAMIC EXERCISE INPUT
    if language == "English":
        exercise_options = {"Regular": "regular", "Occasional": "occasional", "Rare": "rare", "None": "none"}
        exercise_key = exercise_options.get(exercise, "none")
        
        if exercise_key == "regular":
            exercise_risk = "protective"
            exercise_symbol = "↓"
            exercise_note = "Regular exercise is proven to reduce multiple cancer risks"
        elif exercise_key == "occasional":
            exercise_risk = "neutral"
            exercise_symbol = "↔"
            exercise_note = "Some exercise provides moderate protection"
        elif exercise_key == "rare":
            exercise_risk = "mild_risk"
            exercise_symbol = "↗"
            exercise_note = "Minimal exercise provides limited protection"
        else:
            exercise_risk = "risk"
            exercise_symbol = "↑"
            exercise_note = "Sedentary lifestyle increases cancer risk"
    else:
        exercise_bn_options = {"নিয়মিত": "regular", "মাঝে মাঝে": "occasional", "কদাচিৎ": "rare", "না": "none"}
        exercise_key = exercise_bn_options.get(exercise, "none")
        
        if exercise_key == "regular":
            exercise_risk = "protective"
            exercise_symbol = "↓"
            exercise_note = "নিয়মিত ব্যায়াম একাধিক ক্যান্সারের ঝুঁকি কমাতে প্রমাণিত"
        elif exercise_key == "occasional":
            exercise_risk = "neutral"
            exercise_symbol = "↔"
            exercise_note = "কিছু ব্যায়াম মাঝারি সুরক্ষা প্রদান করে"
        elif exercise_key == "rare":
            exercise_risk = "mild_risk"
            exercise_symbol = "↗"
            exercise_note = "ন্যূনতম ব্যায়াম সীমিত সুরক্ষা প্রদান করে"
        else:
            exercise_risk = "risk"
            exercise_symbol = "↑"
            exercise_note = "নিষ্ক্রিয় জীবনযাত্রা ক্যান্সারের ঝুঁকি বাড়ায়"
    
    factors.append({
        "factor": f"Exercise: {exercise}" if language == "English" else f"ব্যায়াম: {exercise}",
        "risk_level": exercise_risk,
        "symbol": exercise_symbol,
        "note": exercise_note
    })
    
    # Sun exposure analysis - USING DYNAMIC SUN EXPOSURE INPUT
    if language == "English":
        sun_options = {"Low": "low", "Moderate": "moderate", "High": "high", "Excessive": "excessive"}
        sun_key = sun_options.get(sun_exposure, "moderate")
        
        if sun_key == "low":
            sun_risk = "protective"
            sun_symbol = "↓"
            sun_note = "Low sun exposure reduces melanoma risk significantly"
        elif sun_key == "moderate":
            sun_risk = "neutral"
            sun_symbol = "↔"
            sun_note = "Moderate sun exposure with protection is generally safe"
        elif sun_key == "high":
            sun_risk = "mild_risk"
            sun_symbol = "↗"
            sun_note = "High sun exposure increases skin cancer risk"
        else:
            sun_risk = "risk"
            sun_symbol = "↑"
            sun_note = "Excessive sun exposure significantly increases melanoma and skin cancer risk"
    else:
        sun_bn_options = {"কম": "low", "মধ্যম": "moderate", "বেশি": "high", "অতিরিক্ত": "excessive"}
        sun_key = sun_bn_options.get(sun_exposure, "moderate")
        
        if sun_key == "low":
            sun_risk = "protective"
            sun_symbol = "↓"
            sun_note = "কম রোদে থাকা মেলানোমার ঝুঁকি উল্লেখযোগ্যভাবে কমায়"
        elif sun_key == "moderate":
            sun_risk = "neutral"
            sun_symbol = "↔"
            sun_note = "সুরক্ষা সহ মাঝারি রোদে থাকা সাধারণত নিরাপদ"
        elif sun_key == "high":
            sun_risk = "mild_risk"
            sun_symbol = "↗"
            sun_note = "বেশি রোদে থাকা ত্বকের ক্যান্সারের ঝুঁকি বাড়ায়"
        else:
            sun_risk = "risk"
            sun_symbol = "↑"
            sun_note = "অতিরিক্ত রোদে থাকা মেলানোমা এবং ত্বকের ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে বাড়ায়"
    
    factors.append({
        "factor": f"Sun Exposure: {sun_exposure}" if language == "English" else f"রোদে থাকা: {sun_exposure}",
        "risk_level": sun_risk,
        "symbol": sun_symbol,
        "note": sun_note
    })
    
    return factors

def calculate_overall_risk_level(factors_analysis):
    """Calculate overall risk level based on individual factors"""
    
    protective_count = sum(1 for f in factors_analysis if f["risk_level"] == "protective")
    neutral_count = sum(1 for f in factors_analysis if f["risk_level"] == "neutral")
    mild_risk_count = sum(1 for f in factors_analysis if f["risk_level"] == "mild_risk")
    risk_count = sum(1 for f in factors_analysis if f["risk_level"] == "risk")
    high_risk_count = sum(1 for f in factors_analysis if f["risk_level"] == "high_risk")
    
    # Weighted scoring
    score = (protective_count * -2) + (neutral_count * 0) + (mild_risk_count * 1) + (risk_count * 2) + (high_risk_count * 3)
    
    if score <= -4:
        return "very_low"
    elif score <= -1:
        return "low"
    elif score <= 2:
        return "moderate"
    elif score <= 5:
        return "high"
    else:
        return "very_high"

def display_final_risk_evaluation(overall_risk, factors_analysis, language):
    """Display the final risk evaluation with detailed reasoning using STREAMLIT CONTAINERS"""
    
    # Risk level colors and icons
    risk_config = {
        "very_low": {"color": "#4caf50", "icon": "🟢", "bg": "#e8f5e9"},
        "low": {"color": "#8bc34a", "icon": "🟢", "bg": "#f1f8e9"},
        "moderate": {"color": "#ff9800", "icon": "🟡", "bg": "#fff3e0"},
        "high": {"color": "#f44336", "icon": "🔴", "bg": "#ffebee"},
        "very_high": {"color": "#d32f2f", "icon": "🔴", "bg": "#ffcdd2"}
    }
    
    config = risk_config.get(overall_risk, risk_config["moderate"])
    
    if language == "Bengali":
        risk_labels = {
            "very_low": "অত্যন্ত কম ঝুঁকি",
            "low": "কম ঝুঁকি", 
            "moderate": "মাঝারি ঝুঁকি",
            "high": "উচ্চ ঝুঁকি",
            "very_high": "অত্যন্ত উচ্চ ঝুঁকি"
        }
    else:
        risk_labels = {
            "very_low": "VERY LOW RISK",
            "low": "LOW RISK", 
            "moderate": "MODERATE RISK",
            "high": "HIGH RISK",
            "very_high": "VERY HIGH RISK"
        }
    
    risk_label = risk_labels.get(overall_risk, "MODERATE RISK")
    
    # Count protective vs risk factors for reasoning
    protective_factors = [f for f in factors_analysis if f["risk_level"] == "protective"]
    risk_factors = [f for f in factors_analysis if f["risk_level"] in ["mild_risk", "risk", "high_risk"]]
    
    # Use Streamlit containers instead of raw HTML to avoid rendering issues
    if language == "Bengali":
        st.markdown("---")
        st.markdown(f"## {config['icon']} **চূড়ান্ত ঝুঁকি মূল্যায়ন: {risk_label}**")
        
        # Create columns for better layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 বিশ্লেষণের সারসংক্ষেপ:")
            st.markdown(f"**সুরক্ষামূলক কারণ:** {len(protective_factors)} টি")
            for factor in protective_factors:
                st.markdown(f"• {factor['factor']}")
            
        with col2:
            st.markdown("### ⚠️ ঝুঁকি বৃদ্ধিকারী কারণ:")
            st.markdown(f"**ঝুঁকি বৃদ্ধিকারী কারণ:** {len(risk_factors)} টি")
            for factor in risk_factors:
                st.markdown(f"• {factor['factor']}")
        
        # Assessment explanation
        st.markdown("### 🎯 মূল্যায়ন:")
        explanation = get_risk_explanation(overall_risk, protective_factors, risk_factors, language)
        st.info(explanation)
        
    else:
        st.markdown("---")
        st.markdown(f"## {config['icon']} **Final Risk Evaluation: {risk_label}**")
        
        # Create columns for better layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Analysis Summary:")
            st.markdown(f"**Protective Factors:** {len(protective_factors)} identified")
            for factor in protective_factors:
                st.markdown(f"• {factor['factor']}")
            
        with col2:
            st.markdown("### ⚠️ Risk-Enhancing Factors:")
            st.markdown(f"**Risk-Enhancing Factors:** {len(risk_factors)} identified")
            for factor in risk_factors:
                st.markdown(f"• {factor['factor']}")
        
        # Assessment explanation
        st.markdown("### 🎯 Assessment:")
        explanation = get_risk_explanation(overall_risk, protective_factors, risk_factors, language)
        st.info(explanation)

def get_risk_explanation(overall_risk, protective_factors, risk_factors, language):
    """Generate detailed explanation for the risk assessment"""
    
    if language == "Bengali":
        if overall_risk in ["very_low", "low"]:
            if len(protective_factors) >= 5:
                return f"""আপনার জীবনযাত্রায় **{len(protective_factors)}টি শক্তিশালী সুরক্ষামূলক কারণ** রয়েছে যা ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে কমায়। 
                {f"যদিও {len(risk_factors)}টি ঝুঁকির কারণ আছে, " if risk_factors else ""}
                সামগ্রিকভাবে আপনার প্রোফাইল **কম ঝুঁকির** শ্রেণীতে পড়ে। 
                এই ইতিবাচক অভ্যাসগুলো বজায় রাখুন।"""
            else:
                return f"""আপনার বেশিরভাগ জীবনযাত্রার কারণ ক্যান্সার প্রতিরোধে সহায়ক। 
                {f"কিছু ঝুঁকির কারণ থাকলেও, " if risk_factors else ""}
                সামগ্রিক মূল্যায়নে আপনি **কম ঝুঁকির** গ্রুপে রয়েছেন।"""
        
        elif overall_risk == "moderate":
            return f"""আপনার ঝুঁকি প্রোফাইলে সুরক্ষামূলক এবং ঝুঁকিপূর্ণ উভয় ধরনের কারণ রয়েছে। 
            {len(protective_factors)}টি সুরক্ষামূলক কারণ আছে, কিন্তু {len(risk_factors)}টি ঝুঁকির কারণও উপস্থিত। 
            জীবনযাত্রার কিছু পরিবর্তনের মাধ্যমে ঝুঁকি আরো কমানো সম্ভব।"""
        
        else:  # high or very_high
            return f"""আপনার প্রোফাইলে {len(risk_factors)}টি উল্লেখযোগ্য ঝুঁকির কারণ রয়েছে যা ক্যান্সারের সম্ভাবনা বাড়ায়। 
            যদিও {len(protective_factors)}টি সুরক্ষামূলক কারণ আছে, 
            **অগ্রাধিকার ভিত্তিতে জীবনযাত্রার পরিবর্তন এবং নিয়মিত স্ক্রিনিং** প্রয়োজন।"""
    
    else:  # English
        if overall_risk in ["very_low", "low"]:
            if len(protective_factors) >= 5:
                return f"""Your lifestyle includes **{len(protective_factors)} strong protective factors** that significantly reduce cancer risk. 
                {f"Despite having {len(risk_factors)} risk factor(s), " if risk_factors else ""}
                your overall profile places you **firmly in the low risk category** based on lifestyle factors. 
                Continue maintaining these positive health behaviors."""
            else:
                return f"""Most of your lifestyle factors support cancer prevention. 
                {f"While some risk factors are present, " if risk_factors else ""}
                your overall assessment places you in the **low risk group**."""
        
        elif overall_risk == "moderate":
            return f"""Your risk profile shows a balance of protective and risk-enhancing factors. 
            With {len(protective_factors)} protective factors but {len(risk_factors)} risk factor(s) present, 
            there are opportunities to further reduce risk through targeted lifestyle modifications."""
        
        else:  # high or very_high
            return f"""Your profile contains {len(risk_factors)} significant risk factor(s) that elevate cancer probability. 
            While {len(protective_factors)} protective factor(s) are present, 
            **priority should be given to lifestyle changes and regular screening protocols**."""

def display_risk_visualization(risk_assessment: dict, language: str):
    """Display interactive risk visualization"""
    
    cancer_risks = risk_assessment.get("cancer_specific_risks", {})
    
    if cancer_risks:
        if language == "Bengali":
            st.markdown("### 📊 ভিজুয়াল ঝুঁকি মূল্যায়ন")
        else:
            st.markdown("### 📊 Visual Risk Assessment")
        
        # Create risk level distribution
        risk_levels = {"low": 0, "moderate": 0, "high": 0, "critical": 0}
        
        for cancer, risk_data in cancer_risks.items():
            risk_level = risk_data.get("risk_level", "low")
            risk_levels[risk_level] += 1
        
        # Display risk level summary
        col1, col2, col3, col4 = st.columns(4)
        
        risk_colors = {
            "low": "#4caf50",
            "moderate": "#ffeb3b", 
            "high": "#ffa726",
            "critical": "#f44336"
        }
        
        risk_labels = {
            "en": {"low": "Low", "moderate": "Moderate", "high": "High", "critical": "Critical"},
            "bn": {"low": "কম", "moderate": "মধ্যম", "high": "উচ্চ", "critical": "গুরুতর"}
        }
        
        lang_key = "bn" if language == "Bengali" else "en"
        
        with col1:
            st.markdown(f"""
            <div style="background: {risk_colors['low']}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0;">{risk_levels['low']}</h3>
                <p style="margin: 5px 0 0 0;">{risk_labels[lang_key]['low']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: {risk_colors['moderate']}; color: #333; padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0;">{risk_levels['moderate']}</h3>
                <p style="margin: 5px 0 0 0;">{risk_labels[lang_key]['moderate']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: {risk_colors['high']}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0;">{risk_levels['high']}</h3>
                <p style="margin: 5px 0 0 0;">{risk_labels[lang_key]['high']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: {risk_colors['critical']}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin: 0;">{risk_levels['critical']}</h3>
                <p style="margin: 5px 0 0 0;">{risk_labels[lang_key]['critical']}</p>
            </div>
            """, unsafe_allow_html=True)

def display_detailed_risk_breakdown(risk_assessment: dict, reasoning_engine, language: str):
    """Display detailed risk breakdown with reasoning"""
    
    cancer_risks = risk_assessment.get("cancer_specific_risks", {})
    
    if cancer_risks:
        if language == "Bengali":
            st.markdown("### 🔍 বিস্তারিত ঝুঁকি বিশ্লেষণ")
        else:
            st.markdown("### 🔍 Detailed Risk Analysis")
        
        for cancer_type, risk_data in cancer_risks.items():
            risk_score = risk_data.get("risk_score", 0)
            risk_level = risk_data.get("risk_level", "low")
            contributing_factors = risk_data.get("contributing_factors", [])
            
            # Color based on risk level
            colors = {
                "low": "#4caf50",
                "moderate": "#ffeb3b",
                "high": "#ffa726", 
                "critical": "#f44336"
            }
            
            color = colors.get(risk_level, "#757575")
            
            cancer_name = cancer_type.replace("_", " ").title()
            if language == "Bengali":
                cancer_translations = {
                    "Breast Cancer": "স্তন ক্যান্সার",
                    "Lung Cancer": "ফুসফুস ক্যান্সার",
                    "Colorectal Cancer": "কোলোরেক্টাল ক্যান্সার",
                    "Prostate Cancer": "প্রোস্টেট ক্যান্সার",
                    "Cervical Cancer": "জরায়ু মুখের ক্যান্সার"
                }
                cancer_name = cancer_translations.get(cancer_name, cancer_name)
                
                risk_level_bn = {
                    "low": "কম",
                    "moderate": "মধ্যম",
                    "high": "উচ্চ", 
                    "critical": "গুরুতর"
                }
                risk_level_text = risk_level_bn.get(risk_level, risk_level)
            else:
                risk_level_text = risk_level.title()
            
            # Progress bar for risk score
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; border-left: 4px solid {color}; margin: 10px 0;">
                <h4 style="margin: 0 0 10px 0; color: {color};">{cancer_name}</h4>
                <div style="background: #e0e0e0; border-radius: 10px; height: 10px; margin: 10px 0;">
                    <div style="background: {color}; height: 10px; border-radius: 10px; width: {risk_score*100}%;"></div>
                </div>
                <p style="margin: 5px 0 0 0;"><strong>{'ঝুঁকি স্তর' if language == 'Bengali' else 'Risk Level'}:</strong> {risk_level_text} ({risk_score:.1%})</p>
            </div>
            """, unsafe_allow_html=True)


def render_enhanced_reasoning_viewer(language: str):
    """Render enhanced AI reasoning process viewer"""
    
    if language == "Bengali":
        st.markdown("""
        <div class="ai-reasoning-card">
            <h2 style="margin: 0;">🧠 AI যুক্তি প্রক্রিয়া ভিউয়ার</h2>
            <p style="margin: 10px 0 0 0;">AI কীভাবে ক্যান্সার ঝুঁকি বিশ্লেষণ করে তা দেখুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ai-reasoning-card">
            <h2 style="margin: 0;">🧠 AI Reasoning Process Viewer</h2>
            <p style="margin: 10px 0 0 0;">See how AI analyzes cancer risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check for reasoning data from enhanced consultation
    reasoning_data = get_enhanced_reasoning_data()
    
    if reasoning_data:
        display_enhanced_reasoning_trace(reasoning_data, language)
    else:
        if language == "Bengali":
            st.info("কোনো যুক্তি ডেটা পাওয়া যায়নি। প্রথমে একটি পরামর্শ সম্পন্ন করুন।")
            
            if st.button("🎬 ডেমো যুক্তি প্রক্রিয়া দেখুন"):
                display_enhanced_demo_reasoning(language)
        else:
            st.info("No reasoning data found. Complete a consultation first to see AI reasoning.")
            
            if st.button("🎬 Show Demo Reasoning Process"):
                display_enhanced_demo_reasoning(language)


def process_enhanced_cancer_multimodal_input(audio_file, image_file, language: str):
    """Process voice and vision input for enhanced cancer analysis"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize reasoning engine
    reasoning_engine = CancerReasoningEngine(lang_code)
    
    transcribed_text = ""
    analysis_results = {}
    
    try:
        # Step 1: Process audio if provided
        if audio_file:
            with st.status("🎯 Converting speech to text..." if language == "English" else "🎯 কথাকে টেক্সটে রূপান্তর করা হচ্ছে..."):
                # Save audio to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                    tmp_audio.write(audio_file.read())
                    audio_path = tmp_audio.name
                
                # Transcribe
                transcribed_text = transcribe_with_groq(
                    stt_model="whisper-large-v3",
                    audio_filepath=audio_path,
                    GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                    language=lang_code
                )
                
                os.unlink(audio_path)  # Cleanup
        
        # Step 2: Process image if provided
        image_analysis = ""
        if image_file:
            with st.status("📷 Analyzing image..." if language == "English" else "📷 ছবি বিশ্লেষণ করা হচ্ছে..."):
                # Save image to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(image_file.getvalue())
                    image_path = tmp_img.name
                
                # Analyze with cancer-specific prompt
                cancer_image_prompt = get_enhanced_cancer_image_analysis_prompt(lang_code)
                image_analysis = analyze_image_with_query(
                    query=cancer_image_prompt,
                    encoded_image=encode_image(image_path),
                    language=lang_code
                )
                
                os.unlink(image_path)  # Cleanup
        
        # Step 3: Combine inputs for comprehensive analysis
        combined_input = f"{transcribed_text}\n\nImage Analysis: {image_analysis}".strip()
        
        if combined_input:
            with st.status("🧠 Advanced cancer analysis..." if language == "English" else "🧠 উন্নত ক্যান্সার বিশ্লেষণ..."):
                # Run through reasoning engine
                symptoms_data = {
                    "description": combined_input,
                    "severity": 5,
                    "duration": "unknown"
                }
                
                # Step-by-step analysis
                symptoms_analysis = reasoning_engine.analyze_symptoms(symptoms_data)
                
                # Basic risk assessment (would need more user data for complete assessment)
                risk_assessment = reasoning_engine.assess_risk_factors({
                    "age": 40,  # Default values
                    "gender": "unknown"
                })
                
                differential_diagnosis = reasoning_engine.generate_differential_diagnosis(
                    symptoms_analysis, risk_assessment
                )
                
                recommendations = reasoning_engine.generate_comprehensive_recommendations(
                    symptoms_analysis, risk_assessment, differential_diagnosis
                )
                
                # Generate comprehensive response
                analysis_results = {
                    "symptoms_analysis": symptoms_analysis,
                    "risk_assessment": risk_assessment,
                    "differential_diagnosis": differential_diagnosis,
                    "recommendations": recommendations
                }
                
                comprehensive_response = reasoning_engine.generate_llm_enhanced_response(analysis_results)
        
        # Display results
        display_enhanced_multimodal_cancer_results(transcribed_text, image_analysis, analysis_results, comprehensive_response, language)
        
    except Exception as e:
        logging.error(f"Error in enhanced cancer multimodal processing: {e}")
        error_msg = (
            f"বিশ্লেষণে ত্রুটি: {str(e)}"
            if language == "Bengali" else
            f"Analysis error: {str(e)}"
        )
        st.error(error_msg)


def get_enhanced_cancer_image_analysis_prompt(lang_code: str) -> str:
    """Get enhanced cancer-specific image analysis prompt"""
    
    if lang_code == "bn":
        return """আপনি একজন ক্যান্সার বিশেষজ্ঞ যিনি ছবি বিশ্লেষণ করেন। এই ছবিতে কোনো অস্বাভাবিক বৃদ্ধি, পরিবর্তন, বা ক্যান্সারের সম্ভাব্য লক্ষণ আছে কিনা তা পরীক্ষা করুন।

বিশেষভাবে লক্ষ্য করুন:
- ত্বকের কোনো পরিবর্তন বা নতুন দাগ (মেলানোমা/স্কিন ক্যান্সার)
- অস্বাভাবিক পিণ্ড বা ফোলা
- রঙের পরিবর্তন বা অসিমেট্রি
- সীমানার অনিয়মিততা
- আকারের পরিবর্তন
- পৃষ্ঠের টেক্সচার পরিবর্তন

সতর্কতার সাথে বিশ্লেষণ করুন এবং যদি কোনো উদ্বেগজনক বিষয় দেখেন তাহলে চিকিৎসা পরামর্শ নেওয়ার সুপারিশ করুন।"""
    else:
        return """You are a cancer specialist analyzing images. Examine this image for any abnormal growths, changes, or potential signs of cancer.

Pay special attention to:
- Skin changes or new spots (melanoma/skin cancer)
- Unusual lumps or swelling  
- Color changes or asymmetry
- Border irregularities
- Size variations
- Surface texture changes

Analyze carefully and recommend medical consultation if you see anything concerning."""


def display_enhanced_multimodal_cancer_results(transcribed_text: str, image_analysis: str, analysis_results: dict, comprehensive_response: str, language: str):
    """Display results from enhanced multimodal cancer analysis"""
    
    if transcribed_text:
        if language == "Bengali":
            st.markdown("""
            <div class="question-card">
                <h4>👤 আপনি যা বলেছেন:</h4>
                <p style="font-style: italic; background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    "{}"
                </p>
            </div>
            """.format(transcribed_text), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="question-card">
                <h4>👤 What you said:</h4>
                <p style="font-style: italic; background: #f8f9fa; padding: 15px; border-radius: 10px;">
                    "{}"
                </p>
            </div>
            """.format(transcribed_text), unsafe_allow_html=True)
    
    if image_analysis:
        if language == "Bengali":
            st.markdown("""
            <div class="question-card">
                <h4>📷 ছবি বিশ্লেষণ:</h4>
                <div style="background: #f0f8ff; padding: 15px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(image_analysis.replace('\n', '<br>')), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="question-card">
                <h4>📷 Image Analysis:</h4>
                <div style="background: #f0f8ff; padding: 15px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(image_analysis.replace('\n', '<br>')), unsafe_allow_html=True)
    
    if analysis_results and comprehensive_response:
        # Show urgency level
        urgency_level = determine_enhanced_urgency_from_analysis(analysis_results)
        display_enhanced_urgency_alert(urgency_level, language)
        
        # Show comprehensive response
        if language == "Bengali":
            st.markdown("""
            <div class="ai-reasoning-card">
                <h4>🏥 বিস্তারিত ক্যান্সার বিশ্লেষণ:</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(comprehensive_response.replace('\n', '<br>')), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ai-reasoning-card">
                <h4>🏥 Comprehensive Cancer Analysis:</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    {}
                </div>
            </div>
            """.format(comprehensive_response.replace('\n', '<br>')), unsafe_allow_html=True)


def display_quick_risk_results(age, smoking, family_history, symptoms, exercise, alcohol, language):
    """Display quick risk assessment results"""
    
    # Calculate basic risk score
    risk_score = 0
    risk_factors = []
    
    # Age factor
    if language == "Bengali":
        if age == "৫০+":
            risk_score += 2
            risk_factors.append("বয়স ৫০+")
        elif age == "৩০-৫০":
            risk_score += 1
            risk_factors.append("মধ্যবয়সী")
    else:
        if age == "50+":
            risk_score += 2
            risk_factors.append("Age 50+")
        elif age == "30-50":
            risk_score += 1
            risk_factors.append("Middle age")
    
    # Smoking factor
    if (language == "Bengali" and smoking == "হ্যাঁ") or (language == "English" and smoking == "Yes"):
        risk_score += 3
        if language == "Bengali":
            risk_factors.append("ধূমপান")
        else:
            risk_factors.append("Smoking")
    
    # Family history factor
    if (language == "Bengali" and family_history == "হ্যাঁ") or (language == "English" and family_history == "Yes"):
        risk_score += 2
        if language == "Bengali":
            risk_factors.append("পারিবারিক ইতিহাস")
        else:
            risk_factors.append("Family history")
    
    # Symptoms factor
    if (language == "Bengali" and symptoms == "হ্যাঁ") or (language == "English" and symptoms == "Yes"):
        risk_score += 3
        if language == "Bengali":
            risk_factors.append("উপসর্গ উপস্থিত")
        else:
            risk_factors.append("Symptoms present")
    
    # Exercise factor (protective)
    if (language == "Bengali" and exercise == "না") or (language == "English" and exercise == "No"):
        risk_score += 1
        if language == "Bengali":
            risk_factors.append("ব্যায়ামের অভাব")
        else:
            risk_factors.append("Lack of exercise")
    
    # Alcohol factor
    if (language == "Bengali" and alcohol == "হ্যাঁ") or (language == "English" and alcohol == "Yes"):
        risk_score += 1
        if language == "Bengali":
            risk_factors.append("মদ্যপান")
        else:
            risk_factors.append("Alcohol consumption")
    
    # Determine risk level
    if risk_score >= 6:
        risk_level = "high"
        risk_class = "risk-indicator-high"
    elif risk_score >= 3:
        risk_level = "moderate"
        risk_class = "risk-indicator-moderate"
    else:
        risk_level = "low"
        risk_class = "risk-indicator-low"
    
    # Display results
    if language == "Bengali":
        risk_level_text = {"low": "কম ঝুঁকি", "moderate": "মধ্যম ঝুঁকি", "high": "উচ্চ ঝুঁকি"}[risk_level]
        
        st.markdown(f"""
        <div class="{risk_class}">
            <h3 style="margin: 0 0 10px 0;">📊 আপনার ঝুঁকি স্তর: {risk_level_text}</h3>
            <p style="margin: 0;">স্কোর: {risk_score}/10</p>
        </div>
        """, unsafe_allow_html=True)
        
        if risk_factors:
            st.markdown("#### 🔍 চিহ্নিত ঝুঁকির কারণ:")
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        
        if risk_level == "high":
            st.error("⚠️ উচ্চ ঝুঁকি: অনুগ্রহ করে একজন অনকোলজিস্টের সাথে পরামর্শ করুন।")
        elif risk_level == "moderate":
            st.warning("📋 মধ্যম ঝুঁকি: নিয়মিত স্ক্রিনিং এবং চিকিৎসক পরামর্শ নিন।")
        else:
            st.success("✅ কম ঝুঁকি: স্বাস্থ্যকর জীবনযাত্রা বজায় রাখুন এবং নিয়মিত চেকআপ করান।")
    else:
        risk_level_text = {"low": "Low Risk", "moderate": "Moderate Risk", "high": "High Risk"}[risk_level]
        
        st.markdown(f"""
        <div class="{risk_class}">
            <h3 style="margin: 0 0 10px 0;">📊 Your Risk Level: {risk_level_text}</h3>
            <p style="margin: 0;">Score: {risk_score}/10</p>
        </div>
        """, unsafe_allow_html=True)
        
        if risk_factors:
            st.markdown("#### 🔍 Identified Risk Factors:")
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        
        if risk_level == "high":
            st.error("⚠️ High Risk: Please consult with an oncologist.")
        elif risk_level == "moderate":
            st.warning("📋 Moderate Risk: Regular screening and medical consultation recommended.")
        else:
            st.success("✅ Low Risk: Maintain healthy lifestyle and regular checkups.")


def display_enhanced_urgency_alert(urgency_level: str, language: str):
    """Display enhanced urgency alert based on analysis"""
    
    urgency_classes = {
        "CRITICAL": "emergency-alert",
        "HIGH": "risk-indicator-high", 
        "MODERATE": "risk-indicator-moderate",
        "LOW": "risk-indicator-low"
    }
    
    urgency_messages = {
        "en": {
            "CRITICAL": "🚨 CRITICAL: Seek immediate medical attention",
            "HIGH": "⚠️ HIGH: Schedule medical consultation within 24-48 hours",
            "MODERATE": "📋 MODERATE: Schedule routine medical consultation within 1-2 weeks",
            "LOW": "✅ LOW: Continue regular health monitoring"
        },
        "bn": {
            "CRITICAL": "🚨 গুরুতর: অবিলম্বে চিকিৎসা সহায়তা নিন",
            "HIGH": "⚠️ উচ্চ: ২৪-৪৮ ঘন্টার মধ্যে চিকিৎসক দেখান",
            "MODERATE": "📋 মধ্যম: ১-২ সপ্তাহের মধ্যে নিয়মিত চিকিৎসা পরামর্শ নিন",
            "LOW": "✅ কম: নিয়মিত স্বাস্থ্য পর্যবেক্ষণ চালিয়ে যান"
        }
    }
    
    lang_key = "bn" if language == "Bengali" else "en"
    css_class = urgency_classes.get(urgency_level, "risk-indicator-low")
    message = urgency_messages[lang_key].get(urgency_level, "")
    
    st.markdown(f"""
    <div class="{css_class}">
        <h3 style="margin: 0 0 10px 0;">{'জরুরিত্বের স্তর' if language == 'Bengali' else 'Urgency Level'}: {urgency_level}</h3>
        <p style="margin: 0; font-size: 1.1em;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def determine_enhanced_urgency_from_analysis(analysis_results: dict) -> str:
    """Determine urgency level from enhanced analysis results"""
    
    symptoms_analysis = analysis_results.get("symptoms_analysis", {})
    urgency_score = symptoms_analysis.get("urgency_score", 0)
    requires_immediate = symptoms_analysis.get("requires_immediate_attention", False)
    
    if requires_immediate or urgency_score >= 8:
        return "CRITICAL"
    elif urgency_score >= 6:
        return "HIGH"
    elif urgency_score >= 4:
        return "MODERATE"
    else:
        return "LOW"


def get_enhanced_reasoning_data():
    """Get enhanced reasoning data from session state"""
    
    # Check for reasoning data in enhanced consultation sessions
    reasoning_keys = [
        'enhanced_cancer_consultation_en',
        'enhanced_cancer_consultation_bn'
    ]
    
    for key in reasoning_keys:
        if key in st.session_state:
            consultation = st.session_state[key]
            if hasattr(consultation, 'reasoning_engine') and consultation.reasoning_engine.reasoning_trace:
                return consultation.reasoning_engine.get_reasoning_explanation()
    
    return None


def display_enhanced_reasoning_trace(reasoning_data: dict, language: str):
    """Display enhanced reasoning trace in an interactive format"""
    
    step_details = reasoning_data.get("step_details", [])
    overall_confidence = reasoning_data.get("overall_confidence", 0)
    
    if language == "Bengali":
        st.markdown(f"### 📊 সামগ্রিক আত্মবিশ্বাস: {overall_confidence:.2f}")
    else:
        st.markdown(f"### 📊 Overall Confidence: {overall_confidence:.2f}")
    
    # Display confidence meter
    confidence_color = "#4caf50" if overall_confidence > 0.8 else "#ff9800" if overall_confidence > 0.6 else "#f44336"
    st.markdown(f"""
    <div style="background: #e0e0e0; border-radius: 10px; height: 20px; margin: 10px 0;">
        <div style="background: {confidence_color}; height: 20px; border-radius: 10px; width: {overall_confidence*100}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each reasoning step in enhanced format
    for i, step in enumerate(step_details, 1):
        step_name = step['step'].replace('_', ' ').title()
        reasoning = step['reasoning']
        confidence = step['confidence']
        timestamp = step['timestamp']
        
        # Step confidence color
        step_color = "#4caf50" if confidence > 0.8 else "#ff9800" if confidence > 0.6 else "#f44336"
        
        if language == "Bengali":
            step_translations = {
                "Symptom Analysis": "লক্ষণ বিশ্লেষণ",
                "Risk Assessment": "ঝুঁকি মূল্যায়ন", 
                "Differential Diagnosis": "পার্থক্যমূলক রোগ নির্ণয়",
                "Recommendation Generation": "সুপারিশ প্রস্তুতি",
                "Urgency Evaluation": "জরুরিত্ব মূল্যায়ন"
            }
            step_name = step_translations.get(step_name, step_name)
        
        with st.expander(f"পদক্ষেপ {i}: {step_name} (আত্মবিশ্বাস: {confidence:.2f})" if language == "Bengali" 
                        else f"Step {i}: {step_name} (Confidence: {confidence:.2f})"):
            
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid {step_color};">
                <h4 style="color: {step_color}; margin: 0 0 15px 0;">
                    {step_name}
                </h4>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <strong>{'যুক্তি প্রক্রিয়া' if language == 'Bengali' else 'Reasoning Process'}:</strong>
                    <p style="margin: 10px 0 0 0; line-height: 1.6;">{reasoning}</p>
                </div>
                <div style="background: {step_color}20; padding: 10px; border-radius: 8px;">
                    <strong>{'আত্মবিশ্বাস স্তর' if language == 'Bengali' else 'Confidence Level'}:</strong> {confidence:.2f}
                    <div style="background: #e0e0e0; border-radius: 5px; height: 8px; margin: 5px 0;">
                        <div style="background: {step_color}; height: 8px; border-radius: 5px; width: {confidence*100}%;"></div>
                    </div>
                </div>
                <p style="color: #666; font-size: 0.9em; margin: 15px 0 0 0;">
                    <strong>{'সময়' if language == 'Bengali' else 'Timestamp'}:</strong> {timestamp}
                </p>
            </div>
            """, unsafe_allow_html=True)


def display_enhanced_demo_reasoning(language: str):
    """Display enhanced demo reasoning process"""
    
    if language == "Bengali":
        demo_steps = [
            {
                "step": "লক্ষণ বিশ্লেষণ",
                "reasoning": "রোগী দীর্ঘস্থায়ী কাশি এবং ওজন হ্রাসের কথা বলেছেন। এই লক্ষণগুলি ফুসফুস ক্যান্সারের সাথে সামঞ্জস্যপূর্ণ হতে পারে। কাশি ৩ সপ্তাহের বেশি স্থায়ী হলে তা উদ্বেগজনক।",
                "confidence": 0.78,
                "details": "লক্ষণের তীব্রতা: মধ্যম, সময়কাল: দীর্ঘমেয়াদী, জরুরিত্ব স্কোর: ৭/১০"
            },
            {
                "step": "ঝুঁকি মূল্যায়ন", 
                "reasoning": "রোগীর ধূমপানের ইতিহাস এবং ৫০+ বয়স ফুসফুস ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে বাড়ায়। পারিবারিক ইতিহাস অতিরিক্ত ঝুঁকি যোগ করে।",
                "confidence": 0.85,
                "details": "প্রধান ঝুঁকি: ধূমপান (উচ্চ), বয়স (মধ্যম), পারিবারিক ইতিহাস (মধ্যম)"
            },
            {
                "step": "পার্থক্যমূলক রোগ নির্ণয়",
                "reasoning": "লক্ষণ এবং ঝুঁকির কারণের ভিত্তিতে, ফুসফুস ক্যান্সার সবচেয়ে সম্ভাব্য। অন্যান্য সম্ভাবনা: দীর্ঘমেয়াদী ব্রংকাইটিস, COPD।",
                "confidence": 0.82,
                "details": "১ম সম্ভাবনা: ফুসফুস ক্যান্সার (৭৫%), ২য়: COPD (২০%), ৩য়: সংক্রমণ (৫%)"
            },
            {
                "step": "সুপারিশ প্রস্তুতি",
                "reasoning": "তাৎক্ষণিক চেস্ট এক্স-রে এবং পুলমোনোলজিস্টের পরামর্শ প্রয়োজন। CT স্ক্যান এবং ব্রংকোস্কোপি বিবেচনা করা উচিত।",
                "confidence": 0.92,
                "details": "অগ্রাধিকার: চেস্ট এক্স-রে (জরুরি), CT স্ক্যান (১ সপ্তাহের মধ্যে), বিশেষজ্ঞ পরামর্শ"
            }
        ]
    else:
        demo_steps = [
            {
                "step": "Symptom Analysis",
                "reasoning": "Patient reports persistent cough and weight loss. These symptoms may be consistent with lung cancer. Cough lasting more than 3 weeks is concerning.",
                "confidence": 0.78,
                "details": "Symptom severity: Moderate, Duration: Long-term, Urgency score: 7/10"
            },
            {
                "step": "Risk Assessment",
                "reasoning": "Patient's smoking history and age 50+ significantly increases lung cancer risk. Family history adds additional risk factor.",
                "confidence": 0.85,
                "details": "Major risks: Smoking (High), Age (Moderate), Family history (Moderate)"
            },
            {
                "step": "Differential Diagnosis",
                "reasoning": "Based on symptoms and risk factors, lung cancer is most probable. Other possibilities: Chronic bronchitis, COPD.",
                "confidence": 0.82,
                "details": "1st possibility: Lung cancer (75%), 2nd: COPD (20%), 3rd: Infection (5%)"
            },
            {
                "step": "Recommendation Generation", 
                "reasoning": "Immediate chest X-ray and pulmonologist consultation needed. CT scan and bronchoscopy should be considered.",
                "confidence": 0.92,
                "details": "Priority: Chest X-ray (urgent), CT scan (within 1 week), specialist consultation"
            }
        ]
    
    for i, step in enumerate(demo_steps, 1):
        step_color = "#4caf50" if step['confidence'] > 0.8 else "#ff9800" if step['confidence'] > 0.6 else "#f44336"
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {step_color};">
            <h4 style="color: {step_color};">
                {'পদক্ষেপ' if language == 'Bengali' else 'Step'} {i}: {step['step']}
            </h4>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p style="margin: 0; line-height: 1.6;">{step['reasoning']}</p>
            </div>
            <div style="background: {step_color}20; padding: 10px; border-radius: 8px; margin: 10px 0;">
                <strong>{'বিস্তারিত তথ্য' if language == 'Bengali' else 'Details'}:</strong>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">{step['details']}</p>
            </div>
            <div style="background: {step_color}20; padding: 10px; border-radius: 8px;">
                <strong>{'আত্মবিশ্বাস' if language == 'Bengali' else 'Confidence'}:</strong> {step['confidence']:.2f}
                <div style="background: #e0e0e0; border-radius: 5px; height: 8px; margin: 5px 0;">
                    <div style="background: {step_color}; height: 8px; border-radius: 5px; width: {step['confidence']*100}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)