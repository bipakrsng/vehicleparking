<template>
  <section class="container my-4">
    <div class="row align-items-center mb-3">
      <div class="col-auto">
        <label for="pincodeInput" class="form-label fw-bold">Search by Pincode:</label>
      </div>
      <div class="col">
        <input
          id="pincodeInput"
          type="text"
          class="form-control"
          v-model="search"
          placeholder="Enter pincode"
        />
      </div>
    </div>

    <div v-if="loading" class="alert alert-info">Loading...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="lots.length" class="table-responsive">
      <table class="table table-bordered table-striped">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Location</th>
            <th>Price</th>
            <th>Address</th>
            <th>City</th>
            <th>State</th>
            <th>Pincode</th>
            <th>Availability</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(lot, i) in lots" :key="lot.id">
            <td>{{ i + 1 }}</td>
            <td>{{ lot.prime_location_name }}</td>
            <td>{{ lot.price }}</td>
            <td>{{ lot.address_line1 }} {{ lot.address_lin2 }}</td>
            <td>{{ lot.city }}</td>
            <td>{{ lot.state }}</td>
            <td>{{ lot.pincode }}</td>
            <td>
              <span v-if="availability[lot.id]">
                {{ availability[lot.id].available }}/{{ availability[lot.id].total }}
              </span>
              <span v-else>Loading...</span>
            </td>
            <td>
                <router-link
                    :to="{ name: 'booking', params: { lotId: lot.id } }"
                    class="btn btn-primary btn-sm"
                >
                    Book
                </router-link>
                </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SearchParkingLots',
  data () {
    return {
      search: '',
      lots: [],
      loading: false,
      error: null,
      availability: {}  // holds lotId -> { available, total }
    }
  },
  watch: {
    search: {
      handler (newValue) {
        this.fetchLots(newValue)
      },
      immediate: true
    }
  },
  methods: {
    async fetchLots (query) {
      if (query === '') {
        this.lots = []
        this.availability = {}
        return
      }

      this.loading = true
      this.error = null

      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`/api/search_parking_lots?q=${encodeURIComponent(query)}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)

        this.lots = await res.json()

        // Fetch availability for each lot
        for (const lot of this.lots) {
          this.getSpotAvailability(lot.id)
        }
      } catch (err) {
        this.error = err.message || 'Failed to load parking lots'
      } finally {
        this.loading = false
      }
    },

    async getSpotAvailability (lotId) {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`/api/lot_availability/${lotId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)

        const data = await res.json()
        this.availability = {...this.availability, [lotId]: data}
      } catch (err) {
        console.error(`Error fetching availability for lot ${lotId}:`, err.message)
         this.availability = {
      ...this.availability,
      [lotId]: { available: 0, total: 0 }
      }
    }
  }
}}
</script>
