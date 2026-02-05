<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'colorSelected'])

const fileInput = ref(null)
const canvasRef = ref(null)
const imageSrc = ref(null)
const isDragging = ref(false)

// Adjustment parameters
const brightness = ref(100) // 100 = original
const contrast = ref(100) // 100 = original
const saturation = ref(100) // 100 = original
const hue = ref(0) // 0 = original, in degrees

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  processImageFile(file)
}

const processImageFile = (file) => {
  const reader = new FileReader()
  reader.onload = (event) => {
    imageSrc.value = event.target.result
    drawImage()
  }
  reader.readAsDataURL(file)
}

// Drag and drop handlers
const handleDragEnter = (e) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = true
}

const handleDragLeave = (e) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false
}

const handleDragOver = (e) => {
  e.preventDefault()
  e.stopPropagation()
}

const handleDrop = (e) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false
  
  const files = e.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    // Only process image files
    if (file.type.startsWith('image/')) {
      processImageFile(file)
    }
  }
}

const drawImage = () => {
  const img = new Image()
  img.onload = () => {
    const canvas = canvasRef.value
    const ctx = canvas.getContext('2d')
    
    // Resize logic for mobile
    const maxWidth = window.innerWidth - 40 // Padding
    const scale = Math.min(1, maxWidth / img.width)
    
    canvas.width = img.width * scale
    canvas.height = img.height * scale
    
    // Apply adjustments
    applyAdjustments(ctx, img, canvas.width, canvas.height)
  }
  img.src = imageSrc.value
}

const applyAdjustments = (ctx, img, width, height) => {
  // First, draw the original image
  ctx.clearRect(0, 0, width, height)
  ctx.drawImage(img, 0, 0, width, height)
  
  // Get image data to apply adjustments
  const imageData = ctx.getImageData(0, 0, width, height)
  const data = imageData.data
  
  // Apply adjustments to each pixel
  for (let i = 0; i < data.length; i += 4) {
    let r = data[i]
    let g = data[i + 1]
    let b = data[i + 2]
    
    // Apply brightness adjustment
    if (brightness.value !== 100) {
      r = r * (brightness.value / 100)
      g = g * (brightness.value / 100)
      b = b * (brightness.value / 100)
    }
    
    // Apply contrast adjustment
    if (contrast.value !== 100) {
      const factor = (259 * (contrast.value + 255)) / (255 * (259 - contrast.value))
      r = factor * (r - 128) + 128
      g = factor * (g - 128) + 128
      b = factor * (b - 128) + 128
    }
    
    // Apply saturation adjustment
    if (saturation.value !== 100) {
      // Convert to grayscale
      const gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
      const satFactor = saturation.value / 100
      
      r = gray + satFactor * (r - gray)
      g = gray + satFactor * (g - gray)
      b = gray + satFactor * (b - gray)
    }
    
    // Apply hue adjustment (simplified version)
    if (hue.value !== 0) {
      // Convert RGB to HSL
      const hsl = rgbToHsl(r, g, b)
      // Adjust hue
      hsl[0] = (hsl[0] + hue.value) % 360
      if (hsl[0] < 0) hsl[0] += 360
      
      // Convert back to RGB
      const newRgb = hslToRgb(hsl[0], hsl[1], hsl[2])
      r = newRgb[0]
      g = newRgb[1]
      b = newRgb[2]
    }
    
    // Clamp values to valid range
    data[i] = Math.min(255, Math.max(0, r))
    data[i + 1] = Math.min(255, Math.max(0, g))
    data[i + 2] = Math.min(255, Math.max(0, b))
  }
  
  // Put the adjusted image data back
  ctx.putImageData(imageData, 0, 0)
}

