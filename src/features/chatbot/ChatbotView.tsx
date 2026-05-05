import React, { useRef, useEffect } from 'react';
import { Bot, Send, RefreshCw } from 'lucide-react';
import { TypingDots, Button, Card } from '../../components';
import { useChat } from '../../hooks/useChat';
import styles from './ChatbotView.module.css';

interface QuickReply {
  label: string;
  msg: string;
}

const quickReplies: QuickReply[] = [
  { label: "📅 Book appointment", msg: "I want to book an appointment" },
  { label: "🗓️ My appointment", msg: "Show my upcoming appointment" },
  { label: "👨‍⚕️ Available doctors", msg: "Which doctors are available today?" },
  { label: "📄 My reports", msg: "Show my recent reports" },
  { label: "🤒 I have fever", msg: "I have fever and cough" },
  { label: "💔 Chest pain", msg: "I'm having chest pain" },
];

function ChatbotView() {
  const { msgs, input, typing, error, setInput, send, reset } = useChat();
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, typing]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.botIcon}>
          <Bot size={20} color="var(--color-primary)" />
        </div>
        <div>
          <div className={styles.title}>MedBot — AI Assistant</div>
          <div className={styles.status}>
            <div className={styles.statusDot} />Online
          </div>
        </div>
        <Button onClick={reset} variant="ghost" size="sm" className={styles.resetButton}>
          <RefreshCw size={12} /> Reset
        </Button>
      </div>

      <Card className={styles.chatCard}>
        <div className={styles.messagesContainer}>
          {msgs.map((m, i) => (
            <div 
              key={i} 
              className={`${styles.messageWrapper} ${m.from === "user" ? styles.user : ''}`}
            >
              <div className={`${styles.message} ${m.from}`}>
                {m.text}
              </div>
            </div>
          ))}
          {typing && <TypingDots size="sm" />}
          <div ref={bottom} />
        </div>

        <div className={styles.inputArea}>
          <div className={styles.quickReplies}>
            {quickReplies.map((qr) => (
              <button
                key={qr.label}
                onClick={() => send(qr.msg)}
                className={styles.quickReplyButton}
              >
                {qr.label}
              </button>
            ))}
          </div>

          <div className={styles.inputWrapper}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && send()}
              placeholder="Ask MedBot..."
              className={styles.chatInput}
            />
            <Button onClick={() => send()} disabled={typing}>
              <Send size={14} />
            </Button>
          </div>

          {error && <div className={styles.errorMessage}>{error}</div>}
        </div>
      </Card>
    </div>
  );
}

export default ChatbotView;