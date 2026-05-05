/**
 * AI Routes
 * Handles AI-powered endpoints: chat, symptom analysis, lab report analysis, prescription check
 * This is a critical security improvement - moves API calls from frontend to backend
 */

const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const { PrismaClient } = require('@prisma/client');
const { authenticate } = require('../middleware/auth');

const prisma = new PrismaClient();

// MedBot system prompt - should be in environment variable in production
const MEDBOT_SYSTEM = process.env.MEDBOT_SYSTEM || `You are MedBot, the AI assistant for MedCore Diagnostic Centre in Dhaka, Bangladesh. Be concise, warm, and helpful. Use plain text only (no markdown, no asterisks, no headers) - format with line breaks, bullet points (•), and emojis only.

CLINIC DATA (answer questions using this):
Doctors: 1) Dr. Fatima Rahman – Cardiologist, MBBS MD, fee ৳1500, today 3:00PM/3:30PM/5:00PM/5:30PM | 2) Dr. Ahmed Hossain – Neurologist, MBBS MD, fee ৳2000, tomorrow 10:00AM/10:30AM/11:00AM/2:00PM | 3) Dr. Nasrin Khatun – Pediatrician, MBBS DCH, fee ৳1200, today 5:00PM/5:30PM/6:00PM | 4) Dr. Karim Uddin – Orthopedist, MBBS MS, fee ৳1800, Thu 11:00AM/11:30AM/2:30PM/3:00PM | 5) Dr. Sultana Begum – Dermatologist, MBBS DDV, fee ৳1500, today 6:00PM/6:30PM/7:00PM
Patient on record: Farhan Ahmed, PAT-00142, blood group B+
Appointment on record: APT-2847, Dr. Fatima Rahman, May 8 2026 3:00PM, Serial #7, Chamber 2B, Status: Confirmed
Recent reports: CBC (Apr 28, flagged: Low Hb 11.2 g/dL, High WBC 11800), ECG (Apr 15), Chest X-Ray (Mar 20)
Emergency: Call 999. Hotline: 01700-000000. Address: House 7, Road 12, Dhanmondi, Dhaka.

RULES:
• When user says yes/no or picks a number (1,2,3 etc), understand it in context of your last question
• For appointments: confirm doctor, date, time, then ask for name & phone to complete
• For symptoms: give brief guidance, suggest relevant doctor, ask if they want to book
• For cancellation: ask "yes" to confirm, warn about ৳500 fee if <24h
• Keep responses under 120 words
• Always end with a clear next action or question when the conversation is ongoing
• NEVER say you cannot help — always guide them to the right option`;

// Check for API key
const getApiKey = () => {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY not configured');
  }
  return apiKey;
};

// POST /api/ai/chat - Proxy to Anthropic API (SECURE - requires authentication)
router.post('/chat', authenticate, async (req, res) => {
  try {
    const { message, history } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }
    
    // Build message history for Claude
    const messages = [];
    
    // Add previous messages if provided
    if (history && Array.isArray(history)) {
      history.forEach(msg => {
        if (msg.role && msg.content) {
          messages.push({ role: msg.role, content: msg.content });
        }
      });
    }
    
    // Add the new user message
    messages.push({ role: 'user', content: message });
    
    // Call Anthropic API from backend (API key never exposed to client)
    const apiKey = getApiKey();
    
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 200,
        system: MEDBOT_SYSTEM,
        messages: messages
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Anthropic API error:', response.status, errorData);
      throw new Error('AI service temporarily unavailable');
    }
    
    const data = await response.json();
    
    const replyText = data.content
      ?.map(b => b.type === 'text' ? b.text : '')
      .join('') || 'Sorry, I couldn\'t process that. Please try again.';
    
    // Return the response and updated history
    const updatedHistory = [
      ...messages,
      { role: 'assistant', content: replyText }
    ];
    
    res.json({
      reply: replyText,
      history: updatedHistory
    });
  } catch (error) {
    console.error('AI chat error:', error);
    
    if (error.message === 'ANTHROPIC_API_KEY not configured') {
      return res.status(503).json({ error: 'AI service not configured' });
    }
    
    res.status(500).json({ error: 'Failed to get AI response' });
  }
});

