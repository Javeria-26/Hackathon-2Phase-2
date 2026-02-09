'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth/auth-hooks'
import { todoApi } from '@/lib/api/todos'
import { Todo } from '@/types/todo'
import TodoList from '@/components/todo/TodoList'
import TodoForm from '@/components/todo/TodoForm'
import Modal from '@/components/ui/Modal'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import ErrorMessage from '@/components/ui/ErrorMessage'
import styles from './page.module.css'

export default function DashboardPage() {
  const { user } = useAuth()
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    if (user?.id) {
      fetchTodos()
    }
  }, [user?.id])

  const fetchTodos = async () => {
    if (!user?.id) return

    try {
      setLoading(true)
      setError(null)
      const fetchedTodos = await todoApi.getAll(user.id)
      setTodos(fetchedTodos)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to fetch todos'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  const handleFormSuccess = () => {
    setIsModalOpen(false)
    fetchTodos()
  }

  if (loading) {
    return (
      <div className={styles.container}>
        <LoadingSpinner size="large" />
      </div>
    )
  }

  if (error) {
    return (
      <div className={styles.container}>
        <ErrorMessage message={error} onDismiss={() => setError(null)} />
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          <h1 className={styles.title}>My Tasks</h1>
          <Button
            variant="primary"
            onClick={() => setIsModalOpen(true)}
          >
            + Add Task
          </Button>
        </div>
        <TodoList todos={todos} />
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Create New Task"
      >
        <TodoForm
          onSuccess={handleFormSuccess}
          onCancel={() => setIsModalOpen(false)}
        />
      </Modal>
    </div>
  )
}
