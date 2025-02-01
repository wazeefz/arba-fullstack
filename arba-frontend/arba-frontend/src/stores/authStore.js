// store/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: JSON.parse(localStorage.getItem('isLoggedIn')) || false,
  }),
  actions: {
    login() {
      this.isLoggedIn = true
      localStorage.setItem('isLoggedIn', true)
    },
    logout() {
      this.isLoggedIn = false
      // Remove token from localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('email')
      localStorage.removeItem('name')
      localStorage.removeItem('isLoggedIn')
    },
    checkLoginStatus() {
      // Check localStorage to set the initial state
      const token = localStorage.getItem('token')
      this.isLoggedIn = !!token
    },
  },
})
