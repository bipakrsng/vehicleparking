<!-- src/components/EditProfile.vue -->

<template>
    <nav-bar></nav-bar>
  <section class="container my-5" v-if="loaded">
    <h2 class="h4 mb-4">Edit Profile</h2>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="success" class="alert alert-success">{{ success }}</div>

    <form @submit.prevent="saveChanges" class="row g-3">
      <!-- First / Last name -->
      <div class="col-md-6">
        <label class="form-label">First name</label>
        <input class="form-control" v-model="form.first_name" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Last name</label>
        <input class="form-control" v-model="form.last_name" />
      </div>

      <!-- Email (readonly) -->
      <div class="col-md-6">
        <label class="form-label">Email</label>
        <input class="form-control" :value="form.email" readonly />
      </div>
      <div class="col-md-6">
        <label class="form-label">Username</label>
        <input class="form-control" :value="form.username" readonly />
      </div>

      <!-- Phone -->
      <div class="col-md-6">
        <label class="form-label">Phone</label>
        <input class="form-control" v-model="form.phone_number" />
      </div>

      <!-- Address -->
      <div class="col-12">
        <label class="form-label">Address Line 1</label>
        <input class="form-control" v-model="form.address_line1" />
      </div>
      <div class="col-12">
        <label class="form-label">Address Line 2</label>
        <input class="form-control" v-model="form.address_line2" />
      </div>
      <div class="col-md-4">
        <label class="form-label">City</label>
        <input class="form-control" v-model="form.city" />
      </div>
      <div class="col-md-4">
        <label class="form-label">State</label>
        <input class="form-control" v-model="form.state" />
      </div>
      <div class="col-md-4">
        <label class="form-label">Country</label>
        <input class="form-control" v-model="form.country" />
      </div>
      <div class="col-md-4">
        <label class="form-label">Pincode</label>
        <input class="form-control" v-model="form.pincode" />
      </div>

      <!-- Gender / DOB -->
      <div class="col-md-4">
        <label class="form-label">Gender</label>
        <select class="form-select" v-model="form.gender">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>
      <div class="col-md-4">
        <label class="form-label">Date of birth</label>
        <input type="date" class="form-control" v-model="form.date_of_birth" />
      </div>

      <!-- New password -->
      <div class="col-md-6">
        <label class="form-label">New Password (leave blank to keep)</label>
        <input type="password" class="form-control" v-model="form.new_password" />
      </div>

      <!-- Admin‑only: Active flag -->
      <div v-if="isAdminOrHigher" class="col-md-4">
        <label class="form-label">Active</label>
        <select class="form-select" v-model="form.active">
          <option :value="true">Yes</option>
          <option :value="false">No</option>
        </select>
      </div>

      <!-- Super‑admin‑only: Role selector -->
      <div v-if="isSuperAdmin" class="col-md-4">
        <label class="form-label">Role</label>
        <select class="form-select" v-model="form.role">
          <option>user</option>
          <option>admin</option>
          <option>super_admin</option>
        </select>
      </div>

      <div class="col-12">
        <button class="btn btn-primary" type="submit" :disabled="saving">
          {{ saving ? 'Saving…' : 'Save Changes' }}
        </button>
      </div>
    </form>
  </section>

  <div v-else class="container my-5 text-center">
    <div class="spinner-border" role="status" />
  </div>
</template>

<script>
import { decodeToken } from '@/utils/auth';
import { useUserStore } from '@/store/userStore';

export default {
  name: 'EditProfile',

  data () {
    return {
      form: {
        id: null,
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        address_line1: '',
        address_line2: '',
        city: '',
        state: '',
        country: '',
        pincode: '',
        gender: '',
        date_of_birth: '',
        active: true,
        role: 'user',
        new_password: ''
      },
      loaded: false,
      saving: false,
      error: null,
      success: null,
      userRole: null,
      userId: null
    }
  },

  computed: {
    isAdminOrHigher () {
      return this.userRole === 'admin' || this.userRole === 'super_admin'
    },
    isSuperAdmin () {
      return this.userRole === 'super_admin'
    }
  },

  mounted () {
    this.initAuth()
    this.fetchProfile()
  },

  methods: {
    // --------------------------
    initAuth () {
      // Prefer Pinia if you have it
      const auth = useUserStore()
      if (auth.token) {
        this.userRole = auth.role
        this.userId = auth.user_id
      } else {
        const payload = decodeToken()
        this.userRole = payload?.role || null
        this.userId = payload?.user_id || null
      }
    },

    // --------------------------
    async fetchProfile () {
      this.error = null
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`/api/edit_users/${this.userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        Object.assign(this.form, data)   // prefill
      } catch (e) {
        this.error = e.message || 'Failed to load profile'
      } finally {
        this.loaded = true
      }
    },

    // --------------------------
    async saveChanges () {
      this.saving = true
      this.error = this.success = null
      try {
        const token = localStorage.getItem('token')

        // Build payload: send only fields user is allowed to change
        const payload = { }

        // Common editable fields
        const common = ['first_name','last_name','phone_number','address_line1',
                        'address_line2','city','state','country','pincode',
                        'gender','date_of_birth']
        common.forEach(f => payload[f] = this.form[f])

        // New password if provided
        if (this.form.new_password) payload.new_password = this.form.new_password

        // Admin can toggle active
        if (this.isAdminOrHigher) payload.active = this.form.active

        // Super admin can change role (but NOT if editing self)
        if (this.isSuperAdmin && this.userId !== this.form.id) {
          payload.role = this.form.role
        }

        const res = await fetch(`/api/edit_users/${this.form.id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const updated = await res.json()
        Object.assign(this.form, updated)
        this.success = 'Profile updated successfully'
      } catch (e) {
        this.error = e.message || 'Failed to save changes'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>