<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm">
    <div class="flex flex-col md:flex-col md:items-end md:justify-between mb-8">
      <div class="flex justify-start flex-row w-full">
        <h1 class="text-3xl font-bold">Tags</h1>
      </div>

      <div class="mt-4 flex justify-end">
        <button
          v-if="authStore?.user?.role === 'admin'"
          class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer active:bg-emerald-900"
          @click="tagIsOpen = true"
        >
          Add Tag
        </button>
      </div>
    </div>
    <div class="border-gray-300 border rounded-sm border-l p-5">
      <div
        v-if="loading"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        Tags Loading...
      </div>

      <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>

      <div v-else-if="tags.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm">
        <h2 class="text-xl font-semibold text-gray-800">No tags yet</h2>
        <p class="text-gray-500 mt-2">Add your first tag</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="tag in tags"
          :key="tag.uid"
          class="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group"
        >
          <div class="h-2"></div>
          <div class="p-5 flex flex-col h-full">
            <div class="flex justify-between">
              <h2 class="text-lg font-semibold text-gray-900transition">
                {{ tag.name }}
              </h2>
              <button
                class="ml-2 text-red-500 cursor-pointer active:text-red-900"
                @click="deleteTag(tag.uid)"
              >
                <i class="pi pi-times-circle"></i>
              </button>
            </div>

            <div class="mt-auto pt-4 flex items-center">
              <span class="text-xs text-gray-400"> id: {{ tag.uid }} </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CommonModal v-model="tagIsOpen" title="Add Tag" size="md">
      <div v-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl">{{ error }}</div>
      <div>
        <label class="text-sm font-medium text-gray-700">Tag Name</label>
        <input
          v-model="tagValue"
          type="text"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Tag Name..."
        />
      </div>

      <template #footer>
        <button
          @click="tagIsOpen = false"
          class="px-4 py-2 text-sm font-medium rounded-lg text-gray-800 bg-gray-300 cursor-pointer"
        >
          Cancel
        </button>
        <button
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 cursor-pointer"
          @click="addTag(tagValue)"
        >
          Add Tag
        </button>
      </template>
    </CommonModal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { tagService } from '@/services/tag_service'
import { useAuthStore } from '@/stores/auth_store'
import CommonModal from '@/components/modals/CommonModal.vue'
import { useToastNotifications } from '@/_helper/useToastNotifications'

const authStore = useAuthStore()
const toastNotifications = useToastNotifications();

const tags = ref<{ name: string; uid: string }[]>([])
const loading = ref(true)
const error = ref('')
const tagIsOpen = ref(false);
const tagValue = ref('');

const addTag = async (tag_name: string) => {
  try {
    const response = await tagService.create_tag(tag_name)
    console.log(response);
    tags.value = await tagService.get_all_tags();
    tagIsOpen.value = false;
    tagValue.value = '';
    toastNotifications.addToastNotifications(`Tag '${response.name ?? ''}' added.`, 'green')
  } catch (e: any) {
    console.log(e.response.data)
    toastNotifications.addToastNotifications(e.response.data.detail ?? 'Something went wrong', 'red', 5000)
  }
}

const deleteTag = async (tag_uid: string) => {
  if (!tag_uid) return

  try {
    await tagService.delete_tag(tag_uid)
    toastNotifications.addToastNotifications('Tag deleted successfully.', 'green')
    tags.value = await tagService.get_all_tags()
  } catch (e: any) {
    console.log(e.response.data)
    toastNotifications.addToastNotifications(e.response.data.detail ?? 'Something went wrong', 'red', 5000)
  }
}

onMounted(async () => {
  try {
    tags.value = await tagService.get_all_tags()
  } catch (e: any) {
    error.value = 'Failed to load tags'
  } finally {
    loading.value = false
  }
})
</script>
