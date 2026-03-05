"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { isLoggedIn, logout } from "@/lib/api";

export default function Header() {
  const [logged, setLogged] = useState(false);

  useEffect(() => {
    const checkLogin = () => {
      setLogged(isLoggedIn());
    };
    checkLogin();
  }, []);

  const handleLogout = () => {
    logout();
    setLogged(false);
    window.location.href = "/";
  };

  return (
    <header className="w-full border-b border-[var(--color-border)] bg-white/70 backdrop-blur-xl sticky top-0 z-50 no-print">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-[var(--color-foreground)] flex items-center justify-center shadow-[0_8px_18px_rgba(0,0,0,0.16)]">
            <svg
              className="w-5 h-5 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
          </div>
          <Link
            href="/"
            className="text-xl font-semibold tracking-tight text-[var(--color-foreground)]"
          >
            PhishGuard
          </Link>
        </div>

        <div className="flex items-center gap-6">
          <nav className="hidden md:flex items-center gap-6 mr-4">
            <Link
              href="/"
              className="text-sm font-medium text-[var(--color-muted)] hover:text-[var(--color-foreground)]"
            >
              Басты бет
            </Link>
            {logged && (
              <Link
                href="/history"
                className="text-sm font-medium text-[var(--color-muted)] hover:text-[var(--color-foreground)]"
              >
                Тарих
              </Link>
            )}
          </nav>

          <div className="flex items-center gap-3">
            {!logged ? (
              <>
                <Link
                  href="/login"
                  className="text-sm font-medium text-[var(--color-muted)] hover:text-[var(--color-foreground)]"
                >
                  Кіру
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-1.5 bg-[var(--color-foreground)] hover:opacity-90 text-white text-sm font-semibold rounded-lg shadow-[0_12px_24px_rgba(0,0,0,0.16)]"
                >
                  Тіркелу
                </Link>
              </>
            ) : (
              <button
                onClick={handleLogout}
                className="text-sm font-medium text-[var(--color-muted)] hover:text-[var(--color-foreground)]"
              >
                Шығу
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
