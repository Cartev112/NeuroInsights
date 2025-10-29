import { Outlet, Link, useLocation } from 'react-router-dom'
import { Brain, MessageSquare, LayoutDashboard, Lightbulb } from 'lucide-react'

export function Layout() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold">NeuroInsights</h1>
            </div>
            <nav className="flex gap-6">
              <Link
                to="/chat"
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isActive('/chat')
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent/60'
                }`}
              >
                <MessageSquare
                  className={`h-5 w-5 ${
                    isActive('/chat') ? 'text-primary-foreground' : 'text-primary'
                  }`}
                />
                <span>Chat</span>
              </Link>
              <Link
                to="/dashboard"
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isActive('/dashboard')
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent/60'
                }`}
              >
                <LayoutDashboard
                  className={`h-5 w-5 ${
                    isActive('/dashboard') ? 'text-primary-foreground' : 'text-primary'
                  }`}
                />
                <span>Dashboard</span>
              </Link>
              <Link
                to="/insights"
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isActive('/insights')
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent/60'
                }`}
              >
                <Lightbulb
                  className={`h-5 w-5 ${
                    isActive('/insights') ? 'text-primary-foreground' : 'text-primary'
                  }`}
                />
                <span>Insights</span>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
