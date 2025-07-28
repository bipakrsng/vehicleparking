<template>
  <section class="h-100 bg-dark">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col">
          <div class="card card-registration my-4">
            <div class="row g-0">
              <!-- Left‑side hero image -->
              <div class="col-xl-6 d-none d-xl-block">
                <img
                  src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/img4.webp"
                  alt="Sample"
                  class="img-fluid"
                  style="border-top-left-radius:.25rem;border-bottom-left-radius:.25rem;"
                />
              </div>

              <!-- Right‑side form -->
              <div class="col-xl-6">
                <form class="card-body p-md-5 text-black" @submit.prevent="submitForm">
                  <h3 class="mb-5 text-uppercase">User Registration</h3>

                  <!-- 1️⃣ Name -->
                  <div class="row">
                    <div class="col-md-6 mb-4">
                      <input v-model="form.first_name" type="text" class="form-control form-control-lg"
                             placeholder="First name" required />
                    </div>
                    <div class="col-md-6 mb-4">
                      <input v-model="form.last_name" type="text" class="form-control form-control-lg"
                             placeholder="Last name" required />
                    </div>
                  </div>

                  <!-- 2️⃣ Username / Email / Password -->
                  <div class="mb-4">
                    <input v-model="form.username" type="text" class="form-control form-control-lg"
                           placeholder="Username" required />
                  </div>
                  <div class="mb-4">
                    <input v-model="form.email" type="email" class="form-control form-control-lg"
                           placeholder="Email ID" required />
                  </div>
                  <div class="mb-4">
                    <input v-model="form.password" type="password" class="form-control form-control-lg"
                           placeholder="Password" required />
                  </div>

                  <!-- 3️⃣ Phone & DOB -->
                  <div class="mb-4">
                    <input v-model="form.phone_number" type="text" class="form-control form-control-lg"
                           placeholder="Phone Number" />
                  </div>
                  <div class="mb-4">
                    <input v-model="form.date_of_birth" type="date" class="form-control form-control-lg"
                           placeholder="Date of Birth" />
                  </div>

                  <!-- 4️⃣ Gender -->
                  <div class="d-md-flex justify-content-start align-items-center mb-4 py-2">
                    <h6 class="mb-0 me-4">Gender:</h6>
                    <div class="form-check form-check-inline mb-0 me-4">
                      <input class="form-check-input" type="radio" id="femaleGender" value="female"
                             v-model="form.gender" />
                      <span class="form-check-label">Female</span>
                    </div>
                    <div class="form-check form-check-inline mb-0 me-4">
                      <input class="form-check-input" type="radio" id="maleGender" value="male"
                             v-model="form.gender" />
                      <span class="form-check-label">Male</span>
                    </div>
                    <div class="form-check form-check-inline mb-0">
                      <input class="form-check-input" type="radio" id="otherGender" value="other"
                             v-model="form.gender" />
                      <span class="form-check-label">Other</span>
                    </div>
                  </div>

                  <!-- 5️⃣ Address -->
                  <div class="mb-4">
                    <input v-model="form.address_line1" type="text" class="form-control form-control-lg"
                           placeholder="Address Line 1" />
                  </div>
                  <div class="mb-4">
                    <input v-model="form.address_line2" type="text" class="form-control form-control-lg"
                           placeholder="Address Line 2" />
                  </div>

                  <!-- 6️⃣ Country – State – City -->
                  <div class="row">
                    <div class="col-md-4 mb-4">
                      <select v-model="selectedCountry" class="form-select">
                        <option disabled value="">Select Country</option>
                        <option v-for="c in countries" :key="c.id" :value="c.iso2">
                          {{ c.name }}
                        </option>
                      </select>
                    </div>

                    <div class="col-md-4 mb-4">
                      <select v-model="selectedState" class="form-select" :disabled="!states.length">
                        <option disabled value="">Select State</option>
                        <option v-for="s in states" :key="s.id" :value="s.state_code">
                          {{ s.name }}
                        </option>
                      </select>
                    </div>

                    <div class="col-md-4 mb-4">
                      <select v-model="form.city" class="form-select" :disabled="!cities.length">
                        <option disabled value="">Select City</option>
                        <option v-for="ct in cities" :key="ct.id" :value="ct.name">
                          {{ ct.name }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- 7️⃣ Country, Pincode (separate) -->
                  <div class="mb-4">
                    <input v-model="form.country" type="text" class="form-control form-control-lg"
                           placeholder="Country (text fallback)" />
                  </div>
                  <div class="mb-4">
                    <input v-model="form.pincode" type="text" class="form-control form-control-lg"
                           placeholder="Pincode" />
                  </div>

                  <!-- Submit / Reset -->
                  <div class="d-flex justify-content-end pt-3">
                    <button type="reset" class="btn btn-light btn-lg">Reset</button>
                    <button type="submit" class="btn btn-warning btn-lg ms-2" @click="submitForm" :disabled="isSubmitting">Register</button>
                  </div>
                </form>
              </div><!-- /col-xl-6 -->
            </div><!-- /row g‑0 -->
          </div><!-- /card -->
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.card-registration .select-input.form-control[readonly]:not([disabled]) {
  font-size: 1rem;
  line-height: 2.15;
  padding-left: 0.75em;
  padding-right: 0.75em;
}
.card-registration .select-arrow {
  top: 13px;
}
</style>

<script>
/* ---------- 𝟙  Import JSON data ------------- */
import countriesData from '@/assets/countries.json'
import statesData    from '@/assets/states.json'
import citiesData    from '@/assets/cities.json'

export default {
  data () {
    return {
      /* -------------- form model -------------- */
      form: {
        first_name: '', last_name: '', username: '', email: '', password: '',
        phone_number: '', gender: '', date_of_birth: '',
        address_line1: '', address_line2: '', city: '',
        country: '', state: '', pincode: ''
      },
      isSubmitting: false,
      /* -------------- dropdown lists ---------- */
      countries: [],   // all countries
      states: [],      // states filtered by country
      cities: [],      // cities filtered by state

      /* -------------- dropdown selections ----- */
      selectedCountry: '',
      selectedState: ''
    }
  },

  /* ---------- 𝟚  Initialize country list ----- */
  mounted () {
    this.countries = countriesData
  },

  /* ---------- 𝟛  React to changes ------------ */
  watch: {
    /* Vue calls this function automatically whenever
       `selectedCountry` (v‑model on the first <select>)
       changes. The **new value** is passed as the first
       argument (`newCountryCode`). */
    selectedCountry (newCountryCode) {
      // Filter states belonging to the chosen country
      this.states = statesData.filter(
        s => s.country_code === newCountryCode
      )
      this.selectedState = ''  // reset lower levels
      this.cities = []
      // Optional: keep text copy in main form
      this.form.country = this.countries.find(
        c => c.iso2 === newCountryCode
      )?.name || ''
    },

    /* Runs whenever the user picks a state. */
   selectedState(newStateCode) {
  const selectedStateObj = this.states.find(s => s.state_code === newStateCode)

  this.cities = citiesData.filter(
    ct =>
      ct.state_code === newStateCode &&
      ct.country_code === this.selectedCountry
  )

  this.form.state = selectedStateObj?.name || ''
}

  },

  /* ---------- 𝟜  Submission handler ---------- */
  methods: {
  async submitForm () {
    this.isSubmitting = true
    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })

      const data = await res.json()

      if (res.ok) {
        // ✅ Registration successful
        alert(`✅ Registration successful! Welcome, ${data.username}`)
        this.$router.push('/login')
      } else {
        // ❌ Error from backend (e.g., validation or conflict)
        this.error = data.error || data.message || 'Registration failed. Please check your input.'
      }
    } catch (err) {
      // ❌ Network or unexpected error
      console.error(err)
      this.error = 'An error occurred. Please check your connection and try again.'
    }
  }
}

}
</script>
