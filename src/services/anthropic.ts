import { MEDBOT_SYSTEM } from '../constants/prompts';

export const callClaude = async (userText: string, history: any[]) => {
  const newHistory = [...history, { role: "user", content: userText }];
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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