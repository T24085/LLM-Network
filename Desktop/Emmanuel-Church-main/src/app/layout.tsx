import type { Metadata } from "next";
import { Cormorant_Garamond, Manrope } from "next/font/google";
import type { ReactNode } from "react";
import { SiteFooter } from "@/components/site-footer";
import { MotionShell } from "@/components/motion-shell";
import { SiteHeader } from "@/components/site-header";
import "./globals.css";
import "./site-overrides.css";

const display = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-display",
  display: "swap",
});

const body = Manrope({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-body",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Emmanuel Church",
    template: "%s | Emmanuel Church",
  },
  description:
    "A bright editorial website for Emmanuel Church in Abilene, Kansas, centered on worship, ministries, staff, events, sermons, and giving.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body>
        <div className="page-backdrop" />
        <SiteHeader />
        <main>
          <MotionShell>{children}</MotionShell>
        </main>
        <SiteFooter />
      </body>
    </html>
  );
}
