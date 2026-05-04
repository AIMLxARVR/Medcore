import { useState } from 'react';
import { callClaude } from '../services/anthropic';

const INIT_MSG = { from: "bot", text: "Hello! 👋 I'm MedBot, your MedCore AI assistant.\n\nI can help you:\n• 📅 Book or manage appointments\n• 🩺 Check doctor availability\n• 📊 View your reports & history\n• 💊 Symptom guidance\n• 🔔 Check appointment status\n\nWhat do you need today?" };

export const useChat = () => {
  const [msgs, setMsgs] = useState([INIT_MSG]);
  const [apiHistory, setApiHistory] = useState([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState(null);

  const send = async (text?: string) => {
    const txt = (text || input).trim();
    if (!txt || typing) return;
    setInput("");
    setError(null);
    setMsgs(p => [...p, { from: "user", text: txt }]);
    setTyping(true);
    try {
      const { replyText, updatedHistory } = await callClaude(txt, apiHistory);
      setApiHistory(updatedHistory);
      setMsgs(p => [...p, { from: "bot", text: replyText }]);
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