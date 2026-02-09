'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { User, AuthState } from '@/types/auth'
import { authClient } from './better-auth-client'

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    // Check for existing session on mount
    checkSession()
  }, [])

  const checkSession = async () => {
    try {
      const session = await authClient.getSession()
      if (session?.user) {
        setAuthState({
          user: { id: session.user.id, email: session.user.email },
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
      } else {
        setAuthState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
      }
    } catch (error) {
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: 'Failed to check session',
      })
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setAuthState((prev) => ({ ...prev, isLoading: true, error: null }))

      const result = await authClient.signIn.email({
        email,
        password,
      })

      if (result.error) {
        throw new Error(result.error.message || 'Login failed')
      }

      if (result.data?.user) {
        setAuthState({
          user: { id: result.data.user.id, email: result.data.user.email },
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed'
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: message,
      })
      throw error
    }
  }

  const register = async (email: string, password: string) => {
    try {
      setAuthState((prev) => ({ ...prev, isLoading: true, error: null }))

      const result = await authClient.signUp.email({
        email,
        password,
        name: email.split('@')[0], // Use email prefix as name
      })

      if (result.error) {
        throw new Error(result.error.message || 'Registration failed')
      }

      if (result.data?.user) {
        setAuthState({
          user: { id: result.data.user.id, email: result.data.user.email },
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Registration failed'
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: message,
      })
      throw error
    }
  }

  const logout = async () => {
    try {
      await authClient.signOut()
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      })
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <AuthContext.Provider value={{ ...authState, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}
