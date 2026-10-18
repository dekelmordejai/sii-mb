import type { Metadata } from "next";
import "./globals.css";
import { Navigation } from "@/components/navigation";
import { AuthGate } from "@/components/auth-gate";

export const metadata: Metadata = {
  title: "SII-MB · Sistema Integral de Indicadores",
  description: "Entorno local de desarrollo del SII-MB",
};

export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) {
  return <html lang="es"><body><AuthGate><div className="shell"><Navigation/><main className="main"><div className="topstrip"><span>Sistema Integral de Indicadores · Metrobús</span><span className="topstrip-status">● DESARROLLO LOCAL · DATOS SINTÉTICOS</span></div>{children}</main></div></AuthGate></body></html>;
}
