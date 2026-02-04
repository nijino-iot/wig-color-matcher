<script setup>
defineProps(['wigs'])

// 使用 import.meta.env.BASE_URL 获取基础路径 (vite.config.js 中配置的 /wig/)
const baseUrl = import.meta.env.BASE_URL

const formatDistance = (d) => d.toFixed(2)
const getWigImage = (filename) => {
  // 必须对文件名进行编码，因为文件名中包含 '#' (会被浏览器识别为锚点)
  return `${baseUrl}wig_cards/${encodeURIComponent(filename)}`
}
</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full">
    <div 
      v-for="wig in wigs" 
      :key="wig.filename"
      class="border rounded-lg p-2 shadow-sm bg-white flex flex-col items-center hover:shadow-md transition-shadow"
    >
      <div class="w-24 h-24 mb-2 overflow-hidden rounded bg-gray-100 relative">
        <img 
          :src="getWigImage(wig.filename)" 
          class="w-full h-full object-cover" 
          loading="lazy"
        />
        <!-- Color swatch overlay -->
        <div 
            class="absolute bottom-0 right-0 w-6 h-6 border border-white shadow-sm"
            :style="{ backgroundColor: `rgb(${wig.rgb.join(',')})` }"
        ></div>
      </div>
      
      <div class="text-center w-full">
        <h3 class="font-bold text-gray-800 text-sm truncate w-full">{{ wig.brand }} {{ wig.code }}</h3>
        <p class="text-xs text-gray-600 truncate w-full">{{ wig.color_name }}</p>
        <span class="text-[10px] text-gray-400 mt-1 block">匹配度: {{ formatDistance(wig.distance) }}</span>
      </div>
    </div>
  </div>
</template>
