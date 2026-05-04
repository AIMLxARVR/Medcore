# cancer_reasoning_engine.py - Advanced cancer domain AI with reasoning capabilities

import os
import logging
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CancerType(Enum):
    """Enumeration of cancer types for structured reasoning"""
    BREAST = "breast_cancer"
    LUNG = "lung_cancer"
    COLORECTAL = "colorectal_cancer"
    PROSTATE = "prostate_cancer"
    CERVICAL = "cervical_cancer"
    LIVER = "liver_cancer"
    STOMACH = "stomach_cancer"
    SKIN = "skin_cancer"
    BLOOD = "blood_cancer"
    UNKNOWN = "unknown"

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class ReasoningStep(Enum):
    """Steps in the reasoning process"""
    SYMPTOM_ANALYSIS = "symptom_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    RECOMMENDATION_GENERATION = "recommendation_generation"
    URGENCY_EVALUATION = "urgency_evaluation"

@dataclass
class CancerSymptom:
    """Structured representation of cancer symptoms"""
    name: str
    severity: int  # 1-10 scale
    duration: str
    associated_symptoms: List[str]
    cancer_types: List[CancerType]
    urgency_score: int  # 1-10 scale

@dataclass
class RiskFactor:
    """Cancer risk factors"""
    factor: str
    weight: float  # 0.1-1.0
    applicable_cancers: List[CancerType]

@dataclass
class ReasoningTrace:
    """Trace of reasoning steps for explainability"""
    step: ReasoningStep
    input_data: Dict[str, Any]
    reasoning: str
    output: Dict[str, Any]
    confidence: float
    timestamp: datetime

class CancerKnowledgeBase:
    """Knowledge base for cancer domain reasoning"""
    
    def __init__(self):
        self.symptoms_db = self._initialize_symptoms_db()
        self.risk_factors_db = self._initialize_risk_factors_db()
        self.screening_guidelines = self._initialize_screening_guidelines()
        
    def _initialize_symptoms_db(self) -> Dict[str, CancerSymptom]:
        """Initialize comprehensive cancer symptoms database"""
        return {
            "persistent_cough": CancerSymptom(
                name="Persistent Cough",
                severity=0,  # Will be set based on user input
                duration="",
                associated_symptoms=["blood_in_sputum", "chest_pain", "shortness_of_breath"],
                cancer_types=[CancerType.LUNG],
                urgency_score=7
            ),
            "breast_lump": CancerSymptom(
                name="Breast Lump",
                severity=0,
                duration="",
                associated_symptoms=["nipple_discharge", "breast_pain", "skin_changes"],
                cancer_types=[CancerType.BREAST],
                urgency_score=8
            ),
            "blood_in_stool": CancerSymptom(
                name="Blood in Stool",
                severity=0,
                duration="",
                associated_symptoms=["abdominal_pain", "weight_loss", "change_in_bowel_habits"],
                cancer_types=[CancerType.COLORECTAL],
                urgency_score=8
            ),
            "unexplained_weight_loss": CancerSymptom(
                name="Unexplained Weight Loss",
                severity=0,
                duration="",
                associated_symptoms=["fatigue", "loss_of_appetite", "night_sweats"],
                cancer_types=[CancerType.LUNG, CancerType.STOMACH, CancerType.LIVER, CancerType.BLOOD],
                urgency_score=6
            ),
            "persistent_fatigue": CancerSymptom(
                name="Persistent Fatigue",
                severity=0,
                duration="",
                associated_symptoms=["weakness", "pale_skin", "shortness_of_breath"],
                cancer_types=[CancerType.BLOOD, CancerType.LIVER],
                urgency_score=5
            ),
            "unusual_bleeding": CancerSymptom(
                name="Unusual Bleeding",
                severity=0,
                duration="",
                associated_symptoms=["pelvic_pain", "irregular_periods", "post_coital_bleeding"],
                cancer_types=[CancerType.CERVICAL],
                urgency_score=7
            ),
            "skin_changes": CancerSymptom(
                name="Skin Changes",
                severity=0,
                duration="",
                associated_symptoms=["mole_changes", "new_growths", "non_healing_sores"],
                cancer_types=[CancerType.SKIN],
                urgency_score=6
            )
        }
    
    def _initialize_risk_factors_db(self) -> Dict[str, RiskFactor]:
        """Initialize cancer risk factors database"""
        return {
            "smoking": RiskFactor(
                factor="Smoking",
                weight=0.9,
                applicable_cancers=[CancerType.LUNG, CancerType.CERVICAL, CancerType.COLORECTAL]
            ),
            "family_history": RiskFactor(
                factor="Family History",
                weight=0.7,
                applicable_cancers=[CancerType.BREAST, CancerType.COLORECTAL, CancerType.PROSTATE]
            ),
            "age_over_50": RiskFactor(
                factor="Age over 50",
                weight=0.6,
                applicable_cancers=[CancerType.BREAST, CancerType.COLORECTAL, CancerType.PROSTATE]
            ),
            "alcohol_consumption": RiskFactor(
                factor="Heavy Alcohol Consumption",
                weight=0.5,
                applicable_cancers=[CancerType.LIVER, CancerType.BREAST, CancerType.COLORECTAL]
            ),
            "hpv_infection": RiskFactor(
                factor="HPV Infection",
                weight=0.8,
                applicable_cancers=[CancerType.CERVICAL]
            ),
            "sun_exposure": RiskFactor(
                factor="Excessive Sun Exposure",
                weight=0.7,
                applicable_cancers=[CancerType.SKIN]
            )
        }
    
    def _initialize_screening_guidelines(self) -> Dict[CancerType, Dict]:
        """Initialize screening guidelines for different cancers"""
        return {
            CancerType.BREAST: {
                "age_start": 40,
                "frequency": "annually",
                "method": "mammography",
                "high_risk_start": 30
            },
            CancerType.CERVICAL: {
                "age_start": 21,
                "frequency": "every 3 years",
                "method": "pap smear",
                "high_risk_frequency": "annually"
            },
            CancerType.COLORECTAL: {
                "age_start": 45,
                "frequency": "every 10 years",
                "method": "colonoscopy",
                "alternative": "FIT test annually"
            },
            CancerType.PROSTATE: {
                "age_start": 50,
                "frequency": "annually",
                "method": "PSA test",
                "high_risk_start": 45
            }
        }

