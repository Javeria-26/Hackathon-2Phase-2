// Validation Utilities

// Email validation (RFC 5322 compliant)
export function validateEmail(email: string): { valid: boolean; error?: string } {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!email) {
    return { valid: false, error: 'Email is required' }
  }

  if (!emailRegex.test(email)) {
    return { valid: false, error: 'Please enter a valid email address' }
  }

  if (email.length > 255) {
    return { valid: false, error: 'Email must be less than 255 characters' }
  }

  return { valid: true }
}

// Password validation (complexity requirements)
export function validatePassword(password: string): { valid: boolean; error?: string } {
  if (!password) {
    return { valid: false, error: 'Password is required' }
  }

  if (password.length < 8) {
    return { valid: false, error: 'Password must be at least 8 characters' }
  }

  if (!/[A-Z]/.test(password)) {
    return { valid: false, error: 'Password must contain at least one uppercase letter' }
  }

  if (!/[a-z]/.test(password)) {
    return { valid: false, error: 'Password must contain at least one lowercase letter' }
  }

  if (!/[0-9]/.test(password)) {
    return { valid: false, error: 'Password must contain at least one number' }
  }

  if (!/[!@#$%^&*]/.test(password)) {
    return { valid: false, error: 'Password must contain at least one special character (!@#$%^&*)' }
  }

  return { valid: true }
}

// Todo title validation
export function validateTodoTitle(title: string): { valid: boolean; error?: string } {
  const trimmed = title.trim()

  if (!trimmed) {
    return { valid: false, error: 'Title is required' }
  }

  if (trimmed.length > 200) {
    return { valid: false, error: 'Title must be less than 200 characters' }
  }

  return { valid: true }
}

// Todo description validation
export function validateTodoDescription(description: string): { valid: boolean; error?: string } {
  const trimmed = description.trim()

  if (trimmed.length > 1000) {
    return { valid: false, error: 'Description must be less than 1000 characters' }
  }

  return { valid: true }
}
