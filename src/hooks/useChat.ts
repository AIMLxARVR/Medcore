import { useState } from 'react';
import { aiApi, ApiError } from '../services/api';
import { sanitizeInput } from '../utils/inputSanitizer';

interface Message {
  from: 'user' | 'bot';
  text: string;
  isError?: boolean;
}

interface ApiMessage {
  role: 'user' | 'assistant';
  content: string;
}

const INIT_MSG: Message = { from: "bot", text: "Hello! 👋 I'm MedBot, your MedCore AI assistant.\n\nI can help you:\n• 📅 Book or manage appointments\n• 🩺 Check doctor availability\n• 📊 View your reports & history\n• 💊 Symptom guidance\n• 🔔 Check appointment status\n\nWhat do you need today?" };

export const useChat = () => {
  const [msgs, setMsgs] = useState<Message[]>([INIT_MSG]);
  const [apiHistory, setApiHistory] = useState<ApiMessage[]>([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = async (text?: string) => {
    const txt = (text || input).trim();
    if (!txt || typing) return;
    
    // Sanitize user input for security
    const sanitizedText = sanitizeInput(txt);
    
    setInput("");
    setError(null);
    setMsgs(p => [...p, { from: "user", text: sanitizedText }]);
    setTyping(true);
    try {
      // Call backend AI API (secured with JWT)
      const { reply, history } = await aiApi.chat({
        message: sanitizedText,
        history: apiHistory,
      });
      // Cast history from backend response
      setApiHistory(history as ApiMessage[]);
      setMsgs(p => [...p, { from: "bot", text: reply }]);
    } catch (e) {
      const errorMessage = e instanceof ApiError 
        ? e.message 
        : "MedBot is temporarily unavailable. Please try again.";
      setError(errorMessage);
      setMsgs(p => [...p, { from: "bot", text: "⚠️ I'm having a brief connectivity issue. Please try again in a moment.", isError: true }]);
    } finally {
      setTyping(false);
    }
  };

  const reset = () => {
    setMsgs([INIT_MSG]);
    setApiHistory([]);
    setInput("");
    setError(null);
  };

  return { msgs, input, typing, error, setInput, send, reset };
};
