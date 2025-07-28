// 🚀 Vue component to edit parking lot details
<template>
  <div class="container py-4">
    <h2 class="text-center mb-4">Edit Parking Lot</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <form v-else @submit.prevent="updateLot">
      <div class="mb-3">
        <label class="form-label">Prime Location Name</label>
        <input v-model="lot.prime_location_name" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Price</label>
        <input v-model.number="lot.price" type="number" step="0.01" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Address Line 1</label>
        <input v-model="lot.address_line1" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Address Line 2</label>
        <input v-model="lot.address_lin2" type="text" class="form-control" />
      </div>
      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label">City</label>
          <input v-model="lot.city" type="text" class="form-control" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">State</label>
          <input v-model="lot.state" type="text" class="form-control" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Country</label>
          <input v-model="lot.country" type="text" class="form-control" required />
        </div>
        <div class="col-md-6 mb-3">
          <label class="form-label">Pincode</label>
          <input v-model="lot.pincode" type="text" class="form-control" />
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Update</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ['id'], // parking lot ID from route params
  data() {
    return {
      lot: {},
      loading: true,
      error: null
    };
  },
  async mounted() {
      console.log(this.id)
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`/api/edit_parking_lot/${this.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const data = await res.json();
      if (res.ok) {
        this.lot = data;
      } else {
        this.error = data.message || 'Failed to load lot';
      }
    } catch (err) {
      this.error = 'Error loading lot details';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async updateLot() {
      
      const token = localStorage.getItem('token');
      try {
        const res = await fetch(`/api/edit_parking_lot/${this.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(this.lot)
        });

        const data = await res.json();
        if (res.ok) {
          alert('Updated successfully');
          this.$router.push('/admin-dashboard');
        } else {
          alert(data.error || 'Update failed');
        }
      } catch (err) {
        alert('Network error');
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
