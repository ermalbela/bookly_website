// useUserSearch.ts
import { ref, watch } from 'vue'
import { useDebounce } from './useDebounce'
import { authService } from '@/services/auth_service'
import type { UserSearch } from '@/types/user_types'


export function useUserSearch() {
  const query = ref('')
  const results = ref<UserSearch[]>([])
  const isSearching = ref(false)
  const showDropdown = ref(false)
  const debouncedQuery = useDebounce(query, 500)

  watch(query, (val) => {
    if (val.trim()) isSearching.value = true
    else { results.value = []; showDropdown.value = false }
  })

  watch(debouncedQuery, async (val) => {
    if (!val.trim()) {
      isSearching.value = false
      return
    }
    try {
      results.value = await authService.search_users(val)
      showDropdown.value = true
    } catch {
      results.value = []
    } finally {
      isSearching.value = false
    }
  })

  const clear = () => {
    query.value = ''
    results.value = []
    showDropdown.value = false
  }

  return { query, results, isSearching, showDropdown, clear }
}