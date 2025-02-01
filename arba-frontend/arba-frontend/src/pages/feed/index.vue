<route>
    {
        meta: {
            requiresAuth: true,
        }
    }
</route>

<template>
  <v-container>
    <!-- Show Loading Spinner if data is being fetched -->
    <v-row v-if="loading" justify="center">
      <v-col cols="auto">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <!-- Only show the posts list and other components once loading is complete -->
    <v-row v-else class="d-flex flex-column">
      <!-- New Post Component -->
      <NewPost @postUploaded="fetchPosts" />

      <!-- Posts List -->
      <v-row v-for="post in posts" :key="post.post_id">
        <v-col cols="12">
          <PostCard :post="post" @postDeleted="fetchPosts" />
        </v-col>
      </v-row>
    </v-row>
  </v-container>
</template>

<script setup>
import PostCard from '@/components/feed/post/index.vue'
import NewPost from '@/components/form/new-post/index.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const loading = ref(true) // Set loading to true initially

// Fetch posts when the component is mounted
const fetchPosts = async () => {
  try {
    // Get the token from localStorage
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found, user may not be authenticated')
      return
    }

    const response = await axios.get('http://127.0.0.1:8000/posts', {
      headers: {
        Authorization: `Bearer ${token}`, // Attach the bearer token
      },
    })

    // Set the posts data
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    loading.value = false // Set loading to false after fetching
  }
}

// Call fetchPosts when the component is mounted
onMounted(() => {
  fetchPosts()
})
</script>
