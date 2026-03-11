import { useState } from "react";
import { Sidebar } from "./Sidebar";
import { UploadCard } from "./UploadCard";
import { ChatContainer } from "./ChatContainer";
import { ChatInput } from "./ChatInput";

export function KnowledgeLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <main className="flex flex-1 flex-col min-w-0 md:ml-[260px]">
        {/* Hamburger: only on small screens */}
        <button
          type="button"
          aria-label="Open menu"
          onClick={() => setSidebarOpen(true)}
          className="fixed left-4 top-4 z-10 flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-card/95 text-text-primary shadow-lg backdrop-blur-sm transition hover:bg-background/80 md:hidden"
        >
          <MenuIcon className="h-5 w-5" />
        </button>

        <section className="shrink-0 border-b border-border bg-background/50 px-6 py-3 backdrop-blur-sm">
          <UploadCard />
        </section>

        <section className="flex flex-1 flex-col min-h-0">
          <ChatContainer />
          <ChatInput />
        </section>
      </main>
    </div>
  );
}

function MenuIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}
