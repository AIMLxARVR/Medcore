# medical_imaging_analysis.py - Medical Imaging Analysis with Multiple Specialist Agents
import os
import uuid
import tempfile
import logging
from typing import Dict, List, Optional, Tuple
import streamlit as st
from groq import Groq
from brain_of_the_doctor import encode_image, analyze_image_with_query
from PIL import Image as PILImage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Vision model

class MedicalImagingSpecialist:
    """Medical imaging specialist using Groq's vision capabilities"""
    
    def __init__(self, specialist_type: str, language: str = "en"):
        self.specialist_type = specialist_type
        self.language = language
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        
    def get_specialist_prompt(self) -> str:
        """Get specialist-specific analysis prompt"""
        
        prompts = {
            "en": {
                "ophthalmology": """You are an experienced ophthalmologist specializing in retinal imaging and eye disease diagnosis. Analyze the medical image and respond according to this structure:

### 1. Image Type & Region
- Identify the image type (retinal photography, OCT, fundus image, etc.)
- Specify which eye region (retina, optic disc, macula, etc.) and position
- Assess image quality and technical standards

### 2. Key Observations
- Highlight main findings (retinal condition, blood vessel structure)
- Identify potential abnormalities (diabetic retinopathy, macular degeneration)
- Include relevant measurements (macular thickness) where applicable

### 3. Diagnostic Analysis
- Provide likely primary diagnosis with confidence
- List other possible conditions
- Explain each diagnosis based on observations
- Highlight urgent matters (vision loss risk)

### 4. Patient-Friendly Explanation
- Explain findings in simple language
- Simplify medical terms (macula, retinopathy)
- Use real-life examples

### 5. Clinical Recommendations
- Immediate actions needed
- Follow-up schedule
- Additional tests required
- Lifestyle modifications""",

                "cardiology": """You are an experienced cardiologist specializing in cardiac imaging (echocardiogram, angiogram) analysis. Analyze the medical image and respond according to this structure:

### 1. Image Type & Region
- Identify the image type (echocardiogram, cardiac CT, angiogram, etc.)
- Specify which heart region (valves, ventricles, coronary arteries) and position
- Assess image quality and technical standards

### 2. Key Observations
- Highlight main findings (valve function, arterial narrowing)
- Identify potential abnormalities (stenosis, ejection fraction abnormalities)
- Include relevant measurements (ejection fraction, arterial diameter)

### 3. Diagnostic Analysis
- Provide likely primary diagnosis with confidence
- List other possible conditions
- Explain each diagnosis based on observations
- Highlight urgent matters (acute coronary syndrome)

### 4. Patient-Friendly Explanation
- Explain findings in simple language
- Simplify medical terms (ejection fraction, stenosis)
- Use practical examples

### 5. Clinical Recommendations
- Immediate actions needed
- Treatment options
- Lifestyle modifications
- Follow-up care plan""",

                "orthopedics": """You are an experienced orthopedic specialist skilled in bone and joint imaging analysis (X-ray, MRI, CT scan). Analyze the medical image and respond according to this structure:

### 1. Image Type & Region
- Identify the image type (X-ray, MRI, CT scan, etc.)
- Specify which body region (bones, joints, spine, fracture site) and position
- Assess image quality and technical standards

### 2. Key Observations
- Highlight main findings (bone structure, joint space, fracture type)
- Identify potential abnormalities (fracture, osteoarthritis, dislocation)
- Include relevant measurements (joint space width, fracture length)

### 3. Diagnostic Analysis
- Provide likely primary diagnosis with confidence
- List other possible conditions
- Explain each diagnosis based on observations
- Highlight urgent matters (fracture displacement, infection risk)

### 4. Patient-Friendly Explanation
- Explain findings in simple language
- Simplify medical terms (fracture, osteoarthritis)
- Use practical examples

### 5. Clinical Recommendations
- Immediate treatment needed
- Surgical vs conservative management
- Rehabilitation plan
- Recovery timeline""",

                "general_medicine": """You are an experienced internal medicine specialist. Analyze this medical image and provide a concise overview focusing on:

### 1. Initial Assessment
- Image type and body system involved
- Primary area of concern

### 2. Key Findings
- Main observations
- Any abnormalities noted

### 3. Specialist Referral Recommendations
- Which specialists should evaluate this case
- Brief explanation of why each specialist is relevant
- Priority level (urgent vs routine)

Keep the analysis concise and focus on directing appropriate specialist care."""
            },
            
            "bn": {
                "ophthalmology": """আপনি একজন অভিজ্ঞ চক্ষু বিশেষজ্ঞ, যিনি রেটিনাল ইমেজিং এবং চোখের রোগ নির্ণয়ে বিশেষজ্ঞ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (রেটিনাল ফটোগ্রাফি, OCT, ফান্ডাস ইমেজ ইত্যাদি)
- কোন চোখের অঞ্চল (রেটিনা, অপটিক ডিস্ক, ম্যাকুলা ইত্যাদি) এবং পজিশন তা বলুন
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো সুনির্দিষ্টভাবে তুলে ধরুন (যেমন রেটিনার অবস্থা, রক্তনালীর গঠন)
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন ডায়াবেটিক রেটিনোপ্যাথি, ম্যাকুলার ডিজেনারেশন)
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন ম্যাকুলার পুরুত্ব) উল্লেখ করুন

### ৩. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে
- সম্ভাব্য অন্যান্য রোগসমূহ তালিকাভুক্ত করুন
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন
- জরুরি বা গুরুত্বপূর্ণ বিষয় (যেমন দৃষ্টিহানির ঝুঁকি) হাইলাইট করুন

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন
- চিকিৎসাগত শব্দ (যেমন ম্যাকুলা, রেটিনোপ্যাথি) সহজ করে বোঝান
- বাস্তব জীবনের উদাহরণ ব্যবহার করুন

### ৫. ক্লিনিক্যাল সুপারিশ
- তাৎক্ষণিক প্রয়োজনীয় পদক্ষেপ
- ফলো-আপ সূচি
- অতিরিক্ত পরীক্ষার প্রয়োজন
- জীবনযাত্রার পরিবর্তন""",

                "cardiology": """আপনি একজন অভিজ্ঞ কার্ডিওলজিস্ট, যিনি হৃদরোগ সম্পর্কিত ইমেজিং (যেমন ইকোকার্ডিওগ্রাম, এনজিওগ্রাম) বিশ্লেষণে বিশেষজ্ঞ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (ইকোকার্ডিওগ্রাম, কার্ডিয়াক CT, এনজিওগ্রাম ইত্যাদি)
- হৃদপিণ্ডের কোন অঞ্চল (ভাল্ভ, ভেন্ট্রিকল, করোনারি ধমনী) এবং পজিশন তা বলুন
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো তুলে ধরুন (যেমন ভাল্ভের কার্যকারিতা, ধমনীর সংকীর্ণতা)
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন স্টেনোসিস, ইজেকশন ফ্রাকশন অস্বাভাবিকতা)
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন ইজেকশন ফ্রাকশন, ধমনীর ব্যাস) উল্লেখ করুন

### ৩. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে
- সম্ভাব্য অন্যান্য রোগ তালিকাভুক্ত করুন
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন
- জরুরি বিষয় (যেমন তীব্র করোনারি সিনড্রোম) হাইলাইট করুন

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন
- চিকিৎসাগত শব্দ (যেমন ইজেকশন ফ্রাকশন, স্টেনোসিস) সহজ করে বোঝান
- বাস্তব উদাহরণ ব্যবহার করুন

### ৫. ক্লিনিক্যাল সুপারিশ
- তাৎক্ষণিক প্রয়োজনীয় পদক্ষেপ
- চিকিৎসার বিকল্প
- জীবনযাত্রার পরিবর্তন
- ফলো-আপ যত্ন পরিকল্পনা""",

                "orthopedics": """আপনি একজন অভিজ্ঞ অর্থোপেডিক বিশেষজ্ঞ, যিনি হাড় এবং জয়েন্ট সম্পর্কিত ইমেজিং (যেমন এক্স-রে, MRI, CT স্ক্যান) বিশ্লেষণে দক্ষ। নিচের মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিচের কাঠামো অনুসারে উত্তর দিন:

### ১. চিত্রের ধরন ও অঞ্চল
- চিত্রের ধরন শনাক্ত করুন (এক্স-রে, MRI, CT স্ক্যান ইত্যাদি)
- কোন শারীরিক অঞ্চল (হাড়, জয়েন্ট, মেরুদণ্ড, ফ্র্যাকচার সাইট) এবং পজিশন তা বলুন
- চিত্রের গুণমান এবং কারিগরি মান যাচাই করুন

### ২. মূল পর্যবেক্ষণ
- প্রধান বিষয়গুলো তুলে ধরুন (যেমন হাড়ের গঠন, জয়েন্টের স্থান, ফ্র্যাকচারের ধরন)
- সম্ভাব্য অস্বাভাবিকতা চিহ্নিত করুন (যেমন ফ্র্যাকচার, অস্টিওআর্থ্রাইটিস, ডিসলোকেশন)
- প্রাসঙ্গিক ক্ষেত্রে পরিমাপ (যেমন জয়েন্ট স্পেস প্রস্থ, ফ্র্যাকচারের দৈর্ঘ্য) উল্লেখ করুন

### ৩. রোগ নির্ণয়মূলক বিশ্লেষণ
- সম্ভাব্য প্রাথমিক রোগ নির্ণয় দিন আত্মবিশ্বাসের সাথে
- সম্ভাব্য অন্যান্য রোগ তালিকাভুক্ত করুন
- প্রতিটি নির্ণয়ের জন্য পর্যবেক্ষণের ভিত্তিতে ব্যাখ্যা দিন
- জরুরি বিষয় (যেমন ফ্র্যাকচারের স্থানচ্যুতি, সংক্রমণের ঝুঁকি) হাইলাইট করুন

### ৪. রোগীর জন্য সহজ ব্যাখ্যা
- ফলাফল সহজ ভাষায় ব্যাখ্যা করুন
- চিকিৎসাগত শব্দ (যেমন ফ্র্যাকচার, অস্টিওআর্থ্রাইটিস) সহজ করে বোঝান
- বাস্তব উদাহরণ ব্যবহার করুন

### ৫. ক্লিনিক্যাল সুপারিশ
- তাৎক্ষণিক চিকিৎসার প্রয়োজন
- সার্জিক্যাল বনাম রক্ষণশীল ব্যবস্থাপনা
- পুনর্বাসন পরিকল্পনা
- সুস্থতার সময়সীমা""",

                "general_medicine": """আপনি একজন অভিজ্ঞ ইন্টারনাল মেডিসিন বিশেষজ্ঞ। এই মেডিকেল ইমেজটি বিশ্লেষণ করুন এবং নিম্নলিখিত বিষয়ে ফোকাস করে একটি সংক্ষিপ্ত ওভারভিউ প্রদান করুন:

### ১. প্রাথমিক মূল্যায়ন
- ইমেজের ধরন এবং জড়িত শরীরের সিস্টেম
- প্রাথমিক উদ্বেগের ক্ষেত্র

### ২. মূল অনুসন্ধান
- প্রধান পর্যবেক্ষণ
- উল্লেখিত কোনো অস্বাভাবিকতা

### ৩. বিশেষজ্ঞ রেফারেল সুপারিশ
- কোন বিশেষজ্ঞদের এই কেসটি মূল্যায়ন করা উচিত
- প্রতিটি বিশেষজ্ঞ কেন প্রাসঙ্গিক তার সংক্ষিপ্ত ব্যাখ্যা
- অগ্রাধিকার স্তর (জরুরি বনাম নিয়মিত)

বিশ্লেষণটি সংক্ষিপ্ত রাখুন এবং উপযুক্ত বিশেষজ্ঞ যত্নের দিকে পরিচালনার উপর ফোকাস করুন।"""
            }
        }
        
        return prompts[self.language][self.specialist_type]
    
    def analyze_image(self, image_path: str) -> str:
        """Analyze medical image using Groq's vision model"""
        
        if not self.client:
            return "API key not available" if self.language == "en" else "API কী উপলব্ধ নেই"
        
        try:
            # Get specialist-specific prompt
            prompt = self.get_specialist_prompt()
            
            # Encode image
            encoded_image = encode_image(image_path)
            
            # Analyze with Groq's vision model
            response = analyze_image_with_query(
                query=prompt,
                encoded_image=encoded_image,
                language=self.language
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Image analysis failed for {self.specialist_type}: {e}")
            error_msg = f"Analysis failed: {str(e)}" if self.language == "en" else f"বিশ্লেষণ ব্যর্থ: {str(e)}"
            return error_msg


class MedicalImagingAnalysisSystem:
    """Complete medical imaging analysis system with multiple specialists"""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.specialists = {
            "ophthalmology": MedicalImagingSpecialist("ophthalmology", language),
            "cardiology": MedicalImagingSpecialist("cardiology", language),
            "orthopedics": MedicalImagingSpecialist("orthopedics", language),
            "general_medicine": MedicalImagingSpecialist("general_medicine", language)
        }
    
    def get_specialist_names(self) -> Dict[str, str]:
        """Get specialist names in the current language"""
        
        if self.language == "bn":
            return {
                "ophthalmology": "চক্ষু বিশেষজ্ঞ",
                "cardiology": "হৃদরোগ বিশেষজ্ঞ", 
                "orthopedics": "অর্থোপেডিক বিশেষজ্ঞ",
                "general_medicine": "সাধারণ চিকিৎসক (প্রাথমিক মতামত)"
            }
        else:
            return {
                "ophthalmology": "Eye Specialist (Ophthalmologist)",
                "cardiology": "Heart Specialist (Cardiologist)",
                "orthopedics": "Bone & Joint Specialist",
                "general_medicine": "General Medicine Doctor (Initial Opinion)"
            }
    
    def analyze_with_multiple_specialists(self, image_path: str, selected_specialists: List[str]) -> Dict[str, str]:
        """Analyze image with selected specialists"""
        
        results = {}
        
        for specialist_key in selected_specialists:
            if specialist_key in self.specialists:
                specialist_name = self.get_specialist_names()[specialist_key]
                
                try:
                    with st.status(f"Analyzing with {specialist_name}..." if self.language == "en" 
                                 else f"{specialist_name} দ্বারা বিশ্লেষণ...", expanded=False):
                        
                        analysis = self.specialists[specialist_key].analyze_image(image_path)
                        results[specialist_name] = analysis
                        
                except Exception as e:
                    error_msg = f"Analysis failed: {str(e)}" if self.language == "en" else f"বিশ্লেষণ ব্যর্থ: {str(e)}"
                    results[specialist_name] = error_msg
                    logging.error(f"Specialist analysis failed for {specialist_key}: {e}")
        
        return results


def create_medical_imaging_analysis_interface(language: str = "English"):
    """Create the medical imaging analysis interface for Streamlit"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize the analysis system
    analysis_system = MedicalImagingAnalysisSystem(lang_code)
    specialist_names = analysis_system.get_specialist_names()
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🔬 মেডিকেল ইমেজিং বিশ্লেষণ</h1>
            <p style="margin: 5px 0 0 0;">একাধিক বিশেষজ্ঞ AI এজেন্ট দ্বারা উন্নত মেডিকেল ইমেজ বিশ্লেষণ</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🔬 Medical Imaging Analysis</h1>
            <p style="margin: 5px 0 0 0;">Advanced medical image analysis with multiple specialist AI agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features overview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if language == "Bengali":
            st.markdown("""
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>🌟 বৈশিষ্ট্যসমূহ</h3>
                <ul>
                    <li>👁️ চক্ষু বিশেষজ্ঞ বিশ্লেষণ</li>
                    <li>❤️ হৃদরোগ বিশেষজ্ঞ বিশ্লেষণ</li>
                    <li>🦴 অর্থোপেডিক বিশ্লেষণ</li>
                    <li>🩺 সাধারণ চিকিৎসা মতামত</li>
                    <li>🧠 উন্নত AI ভিশন মডেল</li>
                    <li>📊 বিস্তারিত রিপোর্ট</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>🌟 Features</h3>
                <ul>
                    <li>👁️ Ophthalmology Analysis</li>
                    <li>❤️ Cardiology Analysis</li>
                    <li>🦴 Orthopedic Analysis</li>
                    <li>🩺 General Medicine Opinion</li>
                    <li>🧠 Advanced AI Vision Models</li>
                    <li>📊 Detailed Reports</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if language == "Bengali":
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>📝 সাপোর্ট করা ইমেজ</h3>
                <ul>
                    <li>👁️ রেটিনাল ফটোগ্রাফি</li>
                    <li>❤️ ইকোকার্ডিওগ্রাম</li>
                    <li>🦴 এক্স-রে, MRI, CT</li>
                    <li>🩺 যেকোনো মেডিকেল ইমেজ</li>
                    <li>📷 JPG, PNG, BMP</li>
                    <li>⚡ তাৎক্ষণিক বিশ্লেষণ</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>📝 Supported Images</h3>
                <ul>
                    <li>👁️ Retinal Photography</li>
                    <li>❤️ Echocardiograms</li>
                    <li>🦴 X-rays, MRI, CT Scans</li>
                    <li>🩺 Any Medical Images</li>
                    <li>📷 JPG, PNG, BMP Formats</li>
                    <li>⚡ Instant Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Image upload section
    if language == "Bengali":
        st.markdown("## 📤 মেডিকেল ইমেজ আপলোড করুন")
        uploaded_file = st.file_uploader(
            "ইমেজ নির্বাচন করুন",
            type=['jpg', 'jpeg', 'png', 'bmp', 'gif'],
            help="যেকোনো মেডিকেল ইমেজ আপলোড করুন (রেটিনা, হার্ট, হাড় ইত্যাদি)"
        )
    else:
        st.markdown("## 📤 Upload Medical Image")
        uploaded_file = st.file_uploader(
            "Select Image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'gif'],
            help="Upload any medical image (retina, heart, bones, etc.)"
        )
    
    # Specialist selection and analysis
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Medical Image" if language == "English" else "আপলোড করা মেডিকেল ইমেজ", 
                    width='stretch')
        
        with col2:
            # Specialist selection
            if language == "Bengali":
                st.markdown("### 🩺 বিশেষজ্ঞ নির্বাচন করুন")
                st.write("কোন বিশেষজ্ঞদের মতামত চান?")
            else:
                st.markdown("### 🩺 Select Specialists")
                st.write("Which specialists would you like to consult?")
            
            # Create checkboxes for each specialist
            specialist_options = {}
            for key, name in specialist_names.items():
                specialist_options[key] = st.checkbox(name, value=False, key=f"specialist_{key}")
            
            # Analysis button
            if language == "Bengali":
                analyze_button = st.button("🔍 বিশ্লেষণ শুরু করুন", type="primary", width='stretch')
            else:
                analyze_button = st.button("🔍 Start Analysis", type="primary", width='stretch')
        
        # Perform analysis when button is clicked
        if analyze_button:
            selected_specialists = [key for key, selected in specialist_options.items() if selected]
            
            if not selected_specialists:
                if language == "Bengali":
                    st.error("⚠️ অন্তত একজন বিশেষজ্ঞ নির্বাচন করুন!")
                else:
                    st.error("⚠️ Please select at least one specialist!")
                return
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_image_path = tmp_file.name
            
            try:
                # Perform analysis
                if language == "Bengali":
                    st.markdown("## 📋 বিশ্লেষণ ফলাফল")
                else:
                    st.markdown("## 📋 Analysis Results")
                
                results = analysis_system.analyze_with_multiple_specialists(temp_image_path, selected_specialists)
                
                # Display results
                for specialist_name, analysis_result in results.items():
                    with st.expander(f"📊 {specialist_name}", expanded=True):
                        st.markdown(analysis_result)
                        
                        # Add download button for individual analysis
                        if language == "Bengali":
                            st.download_button(
                                label="📥 এই বিশ্লেষণ ডাউনলোড করুন",
                                data=analysis_result,
                                file_name=f"{specialist_name}_analysis.txt",
                                mime="text/plain",
                                key=f"download_{specialist_name}"
                            )
                        else:
                            st.download_button(
                                label="📥 Download This Analysis",
                                data=analysis_result,
                                file_name=f"{specialist_name}_analysis.txt",
                                mime="text/plain",
                                key=f"download_{specialist_name}"
                            )
                
                # Combined report download
                st.markdown("---")
                
                if language == "Bengali":
                    st.markdown("### 📄 সম্পূর্ণ রিপোর্ট")
                else:
                    st.markdown("### 📄 Complete Report")
                
                # Generate combined report
                combined_report = generate_combined_report(results, language)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if language == "Bengali":
                        st.download_button(
                            label="📥 সম্পূর্ণ রিপোর্ট ডাউনলোড করুন",
                            data=combined_report,
                            file_name="complete_medical_analysis.txt",
                            mime="text/plain",
                            type="primary"
                        )
                    else:
                        st.download_button(
                            label="📥 Download Complete Report",
                            data=combined_report,
                            file_name="complete_medical_analysis.txt",
                            mime="text/plain",
                            type="primary"
                        )
                
                with col2:
                    if language == "Bengali":
                        if st.button("🔄 নতুন বিশ্লেষণ", width='stretch'):
                            st.rerun()
                    else:
                        if st.button("🔄 New Analysis", width='stretch'):
                            st.rerun()
                
            except Exception as e:
                logging.error(f"Analysis failed: {e}")
                if language == "Bengali":
                    st.error(f"❌ বিশ্লেষণে সমস্যা হয়েছে: {str(e)}")
                else:
                    st.error(f"❌ Analysis failed: {str(e)}")
            
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_image_path)
                except:
                    pass
    
    # Additional information section
    st.markdown("---")
    
    if language == "Bengali":
        st.markdown("## ℹ️ গুরুত্বপূর্ণ তথ্য")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: #f8d7da; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545;">
                <h4 style="color: #721c24;">⚠️ চিকিৎসা সংক্রান্ত দাবিত্যাগ</h4>
                <p style="color: #721c24;">এই AI বিশ্লেষণ শুধুমাত্র তথ্যগত উদ্দেশ্যে। এটি পেশাদার চিকিৎসা পরামর্শ, নির্ণয় বা চিকিৎসার বিকল্প নয়। সর্বদা যোগ্য স্বাস্থ্যসেবা প্রদানকারীর সাথে পরামর্শ করুন।</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #d1ecf1; padding: 15px; border-radius: 10px; border-left: 5px solid #0c5460;">
                <h4 style="color: #0c5460;">🔒 গোপনীয়তা ও নিরাপত্তা</h4>
                <p style="color: #0c5460;">আপলোড করা সকল ইমেজ অস্থায়ীভাবে প্রক্রিয়াজাত হয় এবং বিশ্লেষণের পর স্বয়ংক্রিয়ভাবে মুছে ফেলা হয়। আমরা কোনো ব্যক্তিগত চিকিৎসা তথ্য সংরক্ষণ করি না।</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("## ℹ️ Important Information")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: #f8d7da; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545;">
                <h4 style="color: #721c24;">⚠️ Medical Disclaimer</h4>
                <p style="color: #721c24;">This AI analysis is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #d1ecf1; padding: 15px; border-radius: 10px; border-left: 5px solid #0c5460;">
                <h4 style="color: #0c5460;">🔒 Privacy & Security</h4>
                <p style="color: #0c5460;">All uploaded images are processed temporarily and automatically deleted after analysis. We do not store any personal medical information.</p>
            </div>
            """, unsafe_allow_html=True)


def generate_combined_report(results: Dict[str, str], language: str) -> str:
    """Generate a combined report from all specialist analyses"""
    
    if language == "Bengali":
        report = """
