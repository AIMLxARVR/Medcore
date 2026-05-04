# cancer_consultation_system.py - Enhanced cancer-specific consultation with reasoning

import os
import logging
import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
from cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel

# Configure logging
logging.basicConfig(level=logging.INFO, git addformat='%(asctime)s - %(levelname)s - %(message)s')

class CancerConsultationSession:
    """Enhanced consultation session specifically for cancer domain"""
    
    def __init__(self, language="en"):
        self.language = language
        self.reasoning_engine = CancerReasoningEngine(language)
        self.consultation_data = {
            "patient_demographics": {},
            "symptoms": {},
            "risk_factors": {},
            "family_history": {},
            "lifestyle_factors": {},
            "current_stage": "initial",
            "consultation_complete": False
        }
        self.consultation_flow = [
            "demographics",
            "chief_complaint", 
            "symptom_details",
            "risk_factors",
            "family_history",
            "lifestyle_assessment",
            "comprehensive_analysis"
        ]
        self.current_step = 0
        
    def get_current_stage_info(self) -> Dict[str, Any]:
        """Get information about current consultation stage"""
        if self.current_step >= len(self.consultation_flow):
            return {
                "stage": "complete",
                "progress": 100,
                "next_question": None,
                "stage_description": "Consultation Complete" if self.language == "en" else "পরামর্শ সম্পন্ন"
            }
        
        current_stage = self.consultation_flow[self.current_step]
        progress = (self.current_step / len(self.consultation_flow)) * 100
        
        stage_descriptions = {
            "en": {
                "demographics": "Basic Information",
                "chief_complaint": "Main Concern",
                "symptom_details": "Symptom Analysis", 
                "risk_factors": "Risk Assessment",
                "family_history": "Family History",
                "lifestyle_assessment": "Lifestyle Factors",
                "comprehensive_analysis": "Final Analysis"
            },
            "bn": {
                "demographics": "মৌলিক তথ্য",
                "chief_complaint": "প্রধান সমস্যা",
                "symptom_details": "লক্ষণ বিশ্লেষণ",
                "risk_factors": "ঝুঁকি মূল্যায়ন", 
                "family_history": "পারিবারিক ইতিহাস",
                "lifestyle_assessment": "জীবনযাত্রার কারণ",
                "comprehensive_analysis": "চূড়ান্ত বিশ্লেষণ"
            }
        }
        
        return {
            "stage": current_stage,
            "progress": progress,
            "next_question": self._get_stage_question(current_stage),
            "stage_description": stage_descriptions[self.language][current_stage]
        }
    
    def process_user_response(self, user_input: str) -> Dict[str, Any]:
        """Process user response and advance consultation"""
        
        if self.current_step >= len(self.consultation_flow):
            return self._generate_final_response()
        
        current_stage = self.consultation_flow[self.current_step]
        
        # Store the response in appropriate section
        self._store_response(current_stage, user_input)
        
        # Advance to next stage
        self.current_step += 1
        
        # Check if consultation is complete
        if self.current_step >= len(self.consultation_flow):
            return self._generate_comprehensive_analysis()
        else:
            return self._get_next_stage_response()
    
    def _get_stage_question(self, stage: str) -> str:
        """Get question for specific consultation stage"""
        
        questions = {
            "en": {
                "demographics": "Please tell me your age, gender, and current location. Also, do you have any ongoing medical conditions or take any medications regularly?",
                
                "chief_complaint": "What is your main health concern that brought you here today? Please describe your symptoms in detail.",
                
                "symptom_details": """Let me ask about specific symptoms. Please answer yes/no and provide details if yes:
                
                1. Do you have any persistent cough or breathing difficulties?
                2. Have you noticed any unusual lumps or masses anywhere on your body?
                3. Have you experienced unexplained weight loss (more than 5 kg in 6 months)?
                4. Do you have any unusual bleeding or discharge?
                5. Have you noticed any changes in your skin, moles, or existing marks?
                6. Are you experiencing persistent fatigue or weakness?
                7. Do you have any persistent pain that doesn't go away?""",
                
                "risk_factors": """Now I need to assess your cancer risk factors:
                
                1. Do you currently smoke or have you smoked in the past? If yes, for how long?
                2. Do you consume alcohol regularly? If yes, how much per week?
                3. What is your typical diet like? (fruits/vegetables vs processed foods)
                4. Do you get regular sun exposure or use tanning beds?
                5. Have you been exposed to any chemicals, radiation, or occupational hazards?
                6. For women: Age at first menstruation, pregnancies, breastfeeding history?""",
                
                "family_history": """Family history is important for cancer risk:
                
                1. Has anyone in your immediate family (parents, siblings, children) been diagnosed with cancer?
                2. If yes, what type of cancer and at what age?
                3. Do you know of any family members with breast, ovarian, colorectal, or prostate cancer?
                4. Are there any known genetic conditions in your family?""",
                
                "lifestyle_assessment": """Finally, let me understand your lifestyle:
                
                1. How would you describe your stress levels (low, moderate, high)?
                2. Do you exercise regularly? What type and how often?
                3. How many hours of sleep do you typically get?
                4. Do you have regular medical check-ups and screenings?
                5. Are you up to date with recommended cancer screenings for your age?"""
            },
            
            "bn": {
                "demographics": "অনুগ্রহ করে আপনার বয়স, লিঙ্গ এবং বর্তমান অবস্থান বলুন। এছাড়াও, আপনার কি কোন চলমান চিকিৎসা সমস্যা আছে বা নিয়মিত কোন ওষুধ খান?",
                
                "chief_complaint": "আজ আপনাকে এখানে নিয়ে এসেছে এমন প্রধান স্বাস্থ্য সমস্যা কী? অনুগ্রহ করে আপনার লক্ষণগুলি বিস্তারিত বর্ণনা করুন।",
                
                "symptom_details": """নির্দিষ্ট লক্ষণ সম্পর্কে জিজ্ঞাসা করি। অনুগ্রহ করে হ্যাঁ/না উত্তর দিন এবং হ্যাঁ হলে বিস্তারিত বলুন:
                
                ১. আপনার কি অবিরাম কাশি বা শ্বাসকষ্ট আছে?
                ২. আপনি কি শরীরের কোথাও অস্বাভাবিক গাঁট বা পিণ্ড লক্ষ্য করেছেন?
                ৩. আপনি কি অব্যাখ্যাত ওজন হ্রাস অনুভব করেছেন (৬ মাসে ৫ কেজির বেশি)?
                ৪. আপনার কি কোন অস্বাভাবিক রক্তপাত বা স্রাব আছে?
                ৫. আপনি কি আপনার ত্বক, তিল বা বিদ্যমান দাগে কোন পরিবর্তন লক্ষ্য করেছেন?
                ৬. আপনি কি ক্রমাগত ক্লান্তি বা দুর্বলতা অনুভব করছেন?
                ৭. আপনার কি এমন কোন ব্যথা আছে যা যায় না?""",
                
                "risk_factors": """এখন আমার আপনার ক্যান্সারের ঝুঁকির কারণগুলি মূল্যায়ন করতে হবে:
                
                ১. আপনি কি বর্তমানে ধূমপান করেন বা অতীতে করেছেন? হ্যাঁ হলে, কত দিন ধরে?
                ২. আপনি কি নিয়মিত মদ্যপান করেন? হ্যাঁ হলে, সপ্তাহে কতটুকু?
                ৩. আপনার সাধারণ খাদ্যাভ্যাস কেমন? (ফল/সবজি বনাম প্রক্রিয়াজাত খাবার)
                ৪. আপনি কি নিয়মিত রোদে থাকেন বা ট্যানিং বেড ব্যবহার করেন?
                ৫. আপনি কি কোন রাসায়নিক, বিকিরণ বা পেশাগত ঝুঁকির সম্মুখীন হয়েছেন?
                ৬. মহিলাদের জন্য: প্রথম ঋতুস্রাবের বয়স, গর্ভধারণ, বুকের দুধ খাওয়ানোর ইতিহাস?""",
                
                "family_history": """পারিবারিক ইতিহাস ক্যান্সারের ঝুঁকির জন্য গুরুত্বপূর্ণ:
                
                ১. আপনার নিকট পরিবারের কেউ (বাবা-মা, ভাইবোন, সন্তান) কি ক্যান্সারে আক্রান্ত হয়েছেন?
                ২. হ্যাঁ হলে, কি ধরনের ক্যান্সার এবং কত বয়সে?
                ৩. আপনার পরিবারে কি স্তন, ডিম্বাশয়, কোলোরেক্টাল বা প্রোস্টেট ক্যান্সারের কোন সদস্য আছেন?
                ৪. আপনার পরিবারে কি কোন জানা জেনেটিক রোগ আছে?""",
                
                "lifestyle_assessment": """অবশেষে, আমাকে আপনার জীবনযাত্রা বুঝতে দিন:
                
                ১. আপনি আপনার মানসিক চাপের মাত্রা কীভাবে বর্ণনা করবেন (কম, মধ্যম, উচ্চ)?
                ২. আপনি কি নিয়মিত ব্যায়াম করেন? কি ধরনের এবং কত ঘন ঘন?
                ৩. আপনি সাধারণত কত ঘন্টা ঘুমান?
                ৪. আপনার কি নিয়মিত চিকিৎসা পরীক্ষা এবং স্ক্রিনিং হয়?
                ৫. আপনার বয়সের জন্য সুপারিশকৃত ক্যান্সার স্ক্রিনিংগুলি কি আপ টু ডেট?"""
            }
        }
        
        return questions[self.language].get(stage, "Please provide more information.")
    
    def _store_response(self, stage: str, response: str):
        """Store user response in appropriate consultation data section"""
        
        if stage == "demographics":
            self.consultation_data["patient_demographics"]["raw_response"] = response
            # Parse basic demographics
            self._parse_demographics(response)
            
        elif stage == "chief_complaint":
            self.consultation_data["symptoms"]["chief_complaint"] = response
            
        elif stage == "symptom_details":
            self.consultation_data["symptoms"]["detailed_symptoms"] = response
            
        elif stage == "risk_factors":
            self.consultation_data["risk_factors"]["raw_response"] = response
            self._parse_risk_factors(response)
            
        elif stage == "family_history":
            self.consultation_data["family_history"]["raw_response"] = response
            
        elif stage == "lifestyle_assessment":
            self.consultation_data["lifestyle_factors"]["raw_response"] = response
    
    def _parse_demographics(self, response: str):
        """Parse demographics from user response"""
        # Simple parsing - can be enhanced with NLP
        demographics = {}
        
        # Extract age
        import re
        age_match = re.search(r'\b(\d{1,3})\s*(year|বছর)', response.lower())
        if age_match:
            demographics["age"] = int(age_match.group(1))
        
        # Extract gender
        if any(word in response.lower() for word in ["male", "man", "পুরুষ"]):
            demographics["gender"] = "male"
        elif any(word in response.lower() for word in ["female", "woman", "মহিলা", "নারী"]):
            demographics["gender"] = "female"
        
        self.consultation_data["patient_demographics"].update(demographics)
    
    def _parse_risk_factors(self, response: str):
        """Parse risk factors from user response"""
        risk_factors = {}
        
        # Smoking
        if any(word in response.lower() for word in ["smoke", "smoking", "cigarette", "ধূমপান", "সিগারেট"]):
            risk_factors["smoking"] = True
        
        # Alcohol
        if any(word in response.lower() for word in ["alcohol", "drink", "beer", "wine", "মদ", "মদ্যপান"]):
            risk_factors["heavy_drinking"] = True
        
        # Sun exposure
        if any(word in response.lower() for word in ["sun", "tanning", "রোদ"]):
            risk_factors["excessive_sun_exposure"] = True
        
        self.consultation_data["risk_factors"].update(risk_factors)
    
    def _get_next_stage_response(self) -> Dict[str, Any]:
        """Get response for next consultation stage"""
        stage_info = self.get_current_stage_info()
        
        if self.language == "bn":
            response_text = f"""ধন্যবাদ! আপনার তথ্য সংরক্ষিত হয়েছে।

📋 **পরবর্তী বিভাগ: {stage_info['stage_description']}**

{stage_info['next_question']}

অনুগ্রহ করে বিস্তারিত উত্তর দিন।"""
        else:
            response_text = f"""Thank you! Your information has been recorded.

📋 **Next Section: {stage_info['stage_description']}**

{stage_info['next_question']}

Please provide detailed answers."""
        
        return {
            "response": response_text,
            "stage_info": stage_info,
            "consultation_complete": False
        }
    
    def _generate_comprehensive_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive cancer risk analysis using reasoning engine"""
        
        try:
            # Step 1: Analyze symptoms
            symptoms_data = {
                "description": f"{self.consultation_data['symptoms'].get('chief_complaint', '')} {self.consultation_data['symptoms'].get('detailed_symptoms', '')}",
                "severity": 5,  # Default, can be enhanced
                "duration": "unknown"  # Can be parsed from responses
            }
            
            symptoms_analysis = self.reasoning_engine.analyze_symptoms(symptoms_data)
            
            # Step 2: Assess risk factors
            patient_data = {
                **self.consultation_data["patient_demographics"],
                **self.consultation_data["risk_factors"],
                "family_history_cancer": "family history" in self.consultation_data["family_history"].get("raw_response", "").lower()
            }
            
            risk_assessment = self.reasoning_engine.assess_risk_factors(patient_data)
            
            # Step 3: Generate differential diagnosis
            differential_diagnosis = self.reasoning_engine.generate_differential_diagnosis(
                symptoms_analysis, risk_assessment
            )
            
            # Step 4: Generate recommendations
            recommendations = self.reasoning_engine.generate_comprehensive_recommendations(
                symptoms_analysis, risk_assessment, differential_diagnosis
            )
            
            # Step 5: Generate human-readable response
            analysis_results = {
                "symptoms_analysis": symptoms_analysis,
                "risk_assessment": risk_assessment,
                "differential_diagnosis": differential_diagnosis,
                "recommendations": recommendations,
                "consultation_data": self.consultation_data
            }
            
            comprehensive_response = self.reasoning_engine.generate_llm_enhanced_response(analysis_results)
            
            # Step 6: Get reasoning explanation
            reasoning_explanation = self.reasoning_engine.get_reasoning_explanation()
            
            self.consultation_data["consultation_complete"] = True
            
            return {
                "response": comprehensive_response,
                "analysis_results": analysis_results,
                "reasoning_explanation": reasoning_explanation,
                "consultation_complete": True,
                "urgency_level": self._determine_urgency_level(symptoms_analysis, risk_assessment)
            }
            
        except Exception as e:
            logging.error(f"Error in comprehensive analysis: {e}")
            
            error_message = (
                "দুঃখিত, বিশ্লেষণে একটি ত্রুটি হয়েছে। অনুগ্রহ করে একজন যোগ্য চিকিৎসকের সাথে পরামর্শ করুন।"
                if self.language == "bn" else
                "Sorry, there was an error in the analysis. Please consult with a qualified healthcare provider."
            )
            
            return {
                "response": error_message,
                "consultation_complete": True,
                "error": True
            }
    
    def _determine_urgency_level(self, symptoms_analysis: Dict, risk_assessment: Dict) -> str:
        """Determine urgency level based on analysis"""
        urgency_score = symptoms_analysis.get("urgency_score", 0)
        requires_immediate = symptoms_analysis.get("requires_immediate_attention", False)
        high_risk_cancers = risk_assessment.get("high_risk_cancers", [])
        
        if requires_immediate or urgency_score >= 8:
            return "CRITICAL"
        elif urgency_score >= 6 or len(high_risk_cancers) > 0:
            return "HIGH"
        elif urgency_score >= 4:
            return "MODERATE"
        else:
            return "LOW"
    
    def get_consultation_summary(self) -> Dict[str, Any]:
        """Get summary of consultation for export"""
        return {
            "consultation_date": datetime.now().isoformat(),
            "language": self.language,
            "stages_completed": self.current_step,
            "total_stages": len(self.consultation_flow),
            "consultation_data": self.consultation_data,
            "completion_status": "complete" if self.consultation_data["consultation_complete"] else "in_progress"
        }
    
    def reset_consultation(self):
        """Reset consultation for new session"""
        self.consultation_data = {
            "patient_demographics": {},
            "symptoms": {},
            "risk_factors": {},
            "family_history": {},
            "lifestyle_factors": {},
            "current_stage": "initial",
            "consultation_complete": False
        }
        self.current_step = 0
        self.reasoning_engine.reset_reasoning_trace()


def create_cancer_consultation_interface(language="English"):
    """Create cancer-specific consultation interface for Streamlit"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize consultation session
    session_key = f'cancer_consultation_{lang_code}'
    if session_key not in st.session_state:
        st.session_state[session_key] = CancerConsultationSession(lang_code)
    
    consultation = st.session_state[session_key]
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🎯 ক্যান্সার বিশেষজ্ঞ পরামর্শ</h1>
            <p style="margin: 5px 0 0 0;">উন্নত যুক্তি ও বিশ্লেষণ সহ বিস্তারিত ক্যান্সার ঝুঁকি মূল্যায়ন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🎯 Cancer Specialist Consultation</h1>
            <p style="margin: 5px 0 0 0;">Comprehensive cancer risk assessment with advanced reasoning and analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show consultation progress
    stage_info = consultation.get_current_stage_info()
    
    if not consultation.consultation_data["consultation_complete"]:
        # Progress bar
        progress_bar = st.progress(stage_info["progress"] / 100)
        
        if language == "Bengali":
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 15px; border-radius: 10px; margin: 15px 0; 
                        border-left: 4px solid #2196f3;">
                <strong>📋 বর্তমান পর্যায়:</strong> {stage_info['stage_description']}<br>
                <strong>📊 অগ্রগতি:</strong> {stage_info['progress']:.1f}% সম্পন্ন
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 15px; border-radius: 10px; margin: 15px 0; 
                        border-left: 4px solid #2196f3;">
                <strong>📋 Current Stage:</strong> {stage_info['stage_description']}<br>
                <strong>📊 Progress:</strong> {stage_info['progress']:.1f}% Complete
            </div>
            """, unsafe_allow_html=True)
        
        # Display current question
        if stage_info["next_question"]:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 10px; 
                        border: 2px solid #ff6b6b; margin: 15px 0;">
                <h3 style="color: #ff6b6b; margin-top: 0;">
                    🏥 {'ডাক্তারের প্রশ্ন' if language == 'Bengali' else 'Doctor\'s Question'}:
                </h3>
                <p style="white-space: pre-line; line-height: 1.6;">{stage_info["next_question"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Input area
        user_input = st.text_area(
            "💭 আপনার উত্তর এখানে টাইপ করুন..." if language == "Bengali" else "💭 Type your answer here...",
            height=150,
            key=f"cancer_consultation_input_{lang_code}_{consultation.current_step}",
            placeholder="বিস্তারিত উত্তর দিন..." if language == "Bengali" else "Please provide detailed answers..."
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if language == "Bengali":
                submit_button = st.button(
                    "📤 উত্তর জমা দিন", 
                    type="primary", 
                    use_container_width=True,
                    disabled=not user_input or not user_input.strip()
                )
            else:
                submit_button = st.button(
                    "📤 Submit Answer", 
                    type="primary", 
                    use_container_width=True,
                    disabled=not user_input or not user_input.strip()
                )
        
        # Process submission
        if submit_button and user_input and user_input.strip():
            with st.spinner("🔬 আপনার উত্তর বিশ্লেষণ করা হচ্ছে..." if language == "Bengali" else "🔬 Analyzing your response..."):
                result = consultation.process_user_response(user_input.strip())
                st.rerun()
    
    else:
        # Show consultation results
        display_consultation_results(consultation, language)
    
    # Sidebar with consultation info
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h3 style="margin: 0;">{'পরামর্শ তথ্য' if language == 'Bengali' else 'Consultation Info'}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if language == "Bengali":
            st.markdown(f"""
            **📊 অগ্রগতি:** {stage_info['progress']:.1f}%  
            **📋 পর্যায়:** {stage_info['stage_description']}  
            **🎯 বিশেষত্ব:** ক্যান্সার ঝুঁকি মূল্যায়ন  
            **🧠 এআই:** উন্নত যুক্তি ইঞ্জিন
            """)
        else:
            st.markdown(f"""
            **📊 Progress:** {stage_info['progress']:.1f}%  
            **📋 Stage:** {stage_info['stage_description']}  
            **🎯 Specialty:** Cancer Risk Assessment  
            **🧠 AI:** Advanced Reasoning Engine
            """)
        
        st.markdown("---")
        
        # Reset button
        if language == "Bengali":
            if st.button("🔄 নতুন পরামর্শ শুরু করুন", use_container_width=True):
                consultation.reset_consultation()
                st.rerun()
        else:
            if st.button("🔄 Start New Consultation", use_container_width=True):
                consultation.reset_consultation()
                st.rerun()
        
        # Export consultation data
        if consultation.consultation_data["consultation_complete"]:
            consultation_summary = consultation.get_consultation_summary()
            
            if language == "Bengali":
                st.download_button(
                    label="📥 পরামর্শ ডাউনলোড করুন",
                    data=json.dumps(consultation_summary, indent=2, ensure_ascii=False),
                    file_name=f"cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.download_button(
                    label="📥 Download Consultation",
                    data=json.dumps(consultation_summary, indent=2),
                    file_name=f"cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )


def display_consultation_results(consultation: CancerConsultationSession, language: str):
    """Display comprehensive consultation results with reasoning"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ পরামর্শ সম্পন্ন</h2>
            <p style="margin: 5px 0 0 0;">বিস্তারিত বিশ্লেষণ ও সুপারিশ প্রস্তুত</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ Consultation Complete</h2>
            <p style="margin: 5px 0 0 0;">Comprehensive analysis and recommendations ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get the last analysis result from reasoning engine
    if hasattr(consultation.reasoning_engine, 'reasoning_trace') and consultation.reasoning_engine.reasoning_trace:
        
        # Create tabs for different sections
        if language == "Bengali":
            tab1, tab2, tab3, tab4 = st.tabs([
                "🏥 চিকিৎসা পরামর্শ", 
                "🧠 যুক্তি বিশ্লেষণ", 
                "📊 ঝুঁকি মূল্যায়ন", 
                "📋 সুপারিশ"
            ])
        else:
            tab1, tab2, tab3, tab4 = st.tabs([
                "🏥 Medical Analysis", 
                "🧠 Reasoning Process", 
                "📊 Risk Assessment", 
                "📋 Recommendations"
            ])
        
        with tab1:
            display_medical_analysis(consultation, language)
        
        with tab2:
            display_reasoning_process(consultation, language)
        
        with tab3:
            display_risk_assessment(consultation, language)
        
        with tab4:
            display_recommendations(consultation, language)
    
    else:
        if language == "Bengali":
            st.error("বিশ্লেষণ ডেটা পাওয়া যায়নি। অনুগ্রহ করে আবার চেষ্টা করুন।")
        else:
            st.error("Analysis data not available. Please try again.")


