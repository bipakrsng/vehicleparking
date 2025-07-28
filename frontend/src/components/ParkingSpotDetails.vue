<template>
    <nav-bar></nav-bar>
  <div class="container mt-4">
    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else>
      <div class="card p-4 shadow-sm">
        <h4 class="text-primary">Parking Spot Details</h4>
        <p><strong>Spot ID:</strong> {{ parkingSpot.id }}</p>
        <p><strong>Status:</strong> 
          <span :class="{
            'text-success': parkingSpot.status === 'available',
            'text-danger': parkingSpot.status === 'occupied'
          }">{{ parkingSpot.status }}</span>
        </p>

        <!-- View Booking Details button -->
        <button 
          v-if="parkingSpot.status === 'occupied'" 
          class="btn btn-info btn-sm me-2"
          @click="showBooking = !showBooking"
        >
          {{ showBooking ? 'Hide' : 'View' }} Booking Details
        </button>

        <!-- Delete Button -->
        <button 
          class="btn btn-danger btn-sm"
          :disabled="parkingSpot.status === 'occupied'"
          @click="deleteSpot"
        >
          Delete Spot
        </button>
         <button class="btn btn-sm btn-secondary" @click="closeDetails">Close</button>
      </div>

      <!-- Booking Details Section -->
      <div v-if="showBooking" class="card mt-4 p-3">
        <h5>Booking Info</h5>
        <p><strong>Booking ID:</strong> {{ booking.id }}</p>
        <p><strong>User ID:</strong> {{ booking.user_id }}</p>
        <p><strong>Parking Time:</strong> {{ booking.parking_time }}</p>
        <p><strong>Leaving Time:</strong> {{ booking.leaving_timestamp || 'Still Parked' }}</p>
        <p><strong>Cost:</strong> ₹{{ booking.cost }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['id'],
  data() {
    return {
      parkingSpot: {},
      booking: {},
      showBooking: false,
      loading: true,
      error: null
    };
  },
  mounted() {
    this.getParkingSpot();
  },
  methods: {
    async getParkingSpot() {
      try {
        const res = await fetch(`/api/parking_spot_details/${this.id}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
          },
        });
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.message || 'Failed to fetch spot');
        }
        const data = await res.json();
        this.parkingSpot = data.parkingDetails;
        this.booking = data.booking;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async deleteSpot() {
      try {
        const res = await fetch(`/api/delete_spot/${this.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
          },
        });
        if (!res.ok) {
          throw new Error('Failed to delete spot');
        }
        alert('Spot deleted successfully');
        this.$router.push('/admin-dashboard'); // Or wherever you want to redirect
      } catch (err) {
        alert(err.message);
      }
    },
    closeDetails(){
        this.$router.push('/admin-dashboard'); // Redirect to admin dashboard
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>
