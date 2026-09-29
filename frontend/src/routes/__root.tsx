import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HeadContent, Link, Outlet, Scripts, createRootRouteWithContext, useRouter } from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import { AppShell } from "@/components/incidentlens/app-shell";
import { IncidentLensProvider } from "@/context/incident-lens-context";
import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
function NotFoundComponent(){return <div className="flex min-h-screen items-center justify-center bg-background p-6"><div className="text-center"><p className="font-mono text-sm text-primary">404</p><h1 className="mt-3 text-2xl font-semibold">Page not found</h1><p className="mt-2 text-sm text-muted-foreground">This investigation view does not exist.</p><Button asChild className="mt-5"><Link to="/dashboard">Return to Command Center</Link></Button></div></div>}
function ErrorComponent({error,reset}:{error:Error;reset:()=>void}){const router=useRouter();useEffect(()=>{reportLovableError(error,{boundary:"tanstack_root_error_component"})},[error]);return <div className="flex min-h-screen items-center justify-center bg-background p-6"><div className="text-center"><h1 className="text-xl font-semibold">This page didn’t load</h1><p className="mt-2 text-sm text-muted-foreground">The local workspace hit an unexpected error.</p><Button className="mt-5" onClick={()=>{router.invalidate();reset()}}>Try again</Button></div></div>}
export const Route=createRootRouteWithContext<{queryClient:QueryClient}>()({head:()=>({meta:[{charSet:"utf-8"},{name:"viewport",content:"width=device-width, initial-scale=1"},{name:"author",content:"IncidentLens"}],links:[{rel:"stylesheet",href:appCss},{rel:"preconnect",href:"https://fonts.googleapis.com"},{rel:"preconnect",href:"https://fonts.gstatic.com",crossOrigin:"anonymous"},{rel:"stylesheet",href:"https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"},{rel:"icon",href:"/favicon.ico",type:"image/x-icon"}]}),shellComponent:RootShell,component:RootComponent,notFoundComponent:NotFoundComponent,errorComponent:ErrorComponent});
function RootShell({children}:{children:ReactNode}){return <html lang="en" className="dark"><head><HeadContent/></head><body>{children}<Scripts/></body></html>}
function RootComponent(){const {queryClient}=Route.useRouteContext();return <QueryClientProvider client={queryClient}><IncidentLensProvider><AppShell><Outlet/></AppShell><Toaster theme="dark" richColors/></IncidentLensProvider></QueryClientProvider>}
