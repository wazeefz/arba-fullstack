<template>
  <v-card class="mx-auto my-0" max-width="500">
    <v-card-title>
      Comments
      <v-btn
        @click="openAddCommentModal"
        color="primary"
        size="small"
        class="ml-3"
      >
        Add Comment
      </v-btn>
    </v-card-title>

    <v-divider></v-divider>

    <v-card-text v-if="comments.length">
      <v-list>
        <v-list-item v-for="comment in comments" :key="comment.comment_id">
          <v-list-item-title class="font-weight-bold">
            {{ comment.user_email }}
          </v-list-item-title>
          <v-list-item-content>
            {{ comment.text }}
          </v-list-item-content>
          <v-list-item-subtitle class="text-caption mt-1">
            {{ new Date(comment.created_at).toLocaleString() }}
          </v-list-item-subtitle>

          <!-- Only show edit and delete buttons for comment owner -->
          <v-btn
            v-if="isCommentOwner(comment)"
            @click="openEditModal(comment)"
            color="blue"
            size="x-small"
            class="mr-2"
          >
            Edit
          </v-btn>

          <v-btn
            v-if="isCommentOwner(comment)"
            @click="openDeleteModal(comment)"
            color="red"
            size="x-small"
          >
            Delete
          </v-btn>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-card-text v-else>
      <p class="text-center">No comments yet.</p>
    </v-card-text>

    <!-- Add Comment Modal -->
    <AddCommentModal
      v-if="showAddCommentModal"
      :postId="postId"
      @addComment="fetchComments"
      @close="closeAddCommentModal"
    />

    <!-- Edit Comment Modal -->
    <EditCommentModal
      v-if="showEditModal"
      :commentId="editCommentId"
      :postId="postId"
      :currentText="editCommentText"
      @editComment="fetchComments"
      @close="closeEditModal"
    />

    <!-- Delete Comment Modal -->
    <DeleteCommentModal
      v-if="showDeleteModal"
      :commentId="deleteCommentId"
      :postId="postId"
      @deleteComment="fetchComments"
      @close="closeDeleteModal"
    />
  </v-card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import AddCommentModal from '@/components/form/add-comment/index'
import EditCommentModal from '@/components/form/edit-comment/index'
import DeleteCommentModal from '@/components/form/delete-comment/index'

const props = defineProps({
  postId: {
    type: String,
    required: true,
  },
})

const comments = ref([])
const showAddCommentModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editCommentId = ref(null)
const editCommentText = ref('')
const deleteCommentId = ref(null)

// Fetch comments when the component is mounted
const fetchComments = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found, user may not be authenticated')
      return
    }

    const response = await axios.get(
      `http://127.0.0.1:8000/comments?post_id=${props.postId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    comments.value = response.data
  } catch (error) {
    console.error('Error fetching comments:', error)
  }
}

// Check if the current user is the owner of the comment
const isCommentOwner = (comment) => {
  const token = localStorage.getItem('token')
  if (!token) return false
  const userEmail = JSON.parse(atob(token.split('.')[1])).sub
  return userEmail === comment.user_email
}

// Handle Add Comment
const openAddCommentModal = () => {
  showAddCommentModal.value = true
}

const closeAddCommentModal = () => {
  showAddCommentModal.value = false
}

// Handle Edit Comment
const openEditModal = (comment) => {
  editCommentId.value = comment.comment_id
  editCommentText.value = comment.text
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

// Handle Delete Comment
const openDeleteModal = (comment) => {
  deleteCommentId.value = comment.comment_id
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

// Fetch comments on mount
onMounted(() => {
  fetchComments()
})
</script>
