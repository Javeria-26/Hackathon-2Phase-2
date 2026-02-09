'use client'

import { useAuth } from '@/lib/auth/auth-hooks'
import { useRouter } from 'next/navigation'
import styles from './Header.module.css'

export default function Header() {
  const { user, logout } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    await logout()
    router.push('/login')
  }

  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <h2>Todo App</h2>
        </div>
        <div className={styles.userSection}>
          <span className={styles.userEmail}>{user?.email}</span>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}