// GET /api/ai/doctors - Get available doctors for AI context
router.get('/doctors', authenticate, async (req, res) => {
  try {
    const doctors = await prisma.doctorProfile.findMany({
      where: { isActive: true },
      include: {
        user: {
          select: {
            firstName: true,
            lastName: true,
            email: true
          }
        },
        specialization: true
      }
    });
    
    const formattedDoctors = doctors.map(d => ({
      id: d.id,
      name: `Dr. ${d.user.firstName} ${d.user.lastName}`,
      specialization: d.specialization?.name || 'General',
      consultationFee: d.consultationFee,
      availableDays: d.availableDays,
      availableTimeSlots: d.availableTimeSlots
    }));
    
    res.json(formattedDoctors);
  } catch (error) {
    console.error('Get doctors error:', error);
    res.status(500).json({ error: 'Failed to get doctors' });
  }
});

// POST /api/ai/analyze-symptoms - Symptom analysis endpoint
router.post('/analyze-symptoms', authenticate, async (req, res) => {
  try {
    const { symptoms } = req.body;
    
    if (!symptoms) {
      return res.status(400).json({ error: 'Symptoms are required' });
    }
    
    // Simple rule-based analysis (in production, use more sophisticated AI)
    const symptomLower = symptoms.toLowerCase();
    let analysis = null;
    
    if (symptomLower.includes('chest pain') || symptomLower.includes('shortness of breath')) {
      analysis = {
        conditions: [
          { name: 'Angina Pectoris', confidence: 78, icd: 'I20' },
          { name: 'Acute MI (rule out)', confidence: 62, icd: 'I21' },
          { name: 'Costochondritis', confidence: 41, icd: 'M94.0' }
        ],
        tests: ['ECG', 'Troponin I/T', 'Chest X-Ray', 'CBC'],
        urgency: 'high',
        recommendation: 'Refer to cardiology. ECG immediately.'
      };
    } else if (symptomLower.includes('fever') || symptomLower.includes('cough') || symptomLower.includes('fatigue')) {
      analysis = {
        conditions: [
          { name: 'Viral URI', confidence: 85, icd: 'J06.9' },
          { name: 'Influenza', confidence: 72, icd: 'J11' },
          { name: 'COVID-19', confidence: 55, icd: 'U07.1' }
        ],
        tests: ['CBC', 'CRP', 'COVID Antigen', 'Chest X-Ray'],
        urgency: 'medium',
        recommendation: 'Symptomatic management. Isolate if COVID suspected.'
      };
    } else if (symptomLower.includes('headache') || symptomLower.includes('dizziness') || symptomLower.includes('nausea')) {
      analysis = {
        conditions: [
          { name: 'Migraine', confidence: 82, icd: 'G43' },
          { name: 'Tension Headache', confidence: 68, icd: 'G44.2' },
          { name: 'Hypertension', confidence: 45, icd: 'I10' }
        ],
        tests: ['BP monitoring', 'CBC', 'Blood glucose'],
        urgency: 'low',
        recommendation: 'Analgesics PRN. Monitor BP. Neuro referral if recurrent.'
      };
    } else if (symptomLower.includes('joint pain') || symptomLower.includes('swelling')) {
      analysis = {
        conditions: [
          { name: 'Rheumatoid Arthritis', confidence: 71, icd: 'M06' },
          { name: 'Osteoarthritis', confidence: 65, icd: 'M19' },
          { name: 'Gout', confidence: 48, icd: 'M10' }
        ],
        tests: ['ESR', 'CRP', 'RF', 'Uric Acid', 'X-Ray joints'],
        urgency: 'medium',
        recommendation: 'NSAIDs. Rheumatology referral recommended.'
      };
    } else {
      analysis = {
        conditions: [
          { name: 'Unspecified Condition', confidence: 35, icd: 'R69' }
        ],
        tests: ['CBC', 'CMP', 'Urinalysis'],
        urgency: 'low',
        recommendation: 'Full clinical workup recommended.'
      };
    }
    
    // Log the analysis for audit
    await prisma.aiAnalysisLog.create({
      data: {
        userId: req.user.id,
        type: 'SYMPTOMS',
        input: symptoms,
        output: JSON.stringify(analysis),
        timestamp: new Date()
      }
    });
    
    res.json(analysis);
  } catch (error) {
    console.error('Analyze symptoms error:', error);
    res.status(500).json({ error: 'Failed to analyze symptoms' });
  }
});

