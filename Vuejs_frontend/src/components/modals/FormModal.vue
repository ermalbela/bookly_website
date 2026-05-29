<template>
  <CommonModal v-model="isOpen" title="Add Book" size="md">
    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>
    <div class="space-y-4 grid grid-cols-2 gap-4">
      <div>
        <label class="text-sm font-medium text-gray-700">Title</label>
        <input
          v-model="form.title"
          type="text"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Book Title"
        />
      </div>
      <div>
        <label class="text-sm font-medium text-gray-700">Author</label>
        <input
          v-model="form.author"
          type="text"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Author Name"
        />
      </div>
      <div>
        <label class="text-sm font-medium text-gray-700">Publisher</label>
        <input
          v-model="form.publisher"
          type="text"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Publisher"
        />
      </div>
      <div>
        <label class="text-sm font-medium text-gray-700">Published Date</label>
        <input
          v-model="form.published_date"
          type="date"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Published Date"
        />
      </div>
      <div>
        <label class="text-sm font-medium text-gray-700">Page Count</label>
        <input
          v-model="form.page_count"
          type="number"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Page Count"
        />
      </div>
      <div>
        <label class="text-sm font-medium text-gray-700">Language</label>
        <input
          v-model="form.language"
          type="text"
          class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Language"
        />
      </div>
    </div>

    <template #footer>
      <button
        @click="isOpen = false"
        class="px-4 py-2 text-sm font-medium rounded-lg text-gray-800 bg-gray-300 cursor-pointer"
      >
        Cancel
      </button>
      <button
        class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 cursor-pointer"
        @click="handleSave()"
      >
        Save Book
      </button>
    </template>
  </CommonModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import CommonModal from './CommonModal.vue'
import type { BookCreateModel } from '@/types/book_types'
import { patterns } from '@/Validation'

const isOpen = ref(false)

const form = reactive({
  title: '',
  author: '',
  publisher: '',
  published_date: '',
  page_count: '',
  language: '',
})
const error = ref('');

const emit = defineEmits<{
  save: [data: BookCreateModel],
}>()


const open = () => { isOpen.value = true }
const close = () => {isOpen.value = false}

const handleSave = () => {
  if(!patterns.name.test(form.title) || form.title === ''){
    error.value = 'Please fill the title field.'
    return;
  }
  if(!patterns.name.test(form.author) || form.author === ''){
    error.value = 'Please fill the author field.'
    return;
  }
  if(!patterns.name.test(form.language) || form.language === ''){
    error.value = 'Please fill the language field.'
    return;
  }
  if(!patterns.name.test(form.publisher) || form.publisher === ''){
    error.value = 'Please fill the publisher field.'
    return;
  }
  if(!form.published_date){
    error.value = 'Please fill the published date field.'
    return;
  }
  if(!form.page_count){
    error.value = 'Please fill the page count field.'
    return;
  }
  try{
    emit('save', { ...form, page_count: Number(form.page_count)})
    error.value = '';
    form.author = '';
    form.language = '';
    form.page_count = '';
    form.published_date = '';
    form.publisher = '';
    form.title = '';
  } catch(e){
    console.log(e);
  } finally{
    close();
  }
}

defineExpose({ open, close })
</script>
