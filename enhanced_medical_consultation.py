# enhanced_medical_consultation.py - Advanced consultation system with follow-up questions
import os
import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import streamlit as st
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

class MedicalConsultationManager:
    """
    Manages the medical consultation process with follow-up questions
    """
    
    def __init__(self, language="en"):
        self.language = language
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        self.consultation_state = {
            'stage': 'initial',  # initial, gathering_info, analysis, recommendation
            'chief_complaint': '',
            'collected_info': {},
            'follow_up_questions': [],
            'current_question_index': 0,
            'consultation_complete': False
        }
        
    def analyze_initial_complaint(self, user_message: str) -> Dict:
        """
        Analyze the initial user message to determine if it's health-related
        and what type of follow-up questions are needed
        """
        
        # System prompt to analyze the complaint
        analysis_prompt = self._get_analysis_prompt()
        
        try:
            messages = [
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": f"Patient says: {user_message}"}
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=DEFAULT_MODEL,
                temperature=0.3,
                max_tokens=800
            )
            
            # Parse the response to extract structured information
            analysis_text = response.choices[0].message.content
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            logging.error(f"Error analyzing initial complaint: {e}")
            return {"is_medical": False, "category": "unknown", "questions": []}
    
    def generate_follow_up_questions(self, complaint_analysis: Dict) -> List[str]:
        """
        Generate appropriate follow-up questions based on the complaint analysis
        """
        
        category = complaint_analysis.get('category', 'general')
        severity = complaint_analysis.get('severity', 'mild')
        
        # Get category-specific questions
        base_questions = self._get_base_questions_for_category(category)
        
        # Add general medical history questions
        general_questions = self._get_general_medical_questions()
        
        # Combine and prioritize questions based on severity
        all_questions = base_questions + general_questions
        
        # Limit to 5-7 questions to avoid overwhelming the user
        if severity == 'severe':
            return all_questions[:7]
        elif severity == 'moderate':
            return all_questions[:5]
        else:
            return all_questions[:4]
    
    def ask_next_question(self) -> Optional[str]:
        """
        Get the next follow-up question to ask the user
        """
        if (self.consultation_state['current_question_index'] < 
            len(self.consultation_state['follow_up_questions'])):
            
            question = self.consultation_state['follow_up_questions'][
                self.consultation_state['current_question_index']
            ]
            return question
        else:
            self.consultation_state['consultation_complete'] = True
            return None
    
    def process_follow_up_answer(self, question: str, answer: str):
        """
        Process the user's answer to a follow-up question
        """
        # Store the answer
        question_key = f"question_{self.consultation_state['current_question_index']}"
        self.consultation_state['collected_info'][question_key] = {
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }
        
        # Move to next question
        self.consultation_state['current_question_index'] += 1
    
    def generate_comprehensive_analysis(self) -> str:
        """
        Generate comprehensive medical analysis based on all collected information
        """
        
        # Compile all information
        complaint = self.consultation_state['chief_complaint']
        collected_info = self.consultation_state['collected_info']
        
        # Create comprehensive analysis prompt
        analysis_prompt = self._get_comprehensive_analysis_prompt()
        
        # Format the collected information
        info_summary = self._format_collected_information(collected_info)
        
        try:
            messages = [
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": f"""
                Chief Complaint: {complaint}
                
                Additional Information Collected:
                {info_summary}
                
                Please provide a comprehensive analysis and recommendations.
                """}
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=DEFAULT_MODEL,
                temperature=0.7,
                max_tokens=1200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating comprehensive analysis: {e}")
            if self.language == "bn":
                return "দুঃখিত, বিশ্লেষণ তৈরি করতে একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
            else:
                return "Sorry, there was an error generating the analysis. Please try again."
    
    def _get_analysis_prompt(self) -> str:
        """Get the system prompt for analyzing initial complaints"""
        
        if self.language == "bn":
            return """আপনি একজন অভিজ্ঞ চিকিৎসক যিনি রোগীর প্রাথমিক অভিযোগ বিশ্লেষণ করেন।

আপনার কাজ:
1. রোগীর বার্তা চিকিৎসা সংক্রান্ত কিনা তা নির্ধারণ করুন
2. যদি চিকিৎসা সংক্রান্ত হয়, তাহলে বিভাগ নির্ধারণ করুন (যেমন: জ্বর, ব্যথা, হজম, শ্বাসযন্ত্র, চর্মরোগ, মানসিক স্বাস্থ্য)
3. গুরুত্বের মাত্রা নির্ধারণ করুন (হালকা, মাঝারি, গুরুতর)

উত্তর এই ফরম্যাটে দিন:
MEDICAL: [হ্যাঁ/না]
CATEGORY: [বিভাগ]
SEVERITY: [হালকা/মাঝারি/গুরুতর]
EMERGENCY: [হ্যাঁ/না]"""

        else:
            return """You are an experienced medical doctor analyzing a patient's initial complaint.

Your task:
1. Determine if the patient's message is medical/health-related
2. If medical, categorize it (e.g., fever, pain, digestive, respiratory, dermatology, mental_health, injury, chronic_condition)
3. Assess severity level (mild, moderate, severe)
4. Determine if it's an emergency requiring immediate medical attention

Respond in this format:
MEDICAL: [Yes/No]
CATEGORY: [category]
SEVERITY: [mild/moderate/severe]
EMERGENCY: [Yes/No]"""
    
    def _parse_analysis_response(self, analysis_text: str) -> Dict:
        """Parse the structured analysis response"""
        
        result = {
            "is_medical": False,
            "category": "general",
            "severity": "mild",
            "emergency": False
        }
        
        try:
            # Extract information using regex
            medical_match = re.search(r'MEDICAL:\s*(Yes|No|হ্যাঁ|না)', analysis_text, re.IGNORECASE)
            category_match = re.search(r'CATEGORY:\s*(\w+)', analysis_text, re.IGNORECASE)
            severity_match = re.search(r'SEVERITY:\s*(mild|moderate|severe|হালকা|মাঝারি|গুরুতর)', analysis_text, re.IGNORECASE)
            emergency_match = re.search(r'EMERGENCY:\s*(Yes|No|হ্যাঁ|না)', analysis_text, re.IGNORECASE)
            
            if medical_match:
                medical_value = medical_match.group(1).lower()
                result["is_medical"] = medical_value in ['yes', 'হ্যাঁ']
            
            if category_match:
                result["category"] = category_match.group(1).lower()
            
            if severity_match:
                severity_value = severity_match.group(1).lower()
                if severity_value in ['moderate', 'মাঝারি']:
                    result["severity"] = "moderate"
                elif severity_value in ['severe', 'গুরুতর']:
                    result["severity"] = "severe"
                else:
                    result["severity"] = "mild"
            
            if emergency_match:
                emergency_value = emergency_match.group(1).lower()
                result["emergency"] = emergency_value in ['yes', 'হ্যাঁ']
                
        except Exception as e:
            logging.error(f"Error parsing analysis response: {e}")
        
        return result
    
    def _get_base_questions_for_category(self, category: str) -> List[str]:
        """Get category-specific follow-up questions"""
        
        if self.language == "bn":
            questions_bn = {
                'fever': [
                    "আপনার জ্বর কত ডিগ্রি এবং কতদিন ধরে আছে?",
                    "জ্বরের সাথে কি অন্য কোন লক্ষণ আছে? (যেমন: কাশি, গলা ব্যথা, মাথা ব্যথা)",
                    "আপনি কি কোন ওষুধ খেয়েছেন? যদি হ্যাঁ, কি ওষুধ?",
                    "আপনার কি ঠান্ডা লাগার মত অনুভূতি হয় নাকি শুধু গরম লাগে?"
                ],
                'pain': [
                    "ব্যথাটি কোথায় এবং কতক্ষণ ধরে আছে?",
                    "ব্যথার ধরন কেমন? (তীক্ষ্ণ, ভোঁতা, জ্বালাপোড়া, চাপ ধরা)",
                    "ব্যথা কি ক্রমাগত নাকি মাঝে মাঝে হয়?",
                    "কোন কিছু করলে ব্যথা বাড়ে বা কমে?",
                    "১০ এর মধ্যে ব্যথার মাত্রা কত দিবেন?"
                ],
                'digestive': [
                    "পেটের সমস্যা কতদিন ধরে আছে?",
                    "আপনার কি বমি বমি ভাব বা বমি হয়েছে?",
                    "মলত্যাগে কোন সমস্যা আছে? (ডায়রিয়া বা কোষ্ঠকাঠিন্য)",
                    "খাবারের পর সমস্যা বেশি হয় নাকি খালি পেটে?",
                    "গত ২৪ ঘন্টায় আপনি কি খেয়েছেন?"
                ],
                'respiratory': [
                    "কাশি কতদিন ধরে আছে এবং কেমন ধরনের? (শুকনো নাকি কফ সহ)",
                    "শ্বাস নিতে কষ্ট হয় কি?",
                    "বুকে ব্যথা বা চাপ অনুভব করেন?",
                    "আপনি কি ধূমপান করেন বা ধূমপায়ীদের সাথে থাকেন?"
                ]
            }
            return questions_bn.get(category, questions_bn['pain'])
        
        else:
            questions_en = {
                'fever': [
                    "What is your temperature and how long have you had the fever?",
                    "Are there any other symptoms with the fever? (cough, sore throat, headache, etc.)",
                    "Have you taken any medication? If yes, which ones?",
                    "Do you experience chills or just feel hot?"
                ],
                'pain': [
                    "Where is the pain located and how long have you had it?",
                    "What type of pain is it? (sharp, dull, burning, pressure)",
                    "Is the pain constant or does it come and go?",
                    "What makes the pain better or worse?",
                    "On a scale of 1-10, how would you rate the pain intensity?"
                ],
                'digestive': [
                    "How long have you been experiencing digestive issues?",
                    "Have you experienced nausea or vomiting?",
                    "Any changes in bowel movements? (diarrhea or constipation)",
                    "Are symptoms worse after eating or on an empty stomach?",
                    "What have you eaten in the last 24 hours?"
                ],
                'respiratory': [
                    "How long have you had the cough and what type is it? (dry or with phlegm)",
                    "Do you experience shortness of breath?",
                    "Any chest pain or tightness?",
                    "Do you smoke or are you exposed to secondhand smoke?"
                ]
            }
            return questions_en.get(category, questions_en['pain'])
    
    def _get_general_medical_questions(self) -> List[str]:
        """Get general medical history questions"""
        
        if self.language == "bn":
            return [
                "আপনার বয়স কত এবং আগে কি এ ধরনের সমস্যা হয়েছে?",
                "আপনি কি নিয়মিত কোন ওষুধ খান বা কোন অ্যালার্জি আছে?",
                "আপনার কি কোন দীর্ঘমেয়াদী রোগ আছে? (যেমন: ডায়াবেটিস, উচ্চ রক্তচাপ)",
                "আপনি কি গর্ভবতী বা কোন বিশেষ অবস্থায় আছেন?"
            ]
        else:
            return [
                "What is your age and have you experienced this type of problem before?",
                "Are you taking any regular medications or do you have any allergies?",
                "Do you have any chronic medical conditions? (diabetes, high blood pressure, etc.)",
                "Are you pregnant or in any special condition I should know about?"
            ]
    
    def _get_comprehensive_analysis_prompt(self) -> str:
        """Get the system prompt for comprehensive analysis"""
        
        if self.language == "bn":
            return """আপনি একজন অভিজ্ঞ চিকিৎসক যিনি রোগীর সম্পূর্ণ তথ্যের ভিত্তিতে বিস্তারিত বিশ্লেষণ ও পরামর্শ প্রদান করেন।

আপনার উত্তরে অন্তর্ভুক্ত করুন:

১. **লক্ষণ বিশ্লেষণ**: 
   - প্রধান লক্ষণ ও সহযোগী লক্ষণের মূল্যায়ন
   - সম্ভাব্য কারণসমূহ

২. **সম্ভাব্য রোগ নির্ণয়**:
   - সবচেয়ে সম্ভাব্য ২-৩টি রোগের নাম
   - প্রতিটির সংক্ষিপ্ত ব্যাখ্যা

৩. **তাৎক্ষণিক পরামর্শ**:
   - ঘরোয়া চিকিৎসা (যদি প্রযোজ্য)
   - কি এড়িয়ে চলবেন
   - সতর্কতা লক্ষণ

৪. **পরবর্তী পদক্ষেপ**:
   - কখন ডাক্তার দেখাবেন
   - কি ধরনের পরীক্ষা লাগতে পারে
   - জরুরি অবস্থার লক্ষণ

৫. **প্রতিরোধ ও জীবনযাত্রা**:
   - ভবিষ্যতে প্রতিরোধের উপায়
   - জীবনযাত্রার পরিবর্তন

⚠️ **গুরুত্বপূর্ণ**: সর্বদা উল্লেখ করুন যে এটি প্রাথমিক মূল্যায়ন এবং চূড়ান্ত রোগ নির্ণয়ের জন্য একজন যোগ্য চিকিৎসকের পরামর্শ নিতে হবে।"""

        else:
            return """You are an experienced medical doctor providing comprehensive analysis and recommendations based on complete patient information.

Structure your response with:

1. **Symptom Analysis**:
   - Assessment of primary and associated symptoms
   - Possible underlying causes

2. **Differential Diagnosis**:
   - 2-3 most likely conditions
   - Brief explanation of each

3. **Immediate Recommendations**:
   - Home care measures (if applicable)
   - What to avoid
   - Warning signs to watch for

4. **Next Steps**:
   - When to see a doctor
   - What type of tests might be needed
   - Emergency warning signs

5. **Prevention & Lifestyle**:
   - How to prevent recurrence
   - Lifestyle modifications

⚠️ **Important**: Always emphasize that this is a preliminary assessment and professional medical consultation is needed for definitive diagnosis and treatment."""
    
    def _format_collected_information(self, collected_info: Dict) -> str:
        """Format the collected information for analysis"""
        
        formatted_info = []
        for key, value in collected_info.items():
            question = value.get('question', '')
            answer = value.get('answer', '')
            formatted_info.append(f"Q: {question}\nA: {answer}\n")
        
        return "\n".join(formatted_info)
    
    def reset_consultation(self):
        """Reset the consultation state for a new consultation"""
        self.consultation_state = {
            'stage': 'initial',
            'chief_complaint': '',
            'collected_info': {},
            'follow_up_questions': [],
            'current_question_index': 0,
            'consultation_complete': False
        }


class EnhancedChatSession:
    """Enhanced chat session with medical consultation capabilities"""
    
    def __init__(self, language="en"):
        self.language = language
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        self.consultation_manager = MedicalConsultationManager(language)
        self.history = []
        self.in_consultation = False
        
    def process_message(self, user_message: str) -> str:
        """Process user message with consultation flow"""
        
        # Add user message to history
        self.add_user_message(user_message)
        
        # Check if we're in an active consultation
        if self.in_consultation:
            return self._handle_consultation_flow(user_message)
        else:
            return self._handle_initial_message(user_message)
    
    def _handle_initial_message(self, user_message: str) -> str:
        """Handle the initial message from the user"""
        
        # Analyze if this is a medical complaint
        complaint_analysis = self.consultation_manager.analyze_initial_complaint(user_message)
        
        if complaint_analysis["is_medical"]:
            # Check if it's an emergency
            if complaint_analysis.get("emergency", False):
                return self._handle_emergency_response(user_message)
            
            # Start consultation process
            self.in_consultation = True
            self.consultation_manager.consultation_state['chief_complaint'] = user_message
            self.consultation_manager.consultation_state['stage'] = 'gathering_info'
            
            # Generate follow-up questions
            questions = self.consultation_manager.generate_follow_up_questions(complaint_analysis)
            self.consultation_manager.consultation_state['follow_up_questions'] = questions
            
            # Get the first follow-up question
            first_question = self.consultation_manager.ask_next_question()
            
            if self.language == "bn":
                initial_response = f"""আমি আপনার সমস্যাটি বুঝতে পেরেছি। আরও ভাল পরামর্শ দেওয়ার জন্য আমার কিছু প্রশ্ন আছে।

📋 **প্রশ্ন ১**: {first_question}

অনুগ্রহ করে বিস্তারিত উত্তর দিন।"""
            else:
                initial_response = f"""I understand your concern. To provide you with better guidance, I need to ask you some follow-up questions.

📋 **Question 1**: {first_question}

Please provide detailed answers."""
            
            response = initial_response
            
        else:
            # Handle non-medical queries with regular response
            response = self._get_regular_response(user_message)
        
        # Add response to history
        self.add_assistant_message(response)
        return response
    
    def _handle_consultation_flow(self, user_message: str) -> str:
        """Handle the consultation flow with follow-up questions"""
        
        # Get the current question
        current_question_index = self.consultation_manager.consultation_state['current_question_index'] - 1
        current_question = self.consultation_manager.consultation_state['follow_up_questions'][current_question_index]
        
        # Process the user's answer
        self.consultation_manager.process_follow_up_answer(current_question, user_message)
        
        # Check if there are more questions
        next_question = self.consultation_manager.ask_next_question()
        
        if next_question:
            # Ask the next question
            question_number = self.consultation_manager.consultation_state['current_question_index']
            
            if self.language == "bn":
                response = f"ধন্যবাদ। \n\n📋 **প্রশ্ন {question_number + 1}**: {next_question}"
            else:
                response = f"Thank you for the information.\n\n📋 **Question {question_number + 1}**: {next_question}"
        else:
            # All questions answered, provide comprehensive analysis
            self.consultation_manager.consultation_state['stage'] = 'analysis'
            
            if self.language == "bn":
                thinking_message = "ধন্যবাদ! এখন আমি আপনার সমস্ত তথ্য বিশ্লেষণ করে বিস্তারিত পরামর্শ প্রদান করছি...\n\n"
            else:
                thinking_message = "Thank you! Now I'm analyzing all your information to provide detailed recommendations...\n\n"
            
            comprehensive_analysis = self.consultation_manager.generate_comprehensive_analysis()
            response = thinking_message + comprehensive_analysis
            
            # End consultation
            self.in_consultation = False
            self.consultation_manager.reset_consultation()
        
        # Add response to history
        self.add_assistant_message(response)
        return response
    
    def _handle_emergency_response(self, user_message: str) -> str:
        """Handle emergency situations"""
        
        if self.language == "bn":
            emergency_response = """🚨 **জরুরি অবস্থা সনাক্ত করা হয়েছে**

আপনার বর্ণিত লক্ষণগুলি গুরুতর হতে পারে। অনুগ্রহ করে:

⚡ **তাৎক্ষণিক পদক্ষেপ**:
- এখনই নিকটস্থ হাসপাতালে যান
- জরুরি নম্বরে কল করুন (999 বা স্থানীয় জরুরি সেবা)
- পরিবারের কোন সদস্যকে সাথে নিন

⚠️ **সতর্কতা**: আমি একজন AI সহকারী, প্রকৃত চিকিৎসক নই। গুরুতর অবস্থায় অবিলম্বে পেশাদার চিকিৎসা সেবা নিন।

আপনি কি এখনই চিকিৎসা সেবা নিতে পারবেন?"""
        else:
            emergency_response = """🚨 **EMERGENCY SITUATION DETECTED**

Your described symptoms may be serious. Please:

⚡ **IMMEDIATE ACTION**:
- Go to the nearest hospital NOW
- Call emergency services (911 or local emergency number)
- Take someone with you if possible

⚠️ **WARNING**: I am an AI assistant, not a real doctor. In serious situations, seek immediate professional medical care.

Are you able to seek medical care right now?"""
        
        # End any ongoing consultation
        self.in_consultation = False
        self.consultation_manager.reset_consultation()
        
        # Add response to history
        self.add_assistant_message(emergency_response)
        return emergency_response
    
    def _get_regular_response(self, user_message: str) -> str:
        """Get regular AI response for non-medical queries"""
        
        try:
            # Get appropriate system prompt for regular conversation
            system_prompt = self._get_regular_system_prompt()
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.history)
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=DEFAULT_MODEL,
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating regular response: {e}")
            if self.language == "bn":
                return "দুঃখিত, একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
            else:
                return "Sorry, an error occurred. Please try again."
    
    def _get_regular_system_prompt(self) -> str:
        """Get system prompt for regular conversation"""
        
        if self.language == "bn":
            return """আপনি একজন সহায়ক AI চিকিৎসা সহকারী। আপনি সাধারণ স্বাস্থ্য তথ্য, প্রতিরোধমূলক যত্ন, এবং জীবনযাত্রার পরামর্শ প্রদান করতে পারেন।

যদি কেউ নির্দিষ্ট চিকিৎসা সমস্যার কথা বলে, তাহলে আরও বিস্তারিত তথ্যের জন্য প্রশ্ন করুন।

সর্বদা মনে রাখবেন যে আপনি প্রাথমিক তথ্য প্রদান করছেন এবং গুরুতর সমস্যার জন্য একজন যোগ্য চিকিৎসকের পরামর্শ নেওয়া জরুরি।"""
        else:
            return """You are a helpful AI medical assistant. You can provide general health information, preventive care advice, and lifestyle recommendations.

If someone mentions specific medical problems, ask for more detailed information to provide better guidance.

Always remember to emphasize that you're providing preliminary information and that serious issues require consultation with a qualified healthcare provider."""
    
    def add_user_message(self, message: str):
        """Add user message to chat history"""
        self.history.append({"role": "user", "content": message})
    
    def add_assistant_message(self, message: str):
        """Add assistant message to chat history"""
        self.history.append({"role": "assistant", "content": message})
    
    def clear_history(self):
        """Clear chat history and reset consultation"""
        self.history = []
        self.in_consultation = False
        self.consultation_manager.reset_consultation()
    
    def get_consultation_progress(self) -> Dict:
        """Get current consultation progress information"""
        if not self.in_consultation:
            return {"active": False}
        
        total_questions = len(self.consultation_manager.consultation_state['follow_up_questions'])
        current_index = self.consultation_manager.consultation_state['current_question_index']
        
        return {
            "active": True,
            "stage": self.consultation_manager.consultation_state['stage'],
            "progress": f"{current_index}/{total_questions}",
            "questions_completed": current_index,
            "total_questions": total_questions,
            "chief_complaint": self.consultation_manager.consultation_state['chief_complaint']
        }


# Integration functions for the existing streamlit app
def create_enhanced_chat_session(language="en"):
    """Create an enhanced chat session with consultation capabilities"""
    return EnhancedChatSession(language)


def process_consultation_message(chat_session, user_message):
    """Process a message through the consultation system"""
    return chat_session.process_message(user_message)


def get_consultation_status_display(chat_session, language="en"):
    """Get consultation status for display in UI"""
    progress = chat_session.get_consultation_progress()
    
    if not progress["active"]:
        return None
    
    if language == "bn":
        if progress["stage"] == "gathering_info":
            return f"""
            📋 **পরামর্শ চলছে** 
            প্রগতি: {progress["progress"]} প্রশ্ন সম্পন্ন
            মূল সমস্যা: {progress["chief_complaint"][:50]}...
            """
        elif progress["stage"] == "analysis":
            return "🔍 **বিশ্লেষণ করা হচ্ছে...** সম্পূর্ণ তথ্যের ভিত্তিতে পরামর্শ প্রস্তুত করা হচ্ছে"
    else:
        if progress["stage"] == "gathering_info":
            return f"""
            📋 **Consultation in Progress** 
            Progress: {progress["progress"]} questions completed
            Chief complaint: {progress["chief_complaint"][:50]}...
            """
        elif progress["stage"] == "analysis":
            return "🔍 **Analyzing...** Preparing recommendations based on complete information"
    
    return None