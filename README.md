# 🎨 Wig Color Matcher (假发色卡匹配助手)

A mobile-friendly web tool for Kigurumi mask makers and cosplayers to find the matching wig color from reference images.

## ✨ Features

- **Upload & Pick**: Upload any anime character image and pick a color point.
- **Magnifier**: Precision color picking with a 4x zoom magnifier (mobile optimized).
- **Smart Matching**: Uses CIELAB color space + Delta E algorithm for perceptual color matching.
- **Database**: Includes 600+ wig color cards (Manqi/Seven/etc.) from `anime-chara-tool`.
- **PWA Ready**: Works great on mobile browsers.

## 🛠️ Tech Stack

- **Vue 3** + **Vite**
- **Tailwind CSS**
- **Canvas API** (for image processing)

## 🚀 Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## 🔗 Links

- **Live Demo**: [ruruka.toyama.moe/wig](https://ruruka.toyama.moe/wig/)
- **MEIS 莓萌**: [kigis.me](https://kigis.me)

## 📄 License

MIT
