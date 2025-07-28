<template>
  <section class="vh-100 gradient-custom">
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <div class="card bg-dark text-white" style="border-radius: 1rem;">
            <div class="card-body p-5 text-center">

              <div class="mb-md-5 mt-md-4 pb-5">
                <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
                <p class="text-white-50 mb-5">Please enter your login and password!</p>

                <div class="form-outline form-white mb-4">
                  <input
                    type="email"
                    id="typeEmailX"
                    class="form-control form-control-lg"
                    placeholder="Email"
                    v-model="cred.email"
                  />
                </div>

                <div class="form-outline form-white mb-4">
                  <input
                    type="password"
                    id="typePasswordX"
                    class="form-control form-control-lg"
                    placeholder="Password"
                    v-model="cred.password"
                  />
                </div>

                <p class="small mb-5 pb-lg-2">
                  <a class="text-white-50" href="#!">Forgot password?</a>
                </p>

                <button
                  class="btn btn-outline-light btn-lg px-5"
                  type="submit"
                  @click="login"
                >
                  Login
                </button>

                <div class="d-flex justify-content-center text-center mt-4 pt-1">
                  <a href="#!" class="text-white"><i class="fab fa-facebook-f fa-lg"></i></a>
                  <a href="#!" class="text-white"><i class="fab fa-twitter fa-lg mx-4 px-2"></i></a>
                  <a href="#!" class="text-white"><i class="fab fa-google fa-lg"></i></a>
                </div>
              </div>

              <div>
                <p class="mb-0">Don't have an account? <a href="/register" class="text-white-50 fw-bold">Sign Up</a></p>
              </div>

              <div v-if="error" class="text-danger mt-3">{{ error }}</div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { decodeToken } from '@/utils/auth';
import { useUserStore } from '@/store/userStore';

export default {
  data() {
    return {
      cred: {
        email: null,
        password: null
      },
      error: null
    };
  },
  methods: {
    async login() {
      try {
        const res = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.cred)
        });
        const data = await res.json();

        if (res.ok) {
          localStorage.setItem('token', data.token);

          const decoded = decodeToken(); // securely decode the token
          const store = useUserStore();
          store.setUserFromToken(decoded); // update global state

          // Role-based redirect
          if (decoded.role === 'admin') {
            this.$router.push('/admin-dashboard');
          } else if (decoded.role === 'user') {
            this.$router.push('/user-dashboard');
          } else {
            this.$router.push('/'); // fallback or error route
          }

        } else {
          this.error = data.error || 'Invalid login credentials';
        }
      } catch (err) {
        this.error = 'An error occurred. Please check your connection and try again.';
      }
    }
  }
};
</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(to right, rgba(106, 17, 203, 1), rgba(37, 117, 252, 1));
}
</style>
