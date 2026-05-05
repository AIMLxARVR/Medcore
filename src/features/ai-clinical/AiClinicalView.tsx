import React, { useState } from 'react';
import { C } from '../../constants/colors';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

// Define analysis result type
interface AnalysisResult {
  possibleConditions: Array<{ condition: string; probability: number; severity: string }>;
  recommendations: string[];
  urgency: string;
}

function AiClinicalView({ onNav }: { onNav: (view: string) => void }) {
  const [symptoms, setSymptoms] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!symptoms.trim()) return;
    
    setLoading(true);
    // Simulate AI analysis
    setTimeout(() => {
      setAnalysis({
        possibleConditions: [
          { condition: 'Common Cold', probability: 0.7, severity: 'mild' },
          { condition: 'Flu', probability: 0.4, severity: 'moderate' },
          { condition: 'Allergies', probability: 0.3, severity: 'mild' }
        ],
        recommendations: [
          'Rest and stay hydrated',
          'Monitor symptoms for 2-3 days',
          'Consider over-the-counter medication for symptom relief',
          'Seek medical attention if symptoms worsen'
        ],
        urgency: 'low'
      });
      setLoading(false);
    }, 2000);
  };

  const clearAnalysis = () => {
    setAnalysis(null);
    setSymptoms('');
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '16px 12px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800, color: C.text }}>AI Clinical Assistant</h1>
        <Button onClick={() => onNav('home')} variant="outline">Back to Home</Button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Input Section */}
        <div>
          <Card style={{ padding: 24 }}>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text, marginBottom: 16 }}>
              Describe Your Symptoms
            </h2>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="Please describe your symptoms in detail... Include information such as:
- When symptoms started
- Severity and duration
- Any triggers or patterns
- Related symptoms
- Previous medical history"
              rows={10}
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none',
                resize: 'vertical',
                minHeight: 200
              }}
              onFocus={(e) => e.target.style.borderColor = C.primary}
              onBlur={(e) => e.target.style.borderColor = C.border}
            />
            <div style={{ display: 'flex', gap: 12, marginTop: 16 }}>
              <Button 
                onClick={handleAnalyze}
                disabled={loading || !symptoms.trim()}
                style={{ flex: 1 }}
              >
                {loading ? 'Analyzing...' : 'Analyze Symptoms'}
              </Button>
              {analysis && (
                <Button onClick={clearAnalysis} variant="outline">
                  Clear
                </Button>
              )}
            </div>
          </Card>

          {/* Disclaimer */}
          <Card style={{ padding: 16, marginTop: 16, backgroundColor: '#fff3cd', borderColor: '#ffeaa7' }}>
            <div style={{ fontSize: 12, color: '#856404' }}>
              <strong>Important:</strong> This AI analysis is for informational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment.
            </div>
          </Card>
        </div>

        {/* Results Section */}
        <div>
          {loading && (
            <Card style={{ padding: 24, textAlign: 'center' }}>
              <div style={{ fontSize: 16, color: C.muted, marginBottom: 16 }}>
                AI is analyzing your symptoms...
              </div>
              <div style={{ 
                width: 40, 
                height: 40, 
                border: `3px solid ${C.primary}`, 
                borderTop: '3px solid transparent',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                margin: '0 auto'
              }}></div>
            </Card>
          )}

          {analysis && !loading && (
            <div>
              {/* Urgency Level */}
              <Card style={{ 
                padding: 16, 
                marginBottom: 16,
                backgroundColor: analysis.urgency === 'high' ? '#f8d7da' : 
                               analysis.urgency === 'medium' ? '#fff3cd' : '#d1edff',
                borderColor: analysis.urgency === 'high' ? '#f5c6cb' : 
                            analysis.urgency === 'medium' ? '#ffeaa7' : '#b8daff'
              }}>
                <div style={{ 
                  fontSize: 16, 
                  fontWeight: 600, 
                  color: analysis.urgency === 'high' ? '#721c24' : 
                         analysis.urgency === 'medium' ? '#856404' : '#004085'
                }}>
                  Urgency Level: {analysis.urgency.charAt(0).toUpperCase() + analysis.urgency.slice(1)}
                </div>
              </Card>

              {/* Possible Conditions */}
              <Card style={{ padding: 24, marginBottom: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>
                  Possible Conditions
                </h3>
                {analysis.possibleConditions.map((condition, index) => (
                  <div key={index} style={{ marginBottom: 12, padding: 12, backgroundColor: '#f8f9fa', borderRadius: 8 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>
                        {condition.condition}
                      </div>
                      <div style={{ fontSize: 12, color: C.muted }}>
                        {Math.round(condition.probability * 100)}% probability
                      </div>
                    </div>
                    <div style={{ 
                      width: '100%', 
                      height: 4, 
                      backgroundColor: C.border, 
                      borderRadius: 2, 
                      marginTop: 8 
                    }}>
                      <div style={{ 
                        width: `${condition.probability * 100}%`, 
                        height: '100%', 
                        backgroundColor: condition.severity === 'severe' ? '#dc3545' : 
                                         condition.severity === 'moderate' ? '#ffc107' : '#28a745',
                        borderRadius: 2 
                      }}></div>
                    </div>
                  </div>
                ))}
              </Card>

              {/* Recommendations */}
              <Card style={{ padding: 24, marginBottom: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>
                  Recommendations
                </h3>
                {analysis.recommendations.map((rec, index) => (
                  <div key={index} style={{ 
                    display: 'flex', 
                    alignItems: 'flex-start', 
                    marginBottom: 8,
                    padding: 8,
                    backgroundColor: '#f8f9fa',
                    borderRadius: 6
                  }}>
                    <div style={{ 
                      width: 6, 
                      height: 6, 
                      backgroundColor: C.primary, 
                      borderRadius: '50%', 
                      marginTop: 8, 
                      marginRight: 12,
                      flexShrink: 0
                    }}></div>
                    <div style={{ fontSize: 14, color: C.text }}>{rec}</div>
                  </div>
                ))}
              </Card>

              {/* Action Buttons */}
              <div style={{ display: 'flex', gap: 12 }}>
                <Button onClick={() => onNav('doctors')} style={{ flex: 1 }}>
                  Find a Doctor
                </Button>
                <Button onClick={() => onNav('chatbot')} variant="outline" style={{ flex: 1 }}>
                  Chat with Assistant
                </Button>
              </div>
            </div>
          )}

          {!analysis && !loading && (
            <Card style={{ padding: 24, textAlign: 'center' }}>
              <div style={{ fontSize: 16, color: C.muted }}>
                Enter your symptoms to get AI-powered analysis and recommendations.
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

export default AiClinicalView;