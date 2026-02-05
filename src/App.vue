<script setup>
import { ref, computed, onMounted, onUpdated } from 'vue'
import ColorPicker from './components/ColorPicker.vue'
import WigList from './components/WigList.vue'
import ColorCardBrowser from './components/ColorCardBrowser.vue'
import { findNearestWigs } from './utils/colorUtils.js'
import wigsData from './assets/wigs.json'

const selectedColor = ref(null)
const matchedWigs = ref([])
const currentPage = ref('picker') // 'picker' or 'browser'

// Initialize page from URL hash
onMounted(() => {
  checkUrlAndSetPage()
  updateTitle()
  window.addEventListener('hashchange', checkUrlAndSetPage)
})

onUpdated(() => {
  updateTitle()
})

// Check URL hash and set current page
const checkUrlAndSetPage = () => {
  const hash = window.location.hash
  if (hash === '#/browser') {
    currentPage.value = 'browser'
  } else {
    currentPage.value = 'picker'
  }
}

// Update page title based on current view
const updateTitle = () => {
  if (currentPage.value === 'browser') {
    document.title = '色卡浏览器 - MEIS 莓萌 | 拼好头 kigurumi'
  } else {
    document.title = '假发工具 - MEIS 莓萌 | 拼好头 kigurumi'
  }
}

const handleColorSelected = (rgb) => {
  selectedColor.value = rgb
  matchedWigs.value = findNearestWigs(rgb, wigsData, 12)
}

const rgbString = (rgb) => rgb ? `rgb(${rgb.join(',')})` : 'transparent'

// Switch page and update URL hash
const switchPage = (page) => {
  currentPage.value = page
  if (page === 'browser') {
    window.location.hash = '#/browser'
  } else {
    window.location.hash = '#/'
  }
}

// Filter to only show 千型 wigs if on browser page
const filteredWigsData = computed(() => {
  if (currentPage.value === 'browser') {
    return wigsData.filter(wig => wig.brand === '千型')
  }
  return wigsData
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 font-sans">
    <header class="mb-6 text-center">
      <h1 class="text-2xl font-bold" :style="{color: '#df6f92'}">
        <template v-if="currentPage === 'picker'">✨ 假发色彩匹配助手</template>
        <template v-else>🎨 色卡浏览器</template>
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        <template v-if="currentPage === 'picker'">上传图片 -> 点击颜色 -> 自动匹配</template>
        <template v-else>浏览所有可用的色卡，支持按色系和色号排序</template>
      </p>
      
      <!-- Navigation -->
      <nav class="mt-3 flex justify-center gap-4">
        <button
          @click="switchPage('picker')"
          :class="['px-4 py-2 rounded-lg text-sm font-medium transition-colors', currentPage === 'picker' ? 'text-white' : 'text-gray-700 hover:bg-gray-300']"
          :style="{ 
            backgroundColor: currentPage === 'picker' ? '#df6f92' : 'bg-gray-200',
            color: currentPage === 'picker' ? 'white' : 'inherit'
          }"
        >
          色彩匹配
        </button>
        <button
          @click="switchPage('browser')"
          :class="['px-4 py-2 rounded-lg text-sm font-medium transition-colors', currentPage === 'browser' ? 'text-white' : 'text-gray-700 hover:bg-gray-300']"
          :style="{ 
            backgroundColor: currentPage === 'browser' ? '#df6f92' : 'bg-gray-200',
            color: currentPage === 'browser' ? 'white' : 'inherit'
          }"
        >
          色卡浏览
        </button>
      </nav>
    </header>
    
    <main class="max-w-4xl mx-auto flex flex-col items-center gap-8">
      <!-- Color Picker View -->
      <div v-if="currentPage === 'picker'">
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
          <h2 class="text-lg font-bold text-gray-700 mb-4 px-2 border-l-4" :style="{borderLeftColor: '#df6f92'}">
            推荐假发色号
          </h2>
          <WigList :wigs="matchedWigs" />
        </section>
        
        <!-- Empty State -->
        <div v-else-if="!selectedColor" class="text-center text-gray-400 py-12">
          <p>还没有选择颜色哦 ~</p>
        </div>
      </div>

      <!-- Color Card Browser View -->
      <div v-else-if="currentPage === 'browser'">
        <ColorCardBrowser />
      </div>
    </main>
    
    <!-- Disclaimer -->
    <section class="max-w-2xl mx-auto mt-8 px-4">
      <div class="bg-gray-100 rounded-lg p-4 text-sm text-gray-600">
        <p class="mb-2"><strong>📌 使用说明</strong></p>
        <p class="mb-2">本工具用于快速筛选假发色号。由于屏幕显示与实物在不同光线条件下存在色差，专业工作室建议自备实物色卡进行最终确认。</p>
        <p>以上假发均可在 <a href="https://www.taobao.com" target="_blank" class="text-[#df6f92] hover:underline">淘宝</a> 搜索对应品牌和色号购买。</p>
      </div>
    </section>

    <footer class="mt-8 text-center text-xs text-gray-300 pb-8 flex flex-col items-center gap-2">
      <div class="text-sm text-gray-600">
        © 2026 MEIS 莓萌 | 拼好头 kigurumi - QQ群: 1036511798
      </div>
      <div class="flex gap-4">
        <a href="https://kigis.me" target="_blank" class="text-gray-600 hover:opacity-75 transition-opacity font-medium">
          MEIS 莓萌
        </a>
        <span class="text-gray-200">|</span>
        <a href="https://twitter.com/KigMEIS" target="_blank" class="text-[#df6f92] hover:opacity-75 transition-opacity font-medium">
          @KigMEIS
        </a>
        <span class="text-gray-200">|</span>
        <a href="https://github.com/nijino-iot/wig-color-matcher" target="_blank" class="text-gray-600 hover:opacity-75 transition-opacity font-medium">
          GitHub
        </a>
      </div>
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