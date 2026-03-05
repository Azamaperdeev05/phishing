interface FactorCardProps {
  name: string;
  label: string;
  score: number;
}

export default function FactorCard({ name, label, score }: FactorCardProps) {
  const getBarColor = () => {
    if (score >= 61) return "bg-zinc-900";
    if (score >= 31) return "bg-zinc-600";
    return "bg-zinc-400";
  };

  const getIcon = () => {
    switch (name) {
      case "url_analysis":
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
        );
      case "ssl_check":
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        );
      case "whois_check":
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        );
      case "content_analysis":
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        );
      case "text_analysis":
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-4 rounded-2xl bg-white border border-[var(--color-border)]">
      <div className="flex items-center gap-3 mb-3">
        <div className="text-[var(--color-muted)]">{getIcon()}</div>
        <span className="text-sm font-medium text-[var(--color-foreground)]">{label}</span>
        <span className="ml-auto text-sm font-bold text-[var(--color-foreground)]">
          {Math.round(score)}
        </span>
      </div>
      <div className="w-full h-2 bg-zinc-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ease-out ${getBarColor()}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}
