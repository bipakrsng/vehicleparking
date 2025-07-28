<template>
  <section id="features" class="py-1">
    <div class="container py-5">
      <h2 class="text-center mb-4">Features</h2>
      <div class="row">
        <!-- Column 1 -->
        <div class="col-md-4 d-flex text-center p-3">
          <div class="feature-card p-4 rounded shadow w-100 text-white">
            <i class="bi bi-search fs-1 text-primary"></i>
            <h5 class="mt-3">Search Nearby Parking</h5>
            <p>Use GPS to locate available parking spots in real-time.</p>
          </div>
        </div>
        
        <!-- Column 2 -->
        <div class="col-md-4 d-flex text-center p-3">
          <div class="feature-card p-4 rounded shadow w-100 text-white">
            <i class="bi bi-calendar-check fs-1 text-primary"></i>
            <h5 class="mt-3">Reserve in Advance</h5>
            <p>Book your spot before you arrive and avoid the hassle.</p>
          </div>
        </div>
        
        <!-- Column 3 -->
        <div class="col-md-4 d-flex text-center p-3">
          <div class="feature-card p-4 rounded shadow w-100 text-white">
            <i class="bi bi-credit-card fs-1 text-primary"></i>
            <h5 class="mt-3">Cashless Payments</h5>
            <p>Pay online through UPI, cards, or wallet.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.feature-card {
  background-color: rgba(0, 0, 0, 0.4);
  height: 100%; /* 🔥 Let flexbox stretch it */
}
</style>
