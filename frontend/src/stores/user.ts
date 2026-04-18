import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

type User = {
  id: number
  username: string
};

export const userStore = defineStore('auth',{
  state: () => ({
    token: localStorage.getItem('accessToken') as string | null,
    refreshToken: localStorage.getItem('refreshToken') as string | null,
    user: (localStorage.getItem('user') ? JSON.parse(localStorage.getItem("user")!) as User : null) as User | null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    username: (state) => state.user?.username ?? '',
  },
  actions: {
    setToken(token: string | null) {
      this.token = token;
      if (token) {
          localStorage.setItem("accessToken", token);
      }
      else{
          localStorage.removeItem("accessToken");

      }
    },
    setUser(user:User | null){
      this.user = user;
      if(user){
        localStorage.setItem('user', JSON.stringify(user))
      }
      else{
        localStorage.removeItem('user')
      }
    },
    async login(username: string, password: string)  {
      try{
          const { data } = await api.post('login/', { username, password })
          this.setToken(data.access)
          localStorage.setItem('refreshToken', data.refresh)

          const profile = await api.get("getme/")
          this.setUser(profile.data)
          window.location.href = "/"
          return data
      }
      catch(err: any) {
          window.location.href = "/auth";
          if (err.response) {
              const status = err.response.status;
              const message = err.response.data?.detail || "Error";

              if (status === 401) {
                  throw new Error("Invalid login credentials");
              } else if (status >= 500) {
                  throw new Error("Server error");
              } else{
                  throw new Error(message)
              }
          }
          else if (err.request) {
              throw new Error('No server response');
          }
          else{
              throw new Error('Unknown error')
          }


      }
  },
  async register(username: string, password: string) {
    try {
        const { data } = await api.post('register/', { username, password })
        this.setToken(data.access)
        localStorage.setItem('refreshToken', data.refresh)

        const profile = await api.get('getme/')
        this.setUser(profile.data)
        window.location.href = "/"
        return data
        
    }
    catch(err : any){
        if (err.response) {
              const status = err.response.status;
              const message = err.response.data?.detail || "Error";

              if (status === 401) {
                  throw new Error("Invalid register data");
              } else if (status >= 500) {
                  throw new Error("Server error");
              } else{
                  throw new Error(message)
              }
          }
    }
  },

  logout() {
      this.setToken(null);
      this.setUser(null);
      localStorage.removeItem('refreshToken')
  },
  async initFromStore () {
      if (this.token && !this.user ) {
          try {
              const profile = await api.get("getme/");
              this.setUser(profile.data);

          }
          catch{
              this.logout();
          }
      }
  }


}})

