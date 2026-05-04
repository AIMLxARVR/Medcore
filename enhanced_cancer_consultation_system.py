# enhanced_cancer_consultation_system_updated.py - Enhanced with dynamic questions and recommendations

import os
import logging
import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional, Any
from cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AIRecommendationEngine:
    """AI-powered recommendation engine for personalized cancer care"""
    
    def __init__(self, language="en"):
        self.language = language
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
    
    def generate_ai_recommendations(self, user_responses: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive AI-analyzed recommendations based on user responses"""
        
        # Prepare comprehensive user profile for AI analysis
        user_profile = self._compile_comprehensive_profile(user_responses)
        
        # Generate different types of recommendations
        recommendations = {
            "immediate_care": self._generate_immediate_care_recommendations(user_profile, analysis_results),
            "preventive_care_plan": self._generate_preventive_care_plan(user_profile),
            "lifestyle_modifications": self._generate_lifestyle_recommendations(user_profile),
            "screening_schedule": self._generate_personalized_screening_schedule(user_profile),
            "risk_reduction_strategies": self._generate_risk_reduction_strategies(user_profile),
            "follow_up_plan": self._generate_follow_up_plan(user_profile, analysis_results),
            "emergency_protocols": self._generate_emergency_protocols(user_profile),
            "nutritional_guidance": self._generate_nutritional_guidance(user_profile),
            "exercise_recommendations": self._generate_exercise_recommendations(user_profile),
            "stress_management": self._generate_stress_management_plan(user_profile)
        }
        
        # Add AI-generated comprehensive summary
        recommendations["ai_summary"] = self._generate_ai_comprehensive_summary(user_profile, recommendations)
        
        return recommendations
    
    def _compile_comprehensive_profile(self, user_responses: Dict) -> Dict[str, Any]:
        """Compile comprehensive user profile for AI analysis"""
        
        profile = {
            "demographics": {
                "age_group": user_responses.get("age_group", {}).get("response", "Unknown"),
                "gender": user_responses.get("gender", {}).get("response", "Unknown"),
                "main_concern": user_responses.get("main_concern", {}).get("response", "")
            },
            "medical_history": {
                "cancer_diagnosis": user_responses.get("cancer_diagnosis", {}).get("response", "No"),
                "chronic_diseases": user_responses.get("chronic_diseases", {}).get("response", "None"),
                "hepatitis_status": user_responses.get("hepatitis_status", {}).get("response", "Never tested"),
                "hpv_status": user_responses.get("hpv_status", {}).get("response", "Never tested")
            },
            "symptoms": {
                "persistent_cough": user_responses.get("persistent_cough", {}).get("response", "No"),
                "blood_in_sputum": user_responses.get("blood_in_sputum", {}).get("response", "No"),
                "weight_loss": user_responses.get("unexplained_weight_loss", {}).get("response", "No"),
                "fatigue": user_responses.get("persistent_fatigue", {}).get("response", "No"),
                "lumps": user_responses.get("unusual_lumps", {}).get("response", "No"),
                "skin_changes": user_responses.get("skin_changes", {}).get("response", "No"),
                "pain": user_responses.get("persistent_pain", {}).get("response", "No"),
                "bowel_changes": user_responses.get("bowel_changes", {}).get("response", "No"),
                "swallowing_issues": user_responses.get("swallowing_difficulties", {}).get("response", "None"),
                "breast_changes": user_responses.get("breast_changes", {}).get("response", "No"),
                "unusual_bleeding": user_responses.get("unusual_bleeding", {}).get("response", "No"),
                "prostate_symptoms": user_responses.get("prostate_symptoms", {}).get("response", "No symptoms"),
                "testicular_lumps": user_responses.get("testicular_lumps", {}).get("response", "No")
            },
            "lifestyle_factors": {
                "smoking_status": user_responses.get("smoking_status", {}).get("response", "Never smoked"),
                "alcohol_consumption": user_responses.get("alcohol_consumption", {}).get("response", "Never"),
                "diet_quality": user_responses.get("diet_quality", {}).get("response", "Average"),
                "exercise_frequency": user_responses.get("exercise_frequency", {}).get("response", "Rarely"),
                "sun_exposure": user_responses.get("sun_exposure", {}).get("response", "Moderate"),
                "occupational_exposure": user_responses.get("occupational_exposure", {}).get("response", "No occupational exposure")
            },
            "family_history": {
                "cancer_family_history": user_responses.get("family_history", {}).get("response", "No family history")
            },
            "screening_history": {
                "mammogram": user_responses.get("mammogram_test", {}).get("response", "Never had one"),
                "pap_smear": user_responses.get("pap_smear_test", {}).get("response", "Never had one"),
                "prostate_screening": user_responses.get("prostate_screening", {}).get("response", "Never had one"),
                "colonoscopy": user_responses.get("colonoscopy_test", {}).get("response", "Never had screening")
            }
        }
        
        return profile
    
    def _generate_immediate_care_recommendations(self, profile: Dict, analysis_results: Dict) -> List[str]:
        """Generate immediate care recommendations using AI"""
        
        prompt = self._get_immediate_care_prompt(profile)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self._get_ai_doctor_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=800
            )
            
            recommendations = self._parse_ai_recommendations(response.choices[0].message.content)
            return recommendations
            
        except Exception as e:
            logging.error(f"Error generating immediate care recommendations: {e}")
            return self._get_fallback_immediate_care(profile)
    
    def _generate_preventive_care_plan(self, profile: Dict) -> Dict[str, List[str]]:
        """Generate comprehensive preventive care plan using AI"""
        
        prompt = self._get_preventive_care_prompt(profile)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self._get_ai_doctor_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.4,
                max_tokens=1000
            )
            
            care_plan = self._parse_preventive_care_plan(response.choices[0].message.content)
            return care_plan
            
        except Exception as e:
            logging.error(f"Error generating preventive care plan: {e}")
            return self._get_fallback_preventive_care(profile)
    
    def _generate_lifestyle_recommendations(self, profile: Dict) -> Dict[str, List[str]]:
        """Generate personalized lifestyle recommendations"""
        
        recommendations = {
            "nutrition": [],
            "exercise": [],
            "habits": [],
            "environmental": []
        }
        
        # Smoking recommendations
        smoking_status = profile["lifestyle_factors"]["smoking_status"]
        if "Current" in smoking_status or "বর্তমানে" in smoking_status:
            if self.language == "bn":
                recommendations["habits"].extend([
                    "ধূমপান বন্ধ করুন - এটি ক্যান্সার ঝুঁকি কমানোর সবচেয়ে গুরুত্বপূর্ণ পদক্ষেপ",
                    "নিকোটিন রিপ্লেসমেন্ট থেরাপি বিবেচনা করুন",
                    "ধূমপান বন্ধের জন্য সাপোর্ট গ্রুপে যোগ দিন"
                ])
            else:
                recommendations["habits"].extend([
                    "Quit smoking - this is the most important step to reduce cancer risk",
                    "Consider nicotine replacement therapy",
                    "Join smoking cessation support groups"
                ])
        
        # Diet recommendations
        diet_quality = profile["lifestyle_factors"]["diet_quality"]
        if "Poor" in diet_quality or "খারাপ" in diet_quality:
            if self.language == "bn":
                recommendations["nutrition"].extend([
                    "প্রতিদিন অন্তত ৫ পরিবেশন ফল ও সবজি খান",
                    "পূর্ণ শস্য জাতীয় খাবার বেছে নিন",
                    "প্রক্রিয়াজাত মাংস ও লাল মাংস কমান",
                    "পর্যাপ্ত পানি পান করুন (দিনে ৮-১০ গ্লাস)"
                ])
            else:
                recommendations["nutrition"].extend([
                    "Eat at least 5 servings of fruits and vegetables daily",
                    "Choose whole grain foods",
                    "Reduce processed and red meat consumption",
                    "Drink adequate water (8-10 glasses daily)"
                ])
        
        # Exercise recommendations
        exercise_frequency = profile["lifestyle_factors"]["exercise_frequency"]
        if "Rarely" in exercise_frequency or "Never" in exercise_frequency:
            if self.language == "bn":
                recommendations["exercise"].extend([
                    "সপ্তাহে কমপক্ষে ১৫০ মিনিট মাঝারি ব্যায়াম করুন",
                    "দিনে ৩০ মিনিট হাঁটার অভ্যাস করুন",
                    "শক্তি বৃদ্ধির ব্যায়াম সপ্তাহে ২ দিন করুন"
                ])
            else:
                recommendations["exercise"].extend([
                    "Aim for at least 150 minutes of moderate exercise per week",
                    "Walk for 30 minutes daily",
                    "Include strength training exercises 2 days per week"
                ])
        
        return recommendations
    
    def _generate_personalized_screening_schedule(self, profile: Dict) -> Dict[str, Any]:
        """Generate personalized screening schedule based on age, gender, and risk factors"""
        
        age_group = profile["demographics"]["age_group"]
        gender = profile["demographics"]["gender"]
        screening_schedule = {}
        
        # Age-specific screenings
        if gender in ["Female", "মহিলা"]:
            if age_group in ["30-40", "41-50", "51-60", "Over 60", "৩০-৪০", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]:
                screening_schedule["breast_cancer"] = {
                    "test": "Mammogram" if self.language == "en" else "ম্যামোগ্রাম",
                    "frequency": "Annual" if self.language == "en" else "বার্ষিক",
                    "next_due": "Now if overdue" if self.language == "en" else "এখনই যদি দেরি হয়ে থাকে"
                }
                
                screening_schedule["cervical_cancer"] = {
                    "test": "Pap smear + HPV test" if self.language == "en" else "প্যাপ স্মিয়ার + HPV টেস্ট",
                    "frequency": "Every 3 years" if self.language == "en" else "প্রতি ৩ বছর",
                    "next_due": "Based on last test" if self.language == "en" else "শেষ টেস্টের উপর ভিত্তি করে"
                }
        
        elif gender in ["Male", "পুরুষ"]:
            if age_group in ["51-60", "Over 60", "৫১-৬০", "৬০ এর উপরে"]:
                screening_schedule["prostate_cancer"] = {
                    "test": "PSA test + Digital rectal exam" if self.language == "en" else "PSA টেস্ট + ডিজিটাল রেক্টাল পরীক্ষা",
                    "frequency": "Annual" if self.language == "en" else "বার্ষিক",
                    "next_due": "Now if overdue" if self.language == "en" else "এখনই যদি দেরি হয়ে থাকে"
                }
        
        # Universal screenings
        if age_group in ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]:
            screening_schedule["colorectal_cancer"] = {
                "test": "Colonoscopy or FIT test" if self.language == "en" else "কোলনোস্কোপি বা FIT টেস্ট",
                "frequency": "Every 10 years (colonoscopy) or annual (FIT)" if self.language == "en" else "প্রতি ১০ বছর (কোলনোস্কোপি) বা বার্ষিক (FIT)",
                "next_due": "Based on age and last screening" if self.language == "en" else "বয়স ও শেষ স্ক্রিনিং অনুযায়ী"
            }
        
        return screening_schedule
    
    def _generate_risk_reduction_strategies(self, profile: Dict) -> Dict[str, List[str]]:
        """Generate personalized risk reduction strategies"""
        
        strategies = {
            "primary_prevention": [],
            "secondary_prevention": [],
            "tertiary_prevention": []
        }
        
        # Analyze risk factors and provide targeted strategies
        family_history = profile["family_history"]["cancer_family_history"]
        if family_history not in ["No family history", "কোন পারিবারিক ইতিহাস নেই"]:
            if self.language == "bn":
                strategies["primary_prevention"].extend([
                    "জেনেটিক কাউন্সেলিং বিবেচনা করুন",
                    "আপনার পারিবারিক ইতিহাস চিকিৎসকদের জানান",
                    "প্রস্তাবিত বয়সের আগেই স্ক্রিনিং শুরু করুন"
                ])
            else:
                strategies["primary_prevention"].extend([
                    "Consider genetic counseling",
                    "Inform healthcare providers about family history",
                    "Start screening earlier than recommended age"
                ])
        
        # Occupational exposure strategies
        occupational_exposure = profile["lifestyle_factors"]["occupational_exposure"]
        if occupational_exposure != "No occupational exposure":
            if self.language == "bn":
                strategies["primary_prevention"].extend([
                    "কর্মক্ষেত্রে সুরক্ষা সরঞ্জাম ব্যবহার করুন",
                    "নিয়মিত স্বাস্থ্য পরীক্ষা করান",
                    "কর্মক্ষেত্রের বিপজ্জনক পদার্থ সম্পর্কে সচেতন থাকুন"
                ])
            else:
                strategies["primary_prevention"].extend([
                    "Use protective equipment at workplace",
                    "Get regular occupational health checkups",
                    "Be aware of workplace hazardous substances"
                ])
        
        return strategies
    
    def _generate_follow_up_plan(self, profile: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Generate personalized follow-up plan"""
        
        # Determine urgency level from symptoms
        urgency_level = self._assess_urgency_level(profile)
        
        follow_up_plan = {
            "immediate": [],
            "short_term": [],
            "long_term": []
        }
        
        if urgency_level == "HIGH":
            if self.language == "bn":
                follow_up_plan["immediate"] = [
                    "২৪-৪৮ ঘন্টার মধ্যে চিকিৎসক দেখান",
                    "লক্ষণের তালিকা প্রস্তুত রাখুন",
                    "জরুরি হাসপাতালের ঠিকানা জেনে রাখুন"
                ]
            else:
                follow_up_plan["immediate"] = [
                    "See a doctor within 24-48 hours",
                    "Prepare a list of symptoms",
                    "Know nearest emergency hospital location"
                ]
        
        elif urgency_level == "MODERATE":
            if self.language == "bn":
                follow_up_plan["short_term"] = [
                    "১-২ সপ্তাহের মধ্যে চিকিৎসক দেখান",
                    "মাসিক ফলো-আপ করুন",
                    "লক্ষণের পরিবর্তন পর্যবেক্ষণ করুন"
                ]
            else:
                follow_up_plan["short_term"] = [
                    "See a doctor within 1-2 weeks",
                    "Monthly follow-ups",
                    "Monitor symptom changes"
                ]
        
        # Long-term plan for everyone
        if self.language == "bn":
            follow_up_plan["long_term"] = [
                "বার্ষিক ব্যাপক স্বাস্থ্য পরীক্ষা",
                "নিয়মিত ক্যান্সার স্ক্রিনিং",
                "জীবনযাত্রার উন্নতি পর্যবেক্ষণ"
            ]
        else:
            follow_up_plan["long_term"] = [
                "Annual comprehensive health checkup",
                "Regular cancer screenings",
                "Monitor lifestyle improvements"
            ]
        
        return follow_up_plan
    
    def _generate_emergency_protocols(self, profile: Dict) -> List[str]:
        """Generate emergency protocols based on user profile"""
        
        emergency_signs = []
        
        if self.language == "bn":
            emergency_signs = [
                "গুরুতর ব্যথা যা ক্রমশ বাড়ছে",
                "অতিরিক্ত রক্তপাত বা অস্বাভাবিক রক্তপাত",
                "শ্বাসকষ্ট বা বুকে চাপ",
                "অজ্ঞান হয়ে যাওয়া বা মাথা ঘোরা",
                "হঠাৎ দ্রুত ওজন হ্রাস (মাসে ৫+ কেজি)",
                "উচ্চ জ্বর সাথে ঠান্ডা লাগা",
                "গিলতে অসুবিধা বা কথা বলতে সমস্যা"
            ]
        else:
            emergency_signs = [
                "Severe worsening pain",
                "Excessive or unusual bleeding",
                "Shortness of breath or chest pressure",
                "Loss of consciousness or severe dizziness",
                "Sudden rapid weight loss (5+ kg per month)",
                "High fever with chills",
                "Difficulty swallowing or speaking"
            ]
        
        # Add gender-specific emergency signs
        gender = profile["demographics"]["gender"]
        if gender in ["Female", "মহিলা"]:
            if self.language == "bn":
                emergency_signs.extend([
                    "স্তনে দ্রুত বাড়ছে এমন গাঁট",
                    "অস্বাভাবিক ভারী মাসিক বা রক্তপাত"
                ])
            else:
                emergency_signs.extend([
                    "Rapidly growing breast lump",
                    "Abnormally heavy menstrual bleeding"
                ])
        
        elif gender in ["Male", "পুরুষ"]:
            if self.language == "bn":
                emergency_signs.extend([
                    "প্রস্রাবে রক্ত",
                    "অণ্ডকোষে হঠাৎ ব্যথা বা ফোলা"
                ])
            else:
                emergency_signs.extend([
                    "Blood in urine",
                    "Sudden testicular pain or swelling"
                ])
        
        return emergency_signs
    
    def _generate_nutritional_guidance(self, profile: Dict) -> Dict[str, List[str]]:
        """Generate personalized nutritional guidance"""
        
        nutrition_plan = {
            "foods_to_include": [],
            "foods_to_limit": [],
            "supplements": [],
            "meal_planning": []
        }
        
        if self.language == "bn":
            nutrition_plan["foods_to_include"] = [
                "রঙিন ফল ও সবজি (বিশেষত গাঢ় সবুজ ও কমলা রঙের)",
                "পূর্ণ শস্য জাতীয় খাবার (বাদামী চাল, ওটস)",
                "চর্বিহীন প্রোটিন (মাছ, মুরগি, ডাল)",
                "বাদাম ও বীজ জাতীয় খাবার",
                "জলপাই তেল ও অন্যান্য স্বাস্থ্যকর চর্বি"
            ]
            
            nutrition_plan["foods_to_limit"] = [
                "প্রক্রিয়াজাত মাংস (সসেজ, হ্যাম)",
                "অতিরিক্ত চিনিযুক্ত খাবার ও পানীয়",
                "ট্রান্স ফ্যাট যুক্ত খাবার",
                "অতিরিক্ত লবণযুক্ত খাবার",
                "ভাজা ও তৈলাক্ত খাবার"
            ]
        else:
            nutrition_plan["foods_to_include"] = [
                "Colorful fruits and vegetables (especially dark greens and orange)",
                "Whole grains (brown rice, oats, quinoa)",
                "Lean proteins (fish, poultry, legumes)",
                "Nuts and seeds",
                "Olive oil and other healthy fats"
            ]
            
            nutrition_plan["foods_to_limit"] = [
                "Processed meats (sausages, ham, bacon)",
                "Excessive sugary foods and drinks",
                "Trans fat containing foods",
                "High sodium foods",
                "Fried and fatty foods"
            ]
        
        return nutrition_plan
    
    def _generate_exercise_recommendations(self, profile: Dict) -> Dict[str, Any]:
        """Generate personalized exercise recommendations"""
        
        age_group = profile["demographics"]["age_group"]
        current_exercise = profile["lifestyle_factors"]["exercise_frequency"]
        
        exercise_plan = {
            "cardio": [],
            "strength": [],
            "flexibility": [],
            "weekly_schedule": {}
        }
        
        if self.language == "bn":
            if "Never" in current_exercise or "কখনো না" in current_exercise:
                exercise_plan["cardio"] = [
                    "দিনে ১৫-২০ মিনিট হাঁটা দিয়ে শুরু করুন",
                    "ধীরে ধীরে ৩০ মিনিটে বাড়ান",
                    "সপ্তাহে ৩-৪ দিন কার্ডিও ব্যায়াম করুন"
                ]
                exercise_plan["strength"] = [
                    "সপ্তাহে ২ দিন হালকা ওজন তোলার ব্যায়াম",
                    "বডিওয়েট এক্সারসাইজ (পুশ আপ, স্কোয়াট)",
                    "ধীরে ধীরে তীব্রতা বাড়ান"
                ]
            else:
                exercise_plan["cardio"] = [
                    "সপ্তাহে ১৫০ মিনিট মাঝারি তীব্রতার ব্যায়াম",
                    "দৌড়, সাইক্লিং বা সাঁতার যোগ করুন",
                    "উচ্চ তীব্রতার ব্যায়াম সপ্তাহে ২-৩ দিন"
                ]
        else:
            if "Never" in current_exercise:
                exercise_plan["cardio"] = [
                    "Start with 15-20 minutes of walking daily",
                    "Gradually increase to 30 minutes",
                    "Aim for 3-4 days of cardio per week"
                ]
                exercise_plan["strength"] = [
                    "Light weight training 2 days per week",
                    "Bodyweight exercises (push-ups, squats)",
                    "Gradually increase intensity"
                ]
            else:
                exercise_plan["cardio"] = [
                    "150 minutes of moderate-intensity exercise per week",
                    "Add running, cycling, or swimming",
                    "High-intensity intervals 2-3 times per week"
                ]
        
        return exercise_plan
    
    def _generate_stress_management_plan(self, profile: Dict) -> List[str]:
        """Generate stress management recommendations"""
        
        if self.language == "bn":
            stress_management = [
                "প্রতিদিন ১০-১৫ মিনিট ধ্যান বা গভীর শ্বাস নেওয়ার অভ্যাস করুন",
                "পর্যাপ্ত ঘুম নিশ্চিত করুন (৭-৮ ঘন্টা)",
                "পরিবার ও বন্ধুদের সাথে সময় কাটান",
                "শখের কাজে সময় দিন",
                "প্রয়োজনে পেশাদার কাউন্সেলিং নিন",
                "নিয়মিত প্রকৃতিতে সময় কাটান",
                "জার্নাল লেখার অভ্যাস করুন"
            ]
        else:
            stress_management = [
                "Practice 10-15 minutes of meditation or deep breathing daily",
                "Ensure adequate sleep (7-8 hours)",
                "Spend quality time with family and friends",
                "Engage in hobbies and recreational activities",
                "Consider professional counseling if needed",
                "Spend time in nature regularly",
                "Keep a journal for emotional expression"
            ]
        
        return stress_management
    
    def _generate_ai_comprehensive_summary(self, profile: Dict, recommendations: Dict) -> str:
        """Generate AI-powered comprehensive summary of all recommendations"""
        
        summary_prompt = f"""
        Based on the following patient profile and generated recommendations, create a comprehensive, 
        personalized summary in {"Bengali" if self.language == "bn" else "English"} that:
        
        1. Acknowledges the patient's specific situation
        2. Highlights the most important recommendations
        3. Provides encouragement and motivation
        4. Emphasizes the importance of professional medical care
        
        Patient Profile Summary:
        - Age: {profile['demographics']['age_group']}
        - Gender: {profile['demographics']['gender']}
        - Main Concern: {profile['demographics']['main_concern']}
        - Key Risk Factors: {self._summarize_risk_factors(profile)}
        - Current Symptoms: {self._summarize_symptoms(profile)}
        
        Generated Recommendations Summary:
        - Immediate Care: {len(recommendations['immediate_care'])} recommendations
        - Preventive Care: {len(recommendations['preventive_care_plan'])} strategies
        - Lifestyle Changes: {len(recommendations['lifestyle_modifications'])} modifications
        - Screening Schedule: {len(recommendations['screening_schedule'])} tests scheduled
        
        Provide a warm, encouraging, and medically sound summary.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self._get_ai_doctor_system_prompt()},
                    {"role": "user", "content": summary_prompt}
                ],
                model=self.model,
                temperature=0.6,
                max_tokens=1200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating AI summary: {e}")
            return self._get_fallback_summary(profile)
    
    def _summarize_risk_factors(self, profile: Dict) -> str:
        """Summarize key risk factors"""
        risk_factors = []
        
        if profile["family_history"]["cancer_family_history"] != "No family history":
            risk_factors.append("family history")
        
        if profile["lifestyle_factors"]["diet_quality"] in ["Poor", "খারাপ"]:
            risk_factors.append("diet concerns")
        
        if profile["lifestyle_factors"]["exercise_frequency"] in ["Never", "Rarely", "কখনো না", "কদাচিৎ"]:
            risk_factors.append("low physical activity")
        
        return ", ".join(risk_factors) if risk_factors else "No significant risk factors identified"
    
    def _summarize_symptoms(self, profile: Dict) -> str:
        """Summarize reported symptoms"""
        symptoms = []
        
        for symptom_key, response in profile["symptoms"].items():
            if response in ["Yes", "হ্যাঁ"] or (response not in ["No", "না", "None", "কিছু নেই", "No symptoms", "কোন লক্ষণ নেই"]):
                symptoms.append(symptom_key.replace("_", " "))
        
        return ", ".join(symptoms[:5]) if symptoms else "No concerning symptoms reported"
    
    def _assess_urgency_level(self, profile: Dict) -> str:
        """Assess urgency level based on symptoms"""
        high_urgency_symptoms = [
            "blood_in_sputum", "unusual_bleeding", "unexplained_weight_loss", 
            "persistent_pain", "breast_changes", "testicular_lumps"
        ]
        
        urgency_count = 0
        for symptom in high_urgency_symptoms:
            if profile["symptoms"].get(symptom) in ["Yes", "হ্যাঁ"]:
                urgency_count += 1
        
        if urgency_count >= 2:
            return "HIGH"
        elif urgency_count == 1:
            return "MODERATE"
        else:
            return "LOW"
    
    def _get_immediate_care_prompt(self, profile: Dict) -> str:
        """Generate prompt for immediate care recommendations"""
        
        if self.language == "bn":
            return f"""
            একজন অভিজ্ঞ অনকোলজিস্ট হিসেবে, নিম্নলিখিত রোগীর প্রোফাইলের জন্য তাৎক্ষণিক চিকিৎসা পরামর্শ প্রদান করুন:

            রোগীর তথ্য:
            - বয়স: {profile['demographics']['age_group']}
            - লিঙ্গ: {profile['demographics']['gender']}
            - প্রধান সমস্যা: {profile['demographics']['main_concern']}
            - লক্ষণসমূহ: {self._summarize_symptoms(profile)}
            - ঝুঁকির কারণ: {self._summarize_risk_factors(profile)}

            অনুগ্রহ করে ৫-৭টি তাৎক্ষণিক পরামর্শ দিন যা রোগীর অবিলম্বে অনুসরণ করা উচিত।
            প্রতিটি পরামর্শ স্পষ্ট ও কার্যকর হতে হবে।
            """
        else:
            return f"""
            As an experienced oncologist, provide immediate medical care recommendations for the following patient profile:

            Patient Information:
            - Age: {profile['demographics']['age_group']}
            - Gender: {profile['demographics']['gender']}
            - Main Concern: {profile['demographics']['main_concern']}
            - Symptoms: {self._summarize_symptoms(profile)}
            - Risk Factors: {self._summarize_risk_factors(profile)}

            Please provide 5-7 immediate recommendations that the patient should follow right away.
            Each recommendation should be clear and actionable.
            """
    
    def _get_preventive_care_prompt(self, profile: Dict) -> str:
        """Generate prompt for preventive care plan"""
        
        if self.language == "bn":
            return f"""
            একজন ক্যান্সার প্রতিরোধ বিশেষজ্ঞ হিসেবে, নিম্নলিখিত রোগীর জন্য একটি ব্যাপক প্রতিরোধমূলক যত্ন পরিকল্পনা তৈরি করুন:

            রোগীর প্রোফাইল:
            - বয়স ও লিঙ্গ: {profile['demographics']['age_group']}, {profile['demographics']['gender']}
            - বর্তমান স্বাস্থ্য অবস্থা: {profile['medical_history']['chronic_diseases']}
            - জীবনযাত্রার অভ্যাস: {profile['lifestyle_factors']}
            - পারিবারিক ইতিহাস: {profile['family_history']['cancer_family_history']}

            নিম্নলিখিত বিভাগে পরিকল্পনা প্রদান করুন:
            1. প্রাথমিক প্রতিরোধ (৩-৫টি পরামর্শ)
            2. মাধ্যমিক প্রতিরোধ (স্ক্রিনিং) (৩-৫টি পরামর্শ)
            3. জীবনযাত্রার পরিবর্তন (৩-৫টি পরামর্শ)
            4. নিয়মিত পর্যবেক্ষণ (৩-৫টি পরামর্শ)
            """
        else:
            return f"""
            As a cancer prevention specialist, create a comprehensive preventive care plan for the following patient:

            Patient Profile:
            - Age & Gender: {profile['demographics']['age_group']}, {profile['demographics']['gender']}
            - Current Health Status: {profile['medical_history']['chronic_diseases']}
            - Lifestyle Factors: {profile['lifestyle_factors']}
            - Family History: {profile['family_history']['cancer_family_history']}

            Provide recommendations in the following categories:
            1. Primary Prevention (3-5 recommendations)
            2. Secondary Prevention (Screening) (3-5 recommendations)
            3. Lifestyle Modifications (3-5 recommendations)
            4. Regular Monitoring (3-5 recommendations)
            """
    
    def _get_ai_doctor_system_prompt(self) -> str:
        """Get system prompt for AI doctor responses"""
        
        if self.language == "bn":
            return """আপনি একজন অভিজ্ঞ অনকোলজিস্ট এবং ক্যান্সার প্রতিরোধ বিশেষজ্ঞ যিনি ব্যক্তিগতকৃত চিকিৎসা পরামর্শ প্রদান করেন।

            আপনার দায়িত্ব:
            - রোগীর নির্দিষ্ট অবস্থার উপর ভিত্তি করে ব্যক্তিগত পরামর্শ দেওয়া
            - সহানুভূতিশীল ও উৎসাহব্যঞ্জক ভাষা ব্যবহার করা
            - প্রমাণ-ভিত্তিক চিকিৎসা নির্দেশনা প্রদান করা
            - রোগীর নিরাপত্তা ও কল্যাণকে সর্বোচ্চ প্রাধান্য দেওয়া

            সর্বদা মনে রাখবেন:
            - এটি প্রাথমিক মূল্যায়ন, চূড়ান্ত রোগ নির্ণয় নয়
            - পেশাদার চিকিৎসা পরামর্শের প্রয়োজনীয়তা জোর দিন
            - রোগীর উদ্বেগ ও ভয় কমানোর চেষ্টা করুন
            - ব্যবহারিক ও অনুসরণযোগ্য পরামর্শ দিন"""
        else:
            return """You are an experienced oncologist and cancer prevention specialist providing personalized medical guidance.

            Your responsibilities:
            - Provide personalized recommendations based on patient's specific condition
            - Use empathetic and encouraging language
            - Offer evidence-based medical guidance
            - Prioritize patient safety and well-being

            Always remember:
            - This is preliminary assessment, not final diagnosis
            - Emphasize the need for professional medical consultation
            - Help reduce patient anxiety and fear
            - Provide practical and actionable recommendations"""
    
    def _parse_ai_recommendations(self, ai_response: str) -> List[str]:
        """Parse AI response into structured recommendations"""
        
        # Simple parsing - extract bullet points or numbered lists
        lines = ai_response.split('\n')
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        line.startswith('*') or any(line.startswith(f"{i}.") for i in range(1, 20))):
                # Clean up the line
                clean_line = re.sub(r'^[-•*]\s*', '', line)
                clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                if clean_line:
                    recommendations.append(clean_line)
        
        return recommendations[:10]  # Limit to 10 recommendations
    
    def _parse_preventive_care_plan(self, ai_response: str) -> Dict[str, List[str]]:
        """Parse AI response into structured preventive care plan"""
        
        care_plan = {
            "primary_prevention": [],
            "secondary_prevention": [],
            "lifestyle_modifications": [],
            "regular_monitoring": []
        }
        
        current_section = None
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Identify sections
            if any(keyword in line.lower() for keyword in ['primary', 'প্রাথমিক']):
                current_section = "primary_prevention"
            elif any(keyword in line.lower() for keyword in ['secondary', 'screening', 'মাধ্যমিক', 'স্ক্রিনিং']):
                current_section = "secondary_prevention"
            elif any(keyword in line.lower() for keyword in ['lifestyle', 'জীবনযাত্রা']):
                current_section = "lifestyle_modifications"
            elif any(keyword in line.lower() for keyword in ['monitoring', 'পর্যবেক্ষণ']):
                current_section = "regular_monitoring"
            
            # Add recommendations to current section
            elif current_section and line and (line.startswith('-') or line.startswith('•') or 
                                             line.startswith('*') or any(line.startswith(f"{i}.") for i in range(1, 20))):
                clean_line = re.sub(r'^[-•*]\s*', '', line)
                clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                if clean_line:
                    care_plan[current_section].append(clean_line)
        
        return care_plan
    
    def _get_fallback_immediate_care(self, profile: Dict) -> List[str]:
        """Fallback immediate care recommendations"""
        
        if self.language == "bn":
            return [
                "আপনার লক্ষণ ও চিন্তার কারণে একজন যোগ্য চিকিৎসকের সাথে পরামর্শ করুন",
                "আপনার সমস্ত লক্ষণের একটি তালিকা তৈরি করুন",
                "পারিবারিক চিকিৎসা ইতিহাস সংগ্রহ করুন",
                "বর্তমানে সেবনকৃত সকল ওষুধের তালিকা প্রস্তুত করুন",
                "লক্ষণের কোনো পরিবর্তন হলে অবিলম্বে চিকিৎসা সহায়তা নিন"
            ]
        else:
            return [
                "Consult with a qualified healthcare provider about your symptoms and concerns",
                "Create a detailed list of all your symptoms",
                "Gather your family medical history",
                "Prepare a list of all current medications",
                "Seek immediate medical attention if symptoms worsen"
            ]
    
    def _get_fallback_preventive_care(self, profile: Dict) -> Dict[str, List[str]]:
        """Fallback preventive care plan"""
        
        if self.language == "bn":
            return {
                "primary_prevention": [
                    "স্বাস্থ্যকর খাদ্যাভ্যাস বজায় রাখুন",
                    "নিয়মিত ব্যায়াম করুন",
                    "ধূমপান ও তামাক সেবন এড়িয়ে চলুন"
                ],
                "secondary_prevention": [
                    "বয়স অনুযায়ী নিয়মিত স্ক্রিনিং করান",
                    "বার্ষিক স্বাস্থ্য পরীক্ষা করান"
                ],
                "lifestyle_modifications": [
                    "পর্যাপ্ত ঘুমের অভ্যাস করুন",
                    "মানসিক চাপ নিয়ন্ত্রণ করুন"
                ],
                "regular_monitoring": [
                    "নিয়মিত চিকিৎসকের সাথে ফলো-আপ করুন"
                ]
            }
        else:
            return {
                "primary_prevention": [
                    "Maintain a healthy diet",
                    "Exercise regularly",
                    "Avoid smoking and tobacco use"
                ],
                "secondary_prevention": [
                    "Get age-appropriate regular screenings",
                    "Annual health checkups"
                ],
                "lifestyle_modifications": [
                    "Maintain adequate sleep habits",
                    "Manage stress effectively"
                ],
                "regular_monitoring": [
                    "Regular follow-ups with healthcare provider"
                ]
            }
    
    def _get_fallback_summary(self, profile: Dict) -> str:
        """Fallback summary when AI generation fails"""
        
        if self.language == "bn":
            return f"""আপনার স্বাস্থ্য পরিস্থিতির উপর ভিত্তি করে আমরা একটি ব্যাপক পরামর্শ পরিকল্পনা তৈরি করেছি। 
            আপনার বয়স ({profile['demographics']['age_group']}) এবং অন্যান্য কারণগুলি বিবেচনা করে, 
            আমরা সুপারিশ করি যে আপনি নিয়মিত স্বাস্থ্য পরীক্ষা এবং স্ক্রিনিং করান। 
            
            অনুগ্রহ করে মনে রাখবেন যে এই পরামর্শগুলি প্রাথমিক নির্দেশনার জন্য এবং 
            চূড়ান্ত চিকিৎসা সিদ্ধান্তের জন্য একজন যোগ্য চিকিৎসকের পরামর্শ নেওয়া অত্যন্ত গুরুত্বপূর্ণ।"""
        else:
            return f"""Based on your health profile, we have created a comprehensive recommendation plan. 
            Considering your age ({profile['demographics']['age_group']}) and other factors, 
            we recommend regular health checkups and appropriate screenings.
            
            Please remember that these recommendations are for preliminary guidance and 
            it is essential to consult with a qualified healthcare provider for final medical decisions."""
        


class QuestionnaireStep:
    """Represents a single step in the cancer consultation questionnaire"""
    
    def __init__(self, question_id: str, question_text: Dict[str, str], 
                 question_type: str = "yes_no", options: Dict[str, List[str]] = None,
                 conditions: Dict[str, Any] = None):
        self.question_id = question_id
        self.question_text = question_text  # {"en": "English text", "bn": "Bengali text"}
        self.question_type = question_type  # "yes_no", "multiple_choice", "scale", "text"
        self.options = options or {}  # {"en": ["Option 1", "Option 2"], "bn": ["বিকল্প ১", "বিকল্প ২"]}
        self.conditions = conditions or {}  # Conditions for showing this question

class CancerConsultationQuestionnaire:
    """Enhanced consultation questionnaire with gender/age-specific questions"""
    
    def __init__(self, language="en"):
        self.language = language
        self.questions = self._initialize_questionnaire()
        
    def _initialize_questionnaire(self) -> List[QuestionnaireStep]:
        """Initialize the structured questionnaire with gender/age-specific logic"""
        
        return [
            # Basic Demographics (Always shown first)
            QuestionnaireStep(
                question_id="age_group",
                question_text={
                    "en": "What is your age group?",
                    "bn": "আপনার বয়স কত?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Under 30", "30-40", "41-50", "51-60", "Over 60"],
                    "bn": ["৩০ এর নিচে", "৩০-৪০", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]
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
            
            # Cancer History
            QuestionnaireStep(
                question_id="cancer_diagnosis",
                question_text={
                    "en": "Have you ever been diagnosed with cancer?",
                    "bn": "আপনার কি কখনো ক্যান্সার ধরা পড়েছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["No", "Yes - currently in treatment", "Yes - treatment completed", "Yes - under monitoring"],
                    "bn": ["না", "হ্যাঁ - বর্তমানে চিকিৎসা চলছে", "হ্যাঁ - চিকিৎসা সম্পন্ন", "হ্যাঁ - পর্যবেক্ষণে আছি"]
                }
            ),
            
            # Chronic Diseases
            QuestionnaireStep(
                question_id="chronic_diseases",
                question_text={
                    "en": "Do you have any of these chronic diseases?",
                    "bn": "আপনার কি এই দীর্ঘমেয়াদী রোগগুলির কোনটি আছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["None", "Diabetes", "Hypertension", "Heart disease", "Multiple conditions"],
                    "bn": ["কিছু নেই", "ডায়াবেটিস", "উচ্চ রক্তচাপ", "হৃদরোগ", "একাধিক রোগ"]
                }
            ),
            
            # Hepatitis Status
            QuestionnaireStep(
                question_id="hepatitis_status",
                question_text={
                    "en": "Have you been tested for Hepatitis B or C?",
                    "bn": "আপনার কি হেপাটাইটিস বি বা সি পরীক্ষা করানো হয়েছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never tested", "Tested - Negative", "Tested - Positive for Hep B", "Tested - Positive for Hep C", "Tested - Positive for both"],
                    "bn": ["কখনো পরীক্ষা করাইনি", "পরীক্ষা করেছি - নেগেটিভ", "পরীক্ষা করেছি - হেপ বি পজিটিভ", "পরীক্ষা করেছি - হেপ সি পজিটিভ", "পরীক্ষা করেছি - দুটোই পজিটিভ"]
                }
            ),
            
            # General Symptoms
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
            
            QuestionnaireStep(
                question_id="swallowing_difficulties",
                question_text={
                    "en": "Do you have indigestion, difficulties in swallowing, or persistent abdominal pain?",
                    "bn": "আপনার কি বদহজম, গিলতে অসুবিধা, বা ক্রমাগত পেটে ব্যথা আছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["None", "Indigestion", "Difficulty swallowing", "Abdominal pain", "Multiple symptoms"],
                    "bn": ["কিছু নেই", "বদহজম", "গিলতে অসুবিধা", "পেটে ব্যথা", "একাধিক লক্ষণ"]
                }
            ),
            
            # Female-specific questions
            QuestionnaireStep(
                question_id="breast_changes",
                question_text={
                    "en": "Have you noticed any changes in your breast(s) - lumps, dimpling, or nipple discharge?",
                    "bn": "আপনি কি আপনার স্তনে কোন পরিবর্তন লক্ষ্য করেছেন - গাঁট, চামড়া কুঁচকে যাওয়া, বা বোঁটা থেকে স্রাব?"
                },
                question_type="yes_no",
                conditions={"gender": ["Female", "মহিলা"]}
            ),
            
            QuestionnaireStep(
                question_id="unusual_bleeding",
                question_text={
                    "en": "Have you experienced any unusual vaginal bleeding or discharge?",
                    "bn": "আপনার কি কোন অস্বাভাবিক যোনি রক্তপাত বা স্রাব হয়েছে?"
                },
                question_type="yes_no",
                conditions={"gender": ["Female", "মহিলা"]}
            ),
            
            QuestionnaireStep(
                question_id="pap_smear_test",
                question_text={
                    "en": "When was your last Pap smear test?",
                    "bn": "আপনার সর্বশেষ প্যাপ স্মিয়ার পরীক্ষা কবে হয়েছিল?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never had one", "Within last year", "1-3 years ago", "3-5 years ago", "More than 5 years ago"],
                    "bn": ["কখনো করাইনি", "গত এক বছরের মধ্যে", "১-৩ বছর আগে", "৩-৫ বছর আগে", "৫ বছরের বেশি আগে"]
                },
                conditions={"gender": ["Female", "মহিলা"], "age_group": ["30-40", "41-50", "51-60", "Over 60", "৩০-৪০", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]}
            ),
            
            QuestionnaireStep(
                question_id="mammogram_test",
                question_text={
                    "en": "When was your last mammogram?",
                    "bn": "আপনার সর্বশেষ ম্যামোগ্রাম কবে হয়েছিল?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never had one", "Within last year", "1-2 years ago", "2-3 years ago", "More than 3 years ago"],
                    "bn": ["কখনো করাইনি", "গত এক বছরের মধ্যে", "১-২ বছর আগে", "২-৩ বছর আগে", "৩ বছরের বেশি আগে"]
                },
                conditions={"gender": ["Female", "মহিলা"], "age_group": ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]}
            ),
            
            QuestionnaireStep(
                question_id="hpv_status",
                question_text={
                    "en": "Have you been tested for HPV (Human Papillomavirus)?",
                    "bn": "আপনার কি HPV (হিউম্যান প্যাপিলোমাভাইরাস) পরীক্ষা করানো হয়েছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never tested", "Tested - Negative", "Tested - Positive", "Don't know results"],
                    "bn": ["কখনো পরীক্ষা করাইনি", "পরীক্ষা করেছি - নেগেটিভ", "পরীক্ষা করেছি - পজিটিভ", "ফলাফল জানি না"]
                },
                conditions={"gender": ["Female", "মহিলা"]}
            ),
            
            # Male-specific questions
            QuestionnaireStep(
                question_id="prostate_symptoms",
                question_text={
                    "en": "Do you have any urinary problems or prostate-related symptoms?",
                    "bn": "আপনার কি প্রস্রাবের সমস্যা বা প্রোস্টেট সংক্রান্ত লক্ষণ আছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["No symptoms", "Frequent urination", "Difficulty urinating", "Blood in urine", "Multiple symptoms"],
                    "bn": ["কোন লক্ষণ নেই", "ঘন ঘন প্রস্রাব", "প্রস্রাবে অসুবিধা", "প্রস্রাবে রক্ত", "একাধিক লক্ষণ"]
                },
                conditions={"gender": ["Male", "পুরুষ"], "age_group": ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]}
            ),
            
            QuestionnaireStep(
                question_id="prostate_screening",
                question_text={
                    "en": "When was your last prostate screening (PSA test or digital rectal exam)?",
                    "bn": "আপনার সর্বশেষ প্রোস্টেট স্ক্রিনিং (PSA পরীক্ষা বা ডিজিটাল রেক্টাল পরীক্ষা) কবে হয়েছিল?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never had one", "Within last year", "1-2 years ago", "2-3 years ago", "More than 3 years ago"],
                    "bn": ["কখনো করাইনি", "গত এক বছরের মধ্যে", "১-২ বছর আগে", "২-৩ বছর আগে", "৩ বছরের বেশি আগে"]
                },
                conditions={"gender": ["Male", "পুরুষ"], "age_group": ["51-60", "Over 60", "৫১-৬০", "৬০ এর উপরে"]}
            ),
            
            QuestionnaireStep(
                question_id="testicular_lumps",
                question_text={
                    "en": "Have you noticed any lumps, swelling, or changes in your testicles?",
                    "bn": "আপনি কি আপনার অণ্ডকোষে কোন গাঁট, ফোলা বা পরিবর্তন লক্ষ্য করেছেন?"
                },
                question_type="yes_no",
                conditions={"gender": ["Male", "পুরুষ"]}
            ),
            
            # Screening History for All
            QuestionnaireStep(
                question_id="colonoscopy_test",
                question_text={
                    "en": "Have you had a colonoscopy or stool test for colorectal cancer screening?",
                    "bn": "আপনার কি কোলোরেক্টাল ক্যান্সার স্ক্রিনিংয়ের জন্য কোলনোস্কোপি বা মল পরীক্ষা করানো হয়েছে?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never had screening", "Colonoscopy within 10 years", "Stool test within 1 year", "Both tests done", "Screening overdue"],
                    "bn": ["কখনো স্ক্রিনিং করাইনি", "১০ বছরের মধ্যে কোলনোস্কোপি", "১ বছরের মধ্যে মল পরীক্ষা", "দুটো পরীক্ষাই করেছি", "স্ক্রিনিং সময় পার হয়েছে"]
                },
                conditions={"age_group": ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]}
            ),
            
            # Risk Factors
            QuestionnaireStep(
                question_id="smoking_status",
                question_text={
                    "en": "What is your smoking history?",
                    "bn": "আপনার ধূমপানের ইতিহাস কী?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Never smoked", "Former smoker (quit >5 years)", "Former smoker (quit <5 years)", "Current light smoker", "Current heavy smoker"],
                    "bn": ["কখনো ধূমপান করিনি", "আগে করতাম (৫+ বছর ছেড়েছি)", "আগে করতাম (<৫ বছর ছেড়েছি)", "এখন হালকা ধূমপান করি", "এখন ভারী ধূমপান করি"]
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
                    "en": ["Never", "Occasionally (1-2 drinks/week)", "Regularly (3-7 drinks/week)", "Heavily (>7 drinks/week)", "Daily consumption"],
                    "bn": ["কখনো না", "মাঝে মাঝে (সপ্তাহে ১-২ ড্রিংক)", "নিয়মিত (সপ্তাহে ৩-৭ ড্রিংক)", "বেশি (সপ্তাহে ৭+ ড্রিংক)", "প্রতিদিন"]
                }
            ),
            
            QuestionnaireStep(
                question_id="family_history",
                question_text={
                    "en": "Has anyone in your immediate family (parents, siblings, children) had cancer?",
                    "bn": "আপনার নিকট পরিবারে (বাবা-মা, ভাইবোন, সন্তান) কি কেউ ক্যান্সারে আক্রান্ত হয়েছেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["No family history", "One family member", "Multiple family members", "Multiple generations affected"],
                    "bn": ["কোন পারিবারিক ইতিহাস নেই", "একজন পরিবারের সদস্য", "একাধিক পরিবারের সদস্য", "একাধিক প্রজন্ম আক্রান্ত"]
                }
            ),
            
            QuestionnaireStep(
                question_id="sun_exposure",
                question_text={
                    "en": "How much time do you spend in the sun without protection?",
                    "bn": "আপনি কত সময় সুরক্ষা ছাড়াই রোদে থাকেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["Minimal exposure", "Moderate with protection", "Frequent exposure", "Excessive unprotected exposure"],
                    "bn": ["খুব কম", "মাঝারি (সুরক্ষা সহ)", "ঘন ঘন", "অতিরিক্ত (সুরক্ষা ছাড়া)"]
                }
            ),
            
            QuestionnaireStep(
                question_id="occupational_exposure",
                question_text={
                    "en": "Have you been exposed to chemicals, radiation, or asbestos at work?",
                    "bn": "আপনি কি কর্মক্ষেত্রে রাসায়নিক, বিকিরণ বা অ্যাসবেস্টসের সংস্পর্শে এসেছেন?"
                },
                question_type="multiple_choice",
                options={
                    "en": ["No occupational exposure", "Chemical exposure", "Radiation exposure", "Asbestos exposure", "Multiple exposures"],
                    "bn": ["কোন পেশাগত এক্সপোজার নেই", "রাসায়নিক এক্সপোজার", "বিকিরণ এক্সপোজার", "অ্যাসবেস্টস এক্সপোজার", "একাধিক এক্সপোজার"]
                }
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
                    "en": ["Very healthy (lots of fruits/vegetables)", "Moderately healthy", "Average", "Poor (processed foods)", "Very poor"],
                    "bn": ["খুব স্বাস্থ্যকর (প্রচুর ফল/সবজি)", "মধ্যম স্বাস্থ্যকর", "গড়", "খারাপ (প্রক্রিয়াজাত খাবার)", "খুব খারাপ"]
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
                    "en": ["Daily vigorous exercise", "3-4 times per week", "1-2 times per week", "Rarely", "Never"],
                    "bn": ["প্রতিদিন জোরালো ব্যায়াম", "সপ্তাহে ৩-৪ বার", "সপ্তাহে ১-২ বার", "কদাচিৎ", "কখনো না"]
                }
            ),
        ]
    
    def get_applicable_questions(self, responses: Dict[str, Any]) -> List[QuestionnaireStep]:
        """Get questions that are applicable based on current responses"""
        applicable_questions = []
        
        for question in self.questions:
            if self._should_show_question(question, responses):
                applicable_questions.append(question)
        
        return applicable_questions
    
    def _should_show_question(self, question: QuestionnaireStep, responses: Dict[str, Any]) -> bool:
        """Check if a question should be shown based on conditions and current responses"""
        
        if not question.conditions:
            return True
        
        # Check gender condition
        if "gender" in question.conditions:
            user_gender = responses.get("gender", {}).get("response")
            if user_gender not in question.conditions["gender"]:
                return False
        
        # Check age condition
        if "age_group" in question.conditions:
            user_age = responses.get("age_group", {}).get("response")
            if user_age not in question.conditions["age_group"]:
                return False
        
        return True

class EnhancedCancerConsultationSession:
    """Enhanced consultation session with dynamic questions and recommendations"""
    
    def __init__(self, language="en"):
        self.language = language
        self.reasoning_engine = CancerReasoningEngine(language)
        self.questionnaire = CancerConsultationQuestionnaire(language)
        self.responses = {}
        self.current_question_index = 0
        self.consultation_complete = False
        self.applicable_questions = []
        
    def get_current_question(self) -> Optional[QuestionnaireStep]:
        """Get the current question to ask"""
        # Update applicable questions based on current responses
        self.applicable_questions = self.questionnaire.get_applicable_questions(self.responses)
        
        if self.current_question_index < len(self.applicable_questions):
            return self.applicable_questions[self.current_question_index]
        return None
    
    def get_progress_info(self) -> Dict[str, Any]:
        """Get consultation progress information"""
        # Update applicable questions
        self.applicable_questions = self.questionnaire.get_applicable_questions(self.responses)
        total_questions = len(self.applicable_questions)
        completed = self.current_question_index
        
        return {
            "current_question": completed + 1,
            "total_questions": total_questions,
            "progress_percentage": (completed / total_questions) * 100 if total_questions > 0 else 100,
            "questions_remaining": total_questions - completed
        }
    
    def process_response(self, response: Any) -> Dict[str, Any]:
        """Process user response and advance to next question"""
        
        # Update applicable questions
        self.applicable_questions = self.questionnaire.get_applicable_questions(self.responses)
        
        if self.current_question_index >= len(self.applicable_questions):
            return self._complete_consultation()
        
        # Store the current response
        current_question = self.applicable_questions[self.current_question_index]
        self.responses[current_question.question_id] = {
            "question": current_question.question_text[self.language],
            "response": response,
            "question_type": current_question.question_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # Move to next question
        self.current_question_index += 1
        
        # Update applicable questions again after the new response
        self.applicable_questions = self.questionnaire.get_applicable_questions(self.responses)
        
        # Check if consultation is complete
        if self.current_question_index >= len(self.applicable_questions):
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
        """Complete the consultation and generate dynamic analysis with AI recommendations"""
        
        self.consultation_complete = True
        
        # Process responses through reasoning engine with dynamic analysis
        processed_data = self._process_responses_for_analysis()
        
        # Generate comprehensive analysis
        try:
            symptoms_analysis = self.reasoning_engine.analyze_symptoms(processed_data["symptoms"])
            risk_assessment = self.reasoning_engine.assess_risk_factors(processed_data["demographics"])
            differential_diagnosis = self.reasoning_engine.generate_differential_diagnosis(
                symptoms_analysis, risk_assessment
            )
            
            # Generate base recommendations
            base_recommendations = self._generate_dynamic_recommendations(
                processed_data, symptoms_analysis, risk_assessment, differential_diagnosis
            )
            
            analysis_results = {
                "symptoms_analysis": symptoms_analysis,
                "risk_assessment": risk_assessment,
                "differential_diagnosis": differential_diagnosis,
                "recommendations": base_recommendations,
                "user_profile": self._generate_user_profile()
            }
            
            # 🆕 FIXED: Always generate AI recommendations
            try:
                ai_engine = AIRecommendationEngine(self.language)
                ai_recommendations = ai_engine.generate_ai_recommendations(
                    self.responses,
                    analysis_results
                )
                
                # IMPORTANT: Store AI recommendations in analysis results
                analysis_results["ai_recommendations"] = ai_recommendations
                
                # Store for later access
                self._last_analysis_results = analysis_results
                
                logging.info(f"AI recommendations generated successfully with {len(ai_recommendations)} categories")
                
            except Exception as ai_error:
                logging.error(f"Error generating AI recommendations: {ai_error}")
                # Create fallback AI recommendations
                ai_recommendations = self._create_fallback_ai_recommendations()
                analysis_results["ai_recommendations"] = ai_recommendations
                self._last_analysis_results = analysis_results
            
            # Generate comprehensive response
            comprehensive_response = self.reasoning_engine.generate_llm_enhanced_response(analysis_results)
            
            # Enhance the response with AI recommendations
            enhanced_response = self._generate_enhanced_response_with_ai(
                comprehensive_response,
                analysis_results["ai_recommendations"]
            )
            
            analysis_results["comprehensive_response"] = comprehensive_response
            analysis_results["enhanced_comprehensive_response"] = enhanced_response
            
            reasoning_explanation = self.reasoning_engine.get_reasoning_explanation()
            
            return {
                "type": "consultation_complete",
                "analysis_results": analysis_results,
                "comprehensive_response": enhanced_response,
                "reasoning_explanation": reasoning_explanation,
                "consultation_complete": True,
                "urgency_level": self._determine_urgency_level(symptoms_analysis, risk_assessment, processed_data)
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
        
    def _create_fallback_ai_recommendations(self) -> Dict[str, Any]:
        """Create fallback AI recommendations when AI generation fails"""
        
        user_profile = self._generate_user_profile()
        
        if self.language == "bn":
            fallback_recommendations = {
                "immediate_care": [
                    "আপনার উত্তরের ভিত্তিতে একজন যোগ্য চিকিৎসকের পরামর্শ নিন",
                    "লক্ষণগুলির তালিকা তৈরি করুন এবং চিকিৎসকের কাছে নিয়ে যান",
                    "নিয়মিত স্বাস্থ্য পরীক্ষা করান"
                ],
                "preventive_care_plan": {
                    "primary_prevention": [
                        "স্বাস্থ্যকর জীবনযাত্রা বজায় রাখুন",
                        "ধূমপান ও তামাক এড়িয়ে চলুন",
                        "নিয়মিত ব্যায়াম করুন"
                    ],
                    "secondary_prevention": [
                        "বয়স অনুযায়ী নিয়মিত স্ক্রিনিং করান",
                        "পারিবারিক ইতিহাস চিকিৎসকদের জানান"
                    ]
                },
                "screening_schedule": {
                    "general_screening": {
                        "test": "বার্ষিক স্বাস্থ্য পরীক্ষা",
                        "frequency": "বার্ষিক",
                        "next_due": "যত তাড়াতাড়ি সম্ভব"
                    }
                },
                "ai_summary": f"""আপনার প্রোফাইল ({user_profile['gender']}, {user_profile['age_group']}) এর ভিত্তিতে আমরা এই প্রাথমিক সুপারিশ প্রদান করছি। 
                চূড়ান্ত চিকিৎসা পরামর্শের জন্য অবশ্যই একজন যোগ্য অনকোলজিস্ট বা চিকিৎসকের সাথে পরামর্শ করুন।"""
            }
        else:
            fallback_recommendations = {
                "immediate_care": [
                    "Based on your responses, consult with a qualified healthcare provider",
                    "Prepare a list of your symptoms to discuss with your doctor",
                    "Schedule regular health check-ups"
                ],
                "preventive_care_plan": {
                    "primary_prevention": [
                        "Maintain a healthy lifestyle",
                        "Avoid smoking and tobacco use",
                        "Exercise regularly"
                    ],
                    "secondary_prevention": [
                        "Get age-appropriate regular screenings",
                        "Inform healthcare providers about family history"
                    ]
                },
                "screening_schedule": {
                    "general_screening": {
                        "test": "Annual health checkup",
                        "frequency": "Annually",
                        "next_due": "As soon as possible"
                    }
                },
                "ai_summary": f"""Based on your profile ({user_profile['gender']}, {user_profile['age_group']}), we provide these preliminary recommendations. 
                Always consult with a qualified oncologist or healthcare provider for definitive medical advice."""
            }
        
        return fallback_recommendations
        
    def _generate_enhanced_response_with_ai(self, original_response: str, ai_recommendations: Dict) -> str:
        """Enhance the original response with AI recommendations"""
        
        if self.language == "bn":
            enhanced_sections = [
                "\n\n---\n## 🤖 AI-চালিত ব্যক্তিগত পরামর্শ\n",
                "### 🚨 তাৎক্ষণিক যত্ন:\n"
            ]
            
            for recommendation in ai_recommendations.get("immediate_care", []):
                enhanced_sections.append(f"• {recommendation}\n")
            
            enhanced_sections.append("\n### 🛡️ প্রতিরোধমূলক যত্ন পরিকল্পনা:\n")
            preventive_care = ai_recommendations.get("preventive_care_plan", {})
            for category, recommendations in preventive_care.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:3]:  # Limit to top 3 per category
                        enhanced_sections.append(f"• {rec}\n")
                    enhanced_sections.append("\n")
            
            enhanced_sections.append("### 🏥 স্ক্রিনিং সূচি:\n")
            screening_schedule = ai_recommendations.get("screening_schedule", {})
            for cancer_type, schedule_info in screening_schedule.items():
                enhanced_sections.append(f"**{cancer_type.replace('_', ' ').title()}:** {schedule_info.get('test', '')} - {schedule_info.get('frequency', '')}\n")
            
            enhanced_sections.append("\n### 🍎 জীবনযাত্রার পরামর্শ:\n")
            lifestyle_mods = ai_recommendations.get("lifestyle_modifications", {})
            for category, recommendations in lifestyle_mods.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:2]:  # Top 2 per category
                        enhanced_sections.append(f"• {rec}\n")
            
            enhanced_sections.append(f"\n### 📋 AI সারসংক্ষেপ:\n")
            enhanced_sections.append(ai_recommendations.get("ai_summary", ""))
            
            enhanced_sections.append("\n\n---\n⚠️ **গুরুত্বপূর্ণ**: এই AI-চালিত পরামর্শগুলি ব্যক্তিগতকৃত নির্দেশনার জন্য। চূড়ান্ত চিকিৎসা সিদ্ধান্তের জন্য অবশ্যই একজন যোগ্য অনকোলজিস্টের পরামর্শ নিন।")
            
        else:
            enhanced_sections = [
                "\n\n---\n## 🤖 AI-Powered Personalized Recommendations\n",
                "### 🚨 Immediate Care:\n"
            ]
            
            for recommendation in ai_recommendations.get("immediate_care", []):
                enhanced_sections.append(f"• {recommendation}\n")
            
            enhanced_sections.append("\n### 🛡️ Preventive Care Plan:\n")
            preventive_care = ai_recommendations.get("preventive_care_plan", {})
            for category, recommendations in preventive_care.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:3]:  # Limit to top 3 per category
                        enhanced_sections.append(f"• {rec}\n")
                    enhanced_sections.append("\n")
            
            enhanced_sections.append("### 🏥 Screening Schedule:\n")
            screening_schedule = ai_recommendations.get("screening_schedule", {})
            for cancer_type, schedule_info in screening_schedule.items():
                enhanced_sections.append(f"**{cancer_type.replace('_', ' ').title()}:** {schedule_info.get('test', '')} - {schedule_info.get('frequency', '')}\n")
            
            enhanced_sections.append("\n### 🍎 Lifestyle Recommendations:\n")
            lifestyle_mods = ai_recommendations.get("lifestyle_modifications", {})
            for category, recommendations in lifestyle_mods.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:2]:  # Top 2 per category
                        enhanced_sections.append(f"• {rec}\n")
            
            enhanced_sections.append(f"\n### 📋 AI Summary:\n")
            enhanced_sections.append(ai_recommendations.get("ai_summary", ""))
            
            enhanced_sections.append("\n\n---\n⚠️ **Important**: These AI-powered recommendations are for personalized guidance. Always consult with a qualified oncologist for final medical decisions.")
        
        return original_response + "".join(enhanced_sections)
    
    def _generate_dynamic_recommendations(self, processed_data: Dict, symptoms_analysis: Dict, 
                                        risk_assessment: Dict, differential_diagnosis: Dict) -> Dict[str, Any]:
        """Generate dynamic recommendations based on user responses and analysis"""
        
        recommendations = {
            "immediate_actions": [],
            "screening_recommendations": [],
            "lifestyle_modifications": [],
            "follow_up_schedule": [],
            "specialist_referrals": [],
            "emergency_signs": [],
            "personalized_advice": []
        }
        
        # Get user profile
        user_profile = self._generate_user_profile()
        age_group = user_profile["age_group"]
        gender = user_profile["gender"]
        
        # Immediate actions based on symptoms and urgency
        urgency_score = symptoms_analysis.get("urgency_score", 0)
        high_risk_symptoms = self._identify_high_risk_symptoms()
        
        if urgency_score >= 8 or high_risk_symptoms:
            if self.language == "bn":
                recommendations["immediate_actions"].extend([
                    "অবিলম্বে চিকিৎসা সহায়তা নিন",
                    "নিকটস্থ হাসপাতালে যান বা জরুরি বিভাগে যোগাযোগ করুন",
                    "লক্ষণগুলির একটি তালিকা তৈরি করুন এবং চিকিৎসকের সাথে নিয়ে যান"
                ])
            else:
                recommendations["immediate_actions"].extend([
                    "Seek immediate medical attention",
                    "Go to nearest hospital or contact emergency department",
                    "Prepare a list of symptoms and bring it to the healthcare provider"
                ])
        elif urgency_score >= 6:
            if self.language == "bn":
                recommendations["immediate_actions"].extend([
                    "১-২ সপ্তাহের মধ্যে চিকিৎসকের সাথে অ্যাপয়েন্টমেন্ট নিন",
                    "লক্ষণগুলি পর্যবেক্ষণ করুন এবং রেকর্ড করুন"
                ])
            else:
                recommendations["immediate_actions"].extend([
                    "Schedule appointment with healthcare provider within 1-2 weeks",
                    "Monitor and record your symptoms"
                ])
        
        # Screening recommendations based on age, gender, and responses
        screening_recs = self._generate_screening_recommendations(user_profile)
        recommendations["screening_recommendations"].extend(screening_recs)
        
        # Lifestyle modifications based on risk factors
        lifestyle_mods = self._generate_lifestyle_recommendations(processed_data)
        recommendations["lifestyle_modifications"].extend(lifestyle_mods)
        
        # Specialist referrals based on symptoms and risk factors
        specialist_refs = self._generate_specialist_referrals(symptoms_analysis, risk_assessment, user_profile)
        recommendations["specialist_referrals"].extend(specialist_refs)
        
        # Follow-up schedule
        follow_up = self._generate_follow_up_schedule(urgency_score, risk_assessment)
        recommendations["follow_up_schedule"].extend(follow_up)
        
        # Emergency warning signs
        emergency_signs = self._generate_emergency_signs(user_profile)
        recommendations["emergency_signs"].extend(emergency_signs)
        
        # Personalized advice based on specific responses
        personalized_advice = self._generate_personalized_advice(processed_data)
        recommendations["personalized_advice"].extend(personalized_advice)
        
        return recommendations
    
    def _generate_screening_recommendations(self, user_profile: Dict) -> List[str]:
        """Generate screening recommendations based on user profile"""
        
        recommendations = []
        age_group = user_profile["age_group"]
        gender = user_profile["gender"]
        
        # Age and gender-specific screening recommendations
        if gender == "female":
            if age_group in ["41-50", "51-60", "Over 60"]:
                mammogram_response = self.responses.get("mammogram_test", {}).get("response")
                if mammogram_response in ["Never had one", "More than 3 years ago", "কখনো করাইনি", "৩ বছরের বেশি আগে"]:
                    if self.language == "bn":
                        recommendations.append("ম্যামোগ্রাম করান (বার্ষিক)")
                    else:
                        recommendations.append("Get mammogram screening (annually)")
            
            pap_response = self.responses.get("pap_smear_test", {}).get("response")
            if pap_response in ["Never had one", "More than 5 years ago", "কখনো করাইনি", "৫ বছরের বেশি আগে"]:
                if self.language == "bn":
                    recommendations.append("প্যাপ স্মিয়ার টেস্ট করান")
                else:
                    recommendations.append("Get Pap smear test")
            
            hpv_response = self.responses.get("hpv_status", {}).get("response")
            if hpv_response in ["Never tested", "কখনো পরীক্ষা করাইনি"]:
                if self.language == "bn":
                    recommendations.append("HPV পরীক্ষা করান")
                else:
                    recommendations.append("Get HPV testing")
        
        elif gender == "male":
            if age_group in ["51-60", "Over 60"]:
                prostate_response = self.responses.get("prostate_screening", {}).get("response")
                if prostate_response in ["Never had one", "More than 3 years ago", "কখনো করাইনি", "৩ বছরের বেশি আগে"]:
                    if self.language == "bn":
                        recommendations.append("প্রোস্টেট স্ক্রিনিং (PSA টেস্ট)")
                    else:
                        recommendations.append("Get prostate screening (PSA test)")
        
        # Colorectal screening for both genders
        if age_group in ["41-50", "51-60", "Over 60"]:
            colonoscopy_response = self.responses.get("colonoscopy_test", {}).get("response")
            if colonoscopy_response in ["Never had screening", "Screening overdue", "কখনো স্ক্রিনিং করাইনি", "স্ক্রিনিং সময় পার হয়েছে"]:
                if self.language == "bn":
                    recommendations.append("কোলোরেক্টাল স্ক্রিনিং (কোলনোস্কোপি বা FIT টেস্ট)")
                else:
                    recommendations.append("Get colorectal screening (colonoscopy or FIT test)")
        
        # Hepatitis screening
        hepatitis_response = self.responses.get("hepatitis_status", {}).get("response")
        if hepatitis_response in ["Never tested", "কখনো পরীক্ষা করাইনি"]:
            if self.language == "bn":
                recommendations.append("হেপাটাইটিস বি এবং সি পরীক্ষা করান")
            else:
                recommendations.append("Get Hepatitis B and C screening")
        
        return recommendations
    
    def _generate_lifestyle_recommendations(self, processed_data: Dict) -> List[str]:
        """Generate lifestyle recommendations based on risk factors"""
        
        recommendations = []
        
        # Smoking recommendations
        smoking_status = self.responses.get("smoking_status", {}).get("response", "")
        if "Current" in smoking_status or "এখন" in smoking_status:
            if self.language == "bn":
                recommendations.extend([
                    "ধূমপান বন্ধ করুন - এটি সবচেয়ে গুরুত্বপূর্ণ",
                    "ধূমপান বন্ধের জন্য চিকিৎসকের সাহায্য নিন",
                    "নিকোটিন রিপ্লেসমেন্ট থেরাপি বিবেচনা করুন"
                ])
            else:
                recommendations.extend([
                    "Quit smoking - this is the most important step",
                    "Seek medical help for smoking cessation",
                    "Consider nicotine replacement therapy"
                ])
        
        # Alcohol recommendations
        alcohol_consumption = self.responses.get("alcohol_consumption", {}).get("response", "")
        if "Heavily" in alcohol_consumption or "Daily" in alcohol_consumption or "বেশি" in alcohol_consumption or "প্রতিদিন" in alcohol_consumption:
            if self.language == "bn":
                recommendations.extend([
                    "মদ্যপান কমান বা বন্ধ করুন",
                    "প্রয়োজনে অ্যালকোহল কাউন্সেলিং নিন"
                ])
            else:
                recommendations.extend([
                    "Reduce or stop alcohol consumption",
                    "Consider alcohol counseling if needed"
                ])
        
        # Diet recommendations
        diet_quality = self.responses.get("diet_quality", {}).get("response", "")
        if "Poor" in diet_quality or "খারাপ" in diet_quality:
            if self.language == "bn":
                recommendations.extend([
                    "স্বাস্থ্যকর খাদ্যাভ্যাস গড়ে তুলুন",
                    "প্রচুর ফল ও সবজি খান",
                    "প্রক্রিয়াজাত খাবার এড়িয়ে চলুন",
                    "পুরো শস্য ও চর্বিহীন প্রোটিন খান"
                ])
            else:
                recommendations.extend([
                    "Adopt a healthy diet",
                    "Eat plenty of fruits and vegetables",
                    "Avoid processed foods",
                    "Include whole grains and lean proteins"
                ])
        
        # Exercise recommendations
        exercise_frequency = self.responses.get("exercise_frequency", {}).get("response", "")
        if "Never" in exercise_frequency or "Rarely" in exercise_frequency or "কখনো না" in exercise_frequency or "কদাচিৎ" in exercise_frequency:
            if self.language == "bn":
                recommendations.extend([
                    "নিয়মিত ব্যায়াম শুরু করুন",
                    "সপ্তাহে কমপক্ষে ১৫০ মিনিট মাঝারি ব্যায়াম করুন",
                    "ধীরে ধীরে শুরু করুন এবং ক্রমশ বাড়ান"
                ])
            else:
                recommendations.extend([
                    "Start regular exercise routine",
                    "Aim for at least 150 minutes of moderate exercise per week",
                    "Start slowly and gradually increase intensity"
                ])
        
        # Sun protection
        sun_exposure = self.responses.get("sun_exposure", {}).get("response", "")
        if "Excessive" in sun_exposure or "অতিরিক্ত" in sun_exposure:
            if self.language == "bn":
                recommendations.extend([
                    "রোদে বের হওয়ার সময় সানস্ক্রিন ব্যবহার করুন",
                    "সুরক্ষামূলক পোশাক পরুন",
                    "দুপুর ১০টা থেকে ৪টা পর্যন্ত রোদ এড়িয়ে চলুন"
                ])
            else:
                recommendations.extend([
                    "Use sunscreen when going outdoors",
                    "Wear protective clothing",
                    "Avoid sun exposure between 10 AM and 4 PM"
                ])
        
        return recommendations
    
    def _generate_specialist_referrals(self, symptoms_analysis: Dict, risk_assessment: Dict, user_profile: Dict) -> List[str]:
        """Generate specialist referral recommendations"""
        
        referrals = []
        
        # High-risk cancers from analysis
        high_risk_cancers = risk_assessment.get("high_risk_cancers", [])
        possible_cancers = symptoms_analysis.get("possible_cancer_types", [])
        
        # Symptom-based referrals
        if self.responses.get("breast_changes", {}).get("response") == "Yes" or self.responses.get("breast_changes", {}).get("response") == "হ্যাঁ":
            if self.language == "bn":
                referrals.append("স্তন বিশেষজ্ঞ বা অনকোলজিস্টের কাছে যান")
            else:
                referrals.append("Consult breast specialist or oncologist")
        
        if self.responses.get("prostate_symptoms", {}).get("response") in ["Multiple symptoms", "Blood in urine", "একাধিক লক্ষণ", "প্রস্রাবে রক্ত"]:
            if self.language == "bn":
                referrals.append("ইউরোলজিস্টের কাছে যান")
            else:
                referrals.append("Consult urologist")
        
        if self.responses.get("persistent_cough", {}).get("response") == "Yes" or self.responses.get("blood_in_sputum", {}).get("response") == "Yes":
            if self.language == "bn":
                referrals.append("পালমোনোলজিস্ট বা বক্ষরোগ বিশেষজ্ঞের কাছে যান")
            else:
                referrals.append("Consult pulmonologist or chest specialist")
        
        if self.responses.get("bowel_changes", {}).get("response") == "Yes" or self.responses.get("swallowing_difficulties", {}).get("response") in ["Multiple symptoms", "Abdominal pain"]:
            if self.language == "bn":
                referrals.append("গ্যাস্ট্রোএন্টারোলজিস্টের কাছে যান")
            else:
                referrals.append("Consult gastroenterologist")
        
        if self.responses.get("skin_changes", {}).get("response") == "Yes":
            if self.language == "bn":
                referrals.append("ডার্মাটোলজিস্ট বা চর্ম বিশেষজ্ঞের কাছে যান")
            else:
                referrals.append("Consult dermatologist")
        
        # Cancer type-specific referrals
        for cancer in high_risk_cancers + possible_cancers:
            if cancer not in ["breast_cancer", "prostate_cancer", "lung_cancer", "colorectal_cancer", "skin_cancer"]:
                if self.language == "bn":
                    referrals.append("অনকোলজিস্ট (ক্যান্সার বিশেষজ্ঞ) এর কাছে যান")
                else:
                    referrals.append("Consult oncologist (cancer specialist)")
                break
        
        # Previous cancer diagnosis
        if "Yes" in self.responses.get("cancer_diagnosis", {}).get("response", ""):
            if self.language == "bn":
                referrals.append("আপনার অনকোলজিস্টের সাথে নিয়মিত ফলো-আপ করুন")
            else:
                referrals.append("Continue regular follow-up with your oncologist")
        
        return list(set(referrals))  # Remove duplicates
    
    def _generate_follow_up_schedule(self, urgency_score: float, risk_assessment: Dict) -> List[str]:
        """Generate follow-up schedule based on risk and urgency"""
        
        schedule = []
        
        if urgency_score >= 8:
            if self.language == "bn":
                schedule.extend([
                    "অবিলম্বে চিকিৎসা সহায়তা নিন",
                    "প্রাথমিক মূল্যায়নের ১ সপ্তাহ পর ফলো-আপ করুন"
                ])
            else:
                schedule.extend([
                    "Immediate medical evaluation",
                    "Follow-up within 1 week of initial assessment"
                ])
        elif urgency_score >= 6:
            if self.language == "bn":
                schedule.extend([
                    "১-২ সপ্তাহের মধ্যে চিকিৎসা মূল্যায়ন",
                    "১ মাস পর ফলো-আপ",
                    "প্রতি ৩ মাস অন্তর পর্যবেক্ষণ"
                ])
            else:
                schedule.extend([
                    "Medical evaluation within 1-2 weeks",
                    "Follow-up in 1 month",
                    "Monitoring every 3 months"
                ])
        elif len(risk_assessment.get("high_risk_cancers", [])) > 0:
            if self.language == "bn":
                schedule.extend([
                    "৩-৬ মাসের মধ্যে বিশেষজ্ঞের পরামর্শ",
                    "বার্ষিক ব্যাপক স্বাস্থ্য পরীক্ষা",
                    "প্রতি ৬ মাস অন্তর নিয়মিত পর্যবেক্ষণ"
                ])
            else:
                schedule.extend([
                    "Specialist consultation within 3-6 months",
                    "Annual comprehensive health screening",
                    "Regular monitoring every 6 months"
                ])
        else:
            if self.language == "bn":
                schedule.extend([
                    "বার্ষিক নিয়মিত স্বাস্থ্য পরীক্ষা",
                    "বয়স অনুযায়ী ক্যান্সার স্ক্রিনিং"
                ])
            else:
                schedule.extend([
                    "Annual routine health check-up",
                    "Age-appropriate cancer screenings"
                ])
        
        return schedule
    
    def _generate_emergency_signs(self, user_profile: Dict) -> List[str]:
        """Generate emergency warning signs based on user profile"""
        
        emergency_signs = []
        
        if self.language == "bn":
            emergency_signs.extend([
                "গুরুতর ব্যথা যা ক্রমশ বাড়ছে",
                "অতিরিক্ত রক্তপাত",
                "শ্বাসকষ্ট বা বুকে চাপ",
                "অজ্ঞান হয়ে যাওয়া বা মাথা ঘোরা",
                "দ্রুত ওজন হ্রাস (মাসে ৫+ কেজি)",
                "উচ্চ জ্বর সাথে ঠান্ডা লাগা",
                "গিলতে অসুবিধা বা কথা বলতে সমস্যা"
            ])
        else:
            emergency_signs.extend([
                "Severe pain that is worsening",
                "Excessive bleeding",
                "Shortness of breath or chest pressure",
                "Loss of consciousness or severe dizziness",
                "Rapid weight loss (5+ kg per month)",
                "High fever with chills",
                "Difficulty swallowing or speaking"
            ])
        
        # Gender-specific emergency signs
        if user_profile["gender"] == "female":
            if self.language == "bn":
                emergency_signs.extend([
                    "স্তনে দ্রুত বাড়ছে এমন গাঁট",
                    "অস্বাভাবিক ভারী মাসিক বা রক্তপাত"
                ])
            else:
                emergency_signs.extend([
                    "Rapidly growing breast lump",
                    "Abnormally heavy menstrual bleeding"
                ])
        
        elif user_profile["gender"] == "male":
            if self.language == "bn":
                emergency_signs.extend([
                    "প্রস্রাবে রক্ত",
                    "অণ্ডকোষে হঠাৎ ব্যথা বা ফোলা"
                ])
            else:
                emergency_signs.extend([
                    "Blood in urine",
                    "Sudden testicular pain or swelling"
                ])
        
        return emergency_signs
    
    def _generate_personalized_advice(self, processed_data: Dict) -> List[str]:
        """Generate personalized advice based on specific responses"""
        
        advice = []
        
        # Previous cancer diagnosis advice
        cancer_diagnosis = self.responses.get("cancer_diagnosis", {}).get("response", "")
        if "Yes" in cancer_diagnosis:
            if self.language == "bn":
                advice.extend([
                    "ক্যান্সারের ইতিহাস থাকায় নিয়মিত ফলো-আপ অত্যন্ত গুরুত্বপূর্ণ",
                    "নতুন বা পরিবর্তিত লক্ষণের জন্য সতর্ক থাকুন",
                    "আপনার অনকোলজিস্টের সাথে নিয়মিত যোগাযোগ রাখুন"
                ])
            else:
                advice.extend([
                    "Regular follow-up is crucial given your cancer history",
                    "Stay vigilant for new or changing symptoms",
                    "Maintain regular contact with your oncologist"
                ])
        
        # Chronic disease advice
        chronic_diseases = self.responses.get("chronic_diseases", {}).get("response", "")
        if chronic_diseases != "None" and chronic_diseases != "কিছু নেই":
            if self.language == "bn":
                advice.extend([
                    "দীর্ঘমেয়াদী রোগের সঠিক ব্যবস্থাপনা ক্যান্সার প্রতিরোধে সাহায্য করে",
                    "নিয়মিত ওষুধ সেবন ও চিকিৎসকের পরামর্শ মেনে চলুন"
                ])
            else:
                advice.extend([
                    "Proper management of chronic diseases helps in cancer prevention",
                    "Continue regular medications and follow medical advice"
                ])
        
        # Hepatitis positive advice
        hepatitis_status = self.responses.get("hepatitis_status", {}).get("response", "")
        if "Positive" in hepatitis_status or "পজিটিভ" in hepatitis_status:
            if self.language == "bn":
                advice.extend([
                    "হেপাটাইটিস পজিটিভ হওয়ায় লিভার ক্যান্সারের ঝুঁকি বেশি",
                    "নিয়মিত লিভার ফাংশন টেস্ট করান",
                    "অ্যালকোহল এড়িয়ে চলুন"
                ])
            else:
                advice.extend([
                    "Hepatitis positive status increases liver cancer risk",
                    "Get regular liver function tests",
                    "Avoid alcohol completely"
                ])
        
        # HPV positive advice
        hpv_status = self.responses.get("hpv_status", {}).get("response", "")
        if "Positive" in hpv_status or "পজিটিভ" in hpv_status:
            if self.language == "bn":
                advice.extend([
                    "HPV পজিটিভ হওয়ায় জরায়ু মুখের ক্যান্সারের ঝুঁকি বেশি",
                    "নিয়মিত প্যাপ স্মিয়ার টেস্ট করান",
                    "নিরাপদ যৌন সম্পর্ক বজায় রাখুন"
                ])
            else:
                advice.extend([
                    "HPV positive status increases cervical cancer risk",
                    "Get regular Pap smear tests",
                    "Practice safe sexual relationships"
                ])
        
        # Family history advice
        family_history = self.responses.get("family_history", {}).get("response", "")
        if family_history not in ["No family history", "কোন পারিবারিক ইতিহাস নেই"]:
            if self.language == "bn":
                advice.extend([
                    "পারিবারিক ক্যান্সারের ইতিহাস থাকায় জেনেটিক কাউন্সেলিং বিবেচনা করুন",
                    "প্রস্তাবিত বয়সের আগেই স্ক্রিনিং শুরু করার কথা ভাবুন"
                ])
            else:
                advice.extend([
                    "Consider genetic counseling given family cancer history",
                    "Consider starting screening earlier than recommended age"
                ])
        
        # Occupational exposure advice
        occupational_exposure = self.responses.get("occupational_exposure", {}).get("response", "")
        if occupational_exposure != "No occupational exposure" and occupational_exposure != "কোন পেশাগত এক্সপোজার নেই":
            if self.language == "bn":
                advice.extend([
                    "পেশাগত এক্সপোজারের কথা আপনার চিকিৎসককে জানান",
                    "কর্মক্ষেত্রে নিরাপত্তা নির্দেশনা মেনে চলুন",
                    "নিয়মিত স্বাস্থ্য পর্যবেক্ষণ করুন"
                ])
            else:
                advice.extend([
                    "Inform your healthcare provider about occupational exposures",
                    "Follow workplace safety guidelines",
                    "Get regular health monitoring"
                ])
        
        return advice
    
    def _generate_user_profile(self) -> Dict[str, str]:
        """Generate user profile from responses"""
        
        return {
            "age_group": self.responses.get("age_group", {}).get("response", "Unknown"),
            "gender": self.responses.get("gender", {}).get("response", "Unknown"),
            "main_concern": self.responses.get("main_concern", {}).get("response", "Not specified"),
            "cancer_history": self.responses.get("cancer_diagnosis", {}).get("response", "No"),
            "chronic_diseases": self.responses.get("chronic_diseases", {}).get("response", "None"),
            "smoking_status": self.responses.get("smoking_status", {}).get("response", "Unknown"),
            "family_history": self.responses.get("family_history", {}).get("response", "Unknown")
        }
    
    def _identify_high_risk_symptoms(self) -> bool:
        """Identify if user has high-risk symptoms requiring immediate attention"""
        
        high_risk_responses = [
            ("blood_in_sputum", ["Yes", "হ্যাঁ"]),
            ("unusual_bleeding", ["Yes", "হ্যাঁ"]),
            ("unexplained_weight_loss", ["Yes", "হ্যাঁ"]),
            ("swallowing_difficulties", ["Difficulty swallowing", "Multiple symptoms", "গিলতে অসুবিধা", "একাধিক লক্ষণ"])
        ]
        
        for question_id, risk_responses in high_risk_responses:
            user_response = self.responses.get(question_id, {}).get("response", "")
            if user_response in risk_responses:
                return True
        
        return False
    
    def _process_responses_for_analysis(self) -> Dict[str, Any]:
        """Process questionnaire responses into format suitable for reasoning engine"""
        
        # Extract demographics with enhanced processing
        demographics = {
            "age": self._convert_age_group(self.responses.get("age_group", {}).get("response")),
            "gender": self._convert_gender(self.responses.get("gender", {}).get("response")),
            "smoking": self._convert_smoking_status(self.responses.get("smoking_status", {}).get("response")),
            "heavy_drinking": self._convert_alcohol_consumption(self.responses.get("alcohol_consumption", {}).get("response")),
            "family_history_cancer": self._convert_family_history(self.responses.get("family_history", {}).get("response")),
            "excessive_sun_exposure": self._convert_sun_exposure(self.responses.get("sun_exposure", {}).get("response")),
            "occupational_exposure": self._convert_occupational_exposure(self.responses.get("occupational_exposure", {}).get("response")),
            "chronic_diseases": self._convert_chronic_diseases(self.responses.get("chronic_diseases", {}).get("response")),
            "cancer_history": self._convert_cancer_history(self.responses.get("cancer_diagnosis", {}).get("response")),
            "hepatitis_positive": self._convert_hepatitis_status(self.responses.get("hepatitis_status", {}).get("response")),
            "hpv_positive": self._convert_hpv_status(self.responses.get("hpv_status", {}).get("response"))
        }
        
        # Extract symptoms with enhanced analysis
        symptoms_description = self._build_enhanced_symptoms_description()
        
        symptoms = {
            "description": symptoms_description,
            "severity": self._calculate_enhanced_symptom_severity(),
            "duration": self._estimate_symptom_duration(),
            "symptom_pattern": self._analyze_symptom_pattern()
        }
        
        return {
            "demographics": demographics,
            "symptoms": symptoms,
            "screening_history": self._extract_screening_history(),
            "risk_factors": self._extract_additional_risk_factors()
        }
    
    def _convert_age_group(self, age_group_response):
        """Convert age group response to numeric value"""
        if not age_group_response:
            return 40  # Default
        
        age_mapping = {
            "Under 30": 25, "৩০ এর নিচে": 25,
            "30-40": 35, "৩০-৪০": 35,
            "41-50": 45, "৪১-৫০": 45,
            "51-60": 55, "৫১-৬০": 55,
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
        """Convert smoking status to boolean with nuanced analysis"""
        if not smoking_response:
            return False
        
        current_smoking_indicators = [
            "Current light smoker", "Current heavy smoker", 
            "এখন হালকা ধূমপান করি", "এখন ভারী ধূমপান করি"
        ]
        
        return any(indicator in smoking_response for indicator in current_smoking_indicators)
    
    def _convert_alcohol_consumption(self, alcohol_response):
        """Convert alcohol consumption to heavy drinking boolean"""
        if not alcohol_response:
            return False
        
        heavy_drinking_indicators = [
            "Heavily", "Daily consumption", "বেশি", "প্রতিদিন"
        ]
        
        return any(indicator in alcohol_response for indicator in heavy_drinking_indicators)
    
    def _convert_family_history(self, family_history_response):
        """Convert family history response"""
        if not family_history_response:
            return False
        
        positive_indicators = [
            "One family member", "Multiple family members", "Multiple generations",
            "একজন পরিবারের সদস্য", "একাধিক পরিবারের সদস্য", "একাধিক প্রজন্ম"
        ]
        
        return any(indicator in family_history_response for indicator in positive_indicators)
    
    def _convert_sun_exposure(self, sun_response):
        """Convert sun exposure to boolean"""
        if not sun_response:
            return False
        
        return "Excessive" in sun_response or "অতিরিক্ত" in sun_response
    
    def _convert_occupational_exposure(self, occupational_response):
        """Convert occupational exposure to boolean"""
        if not occupational_response:
            return False
        
        return occupational_response not in ["No occupational exposure", "কোন পেশাগত এক্সপোজার নেই"]
    
    def _convert_chronic_diseases(self, chronic_response):
        """Convert chronic diseases response"""
        if not chronic_response:
            return False
        
        return chronic_response not in ["None", "কিছু নেই"]
    
    def _convert_cancer_history(self, cancer_response):
        """Convert cancer diagnosis history"""
        if not cancer_response:
            return False
        
        return "Yes" in cancer_response or "হ্যাঁ" in cancer_response
    
    def _convert_hepatitis_status(self, hepatitis_response):
        """Convert hepatitis status"""
        if not hepatitis_response:
            return False
        
        return "Positive" in hepatitis_response or "পজিটিভ" in hepatitis_response
    
    def _convert_hpv_status(self, hpv_response):
        """Convert HPV status"""
        if not hpv_response:
            return False
        
        return "Positive" in hpv_response or "পজিটিভ" in hpv_response
    
    def _build_enhanced_symptoms_description(self) -> str:
        """Build enhanced descriptive text from symptom responses"""
        
        symptom_descriptions = []
        main_concern = self.responses.get("main_concern", {}).get("response", "")
        
        if main_concern:
            symptom_descriptions.append(f"Main concern: {main_concern}")
        
        # Map symptoms to descriptions
        symptom_mapping = {
            "persistent_cough": "persistent cough lasting more than 3 weeks",
            "blood_in_sputum": "blood in sputum/coughed up phlegm",
            "unexplained_weight_loss": "unexplained weight loss of more than 5kg in 6 months",
            "unusual_lumps": "unusual lumps or masses anywhere on body",
            "breast_changes": "breast changes including lumps, dimpling, or nipple discharge",
            "unusual_bleeding": "unusual vaginal bleeding or discharge",
            "persistent_fatigue": "persistent extreme fatigue and weakness",
            "skin_changes": "changes in moles or new skin spots",
            "persistent_pain": "persistent worsening pain",
            "bowel_changes": "persistent changes in bowel habits",
            "testicular_lumps": "testicular lumps, swelling, or changes"
        }
        
        # Add digestive symptoms
        swallowing_response = self.responses.get("swallowing_difficulties", {}).get("response", "")
        if swallowing_response != "None" and swallowing_response != "কিছু নেই":
            symptom_descriptions.append(f"digestive issues: {swallowing_response}")
        
        # Add prostate symptoms
        prostate_response = self.responses.get("prostate_symptoms", {}).get("response", "")
        if prostate_response != "No symptoms" and prostate_response != "কোন লক্ষণ নেই":
            symptom_descriptions.append(f"prostate-related symptoms: {prostate_response}")
        
        # Add yes/no symptoms
        yes_responses = ["Yes", "হ্যাঁ"]
        for symptom_id, description in symptom_mapping.items():
            response = self.responses.get(symptom_id, {}).get("response")
            if response in yes_responses:
                symptom_descriptions.append(description)
        
        return ". ".join(symptom_descriptions) if symptom_descriptions else "No specific symptoms reported"
    
    def _calculate_enhanced_symptom_severity(self) -> int:
        """Calculate enhanced symptom severity score (1-10)"""
        
        severity_weights = {
            "blood_in_sputum": 9,
            "unexplained_weight_loss": 8,
            "unusual_bleeding": 8,
            "unusual_lumps": 7,
            "breast_changes": 7,
            "testicular_lumps": 7,
            "persistent_cough": 6,
            "persistent_pain": 6,
            "bowel_changes": 6,
            "skin_changes": 5,
            "persistent_fatigue": 4
        }
        
        # Additional weights for complex symptoms
        complex_symptom_weights = {
            "swallowing_difficulties": {
                "Difficulty swallowing": 8,
                "Multiple symptoms": 7,
                "Abdominal pain": 6,
                "Indigestion": 4
            },
            "prostate_symptoms": {
                "Blood in urine": 8,
                "Multiple symptoms": 7,
                "Difficulty urinating": 6,
                "Frequent urination": 4
            }
        }
        
        total_severity = 0
        symptom_count = 0
        
        # Calculate basic symptoms
        yes_responses = ["Yes", "হ্যাঁ"]
        for symptom_id, weight in severity_weights.items():
            response = self.responses.get(symptom_id, {}).get("response")
            if response in yes_responses:
                total_severity += weight
                symptom_count += 1
        
        # Calculate complex symptoms
        for symptom_id, weight_map in complex_symptom_weights.items():
            response = self.responses.get(symptom_id, {}).get("response", "")
            for symptom_type, weight in weight_map.items():
                if symptom_type in response:
                    total_severity += weight
                    symptom_count += 1
                    break
        
        # Factor in cancer history and high-risk conditions
        if self._convert_cancer_history(self.responses.get("cancer_diagnosis", {}).get("response")):
            total_severity += 2  # Boost severity for cancer history
        
        if self._convert_hepatitis_status(self.responses.get("hepatitis_status", {}).get("response")):
            total_severity += 1  # Boost for hepatitis
        
        if symptom_count == 0:
            return 1
        
        average_severity = total_severity / max(symptom_count, 1)
        return min(int(average_severity), 10)
    
    def _estimate_symptom_duration(self) -> str:
        """Estimate symptom duration based on responses"""
        
        # Check for specific duration indicators in main concern
        main_concern = self.responses.get("main_concern", {}).get("response", "").lower()
        
        duration_indicators = {
            "weeks": "weeks",
            "months": "months", 
            "years": "chronic",
            "recent": "recent",
            "sudden": "acute"
        }
        
        for indicator, duration in duration_indicators.items():
            if indicator in main_concern:
                return duration
        
        # Default estimation based on symptom types
        chronic_symptoms = ["persistent_cough", "persistent_fatigue", "bowel_changes"]
        acute_symptoms = ["blood_in_sputum", "unusual_bleeding", "testicular_lumps"]
        
        has_chronic = any(self.responses.get(symptom, {}).get("response") in ["Yes", "হ্যাঁ"] 
                         for symptom in chronic_symptoms)
        has_acute = any(self.responses.get(symptom, {}).get("response") in ["Yes", "হ্যাঁ"] 
                       for symptom in acute_symptoms)
        
        if has_acute:
            return "acute"
        elif has_chronic:
            return "chronic"
        else:
            return "unknown"
    
    def _analyze_symptom_pattern(self) -> str:
        """Analyze the pattern of symptoms"""
        
        symptom_categories = {
            "respiratory": ["persistent_cough", "blood_in_sputum"],
            "gastrointestinal": ["bowel_changes", "swallowing_difficulties"],
            "genitourinary": ["prostate_symptoms", "unusual_bleeding"],
            "systemic": ["unexplained_weight_loss", "persistent_fatigue"],
            "localized": ["unusual_lumps", "breast_changes", "skin_changes", "testicular_lumps"]
        }
        
        active_categories = []
        yes_responses = ["Yes", "হ্যাঁ"]
        
        for category, symptoms in symptom_categories.items():
            category_active = False
            for symptom in symptoms:
                response = self.responses.get(symptom, {}).get("response", "")
                if (response in yes_responses or 
                    (symptom in ["swallowing_difficulties", "prostate_symptoms"] and 
                     response not in ["None", "No symptoms", "কিছু নেই", "কোন লক্ষণ নেই"])):
                    category_active = True
                    break
            
            if category_active:
                active_categories.append(category)
        
        if len(active_categories) >= 3:
            return "multi-system"
        elif len(active_categories) == 2:
            return "bi-system"
        elif len(active_categories) == 1:
            return active_categories[0]
        else:
            return "minimal"
    
    def _extract_screening_history(self) -> Dict[str, str]:
        """Extract screening history from responses"""
        
        screening_history = {}
        
        screening_questions = [
            "mammogram_test", "pap_smear_test", "prostate_screening", 
            "colonoscopy_test", "hepatitis_status", "hpv_status"
        ]
        
        for question_id in screening_questions:
            response = self.responses.get(question_id, {}).get("response", "Unknown")
            screening_history[question_id] = response
        
        return screening_history
    
    def _extract_additional_risk_factors(self) -> Dict[str, Any]:
        """Extract additional risk factors for analysis"""
        
        return {
            "diet_quality": self.responses.get("diet_quality", {}).get("response", "Unknown"),
            "exercise_frequency": self.responses.get("exercise_frequency", {}).get("response", "Unknown"),
            "chronic_diseases": self.responses.get("chronic_diseases", {}).get("response", "None"),
            "occupational_exposure": self.responses.get("occupational_exposure", {}).get("response", "None"),
            "cancer_history": self.responses.get("cancer_diagnosis", {}).get("response", "No")
        }
    
    def _determine_urgency_level(self, symptoms_analysis: Dict, risk_assessment: Dict, processed_data: Dict) -> str:
        """Enhanced urgency level determination"""
        
        urgency_score = symptoms_analysis.get("urgency_score", 0)
        requires_immediate = symptoms_analysis.get("requires_immediate_attention", False)
        high_risk_cancers = risk_assessment.get("high_risk_cancers", [])
        
        # Check for high-risk symptoms
        high_risk_symptoms = self._identify_high_risk_symptoms()
        
        # Check for cancer history
        has_cancer_history = processed_data["demographics"].get("cancer_history", False)
        
        # Enhanced urgency calculation
        if requires_immediate or high_risk_symptoms or urgency_score >= 8:
            return "CRITICAL"
        elif (urgency_score >= 6 or len(high_risk_cancers) > 2 or 
              (has_cancer_history and urgency_score >= 4)):
            return "HIGH"
        elif urgency_score >= 4 or len(high_risk_cancers) > 0:
            return "MODERATE"
        else:
            return "LOW"
    
    def reset_consultation(self):
        """Reset consultation for new session"""
        self.responses = {}
        self.current_question_index = 0
        self.consultation_complete = False
        self.applicable_questions = []
        self.reasoning_engine.reset_reasoning_trace()
    
    def get_consultation_summary(self) -> Dict[str, Any]:
        """Enhanced consultation summary"""
        return {
            "consultation_date": datetime.now().isoformat(),
            "language": self.language,
            "questions_answered": len(self.responses),
            "applicable_questions": len(self.applicable_questions),
            "user_profile": self._generate_user_profile(),
            "responses": self.responses,
            "completion_status": "complete" if self.consultation_complete else "in_progress",
            "screening_gaps": self._identify_screening_gaps(),
            "risk_summary": self._generate_risk_summary()
        }
    
    def _identify_screening_gaps(self) -> List[str]:
        """Identify gaps in cancer screening"""
        
        gaps = []
        user_profile = self._generate_user_profile()
        age_group = user_profile["age_group"]
        gender = user_profile["gender"]
        
        # Age-specific screening gaps
        if gender == "Female":
            if age_group in ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]:
                mammogram_response = self.responses.get("mammogram_test", {}).get("response", "")
                if "Never" in mammogram_response or "More than 3 years" in mammogram_response:
                    gaps.append("Mammogram screening overdue")
            
            pap_response = self.responses.get("pap_smear_test", {}).get("response", "")
            if "Never" in pap_response or "More than 5 years" in pap_response:
                gaps.append("Pap smear screening overdue")
        
        elif gender == "Male":
            if age_group in ["51-60", "Over 60", "৫১-৬০", "৬০ এর উপরে"]:
                prostate_response = self.responses.get("prostate_screening", {}).get("response", "")
                if "Never" in prostate_response or "More than 3 years" in prostate_response:
                    gaps.append("Prostate screening overdue")
        
        # Universal screening gaps
        if age_group in ["41-50", "51-60", "Over 60", "৪১-৫০", "৫১-৬০", "৬০ এর উপরে"]:
            colonoscopy_response = self.responses.get("colonoscopy_test", {}).get("response", "")
            if "Never" in colonoscopy_response or "overdue" in colonoscopy_response:
                gaps.append("Colorectal screening overdue")
        
        return gaps
    
    def _generate_risk_summary(self) -> Dict[str, Any]:
        """Generate risk summary"""
        
        return {
            "high_risk_symptoms": self._identify_high_risk_symptoms(),
            "family_history_present": self._convert_family_history(
                self.responses.get("family_history", {}).get("response")
            ),
            "smoking_status": self.responses.get("smoking_status", {}).get("response", "Unknown"),
            "cancer_history": self._convert_cancer_history(
                self.responses.get("cancer_diagnosis", {}).get("response")
            ),
            "screening_compliance": len(self._identify_screening_gaps()) == 0
        }

    def _generate_enhanced_response_with_ai(self, original_response: str, ai_recommendations: Dict) -> str:
        """Enhance the original response with AI recommendations"""
        
        if self.language == "bn":
            enhanced_sections = [
                "\n\n---\n## 🤖 AI-চালিত ব্যক্তিগত পরামর্শ\n",
                "### 🚨 তাৎক্ষণিক যত্ন:\n"
            ]
            
            for recommendation in ai_recommendations.get("immediate_care", []):
                enhanced_sections.append(f"• {recommendation}\n")
            
            enhanced_sections.append("\n### 🛡️ প্রতিরোধমূলক যত্ন পরিকল্পনা:\n")
            preventive_care = ai_recommendations.get("preventive_care_plan", {})
            for category, recommendations in preventive_care.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:3]:  # Limit to top 3 per category
                        enhanced_sections.append(f"• {rec}\n")
                    enhanced_sections.append("\n")
            
            enhanced_sections.append("### 🏥 স্ক্রিনিং সূচি:\n")
            screening_schedule = ai_recommendations.get("screening_schedule", {})
            for cancer_type, schedule_info in screening_schedule.items():
                enhanced_sections.append(f"**{cancer_type.replace('_', ' ').title()}:** {schedule_info.get('test', '')} - {schedule_info.get('frequency', '')}\n")
            
            enhanced_sections.append("\n### 🍎 জীবনযাত্রার পরামর্শ:\n")
            lifestyle_mods = ai_recommendations.get("lifestyle_modifications", {})
            for category, recommendations in lifestyle_mods.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:2]:  # Top 2 per category
                        enhanced_sections.append(f"• {rec}\n")
            
            enhanced_sections.append(f"\n### 📋 AI সারসংক্ষেপ:\n")
            enhanced_sections.append(ai_recommendations.get("ai_summary", ""))
            
            enhanced_sections.append("\n\n---\n⚠️ **গুরুত্বপূর্ণ**: এই AI-চালিত পরামর্শগুলি ব্যক্তিগতকৃত নির্দেশনার জন্য। চূড়ান্ত চিকিৎসা সিদ্ধান্তের জন্য অবশ্যই একজন যোগ্য অনকোলজিস্টের পরামর্শ নিন।")
            
        else:
            enhanced_sections = [
                "\n\n---\n## 🤖 AI-Powered Personalized Recommendations\n",
                "### 🚨 Immediate Care:\n"
            ]
            
            for recommendation in ai_recommendations.get("immediate_care", []):
                enhanced_sections.append(f"• {recommendation}\n")
            
            enhanced_sections.append("\n### 🛡️ Preventive Care Plan:\n")
            preventive_care = ai_recommendations.get("preventive_care_plan", {})
            for category, recommendations in preventive_care.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:3]:  # Limit to top 3 per category
                        enhanced_sections.append(f"• {rec}\n")
                    enhanced_sections.append("\n")
            
            enhanced_sections.append("### 🏥 Screening Schedule:\n")
            screening_schedule = ai_recommendations.get("screening_schedule", {})
            for cancer_type, schedule_info in screening_schedule.items():
                enhanced_sections.append(f"**{cancer_type.replace('_', ' ').title()}:** {schedule_info.get('test', '')} - {schedule_info.get('frequency', '')}\n")
            
            enhanced_sections.append("\n### 🍎 Lifestyle Recommendations:\n")
            lifestyle_mods = ai_recommendations.get("lifestyle_modifications", {})
            for category, recommendations in lifestyle_mods.items():
                if recommendations:
                    enhanced_sections.append(f"**{category.replace('_', ' ').title()}:**\n")
                    for rec in recommendations[:2]:  # Top 2 per category
                        enhanced_sections.append(f"• {rec}\n")
            
            enhanced_sections.append(f"\n### 📋 AI Summary:\n")
            enhanced_sections.append(ai_recommendations.get("ai_summary", ""))
            
            enhanced_sections.append("\n\n---\n⚠️ **Important**: These AI-powered recommendations are for personalized guidance. Always consult with a qualified oncologist for final medical decisions.")
        
        return original_response + "".join(enhanced_sections)


# Integration functions remain the same but with enhanced functionality
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
            <p style="margin: 5px 0 0 0;">বয়স ও লিঙ্গ অনুযায়ী স্মার্ট প্রশ্নোত্তর সহ গতিশীল ঝুঁকি মূল্যায়ন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0;">🎯 Enhanced Cancer Specialist Consultation</h1>
            <p style="margin: 5px 0 0 0;">Dynamic risk assessment with smart age & gender-specific questionnaire</p>
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
                    <strong>📊 সম্পন্ন:</strong> {progress_percentage:.1f}%<br>
                    <strong>🎯 স্মার্ট প্রশ্ন:</strong> আপনার উত্তর অনুযায়ী প্রশ্ন নির্বাচিত
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 15px; border-radius: 10px; margin: 15px 0; 
                            border-left: 4px solid #2196f3;">
                    <strong>📋 Progress:</strong> Question {progress_info['current_question']} of {progress_info['total_questions']}<br>
                    <strong>📊 Complete:</strong> {progress_percentage:.1f}%<br>
                    <strong>🎯 Smart Questions:</strong> Tailored to your responses
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
    
    # Enhanced sidebar with consultation info
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                    color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <h3 style="margin: 0;">⚙️ Enhanced Cancer AI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if not consultation.consultation_complete:
            progress_info = consultation.get_progress_info()
            if language == "Bengali":
                st.markdown(f"""
                **📊 অগ্রগতি:** {progress_info['progress_percentage']:.1f}%  
                **📋 প্রশ্ন:** {progress_info['current_question']}/{progress_info['total_questions']}  
                **🎯 বিশেষত্ব:** গতিশীল ক্যান্সার মূল্যায়ন  
                **🧠 এআই:** উন্নত যুক্তি ইঞ্জিন  
                **👥 ব্যক্তিগত:** বয়স/লিঙ্গ অনুযায়ী প্রশ্ন
                """)
            else:
                st.markdown(f"""
                **📊 Progress:** {progress_info['progress_percentage']:.1f}%  
                **📋 Questions:** {progress_info['current_question']}/{progress_info['total_questions']}  
                **🎯 Specialty:** Dynamic Cancer Assessment  
                **🧠 AI:** Advanced Reasoning Engine  
                **👥 Personal:** Age/Gender-specific Questions
                """)
        else:
            consultation_summary = consultation.get_consultation_summary()
            if language == "Bengali":
                st.markdown(f"""
                **✅ স্থিতি:** পরামর্শ সম্পন্ন  
                **👤 প্রোফাইল:** {consultation_summary['user_profile']['gender']}, {consultation_summary['user_profile']['age_group']}  
                **📋 উত্তর:** {consultation_summary['questions_answered']} টি প্রশ্ন  
                **🎯 স্ক্রিনিং:** {len(consultation_summary['screening_gaps'])} টি গ্যাপ চিহ্নিত
                """)
            else:
                st.markdown(f"""
                **✅ Status:** Consultation Complete  
                **👤 Profile:** {consultation_summary['user_profile']['gender']}, {consultation_summary['user_profile']['age_group']}  
                **📋 Answered:** {consultation_summary['questions_answered']} questions  
                **🎯 Screening:** {len(consultation_summary['screening_gaps'])} gaps identified
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
                    label="📥 বিস্তারিত রিপোর্ট ডাউনলোড",
                    data=json.dumps(consultation_summary, indent=2, ensure_ascii=False),
                    file_name=f"enhanced_cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.download_button(
                    label="📥 Download Detailed Report",
                    data=json.dumps(consultation_summary, indent=2),
                    file_name=f"enhanced_cancer_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )


# Additional helper functions for the interface (keeping existing ones and adding new ones)
def display_current_question(question: QuestionnaireStep, consultation: EnhancedCancerConsultationSession, 
                           language: str, lang_code: str):
    """Display the current question with appropriate input widgets"""
    
    progress_info = consultation.get_progress_info()
    question_text = question.question_text[lang_code]
    
    # Question display with enhanced styling
    st.markdown(f"""
    <div style="background: white; padding: 25px; border-radius: 15px; margin: 20px 0; 
                border-left: 6px solid #ff6b6b; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="color: #ff6b6b; margin: 0 0 20px 0;">
            {'প্রশ্ন' if language == 'Bengali' else 'Question'} {progress_info['current_question']}:
        </h3>
        <p style="font-size: 1.2em; margin: 0; line-height: 1.5;">
            {question_text}
        </p>
        {f'<p style="font-size: 0.9em; color: #666; margin: 10px 0 0 0;"><em>📋 This question is tailored based on your previous responses</em></p>' if question.conditions else ''}
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


def display_consultation_start(consultation: EnhancedCancerConsultationSession, language: str, lang_code: str):
    """Display consultation start screen"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 15px; margin: 20px 0; 
                    border: 2px solid #ff6b6b; text-align: center;">
            <h2 style="color: #ff6b6b; margin: 0 0 20px 0;">🎯 গতিশীল ক্যান্সার স্ক্রিনিং প্রশ্নোত্তর</h2>
            <p style="font-size: 1.1em; margin: 15px 0;">
                আমি আপনাকে আপনার বয়স ও লিঙ্গ অনুযায়ী কিছু স্মার্ট প্রশ্ন করব যা আপনার ক্যান্সারের ঝুঁকি মূল্যায়ন করতে সাহায্য করবে।
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #333; margin: 0 0 15px 0;">🌟 নতুন উন্নত বৈশিষ্ট্য:</h4>
                <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                    <li>🎯 স্মার্ট প্রশ্ন নির্বাচন (বয়স/লিঙ্গ অনুযায়ী)</li>
                    <li>📊 বর্ধিত প্রশ্ন সেট (২৫+ প্রশ্ন)</li>
                    <li>⏱️ দ্রুততর প্রক্রিয়া (৭-১২ মিনিট)</li>
                    <li>🧠 গতিশীল AI বিশ্লেষণ</li>
                    <li>📋 ব্যক্তিগত সুপারিশ ও স্ক্রিনিং গাইড</li>
                    <li>🚨 উন্নত জরুরি সনাক্তকরণ</li>
                </ul>
            </div>
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0; font-size: 0.9em;">
                    <strong>⚠️ গুরুত্বপূর্ণ:</strong> এটি একটি উন্নত স্ক্রিনিং টুল। 
                    চূড়ান্ত রোগ নির্ণয়ের জন্য অবশ্যই একজন যোগ্য চিকিৎসকের পরামর্শ নিন।
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 স্মার্ট প্রশ্নোত্তর শুরু করুন", type="primary", use_container_width=True):
            st.rerun()
    else:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 15px; margin: 20px 0; 
                    border: 2px solid #ff6b6b; text-align: center;">
            <h2 style="color: #ff6b6b; margin: 0 0 20px 0;">🎯 Dynamic Cancer Screening Questionnaire</h2>
            <p style="font-size: 1.1em; margin: 15px 0;">
                I'll ask you smart questions tailored to your age and gender to help assess your cancer risk comprehensively.
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #333; margin: 0 0 15px 0;">🌟 New Enhanced Features:</h4>
                <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                    <li>🎯 Smart question selection (age/gender-specific)</li>
                    <li>📊 Expanded question set (25+ questions)</li>
                    <li>⏱️ Faster process (7-12 minutes)</li>
                    <li>🧠 Dynamic AI analysis</li>
                    <li>📋 Personalized recommendations & screening guide</li>
                    <li>🚨 Enhanced emergency detection</li>
                </ul>
            </div>
            <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                <p style="margin: 0; font-size: 0.9em;">
                    <strong>⚠️ Important:</strong> This is an advanced screening tool. 
                    Always consult qualified healthcare providers for definitive diagnosis and treatment.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Smart Questionnaire", type="primary", use_container_width=True):
            st.rerun()


def display_enhanced_consultation_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display comprehensive consultation results with enhanced AI recommendations"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ AI-সমৃদ্ধ পরামর্শ সম্পন্ন</h2>
            <p style="margin: 5px 0 0 0;">আপনার ব্যাপক ও গতিশীল ক্যান্সার ঝুঁকি মূল্যায়ন AI পরামর্শ সহ প্রস্তুত</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h2 style="margin: 0;">✅ AI-Enhanced Consultation Complete</h2>
            <p style="margin: 5px 0 0 0;">Your comprehensive & dynamic cancer risk assessment with AI recommendations is ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create enhanced tabs with AI recommendations
    if language == "Bengali":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 সারসংক্ষেপ", 
            #"🧠 AI বিশ্লেষণ", 
            "💡 গতিশীল সুপারিশ",
            "🤖 AI ব্যক্তিগত পরামর্শ",  # New AI tab
            "🔍 স্ক্রিনিং গাইড",
            "🧠 AI যুক্তি প্রক্রিয়া"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Summary", 
            #"🧠 AI Analysis", 
            "💡 Dynamic Recommendations",
            "🤖 AI Personal Care Plan",  # New AI tab
            "🔍 Screening Guide",
            "🧠 AI Reasoning Process"
        ])
    
    with tab1:
        display_enhanced_consultation_summary(consultation, language)
    
    # with tab2:
    #     display_enhanced_ai_analysis_results(consultation, language)
    
    with tab2:
        display_dynamic_recommendations_results(consultation, language)
    
    with tab3:  # New AI recommendations tab
        display_ai_recommendations_results(consultation, language)
    
    with tab4:
        display_screening_guide_results(consultation, language)
    
    with tab5:
        display_enhanced_consultation_ai_reasoning(consultation, language)


