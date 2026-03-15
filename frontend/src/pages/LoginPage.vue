<template>
 <div class="canvas">
    <div class="image-conatiner">
    </div>
    <div class="main-container glass-effect">
        <div class="heading">
        <h4>Welcome to</h4>
        <div class="brand-name">
            <span>Place</span><span class="green">Mint</span>
        </div>
        </div>
        <p class="alert alert-danger" v-if="error">{{ error }}</p>
        <form class="form-holder" @submit.prevent="login">
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label white-text">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com" v-model="FormData.username">
            </div>
            <div class="mb-3">
                <label for="inputPassword" class="form-label white-text">Password</label>
                    <input type="password" class="form-control" id="inputPassword" v-model="FormData.password">
            </div>

        <div class="btn-container">
            <button  class="btn btn-primary-green btn-login">Sign In</button>
            <router-link to="/register" class="white-text">New on PlaceMint?  <a href="">Register here</a></router-link>
            <!-- <button class="btn btn-secondary">Register</button> -->
        </div>
        </form>

    </div>
 </div>
</template>

<script>
import axios from 'axios';
export default{
    data(){
        return{
            FormData:{
                username:"",
                password:""
            },
            token:"",
            error: ""
        }
    },

    methods:{

        login(){
            // console.log(`Username: ${this.FormData.username}, password: ${this.FormData.password}`)
            const response = axios.post("http://127.0.0.1:5000/api/auth/login", JSON.stringify(this.FormData),{
                headers: {
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
                // "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.token = res.data.access_token
                    localStorage.setItem("token", res.data.access_token)
                    localStorage.setItem("role", res.data.role)
                    this.$router.replace(`/auth/dashboard`)
                    // this.$router.go(0)
            }).catch(
                err => this.error = err.response.data)
                //  console.log(err.response))
            
        }
    }
}
</script>

<style scoped>
body, html {
    margin: 0;
    padding: 0;
    overflow: hidden;
}
.canvas {
    width: 100vw;
    height: 100vh;
    background-color: black;
    background-size: cover;
    background-position: center;
    display: flex;
    /* justify-content: center; */
    flex-direction: row;
    padding: 10px;
}
.image-conatiner {
    width: 50%;
    height: 80dvh;
    /* border: 1px solid red; */
    background-image: url('@/assets/images/homePage.png');
    background-size: cover;
    background-position: center;
    
}

.main-container {
    /* position: absolute; */
    /* top: 16%; */
    left: 55%;
    /* border: 1px solid yellow; */
    width: 450px;
    height: 480px;
    display: flex;
    /* justify-content: center; */
    align-items: center;
    flex-direction: column;
    padding: 10px 15px 10px 15px;
}
.heading {
    height: 100px;
    margin: 0px;
}

.main-container h4 {
    color: white;
    margin: 0px 0px 0px 30px;
}
.brand-name {
    font-size: 48px;
    font-weight: bold;
    color: white;

}
.green {
    color: #008000;
}
.btn {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    cursor: pointer;
    margin: 10px;
}
.btn-primary-green {
    background-color: #056805;
    color: white;
}
.btn-primary-green:hover {
    background-color: #054d05;
    color: #ffffff;
    /* border: 1px solid #054d05; */
}
.btn-secondary {
    background-color: transparent;
    color: #056805;
    border: 1px solid #056805;
}
.btn-secondary:hover {
    background-color: #056805;
    color: white;
}
.btn-container {
    /* height: 100px; */
    width: 100%;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    align-items: center;
}

.btn-login {
    width: 90%;
}

a {
    color: #099a09;
    text-decoration: none;
}

.white-text {
    color: white;
}

.glass-effect {
  background: rgba(0, 0, 0, 0.162);
  backdrop-filter: blur(9px);
  -webkit-backdrop-filter: blur(11px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.105);
  box-shadow: 5px 5px 25px -2px rgba(250, 250, 250, 0.10);
} 

.form-holder {
    width: 85%;
    height: 300px;
    /* border: 1px solid red; */
    display: flex;
    flex-direction: column;
    margin-top: 30px;
}
.form-holder .form-control {
    background-color: transparent;
    /* color: white; */
    border: 1px solid #056805;
}

.form-control:focus {
    background-color: transparent;
    border: 1px solid #056805;
    width: 350px;
    /* margin-left: 20px; */
    color: rgba(255, 255, 255, 0.751);
    box-shadow: 0 0 0 0.25rem rgba(5, 104, 5, 0.25);
}

.alert.alert-danger{
    height: 40px;
    padding: 5px;
    margin: 0;
    border-color: #fe0f0bdb;
    background-color: transparent;
    /* color: rgb(221, 217, 217); */
    color: #fe0f0bdb;
}

</style>