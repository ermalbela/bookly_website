<template>
  <div class="max-w-4xl mx-auto space-y-6 pb-12">

    <div class="h-4 w-28 bg-gray-200 rounded animate-pulse" ></div>

    <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
      <div class="h-2 bg-gray-200 animate-pulse" ></div>
      <div class="p-8">
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
          <div class="flex-1 space-y-3">
            <div class="h-8 bg-gray-200 rounded-lg animate-pulse w-3/4" ></div>
            <div class="h-5 bg-gray-100 rounded-lg animate-pulse w-1/3" ></div>
            <div class="flex gap-2 mt-4">
              <div class="h-6 w-16 bg-gray-100 rounded-full animate-pulse" ></div>
              <div class="h-6 w-20 bg-gray-100 rounded-full animate-pulse" ></div>
              <div class="h-6 w-14 bg-gray-100 rounded-full animate-pulse" ></div>
            </div>
          </div>
          <div class="flex flex-col items-center justify-center bg-gray-50 rounded-xl px-6 py-4 border border-gray-100 min-w-28 gap-2">
            <div class="h-8 w-10 bg-gray-200 rounded animate-pulse" ></div>
            <div class="h-4 w-24 bg-gray-100 rounded animate-pulse" ></div>
            <div class="h-3 w-16 bg-gray-100 rounded animate-pulse" ></div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="n in 4" :key="n" class="bg-white rounded-xl shadow-sm p-5 border border-gray-50 space-y-2">
        <div class="h-3 w-16 bg-gray-200 rounded animate-pulse" ></div>
        <div class="h-4 w-24 bg-gray-100 rounded animate-pulse" ></div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm p-8">
      <div class="h-5 w-24 bg-gray-200 rounded animate-pulse mb-6" ></div>

      <div class="space-y-4">
        <div v-for="n in 3" :key="n" class="p-5 bg-gray-50 rounded-xl border border-gray-100 space-y-3">
          <div class="flex items-center justify-between">
            <div class="h-4 w-24 bg-gray-200 rounded animate-pulse" ></div>
            <div class="h-3 w-20 bg-gray-100 rounded animate-pulse" ></div>
          </div>
          <div class="space-y-2">
            <div class="h-3 bg-gray-100 rounded animate-pulse w-full" ></div>
            <div class="h-3 bg-gray-100 rounded animate-pulse w-5/6" ></div>
            <div class="h-3 bg-gray-100 rounded animate-pulse w-2/3" ></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>