# সম্পূর্ণ মেডিকেল ইমেজিং বিশ্লেষণ রিপোর্ট

## রিপোর্ট তৈরির তারিখ: {}

---

""".format(str(uuid.uuid4())[:8])
        
        for specialist_name, analysis in results.items():
            report += f"""
## {specialist_name} এর বিশ্লেষণ

{analysis}

---

"""
        
        report += """
## গুরুত্বপূর্ণ নোট

⚠️ **চিকিৎসা সংক্রান্ত দাবিত্যাগ:** এই AI বিশ্লেষণ শুধুমাত্র তথ্যগত উদ্দেশ্যে। এটি পেশাদার চিকিৎসা পরামর্শ, নির্ণয় বা চিকিৎসার বিকল্প নয়। সর্বদা যোগ্য স্বাস্থ্যসেবা প্রদানকারীর সাথে পরামর্শ করুন।

🔒 **গোপনীয়তা:** এই রিপোর্টটি আপনার ব্যক্তিগত চিকিৎসা তথ্য। এটি সুরক্ষিত রাখুন এবং শুধুমাত্র আপনার চিকিৎসক ও বিশ্বস্ত ব্যক্তিদের সাথে শেয়ার করুন।

রিপোর্ট তৈরি: মেডিকেল ইমেজিং AI সিস্টেম
"""
    
    else:
        report = """
