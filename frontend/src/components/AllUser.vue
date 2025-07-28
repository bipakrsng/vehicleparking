<!-- src/components/UserTable.vue -->
<template>
  <section class="container my-4">
    <h2 class="h4 mb-3">User Management</h2>

    <!-- Loading & error -->
    <div v-if="loading" class="alert alert-info mb-0">Loading users…</div>
    <div v-else-if="error" class="alert alert-danger mb-0">{{ error }}</div>

    <!-- Users table -->
    <div v-else class="table-responsive">
      <table class="table table-striped table-bordered align-middle">
        <thead class="table-light">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Full&nbsp;Name</th>
            <th scope="col">Email</th>
            <th scope="col" class="text-center">Active</th>
            <th scope="col" class="text-center">Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(user, i) in users" :key="user.id">
            <th scope="row">{{ i + 1 }}</th>
            <td>{{ user.first_name }}&nbsp;{{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td class="text-center">
              <span
                class="badge"
                :class="user.active ? 'bg-success' : 'bg-secondary'"
              >
                {{ user.active ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="text-center">
              <button
                @click="toggleActive(user)"
                :disabled="user._updating"
                :class="[
                  'btn btn-sm',
                  user.active ? 'btn-danger' : 'btn-success'
                ]"
              >
                {{ user.active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  name: 'UserTable',

  data () {
    return {
      users: [],
      loading: true,
      error: null
    }
  },

  mounted () {
    this.fetchUsers()
  },

  methods: {
    async fetchUsers () {
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('/api/admin_users', {
          headers: token ? { Authorization: `Bearer ${token}` } : {}
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        this.users = await res.json()
      } catch (err) {
        this.error = err.message || 'Failed to load users'
      } finally {
        this.loading = false
      }
    },

    async toggleActive (user) {
      user._updating = true
      const endpoint = user.active
        ? `/api/users/${user.id}/deactivate`
        : `/api/users/${user.id}/activate`

      try {
        const token = localStorage.getItem('token')
        const res = await fetch(endpoint, {
          method: 'PATCH',
          headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {})
          }
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const updated = await res.json()
        Object.assign(user, updated) // merge server response
      } catch (err) {
        this.error = err.message || `Failed to update ${user.email}`
      } finally {
        user._updating = false
      }
    }
  }
}
</script>

<!-- No scoped styles needed; styling handled by Bootstrap -->
