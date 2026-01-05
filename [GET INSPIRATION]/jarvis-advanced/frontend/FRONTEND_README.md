# JARVIS Frontend - Modern UI with shadcn/ui

## 🎨 Features

### Design & UX
- ✨ **Modern shadcn/ui Components** - Professional, accessible UI components
- 🎭 **Framer Motion Animations** - Smooth, performant animations
- 🌊 **Matrix Rain Background** - Iconic falling code effect
- 🎨 **Gradient Animations** - Beautiful animated gradients
- 📱 **Fully Responsive** - Works perfectly on all devices
- 🌙 **Dark Theme** - Eye-friendly dark color scheme

### Components
- 🎴 **Card Components** - Elegant, reusable card layouts
- 🔘 **Button Variants** - Multiple styled button options
- 🏷️ **Badge System** - Status indicators and tags
- 📊 **Real-time Status** - Live backend health monitoring
- ⚡ **Interactive Icons** - Lucide React icon library

### Functionality
- 🔄 **Auto Health Check** - Backend status every 15 seconds
- ⏱️ **Uptime Counter** - System runtime tracking
- 🧪 **API Testing** - Built-in API endpoint testing
- 📡 **Latency Display** - Connection speed monitoring
- 🎯 **One-Click Actions** - Quick access to all features

## 🚀 Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality UI components
- **Framer Motion** - Production-ready animations
- **Lucide React** - Beautiful icon library

## 📦 Installation

All dependencies are already installed! Just run:

```bash
cd jarvis-advanced/frontend
npm run dev
```

## 🎯 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## 🌐 Access

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8574
- **API Docs**: http://localhost:8574/docs

## 🎨 Customization

### Colors
Edit `src/styles/globals.css` to customize the color scheme:
- Primary: Cyan (#00ffff)
- Secondary: Green (#00ff00)
- Background: Dark slate

### Components
All UI components are in `src/components/ui/`:
- `button.jsx` - Button component
- `card.jsx` - Card components
- `badge.jsx` - Badge component

### Animations
Framer Motion animations can be customized in `src/App.jsx`:
- Initial states
- Animation durations
- Hover effects
- Transitions

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   │   ├── button.jsx
│   │   │   ├── card.jsx
│   │   │   └── badge.jsx
│   │   └── MatrixRain.jsx # Matrix background effect
│   ├── lib/
│   │   └── utils.js      # Utility functions
│   ├── styles/
│   │   └── globals.css   # Global styles & Tailwind
│   ├── App.jsx           # Main dashboard
│   └── main.jsx          # Entry point
├── index.html
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎭 Features Breakdown

### 1. Matrix Rain Effect
- Custom canvas animation
- Responsive to window resize
- Optimized performance
- Automatic cleanup

### 2. Status Monitoring
- Real-time backend health check
- Latency measurement
- Visual status indicators
- Auto-refresh every 15 seconds

### 3. Interactive Dashboard
- Smooth animations on mount
- Hover effects on cards
- Click actions on all features
- Responsive grid layout

### 4. System Information
- Backend URL display
- Frontend URL display
- Live uptime counter
- Connection latency

## 🔧 Advanced Usage

### Adding New Components

1. Create component in `src/components/ui/`
2. Import in your page/component
3. Use with Tailwind classes

### Custom Animations

```jsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  Your content
</motion.div>
```

### API Integration

The app connects to the backend at `http://localhost:8574`. Update the URL in `src/App.jsx` if needed.

## 🎉 What's New

Compared to the previous version:
- ✅ React-based architecture
- ✅ Professional UI components
- ✅ Smooth animations
- ✅ Better code organization
- ✅ TypeScript-ready
- ✅ Production-ready build
- ✅ Better performance
- ✅ More maintainable code

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Kill process on port 5173
npx kill-port 5173
npm run dev
```

**Build errors?**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📝 License

Part of the JARVIS AI project.
