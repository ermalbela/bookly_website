<template>
  <aside class="w-64 bg-white text-black flex flex-col border-r border-gray-300 shadow-sm tracking-widest">
    <div class="flex flex-col items-center justify-center px-5 pt-7 pb-2 border-b border-gray-300">
      <div class="flex items-end w-full justify-end">
        <i class="pi pi-spin pi-cog text-gray-700 cursor-pointer rounded-full active:text-gray-900" style="font-size: 2rem"></i>
      </div>

      <template v-if="!authStore.isReady">
        <div class="w-30 h-30 rounded-full bg-gray-200 animate-pulse"></div>
        <div class="mt-10 w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
      </template>

      <template v-else>
        <div class="relative group mt-2">
          <img
            :src="authStore.user?.avatar_url"
            class="border-3 border-blue-300 w-30 h-30 rounded-full object-cover"
          />
          <div
            class="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center
                  opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
            @click="fileInput?.click()"
          >
            <i class="pi pi-camera text-white" style="font-size: 1.4rem"></i>
          </div>

          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleAvatarChange"
          />
          <div
            v-if="uploading"
            class="absolute inset-0 rounded-full bg-black/50 flex items-center justify-center"
          >
            <i class="pi pi-spin pi-spinner text-white" style="font-size: 1.4rem"></i>
          </div>
        </div>
        <h3 class="text-center text-sm mt-10 font-medium text-gray-900">
          {{ authStore.user?.username }}
        </h3>
        <h4 :class="{
          'text-center text-sm font-medium mt-1': true,
          'text-red-500': authStore.user?.role === 'admin',
          'text-green-600': authStore.user?.role === 'user'
        }">
          {{ authStore.user?.role?.toUpperCase() }}
        </h4>
      </template>
    </div>

    <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
      <RouterLink
        v-for="item in sidebar_items"
        :key="item.name"
        :to="item.path"
        :class="{
          'text-sm font-semibold block px-4 py-2 rounded hover:bg-blue-500 hover:text-white active:bg-blue-600': true,
          'bg-blue-500 text-white': currentTab === item.name,
        }"
        @click="emit('update:currentTab', item.name)"
      >
        {{ item.name }}
      </RouterLink>
    </nav>

    <div class="p-4 border-t border-gray-300 text-sm text-gray-800">2026 Bookly</div>
  </aside>
</template>

<script setup lang="ts">

import {ref} from 'vue';
import { useAuthStore } from '@/stores/auth_store'
import { sidebar_items } from '@/MENUITEMS'
import { authService } from '@/services/auth_service';
import { useToastNotifications } from '@/_helper/useToastNotifications';

const authStore = useAuthStore();
const toastNotification = useToastNotifications();

const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const handleAvatarChange = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return

  uploading.value = true

  try {
    const formData = new FormData()
    formData.append('file', file)
    const response = await authService.update_avatar(formData)
    if (authStore.user) authStore.user.avatar_url = response.avatar_url
    toastNotification.addToastNotifications('Image uploaded successfully.', 'green')
  } catch (err: any) {
    console.error(err.response);
    toastNotification.addToastNotifications(err.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

defineProps<{
  currentTab: string
}>()

const emit = defineEmits<{
  'update:currentTab': [value: string]
}>()

</script>