<template>
<nav class="navbar navbar-expand-lg bg-dark navbar-dark">
  <div class="container-fluid">

    <!-- Logo -->
    <img src="@/assets/images/logo.png"
         alt="PlaceMint Logo"
         width="69"
         height="50"
         class="d-inline-block align-text-top">

    <a class="navbar-brand ms-2">PlaceMint</a>
 <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div class="navbar-nav">

        <!-- If user logged in -->
        <div v-if="token" class="d-flex">

          <!-- ADMIN -->
                    <!-- ADMIN -->
          <template v-if="role === 'admin'">
            <router-link class="nav-link" to="/auth/dashboard">Dashboard</router-link>
            <router-link class="nav-link" to="/admin/users">Users</router-link>
            <router-link class="nav-link" to="/admin/drives">Drives</router-link>
            <button class="btn btn-danger btn-logout ms-3" @click="logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-power" viewBox="0 0 16 16">
                <path d="M7.5 1v7h1V1z"/>
                <path d="M3 8.812a5 5 0 0 1 2.578-4.375l-.485-.874A6 6 0 1 0 11 3.616l-.501.865A5 5 0 1 1 3 8.812"/>
              </svg>
          </button>
          </template>

          <!-- COMPANY -->
          <template v-else-if="role === 'company'">
            <router-link class="nav-link" to="/auth/dashboard">Dashboard</router-link>
            <router-link class="nav-link" to="/company/create-drive">Create Drive</router-link>
            <button class="btn btn-danger btn-logout ms-3" @click="logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-power" viewBox="0 0 16 16">
                <path d="M7.5 1v7h1V1z"/>
                <path d="M3 8.812a5 5 0 0 1 2.578-4.375l-.485-.874A6 6 0 1 0 11 3.616l-.501.865A5 5 0 1 1 3 8.812"/>
              </svg>
          </button>
            <router-link class="nav-link class-profile" to="/auth/profile">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
              </svg>
            </router-link>
          </template>

          <!-- STUDENT -->
          <template v-else-if="role === 'student'">
            <router-link class="nav-link" to="/auth/dashboard">Dashboard</router-link>
            <router-link class="nav-link" to="/student/history">History</router-link>
            <button class="btn btn-danger btn-logout ms-3" @click="logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-power" viewBox="0 0 16 16">
                <path d="M7.5 1v7h1V1z"/>
                <path d="M3 8.812a5 5 0 0 1 2.578-4.375l-.485-.874A6 6 0 1 0 11 3.616l-.501.865A5 5 0 1 1 3 8.812"/>
              </svg>
            </button>
            <router-link class="nav-link class-profile" to="/auth/profile">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
                <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
              </svg>
            </router-link>
          </template>

        </div>

        <!-- If NOT logged in -->
        <div v-else class="d-flex">
          <router-link class="nav-link" to="/">Home</router-link>
          <router-link class="nav-link" to="/login">Login</router-link>
          <router-link class="nav-link" to="/register">Register</router-link>
        </div>

      </div>
</div>
  </div>
</nav>
</template>

<script>
export default {

  data(){
    return{
      token: null,
      role: null
    }
  },

  mounted(){
    this.loadUser()
  },
  watch:{
    $route(){
      this.loadUser()
    }
  },
  methods:{

    loadUser(){
      this.token = localStorage.getItem("token")
      this.role = localStorage.getItem("role")
      // this.$router.go(0)
    },

    logout(){
      localStorage.removeItem("token")
      localStorage.removeItem("role")

      this.token = null
      this.role = null

      this.$router.push("/login")
      // this.$router.go(0)
    }

  }

}
</script>


<style scoped>

.container-fluid {
  /* width: 50%; */
  /* margin-right: auto; */
  margin-left: 0;
  padding: 0px 28px 0px 0px;
  border: 2px solid #008000;
  border-left: none;
  border-right: none;
  /* border-radius: 0px 2px 35px 0px; */
}
.navbar-brand {
  color: white !important;
}
.nav-link {
  color: white;
  /* border: 1px solid red; */
  /* width: 80px; */
  margin-right: 5px;
}
.nav-link:hover {
  color: #008000 !important;
}
.router-link-active {
  font-weight: bold !important;
  color: #008000 !important;
}

.nav-div-flex{
  display: flex;
}

.btn-logout{
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
  height: 40px;
  width: 40px;
  padding: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #fd0000;     
  border: 1px solid rgba(192, 54, 54, 0.313);

  transition: all 0.25s ease;
}

.btn-logout:hover{
  background: rgba(255,77,77,0.15);
  border-color: #ff4d4d;
  color: #ff6b6b;
  transform: scale(1.05);
}


.class-profile{
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
  height: 40px;
  width: 40px;
  padding: 0;
  margin-left: 10px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #241cb5;     
  border: 1px solid rgba(108, 99, 255, 0.3);

  transition: all 0.25s ease;
}

.class-profile:hover{
  background: rgba(108, 99, 255, 0.2);
  border-color: #6c63ff;
  color: #2a04b7 !important;
  transform: scale(1.05);
}

.class-profile.router-link-active {
  font-weight: bold !important;
  color: #2a04b7 !important;
}
</style>