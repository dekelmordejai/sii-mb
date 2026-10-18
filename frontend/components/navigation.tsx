"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function Navigation() {
  const pathname = usePathname();
  return <aside className="sidebar">
    <div className="brand"><div className="brand-mark">S</div><div><strong>SII-MB</strong><small>Indicadores Metrobús</small></div></div>
    <div className="nav-section">PLATAFORMA</div>
    <nav aria-label="Navegación principal">
      <Link className={`nav-link ${pathname === "/" ? "selected" : ""}`} href="/">▦ <span>Inicio</span></Link>
      <Link className={`nav-link ${pathname.startsWith("/indicadores") ? "selected" : ""}`} href="/indicadores">▤ <span>Indicadores</span></Link>
      <div className="nav-link unavailable" title="Pendiente de implementación">▰ <span>Fuentes de datos</span><small>Próximo</small></div>
      <div className="nav-link unavailable" title="Pendiente de implementación">∑ <span>Motor de cálculo</span><small>Próximo</small></div>
      <div className="nav-link unavailable" title="Pendiente de implementación">▥ <span>Tableros</span><small>Próximo</small></div>
      <div className="nav-link unavailable" title="Pendiente de implementación">⚙ <span>Administración</span><small>Próximo</small></div>
    </nav>
    <div className="sidebar-footer"><span className="env-dot"/> Entorno de desarrollo local<br/><small>V0.1 · Sin autenticación</small></div>
  </aside>;
}
