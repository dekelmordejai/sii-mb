"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession } from "./auth-gate";

export function Navigation() {
  const pathname = usePathname();
  const { user, logout } = useSession();
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">S</div>
        <div>
          <strong>SII-MB</strong>
          <small>Indicadores Metrobús</small>
        </div>
      </div>
      <div className="nav-section">PLATAFORMA</div>
      <nav aria-label="Navegación principal">
        <Link
          className={`nav-link ${pathname === "/" ? "selected" : ""}`}
          aria-label="Inicio"
          href="/"
        >
          ▦ <span>Inicio</span>
        </Link>
        <Link
          className={`nav-link ${pathname.startsWith("/indicadores") ? "selected" : ""}`}
          aria-label="Indicadores"
          href="/indicadores"
        >
          ▤ <span>Indicadores</span>
        </Link>
        <Link
          className={`nav-link ${pathname === "/fuentes" ? "selected" : ""}`}
          aria-label="Fuentes de datos"
          href="/fuentes"
        >
          ▰ <span>Fuentes de datos</span>
        </Link>
        <Link
          className={`nav-link ${pathname === "/resultados" ? "selected" : ""}`}
          aria-label="Resultados e historial"
          href="/resultados"
        >
          ∑ <span>Resultados e historial</span>
        </Link>
        <Link
          className={`nav-link ${pathname === "/tableros" ? "selected" : ""}`}
          aria-label="Tableros"
          href="/tableros"
        >
          ▥ <span>Tableros</span>
        </Link>
        {user?.role === "admin" && (
          <Link
            className={`nav-link ${pathname === "/administracion" ? "selected" : ""}`}
            aria-label="Administración"
            href="/administracion"
          >
            ⚙ <span>Administración</span>
          </Link>
        )}
      </nav>
      <div className="sidebar-footer">
        <span className="env-dot" /> {user?.username}
        <br />
        <small>{user?.role} · Sesión de 8 horas</small>
        <br />
        <button className="button outline small" onClick={logout}>
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
