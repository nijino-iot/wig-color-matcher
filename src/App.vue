<script setup>
import { ref } from 'vue'
import ColorPicker from './components/ColorPicker.vue'
import WigList from './components/WigList.vue'
import { findNearestWigs } from './utils/colorUtils.js'
import wigsData from './assets/wigs.json'

const selectedColor = ref(null)
const matchedWigs = ref([])

const handleColorSelected = (rgb) => {
  selectedColor.value = rgb
  matchedWigs.value = findNearestWigs(rgb, wigsData, 12)
}

const rgbString = (rgb) => rgb ? `rgb(${rgb.join(',')})` : 'transparent'

</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 font-sans">
    <header class="mb-6 text-center">
      <h1 class="text-2xl font-bold text-gray-800">✨ 假发色彩匹配助手</h1>
      <p class="text-sm text-gray-500 mt-1">上传图片 -> 点击颜色 -> 自动匹配</p>
    </header>
    
    <main class="max-w-4xl mx-auto flex flex-col items-center gap-8">
      
      <!-- Upload and Picker Area -->
      <section class="w-full flex flex-col items-center bg-white p-6 rounded-xl shadow-sm">
        <ColorPicker @colorSelected="handleColorSelected" />
        
        <!-- Selected Color Preview -->
        <div 
          v-if="selectedColor" 
          class="mt-6 flex items-center gap-3 animate-fade-in"
        >
          <span class="text-sm text-gray-600 font-medium">选中的颜色:</span>
          <div 
            class="w-12 h-12 rounded-full shadow-inner border border-gray-200 transition-colors duration-300"
            :style="{ backgroundColor: rgbString(selectedColor) }"
          ></div>
          <div class="text-xs text-gray-400 font-mono">
            R:{{selectedColor[0]}} G:{{selectedColor[1]}} B:{{selectedColor[2]}}
          </div>
        </div>
      </section>

      <!-- Results Area -->
      <section v-if="matchedWigs.length > 0" class="w-full">
        <h2 class="text-lg font-bold text-gray-700 mb-4 px-2 border-l-4 border-blue-500">
          推荐假发色号
        </h2>
        <WigList :wigs="matchedWigs" />
      </section>
      
      <!-- Empty State -->
      <div v-else-if="!selectedColor" class="text-center text-gray-400 py-12">
        <p>还没有选择颜色哦 ~</p>
      </div>
      
    </main>
    
    <footer class="mt-12 text-center text-xs text-gray-300 pb-4 flex flex-col items-center gap-2">
      <a href="https://kigis.me" target="_blank" class="text-blue-400 hover:text-blue-300 transition-colors">
        MEIS 莓萌 (Kigurumi Studio)
      </a>
      <span>© 2026 Nijino IOT & MEIS</span>
    </footer>
  </div>
</template>

<style>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
