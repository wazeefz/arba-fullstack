<template>
  <v-app>
    <v-layout class="rounded rounded-md">
      <!-- App Bar -->
      <v-app-bar title="Arba Travel">
        <!-- Home Button -->
        <v-btn
          v-if="authStore.isLoggedIn"
          variant="text"
          to="/feed"
          class="mr-3"
          >Home</v-btn
        >

        <!-- Login & Logout Buttons -->
        <v-btn
          v-if="!authStore.isLoggedIn"
          variant="outlined"
          to="/login"
          class="mr-3"
          >Login</v-btn
        >
        <v-btn v-if="authStore.isLoggedIn" variant="outlined" @click="logout"
          >Logout</v-btn
        >
      </v-app-bar>

      <!-- Main Content with Slot -->
      <v-main
        class="d-flex align-center justify-center"
        style="min-height: 300px"
      >
        <slot />
      </v-main>
    </v-layout>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore() // Accessing the global auth store
const router = useRouter() // Accessing the Vue Router

// Logout function
const logout = () => {
  authStore.logout() // Update global state to logged out
  router.push('/login') // Redirect to the login page
}
</script>
