'use client'

import { useState } from 'react'
import { validateTodoTitle, validateTodoDescription } from '@/lib/utils/validation'
import { todoApi } from '@/lib/api/todos'
import { useAuth } from '@/lib/auth/auth-hooks'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import ErrorMessage from '@/components/ui/ErrorMessage'
import styles from './TodoForm.module.css'

interface TodoFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export default function TodoForm({ onSuccess, onCancel }: TodoFormProps) {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    title: '',
    description: ''
  })
  const [errors, setErrors] = useState({
    title: '',
    description: ''
  })
  const [apiError, setApiError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateForm = (): boolean => {
    const newErrors = {
      title: '',
      description: ''
    }

    const titleValidation = validateTodoTitle(formData.title)
    if (!titleValidation.isValid) {
      newErrors.title = titleValidation.error || 'Invalid title'
    }

    const descriptionValidation = validateTodoDescription(formData.description)
    if (!descriptionValidation.isValid) {
      newErrors.description = descriptionValidation.error || 'Invalid description'
    }

    setErrors(newErrors)
    return !newErrors.title && !newErrors.description
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setApiError(null)

    if (!validateForm()) {
      return
    }

    if (!user?.id) {
      setApiError('User not authenticated')
      return
    }

    setIsSubmitting(true)

    try {
      await todoApi.create(user.id, {
        title: formData.title.trim(),
        description: formData.description.trim() || undefined
      })

      // Reset form
      setFormData({ title: '', description: '' })
      setErrors({ title: '', description: '' })

      // Notify parent of success
      onSuccess()
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to create task')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleChange = (field: 'title' | 'description', value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
    // Clear API error when user makes changes
    if (apiError) {
      setApiError(null)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      {apiError && (
        <ErrorMessage
          message={apiError}
          onDismiss={() => setApiError(null)}
        />
      )}

      <Input
        label="Title"
        type="text"
        value={formData.title}
        onChange={(e) => handleChange('title', e.target.value)}
        error={errors.title}
        placeholder="Enter task title"
        required
        disabled={isSubmitting}
      />

      <div className={styles.textareaGroup}>
        <label htmlFor="description" className={styles.label}>
          Description (optional)
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) => handleChange('description', e.target.value)}
          placeholder="Enter task description"
          className={`${styles.textarea} ${errors.description ? styles.textareaError : ''}`}
          rows={4}
          disabled={isSubmitting}
        />
        {errors.description && (
          <span className={styles.errorText}>{errors.description}</span>
        )}
      </div>

      <div className={styles.actions}>
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          variant="primary"
          isLoading={isSubmitting}
          disabled={isSubmitting}
        >
          Create Task
        </Button>
      </div>
    </form>
  )
}
