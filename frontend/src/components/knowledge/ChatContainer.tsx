import { useRef, useEffect } from "react";
import { useChat } from "../../context/ChatContext";
import { ChatMessage } from "./ChatMessage";
import { ThinkingDots } from "./ThinkingDots";

export function ChatContainer() {
  const { messages, isLoading, error } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-4">
      <div className="mx-auto max-w-3xl space-y-6">
        {messages.length === 0 && !isLoading && (
          <div className="rounded-2xl border border-border bg-card/40 px-6 py-8 backdrop-blur-md">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-amber-400/20 text-amber-400">
                <LightbulbSearchIcon className="h-6 w-6" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="mb-4 text-sm font-medium text-text-primary">
                  Ask questions about your data or knowledge base.
                </p>
                <ul className="space-y-2 text-sm text-text-muted">
                  <li className="flex items-center gap-2">
                    <DatabaseIcon className="h-4 w-4 shrink-0 text-text-muted" />
                    <span>SQL Data Query: &quot;How many employees per department?&quot;</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <DocumentIcon className="h-4 w-4 shrink-0 text-text-muted" />
                    <span>Knowledge Base Search: &quot;What is the remote work policy?&quot;</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {isLoading && <ThinkingDots />}

        {error && (
          <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}

/** Lightbulb + magnifying glass combined (golden/yellow-orange in reference) */
function LightbulbSearchIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 21h6M12 3a5 5 0 0 1 3.9 8.1 3 3 0 0 1 .1 2.2 3 3 0 0 1-6 0 5 5 0 0 1 3.9-8.1M12 18v1" />
      <circle cx="16" cy="10" r="3.5" />
      <path d="m18 12 2 2" />
    </svg>
  );
}

function DatabaseIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
    </svg>
  );
}

function DocumentIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
    </svg>
  );
}
