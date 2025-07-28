<template>
    <div class="container mt-5">
  <div class="card p-3 shadow-sm">
    <h5 class="text-center text-primary">Parking Summary</h5>
    <canvas id="summaryChart" height="200"></canvas>
  </div>
</div>

</template>
<script>
import { Chart, BarElement,BarController, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
Chart.register(BarElement, BarController, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  data() {
    return {
      stats: {
        total_bookings: 0,
        completed: 0,
        in_use: 0
      }
    };
  },
  mounted() {
    this.fetchSummary();
  },
  methods: {
    async fetchSummary() {
      try {
        const res = await fetch('/api/user/parking_summary', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
          }
        });
        const data = await res.json();
        this.stats = data;
        this.renderChart();
      } catch (err) {
        console.error('Failed to load summary', err);
      }
    },
    renderChart() {
      const ctx = document.getElementById('summaryChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Total', 'Completed', 'In Use'],
          datasets: [{
            label: 'Booking Stats',
            data: [
              this.stats.total_bookings,
              this.stats.completed,
              this.stats.in_use
            ],
            backgroundColor: ['#0d6efd', '#198754', '#ffc107']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }
  }
}

</script>