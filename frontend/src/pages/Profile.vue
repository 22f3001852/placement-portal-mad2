<template>

<div v-if="token">

<div class="canvas">
<div class="main-container glass-effect">

<div class="heading">
<h4>Your Profile</h4>
</div>

<form class="form-holder" @submit.prevent="updateProfile">

<!-- USERNAME -->
<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Username</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.username" disabled>
</div>
</div>


<!-- STUDENT PROFILE -->
<template v-if="role === 'student'">

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Full Name</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.name">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Department</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.department">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">CGPA</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.cgpa">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Year</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.year">
</div>
</div>
<div class="mb-3 row">
                    <label for="formFile" class="col-sm-2 col-form-label white-text">Resume</label>
                    <div class="col-sm-10">
                        <input class="form-control" type="file" id="formFile" placeholder="Upload Resume..." @change="uploadFile">
                    </div>
                </div>

        <div class="btn-conatiner details-action">

          <!-- Resume -->
          <button v-if="FormData.has_resume"
          class="btn btn-outline-primary btn-resume"
          @click="viewResume(FormData.user_id)"
          >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                                      <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                                    </svg>
          View Uploaded Resume
          </button>
        </div>

</template>


<!-- COMPANY PROFILE -->
<template v-if="role === 'company'">

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Full Name</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.fullname">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Company Name</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.company_name">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">HR Contact</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.hr_contact">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Website</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.website">
</div>
</div>

<div class="mb-3 row">
<label class="col-sm-2 col-form-label white-text">Location</label>
<div class="col-sm-10">
<input class="form-control" v-model="FormData.location">
</div>
</div>

</template>


<div class="btn-container">

<p class="alert alert-danger" v-if="error">
{{ error }}
</p>

<p class="alert alert-success" v-if="success">
{{ success }}
</p>

<button class="btn btn-primary-green btn-login">
Update Profile
</button>

</div>

</form>

</div>
</div>
</div>


<div v-else>
<h2>Token Expired. Please Login Again.</h2>
</div>

</template>



<script>
import axios from "axios"

export default{

data(){

return{

token:null,
role:null,

FormData:{
    user_id:"",
username:"",
name:"",
fullname:"",
department:"",
cgpa:"",
year:"",
resume:null,
has_resume:false,
company_name:"",
hr_contact:"",
website:"",
location:""
},


error:"",
success:""

}

},

mounted(){
this.loadUser()
this.getProfile()
},

methods:{

loadUser(){

this.token = localStorage.getItem("token")
this.role = localStorage.getItem("role")

},

getProfile(){

axios.get(
"http://127.0.0.1:5000/api/auth/profile",
{
headers:{
Authorization:`Bearer ${this.token}`
}
}
)

.then(res=>{

this.FormData = res.data

})

.catch(err=>{

this.error = err.response?.data?.message || "Failed to load profile"

})

},

updateProfile(){

const formData = new FormData()

formData.append("name", this.FormData.name)
formData.append("department", this.FormData.department)
formData.append("cgpa", this.FormData.cgpa)
formData.append("year", this.FormData.year)

if(this.FormData.resume){
formData.append("resume", this.FormData.resume)
}

axios.put(
"http://127.0.0.1:5000/api/auth/profile",
formData,
{
headers:{
Authorization:`Bearer ${this.token}`,
"Content-Type":"multipart/form-data"
}
}
)

.then(res=>{
this.success = "Profile Updated Successfully"
this.getProfile()
})

.catch(err=>{
this.error = err.response?.data?.message || "Update Failed"
})

},
    viewResume(user_id){
        window.open(`http://127.0.0.1:5000/api/auth/resume/${user_id}`,"_blank")
    },
uploadFile(event) {
      const file = event.target.files[0];
      if (file) {
        this.FormData.resume = file;
      }
    },
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
    /* background-size: cover;
    background-position: center; */
    display: flex;
    /* justify-content: center; */
    flex-direction: row;
    justify-content: space-around;
    padding: 10px;
}

.main-container {

    width: 50%;
    height: fit-content;
    min-height: 500px;
    display: flex;
    align-items: center;
    flex-direction: column;
    padding: 10px 0px 10px 100px;
    overflow-y: auto;
}
.heading {
    margin-top: 10px;
}

.main-container h4 {
    color: white;
    /* margin: 0px 0px 0px 30px; */
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

    width: 100%;
    margin-top: 20px;
    display: flex;
    flex-direction: column;

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
    width: 100%;
    height: 300px;

    display: flex; 
    justify-content: space-around;
    flex-direction: column;
    margin-top: 30px;
    /* align-items: center; */
}

/* .col-form-label{
    width: 180px;
    border: 1px solid red; 
} */

.form-holder .form-control {
    background-color: transparent;
    border: 1px solid #056805;
    width: 300px;
    margin-left: 10px;
    color: rgba(255, 255, 255, 0.454);

}
.form-control:focus {
    background-color: transparent;
    border: 1px solid #056805;
    /* width: 350px; */
    /* margin-left: 20px; */
    color: rgba(255, 255, 255, 0.751);
    box-shadow: 0 0 0 0.25rem rgba(5, 104, 5, 0.25);
}

/* .col-sm-10{
    width:300px ;
} */
.row{
    padding: 0;
}
select.form-control option {
    background-color: white;
    color: black;
}

.alert.alert-success{
    height: 40px;
    padding: 5px;
    margin: 0;
    color: #056805;
    background-color: transparent;
    border-color: #054d05;
    margin-top: 10px;

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
.btn-resume{
    border: 1px solid rgb(71, 71, 241);
}
</style>