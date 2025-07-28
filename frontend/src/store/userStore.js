import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),
  actions: {
    setUserFromToken(decoded) {
      const user = decoded;
      if (!user) {
        console.error('Invalid user data');
        return;
      }
      else{
      console.log(user)
      this.user = decoded;
      }
    },
    logout() {
      this.user = null;
      localStorage.removeItem('token');
    }
  }
});
