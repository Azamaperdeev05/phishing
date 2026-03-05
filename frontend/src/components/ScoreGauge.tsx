"use client";

interface ScoreGaugeProps {
  score: number;
  verdict: string;
  riskLevel: string;
}

export default function ScoreGauge({ score, verdict, riskLevel }: ScoreGaugeProps) {
  const getColor = () => {
    if (score >= 61) return { ring: "text-zinc-900", bg: "bg-white", text: "text-zinc-900" };
    if (score >= 31) return { ring: "text-zinc-600", bg: "bg-white", text: "text-zinc-700" };
    return { ring: "text-zinc-500", bg: "bg-white", text: "text-zinc-700" };
  };

  const getVerdictText = () => {
    switch (verdict) {
      case "SAFE": return "Қауіпсіз";
      case "SUSPICIOUS": return "Күдікті";
      case "PHISHING": return "Фишинг!";
      default: return verdict;
    }
  };

  const getRiskText = () => {
    switch (riskLevel) {
      case "LOW": return "Төмен қауіп";
      case "MEDIUM": return "Орташа қауіп";
      case "HIGH": return "Жоғары қауіп";
      default: return riskLevel;
    }
  };

  const colors = getColor();
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className={`flex flex-col items-center p-8 rounded-3xl border border-[var(--color-border)] shadow-[0_20px_40px_rgba(0,0,0,0.05)] ${colors.bg}`}>
      <div className="relative w-40 h-40">
        <svg className="w-40 h-40 -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-zinc-200"
          />
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            className={colors.ring}
            style={{
              strokeDasharray: circumference,
              strokeDashoffset: offset,
              transition: "stroke-dashoffset 1s ease-out",
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-bold ${colors.text}`}>
            {Math.round(score)}
          </span>
          <span className="text-xs text-[var(--color-muted)]">/ 100</span>
        </div>
      </div>

      <div className="mt-4 text-center">
        <p className={`text-xl font-bold ${colors.text}`}>{getVerdictText()}</p>
        <p className="text-sm text-[var(--color-muted)] mt-1">{getRiskText()}</p>
      </div>
    </div>
  );
}
