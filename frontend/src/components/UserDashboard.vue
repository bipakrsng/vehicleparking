<template>
  <nav-bar></nav-bar>
  <div class="container mt-4">
    <div class="text-center my-4">
  <h2 class="fw-bold text-primary">User Dashboard</h2>
</div>


    <search-lots-user></search-lots-user>

    <!-- Section 1: Current Booking -->
    <div class="card mt-4">
      <div class="card-header bg-primary text-white">
        Current Booking
      </div>
      <div class="card-body">
        <div v-if="currentBooking">
          <table class="table table-bordered">
            <thead>
              <tr >
                <th>Lot</th>
                <th>Spot ID</th>
                <th>Parking Time</th>
                
                <th>Cost @ {{ cost_per_hour }} hour</th>
                <th>Duration</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in currentBooking" :key="item.id">
                <td>{{ item.lot_name }}</td>
                <td>{{ item.spot_id }}</td>
                <td>{{ item.parking_time }}</td>
                
                <td>{{ item.cost }}</td>
                <td>{{ item.duration }}</td>
                <td>
                  <button class="btn btn-danger btn-sm" @click="releaseSpot(item.id)">
                    Release
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-muted">
          No current booking found.
        </div>
      </div>
    </div>

    <!-- Section 2: Booking History -->
    <div class="card mt-5">
      <div class="card-header bg-secondary text-white">
        Booking History
      </div>
      <div class="card-body">
        <div v-if="bookingHistory.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Lot</th>
                <th>Parking Time</th>
                <th>Leaving Time</th>
                <th>Cost</th>
                <th>Duration</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in bookingHistory" :key="item.id">
                <td>{{ item.lot_name }}</td>
                <td>{{ item.parking_time }}</td>
                <td>{{ item.leaving_time }}</td>
                <td>{{ item.cost }}</td>
                <td>{{ item.duration }}</td>
                
                <td>
                  <button  class="btn btn-warning btn-sm">
                    Parked Out
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-muted">
          No history available.
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import SearchLotsUser from './SearchLotsUser.vue';
export default {
  name: 'UserDashboard',
  components: {
    SearchLotsUser
  },
  data() {

    return {
      currentBooking: [],
      bookingHistory: [],
      cost_per_hour:'',
    };
  },
  mounted() {
    this.fetchBookings();
  },
  methods: {
    async fetchBookings() {
      try {
        const res = await fetch('/api/user/bookings', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
          },
        });
        const data = await res.json();
        this.currentBooking = data.current;
        this.bookingHistory = data.history;
        this.cost_per_hour = data.cost_per_hour;
      } catch (err) {
        console.error('Failed to fetch bookings:', err);
      }
    },
    async releaseSpot(reservationId) {

      const confirmRelease = window.confirm("Are you sure you want to release this spot?");
  if (!confirmRelease) return;
      try {
        const res = await fetch(`/api/release/${reservationId}`, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
          },
        });
        if (res.ok) {
          
          this.fetchBookings(); // Refresh both sections
        }
      } catch (err) {
        console.error('Error releasing spot:', err);
      }
    },
    
  },
};
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>
