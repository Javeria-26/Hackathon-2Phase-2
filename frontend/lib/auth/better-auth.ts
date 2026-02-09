// Better Auth Configuration
import { betterAuth } from 'better-auth'
import Database from 'better-sqlite3'
import path from 'path'

// Use absolute path for database file
const dbPath = path.join(process.cwd(), 'auth.db')
const db = new Database(dbPath)

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'development-secret-change-in-production',
  database: db,
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
