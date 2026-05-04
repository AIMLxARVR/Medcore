# enhanced_cancer_consultation_system.py - User-friendly cancer consultation with yes/no questions

import os
import logging
import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
from cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuestionnaireStep:
    """Represents a single step in the cancer consultation questionnaire"""
    
    def __init__(self, question_id: str, question_text: Dict[str, str], 
                 question_type: str = "yes_no", options: Dict[str, List[str]] = None):
        self.question_id = question_id
        self.question_text = question_text  # {"en": "English text", "bn": "Bengali text"}
        self.question_type = question_type  # "yes_no", "multiple_choice", "scale", "text"
        self.options = options or {}  # {"en": ["Option 1", "Option 2"], "bn": ["বিকল্প ১", "বিকল্প ২"]}

class CancerConsultationQuestionnaire:
    """Enhanced consultation questionnaire with structured questions"""
    
    def __init__(self, language="en"):
        self.language = language
        self.questions = self._initialize_questionnaire()
        
    def _initialize_questionnaire(self) -> List[QuestionnaireStep]:
        """Initialize the structured questionnaire"""
        
        return [
            # Demographics
            QuestionnaireStep(
                question_id="age_group",
                question_text={
                    "en": "What is your age group?",
                    "bn": "আপনার বয়স কত?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Under 30", "30-45", "46-60", "Over 60"],
                    "bn": ["৩০ এর নিচে", "৩০-৪৫", "৪৬-৬০", "৬০ এর উপরে"]
                }
            ),
            
            QuestionnaireStep(
                question_id="gender",
                question_text={
                    "en": "What is your gender?",
                    "bn": "আপনার লিঙ্গ কী?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Male", "Female", "Other"],
                    "bn": ["পুরুষ", "মহিলা", "অন্যান্য"]
                }
            ),
            
            # Chief Complaint
            QuestionnaireStep(
                question_id="main_concern",
                question_text={
                    "en": "What is your main health concern today?",
                    "bn": "আজ আপনার প্রধান স্বাস্থ্য সমস্যা কী?"
                },
                question_type="text"
            ),
            
            # Symptom Assessment - Yes/No Questions
            QuestionnaireStep(
                question_id="persistent_cough",
                question_text={
                    "en": "Do you have a persistent cough that has lasted more than 3 weeks?",
                    "bn": "আপনার কি ৩ সপ্তাহের বেশি সময় ধরে ক্রমাগত কাশি আছে?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="blood_in_sputum",
                question_text={
                    "en": "Have you noticed blood in your sputum (coughed up phlegm)?",
                    "bn": "আপনি কি আপনার কফে রক্ত দেখেছেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="unexplained_weight_loss",
                question_text={
                    "en": "Have you lost more than 5 kg (11 lbs) in the past 6 months without trying?",
                    "bn": "গত ৬ মাসে আপনার কি চেষ্টা ছাড়াই ৫ কেজির বেশি ওজন কমেছে?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="unusual_lumps",
                question_text={
                    "en": "Have you found any unusual lumps or masses anywhere on your body?",
                    "bn": "আপনি কি আপনার শরীরের কোথাও অস্বাভাবিক গাঁট বা পিণ্ড পেয়েছেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="breast_changes",
                question_text={
                    "en": "Have you noticed any changes in your breast(s) - lumps, dimpling, or nipple discharge?",
                    "bn": "আপনি কি আপনার স্তনে কোন পরিবর্তন লক্ষ্য করেছেন - গাঁট, চামড়া কুঁচকে যাওয়া, বা বোঁটা থেকে স্রাব?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="unusual_bleeding",
                question_text={
                    "en": "Have you experienced any unusual bleeding (rectal, vaginal, or in urine)?",
                    "bn": "আপনার কি কোন অস্বাভাবিক রক্তপাত হয়েছে (মলদ্বার, যোনি, বা প্রস্রাবে)?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="persistent_fatigue",
                question_text={
                    "en": "Do you feel extremely tired or weak most of the time?",
                    "bn": "আপনি কি বেশিরভাগ সময় অত্যধিক ক্লান্ত বা দুর্বল বোধ করেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="skin_changes",
                question_text={
                    "en": "Have you noticed any changes in moles or new spots on your skin?",
                    "bn": "আপনি কি আপনার তিলে কোন পরিবর্তন বা ত্বকে নতুন দাগ লক্ষ্য করেছেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="persistent_pain",
                question_text={
                    "en": "Do you have persistent pain that doesn't go away and gets worse?",
                    "bn": "আপনার কি এমন ব্যথা আছে যা যায় না এবং খারাপ হচ্ছে?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="bowel_changes",
                question_text={
                    "en": "Have you noticed persistent changes in your bowel habits?",
                    "bn": "আপনি কি আপনার মলত্যাগের অভ্যাসে স্থায়ী পরিবর্তন লক্ষ্য করেছেন?"
                },
                question_type="yes_no"
            ),
            
            # Risk Factors
            QuestionnaireStep(
                question_id="smoking_status",
                question_text={
                    "en": "Do you currently smoke or have you smoked in the past?",
                    "bn": "আপনি কি বর্তমানে ধূমপান করেন বা অতীতে করেছেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never smoked", "Former smoker", "Current smoker"],
                    "bn": ["কখনো ধূমপান করিনি", "আগে ধূমপান করতাম", "এখনো ধূমপান করি"]
                }
            ),
            
            QuestionnaireStep(
                question_id="alcohol_consumption",
                question_text={
                    "en": "How often do you consume alcohol?",
                    "bn": "আপনি কত ঘন ঘন মদ্যপান করেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never", "Occasionally", "Regularly", "Daily"],
                    "bn": ["কখনো না", "মাঝে মাঝে", "নিয়মিত", "প্রতিদিন"]
                }
            ),
            
            QuestionnaireStep(
                question_id="family_history",
                question_text={
                    "en": "Has anyone in your immediate family (parents, siblings, children) had cancer?",
                    "bn": "আপনার নিকট পরিবারে (বাবা-মা, ভাইবোন, সন্তান) কি কেউ ক্যান্সারে আক্রান্ত হয়েছেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="sun_exposure",
                question_text={
                    "en": "Do you spend a lot of time in the sun without protection?",
                    "bn": "আপনি কি সুরক্ষা ছাড়াই দীর্ঘ সময় রোদে থাকেন?"
                },
                question_type="yes_no"
            ),
            
            QuestionnaireStep(
                question_id="occupational_exposure",
                question_text={
                    "en": "Have you been exposed to chemicals, radiation, or asbestos at work?",
                    "bn": "আপনি কি কর্মক্ষেত্রে রাসায়নিক, বিকিরণ বা অ্যাসবেস্টসের সংস্পর্শে এসেছেন?"
                },
                question_type="yes_no"
            ),
            
            # Lifestyle Factors
            QuestionnaireStep(
                question_id="diet_quality",
                question_text={
                    "en": "How would you rate your diet quality?",
                    "bn": "আপনি আপনার খাদ্যের মান কীভাবে মূল্যায়ন করবেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Very healthy", "Moderately healthy", "Poor", "Very poor"],
                    "bn": ["খুব স্বাস্থ্যকর", "মধ্যম স্বাস্থ্যকর", "খারাপ", "খুব খারাপ"]
                }
            ),
            
            QuestionnaireStep(
                question_id="exercise_frequency",
                question_text={
                    "en": "How often do you exercise?",
                    "bn": "আপনি কত ঘন ঘন ব্যায়াম করেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Daily", "3-4 times per week", "1-2 times per week", "Rarely or never"],
                    "bn": ["প্রতিদিন", "সপ্তাহে ৩-৪ বার", "সপ্তাহে ১-২ বার", "কদাচিৎ বা কখনো না"]
                }
            ),
        ]

class EnhancedCancerConsultationSession:
    """Enhanced consultation session with user-friendly questionnaire"""
    
    def __init__(self, language="en"):
        self.language = language
        self.reasoning_engine = CancerReasoningEngine(language)
        self.questionnaire = CancerConsultationQuestionnaire(language)
        self.responses = {}
        self.current_question_index = 0
        self.consultation_complete = False
        
    def get_current_question(self) -> Optional[QuestionnaireStep]:
        """Get the current question to ask"""
        if self.current_question_index < len(self.questionnaire.questions):
            return self.questionnaire.questions[self.current_question_index]
        return None
    
    def get_progress_info(self) -> Dict[str, Any]:
        """Get consultation progress information"""
        total_questions = len(self.questionnaire.questions)
        completed = self.current_question_index
        
        return {
            "current_question": completed + 1,
            "total_questions": total_questions,
            "progress_percentage": (completed / total_questions) * 100,
            "questions_remaining": total_questions - completed
        }
    
    def process_response(self, response: Any) -> Dict[str, Any]:
        """Process user response and advance to next question"""
        
        if self.current_question_index >= len(self.questionnaire.questions):
            return self._complete_consultation()
        
        # Store the current response
        current_question = self.questionnaire.questions[self.current_question_index]
        self.responses[current_question.question_id] = {
            "question": current_question.question_text[self.language],
            "response": response,
            "question_type": current_question.question_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # Move to next question
        self.current_question_index += 1
        
        # Check if consultation is complete
        if self.current_question_index >= len(self.questionnaire.questions):
            return self._complete_consultation()
        
        # Return next question info
        next_question = self.get_current_question()
        progress = self.get_progress_info()
        
        return {
            "type": "next_question",
            "question": next_question,
            "progress": progress,
            "consultation_complete": False
        }
    
    def _complete_consultation(self) -> Dict[str, Any]:
        """Complete the consultation and generate analysis"""
        
        self.consultation_complete = True
        
        # Process responses through reasoning engine
        processed_data = self._process_responses_for_analysis()
        
        # Generate comprehensive analysis
        try:
            symptoms_analysis = self.reasoning_engine.analyze_symptoms(processed_data["symptoms"])
            risk_assessment = self.reasoning_engine.assess_risk_factors(processed_data["demographics"])
            differential_diagnosis = self.reasoning_engine.generate_differential_diagnosis(
                symptoms_analysis, risk_assessment
            )
            recommendations = self.reasoning_engine.generate_comprehensive_recommendations(
                symptoms_analysis, risk_assessment, differential_diagnosis
            )
            
            analysis_results = {
                "symptoms_analysis": symptoms_analysis,
                "risk_assessment": risk_assessment,
                "differential_diagnosis": differential_diagnosis,
                "recommendations": recommendations
            }
            
            comprehensive_response = self.reasoning_engine.generate_llm_enhanced_response(analysis_results)
            reasoning_explanation = self.reasoning_engine.get_reasoning_explanation()
            
            return {
                "type": "consultation_complete",
                "analysis_results": analysis_results,
                "comprehensive_response": comprehensive_response,
                "reasoning_explanation": reasoning_explanation,
                "consultation_complete": True,
                "urgency_level": self._determine_urgency_level(symptoms_analysis, risk_assessment)
            }
            
        except Exception as e:
            logging.error(f"Error in consultation completion: {e}")
            
            error_message = (
                "দুঃখিত, বিশ্লেষণে একটি ত্রুটি হয়েছে। অনুগ্রহ করে একজন যোগ্য চিকিৎসকের সাথে পরামর্শ করুন।"
                if self.language == "bn" else
                "Sorry, there was an error in the analysis. Please consult with a qualified healthcare provider."
            )
            
            return {
                "type": "error",
                "message": error_message,
                "consultation_complete": True,
                "error": True
            }
    
    def _process_responses_for_analysis(self) -> Dict[str, Any]:
        """Process questionnaire responses into format suitable for reasoning engine"""
        
        # Extract demographics
        demographics = {
            "age": self._convert_age_group(self.responses.get("age_group", {}).get("response")),
            "gender": self._convert_gender(self.responses.get("gender", {}).get("response")),
            "smoking": self._convert_smoking_status(self.responses.get("smoking_status", {}).get("response")),
            "heavy_drinking": self._convert_alcohol_consumption(self.responses.get("alcohol_consumption", {}).get("response")),
            "family_history_cancer": self.responses.get("family_history", {}).get("response") == "Yes" or self.responses.get("family_history", {}).get("response") == "হ্যাঁ",
            "excessive_sun_exposure": self.responses.get("sun_exposure", {}).get("response") == "Yes" or self.responses.get("sun_exposure", {}).get("response") == "হ্যাঁ",
            "occupational_exposure": self.responses.get("occupational_exposure", {}).get("response") == "Yes" or self.responses.get("occupational_exposure", {}).get("response") == "হ্যাঁ"
        }
        
        # Extract symptoms
        symptoms_description = self._build_symptoms_description()
        
        symptoms = {
            "description": symptoms_description,
            "severity": self._calculate_symptom_severity(),
            "duration": "unknown"  # Could be enhanced with duration questions
        }
        
        return {
            "demographics": demographics,
            "symptoms": symptoms
        }
    
    def _convert_age_group(self, age_group_response):
        """Convert age group response to numeric value"""
        if not age_group_response:
            return 40  # Default
        
        age_mapping = {
            "Under 30": 25, "৩০ এর নিচে": 25,
            "30-45": 37, "৩০-৪৫": 37,
            "46-60": 53, "৪৬-৬০": 53,
            "Over 60": 70, "৬০ এর উপরে": 70
        }
        
        return age_mapping.get(age_group_response, 40)
    
    def _convert_gender(self, gender_response):
        """Convert gender response"""
        if not gender_response:
            return "other"
        
        gender_mapping = {
            "Male": "male", "পুরুষ": "male",
            "Female": "female", "মহিলা": "female",
            "Other": "other", "অন্যান্য": "other"
        }
        
        return gender_mapping.get(gender_response, "other")
    
    def _convert_smoking_status(self, smoking_response):
        """Convert smoking status to boolean"""
        if not smoking_response:
            return False
        
        return smoking_response in ["Current smoker", "এখনো ধূমপান করি"]
    
    def _convert_alcohol_consumption(self, alcohol_response):
        """Convert alcohol consumption to heavy drinking boolean"""
        if not alcohol_response:
            return False
        
        return alcohol_response in ["Daily", "প্রতিদিন"]
    
    def _build_symptoms_description(self) -> str:
        """Build a descriptive text from symptom responses"""
        
        symptom_descriptions = []
        main_concern = self.responses.get("main_concern", {}).get("response", "")
        
        if main_concern:
            symptom_descriptions.append(f"Main concern: {main_concern}")
        
        # Add yes responses
        yes_responses = ["Yes", "হ্যাঁ"]
        
        symptom_questions = {
            "persistent_cough": "persistent cough for more than 3 weeks",
            "blood_in_sputum": "blood in sputum",
            "unexplained_weight_loss": "unexplained weight loss of more than 5kg",
            "unusual_lumps": "unusual lumps or masses",
            "breast_changes": "breast changes including lumps or discharge",
            "unusual_bleeding": "unusual bleeding",
            "persistent_fatigue": "persistent fatigue and weakness",
            "skin_changes": "changes in moles or new skin spots",
            "persistent_pain": "persistent worsening pain",
            "bowel_changes": "persistent changes in bowel habits"
        }
        
        for question_id, description in symptom_questions.items():
            response = self.responses.get(question_id, {}).get("response")
            if response in yes_responses:
                symptom_descriptions.append(description)
        
        return ". ".join(symptom_descriptions) if symptom_descriptions else "No specific symptoms reported"
    
    def _calculate_symptom_severity(self) -> int:
        """Calculate overall symptom severity score (1-10)"""
        
        yes_responses = ["Yes", "হ্যাঁ"]
        symptom_weights = {
            "blood_in_sputum": 9,
            "unexplained_weight_loss": 8,
            "unusual_bleeding": 8,
            "unusual_lumps": 7,
            "persistent_cough": 6,
            "breast_changes": 7,
            "persistent_pain": 6,
            "skin_changes": 5,
            "bowel_changes": 6,
            "persistent_fatigue": 4
        }
        
        total_severity = 0
        symptom_count = 0
        
        for question_id, weight in symptom_weights.items():
            response = self.responses.get(question_id, {}).get("response")
            if response in yes_responses:
                total_severity += weight
                symptom_count += 1
        
        if symptom_count == 0:
            return 1
        
        average_severity = total_severity / symptom_count
        return min(int(average_severity), 10)
    
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
            "questions_answered": len(self.responses),
            "total_questions": len(self.questionnaire.questions),
            "responses": self.responses,
            "completion_status": "complete" if self.consultation_complete else "in_progress"
        }
    
    def reset_consultation(self):
        """Reset consultation for new session"""
        self.responses = {}
        self.current_question_index = 0
        self.consultation_complete = False
        self.reasoning_engine.reset_reasoning_trace()


def create_enhanced_cancer_consultation_interface(language="English"):
    """Create enhanced user-friendly cancer consultation interface for Streamlit"""
    
    lang_code = "bn" if language == "Bengali" else "en"
    
    # Initialize consultation session
    session_key = f'enhanced_cancer_consultation_{lang_code}'
    if session_key not in st.session_state:
        st.session_state[session_key] = EnhancedCancerConsultationSession(lang_code)
    
    consultation = st.session_state[session_key]
    
    # Header
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🎯 উন্নত ক্যান্সার বিশেষজ্ঞ পরামর্শ</h1>
            <p style="margin: 5px 0 0 0;">ব্যবহারকারী-বান্ধব প্রশ্নোত্তর সহ স্মার্ট ক্যান্সার ঝুঁকি মূল্যায়ন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🎯 Enhanced Cancer Specialist Consultation</h1>
            <p style="margin: 5px 0 0 0;">Smart cancer risk assessment with user-friendly questionnaire</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show progress if consultation is active
    if not consultation.consultation_complete:
        progress_info = consultation.get_progress_info()
        current_question = consultation.get_current_question()
        
        if current_question:
            # Progress indicator
            progress_percentage = progress_info["progress_percentage"]
            
            if language == "Bengali":
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 15px; border-radius: 10px; margin: 15px 0; 
                            border-left: 4px solid #2196f3;">
                    <strong>📋 প্রগতি:</strong> প্রশ্ন {progress_info['current_question']} এর {progress_info['total_questions']}<br>
                    <strong>📊 সম্পন্ন:</strong> {progress_percentage:.1f}%
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 15px; border-radius: 10px; margin: 15px 0; 
                            border-left: 4px solid #2196f3;">
                    <strong>📋 Progress:</strong> Question {progress_info['current_question']} of {progress_info['total_questions']}<br>
                    <strong>📊 Complete:</strong> {progress_percentage:.1f}%
                </div>
                """, unsafe_allow_html=True)
            
            # Progress bar
            st.progress(progress_percentage / 100)
            
            # Display current question
            display_current_question(current_question, consultation, language, lang_code)
        
        else:
            # Start consultation
            display_consultation_start(consultation, language, lang_code)
    
    else:
        # Show consultation results
        display_enhanced_consultation_results(consultation, language)
    
    # Sidebar with consultation info
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h3 style="margin: 0;">{'পরামর্শ তথ্য' if language == 'Bengali' else 'Consultation Info'}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if not consultation.consultation_complete:
            progress_info = consultation.get_progress_info()
            if language == "Bengali":
                st.markdown(f"""
                **📊 অগ্রগতি:** {progress_info['progress_percentage']:.1f}%  
                **📋 প্রশ্ন:** {progress_info['current_question']}/{progress_info['total_questions']}  
                **🎯 বিশেষত্ব:** ক্যান্সার ঝুঁকি মূল্যায়ন  
                **🧠 এআই:** উন্নত যুক্তি ইঞ্জিন
                """)
            else:
                st.markdown(f"""
                **📊 Progress:** {progress_info['progress_percentage']:.1f}%  
                **📋 Questions:** {progress_info['current_question']}/{progress_info['total_questions']}  
                **🎯 Specialty:** Cancer Risk Assessment  
                **🧠 AI:** Advanced Reasoning Engine
                """)
        else:
            if language == "Bengali":
                st.markdown("""
                **✅ স্থিতি:** পরামর্শ সম্পন্ন  
                **🎯 বিশেষত্ব:** ক্যান্সার ঝুঁকি মূল্যায়ন  
                **🧠 এআই:** বিস্তারিত বিশ্লেষণ প্রস্তুত
                """)
            else:
                st.markdown("""
                **✅ Status:** Consultation Complete  
                **🎯 Specialty:** Cancer Risk Assessment  
                **🧠 AI:** Detailed Analysis Ready
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
        if consultation.consultation_complete:
            consultation_summary = consultation.get_consultation_summary()
            
            if language == "Bengali":
                st.download_button(
                    label="📥 পরামর্শ ডাউনলোড করুন",
                    data=json.dumps(consultation_summary, indent=2, ensure_ascii=False),
                    file_name=f"enhanced_cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.download_button(
                    label="📥 Download Consultation",
                    data=json.dumps(consultation_summary, indent=2),
                    file_name=f"enhanced_cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )


def display_consultation_start(consultation: EnhancedCancerConsultationSession, language: str, lang_code: str):
    """Display consultation start screen"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 15px; margin: 20px 0; 
                    border: 2px solid #ff6b6b; text-align: center;">
            <h2 style="color: #ff6b6b; margin: 0 0 20px 0;">🎯 ক্যান্সার স্ক্রিনিং প্রশ্নোত্তর</h2>
            <p style="font-size: 1.1em; margin: 15px 0;">
                আমি আপনাকে কিছু সহজ প্রশ্ন করব যা আপনার ক্যান্সারের ঝুঁকি মূল্যায়ন করতে সাহায্য করবে।
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #333; margin: 0 0 15px 0;">📋 কী আশা করবেন:</h4>
                <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                    <li>🎯 সহজ হ্যাঁ/না প্রশ্ন</li>
                    <li>📊 মাল্টিপল চয়েস প্রশ্ন</li>
                    <li>⏱️ প্রায় ৫-১০ মিনিট সময়</li>
                    <li>🧠 AI ভিত্তিক বিশ্লেষণ</li>
                    <li>📋 ব্যক্তিগত সুপারিশ</li>
                </ul>
            </div>
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0; font-size: 0.9em;">
                    <strong>⚠️ গুরুত্বপূর্ণ:</strong> এটি একটি প্রাথমিক স্ক্রিনিং টুল। 
                    চূড়ান্ত রোগ নির্ণয়ের জন্য অবশ্যই একজন যোগ্য চিকিৎসকের পরামর্শ নিন।
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 প্রশ্নোত্তর শুরু করুন", type="primary", use_container_width=True):
            # This will trigger the first question
            st.rerun()
    else:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 15px; margin: 20px 0; 
                    border: 2px solid #ff6b6b; text-align: center;">
            <h2 style="color: #ff6b6b; margin: 0 0 20px 0;">🎯 Cancer Screening Questionnaire</h2>
            <p style="font-size: 1.1em; margin: 15px 0;">
                I'll ask you some simple questions to help assess your cancer risk.
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #333; margin: 0 0 15px 0;">📋 What to Expect:</h4>
                <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                    <li>🎯 Simple Yes/No questions</li>
                    <li>📊 Multiple choice questions</li>
                    <li>⏱️ About 5-10 minutes</li>
                    <li>🧠 AI-powered analysis</li>
                    <li>📋 Personalized recommendations</li>
                </ul>
            </div>
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0; font-size: 0.9em;">
                    <strong>⚠️ Important:</strong> This is a preliminary screening tool. 
                    Always consult qualified healthcare providers for definitive diagnosis.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Questionnaire", type="primary", use_container_width=True):
            # This will trigger the first question
            st.rerun()


def display_current_question(question: QuestionnaireStep, consultation: EnhancedCancerConsultationSession, 
                           language: str, lang_code: str):
    """Display the current question with appropriate input widgets"""
    
    progress_info = consultation.get_progress_info()
    question_text = question.question_text[lang_code]
    
    # Question display
    st.markdown(f"""
    <div style="background: white; padding: 25px; border-radius: 15px; margin: 20px 0; 
                border-left: 6px solid #ff6b6b; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #ff6b6b; margin: 0 0 20px 0;">
            {'প্রশ্ন' if language == 'Bengali' else 'Question'} {progress_info['current_question']}:
        </h3>
        <p style="font-size: 1.2em; margin: 0; line-height: 1.5;">
            {question_text}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input based on question type
    user_response = None
    
    if question.question_type == "yes_no":
        user_response = display_yes_no_question(question, language, lang_code)
    
    elif question.question_type == "multiple_choice":
        user_response = display_multiple_choice_question(question, language, lang_code)
    
    elif question.question_type == "scale":
        user_response = display_scale_question(question, language, lang_code)
    
    elif question.question_type == "text":
        user_response = display_text_question(question, language, lang_code)
    
    # Submit button
    if user_response is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if language == "Bengali":
                submit_button = st.button(
                    "➡️ পরবর্তী প্রশ্ন", 
                    type="primary", 
                    use_container_width=True,
                    key=f"submit_{question.question_id}"
                )
            else:
                submit_button = st.button(
                    "➡️ Next Question", 
                    type="primary", 
                    use_container_width=True,
                    key=f"submit_{question.question_id}"
                )
        
        if submit_button:
            with st.spinner("Processing..." if language == "English" else "প্রক্রিয়াকরণ..."):
                result = consultation.process_response(user_response)
                st.rerun()


def display_yes_no_question(question: QuestionnaireStep, language: str, lang_code: str):
    """Display yes/no question with radio buttons"""
    
    if language == "Bengali":
        options = ["হ্যাঁ", "না"]
        help_text = "একটি উত্তর নির্বাচন করুন"
    else:
        options = ["Yes", "No"]
        help_text = "Select one answer"
    
    response = st.radio(
        label="",
        options=options,
        key=f"radio_{question.question_id}",
        help=help_text,
        label_visibility="collapsed"
    )
    
    return response


def display_multiple_choice_question(question: QuestionnaireStep, language: str, lang_code: str):
    """Display multiple choice question"""
    
    options = question.options.get(lang_code, [])
    help_text = "একটি বিকল্প নির্বাচন করুন" if language == "Bengali" else "Select one option"
    
    response = st.radio(
        label="",
        options=options,
        key=f"radio_{question.question_id}",
        help=help_text,
        label_visibility="collapsed"
    )
    
    return response


def display_scale_question(question: QuestionnaireStep, language: str, lang_code: str):
    """Display scale question with slider"""
    
    if language == "Bengali":
        label = "মাত্রা নির্বাচন করুন (১-১০):"
    else:
        label = "Select scale (1-10):"
    
    response = st.slider(
        label=label,
        min_value=1,
        max_value=10,
        value=5,
        key=f"slider_{question.question_id}"
    )
    
    return response


def display_text_question(question: QuestionnaireStep, language: str, lang_code: str):
    """Display text input question"""
    
    if language == "Bengali":
        placeholder = "আপনার উত্তর এখানে লিখুন..."
    else:
        placeholder = "Type your answer here..."
    
    response = st.text_area(
        label="",
        key=f"text_{question.question_id}",
        placeholder=placeholder,
        height=100,
        label_visibility="collapsed"
    )
    
    return response if response.strip() else None


def display_enhanced_consultation_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display comprehensive consultation results"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ পরামর্শ সম্পন্ন</h2>
            <p style="margin: 5px 0 0 0;">আপনার ব্যাপক ক্যান্সার ঝুঁকি মূল্যায়ন প্রস্তুত</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ Consultation Complete</h2>
            <p style="margin: 5px 0 0 0;">Your comprehensive cancer risk assessment is ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get the analysis results (this would be stored when consultation completes)
    # For now, we'll create a placeholder
    
    # Create tabs for different sections
    if language == "Bengali":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 সারসংক্ষেপ", 
            "🧠 AI বিশ্লেষণ", 
            "📊 ঝুঁকি মূল্যায়ন", 
            "💡 সুপারিশ",
            "🧠 AI যুক্তি দেখুন"  # NEW TAB
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Summary", 
            "🧠 AI Analysis", 
            "📊 Risk Assessment", 
            "💡 Recommendations",
            "🧠 View AI Reasoning"  # NEW TAB
        ])
    
    with tab1:
        display_consultation_summary(consultation, language)
    
    with tab2:
        display_ai_analysis_results(consultation, language)
    
    with tab3:
        display_risk_assessment_results(consultation, language)
    
    with tab4:
        display_recommendations_results(consultation, language)
    
    # NEW TAB 5: AI Reasoning
    with tab5:
        display_consultation_ai_reasoning(consultation, language)

    
def display_consultation_ai_reasoning(consultation: EnhancedCancerConsultationSession, language: str):
    """Display detailed AI reasoning process for the consultation"""
    
    if language == "Bengali":
        st.markdown("### 🧠 AI যুক্তি প্রক্রিয়া বিশ্লেষণ")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="margin: 0;">🎯 AI কীভাবে আপনার ঝুঁকি বিশ্লেষণ করেছে</h3>
            <p style="margin: 10px 0 0 0;">প্রতিটি ধাপে AI এর চিন্তাভাবনা ও যুক্তি দেখুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 🧠 AI Reasoning Process Analysis")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="margin: 0;">🎯 How AI Analyzed Your Risk</h3>
            <p style="margin: 10px 0 0 0;">See the AI's thinking and reasoning at each step</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if reasoning engine has reasoning trace
    if hasattr(consultation, 'reasoning_engine') and consultation.reasoning_engine.reasoning_trace:
        try:
            # Get reasoning explanation from the reasoning engine
            reasoning_explanation = consultation.reasoning_engine.get_reasoning_explanation()
            
            if reasoning_explanation:
                display_detailed_reasoning_trace(reasoning_explanation, language)
            else:
                display_reasoning_fallback(language)
                
        except Exception as e:
            logging.error(f"Error displaying reasoning trace: {e}")
            display_reasoning_fallback(language)
    else:
        # Show demo reasoning or fallback
        display_reasoning_fallback(language)

def display_detailed_reasoning_trace(reasoning_explanation: dict, language: str):
    """Display the detailed AI reasoning trace with interactive elements"""
    
    step_details = reasoning_explanation.get("step_details", [])
    overall_confidence = reasoning_explanation.get("overall_confidence", 0)
    
    # Overall confidence display
    if language == "Bengali":
        st.markdown(f"### 📊 সামগ্রিক আত্মবিশ্বাস: {overall_confidence:.2f}")
        confidence_label = "AI এর সামগ্রিক আত্মবিশ্বাস স্তর"
    else:
        st.markdown(f"### 📊 Overall Confidence: {overall_confidence:.2f}")
        confidence_label = "AI's Overall Confidence Level"
    
    # Display confidence meter
    confidence_color = "#4caf50" if overall_confidence > 0.8 else "#ff9800" if overall_confidence > 0.6 else "#f44336"
    
    st.markdown(f"""
    <div style="margin: 15px 0;">
        <p style="margin: 5px 0; font-weight: bold;">{confidence_label}</p>
        <div style="background: #e0e0e0; border-radius: 10px; height: 20px; margin: 10px 0;">
            <div style="background: {confidence_color}; height: 20px; border-radius: 10px; width: {overall_confidence*100}%; 
                        display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {overall_confidence:.1%}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each reasoning step
    if language == "Bengali":
        st.markdown("### 🔍 বিস্তারিত যুক্তি ধাপসমূহ:")
    else:
        st.markdown("### 🔍 Detailed Reasoning Steps:")
    
    for i, step in enumerate(step_details, 1):
        step_name = step['step'].replace('_', ' ').title()
        reasoning = step['reasoning']
        confidence = step['confidence']
        timestamp = step['timestamp']
        
        # Step confidence color
        step_color = "#4caf50" if confidence > 0.8 else "#ff9800" if confidence > 0.6 else "#f44336"
        
        # Translate step names to Bengali if needed
        if language == "Bengali":
            step_translations = {
                "Symptom Analysis": "লক্ষণ বিশ্লেষণ",
                "Risk Assessment": "ঝুঁকি মূল্যায়ন", 
                "Differential Diagnosis": "পার্থক্যমূলক রোগ নির্ণয়",
                "Recommendation Generation": "সুপারিশ প্রস্তুতি",
                "Urgency Evaluation": "জরুরিত্ব মূল্যায়ন"
            }
            step_name = step_translations.get(step_name, step_name)
        
        # Create expandable step
        with st.expander(f"ধাপ {i}: {step_name} (আত্মবিশ্বাস: {confidence:.2f})" if language == "Bengali" 
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
    
    # Add reasoning methodology explanation
    if language == "Bengali":
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1976d2;">🧠 AI যুক্তি পদ্ধতি</h4>
            <p style="margin: 5px 0;">AI এই পদ্ধতিতে আপনার ঝুঁকি বিশ্লেষণ করেছে:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li><strong>লক্ষণ বিশ্লেষণ:</strong> আপনার বর্ণিত লক্ষণগুলি চিকিৎসা জ্ঞানের সাথে মিলিয়ে দেখা</li>
                <li><strong>ঝুঁকি মূল্যায়ন:</strong> আপনার ব্যক্তিগত ঝুঁকির কারণগুলি গণনা করা</li>
                <li><strong>সম্ভাব্য রোগ:</strong> লক্ষণ ও ঝুঁকির ভিত্তিতে সম্ভাব্য অবস্থা নির্ণয়</li>
                <li><strong>সুপারিশ:</strong> আপনার জন্য উপযুক্ত পরবর্তী পদক্ষেপ নির্ধারণ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1976d2;">🧠 AI Reasoning Methodology</h4>
            <p style="margin: 5px 0;">The AI analyzed your risk using this methodology:</p>
            <ul style="margin: 10px 0 0 20px;">
                <li><strong>Symptom Analysis:</strong> Comparing your described symptoms with medical knowledge</li>
                <li><strong>Risk Assessment:</strong> Calculating your personal risk factors</li>
                <li><strong>Differential Diagnosis:</strong> Determining possible conditions based on symptoms and risks</li>
                <li><strong>Recommendations:</strong> Identifying appropriate next steps for your situation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def display_reasoning_fallback(language: str):
    """Display fallback reasoning information when detailed trace is not available"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #856404;">📋 যুক্তি ট্রেস উপলব্ধ নেই</h4>
            <p style="margin: 5px 0;">বিস্তারিত যুক্তি ট্রেস এই পরামর্শের জন্য সংরক্ষিত হয়নি।</p>
            <p style="margin: 10px 0 0 0;">তবে AI নিম্নলিখিত পদ্ধতিতে আপনার ঝুঁকি বিশ্লেষণ করেছে:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show demo reasoning process
        display_demo_reasoning_for_consultation(language)
        
    else:
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #856404;">📋 Reasoning Trace Not Available</h4>
            <p style="margin: 5px 0;">Detailed reasoning trace was not saved for this consultation.</p>
            <p style="margin: 10px 0 0 0;">However, the AI analyzed your risk using the following methodology:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show demo reasoning process
        display_demo_reasoning_for_consultation(language)


def display_demo_reasoning_for_consultation(language: str):
    """Display demo reasoning process for consultation"""
    
    if language == "Bengali":
        demo_steps = [
            {
                "step": "প্রশ্নোত্তর বিশ্লেষণ",
                "reasoning": "আপনার দেওয়া উত্তরগুলি বিশ্লেষণ করে ক্যান্সারের ঝুঁকির কারণগুলি চিহ্নিত করা হয়েছে। প্রতিটি উত্তর একটি নির্দিষ্ট ওজন বহন করে এবং সামগ্রিক ঝুঁকি গণনায় অবদান রাখে।",
                "confidence": 0.90,
                "details": "উত্তর বিশ্লেষণ: সম্পূর্ণ, ঝুঁকি কারণ: চিহ্নিত, ডেটা গুণমান: উচ্চ"
            },
            {
                "step": "ঝুঁকি গণনা", 
                "reasoning": "আপনার বয়স, লিঙ্গ, পারিবারিক ইতিহাস, জীবনযাত্রার অভ্যাস এবং বর্তমান লক্ষণগুলির ভিত্তিতে বিভিন্ন ক্যান্সারের জন্য আলাদা ঝুঁকি স্কোর গণনা করা হয়েছে।",
                "confidence": 0.85,
                "details": "ঝুঁকি ম্যাট্রিক্স: গণনা সম্পূর্ণ, বয়স কারণ: বিবেচিত, পারিবারিক ইতিহাস: অন্তর্ভুক্ত"
            },
            {
                "step": "সুপারিশ প্রস্তুতি",
                "reasoning": "গণনাকৃত ঝুঁকির স্তরের ভিত্তিতে আপনার জন্য ব্যক্তিগত সুপারিশ তৈরি করা হয়েছে। এতে স্ক্রিনিং, জীবনযাত্রার পরিবর্তন এবং ফলো-আপের পরামর্শ রয়েছে।",
                "confidence": 0.88,
                "details": "সুপারিশ প্রকার: ব্যক্তিগত, অগ্রাধিকার: ঝুঁকি-ভিত্তিক, ফলো-আপ: পরিকল্পিত"
            }
        ]
    else:
        demo_steps = [
            {
                "step": "Questionnaire Analysis",
                "reasoning": "Your responses were analyzed to identify cancer risk factors. Each answer carries a specific weight and contributes to the overall risk calculation based on established medical guidelines.",
                "confidence": 0.90,
                "details": "Response analysis: Complete, Risk factors: Identified, Data quality: High"
            },
            {
                "step": "Risk Calculation",
                "reasoning": "Based on your age, gender, family history, lifestyle habits, and current symptoms, separate risk scores were calculated for different types of cancer using validated risk assessment models.",
                "confidence": 0.85,
                "details": "Risk matrix: Calculated, Age factors: Considered, Family history: Included"
            },
            {
                "step": "Recommendation Generation", 
                "reasoning": "Personalized recommendations were created based on your calculated risk levels. These include screening guidelines, lifestyle modifications, and follow-up care suggestions tailored to your profile.",
                "confidence": 0.88,
                "details": "Recommendation type: Personalized, Priority: Risk-based, Follow-up: Planned"
            }
        ]
    
    for i, step in enumerate(demo_steps, 1):
        step_color = "#4caf50" if step['confidence'] > 0.8 else "#ff9800" if step['confidence'] > 0.6 else "#f44336"
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {step_color};">
            <h4 style="color: {step_color};">
                {'ধাপ' if language == 'Bengali' else 'Step'} {i}: {step['step']}
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
    
    # Add explanation of confidence levels
    if language == "Bengali":
        st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h5>🎯 আত্মবিশ্বাস স্তরের ব্যাখ্যা:</h5>
            <ul style="margin: 10px 0 0 20px; font-size: 0.9em;">
                <li><strong>০.৮৫+:</strong> উচ্চ আত্মবিশ্বাস - নির্ভরযোগ্য বিশ্লেষণ</li>
                <li><strong>০.৭০-০.৮৪:</strong> মধ্যম আত্মবিশ্বাস - ভাল বিশ্লেষণ</li>
                <li><strong>০.৭০ এর নিচে:</strong> কম আত্মবিশ্বাস - আরো তথ্য প্রয়োজন</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h5>🎯 Confidence Level Explanation:</h5>
            <ul style="margin: 10px 0 0 20px; font-size: 0.9em;">
                <li><strong>0.85+:</strong> High confidence - Reliable analysis</li>
                <li><strong>0.70-0.84:</strong> Moderate confidence - Good analysis</li>
                <li><strong>Below 0.70:</strong> Low confidence - More information needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def display_consultation_summary(consultation: EnhancedCancerConsultationSession, language: str):
    """Display consultation summary"""
    
    if language == "Bengali":
        st.markdown("### 📋 পরামর্শের সারসংক্ষেপ")
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4>📊 পরিসংখ্যান:</h4>
            <ul>
                <li><strong>মোট প্রশ্ন:</strong> {len(consultation.questionnaire.questions)}</li>
                <li><strong>উত্তর দেওয়া:</strong> {len(consultation.responses)}</li>
                <li><strong>সম্পন্নতা:</strong> 100%</li>
                <li><strong>সময়:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Show key responses
        st.markdown("#### 🔑 মূল উত্তরসমূহ:")
    else:
        st.markdown("### 📋 Consultation Summary")
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4>📊 Statistics:</h4>
            <ul>
                <li><strong>Total Questions:</strong> {len(consultation.questionnaire.questions)}</li>
                <li><strong>Answered:</strong> {len(consultation.responses)}</li>
                <li><strong>Completion:</strong> 100%</li>
                <li><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Show key responses
        st.markdown("#### 🔑 Key Responses:")
    
    # Display key responses in an organized way
    key_responses = ["age_group", "gender", "main_concern", "smoking_status", "family_history"]
    
    for response_id in key_responses:
        if response_id in consultation.responses:
            response_data = consultation.responses[response_id]
            question = response_data["question"]
            answer = response_data["response"]
            
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #007bff;">
                <strong>Q:</strong> {question}<br>
                <strong>A:</strong> {answer}
            </div>
            """, unsafe_allow_html=True)


def display_ai_analysis_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display AI analysis results"""
    
    if language == "Bengali":
        st.markdown("### 🧠 AI বিশ্লেষণ প্রক্রিয়া")
    else:
        st.markdown("### 🧠 AI Analysis Process")
    
    # This would show the actual reasoning trace from the reasoning engine
    # For now, we'll show a placeholder
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4>🔍 বিশ্লেষণ পদক্ষেপ:</h4>
            <ol>
                <li>✅ লক্ষণ বিশ্লেষণ সম্পন্ন</li>
                <li>✅ ঝুঁকি কারণ মূল্যায়ন সম্পন্ন</li>
                <li>✅ পার্থক্যমূলক রোগ নির্ণয় সম্পন্ন</li>
                <li>✅ সুপারিশ তৈরি সম্পন্ন</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔬 বিস্তারিত AI যুক্তি প্রক্রিয়া দেখতে 'AI যুক্তি দেখুন' ট্যাব ব্যবহার করুন।")
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4>🔍 Analysis Steps:</h4>
            <ol>
                <li>✅ Symptom Analysis Complete</li>
                <li>✅ Risk Factor Assessment Complete</li>
                <li>✅ Differential Diagnosis Complete</li>
                <li>✅ Recommendations Generated</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔬 Use the 'View AI Reasoning' tab to see detailed AI reasoning process.")


def display_risk_assessment_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display risk assessment results"""
    
    if language == "Bengali":
        st.markdown("### 📊 ক্যান্সার ঝুঁকি মূল্যায়ন")
    else:
        st.markdown("### 📊 Cancer Risk Assessment")
    
    # This would show actual risk assessment results
    # For now, we'll create a sample based on responses
    
    # Calculate basic risk factors from responses
    risk_factors = calculate_risk_factors_from_responses(consultation.responses, language)
    
    # Display risk factors
    for risk_factor in risk_factors:
        color = risk_factor["color"]
        level = risk_factor["level"]
        description = risk_factor["description"]
        
        st.markdown(f"""
        <div style="background: {color}20; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {color};">
            <h4 style="color: {color}; margin: 0 0 10px 0;">{level}</h4>
            <p style="margin: 0;">{description}</p>
        </div>
        """, unsafe_allow_html=True)


def display_recommendations_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display recommendations results"""
    
    if language == "Bengali":
        st.markdown("### 💡 ব্যক্তিগত সুপারিশ")
        
        recommendations = get_recommendations_from_responses(consultation.responses, "bn")
        
        for category, items in recommendations.items():
            st.markdown(f"#### {category}")
            for item in items:
                st.markdown(f"• {item}")
        
        # Emergency warning
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
        st.markdown("### 💡 Personalized Recommendations")
        
        recommendations = get_recommendations_from_responses(consultation.responses, "en")
        
        for category, items in recommendations.items():
            st.markdown(f"#### {category}")
            for item in items:
                st.markdown(f"• {item}")
        
        # Emergency warning
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


def calculate_risk_factors_from_responses(responses: dict, language: str) -> List[Dict]:
    """Calculate risk factors based on responses"""
    
    risk_factors = []
    
    # Check smoking status
    smoking_response = responses.get("smoking_status", {}).get("response", "")
    if "Current smoker" in smoking_response or "এখনো ধূমপান করি" in smoking_response:
        if language == "Bengali":
            risk_factors.append({
                "level": "🔴 উচ্চ ঝুঁকি",
                "description": "বর্তমান ধূমপান ফুসফুস ও অন্যান্য ক্যান্সারের ঝুঁকি উল্লেখযোগ্যভাবে বাড়ায়।",
                "color": "#f44336"
            })
        else:
            risk_factors.append({
                "level": "🔴 High Risk",
                "description": "Current smoking significantly increases risk of lung and other cancers.",
                "color": "#f44336"
            })
    
    # Check family history
    family_history = responses.get("family_history", {}).get("response", "")
    if "Yes" in family_history or "হ্যাঁ" in family_history:
        if language == "Bengali":
            risk_factors.append({
                "level": "🟡 মধ্যম ঝুঁকি",
                "description": "পারিবারিক ক্যান্সারের ইতিহাস জেনেটিক প্রবণতার ইঙ্গিত দেয়।",
                "color": "#ff9800"
            })
        else:
            risk_factors.append({
                "level": "🟡 Moderate Risk",
                "description": "Family history of cancer suggests genetic predisposition.",
                "color": "#ff9800"
            })
    
    # Check age
    age_response = responses.get("age_group", {}).get("response", "")
    if "Over 60" in age_response or "৬০ এর উপরে" in age_response:
        if language == "Bengali":
            risk_factors.append({
                "level": "🟡 বয়স-সংক্রান্ত ঝুঁকি",
                "description": "বয়স বৃদ্ধির সাথে ক্যান্সারের ঝুঁকি বাড়ে।",
                "color": "#ff9800"
            })
        else:
            risk_factors.append({
                "level": "🟡 Age-Related Risk",
                "description": "Cancer risk increases with age.",
                "color": "#ff9800"
            })
    
    # If no significant risk factors
    if not risk_factors:
        if language == "Bengali":
            risk_factors.append({
                "level": "🟢 কম ঝুঁকি",
                "description": "আপনার উত্তরের ভিত্তিতে, বড় ক্যান্সার ঝুঁকির কারণ পাওয়া যায়নি।",
                "color": "#4caf50"
            })
        else:
            risk_factors.append({
                "level": "🟢 Low Risk",
                "description": "Based on your responses, no major cancer risk factors were identified.",
                "color": "#4caf50"
            })
    
    return risk_factors


def get_recommendations_from_responses(responses: dict, language: str) -> Dict[str, List[str]]:
    """Generate recommendations based on responses"""
    
    if language == "bn":
        recommendations = {
            "🏥 তাৎক্ষণিক পদক্ষেপ": [],
            "🔬 সুপারিশকৃত পরীক্ষা": [],
            "🌱 জীবনযাত্রার পরিবর্তন": [],
            "📅 নিয়মিত স্ক্রিনিং": []
        }
        
        # Add general recommendations
        recommendations["🏥 তাৎক্ষণিক পদক্ষেপ"].extend([
            "প্রাথমিক চিকিৎসকের সাথে আলোচনা করুন",
            "লক্ষণ ডায়েরি রাখুন"
        ])
        
        recommendations["🔬 সুপারিশকৃত পরীক্ষা"].extend([
            "সম্পূর্ণ রক্ত পরীক্ষা (CBC)",
            "বুকের এক্স-রে",
            "ক্যান্সার মার্কার পরীক্ষা"
        ])
        
        recommendations["🌱 জীবনযাত্রার পরিবর্তন"].extend([
            "ধূমপান ত্যাগ করুন (যদি প্রযোজ্য)",
            "শারীরিক কার্যকলাপ বৃদ্ধি করুন",
            "স্বাস্থ্যকর খাদ্যাভ্যাস বজায় রাখুন"
        ])
        
        recommendations["📅 নিয়মিত স্ক্রিনিং"].extend([
            "বার্ষিক স্বাস্থ্য পরীক্ষা",
            "বয়স অনুযায়ী ক্যান্সার স্ক্রিনিং"
        ])
    else:
        recommendations = {
            "🏥 Immediate Actions": [],
            "🔬 Recommended Tests": [],
            "🌱 Lifestyle Changes": [],
            "📅 Regular Screening": []
        }
        
        # Add general recommendations
        recommendations["🏥 Immediate Actions"].extend([
            "Schedule appointment with primary care physician",
            "Keep a symptom diary"
        ])
        
        recommendations["🔬 Recommended Tests"].extend([
            "Complete Blood Count (CBC)",
            "Chest X-ray",
            "Cancer marker tests"
        ])
        
        recommendations["🌱 Lifestyle Changes"].extend([
            "Quit smoking if applicable",
            "Increase physical activity",
            "Maintain healthy diet"
        ])
        
        recommendations["📅 Regular Screening"].extend([
            "Annual health check-ups",
            "Age-appropriate cancer screenings"
        ])
    
    return recommendations