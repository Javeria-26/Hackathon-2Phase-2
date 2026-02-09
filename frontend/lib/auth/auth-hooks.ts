// Custom Auth Hooks
import { useAuthContext } from './auth-context'
import { authClient } from './better-auth-client'

export function useAuth() {
  return useAuthContext()
}

export function useSession() {
  return authClient.useSession()
}
