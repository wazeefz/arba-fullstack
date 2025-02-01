<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title>Edit Post</v-card-title>

      <v-card-text>
        <v-text-field v-model="caption" label="Caption" required></v-text-field>

        <!-- Image Upload Input -->
        <v-file-input
          v-model="imageFile"
          label="Upload Image"
          accept="image/*"
          :rules="[
            imageFile && imageFile.size > 0 ? undefined : 'Image is required',
          ]"
          required
        ></v-file-input>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="closeModal" color="grey">Cancel</v-btn>
        <v-btn @click="submitEdit" color="primary">Save Changes</v-btn>
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
  postData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['updatePost', 'close'])

const dialog = ref(false)
const caption = ref('')
const imageFile = ref(null) // To store the uploaded image file

// Open the modal when the component is mounted
watch(
  () => props.postData,
  (newData) => {
    caption.value = newData.caption
    dialog.value = true // This will open the modal
  },
  { immediate: true } // Immediately open the modal when the post data is passed
)

const closeModal = () => {
  dialog.value = false
  emit('close') // Emit event to parent to close the modal
}

const submitEdit = async () => {
  try {
    const token = localStorage.getItem('token')

    // Prepare the form data for the backend
    const formData = new FormData()
    formData.append('caption', caption.value)

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    // Send the form data to the backend
    await axios.put(`http://127.0.0.1:8000/posts/${props.postId}`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })

    // Emit updated post data to parent
    emit('updatePost', { caption: caption.value, image: imageFile.value })
    closeModal()
  } catch (error) {
    console.error('Error editing post:', error)
  }
}
</script>
