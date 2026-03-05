"use client";

import { useEffect, useState } from "react";
import { getHistory, type HistoryItem } from "@/lib/api";

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory(50);
        setHistory(data);
      } catch {
        setError("Тарихты жүктеу кезінде қате болды");
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const getVerdictStyle = (verdict: string) => {
    switch (verdict) {
      case "SAFE":
        return "bg-zinc-100 text-zinc-800 border-zinc-200";
      case "SUSPICIOUS":
        return "bg-zinc-200 text-zinc-800 border-zinc-300";
      case "PHISHING":
        return "bg-zinc-800 text-zinc-100 border-zinc-800";
      default:
        return "bg-zinc-100 text-zinc-700 border-zinc-200";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("kk-KZ", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h2 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)] mb-2">
          Тексеру тарихы
        </h2>
        <p className="text-[var(--color-muted)]">
          Соңғы тексерілген сайттардың тізімі
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-12 h-12 rounded-full border-4 border-zinc-200 border-t-zinc-900 animate-spin" />
        </div>
      ) : error ? (
        <div className="p-4 rounded-xl bg-white border border-[var(--color-border)] text-[var(--color-foreground)] text-center">
          {error}
        </div>
      ) : history.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-2xl border border-[var(--color-border)]">
          <p className="text-[var(--color-muted)]">
            Әлі ешқандай сайт тексерілмеген
          </p>
        </div>
      ) : (
        <div className="overflow-hidden bg-white rounded-2xl border border-[var(--color-border)] shadow-[0_16px_30px_rgba(0,0,0,0.05)]">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-[var(--color-border)]">
                <th className="px-6 py-4 text-sm font-semibold text-[var(--color-foreground)]">URL / Домен</th>
                <th className="px-6 py-4 text-sm font-semibold text-[var(--color-foreground)]">Нәтиже</th>
                <th className="px-6 py-4 text-sm font-semibold text-[var(--color-foreground)]">Ұпай</th>
                <th className="px-6 py-4 text-sm font-semibold text-[var(--color-foreground)] text-right">Уақыты</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-100">
              {history.map((item) => (
                <tr key={item.id} className="hover:bg-zinc-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="max-w-xs md:max-w-md overflow-hidden text-ellipsis whitespace-nowrap">
                      <p className="text-sm font-medium text-[var(--color-foreground)]">{item.domain}</p>
                      <p className="text-xs text-[var(--color-muted)] truncate">{item.url}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${getVerdictStyle(item.verdict)}`}>
                      {item.verdict}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm font-mono font-medium text-[var(--color-foreground)]">
                      {item.score}/100
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <p className="text-sm text-[var(--color-muted)]">
                      {formatDate(item.scan_date)}
                    </p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
