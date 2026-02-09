// Todo API Methods
import apiClient from './client'
import { Todo, TodoFormData } from '@/types/todo'

interface TodoResponse {
  task: Todo
}

interface TodoListResponse {
  tasks: Todo[]
}

export const todoApi = {
  getAll: async (userId: string): Promise<Todo[]> => {
    const response = await apiClient.get<TodoListResponse>(`/api/${userId}/tasks`)
    return response.tasks
  },

  create: async (userId: string, data: TodoFormData): Promise<Todo> => {
    const response = await apiClient.post<TodoResponse>(`/api/${userId}/tasks`, data)
    return response.task
  },

  getById: async (userId: string, id: string): Promise<Todo> => {
    const response = await apiClient.get<TodoResponse>(`/api/${userId}/tasks/${id}`)
    return response.task
  },

  update: async (userId: string, id: string, data: TodoFormData): Promise<Todo> => {
    const response = await apiClient.put<TodoResponse>(`/api/${userId}/tasks/${id}`, data)
    return response.task
  },

  complete: async (userId: string, id: string, completed: boolean): Promise<Todo> => {
    const response = await apiClient.patch<TodoResponse>(
      `/api/${userId}/tasks/${id}/complete`,
      { completed }
    )
    return response.task
  },

  delete: async (userId: string, id: string): Promise<void> => {
    await apiClient.delete(`/api/${userId}/tasks/${id}`)
  },
}
