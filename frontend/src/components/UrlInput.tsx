"use client";

import { useState } from "react";

interface UrlInputProps {
  onScan: (url: string) => void;
  loading: boolean;
}

export default function UrlInput({ onScan, loading }: UrlInputProps) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onScan(url.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative flex items-center rounded-2xl border border-[var(--color-border)] bg-white shadow-[0_12px_30px_rgba(0,0,0,0.06)] p-1.5">
        <div className="absolute left-5 text-[var(--color-muted)]">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="URL мекенжайын енгізіңіз, мысалы: https://example.com"
          className="w-full pl-12 pr-32 py-3.5 text-base rounded-xl border border-transparent bg-transparent text-[var(--color-foreground)] focus:outline-none focus:border-[var(--color-border-strong)] placeholder:text-[var(--color-muted)]"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="absolute right-2 px-6 py-2.5 bg-[var(--color-foreground)] hover:opacity-90 text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <svg
                className="animate-spin h-4 w-4"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Тексеру...
            </div>
          ) : (
            "Тексеру"
          )}
        </button>
      </div>
    </form>
  );
}
