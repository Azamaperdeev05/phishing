"use client";

import { useState } from "react";
import UrlInput from "@/components/UrlInput";
import ResultReport from "@/components/ResultReport";
import { scanUrl, type ScanResult } from "@/lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async (url: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await scanUrl(url);
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Белгісіз қате болды"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-14">
      {!result ? (
        <div className="flex flex-col items-center gap-9">
          <div className="text-center space-y-4 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-white text-[var(--color-muted)] text-sm font-medium mb-4">
              <svg
                className="w-4 h-4"
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
              AI-негізіндегі қауіпсіздік платформасы
            </div>
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight text-[var(--color-foreground)] leading-tight">
              Фишинг сайттарды сенімді әрі жылдам анықтаңыз
            </h2>
            <p className="text-lg text-[var(--color-muted)]">
              URL мекенжайын енгізіп, сайттың қауіпсіздігін жан-жақты тексеріңіз.
              Жүйе URL, SSL, мазмұн, ML-модельдер және базаларды талдайды.
            </p>
          </div>

          <UrlInput onScan={handleScan} loading={loading} />

          {error && (
            <div className="w-full max-w-2xl p-4 rounded-xl bg-white border border-[var(--color-border)] text-[var(--color-foreground)] text-center">
              {error}
            </div>
          )}

          {loading && (
            <div className="flex flex-col items-center gap-4 py-8">
              <div className="relative w-16 h-16">
                <div className="absolute inset-0 rounded-full border-4 border-zinc-200" />
                <div className="absolute inset-0 rounded-full border-4 border-zinc-900 border-t-transparent animate-spin" />
              </div>
              <div className="text-center">
                <p className="font-semibold text-[var(--color-foreground)]">
                  Сайт тексерілуде...
                </p>
                <p className="text-sm text-[var(--color-muted)] mt-1">
                  URL, SSL, мазмұн, ML және қауіпті базалар талданып жатыр
                </p>
              </div>
            </div>
          )}

          {!loading && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl mt-8">
              {[
                {
                  icon: "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1",
                  title: "URL талдау",
                  desc: "Домен құрылымы, SSL, WHOIS деректерін тексеру",
                },
                {
                  icon: "M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4",
                  title: "Мазмұн талдау",
                  desc: "HTML формалар, JavaScript, жасырын элементтер",
                },
                {
                  icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
                  title: "Мәтін талдау",
                  desc: "Фишинг тілін QAZ/RUS/ENG тілдерінде анықтау",
                },
              ].map((feature, i) => (
                <div
                  key={i}
                  className="p-5 rounded-2xl bg-white border border-[var(--color-border)] shadow-[0_12px_24px_rgba(0,0,0,0.04)]"
                >
                  <svg
                    className="w-8 h-8 text-zinc-900 mb-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d={feature.icon}
                    />
                  </svg>
                  <h3 className="font-semibold text-[var(--color-foreground)] mb-1">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-[var(--color-muted)]">
                    {feature.desc}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <ResultReport result={result} onReset={handleReset} />
      )}
    </div>
  );
}
