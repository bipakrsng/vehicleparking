<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark text-light">
    <a class="navbar-brand" href="#">ParkEase</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="/">Home</a>
        </li>

        <!-- If user is logged in and role is 'user' -->
        <template v-if="user && user.role === 'user'">
          <li class="nav-item"><a class="nav-link" href="/user-dashboard">Welcome {{ user.email}}</a></li>
          <li class="nav-item"><a class="nav-link" href="/user_parking_summary">Summary</a></li>
          <li class="nav-item"><a class="nav-link" href="/edit_profile">Edit Profile</a></li>
        </template>

        <!-- If user is logged in and role is 'admin' -->
        <template v-if="user && user.role === 'admin'">
          <li class="nav-item"><a class="nav-link" href="/admin-dashboard">Welcome {{ user.email}}</a></li>
          <li class="nav-item"><a class="nav-link" href="/add-parking-lot">Add Lot</a></li> 
          <li class="nav-item"><a class="nav-link" href="/all_users">Manage Users</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Search</a></li>
          <li class="nav-item"><a class="nav-link" href="#">Summary</a></li>
          <li class="nav-item"><a class="nav-link" href="/edit_profile">Edit profile</a></li>
        </template>
      </ul>

      <ul class="navbar-nav ms-auto">
        <!-- Not logged in -->
        <template v-if="!user">
          <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/register">Register</a>
          </li>
        </template>

        <!-- Logged in -->
        <template v-else>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
          </li>
        </template>
      </ul>
    </div>
  </nav>
</template>

<script>
import { decodeToken, logoutUser } from '@/utils/auth';
import { useUserStore } from '@/store/userStore';


export default {
  data() {
    return {
      user: null
    };
  },
  computed :{
    user() {
      const userStore = useUserStore();
      return userStore.user;  // Access user from the Pinia store
    }
  },
  
  methods: {
    handleLogout() {
      logoutUser();              // remove token & clear store
      this.user = null;          // reset local component state
      this.$router.push('/login');
    }
  },
  
};
</script>
