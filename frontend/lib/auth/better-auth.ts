// Better Auth Configuration
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'development-secret-change-in-production',
  database: {
    // Better Auth will use in-memory storage for development
    // In production, this should connect to a database
    type: 'memory',
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 60 * 60 * 24, // 24 hours
    updateAge: 60 * 60, // 1 hour
  },
})

export type Auth = typeof auth
