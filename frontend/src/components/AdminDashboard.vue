<template>
  <nav-bar></nav-bar>
  <div class="container py-4">
    <h2 class="text-center mb-4">Admin Dashboard - Parking Lots</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div class="row g-3" v-else>
      <div
        v-for="lot in parkingLots"
        :key="lot.id"
        class="col-12 col-sm-6 col-md-4 col-lg-2"
      >
        <div class="card border bg-light h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title text-center">{{ lot.prime_location_name }}</h5>

            <p class="card-text mb-1"><strong>Price:</strong> Rs. {{ lot.price }}</p>
            <p class="card-text mb-1"><strong>Address:</strong> {{ lot.address_line1 }}, {{ lot.address_lin2 }}</p>
            <p class="card-text mb-1">
              <strong>Location:</strong> {{ lot.city }}, {{ lot.state }}, {{ lot.country }} - {{ lot.pincode }}
            </p>

            <p class="card-text mb-1">
              <strong>Occupancy:</strong>
              {{ occupiedCount(lot) }} / {{ lot.spots.length }} (
              {{ occupancyPercentage(lot) }}%)
            </p>

            <!-- Parking Spot Status -->
           
           <div class="d-flex flex-wrap gap-1 mb-3">
  <router-link
    v-for="(spot, index) in lot.spots"
    :key="index"
    :to="{ name: 'spotDetails', params: { id: spot.id } }"
    class="router-link-no-underline"
  >
    <span
      class="spot-rect"
      :class="{
        'available': spot.status === 'available',
        'occupied': spot.status === 'occupied'
      }"
      :title="`Spot ID: ${spot.id}, Status: ${spot.status}`"
    ></span>
  </router-link>
</div>

            <!-- Actions -->
            <div class="mt-auto d-flex justify-content-between">
              <button class="btn btn-sm btn-primary" @click="editLot(lot)">Edit</button>
              <button
                class="btn btn-sm btn-danger"
                @click="deleteLot(lot.id)"
                :disabled="hasOccupiedSpots(lot)"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      parkingLots: [],
      loading: true,
      token: localStorage.getItem('token')
    }
  },
  methods: {
    async fetchLots () {
      this.loading = true
      try {
        const res = await fetch('/api/parking_lots_with_spots', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        if (!res.ok) throw new Error('Failed to fetch parking lots')

        const data = await res.json()
        this.parkingLots = data
      } catch (err) {
        console.error(err)
        alert('Failed to load parking lots')
      } finally {
        this.loading = false
      }
    },
     occupiedCount(lot) {
    return lot.spots.filter(spot => spot.status === 'occupied').length;
  },
  occupancyPercentage(lot) {
    const total = lot.spots.length;
    const occupied = this.occupiedCount(lot);
    return total > 0 ? Math.round((occupied / total) * 100) : 0;
  },
    hasOccupiedSpots (lot) {
      return lot.spots.some(spot => spot.status === 'occupied')
    },
    editLot (lot) {
      // Navigate to edit form with lot ID
      this.$router.push(`/edit_parking_lot/${lot.id}`)
    },
    async deleteLot (id) {
      if (!confirm('Are you sure you want to delete this parking lot?')) return

      try {
        const res = await fetch(`/api/delete_parking_lot/${id}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        if (!res.ok) throw new Error('Delete failed')

        alert('Parking lot deleted')
        this.fetchLots()
      } catch (err) {
        console.error(err)
        alert('Error deleting parking lot')
      }
    }
  },
  mounted () {
    this.fetchLots()
  }
}
</script>

<style scoped>
.spot-circle {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid #ccc;
}
.spot-circle.available {
  background-color: #28a745; /* green */
}
.spot-circle.occupied {
  background-color: #dc3545; /* red */
}
.spot-rect {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  display: inline-block;
  border: 1px solid #999;
}
.available {
  background-color: #4caf50; /* green */
}
.occupied {
  background-color: #f44336; /* red */
}
.card {
  min-height: 360px; /* fixed height */
}
</style>
