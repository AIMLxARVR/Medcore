import React, { useState } from 'react';
import { C } from '../../constants/colors';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { aiApi, ApiError } from '../../services/api';
import { sanitizeInput } from '../../utils/inputSanitizer';

// Define analysis result type from backend
interface AnalysisResult {
  conditions: Array<{ name: string; confidence: number; icd: string }>;
  tests: string[];
  urgency: 'low' | 'medium' | 'high';
  recommendation: string;
}

function AiClinicalView({ onNav }: { onNav: (view: string) => void }) {
  const [symptoms, setSymptoms] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!symptoms.trim()) return;
    
    // Sanitize input for security
    const sanitizedSymptoms = sanitizeInput(symptoms);
    
    setLoading(true);
    setError(null);
    
    try {
      // Call backend AI API for symptom analysis
      const result = await aiApi.analyzeSymptoms(sanitizedSymptoms);
      setAnalysis(result);
    } catch (e) {
      const errorMessage = e instanceof ApiError 
        ? e.message 
        : 'Failed to analyze symptoms. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const clearAnalysis = () => {
    setAnalysis(null);
    setSymptoms('');
    setError(null);
  };

  // Urgency color mapping
  const urgencyColors = {
    high: { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24' },
    medium: { bg: '#fff3cd', border: '#ffeaa7', text: '#856404' },
    low: { bg: '#d1edff', border: '#b8daff', text: '#004085' }
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
          {error && (
            <Card style={{ padding: 24, backgroundColor: '#f8d7da', borderColor: '#f5c6cb' }}>
              <div style={{ fontSize: 14, color: '#721c24' }}>
                Error: {error}
              </div>
            </Card>
          )}

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
                backgroundColor: urgencyColors[analysis.urgency].bg,
                borderColor: urgencyColors[analysis.urgency].border
              }}>
                <div style={{ 
                  fontSize: 16, 
                  fontWeight: 600, 
                  color: urgencyColors[analysis.urgency].text
                }}>
                  Urgency Level: {analysis.urgency.charAt(0).toUpperCase() + analysis.urgency.slice(1)}
                </div>
              </Card>

              {/* Possible Conditions */}
              <Card style={{ padding: 24, marginBottom: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>
                  Possible Conditions
                </h3>
                {analysis.conditions.map((condition, index) => (
                  <div key={index} style={{ marginBottom: 12, padding: 12, backgroundColor: '#f8f9fa', borderRadius: 8 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>
                        {condition.name}
                      </div>
                      <div style={{ fontSize: 12, color: C.muted }}>
                        ICD-10: {condition.icd}
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
                        width: `${condition.confidence}%`, 
                        height: '100%', 
                        backgroundColor: condition.confidence > 70 ? '#28a745' : 
                                         condition.confidence > 50 ? '#ffc107' : '#6c757d',
                        borderRadius: 2 
                      }}></div>
                    </div>
                    <div style={{ fontSize: 12, color: C.muted, marginTop: 4 }}>
                      {condition.confidence}% confidence
                    </div>
                  </div>
                ))}
              </Card>

              {/* Recommended Tests */}
              <Card style={{ padding: 24, marginBottom: 16 }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>
                  Recommended Tests
                </h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {analysis.tests.map((test, index) => (
                    <span key={index} style={{ 
                      padding: '4px 12px', 
                      backgroundColor: C.primaryLight, 
                      borderRadius: 16,
                      fontSize: 12,
                      color: C.primaryMid
                    }}>
                      {test}
                    </span>
                  ))}
                </div>
              </Card>

              {/* Recommendation */}
              <Card style={{ padding: 24, marginBottom: 16, backgroundColor: C.primaryLight }}>
                <h3 style={{ fontSize: 16, fontWeight: 600, color: C.primary, marginBottom: 8 }}>
                  Clinical Recommendation
                </h3>
                <p style={{ fontSize: 14, color: C.text, lineHeight: 1.6 }}>
                  {analysis.recommendation}
                </p>
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

          {!analysis && !loading && !error && (
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
