<template>
  <div class="relative">
    <div class="relative">
      <input
        v-model="query"
        type="text"
        placeholder="Search users..."
        class="w-full bg-white border-b border-gray-300 px-4 py-2 pr-10 focus:outline-none focus:border-b focus:border-gray-700 text-sm"
        @focus="showDropdown = results.length > 0"
        @blur="handleBlur"
      />
      <i v-if="isSearching" class="pi pi-spin pi-spinner absolute right-3 top-2.5 text-gray-400"></i>
      <i v-else-if="query" class="pi pi-times absolute right-3 top-2.5 text-gray-400 cursor-pointer" @click="clear"></i>
    </div>

    <ul
      v-if="showDropdown && results.length > 0"
      class="absolute z-50 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-64 overflow-y-auto"
    > 
      <li
        v-for="user in results"
        :key="user.uid"
        @click="goToProfile(user.uid)"
        class="flex items-center gap-3 px-4 py-3 hover:bg-blue-50 cursor-pointer transition-colors"
      >
        <img
          :src="user.avatar_url ?? `https://ui-avatars.com/api/?name=${user.username}&background=random`"
          class="w-8 h-8 rounded-full object-cover"
        />
        <div>
          <p class="text-sm font-medium text-gray-800">{{ user.username }}</p>
          <p class="text-xs text-gray-400">{{ user.first_name }} {{ user.last_name }}</p>
        </div>
      </li>
    </ul>

    <div
      v-else-if="showDropdown && query && !isSearching"
      class="absolute z-50 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg px-4 py-3 text-sm text-gray-400"
    >
      No users found.
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserSearch } from '@/_helper/useSearchUsers'
import { useRouter } from 'vue-router'

const router = useRouter()
const { query, results, isSearching, showDropdown, clear } = useUserSearch()

const goToProfile = (uid: string) => {
  clear();
  router.push({ name: 'user_profile', params: { uid } })
}

const handleBlur = () => {
  setTimeout(() => { showDropdown.value = false }, 150)
}
</script>