# Complete Medical Imaging Analysis Report

## Report Generated: {}

---

""".format(str(uuid.uuid4())[:8])
        
        for specialist_name, analysis in results.items():
            report += f"""
## {specialist_name} Analysis

{analysis}

---

"""
        
        report += """
## Important Notes

⚠️ **Medical Disclaimer:** This AI analysis is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers.

🔒 **Privacy:** This report contains your personal medical information. Keep it secure and only share with your doctors and trusted individuals.

Report Generated by: Medical Imaging AI System
"""
    
    return report


def main():
    """Main function to run the Streamlit application"""
    
    st.set_page_config(
        page_title="Medical Imaging Analysis",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Language selection in sidebar
    with st.sidebar:
        st.markdown("## 🌐 Language / ভাষা")
        language = st.selectbox(
            "Select Language / ভাষা নির্বাচন করুন:",
            ["English", "Bengali"],
            index=0
        )
        
        st.markdown("---")
        
        if language == "Bengali":
            st.markdown("""
            ## 📋 ব্যবহারের নির্দেশনা
            
            1. **ইমেজ আপলোড করুন** - যেকোনো মেডিকেল ইমেজ
            2. **বিশেষজ্ঞ নির্বাচন করুন** - একাধিক বিশেষজ্ঞ বেছে নিন
            3. **বিশ্লেষণ শুরু করুন** - AI বিশ্লেষণ দেখুন
            4. **রিপোর্ট ডাউনলোড করুন** - বিস্তারিত ফলাফল সংরক্ষণ করুন
            """)
        else:
            st.markdown("""
            ## 📋 How to Use
            
            1. **Upload Image** - Any medical image
            2. **Select Specialists** - Choose multiple experts
            3. **Start Analysis** - View AI analysis
            4. **Download Report** - Save detailed results
            """)
        
        st.markdown("---")
        
        if language == "Bengali":
            st.markdown("""
            ## 🔧 সিস্টেম তথ্য
            - **AI মডেল:** Labaid GPT Vision
            - **বিশেষজ্ঞতা:** ৪টি মেডিকেল ক্ষেত্র
            - **ভাষা সাপোর্ট:** ইংরেজি ও বাংলা
            - **নিরাপত্তা:** সম্পূর্ণ গোপনীয়
            """)
        else:
            st.markdown("""
            ## 🔧 System Info
            - **AI Model:** Labaid GPT Vision
            - **Specialties:** 4 Medical Fields
            - **Language Support:** English & Bengali
            - **Security:** Fully Private
            """)
    
    # Main interface
    create_medical_imaging_analysis_interface(language)


# if __name__ == "__main__":
#     main()