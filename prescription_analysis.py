# prescription_analysis.py - Cloud-friendly Prescription OCR and Analysis Module

import os
import logging
import tempfile
import base64
from typing import Dict, List, Optional, Tuple, Any
import streamlit as st
from datetime import datetime
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Try to import OCR libraries with graceful fallbacks
try:
    from PIL import Image, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    logging.info("EasyOCR is available")
except ImportError:
    EASYOCR_AVAILABLE = False
    logging.warning("EasyOCR not available")

# Tesseract is often not available in cloud environments
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    logging.info("Tesseract is available")
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract not available - this is normal for cloud deployment")

# Set up Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class PrescriptionAnalyzer:
    """Cloud-friendly prescription analysis with OCR and AI interpretation"""
    
    def __init__(self, language="en"):
        self.language = language
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        
        # Initialize OCR readers with error handling
        self.easyocr_reader = None
        if EASYOCR_AVAILABLE:
            try:
                # Support both English and Bengali
                languages = ['en', 'bn'] if language == "bn" else ['en']
                self.easyocr_reader = easyocr.Reader(languages, gpu=False)
                logging.info("EasyOCR reader initialized successfully")
            except Exception as e:
                logging.warning(f"EasyOCR initialization failed: {e}")
                self.easyocr_reader = None
    
    def extract_text_with_multiple_ocr(self, image_path: str) -> Dict[str, Any]:
        """Extract text using available OCR methods for cloud deployment"""
        
        results = {
            "extracted_texts": [],
            "confidence_scores": [],
            "methods_used": [],
            "best_result": "",
            "preprocessing_applied": False
        }
        
        # Preprocess image if PIL is available
        working_path = image_path
        if PIL_AVAILABLE:
            try:
                preprocessed_path = self.preprocess_image(image_path)
                results["preprocessing_applied"] = True
                working_path = preprocessed_path
            except Exception as e:
                logging.warning(f"Image preprocessing failed: {e}")
                working_path = image_path
        
        # Method 1: EasyOCR (Primary method for cloud)
        if self.easyocr_reader:
            try:
                easyocr_results = self.easyocr_reader.readtext(working_path)
                
                # Extract text and confidence
                extracted_text = []
                total_confidence = 0
                
                for (bbox, text, confidence) in easyocr_results:
                    if confidence > 0.3:  # Filter low confidence results
                        extracted_text.append(text)
                        total_confidence += confidence
                
                combined_text = ' '.join(extracted_text)
                avg_confidence = total_confidence / len(easyocr_results) if easyocr_results else 0
                
                results["extracted_texts"].append(combined_text)
                results["confidence_scores"].append(avg_confidence)
                results["methods_used"].append("EasyOCR")
                
                logging.info(f"EasyOCR extraction completed with {avg_confidence:.2f} confidence")
                
            except Exception as e:
                logging.error(f"EasyOCR failed: {e}")
        
        # Method 2: Labaid GPT API (Fallback method)
        try:
            vision_text = self.extract_with_groq_vision(image_path)
            if vision_text and len(vision_text.strip()) > 10:
                results["extracted_texts"].append(vision_text)
                results["confidence_scores"].append(0.8)  # Assume good confidence for API
                results["methods_used"].append("Labaid GPT")
                
                logging.info("Labaid GPT extraction completed")
                
        except Exception as e:
            logging.error(f"Labaid GPT extraction failed: {e}")
        
        # Select best result
        if results["extracted_texts"]:
            # Choose result with highest confidence and reasonable length
            best_index = 0
            best_score = 0
            
            for i, (text, confidence) in enumerate(zip(results["extracted_texts"], results["confidence_scores"])):
                # Score based on confidence and text length
                length_bonus = min(len(text.strip()) / 100, 1.0)  # Bonus for longer text
                score = confidence * 0.7 + length_bonus * 0.3
                
                if score > best_score:
                    best_score = score
                    best_index = i
            
            results["best_result"] = results["extracted_texts"][best_index]
        
        # Cleanup preprocessed image
        try:
            if results["preprocessing_applied"] and working_path != image_path and os.path.exists(working_path):
                os.unlink(working_path)
        except Exception as e:
            logging.warning(f"Cleanup failed: {e}")
        
        return results
    
    def preprocess_image(self, image_path: str) -> str:
        """Preprocess image for better OCR results (only if PIL available)"""
        if not PIL_AVAILABLE:
            return image_path
            
        try:
            # Open and enhance the image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image for better OCR
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply filter to reduce noise
            image = image.filter(ImageFilter.MedianFilter())
            
            # Save preprocessed image
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            image.save(preprocessed_path)
            
            return preprocessed_path
            
        except Exception as e:
            logging.error(f"Image preprocessing failed: {e}")
            return image_path
    
    def extract_with_groq_vision(self, image_path: str) -> str:
        """Extract text using Groq's vision capabilities"""
        
        if not self.client:
            return ""
        
        try:
            # Encode image
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create prompt for text extraction
            if self.language == "bn":
                extraction_prompt = """এই প্রেসক্রিপশনের ছবি থেকে সব টেক্সট নিষ্কাশন করুন। 
                
                বিশেষভাবে নিম্নলিখিত তথ্য খুঁজুন:
                - ডাক্তারের নাম ও যোগ্যতা
                - রোগীর নাম ও বয়স
                - ওষুধের নাম, ডোজ, ও খাওয়ার নিয়ম
                - তারিখ
                - অন্যান্য নির্দেশনা
                
                যদি হাতের লেখা অস্পষ্ট হয়, সম্ভাব্য শব্দগুলি লিখুন।"""
            else:
                extraction_prompt = """Extract all text from this prescription image.
                
                Pay special attention to:
                - Doctor's name and qualifications
                - Patient name and age
                - Medicine names, dosages, and instructions
                - Date
                - Any other instructions
                
                If handwriting is unclear, provide best guesses for the words."""
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": extraction_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}",
                            },
                        },
                    ],
                }
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model="meta-llama/llama-4-scout-17b-16e-instruct",  # Use vision model
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Groq vision extraction failed: {e}")
            return ""
    
    def analyze_prescription_content(self, extracted_text: str) -> Dict[str, Any]:
        """Analyze the extracted prescription text with AI"""
        
        if not self.client or not extracted_text.strip():
            return {"error": "No text to analyze or API not available"}
        
        try:
            # Create comprehensive analysis prompt
            analysis_prompt = self._get_prescription_analysis_prompt()
            
            user_prompt = f"""
            Please analyze this prescription text and provide a detailed breakdown:
            
            EXTRACTED PRESCRIPTION TEXT:
            {extracted_text}
            
            Provide a comprehensive analysis following the structure outlined in your instructions.
            """
            
            messages = [
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=DEFAULT_MODEL,
                temperature=0.3,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the structured response
            parsed_analysis = self._parse_prescription_analysis(analysis_text)
            
            return {
                "success": True,
                "raw_analysis": analysis_text,
                "structured_analysis": parsed_analysis,
                "extracted_text": extracted_text,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Prescription analysis failed: {e}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "extracted_text": extracted_text
            }
    
    def _get_prescription_analysis_prompt(self) -> str:
        """Get AI prompt for prescription analysis"""
        
        if self.language == "bn":
            return """আপনি একজন অভিজ্ঞ ফার্মাসিস্ট এবং চিকিৎসক যিনি প্রেসক্রিপশন বিশ্লেষণে বিশেষজ্ঞ।

আপনার কাজ প্রেসক্রিপশনের টেক্সট বিশ্লেষণ করে নিম্নলিখিত তথ্য প্রদান করা:

**১. প্রেসক্রিপশন তথ্য:**
- ডাক্তারের নাম ও যোগ্যতা
- রোগীর নাম, বয়স, লিঙ্গ
- তারিখ
- হাসপাতাল/ক্লিনিকের নাম

**২. ওষুধের বিশ্লেষণ:**
প্রতিটি ওষুধের জন্য:
- ওষুধের নাম (ব্র্যান্ড ও জেনেরিক)
- ডোজ ও শক্তি
- খাওয়ার নিয়ম (দিনে কতবার, কখন)
- কতদিনের জন্য
- ওষুধের ধরন (ট্যাবলেট, সিরাপ, ইনজেকশন)

**৩. চিকিৎসা বিশ্লেষণ:**
- কি রোগের জন্য এই ওষুধগুলি দেওয়া হয়েছে (সম্ভাব্য)
- ওষুধের কার্যকারিতা
- পার্শ্বপ্রতিক্রিয়ার সম্ভাবনা
- ওষুধের মধ্যে পারস্পরিক ক্রিয়া

**৪. সতর্কতা ও পরামর্শ:**
- গুরুত্বপূর্ণ সতর্কতা
- খাদ্য ও পানীয়ের সাথে সম্পর্ক
- মিস করলে কি করবেন
- কখন ডাক্তারের সাথে যোগাযোগ করবেন

**৫. সামগ্রিক মূল্যায়ন:**
- প্রেসক্রিপশনের গুণমান
- কোন তথ্য অস্পষ্ট বা অনুপস্থিত
- রোগীর জন্য অতিরিক্ত পরামর্শ

সর্বদা স্পষ্ট করুন যে এটি শুধুমাত্র তথ্যমূলক বিশ্লেষণ এবং ডাক্তারের পরামর্শের বিকল্প নয়।"""

        else:
            return """You are an experienced pharmacist and medical doctor specializing in prescription analysis.

Your task is to analyze prescription text and provide the following information:

**1. Prescription Information:**
- Doctor's name and qualifications
- Patient name, age, gender
- Date
- Hospital/clinic name

**2. Medication Analysis:**
For each medication:
- Medicine name (brand and generic)
- Dosage and strength
- Instructions (frequency, timing)
- Duration of treatment
- Form (tablet, syrup, injection, etc.)

**3. Medical Analysis:**
- Likely condition being treated
- How these medications work
- Potential side effects
- Drug interactions

**4. Warnings & Advice:**
- Important precautions
- Food and drink interactions
- What to do if dose is missed
- When to contact doctor

**5. Overall Assessment:**
- Quality of prescription
- Any unclear or missing information
- Additional advice for patient

Always clarify that this is informational analysis only and not a substitute for professional medical advice.

Structure your response clearly with headers and bullet points for easy reading."""
    
    def _parse_prescription_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse the AI analysis into structured format"""
        
        structured = {
            "prescription_info": {},
            "medications": [],
            "medical_analysis": {},
            "warnings": [],
            "assessment": {}
        }
        
        try:
            # Simple parser
            sections = re.split(r'\*\*\d+\.|\n\n', analysis_text)
            
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                
                # Extract key information patterns
                if "doctor" in section.lower() or "ডাক্তার" in section:
                    structured["prescription_info"]["doctor_section"] = section
                elif "medication" in section.lower() or "ওষুধ" in section:
                    structured["medications"].append(section)
                elif "warning" in section.lower() or "সতর্কতা" in section:
                    structured["warnings"].append(section)
                elif "assessment" in section.lower() or "মূল্যায়ন" in section:
                    structured["assessment"]["overall"] = section
            
        except Exception as e:
            logging.error(f"Error parsing analysis: {e}")
            structured["raw_text"] = analysis_text
        
        return structured
    
    def generate_prescription_report(self, analysis_results: Dict) -> str:
        """Generate a formatted prescription report"""
        
        if "error" in analysis_results:
            if self.language == "bn":
                return f"বিশ্লেষণে ত্রুটি: {analysis_results['error']}"
            else:
                return f"Analysis Error: {analysis_results['error']}"
        
        raw_analysis = analysis_results.get("raw_analysis", "")
        extracted_text = analysis_results.get("extracted_text", "")
        
        if self.language == "bn":
            report = f"""
# 📋 প্রেসক্রিপশন বিশ্লেষণ রিপোর্ট

## 🔍 নিষ্কাশিত টেক্সট:
```
{extracted_text}
```

## 🏥 বিস্তারিত বিশ্লেষণ:
{raw_analysis}

---
**⚠️ গুরুত্বপূর্ণ দাবিত্যাগ:** এই বিশ্লেষণ শুধুমাত্র তথ্যমূলক উদ্দেশ্যে। চিকিৎসা সংক্রান্ত যেকোনো সিদ্ধান্তের জন্য আপনার ডাক্তার বা ফার্মাসিস্টের সাথে পরামর্শ করুন।

**তারিখ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        else:
            report = f"""
# 📋 Prescription Analysis Report

## 🔍 Extracted Text:
```
{extracted_text}
```

## 🏥 Detailed Analysis:
{raw_analysis}

---
**⚠️ Important Disclaimer:** This analysis is for informational purposes only. Please consult your doctor or pharmacist for any medical decisions.

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report


def create_prescription_analysis_interface(language="English"):
    """Create the prescription analysis interface for Streamlit"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">📋 প্রেসক্রিপশন বিশ্লেষণ</h1>
            <p style="margin: 5px 0 0 0;">আপনার প্রেসক্রিপশনের ছবি আপলোড করুন এবং বিস্তারিত বিশ্লেষণ পান</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">📋 Prescription Analysis</h1>
            <p style="margin: 5px 0 0 0;">Upload your prescription image and get detailed analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display OCR status
    display_ocr_status(language)
    
    # Features info
    col1, col2 = st.columns(2)
    
    with col1:
        if language == "Bengali":
            st.markdown("""
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>🌟 বৈশিষ্ট্যসমূহ</h3>
                <ul>
                    <li>📸 হাতের লেখা পড়া (EasyOCR)</li>
                    <li>🔍 AI ভিশন বিশ্লেষণ</li>
                    <li>💊 ওষুধ বিশ্লেষণ</li>
                    <li>⚠️ পার্শ্বপ্রতিক্রিয়া সতর্কতা</li>
                    <li>📄 বিস্তারিত রিপোর্ট</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>🌟 Features</h3>
                <ul>
                    <li>📸 Handwriting Recognition (EasyOCR)</li>
                    <li>🔍 AI Vision Analysis</li>
                    <li>💊 Medication Analysis</li>
                    <li>⚠️ Side Effect Warnings</li>
                    <li>📄 Detailed Reports</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if language == "Bengali":
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>📝 টিপস</h3>
                <ul>
                    <li>ভাল আলোতে ছবি তুলুন</li>
                    <li>পুরো প্রেসক্রিপশন দৃশ্যমান হোক</li>
                    <li>ছবি ঝাপসা না হলে ভাল</li>
                    <li>JPG, PNG ফরম্যাট ব্যবহার করুন</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <h3>📝 Tips</h3>
                <ul>
                    <li>Take photo in good lighting</li>
                    <li>Ensure full prescription is visible</li>
                    <li>Avoid blurry images</li>
                    <li>Use JPG, PNG formats</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # File upload
    if language == "Bengali":
        uploaded_file = st.file_uploader(
            "📤 প্রেসক্রিপশনের ছবি আপলোড করুন",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="সমর্থিত ফরম্যাট: JPG, PNG, BMP, TIFF"
        )
    else:
        uploaded_file = st.file_uploader(
            "📤 Upload Prescription Image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Supported formats: JPG, PNG, BMP, TIFF"
        )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(uploaded_file, caption="Uploaded Prescription" if language == "English" else "আপলোড করা প্রেসক্রিপশন", width='stretch')
        
        # Analysis button
        if language == "Bengali":
            if st.button("🔍 প্রেসক্রিপশন বিশ্লেষণ করুন", type="primary", width='stretch'):
                analyze_uploaded_prescription(uploaded_file, language, lang_code)
        else:
            if st.button("🔍 Analyze Prescription", type="primary", width='stretch'):
                analyze_uploaded_prescription(uploaded_file, language, lang_code)


def analyze_uploaded_prescription(uploaded_file, language, lang_code):
    """Analyze the uploaded prescription with cloud-friendly approach"""
    
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            image_path = tmp_file.name
        
        # Initialize analyzer
        analyzer = PrescriptionAnalyzer(lang_code)
        
        # Step 1: OCR Text Extraction
        if language == "Bengali":
            with st.status("📸 ছবি থেকে টেক্সট নিষ্কাশন করা হচ্ছে...", expanded=True) as status:
                st.write("🔍 উপলব্ধ OCR পদ্ধতি ব্যবহার করা হচ্ছে...")
                ocr_results = analyzer.extract_text_with_multiple_ocr(image_path)
                
                if ocr_results["best_result"]:
                    st.write("✅ টেক্সট সফলভাবে নিষ্কাশিত")
                    status.update(label="📸 টেক্সট নিষ্কাশন সম্পন্ন!", state="complete")
                else:
                    st.write("❌ টেক্সট নিষ্কাশনে সমস্যা")
                    status.update(label="❌ টেক্সট নিষ্কাশন ব্যর্থ", state="error")
        else:
            with st.status("📸 Extracting text from image...", expanded=True) as status:
                st.write("🔍 Using available OCR methods...")
                ocr_results = analyzer.extract_text_with_multiple_ocr(image_path)
                
                if ocr_results["best_result"]:
                    st.write("✅ Text extracted successfully")
                    status.update(label="📸 Text extraction complete!", state="complete")
                else:
                    st.write("❌ Text extraction failed")
                    status.update(label="❌ Text extraction failed", state="error")
        
        # Display OCR results
        display_ocr_results(ocr_results, language)
        
        # Step 2: AI Analysis
        if ocr_results["best_result"]:
            if language == "Bengali":
                with st.status("🧠 প্রেসক্রিপশন বিশ্লেষণ করা হচ্ছে...", expanded=True) as status:
                    st.write("💊 ওষুধের তথ্য বিশ্লেষণ...")
                    st.write("⚠️ পার্শ্বপ্রতিক্রিয়া ও সতর্কতা চেক...")
                    st.write("📋 রিপোর্ট প্রস্তুত করা...")
                    
                    analysis_results = analyzer.analyze_prescription_content(ocr_results["best_result"])
                    
                    if analysis_results.get("success"):
                        st.write("✅ বিশ্লেষণ সম্পন্ন")
                        status.update(label="🧠 বিশ্লেষণ সম্পন্ন!", state="complete")
                    else:
                        st.write("❌ বিশ্লেষণে সমস্যা")
                        status.update(label="❌ বিশ্লেষণ ব্যর্থ", state="error")
            else:
                with st.status("🧠 Analyzing prescription...", expanded=True) as status:
                    st.write("💊 Analyzing medication information...")
                    st.write("⚠️ Checking side effects and warnings...")
                    st.write("📋 Preparing report...")
                    
                    analysis_results = analyzer.analyze_prescription_content(ocr_results["best_result"])
                    
                    if analysis_results.get("success"):
                        st.write("✅ Analysis completed")
                        status.update(label="🧠 Analysis complete!", state="complete")
                    else:
                        st.write("❌ Analysis failed")
                        status.update(label="❌ Analysis failed", state="error")
            
            # Display analysis results
            display_analysis_results(analysis_results, language)
            
            # Generate and offer report download
            if analysis_results.get("success"):
                report = analyzer.generate_prescription_report(analysis_results)
                
                if language == "Bengali":
                    st.download_button(
                        label="📥 বিশ্লেষণ রিপোর্ট ডাউনলোড করুন",
                        data=report,
                        file_name=f"prescription_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.download_button(
                        label="📥 Download Analysis Report",
                        data=report,
                        file_name=f"prescription_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
        
        # Cleanup
        os.unlink(image_path)
        
    except Exception as e:
        logging.error(f"Prescription analysis failed: {e}")
        if language == "Bengali":
            st.error(f"বিশ্লেষণে ত্রুটি: {str(e)}")
        else:
            st.error(f"Analysis error: {str(e)}")


def display_ocr_results(ocr_results, language):
    """Display OCR extraction results"""
    
    if language == "Bengali":
        st.markdown("## 📸 টেক্সট নিষ্কাশনের ফলাফল")
    else:
        st.markdown("## 📸 Text Extraction Results")
    
    # Show methods used and their results
    if ocr_results["methods_used"]:
        if language == "Bengali":
            st.markdown("### 🔍 ব্যবহৃত পদ্ধতি:")
        else:
            st.markdown("### 🔍 Methods Used:")
        
        for i, (method, confidence) in enumerate(zip(ocr_results["methods_used"], ocr_results["confidence_scores"])):
            confidence_color = "#4caf50" if confidence > 0.7 else "#ff9800" if confidence > 0.4 else "#f44336"
            
            st.markdown(f"""
            <div style="background: {confidence_color}20; padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 4px solid {confidence_color};">
                <strong>{method}</strong> - {'আত্মবিশ্বাস' if language == 'Bengali' else 'Confidence'}: {confidence:.2%}
            </div>
            """, unsafe_allow_html=True)
    
    # Show best extracted text
    if ocr_results["best_result"]:
        if language == "Bengali":
            st.markdown("### 📄 নিষ্কাশিত টেক্সট (সর্বোত্তম ফলাফল):")
        else:
            st.markdown("### 📄 Extracted Text (Best Result):")
        
        st.code(ocr_results["best_result"], language="text")
    else:
        if language == "Bengali":
            st.error("❌ কোন টেক্সট নিষ্কাশন করা যায়নি। ছবির গুণমান উন্নত করে আবার চেষ্টা করুন।")
        else:
            st.error("❌ No text could be extracted. Please try with a better quality image.")


def display_analysis_results(analysis_results, language):
    """Display prescription analysis results"""
    
    if "error" in analysis_results:
        if language == "Bengali":
            st.error(f"বিশ্লেষণে ত্রুটি: {analysis_results['error']}")
        else:
            st.error(f"Analysis Error: {analysis_results['error']}")
        return
    
    if not analysis_results.get("success"):
        if language == "Bengali":
            st.warning("বিশ্লেষণ সম্পন্ন হয়নি।")
        else:
            st.warning("Analysis not completed.")
        return
    
    # Main analysis display
    if language == "Bengali":
        st.markdown("## 🏥 প্রেসক্রিপশন বিশ্লেষণ")
    else:
        st.markdown("## 🏥 Prescription Analysis")
    
    # Display the AI analysis
    raw_analysis = analysis_results.get("raw_analysis", "")
    if raw_analysis:
        st.markdown(raw_analysis)
    
    # Important disclaimer
    if language == "Bengali":
        st.markdown("""
        <div style="background: #ffebee; padding: 20px; border-radius: 10px; border: 2px solid #f44336; margin: 20px 0;">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">⚠️ গুরুত্বপূর্ণ দাবিত্যাগ</h4>
            <p style="margin: 0;">এই বিশ্লেষণ শুধুমাত্র তথ্যমূলক উদ্দেশ্যে প্রদান করা হয়েছে। এটি পেশাদার চিকিৎসা পরামর্শ, রোগ নির্ণয় বা চিকিৎসার বিকল্প নয়। ওষুধ সেবন বা কোন চিকিৎসা সংক্রান্ত সিদ্ধান্তের জন্য সর্বদা আপনার ডাক্তার বা ফার্মাসিস্টের সাথে পরামর্শ করুন।</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #ffebee; padding: 20px; border-radius: 10px; border: 2px solid #f44336; margin: 20px 0;">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">⚠️ Important Disclaimer</h4>
            <p style="margin: 0;">This analysis is provided for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult your doctor or pharmacist for any medical decisions or medication-related questions.</p>
        </div>
        """, unsafe_allow_html=True)


def display_ocr_status(language):
    """Display OCR library availability status"""
    
    if language == "Bengali":
        st.markdown("## 🛠️ সিস্টেম স্থিতি")
    else:
        st.markdown("## 🛠️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if EASYOCR_AVAILABLE:
            st.success("✅ EasyOCR" + (" উপলব্ধ" if language == "Bengali" else " Available"))
        else:
            st.warning("⚠️ EasyOCR" + (" অনুপস্থিত" if language == "Bengali" else " Not Available"))
    
    with col2:
        if GROQ_API_KEY:
            st.success("✅ Labaid GPT" + (" উপলব্ধ" if language == "Bengali" else " Available"))
        else:
            st.warning("⚠️ Labaid GPT" + (" অনুপস্থিত" if language == "Bengali" else " Not Available"))
    
    with col3:
        if PIL_AVAILABLE:
            st.success("✅ Image Processing" + (" উপলব্ধ" if language == "Bengali" else " Available"))
        else:
            st.warning("⚠️ Image Processing" + (" সীমিত" if language == "Bengali" else " Limited"))
    
    # Show which methods are working
    if language == "Bengali":
        st.info("📋 **কার্যকর পদ্ধতি:** " + 
               ("EasyOCR + Labaid GPT" if EASYOCR_AVAILABLE and GROQ_API_KEY 
                else "শুধু Labaid GPT" if GROQ_API_KEY 
                else "শুধু EasyOCR" if EASYOCR_AVAILABLE 
                else "কোন OCR পদ্ধতি উপলব্ধ নেই"))
    else:
        st.info("📋 **Working Methods:** " + 
               ("EasyOCR + Labaid GPT" if EASYOCR_AVAILABLE and GROQ_API_KEY 
                else "Labaid GPT Only" if GROQ_API_KEY 
                else "EasyOCR Only" if EASYOCR_AVAILABLE 
                else "No OCR methods available"))