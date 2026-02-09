import { Todo } from '@/types/todo'
import styles from './TodoItem.module.css'

interface TodoItemProps {
  todo: Todo
}

export default function TodoItem({ todo }: TodoItemProps) {
  return (
    <div className={`${styles.todoItem} ${todo.completed ? styles.completed : ''}`}>
      <div className={styles.content}>
        <h3 className={styles.title}>{todo.title}</h3>
        {todo.description && <p className={styles.description}>{todo.description}</p>}
      </div>
      <div className={styles.meta}>
        <span className={styles.status}>
          {todo.completed ? '✓ Completed' : 'Pending'}
        </span>
      </div>
    </div>
  )
}
