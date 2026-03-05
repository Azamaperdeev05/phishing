"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { register } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await register(email, password, fullName);
      router.push("/login?registered=true");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Тіркелу кезінде қате болды");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-20">
      <div className="bg-white p-8 rounded-3xl border border-[var(--color-border)] shadow-[0_20px_40px_rgba(0,0,0,0.05)]">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold tracking-tight text-[var(--color-foreground)] mb-2">
            Тіркелу
          </h2>
          <p className="text-[var(--color-muted)]">
            PhishGuard жүйесінде жаңа аккаунт ашыңыз
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-[var(--color-foreground)] mb-1">
              Толық есіміңіз
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[var(--color-border)] bg-white text-[var(--color-foreground)] focus:outline-none focus:border-[var(--color-border-strong)]"
              placeholder="Аты-жөніңіз"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-[var(--color-foreground)] mb-1">
              Электрондық пошта
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[var(--color-border)] bg-white text-[var(--color-foreground)] focus:outline-none focus:border-[var(--color-border-strong)]"
              placeholder="example@mail.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-[var(--color-foreground)] mb-1">
              Құпия сөз
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[var(--color-border)] bg-white text-[var(--color-foreground)] focus:outline-none focus:border-[var(--color-border-strong)]"
              placeholder="••••••••"
            />
          </div>

          {error && (
            <div className="text-sm text-[var(--color-foreground)] bg-[var(--color-surface-soft)] p-3 rounded-xl border border-[var(--color-border)]">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-[var(--color-foreground)] hover:opacity-90 text-white font-semibold rounded-xl disabled:opacity-50"
          >
            {loading ? "Тіркелу..." : "Тіркелу"}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-[var(--color-muted)]">
            Аккаунтыңыз бар ма?{" "}
            <Link
              href="/login"
              className="text-[var(--color-foreground)] hover:opacity-70 font-semibold"
            >
              Кіру
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