def display_medical_analysis(consultation: CancerConsultationSession, language: str):
    """Display medical analysis results"""
    
    # This would contain the comprehensive LLM response
    if language == "Bengali":
        st.markdown("### 🏥 বিস্তারিত চিকিৎসা বিশ্লেষণ")
        
        # Sample analysis display (replace with actual LLM response)
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff;">
            <p>আপনার প্রদত্ত তথ্যের ভিত্তিতে একটি বিস্তারিত বিশ্লেষণ এখানে প্রদর্শিত হবে। 
            এতে অন্তর্ভুক্ত থাকবে:</p>
            <ul>
                <li>লক্ষণ বিশ্লেষণ</li>
                <li>সম্ভাব্য রোগ নির্ণয়</li>
                <li>ঝুঁকি মূল্যায়ন</li>
                <li>পরবর্তী পদক্ষেপ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 🏥 Comprehensive Medical Analysis")
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff;">
            <p>Based on the information you provided, a detailed analysis will be displayed here, including:</p>
            <ul>
                <li>Symptom Analysis</li>
                <li>Differential Diagnosis</li>
                <li>Risk Assessment</li>
                <li>Next Steps</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def display_reasoning_process(consultation: CancerConsultationSession, language: str):
    """Display AI reasoning process"""
    
    if language == "Bengali":
        st.markdown("### 🧠 AI যুক্তি প্রক্রিয়া")
    else:
        st.markdown("### 🧠 AI Reasoning Process")
    
    reasoning_explanation = consultation.reasoning_engine.get_reasoning_explanation()
    
    if reasoning_explanation and reasoning_explanation.get("step_details"):
        for i, step in enumerate(reasoning_explanation["step_details"], 1):
            with st.expander(f"পদক্ষেপ {i}: {step['step'].replace('_', ' ').title()}" if language == "Bengali" 
                           else f"Step {i}: {step['step'].replace('_', ' ').title()}"):
                
                st.markdown(f"**{'যুক্তি' if language == 'Bengali' else 'Reasoning'}:** {step['reasoning']}")
                st.markdown(f"**{'আত্মবিশ্বাস' if language == 'Bengali' else 'Confidence'}:** {step['confidence']:.2f}")
                st.markdown(f"**{'সময়' if language == 'Bengali' else 'Timestamp'}:** {step['timestamp']}")
        
        # Overall confidence
        overall_confidence = reasoning_explanation.get("overall_confidence", 0)
        confidence_color = "#4caf50" if overall_confidence > 0.8 else "#ff9800" if overall_confidence > 0.6 else "#f44336"
        
        st.markdown(f"""
        <div style="background: {confidence_color}20; padding: 15px; border-radius: 10px; border-left: 4px solid {confidence_color}; margin-top: 15px;">
            <strong>{'সামগ্রিক আত্মবিশ্বাস' if language == 'Bengali' else 'Overall Confidence'}:</strong> {overall_confidence:.2f} 
            ({('উচ্চ' if overall_confidence > 0.8 else 'মধ্যম' if overall_confidence > 0.6 else 'কম') if language == 'Bengali' 
              else ('High' if overall_confidence > 0.8 else 'Moderate' if overall_confidence > 0.6 else 'Low')})
        </div>
        """, unsafe_allow_html=True)
    
    else:
        if language == "Bengali":
            st.info("যুক্তি প্রক্রিয়া ডেটা উপলব্ধ নেই।")
        else:
            st.info("Reasoning process data not available.")


