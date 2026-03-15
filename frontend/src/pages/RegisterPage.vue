<template>
 <div class="canvas">
    <div class="main-container glass-effect">
        <div class="heading">
        <h4>Register your details</h4>
        </div>
        <form class="form-holder" @submit.prevent="register">
            <div class="mb-3 row">
                <label for="username" class="col-sm-2 col-form-label white-text">Email</label>
                <div class="col-sm-10">
                    <input type="email" class="form-control" id="username" placeholder="Enter your email" v-model="FormData.username">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="fullname" class="col-sm-2 col-form-label white-text">Fullname</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="fullname" placeholder="Enter your fullname" v-model="FormData.fullname">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="inputPassword" class="col-sm-2 col-form-label white-text">Password</label>
                <div class="col-sm-10">
                    <input type="password" class="form-control" id="inputPassword" v-model="FormData.password">
                </div>
            </div>

            <!-- if role is student then only show department and resume upload option -->

            <div class="mb-3 row">
                <label for="role" class="col-sm-2 col-form-label white-text">Role</label>
                <div class="col-sm-10">
                <select class="form-select form-control" id="role" name="role" v-model="FormData.role">
                    <option value="student" selected>Student</option>
                    <option value="company">Company</option>
                </select>
                </div>
            </div>
            <div v-if=" FormData.role ==='student'">
                <div class="mb-3 row">
                    <label for="department" class="col-sm-2 col-form-label white-text">Department</label>
                    <div class="col-sm-10">
                        <input class="form-control" list="datalistOptions" id="department" placeholder="Type to search..." v-model="FormData.department">
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
                    <label for="cgpa" class="col-sm-2 col-form-label white-text">Current CGPA</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="cgpa" v-model="FormData.cgpa">
                    </div>
                </div>
                <div class="mb-3 row">
                    <label for="year" class="col-sm-2 col-form-label white-text">Current Year</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="year" v-model="FormData.year">
                    </div>
                </div>
                <div class="mb-3 row">
                    <label for="formFile" class="col-sm-2 col-form-label white-text">Resume</label>
                    <div class="col-sm-10">
                        <input class="form-control" type="file" id="formFile" placeholder="Upload Resume..." @change="uploadFile">
                    </div>
                </div>
            </div>
            <!-- else if role is company then only show company name, website and description option -->
            <div v-else>
            <div class="mb-3 row">
                <label for="companyName" class="col-sm-2 col-form-label white-text">Company Name</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="companyName" placeholder="Enter company name" v-model="FormData.companyName">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="hrContact" class="col-sm-2 col-form-label white-text">HR Contact</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="hrContact" placeholder="Enter HR contact email" v-model="FormData.hrContact">
                </div>
            </div>
            <div class="mb-3 row">
                <label for="website" class="col-sm-2 col-form-label white-text">Website</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="website" placeholder="Enter company website link" v-model="FormData.website">
            </div>
            </div>
            <div class="mb-3 row">
                <label for="location" class="col-sm-2 col-form-label white-text">Location</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="location" placeholder="Enter company location" v-model="FormData.location">
            </div>
            </div>
            </div>
            <p class="alert alert-danger" v-if="error">{{ error }}</p>
            <p class="alert  alert-success" v-if="success">{{ success }}</p>
            <div class="btn-container"> 
            <button class="btn btn-primary-green btn-login">Sign Up</button>
            <span class="white-text">Already have an account? </span><span @click="goToLogin" class="green-link">Login here</span>
            <!-- <button class="btn btn-secondary">Register</button> -->
            </div>
        </form>

    </div>
    <div class="image-conatiner">
    </div>
 </div>
</template>

<!-- <script>
export default {
    name: "RegisterPage",
    data() {
        return {
            role: 'student'
        }
    },
    
    methods:{
        goToLogin: function(){
            this.$router.push('/login')
        }
    }
}
</script> -->
<script>
import axios from "axios";

export default {
  name: "RegisterPage",

  data() {
    return {
        error: "",
        success: "",
        FormData:{
            username: "",
            fullname: "",
            password: "",
            role: "student",
            // Student fields
            department: "",
            cgpa: "",
            year: "",
            // resume: "",
            // Company fields
            companyName: "",
            hrContact: "",
            website: "",
            location: ""
        }
    };
  },
  
  methods: {
    goToLogin(){
        this.$router.push("/login");
    },
    uploadFile(event) {
      const file = event.target.files[0];
      if (file) {
        this.FormData.resume = file;
      }
    },

    register() {
        const formData = new FormData();

        formData.append("username", this.FormData.username);
        formData.append("fullname", this.FormData.fullname);
        formData.append("password", this.FormData.password);
        formData.append("role", this.FormData.role);

        if (this.FormData.role === "student") {
            formData.append("department", this.FormData.department);
            formData.append("cgpa", this.FormData.cgpa);
            formData.append("year", this.FormData.year);

            if (this.FormData.resume) {
            formData.append("resume", this.FormData.resume);
            }
        }
        else {
            
            formData.append("companyName", this.FormData.companyName);
            formData.append("hrContact", this.FormData.hrContact);
            formData.append("website", this.FormData.website);
            formData.append("location", this.FormData.location);
        }
        const response = axios.post("http://127.0.0.1:5000/api/auth/register", formData)
            response.then(res => {
                this.success = "Registration successful! Redirecting...";
                          
                setTimeout(() => {
                    this.goToLogin();
                }, 1500);

            }).catch(
                err => {
                    this.error = err.response?.data?.message || "Registration failed"
                }
            )
      }
    }
};

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
.image-conatiner {
    width: 40%;
    height: 88dvh;
    /* border: 1px solid red; */
    background-image: url('@/assets/images/registerPage.png');
    background-size: cover;
    /* background-position: center; */
    
}

.main-container {
    /* position: absolute; */
    /* top: 16%; */
    left: 55%;
    /* border: 1px solid yellow; */
    width: 550px;
    height: fit-content;
    min-height: 500px;
    display: flex;
    /* justify-content: center; */
    align-items: center;
    flex-direction: column;
    padding: 10px 20px 10px 15px;
    overflow-y: auto;
}
.heading {
    /* height: 100px; */
    margin-top: 10px;
}

.main-container h4 {
    color: white;
    margin: 0px 0px 0px 0px;
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
    margin-top: 0px;
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
/* .para {
    height: 200px;
    color: white;
    text-align: left;
    margin-top: 10px;
    padding-left: 5px;
} */

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
    width: 90%;
    height: 300px;
    /* border: 1px solid red; */
    display: flex;
    justify-content: space-between;
    flex-direction: column;
    margin-top: 30px;
}
/* .form-holder .mb-3 {
    margin: 0px 0px 0px 0px;
} */
.form-holder .form-control {
    background-color: transparent;
    border: 1px solid #056805;
    width: 320px;
    margin-left: 20px;
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

/* select.form-control {
    background-color: transparent;
    border: 1px solid #056805;
    width: 320px;
    margin-left: 20px;
    color: rgba(255, 255, 255, 0.454);
}
select.form-select:focus {
    background-color: transparent;
    border: 1px solid #056805;
    color: rgba(255, 255, 255, 0.751);
    box-shadow: 0 0 0 0.25rem rgba(5, 104, 5, 0.25);
} */
select.form-control option {
    background-color: white;
    color: black;
}

.green-link{
    color: #008000;
    font-weight: 700;
    cursor: pointer;
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

.alert.alert-success{
    height: 40px;
    padding: 5px;
    margin: 0;
    color: #056805;
    background-color: transparent;
    border-color: #054d05;
    margin-top: 10px;

}
</style>