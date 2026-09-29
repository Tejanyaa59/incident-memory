import { Link, useRouterState } from "@tanstack/react-router";
import { Activity, Bell, BrainCircuit, History, LayoutDashboard, Menu, Search, ShieldCheck, Siren, X } from "lucide-react";
import { useState, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { LearningStrip } from "./core";

import { useIncidentLens } from "@/context/incident-lens-context";

const nav = [
  { to:"/dashboard", label:"Command Center", icon:LayoutDashboard },
  { to:"/investigate", label:"Investigate", icon:Siren },
  { to:"/memory", label:"Hindsight Memory", icon:BrainCircuit },
  { to:"/learning", label:"Learning", icon:Activity },
  { to:"/history", label:"Incident History", icon:History },
] as const;
function Sidebar({ mobile=false, onNavigate }: { mobile?:boolean; onNavigate?:()=>void }) {
  const pathname=useRouterState({select:(state)=>state.location.pathname});
  const { hindsightConnected } = useIncidentLens();
  return <aside className={cn("flex h-full w-64 flex-col border-r border-border bg-sidebar", !mobile&&"fixed inset-y-0 left-0 z-30 hidden lg:flex")}><div className="border-b border-border px-5 py-5"><div className="flex items-center gap-3"><div className="flex size-8 items-center justify-center rounded bg-primary text-primary-foreground"><ShieldCheck className="size-4"/></div><div><p className="text-sm font-bold">INCIDENTLENS</p><p className="text-[10px] text-muted-foreground">Learning-First Incident Investigator</p></div></div></div><nav className="flex-1 space-y-1 p-3">{nav.map(({to,label,icon:Icon})=><Link key={to} to={to} onClick={onNavigate} className={cn("flex items-center gap-3 rounded px-3 py-2.5 text-sm text-muted-foreground transition-colors hover:bg-sidebar-accent hover:text-foreground", pathname===to&&"bg-sidebar-accent text-foreground shadow-[inset_2px_0_0_var(--primary)]")}><Icon className={cn("size-4", pathname===to&&"text-primary")}/>{label}</Link>)}</nav><div className="border-t border-border p-4"><div className={cn("flex items-center gap-2 text-xs", hindsightConnected ? "text-success" : "text-warning")}><span className={cn("size-2 rounded-full", hindsightConnected ? "bg-success" : "bg-warning")}/>{hindsightConnected ? "Hindsight Connected" : "Local Memory Grounded"}</div><div className="mt-3 flex items-center justify-between text-[11px] text-muted-foreground"><span>Environment</span><span className="font-medium text-foreground">Production</span></div></div></aside>;
}
export function AppShell({ children }: { children:ReactNode }) {
  const [open,setOpen]=useState(false);
  return <TooltipProvider><div className="min-h-screen bg-background text-foreground"><Sidebar/><div className="lg:pl-64"><header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-border bg-background/95 px-4 backdrop-blur md:px-6"><Button variant="ghost" size="icon" className="lg:hidden" onClick={()=>setOpen(true)} aria-label="Open navigation"><Menu/></Button><div className="hidden items-center gap-2 text-xs sm:flex"><span className="rounded border border-border bg-secondary px-2 py-1 font-medium">Production</span><span className="ml-2 size-1.5 rounded-full bg-success"/><span className="text-muted-foreground">Systems Operational</span></div><div className="ml-auto flex items-center gap-2"><div className="relative hidden md:block"><Search className="absolute left-3 top-2.5 size-4 text-muted-foreground"/><Input className="w-64 bg-secondary pl-9" placeholder="Search incidents..." aria-label="Search"/></div><Tooltip><TooltipTrigger asChild><Button variant="ghost" size="icon" aria-label="Notifications"><Bell/></Button></TooltipTrigger><TooltipContent>Notifications</TooltipContent></Tooltip><div className="flex size-8 items-center justify-center rounded-full border border-border bg-secondary text-xs font-semibold">TM</div></div></header><LearningStrip/><main className="mx-auto max-w-7xl p-4 md:p-6 lg:p-8">{children}</main></div>{open&&<div className="fixed inset-0 z-50 lg:hidden"><div className="absolute inset-0 bg-background/80" onClick={()=>setOpen(false)}/><div className="relative h-full w-64"><Sidebar mobile onNavigate={()=>setOpen(false)}/><Button variant="ghost" size="icon" className="absolute left-65 top-3" onClick={()=>setOpen(false)} aria-label="Close navigation"><X/></Button></div></div>}</div></TooltipProvider>;
}
