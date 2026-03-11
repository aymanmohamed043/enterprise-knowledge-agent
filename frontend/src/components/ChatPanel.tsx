import { useRef, useEffect, useState, type FormEvent } from "react";
import { useChat } from "../context/ChatContext";
import { MessageBubble } from "./MessageBubble";
import { UploadPortal } from "./UploadPortal";
import styles from "./ChatPanel.module.css";

export function ChatPanel() {
  const { messages, sendMessage, isLoading, error } = useChat();
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className={styles.panel}>
      <UploadPortal />
      <div className={styles.messages}>
        {messages.length === 0 && (
          <div className={styles.empty}>
            <p>Ask about business data (SQL) or search the knowledge base.</p>
            <p className={styles.hint}>e.g. &quot;How many employees per department?&quot;</p>
          </div>
        )}
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isLoading && (
          <div className={styles.bubble} data-sender="ai">
            <span className={styles.typing}>Thinking…</span>
          </div>
        )}
        {error && (
          <div className={styles.errorBubble}>
            <span>{error}</span>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question…"
          className={styles.input}
          disabled={isLoading}
        />
        <button type="submit" className={styles.send} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
