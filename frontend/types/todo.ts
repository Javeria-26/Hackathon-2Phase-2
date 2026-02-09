// Todo Types

export interface Todo {
  id: string
  title: string
  description: string
  completed: boolean
  userId: string
  createdAt: string
  updatedAt: string
}

export interface TodoListState {
  todos: Todo[]
  loading: boolean
  error: string | null
}

export interface TodoFormData {
  title: string
  description: string
}
