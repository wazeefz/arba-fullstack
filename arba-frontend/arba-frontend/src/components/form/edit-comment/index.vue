<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Edit Comment</v-card-title>

      <v-card-text>
        <v-textarea
          v-model="updatedText"
          label="Edit your comment"
          rows="4"
          required
        ></v-textarea>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="closeModal" color="grey">Cancel</v-btn>
        <v-btn @click="submitEdit" color="primary">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
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
  currentText: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['editComment', 'close'])

const dialog = ref(false)
const updatedText = ref(props.currentText)

// Open modal
const openModal = () => {
  dialog.value = true
}

// Close modal
const closeModal = () => {
  dialog.value = false
  emit('close')
}

// Submit the updated comment
const submitEdit = async () => {
  try {
    const token = localStorage.getItem('token')

    // Send the updated comment as part of the payload
    await axios.put(
      'http://127.0.0.1:8000/comments',
      {
        comment_id: props.commentId,
        post_id: props.postId,
        text: updatedText.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    emit('editComment') // Notify parent to refresh comments
    closeModal()
  } catch (error) {
    console.error('Error editing comment:', error)
  }
}

// Watch for changes to updated text to keep the modal open
watch(
  () => props.currentText,
  (newText) => {
    updatedText.value = newText
  }
)

openModal()
</script>