// RGB to HSL conversion
function rgbToHsl(r, g, b) {
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

// HSL to RGB conversion
function hslToRgb(h, s, l) {
  h /= 360;
  s /= 100;
  l /= 100;

  let r, g, b;

  if (s === 0) {
    r = g = b = l; // achromatic
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }

  return [
    Math.round(r * 255),
    Math.round(g * 255),
    Math.round(b * 255)
  ];
}

const magnifier = ref({
  show: false,
  x: 0,
  y: 0,
  color: [0,0,0]
})
const magnifierCanvas = ref(null)

const drawMagnifier = (x, y) => {
  const canvas = canvasRef.value
  const magCtx = magnifierCanvas.value.getContext('2d')
  const zoom = 4 // 放大倍数
  const size = 100 // 放大镜大小 (px)
  const radius = size / 2
  
  // Clear
  magCtx.clearRect(0, 0, size, size)
  
  // Draw zoomed image
  // source x, y, w, h -> dest x, y, w, h
  // We want to capture a (size/zoom) area around (x,y)
  const srcW = size / zoom
  const srcH = size / zoom
  const srcX = Math.max(0, x - srcW/2)
  const srcY = Math.max(0, y - srcH/2)
  
  // Fill background white first (transparent pngs)
  magCtx.fillStyle = 'white'
  magCtx.fillRect(0, 0, size, size)

  magCtx.drawImage(
    canvas,
    srcX, srcY, srcW, srcH,
    0, 0, size, size
  )
  
  // Draw crosshair
  magCtx.strokeStyle = 'rgba(255, 255, 255, 0.8)'
  magCtx.lineWidth = 2
  magCtx.beginPath()
  magCtx.moveTo(radius - 10, radius)
  magCtx.lineTo(radius + 10, radius)
  magCtx.moveTo(radius, radius - 10)
  magCtx.lineTo(radius, radius + 10)
  magCtx.stroke()
  
  magCtx.strokeStyle = 'rgba(0, 0, 0, 0.5)'
  magCtx.lineWidth = 1
  magCtx.beginPath()
  magCtx.moveTo(radius - 10, radius)
  magCtx.lineTo(radius + 10, radius)
  magCtx.moveTo(radius, radius - 10)
  magCtx.lineTo(radius, radius + 10)
  magCtx.stroke()
}

const pickColor = (event) => {
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  const rect = canvas.getBoundingClientRect()
  
  // Handle both mouse and touch events
  let clientX, clientY
  if (event.touches && event.touches.length > 0) {
    clientX = event.touches[0].clientX
    clientY = event.touches[0].clientY
  } else {
    clientX = event.clientX
    clientY = event.clientY
  }

  const x = (clientX - rect.left) * (canvas.width / rect.width)
  const y = (clientY - rect.top) * (canvas.height / rect.height)
  
  // Clamp coordinates
  const safeX = Math.min(Math.max(0, x), canvas.width - 1)
  const safeY = Math.min(Math.max(0, y), canvas.height - 1)
  
  // Get the adjusted pixel data (apply adjustments to the original image first)
  const img = new Image()
  img.src = imageSrc.value
  img.onload = () => {
    // Create a temporary canvas to get the original pixel
    const tempCanvas = document.createElement('canvas')
    const tempCtx = tempCanvas.getContext('2d')
    tempCanvas.width = canvas.width
    tempCanvas.height = canvas.height
    
    // Apply the same adjustments to the temporary canvas
    applyAdjustments(tempCtx, img, tempCanvas.width, tempCanvas.height)
    
    // Get the pixel color after adjustments
    const pixel = tempCtx.getImageData(safeX, safeY, 1, 1).data
    const rgb = [pixel[0], pixel[1], pixel[2]]
    
    // Update Magnifier
    magnifier.value = {
      show: true,
      x: (clientX - rect.left), // UI position (relative to canvas container)
      y: (clientY - rect.top),
      color: rgb
    }
    
    // Wait for next tick to draw on magnifier canvas
    setTimeout(() => drawMagnifier(safeX, safeY), 0)

    emit('colorSelected', rgb)
  }
}

// Handle drag for better mobile experience
const handleTouchMove = (e) => {
  e.preventDefault() // prevent scroll
  pickColor(e)
}

const triggerUpload = () => {
  fileInput.value.click()
}

// Watch for adjustment changes and redraw image
watch([brightness, contrast, saturation, hue], () => {
  if (imageSrc.value) {
    drawImage()
  }
})
</script>

<template>
  <div class="flex flex-col items-center gap-4">
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden" 
      accept="image/*"
      @change="onFileChange"
    />
    
    <div 
      v-if="!imageSrc"
      @click="triggerUpload"
      @dragenter="handleDragEnter"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      class="w-64 h-64 border-2 border-dashed rounded-lg flex flex-col items-center justify-center cursor-pointer bg-gray-50"
      :class="{
        'border-blue-500 bg-blue-50': isDragging,
        'border-gray-300 hover:border-[#df6f92]': !isDragging
      }"
    >
      <span class="text-4xl mb-2">📷</span>
      <span class="text-gray-500 text-center">
        <span v-if="!isDragging">点击上传图片</span>
        <span v-else class="text-[#df6f92]">释放以上传</span>
      </span>
      <p class="text-xs text-gray-400 mt-1">或拖拽图片至此</p>
    </div>

    <div v-else class="relative touch-none select-none">
      <canvas 
        ref="canvasRef"
        @click="pickColor"
        @touchstart="pickColor"
        @touchmove="handleTouchMove"
        class="border border-gray-200 rounded shadow-sm cursor-crosshair max-w-full"
      ></canvas>
      
      <!-- Magnifier -->
      <div 
        v-if="magnifier.show"
        class="absolute pointer-events-none transform -translate-x-1/2 -translate-y-1/2 z-10 flex flex-col items-center gap-1"
        :style="{ 
          left: `${magnifier.x}px`, 
          top: `${magnifier.y - 80}px` 
        }"
      >
        <div class="relative rounded-full border-4 border-white shadow-xl overflow-hidden bg-white w-[100px] h-[100px]">
          <canvas 
            ref="magnifierCanvas" 
            width="100" 
            height="100"
            class="w-full h-full"
          ></canvas>
          <!-- Ring overlay color -->
          <div 
            class="absolute inset-0 border-[6px] rounded-full pointer-events-none"
            :style="{ borderColor: `rgb(${magnifier.color.join(',')})` }"
          ></div>
        </div>
      </div>

      <button 
        @click="triggerUpload"
        class="mt-4 text-sm block mx-auto"
        :style="{color: '#df6f92'}"
      >
        换一张图
      </button>
    </div>

    <!-- Adjustment Controls -->
    <div v-if="imageSrc" class="w-full max-w-md bg-white p-4 rounded-lg shadow-sm">
      <h3 class="font-medium text-gray-700 mb-3">图片调整</h3>
      <div class="space-y-4">
        <!-- Brightness -->
        <div>
          <label class="block text-sm text-gray-600 mb-1">亮度: {{ brightness }}%</label>
          <input 
            v-model.number="brightness"
            type="range" 
            min="0" 
            max="200" 
            step="1"
            class="w-full"
          />
        </div>
        
        <!-- Contrast -->
        <div>
          <label class="block text-sm text-gray-600 mb-1">对比度: {{ contrast }}%</label>
          <input 
            v-model.number="contrast"
            type="range" 
            min="0" 
            max="200" 
            step="1"
            class="w-full"
          />
        </div>
        
        <!-- Saturation -->
        <div>
          <label class="block text-sm text-gray-600 mb-1">饱和度: {{ saturation }}%</label>
          <input 
            v-model.number="saturation"
            type="range" 
            min="0" 
            max="200" 
            step="1"
            class="w-full"
          />
        </div>
        
        <!-- Hue -->
        <div>
          <label class="block text-sm text-gray-600 mb-1">色相: {{ hue }}°</label>
          <input 
            v-model.number="hue"
            type="range" 
            min="-180" 
            max="180" 
            step="1"
            class="w-full"
          />
        </div>
      </div>
      
      <!-- Reset button -->
      <button 
        @click="[brightness, contrast, saturation, hue] = [100, 100, 100, 0]"
        class="mt-3 text-sm hover:underline"
        :style="{color: '#df6f92'}"
      >
        重置调整
      </button>
    </div>
  </div>
</template>