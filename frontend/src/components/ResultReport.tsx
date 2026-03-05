"use client";

import type { ScanResult } from "@/lib/api";
import ScoreGauge from "./ScoreGauge";
import FactorCard from "./FactorCard";

interface ResultReportProps {
  result: ScanResult;
  onReset: () => void;
}

const FACTOR_LABELS: Record<string, string> = {
  url_analysis: "URL талдау",
  ssl_check: "SSL сертификат",
  whois_check: "WHOIS / Домен жасы",
  content_analysis: "Мазмұн талдау",
  text_analysis: "Мәтін талдау",
  blacklist_check: "База бойынша тексеру",
};

export default function ResultReport({ result, onReset }: ResultReportProps) {
  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      <div className="text-center">
        <p className="text-sm text-[var(--color-muted)] mb-1">Тексерілген URL</p>
        <p className="text-base font-mono text-[var(--color-foreground)] break-all bg-white px-4 py-2 rounded-lg border border-[var(--color-border)] inline-block">
          {result.url}
        </p>
      </div>

      <ScoreGauge
        score={result.score}
        verdict={result.verdict}
        riskLevel={result.risk_level}
      />

      <div
        className="p-4 rounded-2xl text-center font-medium bg-white border border-[var(--color-border)] text-[var(--color-foreground)]"
      >
        {result.recommendation}
      </div>

      <div>
        <h3 className="text-lg font-semibold text-[var(--color-foreground)] mb-3">
          Талдау факторлары
        </h3>
        <div className="grid gap-3">
          {Object.entries(result.factors).map(([key, value]) => (
            <FactorCard
              key={key}
              name={key}
              label={FACTOR_LABELS[key] || key}
              score={value}
            />
          ))}
        </div>
      </div>

      {result.warnings.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-[var(--color-foreground)] mb-3">
            Ескертулер
          </h3>
          <div className="space-y-2">
            {result.warnings.map((warning, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 rounded-xl bg-white border border-[var(--color-border)]"
              >
                <svg
                  className="w-5 h-5 text-zinc-900 mt-0.5 shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                  />
                </svg>
                <span className="text-sm text-[var(--color-foreground)]">
                  {warning}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-6 no-print">
        <button
          onClick={onReset}
          className="w-full sm:w-auto px-8 py-3 bg-white hover:bg-[var(--color-surface-soft)] text-[var(--color-foreground)] font-medium rounded-xl border border-[var(--color-border)]"
        >
          Жаңа тексеру
        </button>
        <button
          onClick={() => window.print()}
          className="w-full sm:w-auto px-8 py-3 bg-[var(--color-foreground)] hover:opacity-90 text-white font-medium rounded-xl flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          PDF ретінде сақтау
        </button>
      </div>
    </div>
  );
}
