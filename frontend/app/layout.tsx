import type { Metadata } from 'next'
import { AuthProvider } from '@/lib/auth/auth-context'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'Multi-user todo application with authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  )
}
