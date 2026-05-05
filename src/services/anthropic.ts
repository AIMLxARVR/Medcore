import { MEDBOT_SYSTEM } from '../constants/prompts';

// Get API key from environment variables (set in .env file for local development)
// Required: VITE_ANTHROPIC_API_KEY=your_api_key_here
const getApiKey = (): string => {
  const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.warn('WARNING: VITE_ANTHROPIC_API_KEY not set. Chatbot will not work in production.');
    // Allow demo mode in development without key
    if (import.meta.env.DEV) {
      return 'demo-key';
    }
    throw new Error('API key required. Set VITE_ANTHROPIC_API_KEY in .env');
  }
  return apiKey;
};

export const callClaude = async (userText: string, history: any[]) => {
  const apiKey = getApiKey();
  
  // Demo mode for development without valid API key
  if (apiKey === 'demo-key') {
    const demoResponses: Record<string, string> = {
      'appointment': 'I can help you book an appointment! Which doctor would you like to see?',
      'symptoms': 'I understand. Could you describe your symptoms in more detail?',
      'reports': 'You have recent reports on file. Would you like me to summarize them?',
      'default': 'Thank you for your message! How can I assist you today?'
    };
    const lowerText = userText.toLowerCase();
    let response = demoResponses.default;
    for (const [key, value] of Object.entries(demoResponses)) {
      if (lowerText.includes(key)) {
        response = value;
        break;
      }
    }
    const updatedHistory = [...history, { role: "user", content: userText }, { role: "assistant", content: response }];
    return { replyText: response, updatedHistory };
  }
  
  const newHistory = [...history, { role: "user", content: userText }];
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 200,
      system: MEDBOT_SYSTEM,
      messages: newHistory,
    }),
  });
  if (!res.ok) throw new Error("API error " + res.status);
  const data = await res.json();
  const replyText =
    data.content?.map((b: any) => (b.type === "text" ? b.text : "")).join("") ||
    "Sorry, I couldn't process that. Please try again.";
  const updatedHistory = [...newHistory, { role: "assistant", content: replyText }];
  return { replyText, updatedHistory };
};
