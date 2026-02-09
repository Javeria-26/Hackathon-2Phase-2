import { Todo } from '@/types/todo'
import TodoItem from './TodoItem'
import styles from './TodoList.module.css'

interface TodoListProps {
  todos: Todo[]
}

export default function TodoList({ todos }: TodoListProps) {
  if (todos.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p className={styles.emptyText}>No tasks yet!</p>
        <p className={styles.emptySubtext}>Create your first task to get started</p>
      </div>
    )
  }

  return (
    <div className={styles.todoList}>
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  )
}
