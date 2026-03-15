<template>
<div v-if="token">
<div class="canvas">

  <div class="upper-div">
    <div class="request-table glass-effect">

      <div class="details-container">

        <h2>Student Application</h2><br>

        <!-- STUDENT DETAILS -->

        <div class="details">
          <span class="details-span">Student Code:</span>
          <span>{{ student.student_code }}</span>
        </div>

        <div class="details">
          <span class="details-span">Student Name:</span>
          <span>{{ student.fullname }}</span>
        </div>

        <div class="details">
          <span class="details-span">Department:</span>
          <span>{{ student.department }}</span>
        </div>

        <div class="details">
          <span class="details-span">CGPA:</span>
          <span>{{ student.cgpa }}</span>
        </div>

        <div class="details">
          <span class="details-span">Current Year:</span>
          <span>{{ student.year }}</span>
        </div>

        <!-- DRIVE DETAILS -->

        <div class="details">
          <span class="details-span">Job Title:</span>
          <span>{{ drive.job_title }}</span>
        </div>

        <div class="details">
          <span class="details-span">Offered Salary:</span>
          <span>{{ drive.salary }} LPA</span>
        </div>

        <div class="details">
          <span class="details-span">Applied On:</span>
          <span>{{formatDate( drive.deadline )}}</span>
        </div>
        <!-- <div class="details">
          <span class="details-span">Applied On:</span>
          <span>{{ formatDate(application.applied_on) }}</span>
        </div> -->

        <!-- ACTION AREA -->

        <div class="btn-conatiner details-action">

          <!-- Resume -->
          <button
          class="btn btn-outline-primary btn-resume"
          @click="viewResume(student.id)"
          >
          View Resume
          </button>

          <!-- if company -->
          <select v-if="role === 'company'" class="form-select form-control" v-model="status">
            <option value="applied">Applied</option>
            <option value="shortlisted">Shortlisted</option>
            <option value="selected">Selected</option>
            <option value="rejected">Rejected</option>
          </select>

          <!-- if admin -->
          <span v-else class="badge btn":class="statusBadge"> {{ application.status }} </span>

        </div>

      </div>

      <!-- BUTTONS -->

      <div class="btn-container">
<p class="alert alert-danger" v-if="error">{{ error }}</p>
        <p class="alert  alert-success" v-if="success">{{ success }}</p>
        <button
        v-if="role === 'company'"
        class="btn btn-primary-green btn-login"
        @click="updateStatus"
        >
        Save Changes
        </button>

        <button
        class="btn btn-primary-green btn-login"
        @click="goBack"
        >
        Go Back
        </button>

      </div>

    </div>
  </div>

</div>
    </div>
    <div v-else>
        <h1>Please Login!</h1>
    </div>
</template>



<script>
import axios from "axios"

export default {
    data(){
        return{
            token:"",
            role:"",
            error:"",
            success:"",

            student:{},
            drive:{},
            application:{},

            status:"applied"

            }
    },
    mounted(){
        this.loadToken()
        this.role = localStorage.getItem("role")

        this.fetchApplication()
},

    computed:{
        statusBadge(){
            if(this.application.status === "applied"){
                return "primary disabled"
            }
            if(this.application.status === "shortlisted"){
                return "warning disabled"
            }
            if(this.application.status === "selected"){
                return "success disabled"
            }   
            if(this.application.status === "rejected"){
                return "danger disabled"
            }
    }

},

methods:{
    loadToken(){
      const token = localStorage.getItem('token'); // here token refers to local storage token
      if(token){   // if there is an local storage token
        this.token = token; // then assign that token to this page's data token
      }
    },
    fetchApplication(){

    const applicationId = this.$route.params.applicationId

        const response = axios.get(`http://127.0.0.1:5000/api/company/application/${applicationId}`,{
                headers:{
                Authorization:`Bearer ${this.token}`
                }
            })
            response.then(res=>{

                this.student = res.data.student
                this.drive = res.data.drive
                this.application = res.data.application

                this.status = res.data.application.status

                })
            .catch(err=>{
            console.log(err.response || err.message)
                // this.error = err.response?.data?.message || "There is an error!"
            })

    },

    viewResume(user_id){
        window.open(`http://127.0.0.1:5000/api/auth/resume/${user_id}`,"_blank")
    },

    updateStatus(){
        const applicationId = this.$route.params.applicationId

        axios.post(`http://127.0.0.1:5000/api/company/update-status/${applicationId}`,
        {
        status:this.status
        },
        {
        headers:{
        Authorization:`Bearer ${this.token}`
        }
        })
        .then(res=>{
        alert("Status updated successfully")
        })
        .catch(err=>{
        this.error = err.response?.data?.message || "Failed to update status!"
        })

    },

    goBack(){
        this.$router.back()
    },

    formatDate(dateString){
        const date = new Date(dateString)
        return date.toLocaleDateString("en-IN",{
            day:"2-digit",
            month:"short",
            year:"numeric"
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
.details{
    margin-bottom: 15px;
}

.details-span{
    font-weight: bold;
    margin-right: 10px;
}

.btn {
    padding: 10px 20px;
    font-size: 16px;
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


.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}


.form-control {
    background-color: transparent;
    border: 1px solid #056805;
    /* width: 300px; */
    margin-left: 10px;
    color: rgba(255, 255, 255, 0.454);

}
.form-control:focus {
    background-color: black;
    border: 1px solid #056805;
    /* width: 350px; */
    /* margin-left: 20px; */
    color: rgba(255, 255, 255, 0.751);
    box-shadow: 0 0 0 0.25rem rgba(5, 104, 5, 0.25);
}
.details-action{
    width: 100%;
    height: 70px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.details-action .btn-outline-primary{
    margin: 0;
}

.mb3 .row{
    margin: 0;
}
.btn-resume{
    width: 300px;
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

.success{
  background-color: green;
  border-color: green;
}

.primary{
  background-color: blue;
  border-color: blue;
}
.warning{
  background-color: rgb(142, 142, 0);
  border-color: rgb(142, 142, 0);
}
.danger{
  background-color: red;
  border-color: red;
}
</style>

