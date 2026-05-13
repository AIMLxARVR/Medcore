import pytest
from unittest.mock import patch
from src.cancer.cancer_reasoning_engine import CancerReasoningEngine, CancerType, RiskLevel

# Fixture to initialize the engine with a mocked client
@pytest.fixture
def engine():
    with patch('src.cancer.cancer_reasoning_engine.Groq') as mock_groq:
        engine = CancerReasoningEngine()
        yield engine

# Test symptom analysis for a clear high-risk symptom
def test_analyze_symptoms_high_risk(engine):
    symptoms_data = {"description": "I have a breast lump", "severity": 8, "duration": "2 months"}
    analysis = engine.analyze_symptoms(symptoms_data)

    assert "Breast Lump" in analysis["identified_symptoms"]
    assert analysis["urgency_score"] >= 7  # High urgency for breast lump
    assert "breast_cancer" in analysis["possible_cancer_types"]

# Test risk factor assessment for a heavy smoker
def test_assess_risk_factors_smoker(engine):
    patient_data = {"age": 60, "smoking": True}
    assessment = engine.assess_risk_factors(patient_data)

    assert "lung_cancer" in assessment["high_risk_cancers"]
    lung_risk = assessment["cancer_specific_risks"]["lung_cancer"]
    assert lung_risk["risk_level"] in ["high", "critical"]
    assert "Smoking" in lung_risk["contributing_factors"]

# Test a low-risk scenario with no significant symptoms or risk factors
def test_low_risk_scenario(engine):
    symptoms_data = {"description": "I feel generally well, just a little tired."}
    patient_data = {"age": 30, "smoking": False, "family_history_cancer": False}

    symptoms_analysis = engine.analyze_symptoms(symptoms_data)
    risk_assessment = engine.assess_risk_factors(patient_data)

    assert not symptoms_analysis["requires_immediate_attention"]
    assert not risk_assessment["high_risk_cancers"]

# Test differential diagnosis generation
def test_generate_differential_diagnosis(engine):
    symptoms_analysis = {
        "possible_cancer_types": ["lung_cancer", "stomach_cancer"],
        "urgency_score": 7
    }
    risk_assessment = {
        "cancer_specific_risks": {
            "lung_cancer": {"risk_score": 0.9, "contributing_factors": ["Smoking"]},
            "stomach_cancer": {"risk_score": 0.2, "contributing_factors": []}
        }
    }

    diagnosis = engine.generate_differential_diagnosis(symptoms_analysis, risk_assessment)

    assert diagnosis["most_likely_diagnosis"][0] == "lung_cancer"
    assert len(diagnosis["differential_diagnoses"]) > 0
    assert diagnosis["differential_diagnoses"][0]["probability"] > diagnosis["differential_diagnoses"][1]["probability"]

# Test LLM-enhanced response generation
def test_generate_llm_enhanced_response(engine):
    with patch.object(engine.client.chat.completions, 'create') as mock_create:
        mock_response = "This is a detailed AI-generated medical consultation."
        mock_create.return_value.choices = [type('Choice', (), {'message': type('Message', (), {'content': mock_response})})()]

        analysis_results = {"final_summary": "High risk of lung cancer detected."}
        response = engine.generate_llm_enhanced_response(analysis_results)

        mock_create.assert_called_once()
        assert response == mock_response
