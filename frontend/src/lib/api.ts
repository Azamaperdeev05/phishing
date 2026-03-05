function resolveApiBase(): string {
  const envApiBase = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (envApiBase) return envApiBase.replace(/\/+$/, "");

  if (typeof window !== "undefined") {
    const { protocol, host } = window.location;
    if (host.endsWith(".up.railway.app")) {
      // Example: phishing-frontend.up.railway.app -> phishing.up.railway.app
      const backendHost = host.replace("-frontend.", ".");
      return `${protocol}//${backendHost}/api/v1`;
    }
  }

  return "http://localhost:8000/api/v1";
}

const API_BASE = resolveApiBase();

const getHeaders = () => {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
};

export interface FactorScores {
  url_analysis: number;
  ssl_check: number;
  whois_check: number;
  content_analysis: number;
  text_analysis: number;
  blacklist_check: number;
}

export interface ScanResult {
  url: string;
  domain: string;
  score: number;
  verdict: "SAFE" | "SUSPICIOUS" | "PHISHING";
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  factors: FactorScores;
  warnings: string[];
  recommendation: string;
}

export interface HistoryItem {
  id: number;
  url: string;
  domain: string;
  score: number;
  verdict: string;
  risk_level: string;
  scan_date: string;
}

export async function scanUrl(
  url: string,
  language: string = "kk"
): Promise<ScanResult> {
  const res = await fetch(`${API_BASE}/scan`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ url, language }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Сканерлеу кезінде қате болды");
  }

  return res.json();
}

export async function getHistory(
  limit: number = 20
): Promise<HistoryItem[]> {
  const res = await fetch(`${API_BASE}/history?limit=${limit}`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error("Тарихты алу мүмкін болмады");
  return res.json();
}

export async function login(email: string, password: string): Promise<void> {
  const formData = new URLSearchParams();
  formData.append("username", email); // OAuth2PasswordRequestForm expects 'username'
  formData.append("password", password);

  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Кіру кезінде қате болды");
  }

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
}

export async function register(email: string, password: string, fullName?: string): Promise<void> {
  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Тіркелу кезінде қате болды");
  }
}

export function logout(): void {
  localStorage.removeItem("token");
}

export function isLoggedIn(): boolean {
  return typeof window !== "undefined" && !!localStorage.getItem("token");
}
