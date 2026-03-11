import { type FormEvent, useState } from "react";
import { useChat } from "../../context/ChatContext";

export function ChatInput() {
  const { sendMessage, isLoading } = useChat();
  const [input, setInput] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="shrink-0 border-t border-border bg-background/80 px-4 py-4 backdrop-blur-sm">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-3xl items-center gap-3 rounded-2xl border border-border bg-card/60 px-4 py-2 shadow-glow-sm transition-shadow focus-within:border-accent/50 focus-within:shadow-glow"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask KnowledgeVolt... (e.g., last quarter sales)"
          className="min-w-0 flex-1 bg-transparent py-3 text-sm text-text-primary placeholder:text-text-muted focus:outline-none"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-accent/20 text-accent shadow-[0_0_12px_rgba(56,189,248,0.25)] transition-all hover:bg-accent/30 hover:shadow-[0_0_16px_rgba(56,189,248,0.4)] disabled:opacity-50 disabled:shadow-none"
          aria-label="Send"
        >
          <SendDiamondIcon className="h-5 w-5" />
        </button>
      </form>
    </div>
  );
}

/** Multi-faceted diamond/star send button (electric blue, stylized) */
function SendDiamondIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2L14 9h6l-5 4 2 7-5-5-5 5 2-7-5-4h6L12 2z" />
    </svg>
  );
}
