<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue', 'colorSelected'])

const fileInput = ref(null)
const canvasRef = ref(null)
const imageSrc = ref(null)

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  const reader = new FileReader()
  reader.onload = (event) => {
    imageSrc.value = event.target.result
    drawImage()
  }
  reader.readAsDataURL(file)
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
    
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
  }
  img.src = imageSrc.value
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
  
  const pixel = ctx.getImageData(safeX, safeY, 1, 1).data
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

// Handle drag for better mobile experience
const handleTouchMove = (e) => {
  e.preventDefault() // prevent scroll
  pickColor(e)
}

const triggerUpload = () => {
  fileInput.value.click()
}

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
      class="w-64 h-64 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 bg-gray-50"
    >
      <span class="text-4xl mb-2">📷</span>
      <span class="text-gray-500">点击上传图片</span>
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
        class="mt-4 text-sm text-blue-600 hover:text-blue-800 underline block mx-auto"
      >
        换一张图
      </button>
    </div>
  </div>
</template>