class CancerReasoningEngine:
    """Advanced reasoning engine for cancer domain AI"""
    
    def __init__(self, language="en"):
        self.language = language
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.knowledge_base = CancerKnowledgeBase()
        self.reasoning_trace: List[ReasoningTrace] = []
        
        # Enhanced model for complex reasoning
        self.reasoning_model = "meta-llama/llama-4-maverick-17b-128e-instruct"
        
    def analyze_symptoms(self, symptoms_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze symptoms with structured reasoning
        
        Args:
            symptoms_data: Dictionary containing symptom information
            
        Returns:
            Analysis results with reasoning trace
        """
        
        step_input = symptoms_data.copy()
        reasoning_text = ""
        
        # Extract and structure symptoms
        identified_symptoms = []
        total_urgency_score = 0
        
        for symptom_key, symptom_obj in self.knowledge_base.symptoms_db.items():
            if self._symptom_mentioned(symptom_key, symptoms_data.get('description', '')):
                # Update symptom with user-specific data
                symptom_obj.severity = symptoms_data.get('severity', 5)
                symptom_obj.duration = symptoms_data.get('duration', 'unknown')
                identified_symptoms.append(symptom_obj)
                total_urgency_score += symptom_obj.urgency_score
                
                reasoning_text += f"Identified symptom: {symptom_obj.name} with urgency score {symptom_obj.urgency_score}. "
        
        # Calculate overall urgency
        avg_urgency = total_urgency_score / len(identified_symptoms) if identified_symptoms else 0
        
        reasoning_text += f"Average urgency score: {avg_urgency:.2f}. "
        
        # Determine possible cancer types
        possible_cancers = self._get_possible_cancer_types(identified_symptoms)
        reasoning_text += f"Possible cancer types based on symptoms: {[ct.value for ct in possible_cancers]}. "
        
        analysis_result = {
            "identified_symptoms": [s.name for s in identified_symptoms],
            "urgency_score": avg_urgency,
            "possible_cancer_types": [ct.value for ct in possible_cancers],
            "requires_immediate_attention": avg_urgency >= 7,
            "symptom_details": {s.name: {
                "severity": s.severity,
                "duration": s.duration,
                "urgency": s.urgency_score
            } for s in identified_symptoms}
        }
        
        # Add to reasoning trace
        self.reasoning_trace.append(ReasoningTrace(
            step=ReasoningStep.SYMPTOM_ANALYSIS,
            input_data=step_input,
            reasoning=reasoning_text,
            output=analysis_result,
            confidence=0.8,
            timestamp=datetime.now()
        ))
        
        return analysis_result
    
    def assess_risk_factors(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess cancer risk factors with reasoning
        """
        
        step_input = patient_data.copy()
        reasoning_text = ""
        
        risk_assessment = {}
        total_risk_score = 0
        applicable_risks = []
        
        for risk_key, risk_factor in self.knowledge_base.risk_factors_db.items():
            if self._risk_factor_present(risk_key, patient_data):
                applicable_risks.append(risk_factor)
                total_risk_score += risk_factor.weight
                reasoning_text += f"Risk factor identified: {risk_factor.factor} (weight: {risk_factor.weight}). "
        
        # Calculate risk levels for different cancer types
        for cancer_type in CancerType:
            if cancer_type == CancerType.UNKNOWN:
                continue
                
            cancer_specific_risk = 0
            cancer_risk_factors = []
            
            for risk in applicable_risks:
                if cancer_type in risk.applicable_cancers:
                    cancer_specific_risk += risk.weight
                    cancer_risk_factors.append(risk.factor)
            
            # Normalize risk score (0-1 scale)
            normalized_risk = min(cancer_specific_risk, 1.0)
            
            if normalized_risk > 0:
                risk_level = self._categorize_risk_level(normalized_risk)
                risk_assessment[cancer_type.value] = {
                    "risk_score": normalized_risk,
                    "risk_level": risk_level.value,
                    "contributing_factors": cancer_risk_factors
                }
                
                reasoning_text += f"{cancer_type.value}: risk score {normalized_risk:.2f} ({risk_level.value}). "
        
        assessment_result = {
            "overall_risk_score": min(total_risk_score, 1.0),
            "cancer_specific_risks": risk_assessment,
            "high_risk_cancers": [k for k, v in risk_assessment.items() 
                                 if v["risk_level"] in ["high", "critical"]],
            "recommended_screenings": self._get_screening_recommendations(risk_assessment, patient_data)
        }
        
        # Add to reasoning trace
        self.reasoning_trace.append(ReasoningTrace(
            step=ReasoningStep.RISK_ASSESSMENT,
            input_data=step_input,
            reasoning=reasoning_text,
            output=assessment_result,
            confidence=0.85,
            timestamp=datetime.now()
        ))
        
        return assessment_result
    
    def generate_differential_diagnosis(self, symptoms_analysis: Dict, risk_assessment: Dict) -> Dict[str, Any]:
        """
        Generate differential diagnosis with reasoning
        """
        
        step_input = {"symptoms": symptoms_analysis, "risks": risk_assessment}
        reasoning_text = ""
        
        # Combine symptom-based and risk-based cancer probabilities
        cancer_probabilities = {}
        
        # Weight from symptoms (60% weight)
        symptom_cancers = symptoms_analysis.get("possible_cancer_types", [])
        for cancer in symptom_cancers:
            cancer_probabilities[cancer] = 0.6
            reasoning_text += f"Symptom-based probability for {cancer}: 0.6. "
        
        # Weight from risk factors (40% weight)
        risk_cancers = risk_assessment.get("cancer_specific_risks", {})
        for cancer, risk_data in risk_cancers.items():
            base_prob = cancer_probabilities.get(cancer, 0.0)
            risk_contribution = risk_data["risk_score"] * 0.4
            cancer_probabilities[cancer] = base_prob + risk_contribution
            reasoning_text += f"Added risk-based probability for {cancer}: +{risk_contribution:.2f}. "
        
        # Sort by probability
        sorted_diagnoses = sorted(cancer_probabilities.items(), 
                                key=lambda x: x[1], reverse=True)
        
        # Generate detailed differential diagnosis
        differential_diagnosis = []
        for i, (cancer, probability) in enumerate(sorted_diagnoses[:5]):  # Top 5
            confidence_level = "High" if probability > 0.7 else "Moderate" if probability > 0.4 else "Low"
            
            differential_diagnosis.append({
                "rank": i + 1,
                "cancer_type": cancer,
                "probability": probability,
                "confidence": confidence_level,
                "supporting_evidence": self._get_supporting_evidence(cancer, symptoms_analysis, risk_assessment)
            })
            
            reasoning_text += f"Rank {i+1}: {cancer} with probability {probability:.2f} ({confidence_level} confidence). "
        
        diagnosis_result = {
            "differential_diagnoses": differential_diagnosis,
            "most_likely_diagnosis": sorted_diagnoses[0] if sorted_diagnoses else None,
            "requires_immediate_evaluation": any(prob > 0.8 for _, prob in sorted_diagnoses),
            "recommended_tests": self._recommend_diagnostic_tests(differential_diagnosis)
        }
        
        # Add to reasoning trace
        self.reasoning_trace.append(ReasoningTrace(
            step=ReasoningStep.DIFFERENTIAL_DIAGNOSIS,
            input_data=step_input,
            reasoning=reasoning_text,
            output=diagnosis_result,
            confidence=0.75,
            timestamp=datetime.now()
        ))
        
        return diagnosis_result
    
    def generate_comprehensive_recommendations(self, 
                                            symptoms_analysis: Dict, 
                                            risk_assessment: Dict, 
                                            differential_diagnosis: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive recommendations with reasoning
        """
        
        step_input = {
            "symptoms": symptoms_analysis,
            "risks": risk_assessment,
            "diagnosis": differential_diagnosis
        }
        reasoning_text = ""
        
        recommendations = {
            "immediate_actions": [],
            "diagnostic_tests": [],
            "lifestyle_modifications": [],
            "follow_up_schedule": [],
            "specialist_referrals": [],
            "emergency_signs": []
        }
        
        # Immediate actions based on urgency
        urgency_score = symptoms_analysis.get("urgency_score", 0)
        if urgency_score >= 8:
            recommendations["immediate_actions"].append("Seek immediate medical attention")
            recommendations["emergency_signs"].extend([
                "Severe unexplained pain",
                "Significant bleeding",
                "Difficulty breathing",
                "Loss of consciousness"
            ])
            reasoning_text += f"High urgency score ({urgency_score}) triggers immediate medical attention. "
        elif urgency_score >= 6:
            recommendations["immediate_actions"].append("Schedule appointment with primary care physician within 1-2 weeks")
            reasoning_text += f"Moderate urgency score ({urgency_score}) requires timely medical evaluation. "
        
        # Diagnostic tests based on differential diagnosis
        top_diagnosis = differential_diagnosis.get("most_likely_diagnosis")
        if top_diagnosis:
            cancer_type, probability = top_diagnosis
            test_recommendations = self._get_specific_diagnostic_tests(cancer_type)
            recommendations["diagnostic_tests"].extend(test_recommendations)
            reasoning_text += f"Diagnostic tests for {cancer_type} (probability {probability:.2f}): {test_recommendations}. "
        
        # Specialist referrals
        high_risk_cancers = risk_assessment.get("high_risk_cancers", [])
        for cancer in high_risk_cancers:
            specialist = self._get_specialist_for_cancer(cancer)
            if specialist and specialist not in recommendations["specialist_referrals"]:
                recommendations["specialist_referrals"].append(specialist)
                reasoning_text += f"High risk for {cancer} requires {specialist} referral. "
        
        # Lifestyle modifications
        lifestyle_mods = self._generate_lifestyle_recommendations(risk_assessment)
        recommendations["lifestyle_modifications"].extend(lifestyle_mods)
        reasoning_text += f"Lifestyle modifications based on risk factors: {lifestyle_mods}. "
        
        # Follow-up schedule
        follow_up = self._generate_follow_up_schedule(symptoms_analysis, risk_assessment)
        recommendations["follow_up_schedule"] = follow_up
        reasoning_text += f"Follow-up schedule: {follow_up}. "
        
        # Add reasoning trace
        self.reasoning_trace.append(ReasoningTrace(
            step=ReasoningStep.RECOMMENDATION_GENERATION,
            input_data=step_input,
            reasoning=reasoning_text,
            output=recommendations,
            confidence=0.9,
            timestamp=datetime.now()
        ))
        
        return recommendations
    
    def generate_llm_enhanced_response(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate human-readable response using LLM with reasoning context
        """
        
        # Compile reasoning trace for context
        reasoning_context = self._compile_reasoning_context()
        
        # Create comprehensive prompt with reasoning trace
        system_prompt = self._get_cancer_specialist_prompt()
        
        user_prompt = f"""
        Based on the following comprehensive analysis and reasoning trace, provide a detailed medical consultation response:

        REASONING TRACE:
        {reasoning_context}

        ANALYSIS RESULTS:
        {json.dumps(analysis_results, indent=2)}

        Please provide:
        1. Clear explanation of findings
        2. Risk assessment with reasoning
        3. Recommended next steps
        4. When to seek immediate care
        5. Preventive measures

        Respond in {"Bengali" if self.language == "bn" else "English"} with empathy and clarity.
        """
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.reasoning_model,
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating LLM response: {e}")
            if self.language == "bn":
                return "দুঃখিত, বিশ্লেষণ তৈরি করতে একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
            else:
                return "Sorry, there was an error generating the analysis. Please try again."
    
    def get_reasoning_explanation(self) -> Dict[str, Any]:
        """
        Get detailed explanation of the reasoning process
        """
        
        explanation = {
            "reasoning_steps": len(self.reasoning_trace),
            "confidence_scores": [trace.confidence for trace in self.reasoning_trace],
            "step_details": []
        }
        
        for trace in self.reasoning_trace:
            step_detail = {
                "step": trace.step.value,
                "reasoning": trace.reasoning,
                "confidence": trace.confidence,
                "timestamp": trace.timestamp.isoformat()
            }
            explanation["step_details"].append(step_detail)
        
        explanation["overall_confidence"] = sum(explanation["confidence_scores"]) / len(explanation["confidence_scores"]) if explanation["confidence_scores"] else 0
        
        return explanation
    
    # Helper methods
    def _symptom_mentioned(self, symptom_key: str, description: str) -> bool:
        """Check if symptom is mentioned in description"""
        # Simple keyword matching - can be enhanced with NLP
        symptom_keywords = {
            "persistent_cough": ["cough", "coughing", "কাশি"],
            "breast_lump": ["breast lump", "breast mass", "স্তনে গাঁট"],
            "blood_in_stool": ["blood in stool", "bloody stool", "মলে রক্ত"],
            "unexplained_weight_loss": ["weight loss", "losing weight", "ওজন কমা"],
            "persistent_fatigue": ["fatigue", "tired", "weakness", "ক্লান্তি"],
            "unusual_bleeding": ["bleeding", "blood", "রক্তপাত"],
            "skin_changes": ["skin changes", "mole", "ত্বকের পরিবর্তন"]
        }
        
        keywords = symptom_keywords.get(symptom_key, [])
        return any(keyword.lower() in description.lower() for keyword in keywords)
    
    def _risk_factor_present(self, risk_key: str, patient_data: Dict) -> bool:
        """Check if risk factor is present in patient data"""
        risk_mappings = {
            "smoking": patient_data.get("smoking", False),
            "family_history": patient_data.get("family_history_cancer", False),
            "age_over_50": patient_data.get("age", 0) > 50,
            "alcohol_consumption": patient_data.get("heavy_drinking", False),
            "hpv_infection": patient_data.get("hpv_positive", False),
            "sun_exposure": patient_data.get("excessive_sun_exposure", False)
        }
        
        return risk_mappings.get(risk_key, False)
    
    def _categorize_risk_level(self, risk_score: float) -> RiskLevel:
        """Categorize numerical risk score into risk level"""
        if risk_score >= 0.8:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.6:
            return RiskLevel.HIGH
        elif risk_score >= 0.3:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
    
    def _get_possible_cancer_types(self, symptoms: List[CancerSymptom]) -> List[CancerType]:
        """Extract possible cancer types from symptoms"""
        cancer_types = set()
        for symptom in symptoms:
            cancer_types.update(symptom.cancer_types)
        return list(cancer_types)
    
    def _get_screening_recommendations(self, risk_assessment: Dict, patient_data: Dict) -> List[str]:
        """Generate screening recommendations based on risk"""
        recommendations = []
        age = patient_data.get("age", 0)
        
        for cancer_type_str, risk_data in risk_assessment.items():
            try:
                cancer_type = CancerType(cancer_type_str)
                if cancer_type in self.knowledge_base.screening_guidelines:
                    guidelines = self.knowledge_base.screening_guidelines[cancer_type]
                    
                    start_age = guidelines.get("high_risk_start" if risk_data["risk_level"] == "high" else "age_start", guidelines["age_start"])
                    
                    if age >= start_age:
                        method = guidelines["method"]
                        frequency = guidelines["frequency"]
                        recommendations.append(f"{cancer_type.value.replace('_', ' ').title()}: {method} {frequency}")
                        
            except ValueError:
                continue
        
        return recommendations
    
    def _get_supporting_evidence(self, cancer_type: str, symptoms_analysis: Dict, risk_assessment: Dict) -> List[str]:
        """Get supporting evidence for a cancer type"""
        evidence = []
        
        # Evidence from symptoms
        if cancer_type in symptoms_analysis.get("possible_cancer_types", []):
            evidence.append("Symptom pattern consistent with this cancer type")
        
        # Evidence from risk factors
        if cancer_type in risk_assessment.get("cancer_specific_risks", {}):
            risk_data = risk_assessment["cancer_specific_risks"][cancer_type]
            evidence.extend([f"Risk factor: {factor}" for factor in risk_data["contributing_factors"]])
        
        return evidence
    
    def _recommend_diagnostic_tests(self, differential_diagnoses: List[Dict]) -> List[str]:
        """Recommend diagnostic tests based on differential diagnoses"""
        tests = set()
        
        for diagnosis in differential_diagnoses[:3]:  # Top 3 diagnoses
            cancer_type = diagnosis["cancer_type"]
            cancer_tests = self._get_specific_diagnostic_tests(cancer_type)
            tests.update(cancer_tests)
        
        return list(tests)
    
    def _get_specific_diagnostic_tests(self, cancer_type: str) -> List[str]:
        """Get specific diagnostic tests for a cancer type"""
        test_mapping = {
            "breast_cancer": ["Mammography", "Breast MRI", "Biopsy", "Ultrasound"],
            "lung_cancer": ["Chest CT scan", "PET scan", "Bronchoscopy", "Sputum cytology"],
            "colorectal_cancer": ["Colonoscopy", "CEA blood test", "CT scan", "FIT test"],
            "prostate_cancer": ["PSA blood test", "Digital rectal exam", "Prostate MRI", "Biopsy"],
            "cervical_cancer": ["Pap smear", "HPV test", "Colposcopy", "Cervical biopsy"],
            "liver_cancer": ["Liver ultrasound", "CT scan", "MRI", "Alpha-fetoprotein test"],
            "stomach_cancer": ["Upper endoscopy", "CT scan", "Barium swallow", "H. pylori test"],
            "skin_cancer": ["Dermoscopy", "Skin biopsy", "Full body skin exam"],
            "blood_cancer": ["Complete blood count", "Bone marrow biopsy", "Flow cytometry", "Genetic tests"]
        }
        
        return test_mapping.get(cancer_type, ["General blood tests", "Imaging studies"])
    
    def _get_specialist_for_cancer(self, cancer_type: str) -> str:
        """Get appropriate specialist for cancer type"""
        specialist_mapping = {
            "breast_cancer": "Oncologist or Breast Surgeon",
            "lung_cancer": "Pulmonologist or Thoracic Oncologist",
            "colorectal_cancer": "Gastroenterologist or Colorectal Surgeon",
            "prostate_cancer": "Urologist or Urologic Oncologist",
            "cervical_cancer": "Gynecologic Oncologist",
            "liver_cancer": "Hepatologist or Liver Surgeon",
            "stomach_cancer": "Gastroenterologist or Surgical Oncologist",
            "skin_cancer": "Dermatologist or Dermatologic Surgeon",
            "blood_cancer": "Hematologist or Hematologic Oncologist"
        }
        
        return specialist_mapping.get(cancer_type, "Oncologist")
    
    def _generate_lifestyle_recommendations(self, risk_assessment: Dict) -> List[str]:
        """Generate lifestyle recommendations based on risk factors"""
        recommendations = []
        
        # General cancer prevention
        recommendations.extend([
            "Maintain a healthy diet rich in fruits and vegetables",
            "Exercise regularly (at least 150 minutes per week)",
            "Maintain a healthy weight",
            "Limit alcohol consumption",
            "Avoid tobacco products",
            "Protect skin from excessive sun exposure",
            "Get recommended cancer screenings"
        ])
        
        return recommendations
    
    def _generate_follow_up_schedule(self, symptoms_analysis: Dict, risk_assessment: Dict) -> List[str]:
        """Generate follow-up schedule"""
        urgency_score = symptoms_analysis.get("urgency_score", 0)
        high_risk_cancers = risk_assessment.get("high_risk_cancers", [])
        
        if urgency_score >= 8:
            return ["Immediate medical evaluation", "Follow-up within 1 week after initial consultation"]
        elif urgency_score >= 6 or high_risk_cancers:
            return ["Medical evaluation within 1-2 weeks", "Follow-up in 1 month", "Regular monitoring every 3-6 months"]
        else:
            return ["Routine check-up in 3-6 months", "Annual comprehensive health screening"]
    
    def _compile_reasoning_context(self) -> str:
        """Compile reasoning trace into readable context"""
        context = "REASONING PROCESS:\n\n"
        
        for i, trace in enumerate(self.reasoning_trace, 1):
            context += f"Step {i}: {trace.step.value.replace('_', ' ').title()}\n"
            context += f"Reasoning: {trace.reasoning}\n"
            context += f"Confidence: {trace.confidence:.2f}\n\n"
        
        return context
    
    def _get_cancer_specialist_prompt(self) -> str:
        """Get specialized system prompt for cancer domain"""
        
        if self.language == "bn":
            return """আপনি একজন অভিজ্ঞ ক্যান্সার বিশেষজ্ঞ এবং অনকোলজিস্ট যিনি রোগীদের সাথে বাংলায় কথা বলেন। 
            আপনার কাজ হল:

            ১. ক্যান্সারের লক্ষণ ও ঝুঁকির কারণগুলি বিশ্লেষণ করা
            ২. যুক্তিযুক্ত চিকিৎসা পরামর্শ প্রদান করা
            ৩. রোগীকে সঠিক পরীক্ষা ও চিকিৎসার দিকনির্দেশনা দেওয়া
            ৪. জরুরি অবস্থা চিহ্নিত করা এবং তাৎক্ষণিক ব্যবস্থার পরামর্শ দেওয়া

            সর্বদা:
            - সহানুভূতিশীল ও স্পষ্ট ভাষা ব্যবহার করুন
            - বৈজ্ঞানিক তথ্যের উপর ভিত্তি করে পরামর্শ দিন
            - রোগীর মানসিক অবস্থার যত্ন নিন
            - প্রয়োজনে বিশেষজ্ঞ চিকিৎসকের কাছে পাঠানোর পরামর্শ দিন

            গুরুত্বপূর্ণ: সর্বদা উল্লেখ করুন যে এটি প্রাথমিক মূল্যায়ন এবং চূড়ান্ত রোগ নির্ণয়ের জন্য একজন যোগ্য অনকোলজিস্টের পরামর্শ প্রয়োজন।"""
        
        else:
            return """You are an experienced cancer specialist and oncologist providing medical consultations. 
            Your role is to:

            1. Analyze cancer symptoms and risk factors with clinical reasoning
            2. Provide evidence-based medical guidance and recommendations
            3. Guide patients toward appropriate diagnostic tests and treatments
            4. Identify emergency situations requiring immediate medical attention

            Always:
            - Use empathetic and clear language
            - Base recommendations on current medical evidence
            - Consider the patient's emotional well-being
            - Recommend specialist referrals when appropriate
            - Explain your reasoning process clearly

            Important: Always emphasize that this is a preliminary assessment and professional oncological consultation is needed for definitive diagnosis and treatment planning.

            Provide comprehensive analysis including:
            - Symptom assessment with reasoning
            - Risk factor evaluation
            - Differential diagnosis considerations
            - Recommended diagnostic approach
            - Next steps and follow-up care
            - When to seek immediate medical attention"""
    
    def reset_reasoning_trace(self):
        """Reset the reasoning trace for new consultation"""
        self.reasoning_trace = []
    
    def export_reasoning_trace(self) -> Dict[str, Any]:
        """Export reasoning trace for analysis or debugging"""
        return {
            "trace_length": len(self.reasoning_trace),
            "language": self.language,
            "timestamp": datetime.now().isoformat(),
            "steps": [
                {
                    "step": trace.step.value,
                    "reasoning": trace.reasoning,
                    "confidence": trace.confidence,
                    "timestamp": trace.timestamp.isoformat(),
                    "input_keys": list(trace.input_data.keys()),
                    "output_keys": list(trace.output.keys())
                }
                for trace in self.reasoning_trace
            ]
        }