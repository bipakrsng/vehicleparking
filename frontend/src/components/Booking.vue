<template>
  <section class="container my-4" v-if="loaded">
    <h3 class="mb-4">Book Parking – Lot #{{ lotId }}</h3>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="success" class="alert alert-success">
      Reservation ID {{ reservation.id }} confirmed!
    </div>

    <form v-if="!success" @submit.prevent="confirmBooking" class="row gy-3">
      <div class="col-md-6">
        <label class="form-label fw-bold">Choose Spot</label>
        <select v-model="selectedSpot" class="form-select" required>
          <option disabled value="">-- select --</option>
          <option v-for="(id,i) in spotIds" :key="id" :value="id">
            Spot {{ i+1 }}
          </option>
        </select>
      </div>
      <div class="col-12">
        <button class="btn btn-primary" :disabled="saving">
          {{ saving ? 'Booking…' : 'Confirm Booking' }}
        </button>
      </div>
    </form>
  </section>

  <div v-else class="container my-4 text-center">
    <div class="spinner-border" role="status"></div>
  </div>
</template>

<script>
export default {
  name: 'Booking',
  props: ['lotId'],
  data () {
    return {
      spotIds: [],
      selectedSpot: '',
      loaded: false,
      saving: false,
      error: null,
      success: null,
      reservation: {}
    }
  },
  mounted () {
    this.fetchAvailableSpots()
  },
  methods: {
    async fetchAvailableSpots () {
      this.error = null
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`/api/lot_available_spots/${this.lotId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        this.spotIds = await res.json()
      } catch (e) {
        this.error = e.message || 'Failed to load spots'
      } finally {
        this.loaded = true
      }
    },

    async confirmBooking () {
      if (!this.selectedSpot) return
      this.saving = true
      this.error = this.success = null
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('/api/reserve', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ parking_spot_id: this.selectedSpot })
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        this.reservation = await res.json()
        this.success = 'Booking successful'
        
        setTimeout(() => {
      this.$router.push('/user-dashboard');
    }, 5000);
      } catch (e) {
        this.error = e.message || 'Booking failed'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