// POST /api/ai/analyze-lab-report - Lab report analysis
router.post('/analyze-lab-report', authenticate, async (req, res) => {
  try {
    const { reportType, values } = req.body;
    
    if (!reportType || !values) {
      return res.status(400).json({ error: 'Report type and values are required' });
    }
    
    let analysis = null;
    let interpretation = '';
    
    if (reportType === 'CBC') {
      const hb = values.find(v => v.param === 'Hemoglobin')?.val;
      const wbc = values.find(v => v.param === 'WBC')?.val;
      
      if (hb && hb < 12) {
        analysis = { status: 'abnormal', flag: 'Low Hemoglobin' };
        interpretation = 'Findings suggest anemia. Differential: iron deficiency vs. infection. Recommend serum ferritin, TIBC.";
      } else if (wbc && wbc > 11000) {
        analysis = { status: 'abnormal', flag: 'Elevated WBC' };
        interpretation = 'Leukocytosis suggests infection or inflammation.';
      } else {
        analysis = { status: 'normal' };
        interpretation = 'CBC values within normal limits.';
      }
    } else if (reportType === 'Lipid Panel') {
      const ldl = values.find(v => v.param === 'LDL')?.val;
      const hdl = values.find(v => v.param === 'HDL')?.val;
      
      if (ldl && ldl > 130) {
        analysis = { status: 'abnormal', flag: 'Elevated LDL' };
        interpretation = 'Dyslipidemia with elevated LDL. Consider lifestyle modification + statin therapy.';
      } else if (hdl && hdl < 40) {
        analysis = { status: 'abnormal', flag: 'Low HDL' };
        interpretation = 'Low HDL is an independent cardiac risk factor.';
      } else {
        analysis = { status: 'normal' };
        interpretation = 'Lipid profile within target ranges.';
      }
    } else {
      analysis = { status: 'unknown' };
      interpretation = 'Report type not recognized for analysis.';
    }
    
    // Log the analysis
    await prisma.aiAnalysisLog.create({
      data: {
        userId: req.user.id,
        type: 'LAB_REPORT',
        input: `${reportType}: ${JSON.stringify(values)}`,
        output: JSON.stringify(analysis),
        timestamp: new Date()
      }
    });
    
    res.json({
      reportType,
      analysis,
      interpretation
    });
  } catch (error) {
    console.error('Analyze lab report error:', error);
    res.status(500).json({ error: 'Failed to analyze lab report' });
  }
});

// POST /api/ai/check-prescription - Drug interaction check
router.post('/check-prescription', authenticate, async (req, res) => {
  try {
    const { medications } = req.body;
    
    if (!medications || !Array.isArray(medications)) {
      return res.status(400).json({ error: 'Medications array is required' });
    }
    
    // Simple drug interaction check (in production, use a drug database API)
    const interactions = [];
    const warnings = [];
    
    const medNames = medications.map(m => m.toLowerCase());
    
    // Check for common interactions
    if (medNames.some(m => m.includes('aspirin')) && medNames.some(m => m.includes('warfarin'))) {
      interactions.push({
        drugs: 'Aspirin + Warfarin',
        severity: 'high',
        note: 'Increased bleeding risk - monitor INR closely'
      });
    }
    
    if (medNames.some(m => m.includes('metformin')) && medNames.some(m => m.includes('contrast'))) {
      warnings.push({
        note: 'Hold Metformin 48h before/after contrast procedures'
      });
    }
    
    // Check for common dosage warnings
    if (medNames.some(m => m.includes('metformin') && m.includes('1000'))) {
      warnings.push({
        note: 'Metformin 1000mg twice daily - confirm eGFR > 30'
      });
    }
    
    const result = {
      interactions,
      warnings,
      recommendation: interactions.length > 0 
        ? 'Interaction alert found. Physician review required before dispensing.'
        : warnings.length > 0
        ? 'Review warnings before dispensing.'
        : 'No significant interactions found.'
    };
    
    // Log the check
    await prisma.aiAnalysisLog.create({
      data: {
        userId: req.user.id,
        type: 'PRESCRIPTION_CHECK',
        input: medications.join(', '),
        output: JSON.stringify(result),
        timestamp: new Date()
      }
    });
    
    res.json(result);
  } catch (error) {
    console.error('Check prescription error:', error);
    res.status(500).json({ error: 'Failed to check prescription' });
  }
});

module.exports = router;
