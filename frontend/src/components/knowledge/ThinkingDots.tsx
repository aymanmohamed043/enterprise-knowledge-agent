export function ThinkingDots() {
  return (
    <div className="flex gap-3">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-amber-500/20 text-lg">
        ⚡
      </div>
      <div className="flex flex-col gap-2 rounded-2xl border border-border bg-card/60 px-4 py-3">
        <p className="text-sm text-text-muted">
          ⚡ KnowledgeVolt is thinking
          <span className="inline-flex pl-1">
            <span className="animate-dots [animation-delay:0ms]">.</span>
            <span className="animate-dots [animation-delay:200ms]">.</span>
            <span className="animate-dots [animation-delay:400ms]">.</span>
          </span>
        </p>
      </div>
    </div>
  );
}
