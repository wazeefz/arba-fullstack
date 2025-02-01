<template>
  <div>
    <!-- Full-width Upload Button -->
    <v-btn block color="primary" @click="dialog = true">
      <v-icon left>mdi-plus</v-icon>
      New Post
    </v-btn>

    <!-- Upload Post Modal -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>New Post</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="caption"
              label="Caption"
              required
            ></v-text-field>

            <v-file-input
              label="Upload Image"
              accept="image/*"
              @change="handleFileUpload"
              required
            ></v-file-input>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!caption || !image || loading"
            @click="uploadPost"
          >
            Upload
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const dialog = ref(false)
const caption = ref('')
const image = ref(null)
const loading = ref(false)

const emit = defineEmits(['postUploaded'])

const handleFileUpload = (event) => {
  image.value = event.target.files[0]
}

const uploadPost = async () => {
  if (!caption.value || !image.value) return
  loading.value = true

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found')
      return
    }

    const formData = new FormData()
    formData.append('caption', caption.value)
    formData.append('image', image.value)

    await axios.post('http://localhost:8000/posts', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })

    emit('postUploaded')

    // Reset form after upload
    dialog.value = false
    caption.value = ''
    image.value = null
  } catch (error) {
    console.error('Upload failed:', error)
  } finally {
    loading.value = false
  }
}
</script>
