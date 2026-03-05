import type { Metadata } from "next";
import { Manrope, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";

const geistSans = Manrope({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

const geistMono = JetBrains_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "PhishGuard — Фишинг сайттарды анықтау",
  description:
    "PhishGuard — веб-сайттардың қауіпсіздігін тексеруге мүмкіндік беретін интеллектуальді платформа",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="kk">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen`}
      >
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
