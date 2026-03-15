<template>
<div v-if="token">
 <div class="canvas">
    <div class="main-container glass-effect">
        <div class="heading">
            <h4 v-if="isEdit">Edit Drive Details</h4>
            <h4 v-else>Enter Drive Details</h4>
        </div>

        <form class="form-holder" @submit.prevent="handleSubmit">
            <div class="mb-3 row">
                <label for="job_title" class="col-sm-2 col-form-label white-text">Job Title</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="job_title" placeholder="Enter Job Title" v-model="FormData.job_title">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="job_description" class="col-sm-2 col-form-label white-text">Job Description</label>
                <div class="col-sm-10">
                    <textarea type="textarea" class="form-control" id="job_description" placeholder="Job Description" v-model="FormData.job_description"></textarea> 
                </div>
            </div>
            <div class="mb-3 row">
                <label for="salary" class="col-sm-2 col-form-label white-text">Salary</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="salary" v-model="FormData.salary">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="eligibility_cgpa" class="col-sm-2 col-form-label white-text">Eligible Cgpa</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="eligibility_cgpa" v-model="FormData.eligibility_cgpa">
                </div>
            </div>
                <div class="mb-3 row">
                    <label for="eligibility_dept" class="col-sm-2 col-form-label white-text">Eligible Department</label>
                    <div class="col-sm-10">
                        <input class="form-control" list="datalistOptions" id="eligibility_dept" placeholder="Search and Select" v-model="FormData.eligibility_dept">
                        <datalist id="datalistOptions">
                            <option value="Computer Science"></option>
                            <option value="Data Science"></option>
                            <option value="Information Technology"></option>
                            <option value="Electronics and Communication"></option>
                            <option value="Mechanical Engineering"></option>
                        </datalist>
                    </div>
                </div>
                            <div class="mb-3 row">
                <label for="deadline" class="col-sm-2 col-form-label white-text">Deadline</label>
                <div class="col-sm-10">
                    <input type="date" class="form-control" id="deadline" v-model="FormData.deadline">
                </div>
            </div>

            <div class="btn-container"> 
                <p class="alert alert-danger" v-if="error">{{ error }}</p>
                <p class="alert  alert-success" v-if="success">{{ success }}</p>
            <button class="btn btn-primary-green btn-login" v-if="isEdit">Update Drive</button>
            <button class="btn btn-primary-green btn-login" v-else>Create Drive</button>
            </div>

        </form>

    </div>
</div>
 </div>
 <div v-else>
    <h1>Token Expired X Please Login to continue!</h1>
 </div>
</template>

<script>
import axios from "axios"

export default {

    name:"CreateDrivePage",

    data(){
        return{
            token:"",
            success:"",
            error:"",

            isEdit:false,
            driveId:null,

            FormData:{
                job_title:"",
                job_description:"",
                salary:"",
                eligibility_cgpa:"",
                eligibility_dept:"",
                deadline:""
            }
        }
    },

mounted(){
    this.loadToken()

// check if editing
    if(this.$route.params.driveId){
        this.isEdit = true
        this.driveId = this.$route.params.driveId
        this.fetchDrive()
    }
    },

    methods:{
        loadToken(){
            const token = localStorage.getItem("token")
            if(token){
                this.token = token
            }else{
                this.$router.push("/login")
            }
        },
        fetchDrive(){
            axios.get(`http://127.0.0.1:5000/api/company/drive/${this.driveId}`,{
            headers:{
                Authorization:`Bearer ${this.token}`
            }
            })
            .then(res=>{
                this.FormData = res.data.drive
            })
            .catch(err=>{
                this.error = err.response?.data?.message || "Failed to load drive"
            })

},
        handleSubmit(){
            this.error = ""
            this.success = ""
            if(this.isEdit){
                this.updateDrive()
            }else{
                this.createDrive()
            }
        },

        createDrive(){
            axios.post("http://127.0.0.1:5000/api/company/create-drive",this.FormData,{
                headers:{
                    Authorization:`Bearer ${this.token}`
                }
            })
            .then(res=>{
                this.success = res.data.message
                setTimeout(()=>{
                    this.$router.push("/auth/dashboard")
                },1500)
            })
            .catch(err=>{
                this.error = err.response?.data?.message || "Drive creation failed"
            })
        },

        updateDrive(){
            axios.put(`http://127.0.0.1:5000/api/company/update-drive/${this.driveId}`,this.FormData,{
                headers:{
                    Authorization:`Bearer ${this.token}`
                }
            })
            .then(res=>{
                this.success = res.data.message
                setTimeout(()=>{
                    this.$router.push("/auth/dashboard")
                },1500)                
            })
            .catch(err=>{
                this.error = err.response?.data?.message || "Drive update failed"
            })
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
</style>