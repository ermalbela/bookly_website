<template>
  <Teleport to="body">
    <Transition name="modal">
      <KeepAlive>
        <div
          v-if="modelValue"
          class="fixed inset-0 z-50 flex items-center justify-center px-4"
        >
          <div 
            class="absolute inset-0 bg-black/40 backdrop-blur-sm"
            @click.self="closeOnBackdrop && emit('update:modelValue', false)"
          ></div>

          <div
            class="relative bg-white rounded-2xl shadow-xl w-full flex flex-col overflow-hidden max-h-[90vh]"
            :class="sizeClass"
          >
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
              <div>
                <h2 class="text-lg font-semibold text-gray-900">{{ title }}</h2>
              </div>
              <button
                @click="emit('update:modelValue', false)"
                class="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full p-1.5 transition-colors"
                aria-label="Close modal"
              >
                <i class="pi pi-times-circle" style="font-size: 1.3rem"></i>
              </button>
            </div>

            <div class="px-6 py-5 overflow-y-auto flex-1 max-h-[70vh]">
              <slot></slot>
            </div>

            <div
              v-if="$slots.footer"
              class="px-6 py-4 border-t border-gray-100 flex items-center justify-end gap-3"
            >
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </KeepAlive>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    title: string
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
    closeOnBackdrop?: boolean
  }>(),
  {
    size: 'md',
    closeOnBackdrop: true,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const sizeClass = computed(() => ({
  'max-w-sm': props.size === 'sm',
  'max-w-lg': props.size === 'md',
  'max-w-2xl': props.size === 'lg',
  'max-w-5xl': props.size === 'xl',
  'max-w-full min-h-screen rounded-none': props.size === 'full',
}))

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.modelValue) {
    emit('update:modelValue', false)
  }
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: translateY(12px);
  opacity: 0;
}
</style>
