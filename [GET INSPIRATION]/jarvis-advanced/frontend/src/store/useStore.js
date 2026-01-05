import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAppStore = create(
  persist(
    (set, get) => ({
      // Theme
      theme: 'dark',
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),

      // User
      user: null,
      setUser: (user) => set({ user }),

      // Chat
      messages: [],
      addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
      clearMessages: () => set({ messages: [] }),

      // Settings
      settings: {
        model: 'gpt-4',
        temperature: 0.7,
        maxTokens: 2000,
        streaming: true,
        animations: true,
      },
      updateSettings: (updates) => set((state) => ({
        settings: { ...state.settings, ...updates }
      })),

      // Stats
      stats: {
        totalQueries: 0,
        totalTokens: 0,
        averageResponseTime: 0,
      },
      updateStats: (stats) => set({ stats }),

      // History
      history: [],
      addToHistory: (item) => set((state) => ({
        history: [item, ...state.history].slice(0, 100)
      })),
      clearHistory: () => set({ history: [] }),

      // Loading states
      isLoading: false,
      setLoading: (isLoading) => set({ isLoading }),

      // Sidebar
      sidebarOpen: true,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    {
      name: 'jarvis-storage',
      partialize: (state) => ({
        theme: state.theme,
        settings: state.settings,
        history: state.history,
      }),
    }
  )
)
