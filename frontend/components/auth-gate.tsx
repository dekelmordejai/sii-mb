"use client";
import { createContext, FormEvent, useContext, useEffect, useState } from "react";
import { User, workspace } from "@/lib/workspace";

const SessionContext = createContext<{user:User|null;logout:()=>void}>({user:null,logout:()=>{}});
export const useSession = () => useContext(SessionContext);

export function AuthGate({children}:{children:React.ReactNode}) {
  const [user,setUser] = useState<User|null>(null);
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState("");
  const [busy,setBusy] = useState(false);
  useEffect(()=>{
    workspace.me().then(setUser).catch(()=>{}).finally(()=>setLoading(false));
    const expire = () => setUser(null);
    window.addEventListener("session-expired",expire);
    return ()=>window.removeEventListener("session-expired",expire);
  },[]);
  async function login(e:FormEvent<HTMLFormElement>) {
    e.preventDefault(); setBusy(true); setError("");
    const form = new FormData(e.currentTarget);
    try { setUser(await workspace.login(String(form.get("username")),String(form.get("password")))); }
    catch(err) { setError(err instanceof Error?err.message:"Error de acceso"); }
    finally {setBusy(false);}
  }
  if(loading) return <div className="login-screen"><p>Conectando con SII-MB…</p></div>;
  if(!user) return <main className="login-screen"><section className="login-card panel"><p className="eyebrow">METROBÚS · ENTORNO LOCAL</p><h1>Sistema Integral de Indicadores</h1><p className="muted">Accede con tu cuenta autorizada.</p><form onSubmit={login} className="form-fields"><div><label htmlFor="username">Usuario</label><input id="username" name="username" required autoComplete="username"/></div><div><label htmlFor="password">Contraseña</label><input id="password" name="password" type="password" required maxLength={128} autoComplete="current-password"/></div><button className="button primary" disabled={busy}>{busy?"Entrando…":"Iniciar sesión"}</button></form>{error&&<p className="error" role="alert">{error}</p>}<p className="form-note">La cuenta inicial se crea durante la instalación local. Usa únicamente datos sintéticos.</p></section></main>;
  return <SessionContext.Provider value={{user,logout:()=>{workspace.logout().then(()=>setUser(null)).catch(err=>setError(String(err)));}}}>{children}</SessionContext.Provider>;
}
