// Base API Client with JWT Token Injection
import { authClient } from '@/lib/auth/better-auth-client'

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async getAuthToken(): Promise<string | null> {
    try {
      const session = await authClient.getSession()
      return session?.session?.token || null
    } catch (error) {
      console.error('Failed to get auth token:', error)
      return null
    }
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = await this.getAuthToken()

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    })

    // Handle 401 Unauthorized - redirect to login
    if (response.status === 401) {
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
      throw new Error('Unauthorized')
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null as T
    }

    // Parse response
    const data = await response.json()

    // Handle error responses
    if (!response.ok) {
      throw new Error(data.error?.message || data.message || 'Request failed')
    }

    return data
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete(endpoint: string): Promise<void> {
    return this.request<void>(endpoint, { method: 'DELETE' })
  }
}

const apiClient = new ApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')

export default apiClient
