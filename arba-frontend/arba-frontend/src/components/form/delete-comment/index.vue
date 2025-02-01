<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Are you sure you want to delete this comment?</v-card-title>

      <v-card-actions>
        <v-btn @click="closeModal" color="grey">Cancel</v-btn>
        <v-btn @click="confirmDelete" color="red">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  commentId: {
    type: String,
    required: true,
  },
  postId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['deleteComment', 'close'])

const dialog = ref(false)

// Open modal
const openModal = () => {
  dialog.value = true
}

// Close modal
const closeModal = () => {
  dialog.value = false
  emit('close') // Emit to close modal
}

// Confirm delete comment
const confirmDelete = async () => {
  try {
    const token = localStorage.getItem('token')

    // Send the DELETE request with comment_id in the URL
    await axios.delete(`http://127.0.0.1:8000/comments/${props.commentId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    // Emit event to notify parent to refresh the comments list
    emit('deleteComment')

    closeModal() // Close modal after successful delete
  } catch (error) {
    console.error('Error deleting comment:', error)
  }
}

openModal()
</script>
