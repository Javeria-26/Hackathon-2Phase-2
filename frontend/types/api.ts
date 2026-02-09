// API Types

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, string>
}

export interface ApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}
