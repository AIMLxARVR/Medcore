import { useState } from 'react';
import { callClaude } from '../services/anthropic';
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
    const rawTxt = text || input;
    const txt = sanitizeInput(rawTxt.trim());
    if (!txt || typing) return;
    setInput("");
    setError(null);
    // Sanitize user input before displaying
    setMsgs(p => [...p, { from: "user", text: txt }]);
    setTyping(true);
    try {
      const { replyText, updatedHistory } = await callClaude(txt, apiHistory);
      setApiHistory(updatedHistory);
      // Sanitize bot response before displaying
      const sanitizedReply = sanitizeInput(replyText);
      setMsgs(p => [...p, { from: "bot", text: sanitizedReply }]);
    } catch (e) {
      setError("MedBot is temporarily unavailable. Please try again.");
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
