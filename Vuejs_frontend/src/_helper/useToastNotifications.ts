import { ref } from 'vue'

interface ToastNotification {
  id: number
  message: string
  color: 'green' | 'red'
}

const notifications = ref<ToastNotification[]>([])

const addToastNotifications = (message: string, color: 'green' | 'red', timer?: number) => {
  const id = Date.now();

  notifications.value.push({
    id,
    message,
    color
  })

  setTimeout(() => removeToastNotifications(id), timer ?? 3000);
}

const removeToastNotifications = (id: number) => {
  notifications.value = notifications.value.filter(n => n.id !== id)
}

export function useToastNotifications() {
  return { notifications, addToastNotifications, removeToastNotifications}
}
