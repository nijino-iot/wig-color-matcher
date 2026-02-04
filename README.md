# 🎨 假发色彩匹配助手 (Wig Color Matcher)

专为 Kigurumi 面具制作师和 Cosplayer 设计的移动端网页工具。上传图片即可快速寻找最接近的假发色号。

## ✨ 功能特点

- **📸 传图取色**: 上传任意二次元角色图片，点击即可取色。
- **🔍 精准放大镜**: 提供 4 倍放大的取色放大镜，专为移动端触屏优化，手指不遮挡。
- **🧠 智能匹配**: 采用 **CIELAB 色彩空间 + Delta E 算法**，比普通 RGB 对比更符合人眼视觉感知。
- **📚 色卡数据库**: 内置 **600+** 张假发色卡数据（涵盖曼柒、千型、漫供、秀琴、漫美等主流品牌）。
- **📱 PWA 体验**: 完美支持手机浏览器，随时随地使用。

## 🛠️ 技术栈

- **Vue 3** + **Vite**
- **Tailwind CSS**
- **Canvas API** (图像处理)

## 🚀 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 🔗 相关链接

- **在线使用**: [wig.meis.moe](https://wig.meis.moe)
- **MEIS 莓萌**: [kigis.me](https://kigis.me)

## 📄 开源协议

MIT License
