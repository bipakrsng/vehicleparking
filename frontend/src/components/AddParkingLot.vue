<template>
  <div class="container mt-5">
    <h2 class="mb-4">Create Parking Lot</h2>

    <!-- Success / Error banners -->
    <div v-if="success" class="alert alert-success">{{ success }}</div>
    <div v-if="error"   class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="submitForm">
      <!-- Prime Location & Price -->
      <div class="mb-3">
        <label class="form-label">Prime Location Name</label>
        <input type="text" class="form-control" v-model="parkingLot.prime_location_name" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Price</label>
        <input type="number" step="0.01" class="form-control" v-model="parkingLot.price" required />
      </div>

      <!-- Address Lines -->
      <div class="mb-3">
        <label class="form-label">Address Line 1</label>
        <input type="text" class="form-control" v-model="parkingLot.address_line1" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Address Line 2</label>
        <input type="text" class="form-control" v-model="parkingLot.address_lin2" />
      </div>

      <!-- Country ▸ State ▸ City -->
      <div class="row">
        <!-- Country -->
        <div class="col-md-4 mb-3">
          <label class="form-label">Country</label>
          <select v-model="selectedCountry" class="form-select">
            <option disabled value="">Choose Country</option>
            <option v-for="c in countries" :key="c.id" :value="c.iso2">
              {{ c.name }}
            </option>
          </select>
        </div>
        <!-- State -->
        <div class="col-md-4 mb-3">
          <label class="form-label">State</label>
          <select v-model="selectedState" class="form-select" :disabled="!states.length">
            <option disabled value="">Choose State</option>
            <option v-for="s in states" :key="s.id" :value="s.state_code">
              {{ s.name }}
            </option>
          </select>
        </div>
        <!-- City -->
        <div class="col-md-4 mb-3">
          <label class="form-label">City</label>
          <select v-model="parkingLot.city" class="form-select" :disabled="!cities.length">
            <option disabled value="">Choose City</option>
            <option v-for="ct in cities" :key="ct.id" :value="ct.name">
              {{ ct.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Pincode & Spots -->
      <div class="mb-3">
        <label class="form-label">Pincode</label>
        <input type="text" class="form-control" v-model="parkingLot.pincode" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Number of Spots</label>
        <input type="number" class="form-control" v-model="parkingLot.number_of_spot" required />
      </div>

      <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
        {{ isSubmitting ? 'Saving…' : 'Create Parking Lot' }}
      </button>
    </form>
  </div>
</template>

<script>
import countriesData from '@/assets/countries.json'
import statesData    from '@/assets/states.json'
import citiesData    from '@/assets/cities.json'

export default {
  data () {
    return {
      parkingLot: {
        prime_location_name: '',
        price: '',
        address_line1: '',
        address_lin2: '',
        city: '',
        state: '',
        country: '',
        pincode: '',
        number_of_spot: 0
      },
      success: '',
      error: '',
      isSubmitting: false,

      // dropdown data
      countries: [],
      states: [],
      cities: [],
      selectedCountry: '',
      selectedState: ''
    }
  },

  mounted () {
    this.countries = countriesData
  },

  watch: {
    selectedCountry (iso2) {
      this.states = statesData.filter(s => s.country_code === iso2)
      this.selectedState = ''
      this.cities = []
      this.parkingLot.country = this.countries.find(c => c.iso2 === iso2)?.name || ''
    },
    selectedState (stateCode) {
      this.cities = citiesData.filter(
        ct => ct.state_code === stateCode && ct.country_code === this.selectedCountry
      )
      this.parkingLot.state = this.states.find(s => s.state_code === stateCode)?.name || ''
    }
  },

  methods: {
    async submitForm () {
      this.isSubmitting = true
      this.success = this.error = ''

      try {
        const token = localStorage.getItem('token') || ''
        const res = await fetch('/api/create_parking_lot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`   // ⬅️ send token
          },
          body: JSON.stringify(this.parkingLot)
        })

        const data = await res.json()

        if (res.ok) {
          this.success = '✅ Parking lot created successfully!'
          this.$router.push('/admin-dashboard') // redirect to dashboard
          this.resetForm()
        } else {
          this.error = data.error || data.message || '❌ Failed to create parking lot.'
        }
      } catch (err) {
        console.error(err)
        this.error = '⚠️ Network error. Please try again later.'
      } finally {
        this.isSubmitting = false
      }
    },

    resetForm () {
      this.parkingLot = {
        prime_location_name: '',
        price: '',
        address_line1: '',
        address_lin2: '',
        city: '',
        state: '',
        country: '',
        pincode: '',
        number_of_spot: 0
      }
      this.selectedCountry = ''
      this.selectedState = ''
      this.states = []
      this.cities = []
    }
  }
}
</script>
