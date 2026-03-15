<template>
    <div class="canvas">

        <div class="upper-div">
            <div class="request-table glass-effect">
                <div class="details-container">
                <h2>Drive</h2><br>
                <div class="details">
                    <span class="details-span">Job Title:  </span> <span>{{ drive.job_title }}</span>
                </div>
                <div class="details"><span class="details-span">Job Description: </span><br>
                    <span>{{ drive.job_description }}</span>
                </div>
                <div class="details">
                    <span class="details-span">Company Name: </span> <span>{{ drive.company_name }}</span>
                </div>
                <div class="details">
                    <span class="details-span">Eligible Department: </span> <span>{{ drive.eligibility_dept }}</span>
                </div>
                <div class="details">
                    <span class="details-span">Eligible CGPA: </span> <span>{{ drive.eligibility_cgpa }}</span>
                </div>
                <div class="details">
                    <span class="details-span">Offered Salary: </span> <span>{{ drive.salary }} LPA</span>
                </div>
                <div class="details">
                    <span class="details-span">Deadline: </span> <span>{{formatDate( drive.deadline )}}</span>
                </div>
                </div>
                <div class="btn-container">
                    <button class="btn btn-primary-green btn-login" @click="goBack">
Go Back
</button>

<button
v-if="role === 'student' && !already_applied"
class="btn btn-success"
@click="applyDrive"
>
Apply
</button>

<button
v-if="role === 'student' && already_applied"
class="btn btn-secondary"
disabled
>
Already Applied
</button>
                </div>
            </div>
            
        </div>
    </div>        
</template>
<script>

import axios from "axios"

export default{

name:"DriveDetails",

data(){

return{

token:"",
role:"",
driveId:null,

drive:{},
already_applied:false

}

},

mounted(){

this.token = localStorage.getItem("token")
this.role = localStorage.getItem("role")

this.driveId = this.$route.params.driveId

this.fetchDrive()

},

methods:{

fetchDrive(){

axios.get(`http://127.0.0.1:5000/api/company/drive/${this.driveId}`,{

headers:{
Authorization:`Bearer ${this.token}`
}

})

.then(res=>{

this.drive = res.data.drive
this.already_applied = res.data.already_applied

})

.catch(err=>{
console.log(err.response || err.message)
})

},

applyDrive(){

axios.post(`http://127.0.0.1:5000/api/student/apply/${this.driveId}`,{},{

headers:{
Authorization:`Bearer ${this.token}`
}

})

.then(res=>{

alert(res.data.message)

this.already_applied = true

})

.catch(err=>{
console.log(err.response || err.message)
})

},

goBack(){

this.$router.go(-1)

},
formatDate(date) {
    return new Date(date).toLocaleString("en-IN",{
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  })
    }

}

}

</script>
<style scoped>
.canvas {
  width: 100%;
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.upper-div {
  display: flex;
  flex-direction: column;
  /* gap: 24px; */
  padding: 24px;
  align-items: center;
  justify-content: center;
}

.request-table {
  /* flex: 1; */
  height: 90%;
  width: 60%;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  display: flex;
    flex-direction: column;
  align-items: center;
  padding: 15px 30px;
}

.details-container{
    display: flex;
    flex-direction: column;
    justify-content: start;
}

.details{
    margin-bottom: 15px;
}

.details-span{
    font-weight: bold;
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
/* .btn-success{
    color: #054d05;
} */

.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}
</style>