<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Add a Comment</v-card-title>

      <v-card-text>
        <v-textarea
          v-model="commentText"
          label="Comment"
          rows="4"
          required
        ></v-textarea>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="closeModal" color="grey">Cancel</v-btn>
        <v-btn @click="submitComment" color="primary">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  postId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['addComment', 'close'])

const dialog = ref(false)
const commentText = ref('')

// Open modal when the component is mounted
const openModal = () => {
  dialog.value = true
}

// Close modal and emit the close event
const closeModal = () => {
  dialog.value = false
  emit('close')
}

// Submit the comment
const submitComment = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `http://127.0.0.1:8000/comments`,
      {
        post_id: props.postId,
        text: commentText.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    // Emit to notify parent to refetch comments
    emit('addComment')
    closeModal()
  } catch (error) {
    console.error('Error adding comment:', error)
  }
}

// Open the modal when the component is mounted
openModal()
</script>
