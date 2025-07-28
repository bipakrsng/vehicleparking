import  {createRouter,createWebHistory} from 'vue-router'

import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import UserDashboard from '@/components/UserDashboard.vue' 
import AdminDashboard from '@/components/AdminDashboard.vue'
import AddParkingLot from '@/components/AddParkingLot.vue'
import EditParkingLot from '@/components/EditParkingLot.vue'
import AllUser from '@/components/AllUser.vue'
import { decodeToken, isAuthenticated } from '@/utils/auth.js';
import EditProfile from '@/components/EditProfile.vue'
import SearchLotsUser from '@/components/SearchLotsUser.vue'
import Booking from '@/components/Booking.vue'
import ParkingSpotDetails from '@/components/ParkingSpotDetails.vue'
import UserParkingSummary from '@/components/SummaryUser.vue'



const routes = [
    {path:'/',component:Home,
      beforeEnter: (to, from, next) => {
        if (isAuthenticated() === 'admin'){
          next('/admin-dashboard'); // Redirect to admin dashboard if logged in as admin
        }
        else if (isAuthenticated() === 'user') {
          next('/user-dashboard'); // Redirect to user dashboard if logged in as user
        }
        else{
          next()
        }
    }},
    {path:'/login',component:Login,
      beforeEnter: (to, from, next) => {
        if (isAuthenticated() === 'admin'){
          next('/admin-dashboard'); // Redirect to admin dashboard if logged in as admin
        }
        else if (isAuthenticated() === 'user') {
          next('/user-dashboard'); // Redirect to user dashboard if logged in as user
        }
        else{
          next()
        }
    }},
    {path:'/register',component:Register},
    {
    path: '/user-dashboard',
    component: UserDashboard,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'user') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/admin-dashboard',
    component: AdminDashboard,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {path:'/add-parking-lot',component:AddParkingLot,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
  }},
  {
    path: '/edit_parking_lot/:id',
    component: EditParkingLot, props:true,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/all_users',
    component: AllUser,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/edit_profile',component: EditProfile,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'user' || user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/search_lots_user', component: SearchLotsUser,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'user') {
        next();
      } else {
        next('/login');
      }
    }
  },
  {
    path: '/booking/:lotId',
    name: 'booking',props:true,
    component: Booking,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'user') {
        next();
      } else {
        next('/login');
      }
    },
  },
  {
    path: '/parking-spot-details/:id',
    name: 'spotDetails', props: true,
    component: ParkingSpotDetails,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'admin') {
        next();
      } else {
        next('/login');
      }
  }},
  {
    path:'/user_parking_summary',
    name: 'userParkingSummary',
    component: UserParkingSummary,
    beforeEnter: (to, from, next) => {
      const user = decodeToken();
      if (user && user.role === 'user') {
        next();
      } else {
        next('/login');
      }
    }
  },
  // Catch-all route for 404 Not Found
  

  { path: '/:pathMatch(.*)*', redirect: '/' }

]

const router = createRouter({
    history: createWebHistory(),
    routes
    })

    export default router;