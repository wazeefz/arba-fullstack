<template>
  <v-container>
    <v-card class="mx-auto pa-4" max-width="400">
      <v-card-title class="text-h5 text-center">Login</v-card-title>

      <v-card-text>
        <v-form @submit.prevent="submitLogin">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            variant="outlined"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            variant="outlined"
            required
          ></v-text-field>

          <v-btn
            :loading="loading"
            type="submit"
            color="primary"
            block
            class="mt-3"
          >
            Login
          </v-btn>

          <!-- Error message below the login button -->
          <div v-if="errorMessage" class="mt-3 text-center text-red">
            {{ errorMessage }}
          </div>
        </v-form>

        <!-- Sign-up Link -->
        <div class="text-center mt-4">
          <span>Don't have an account?</span>
          <v-btn variant="text" color="primary" @click="goToSignUp">
            Sign Up
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore' // Import auth store

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)
const router = useRouter()
const authStore = useAuthStore() // Access the auth store

const submitLogin = async () => {
  loading.value = true // Set loading to true
  try {
    const response = await axios.post('http://localhost:8000/users/login', {
      email: email.value,
      password: password.value,
    })

    // If login is successful, save the token and handle the response
    const { token, name, email: userEmail } = response.data

    // Store the token and other data in localStorage or state
    localStorage.setItem('token', token)
    localStorage.setItem('name', name)
    localStorage.setItem('email', userEmail)
    localStorage.setItem('isLoggedIn', true)

    // Call the login method from the store to update global state
    authStore.login()

    // Redirect user after login
    router.push('/feed')
  } catch (error) {
    if (error.response) {
      // If the server responded with an error, set the error message
      const serverErrorMessage = error.response.data.detail || 'Login failed'
      errorMessage.value = serverErrorMessage
    } else {
      // Error making the request (network issues)
      console.error('Error:', error.message)
      errorMessage.value = 'An error occurred while trying to login.'
    }
  } finally {
    loading.value = false // Set loading to false after the request completes
  }
}

const goToSignUp = () => {
  router.push('/signup') // Navigate to the signup page
}
</script>
