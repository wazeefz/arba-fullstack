<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Are you sure you want to delete this post?</v-card-title>

      <v-card-actions>
        <v-btn @click="closeModal" color="grey">Cancel</v-btn>
        <v-btn @click="confirmDelete" color="red">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  postId: {
    type: String,
    required: true,
  },
  showDeleteModal: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['deletePost', 'close'])

const dialog = ref(false)

// Sync parent modal visibility with dialog
watch(
  () => props.showDeleteModal,
  (newVal) => {
    dialog.value = newVal
  },
  { immediate: true } // This ensures the modal visibility is set when the component is mounted
)

const closeModal = () => {
  dialog.value = false
  emit('close') // Emit to parent to close modal
}

const confirmDelete = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://127.0.0.1:8000/posts/${props.postId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    // Emit to delete the post in the parent
    emit('deletePost', props.postId)
    closeModal()
  } catch (error) {
    console.error('Error deleting post:', error)
  }
}
</script>
