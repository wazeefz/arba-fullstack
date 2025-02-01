<template>
  <v-container>
    <v-card class="mx-auto pa-4" max-width="400">
      <v-card-title class="text-h5 text-center">Sign Up</v-card-title>

      <v-card-text>
        <v-form @submit.prevent="submitSignUp">
          <v-text-field
            v-model="name"
            label="Full Name"
            type="text"
            variant="outlined"
            required
          ></v-text-field>

          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            variant="outlined"
            required
          ></v-text-field>

          <v-text-field
            v-model="password"
            :type="passwordVisible ? 'text' : 'password'"
            label="Password"
            variant="outlined"
            required
            append-icon="mdi-eye"
            @click:append="togglePasswordVisibility"
          ></v-text-field>

          <v-btn
            :loading="loading"
            type="submit"
            color="primary"
            block
            class="mt-3"
            :disabled="isSubmitDisabled"
          >
            Sign Up
          </v-btn>

          <!-- Error message if there is any -->
          <div v-if="errorMessage" class="mt-3 text-center text-red">
            {{ errorMessage }}
          </div>
        </v-form>

        <!-- Login Link -->
        <div class="text-center mt-4">
          <span>Already have an account?</span>
          <v-btn variant="text" color="primary" @click="goToLogin">Login</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const name = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const passwordVisible = ref(false)
const router = useRouter()

// Computed property to check if the signup button should be enabled
const isSubmitDisabled = computed(() => {
  return !(name.value && email.value && password.value) // Enable button only if all fields are filled
})

// Toggle password visibility
const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value
}

const submitSignUp = async () => {
  try {
    loading.value = true
    const response = await axios.post('http://localhost:8000/users/signup', {
      name: name.value,
      email: email.value,
      password: password.value,
    })

    // If signup is successful, redirect to the login page
    const { message } = response.data
    console.log(message)

    // Redirect user to login page after successful signup
    router.push('/login')
  } catch (error) {
    loading.value = false
    if (error.response) {
      // If the backend returns an error (e.g., user already exists)
      errorMessage.value = error.response.data.detail || 'Sign up failed'
      console.error('Error:', errorMessage.value)
    } else {
      // Handle other errors (e.g., network issues)
      errorMessage.value = 'An error occurred while trying to sign up.'
      console.error('Error:', error.message)
    }
  }
}

const goToLogin = () => {
  router.push('/login') // Navigate to the login page
}
</script>
