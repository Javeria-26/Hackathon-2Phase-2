import React from 'react'
import styles from './ErrorMessage.module.css'

interface ErrorMessageProps {
  message: string
  onDismiss?: () => void
}

export default function ErrorMessage({ message, onDismiss }: ErrorMessageProps) {
  return (
    <div className={styles.errorContainer}>
      <div className={styles.errorContent}>
        <span className={styles.errorIcon}>⚠️</span>
        <span className={styles.errorText}>{message}</span>
      </div>
      {onDismiss && (
        <button className={styles.dismissButton} onClick={onDismiss} aria-label="Dismiss">
          ×
        </button>
      )}
    </div>
  )
}