def display_risk_assessment(consultation: CancerConsultationSession, language: str):
    """Display risk assessment visualization"""
    
    if language == "Bengali":
        st.markdown("### 📊 ক্যান্সার ঝুঁকি মূল্যায়ন")
    else:
        st.markdown("### 📊 Cancer Risk Assessment")
    
    # Sample risk data (replace with actual analysis)
    risk_data = {
        "breast_cancer": {"risk_level": "moderate", "risk_score": 0.4},
        "lung_cancer": {"risk_level": "low", "risk_score": 0.2},
        "colorectal_cancer": {"risk_level": "low", "risk_score": 0.3}
    }
    
    for cancer_type, risk_info in risk_data.items():
        risk_score = risk_info["risk_score"]
        risk_level = risk_info["risk_level"]
        
        # Color coding for risk levels
        color_map = {
            "low": "#4caf50",
            "moderate": "#ff9800", 
            "high": "#f44336",
            "critical": "#d32f2f"
        }
        
        color = color_map.get(risk_level, "#757575")
        
        cancer_name = cancer_type.replace("_", " ").title()
        if language == "Bengali":
            cancer_translations = {
                "Breast Cancer": "স্তন ক্যান্সার",
                "Lung Cancer": "ফুসফুস ক্যান্সার", 
                "Colorectal Cancer": "কোলোরেক্টাল ক্যান্সার"
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


def display_recommendations(consultation: CancerConsultationSession, language: str):
    """Display recommendations and next steps"""
    
    if language == "Bengali":
        st.markdown("### 📋 সুপারিশ ও পরবর্তী পদক্ষেপ")
    else:
        st.markdown("### 📋 Recommendations & Next Steps")
    
    # Sample recommendations (replace with actual analysis)
    recommendations = {
        "immediate_actions": [
            "Schedule appointment with primary care physician",
            "Keep a symptom diary"
        ],
        "diagnostic_tests": [
            "Complete Blood Count (CBC)",
            "Chest X-ray",
            "Cancer marker tests"
        ],
        "lifestyle_modifications": [
            "Quit smoking if applicable",
            "Increase physical activity",
            "Maintain healthy diet"
        ],
        "follow_up_schedule": [
            "Follow-up in 2 weeks",
            "Quarterly check-ups"
        ]
    }
    
    recommendation_titles = {
        "en": {
            "immediate_actions": "🚨 Immediate Actions",
            "diagnostic_tests": "🔬 Recommended Tests", 
            "lifestyle_modifications": "🌱 Lifestyle Changes",
            "follow_up_schedule": "📅 Follow-up Schedule"
        },
        "bn": {
            "immediate_actions": "🚨 তাৎক্ষণিক পদক্ষেপ",
            "diagnostic_tests": "🔬 সুপারিশকৃত পরীক্ষা",
            "lifestyle_modifications": "🌱 জীবনযাত্রার পরিবর্তন", 
            "follow_up_schedule": "📅 ফলো-আপ সময়সূচী"
        }
    }
    
    lang_key = "bn" if language == "Bengali" else "en"
    
    for category, items in recommendations.items():
        if items:
            title = recommendation_titles[lang_key][category]
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4 style="color: #007bff; margin: 0 0 10px 0;">{title}</h4>
                <ul style="margin: 0; padding-left: 20px;">
            """, unsafe_allow_html=True)
            
            for item in items:
                st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Emergency warning
    if language == "Bengali":
        st.markdown("""
        <div style="background: #ffebee; padding: 20px; border-radius: 10px; border: 2px solid #f44336; margin: 20px 0;">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">🚨 জরুরি সতর্কতা</h4>
            <p style="margin: 0;">যদি আপনি এই লক্ষণগুলির কোনটি অনুভব করেন তাহলে অবিলম্বে চিকিৎসা সহায়তা নিন:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li>গুরুতর ব্যথা</li>
                <li>অতিরিক্ত রক্তপাত</li>
                <li>শ্বাসকষ্ট</li>
                <li>অজ্ঞান হয়ে যাওয়া</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #ffebee; padding: 20px; border-radius: 10px; border: 2px solid #f44336; margin: 20px 0;">
            <h4 style="color: #d32f2f; margin: 0 0 10px 0;">🚨 Emergency Warning</h4>
            <p style="margin: 0;">Seek immediate medical attention if you experience any of these symptoms:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li>Severe unexplained pain</li>
                <li>Excessive bleeding</li>
                <li>Difficulty breathing</li>
                <li>Loss of consciousness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)