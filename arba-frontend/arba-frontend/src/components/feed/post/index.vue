<template>
  <v-card class="mx-auto my-4" max-width="500">
    <v-img :src="getImageSrc(post.image)" height="300" cover></v-img>

    <v-card-text>
      <div class="text-subtitle-1 font-weight-bold">{{ post.user_email }}</div>
      <p class="mt-2">{{ post.caption }}</p>

      <!-- Edit and Delete Buttons only visible if the user is the owner -->
      <v-btn
        size="small"
        v-if="isOwner"
        @click="openEditModal(post)"
        color="primary"
        >Edit</v-btn
      >
      <v-btn
        class="ml-3"
        v-if="isOwner"
        size="small"
        @click="openDeleteModal"
        color="red"
        >Delete</v-btn
      >
    </v-card-text>

    <!-- Comments List Component -->
    <CommentList :postId="post.post_id" />

    <!-- Edit Post Modal -->
    <EditPostModal
      v-if="showEditModal"
      :postId="post.post_id"
      :postData="post"
      @updatePost="updatePost"
      @close="closeEditModal"
    />

    <!-- Delete Post Modal -->
    <DeletePostModal
      :postId="post.post_id"
      :showDeleteModal="showDeleteModal"
      @deletePost="deletePost"
      @close="closeDeleteModal"
    />
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import EditPostModal from '@/components/form/edit-post/index.vue'
import DeletePostModal from '@/components/form/delete-post/index.vue'
import CommentList from '@/components/feed/comment/index.vue'

const emit = defineEmits(['postDeleted'])

// Props for the post data
const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

// For modals
const showEditModal = ref(false)
const showDeleteModal = ref(false)

// Modal handling
const openEditModal = (post) => {
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const openDeleteModal = () => {
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

// Get the token and parse user data
const token = localStorage.getItem('token')
const userEmail = token ? JSON.parse(atob(token.split('.')[1])).sub : null // Decode token to get the user email

// Check if the current user is the owner of the post
const isOwner = computed(() => {
  return userEmail === props.post.user_email
})

// Handling post update
const updatePost = (updatedPost) => {
  // Update the post locally
  props.post.caption = updatedPost.caption
  props.post.image = updatedPost.image
}

// Handling post deletion
const deletePost = (postId) => {
  // Logic to remove the post from the local list
  emit('postDeleted', postId)
  console.log('Post deleted:', postId)
}

// Function to return the correct image source format
const getImageSrc = (image) => {
  // Prepend the base64 data with the correct MIME type for JPEG images
  return `data:image/jpeg;base64,${image}`
}
</script>