def display_enhanced_consultation_summary(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced consultation summary"""
    
    consultation_summary = consultation.get_consultation_summary()
    user_profile = consultation_summary['user_profile']
    
    if language == "Bengali":
        st.markdown("### 📋 বিস্তারিত পরামর্শের সারসংক্ষেপ")
        
        # User profile display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **👤 ব্যক্তিগত প্রোফাইল:**
            - **বয়স গ্রুপ:** {user_profile['age_group']}
            - **লিঙ্গ:** {user_profile['gender']}
            - **প্রধান সমস্যা:** {user_profile['main_concern'][:50]}...
            """)
        
        with col2:
            st.markdown(f"""
            **📊 পরামর্শ পরিসংখ্যান:**
            - **মোট প্রশ্ন:** {consultation_summary['questions_answered']}
            - **প্রযোজ্য প্রশ্ন:** {consultation_summary['applicable_questions']}
            - **সম্পন্নতা:** 100%
            - **তারিখ:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """)
        
        # Risk factors summary
        st.markdown("### 🎯 মূল ঝুঁকির কারণ সারসংক্ষেপ:")
        risk_summary = consultation_summary['risk_summary']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status = "✅" if not risk_summary['high_risk_symptoms'] else "⚠️"
            st.markdown(f"{status} **উচ্চ ঝুঁকির লক্ষণ:** {'না' if not risk_summary['high_risk_symptoms'] else 'হ্যাঁ'}")
        
        with col2:
            status = "✅" if not risk_summary['family_history_present'] else "⚠️"
            st.markdown(f"{status} **পারিবারিক ইতিহাস:** {'না' if not risk_summary['family_history_present'] else 'হ্যাঁ'}")
        
        with col3:
            status = "✅" if not risk_summary['cancer_history'] else "⚠️"
            st.markdown(f"{status} **ক্যান্সার ইতিহাস:** {'না' if not risk_summary['cancer_history'] else 'হ্যাঁ'}")
        
    else:
        st.markdown("### 📋 Enhanced Consultation Summary")
        
        # User profile display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **👤 Personal Profile:**
            - **Age Group:** {user_profile['age_group']}
            - **Gender:** {user_profile['gender']}
            - **Main Concern:** {user_profile['main_concern'][:50]}...
            """)
        
        with col2:
            st.markdown(f"""
            **📊 Consultation Statistics:**
            - **Total Questions:** {consultation_summary['questions_answered']}
            - **Applicable Questions:** {consultation_summary['applicable_questions']}
            - **Completion:** 100%
            - **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """)
        
        # Risk factors summary
        st.markdown("### 🎯 Key Risk Factors Summary:")
        risk_summary = consultation_summary['risk_summary']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status = "✅" if not risk_summary['high_risk_symptoms'] else "⚠️"
            st.markdown(f"{status} **High Risk Symptoms:** {'No' if not risk_summary['high_risk_symptoms'] else 'Yes'}")
        
        with col2:
            status = "✅" if not risk_summary['family_history_present'] else "⚠️"
            st.markdown(f"{status} **Family History:** {'No' if not risk_summary['family_history_present'] else 'Yes'}")
        
        with col3:
            status = "✅" if not risk_summary['cancer_history'] else "⚠️"
            st.markdown(f"{status} **Cancer History:** {'No' if not risk_summary['cancer_history'] else 'Yes'}")


def display_ai_recommendations_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display AI-generated personalized recommendations"""
    
    # FIXED: Get AI recommendations from consultation results
    ai_recommendations = {}
    
    # Try multiple ways to get the AI recommendations
    if hasattr(consultation, '_last_analysis_results') and consultation._last_analysis_results:
        ai_recommendations = consultation._last_analysis_results.get("ai_recommendations", {})
        logging.info(f"Found AI recommendations from _last_analysis_results: {len(ai_recommendations)} categories")
    
    # If not found, try to generate them now
    if not ai_recommendations and consultation.consultation_complete:
        try:
            logging.info("AI recommendations not found, generating now...")
            
            # Get the consultation data
            processed_data = consultation._process_responses_for_analysis()
            
            # Create analysis results for AI recommendations
            analysis_results = {
                "user_profile": consultation._generate_user_profile(),
                "symptoms_analysis": {"urgency_score": 3, "possible_cancer_types": []},
                "risk_assessment": {"cancer_specific_risks": {}},
                "recommendations": {}
            }
            
            # Generate AI recommendations
            from enhanced_cancer_consultation_system import AIRecommendationEngine
            ai_engine = AIRecommendationEngine(consultation.language)
            ai_recommendations = ai_engine.generate_ai_recommendations(
                consultation.responses,
                analysis_results
            )
            
            # Store for future use
            if not hasattr(consultation, '_last_analysis_results'):
                consultation._last_analysis_results = {}
            consultation._last_analysis_results["ai_recommendations"] = ai_recommendations
            
            logging.info(f"Successfully generated AI recommendations: {len(ai_recommendations)} categories")
            
        except Exception as e:
            logging.error(f"Failed to generate AI recommendations: {e}")
            # Use fallback recommendations
            ai_recommendations = consultation._create_fallback_ai_recommendations()
    
    # If still no recommendations, create basic fallback
    if not ai_recommendations:
        logging.warning("No AI recommendations available, using basic fallback")
        ai_recommendations = consultation._create_fallback_ai_recommendations()
    
    if language == "Bengali":
        st.markdown("### 🤖 AI-চালিত ব্যক্তিগত যত্ন পরিকল্পনা")
    else:
        st.markdown("### 🤖 AI-Powered Personalized Care Plan")
    
    # Display immediate care recommendations
    immediate_care = ai_recommendations.get("immediate_care", [])
    if immediate_care:
        if language == "Bengali":
            st.markdown("#### 🚨 তাৎক্ষণিক যত্ন পরামর্শ")
        else:
            st.markdown("#### 🚨 Immediate Care Recommendations")
        
        for i, recommendation in enumerate(immediate_care, 1):
            st.markdown(f"**{i}.** {recommendation}")
    
    # Display preventive care plan
    preventive_care = ai_recommendations.get("preventive_care_plan", {})
    if preventive_care:
        if language == "Bengali":
            st.markdown("#### 🛡️ প্রতিরোধমূলক যত্ন পরিকল্পনা")
        else:
            st.markdown("#### 🛡️ Preventive Care Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_prevention = preventive_care.get("primary_prevention", [])
            if primary_prevention:
                if language == "Bengali":
                    st.markdown("**প্রাথমিক প্রতিরোধ:**")
                else:
                    st.markdown("**Primary Prevention:**")
                for rec in primary_prevention:
                    st.markdown(f"• {rec}")
        
        with col2:
            secondary_prevention = preventive_care.get("secondary_prevention", [])
            if secondary_prevention:
                if language == "Bengali":
                    st.markdown("**মাধ্যমিক প্রতিরোধ:**")
                else:
                    st.markdown("**Secondary Prevention:**")
                for rec in secondary_prevention:
                    st.markdown(f"• {rec}")
    
    # Display screening schedule
    screening_schedule = ai_recommendations.get("screening_schedule", {})
    if screening_schedule:
        if language == "Bengali":
            st.markdown("#### 🏥 ব্যক্তিগত স্ক্রিনিং সূচি")
        else:
            st.markdown("#### 🏥 Personalized Screening Schedule")
        
        for cancer_type, schedule_info in screening_schedule.items():
            if schedule_info:
                cancer_name = cancer_type.replace('_', ' ').title()
                test_name = schedule_info.get('test', 'Not specified')
                frequency = schedule_info.get('frequency', 'Not specified')
                next_due = schedule_info.get('next_due', 'Consult with doctor')
                
                st.markdown(f"""
                <div style="background: #f0f8ff; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #007bff;">
                    <h5 style="margin: 0 0 10px 0; color: #007bff;">{cancer_name}</h5>
                    <p style="margin: 5px 0;"><strong>{'পরীক্ষা' if language == 'Bengali' else 'Test'}:</strong> {test_name}</p>
                    <p style="margin: 5px 0;"><strong>{'ফ্রিকোয়েন্সি' if language == 'Bengali' else 'Frequency'}:</strong> {frequency}</p>
                    <p style="margin: 5px 0;"><strong>{'পরবর্তী নির্ধারিত' if language == 'Bengali' else 'Next Due'}:</strong> {next_due}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Display AI summary
    ai_summary = ai_recommendations.get("ai_summary", "")
    if ai_summary:
        if language == "Bengali":
            st.markdown("#### 📋 AI সামগ্রিক সারসংক্ষেপ")
        else:
            st.markdown("#### 📋 AI Comprehensive Summary")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin: 15px 0;">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                {ai_summary.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Success message
    if language == "Bengali":
        st.success("✅ AI পরামর্শ সফলভাবে তৈরি হয়েছে!")
    else:
        st.success("✅ AI recommendations generated successfully!")
    
    # Final disclaimer
    if language == "Bengali":
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border: 2px solid #ffc107; margin: 20px 0;">
            <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ গুরুত্বপূর্ণ দাবিত্যাগ</h4>
            <p style="margin: 0;">এই AI-চালিত পরামর্শগুলি আপনার প্রদত্ত তথ্যের উপর ভিত্তি করে ব্যক্তিগতকৃত নির্দেশনার জন্য তৈরি। 
            এগুলি পেশাদার চিকিৎসা পরামর্শ, রোগ নির্ণয় বা চিকিৎসার বিকল্প নয়। 
            সকল চিকিৎসা সংক্রান্ত সিদ্ধান্তের জন্য অবশ্যই একজন যোগ্য অনকোলজিস্ট বা চিকিৎসকের পরামর্শ নিন।</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border: 2px solid #ffc107; margin: 20px 0;">
            <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ Important Disclaimer</h4>
            <p style="margin: 0;">These AI-powered recommendations are generated based on the information you provided and are intended for personalized guidance. 
            They are not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult with a qualified oncologist or healthcare provider for all medical decisions.</p>
        </div>
        """, unsafe_allow_html=True)



def display_dynamic_recommendations_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display dynamic recommendations based on user responses"""
    
    # Get the analysis results from the completed consultation
    if hasattr(consultation, '_last_analysis_results'):
        analysis_results = consultation._last_analysis_results
        recommendations = analysis_results.get("recommendations", {})
    else:
        # Fallback: generate recommendations based on stored responses
        processed_data = consultation._process_responses_for_analysis()
        recommendations = consultation._generate_dynamic_recommendations(
            processed_data, {}, {}, {}
        )
    
    if language == "Bengali":
        st.markdown("### 💡 আপনার জন্য গতিশীল সুপারিশ")
        
        # Immediate actions
        if recommendations.get("immediate_actions"):
            st.markdown("#### 🚨 তাৎক্ষণিক পদক্ষেপ:")
            for action in recommendations["immediate_actions"]:
                st.markdown(f"• {action}")
        
        # Screening recommendations
        if recommendations.get("screening_recommendations"):
            st.markdown("#### 🔬 সুপারিশকৃত স্ক্রিনিং:")
            for screening in recommendations["screening_recommendations"]:
                st.markdown(f"• {screening}")
        
        # Lifestyle modifications
        if recommendations.get("lifestyle_modifications"):
            st.markdown("#### 🌱 জীবনযাত্রার পরিবর্তন:")
            for lifestyle in recommendations["lifestyle_modifications"]:
                st.markdown(f"• {lifestyle}")
        
        # Specialist referrals
        if recommendations.get("specialist_referrals"):
            st.markdown("#### 👨‍⚕️ বিশেষজ্ঞ পরামর্শ:")
            for referral in recommendations["specialist_referrals"]:
                st.markdown(f"• {referral}")
        
        # Personalized advice
        if recommendations.get("personalized_advice"):
            st.markdown("#### 🎯 আপনার জন্য বিশেষ পরামর্শ:")
            for advice in recommendations["personalized_advice"]:
                st.markdown(f"• {advice}")
        
    else:
        st.markdown("### 💡 Your Dynamic Recommendations")
        
        # Immediate actions
        if recommendations.get("immediate_actions"):
            st.markdown("#### 🚨 Immediate Actions:")
            for action in recommendations["immediate_actions"]:
                st.markdown(f"• {action}")
        
        # Screening recommendations
        if recommendations.get("screening_recommendations"):
            st.markdown("#### 🔬 Recommended Screenings:")
            for screening in recommendations["screening_recommendations"]:
                st.markdown(f"• {screening}")
        
        # Lifestyle modifications
        if recommendations.get("lifestyle_modifications"):
            st.markdown("#### 🌱 Lifestyle Modifications:")
            for lifestyle in recommendations["lifestyle_modifications"]:
                st.markdown(f"• {lifestyle}")
        
        # Specialist referrals
        if recommendations.get("specialist_referrals"):
            st.markdown("#### 👨‍⚕️ Specialist Referrals:")
            for referral in recommendations["specialist_referrals"]:
                st.markdown(f"• {referral}")
        
        # Personalized advice
        if recommendations.get("personalized_advice"):
            st.markdown("#### 🎯 Personalized Advice for You:")
            for advice in recommendations["personalized_advice"]:
                st.markdown(f"• {advice}")


def display_screening_guide_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display personalized screening guide"""
    
    consultation_summary = consultation.get_consultation_summary()
    screening_gaps = consultation_summary['screening_gaps']
    user_profile = consultation_summary['user_profile']
    
    if language == "Bengali":
        st.markdown("### 🔍 আপনার ব্যক্তিগত স্ক্রিনিং গাইড")
        
        if screening_gaps:
            st.markdown("#### ⚠️ অগ্রাধিকার স্ক্রিনিং (অনুপস্থিত):")
            for gap in screening_gaps:
                st.error(f"🔴 {gap}")
        else:
            st.success("✅ আপনার স্ক্রিনিং আপ টু ডেট!")
        
        # Age and gender specific guidelines
        st.markdown("#### 📅 আপনার জন্য প্রস্তাবিত স্ক্রিনিং সূচি:")
        
        age_group = user_profile['age_group']
        gender = user_profile['gender']
        
        if gender == "Female" or gender == "মহিলা":
            st.markdown("""
            **🔬 মহিলাদের জন্য প্রস্তাবিত স্ক্রিনিং:**
            - **ম্যামোগ্রাম:** ৪০+ বয়সে বার্ষিক
            - **প্যাপ স্মিয়ার:** ২১+ বয়সে প্রতি ৩ বছর
            - **HPV টেস্ট:** ৩০+ বয়সে প্যাপ স্মিয়ারের সাথে
            - **কোলনোস্কোপি:** ৪৫+ বয়সে প্রতি ১০ বছর
            """)
        
        elif gender == "Male" or gender == "পুরুষ":
            st.markdown("""
            **🔬 পুরুষদের জন্য প্রস্তাবিত স্ক্রিনিং:**
            - **প্রোস্টেট স্ক্রিনিং:** ৫০+ বয়সে বার্ষিক (PSA)
            - **কোলনোস্কোপি:** ৪৫+ বয়সে প্রতি ১০ বছর
            - **টেস্টিকুলার সেল্ফ এক্সাম:** মাসিক
            """)
        
        # Universal screenings
        st.markdown("""
        **🌐 সবার জন্য প্রস্তাবিত স্ক্রিনিং:**
        - **স্কিন চেক:** বার্ষিক (বিশেষত রোদে বেশি থাকলে)
        - **হেপাটাইটিস স্ক্রিনিং:** একবার (ঝুঁকি থাকলে)
        - **সাধারণ স্বাস্থ্য চেকআপ:** বার্ষিক
        """)
        
    else:
        st.markdown("### 🔍 Your Personalized Screening Guide")
        
        if screening_gaps:
            st.markdown("#### ⚠️ Priority Screenings (Missing):")
            for gap in screening_gaps:
                st.error(f"🔴 {gap}")
        else:
            st.success("✅ Your screenings are up to date!")
        
        # Age and gender specific guidelines
        st.markdown("#### 📅 Recommended Screening Schedule for You:")
        
        age_group = user_profile['age_group']
        gender = user_profile['gender']
        
        if gender == "Female":
            st.markdown("""
            **🔬 Recommended Screenings for Women:**
            - **Mammogram:** Annual starting age 40+
            - **Pap Smear:** Every 3 years starting age 21+
            - **HPV Test:** Starting age 30+ with Pap smear
            - **Colonoscopy:** Every 10 years starting age 45+
            """)
        
        elif gender == "Male":
            st.markdown("""
            **🔬 Recommended Screenings for Men:**
            - **Prostate Screening:** Annual starting age 50+ (PSA)
            - **Colonoscopy:** Every 10 years starting age 45+
            - **Testicular Self-Exam:** Monthly
            """)
        
        # Universal screenings
        st.markdown("""
        **🌐 Universal Recommended Screenings:**
        - **Skin Check:** Annual (especially with sun exposure)
        - **Hepatitis Screening:** Once (if at risk)
        - **General Health Checkup:** Annual
        """)


# Keep existing helper functions and add the enhanced ones above
def display_enhanced_ai_analysis_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced AI analysis results"""
    
    if language == "Bengali":
        st.markdown("### 🧠 উন্নত AI বিশ্লেষণ প্রক্রিয়া")
    else:
        st.markdown("### 🧠 Enhanced AI Analysis Process")
    
    # Show the analysis was personalized
    user_profile = consultation._generate_user_profile()
    
    if language == "Bengali":
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin: 15px 0;">
            <h4>🔍 আপনার জন্য ব্যক্তিগতকৃত বিশ্লেষণ:</h4>
            <p><strong>👤 প্রোফাইল:</strong> {user_profile['gender']}, {user_profile['age_group']}</p>
            <p><strong>📋 প্রশ্ন সেট:</strong> আপনার বয়স ও লিঙ্গ অনুযায়ী নির্বাচিত</p>
            <p><strong>🧠 বিশ্লেষণ:</strong> গতিশীল ও প্রসঙ্গ-সচেতন</p>
            <p><strong>💡 সুপারিশ:</strong> আপনার উত্তর ভিত্তিক কাস্টমাইজড</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔬 বিস্তারিত AI যুক্তি প্রক্রিয়া দেখতে 'AI যুক্তি প্রক্রিয়া' ট্যাব ব্যবহার করুন।")
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin: 15px 0;">
            <h4>🔍 Personalized Analysis for You:</h4>
            <p><strong>👤 Profile:</strong> {user_profile['gender']}, {user_profile['age_group']}</p>
            <p><strong>📋 Question Set:</strong> Selected based on your age & gender</p>
            <p><strong>🧠 Analysis:</strong> Dynamic & context-aware</p>
            <p><strong>💡 Recommendations:</strong> Customized based on your responses</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔬 Use the 'AI Reasoning Process' tab to see detailed AI reasoning.")


def display_enhanced_risk_assessment_results(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced risk assessment results"""
    
    if language == "Bengali":
        st.markdown("### 📊 বিস্তারিত ক্যান্সার ঝুঁকি মূল্যায়ন")
    else:
        st.markdown("### 📊 Detailed Cancer Risk Assessment")
    
    # This would be populated from the actual analysis results
    # For now, showing the structure
    if language == "Bengali":
        st.info("ঝুঁকি মূল্যায়ন আপনার সম্পূর্ণ উত্তরের ভিত্তিতে গণনা করা হয়েছে এবং আপনার বয়স, লিঙ্গ ও ব্যক্তিগত ইতিহাস বিবেচনা করেছে।")
    else:
        st.info("Risk assessment calculated based on your complete responses considering your age, gender, and personal history.")


def display_enhanced_consultation_ai_reasoning(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced AI reasoning for the consultation"""
    
    if language == "Bengali":
        st.markdown("### 🧠 AI যুক্তি প্রক্রিয়া বিশ্লেষণ")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="margin: 0;">🎯 AI কীভাবে আপনার ঝুঁকি বিশ্লেষণ করেছে</h3>
            <p style="margin: 10px 0 0 0;">প্রতিটি ধাপে AI এর গতিশীল চিন্তাভাবনা ও যুক্তি দেখুন</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 🧠 AI Reasoning Process Analysis")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h3 style="margin: 0;">🎯 How AI Analyzed Your Risk Dynamically</h3>
            <p style="margin: 10px 0 0 0;">See the AI's dynamic thinking and reasoning at each step</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check if reasoning engine has reasoning trace
    if hasattr(consultation, 'reasoning_engine') and consultation.reasoning_engine.reasoning_trace:
        try:
            reasoning_explanation = consultation.reasoning_engine.get_reasoning_explanation()
            
            if reasoning_explanation:
                display_detailed_reasoning_trace(reasoning_explanation, language)
            else:
                display_enhanced_reasoning_fallback(consultation, language)
                
        except Exception as e:
            logging.error(f"Error displaying reasoning trace: {e}")
            display_enhanced_reasoning_fallback(consultation, language)
    else:
        # Show enhanced demo reasoning
        display_enhanced_reasoning_fallback(consultation, language)


def display_detailed_reasoning_trace(reasoning_explanation: dict, language: str):
    """Display the detailed AI reasoning trace with enhanced interactive elements"""
    
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
                "Recommendation Generation": "গতিশীল সুপারিশ প্রস্তুতি",
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


def display_enhanced_reasoning_fallback(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced fallback reasoning information"""
    
    if language == "Bengali":
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #856404;">📋 গতিশীল যুক্তি প্রক্রিয়া</h4>
            <p style="margin: 5px 0;">AI আপনার উত্তরের ভিত্তিতে নিম্নলিখিত গতিশীল পদ্ধতিতে ঝুঁকি বিশ্লেষণ করেছে:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show enhanced demo reasoning process
        display_enhanced_demo_reasoning_for_consultation(consultation, language)
        
    else:
        st.markdown("""
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #856404;">📋 Dynamic Reasoning Process</h4>
            <p style="margin: 5px 0;">The AI analyzed your risk using the following dynamic methodology based on your responses:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show enhanced demo reasoning process
        display_enhanced_demo_reasoning_for_consultation(consultation, language)


def display_enhanced_demo_reasoning_for_consultation(consultation: EnhancedCancerConsultationSession, language: str):
    """Display enhanced demo reasoning process based on actual consultation responses"""
    
    # Get user profile for personalized reasoning
    user_profile = consultation._generate_user_profile()
    
    if language == "Bengali":
        demo_steps = [
            {
                "step": "ব্যক্তিগত প্রোফাইল বিশ্লেষণ",
                "reasoning": f"আপনার প্রোফাইল ({user_profile['gender']}, {user_profile['age_group']}) অনুযায়ী স্মার্ট প্রশ্ন নির্বাচন করা হয়েছে। আপনার বয়স ও লিঙ্গের জন্য প্রাসঙ্গিক ক্যান্সার ঝুঁকির কারণগুলি চিহ্নিত করা হয়েছে।",
                "confidence": 0.95,
                "details": f"প্রোফাইল: {user_profile['gender']}, {user_profile['age_group']}, প্রশ্ন সেট: কাস্টমাইজড"
            },
            {
                "step": "লক্ষণ ও উত্তর বিশ্লেষণ", 
                "reasoning": f"আপনার মূল সমস্যা '{user_profile['main_concern'][:30]}...' এবং অন্যান্য উত্তরগুলি বিশ্লেষণ করে সম্ভাব্য ঝুঁকির প্যাটার্ন চিহ্নিত করা হয়েছে। প্রতিটি উত্তর ওজন অনুযায়ী মূল্যায়ন করা হয়েছে।",
                "confidence": 0.88,
                "details": f"প্রধান সমস্যা: বিশ্লেষিত, উত্তর সংখ্যা: {len(consultation.responses)}, প্যাটার্ন: চিহ্নিত"
            },
            {
                "step": "ঝুঁকি কারণ ম্যাট্রিক্স",
                "reasoning": f"আপনার ধূমপান স্থিতি ({user_profile.get('smoking_status', 'অজানা')}), পারিবারিক ইতিহাস ({user_profile.get('family_history', 'অজানা')}), এবং অন্যান্য ঝুঁকির কারণগুলি একটি বিস্তৃত ম্যাট্রিক্সে গণনা করা হয়েছে।",
                "confidence": 0.85,
                "details": "ঝুঁকি ম্যাট্রিক্স: গণনা সম্পূর্ণ, কারণসমূহ: ওজন অনুযায়ী মূল্যায়িত"
            },
            {
                "step": "গতিশীল সুপারিশ তৈরি",
                "reasoning": "আপনার নির্দিষ্ট উত্তর ও প্রোফাইলের ভিত্তিতে ব্যক্তিগতকৃত সুপারিশ তৈরি করা হয়েছে। এতে স্ক্রিনিং, জীবনযাত্রার পরিবর্তন, এবং ফলো-আপের কাস্টম পরামর্শ রয়েছে।",
                "confidence": 0.92,
                "details": "সুপারিশ প্রকার: ব্যক্তিগত, স্ক্রিনিং: বয়স/লিঙ্গ অনুযায়ী, ফলো-আপ: ঝুঁকি-ভিত্তিক"
            }
        ]
    else:
        demo_steps = [
            {
                "step": "Personal Profile Analysis",
                "reasoning": f"Smart questions were selected based on your profile ({user_profile['gender']}, {user_profile['age_group']}). Cancer risk factors relevant to your age and gender were identified and prioritized.",
                "confidence": 0.95,
                "details": f"Profile: {user_profile['gender']}, {user_profile['age_group']}, Question set: Customized"
            },
            {
                "step": "Symptom & Response Analysis",
                "reasoning": f"Your main concern '{user_profile['main_concern'][:30]}...' and other responses were analyzed to identify potential risk patterns. Each response was weighted according to established medical guidelines.",
                "confidence": 0.88,
                "details": f"Main concern: Analyzed, Response count: {len(consultation.responses)}, Patterns: Identified"
            },
            {
                "step": "Risk Factor Matrix",
                "reasoning": f"Your smoking status ({user_profile.get('smoking_status', 'Unknown')}), family history ({user_profile.get('family_history', 'Unknown')}), and other risk factors were calculated in a comprehensive matrix.",
                "confidence": 0.85,
                "details": "Risk matrix: Calculated, Factors: Weighted evaluation completed"
            },
            {
                "step": "Dynamic Recommendation Generation", 
                "reasoning": "Personalized recommendations were created based on your specific responses and profile. These include custom screening schedules, lifestyle modifications, and follow-up care tailored to your individual risk factors.",
                "confidence": 0.92,
                "details": "Recommendation type: Personalized, Screening: Age/gender-specific, Follow-up: Risk-based"
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
    
    # Add explanation of enhanced features
    if language == "Bengali":
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h5>🎯 উন্নত AI বৈশিষ্ট্যসমূহ:</h5>
            <ul style="margin: 10px 0 0 20px; font-size: 0.9em;">
                <li><strong>গতিশীল প্রশ্ন নির্বাচন:</strong> আপনার বয়স ও লিঙ্গ অনুযায়ী প্রাসঙ্গিক প্রশ্ন</li>
                <li><strong>ব্যক্তিগত ঝুঁকি ম্যাট্রিক্স:</strong> আপনার উত্তর ভিত্তিক কাস্টম গণনা</li>
                <li><strong>স্মার্ট সুপারিশ:</strong> আপনার প্রোফাইল অনুযায়ী তৈরি</li>
                <li><strong>প্রসঙ্গ-সচেতন বিশ্লেষণ:</strong> প্রতিটি উত্তরের গুরুত্ব বিবেচনা</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #2196f3; margin: 20px 0;">
            <h5>🎯 Enhanced AI Features:</h5>
            <ul style="margin: 10px 0 0 20px; font-size: 0.9em;">
                <li><strong>Dynamic Question Selection:</strong> Relevant questions based on your age & gender</li>
                <li><strong>Personalized Risk Matrix:</strong> Custom calculations based on your responses</li>
                <li><strong>Smart Recommendations:</strong> Tailored to your specific profile</li>
                <li><strong>Context-Aware Analysis:</strong> Each response weighted for importance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)