<template>
  <div class="w-full max-w-6xl mx-auto p-4">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">🎨 色卡浏览器</h1>
      <p class="text-sm text-gray-600">浏览所有可用的色卡，支持按品牌、色系和色号排序</p>
    </div>

    <!-- Controls -->
    <div class="bg-white rounded-lg shadow-sm p-4 mb-6 flex flex-wrap gap-4 items-center">
      <div class="flex items-center gap-2">
        <label class="text-sm font-medium text-gray-700">排序方式:</label>
        <select 
          v-model="sortBy" 
          class="border border-gray-300 rounded px-3 py-1 text-sm focus:outline-none focus:ring-2"
          :style="{ 'box-shadow': '0 0 0 2px rgba(223, 111, 146, 0.2)' }"
        >
          <option value="brand_code">品牌+色号</option>
          <option value="hue">色系</option>
          <option value="brightness">亮度</option>
          <option value="saturation">饱和度</option>
          <option value="brand">品牌</option>
        </select>
      </div>

      <div class="flex items-center gap-2">
        <label class="text-sm font-medium text-gray-700">筛选品牌:</label>
        <select 
          v-model="selectedBrand" 
          class="border border-gray-300 rounded px-3 py-1 text-sm focus:outline-none focus:ring-2"
          :style="{ 'box-shadow': '0 0 0 2px rgba(223, 111, 146, 0.2)' }"
        >
          <option value="all">全部</option>
          <option v-for="brand in availableBrands" :key="brand" :value="brand">{{ brand }}</option>
        </select>
      </div>

      <div class="flex-1 min-w-[200px]">
        <input
          v-model="searchTerm"
          placeholder="搜索色号或颜色..."
          class="w-full border border-gray-300 rounded px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <!-- Stats -->
    <div class="bg-white rounded-lg shadow-sm p-4 mb-6">
      <div class="flex flex-wrap gap-6 text-sm text-gray-600">
        <div>总数: <span class="font-medium text-gray-800">{{ filteredCards.length }}</span></div>
        <div v-for="(count, brand) in brandCounts" :key="brand">
          {{ brand }}: <span class="font-medium text-gray-800">{{ count }}</span>
        </div>
        <div v-if="sortBy === 'hue'">色系分布: <span class="font-medium text-gray-800">{{ hueDistribution }}</span></div>
      </div>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- Color Cards Grid -->
    <div v-else class="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-12 lg:grid-cols-16 xl:grid-cols-20 gap-2">
      <div 
        v-for="card in displayedCards" 
        :key="card.filename"
        class="flex flex-col items-center p-1 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer group"
        @click="selectCard(card)"
        :title="`${card.brand} ${card.code}`"
      >
        <div class="w-12 h-12 mb-1 rounded overflow-hidden border border-gray-200 shadow-sm relative">
          <img 
            :src="card.imageUrl" 
            :alt="`${card.brand} ${card.code}`"
            class="w-full h-full object-cover"
            loading="lazy"
            @error="onImageError"
          />
          <!-- Color swatch overlay -->
          <div 
            class="absolute bottom-0 right-0 w-4 h-4 border border-white shadow-sm"
            :style="{ backgroundColor: `rgb(${card.rgb.join(',')})` }"
          ></div>
        </div>
        <div class="text-xs text-center">
          <div class="text-gray-700 truncate w-full">{{ card.code }}</div>
          <div class="text-gray-500 truncate w-full">{{ getBrandShortName(card.brand) }}</div>
        </div>
      </div>
    </div>

    <!-- Selected Card Modal -->
    <div 
      v-if="selectedCard" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click="selectedCard = null"
    >
      <div 
        class="bg-white rounded-xl max-w-md w-full max-h-[90vh] overflow-y-auto p-6"
        @click.stop
      >
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-lg font-bold text-gray-800">{{ selectedCard.brand }} {{ selectedCard.code }}</h3>
          <button 
            @click="selectedCard = null"
            class="text-gray-400 hover:text-gray-600 text-xl"
          >
            ×
          </button>
        </div>
        
        <div class="flex flex-col items-center">
          <div class="w-32 h-32 mb-4 rounded-lg overflow-hidden border border-gray-200 shadow-sm">
            <img 
              :src="selectedCard.imageUrl" 
              :alt="`${selectedCard.brand} ${selectedCard.code}`"
              class="w-full h-full object-contain"
              @error="onModalImageError"
            />
          </div>
          
          <div class="text-center mb-2" v-if="selectedCard.color_name">
            <div class="text-sm font-medium text-gray-700">{{ selectedCard.color_name }}</div>
          </div>
          
          <div class="text-center mb-4">
            <div class="text-sm text-gray-600 mb-1">RGB值</div>
            <div class="font-mono text-sm bg-gray-100 px-3 py-1 rounded">
              {{ selectedCard.rgb.join(', ') }}
            </div>
          </div>
          
          <div class="flex gap-2">
            <div class="text-center">
              <div class="text-xs text-gray-500">色调</div>
              <div class="text-sm font-medium">{{ Math.round(selectedCard.hsl[0]) }}°</div>
            </div>
            <div class="text-center">
              <div class="text-xs text-gray-500">饱和度</div>
              <div class="text-sm font-medium">{{ Math.round(selectedCard.hsl[1]) }}%</div>
            </div>
            <div class="text-center">
              <div class="text-xs text-gray-500">亮度</div>
              <div class="text-sm font-medium">{{ Math.round(selectedCard.hsl[2]) }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// State
const sortBy = ref('brand_code') // 'brand_code', 'hue', 'brightness', 'saturation', 'brand'
const selectedBrand = ref('all')
const searchTerm = ref('')
const selectedCard = ref(null)
const loading = ref(true)

// Base URL for images
const baseUrl = import.meta.env.BASE_URL

// Load all wigs
const allWigs = ref([])

onMounted(async () => {
  try {
    // Load the wigs data from the existing JSON
    const response = await fetch(`${baseUrl}assets/wigs.json`)
    const data = await response.json()
    
    // Process the data to add image URLs and HSL values
    allWigs.value = data.map(wig => ({
      ...wig,
      imageUrl: `${baseUrl}wig_cards/${encodeURIComponent(wig.filename)}`,
      hsl: rgbToHsl(wig.rgb)
    }))
    
    loading.value = false
  } catch (error) {
    console.error('Failed to load wigs data:', error)
    // Fallback: try loading from the local asset if deployed
    try {
      const wigsData = await import('../assets/wigs.json')
      allWigs.value = wigsData.default.map(wig => ({
        ...wig,
        imageUrl: `${baseUrl}wig_cards/${encodeURIComponent(wig.filename)}`,
        hsl: rgbToHsl(wig.rgb)
      }))
      loading.value = false
    } catch (fallbackError) {
      console.error('Fallback also failed:', fallbackError)
      loading.value = false
    }
  }
})

// RGB to HSL conversion
function rgbToHsl(rgb) {
  let [r, g, b] = rgb
  r /= 255, g /= 255, b /= 255;

  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;

  if (max === min) {
    h = s = 0; // achromatic
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    
    h /= 6;
  }

  return [
    Math.round(h * 360),
    Math.round(s * 100),
    Math.round(l * 100)
  ];
}

// Get short name for brand to display in grid (two characters)
function getBrandShortName(brand) {
  if (!brand) return '??'
  // Return two characters for each brand
  if (brand.includes('千型')) return '千型'
  if (brand.includes('曼柒')) return '曼柒'
  if (brand.includes('漫供')) return '漫供'
  if (brand.startsWith('漫美')) return '漫美'  // All brands starting with 漫美 go under 漫美
  if (brand.includes('漫舞')) return '漫舞'
  if (brand === 'Unknown' || brand.includes('秀琴')) return '秀琴'  // Unknown brands and brands containing 秀琴 go under 秀琴
  if (brand.length >= 2) return brand.substring(0, 2)
  return brand + (brand.length === 0 ? '?' : '')
}

// Handle image errors
function onImageError(event) {
  // Set a fallback color or image
  event.target.style.backgroundColor = '#f0f0f0'
  event.target.style.display = 'flex'
  event.target.style.alignItems = 'center'
  event.target.style.justifyContent = 'center'
  event.target.textContent = '❌'
}

function onModalImageError(event) {
  event.target.style.backgroundColor = '#f0f0f0'
  event.target.style.display = 'flex'
  event.target.style.alignItems = 'center'
  event.target.style.justifyContent = 'center'
  event.target.textContent = 'No Image'
}

// Computed properties
const availableBrands = computed(() => {
  // Normalize brands so those named 'Unknown' or containing '秀琴' are grouped as '秀琴', and '漫美' brands are grouped as '漫美'
  const normalizedBrands = allWigs.value.map(wig => {
    if (wig.brand === 'Unknown' || wig.brand.includes('秀琴')) {
      return '秀琴'
    } else if (wig.brand.startsWith('漫美')) {
      return '漫美'
    } else {
      return wig.brand
    }
  })
  return [...new Set(normalizedBrands)].sort()
})

const brandCounts = computed(() => {
  const counts = {}
  allWigs.value.forEach(wig => {
    let brandKey = wig.brand
    if (wig.brand === 'Unknown' || wig.brand.includes('秀琴')) {
      brandKey = '秀琴'
    } else if (wig.brand.startsWith('漫美')) {
      brandKey = '漫美'
    }
    counts[brandKey] = (counts[brandKey] || 0) + 1
  })
  return counts
})

const filteredCards = computed(() => {
  let cards = [...allWigs.value]
  
  // Filter by selected brand
  if (selectedBrand.value !== 'all') {
    if (selectedBrand.value === '秀琴') {
      cards = cards.filter(card => card.brand === 'Unknown' || card.brand.includes('秀琴'))
    } else if (selectedBrand.value === '漫美') {
      cards = cards.filter(card => card.brand.startsWith('漫美'))
    } else {
      cards = cards.filter(card => card.brand === selectedBrand.value)
    }
  }
  
  // Filter by search term
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    cards = cards.filter(card => 
      card.code.toLowerCase().includes(term) || 
      card.brand.toLowerCase().includes(term) ||
      (card.color_name && card.color_name.toLowerCase().includes(term))
    )
  }
  
  // Sort by selected method
  cards.sort((a, b) => {
    switch (sortBy.value) {
      case 'brand_code':
        // Sort by brand first, then by code
        const brandCompare = a.brand.localeCompare(b.brand)
        if (brandCompare !== 0) return brandCompare
        // Try to sort codes numerically if possible
        const aNum = parseFloat(a.code.replace(/[^\d.-]/g, '')) || 0
        const bNum = parseFloat(b.code.replace(/[^\d.-]/g, '')) || 0
        return aNum - bNum
      case 'hue':
        return a.hsl[0] - b.hsl[0]
      case 'brightness':
        return b.hsl[2] - a.hsl[2] // Descending order for brightness
      case 'saturation':
        return b.hsl[1] - a.hsl[1] // Descending order for saturation
      case 'brand':
        return a.brand.localeCompare(b.brand)
      default:
        return 0
    }
  })
  
  return cards
})

const displayedCards = computed(() => {
  return filteredCards.value
})

const hueDistribution = computed(() => {
  // Calculate rough hue distribution
  const hueRanges = {
    red: 0,
    orange: 0,
    yellow: 0,
    green: 0,
    blue: 0,
    purple: 0,
    pink: 0
  }
  
  filteredCards.value.forEach(card => {
    const hue = card.hsl[0]
    if (hue >= 0 && hue < 15) hueRanges.red++
    else if (hue >= 15 && hue < 45) hueRanges.orange++
    else if (hue >= 45 && hue < 75) hueRanges.yellow++
    else if (hue >= 75 && hue < 165) hueRanges.green++
    else if (hue >= 165 && hue < 255) hueRanges.blue++
    else if (hue >= 255 && hue < 300) hueRanges.purple++
    else hueRanges.pink++
  })
  
  return Object.entries(hueRanges)
    .filter(([_, count]) => count > 0)
    .map(([name, count]) => `${name}(${count})`)
    .join(', ')
})

// Methods
function selectCard(card) {
  selectedCard.value = card
}
</script>