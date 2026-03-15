
<template>

<div v-if="token">
<div class="canvas">

  <div class="lower-div">

    <!-- STUDENT APPLICATIONS -->

    <div class="card student-table glass-effect">
      <div class="header-card">
                <h4>Student Applications</h4>
          <div class="search-bar">
            <input type="text" placeholder="Search applications (student, job, id...)" class="search-input" v-model="applicationQuery" title="appId, student, job Title, Status" required/>
          </div>
        </div>

      <div class="table-responsive">
        <table class="table">

          <thead>
            <tr>
              <th>Id</th>
              <th>Student</th>
              <th>Job Title</th>
              <th>Applied On</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="filteredApplications.length === 0">
              <td colspan="6">No Applications Found</td>
            </tr>

            <tr v-for="app in filteredApplications" :key="app.id">
              <th scope="row">{{ app.id }}</th>
              <td>{{ app.student_name }}</td>
              <td>{{ app.drive_title }}</td>
              <td>{{formatDate( app.applied_on )}}</td>
              <td class="A" :class="statusBadge(app.status)">{{ app.status }}</td>

              <td class="btn-conatiner btn-action-container" >
                                  <button type="button" class="btn btn-outline-primary" title="View Application" @click="viewApplication(app.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                                      <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                                    </svg>
                                  </button>
                                  </td>
            </tr>

          </tbody>

        </table>
      </div>
    </div>


    <!-- ONGOING DRIVES -->

    <div class="card company-table glass-effect">
      <div class="header-card">
                <h4>Ongoing Drives</h4>
          <div class="search-bar">
            <input type="text" placeholder="Search drives (company, job, code...)" class="search-input" v-model="driveQuery" title="DriveId, Company, Job Title" required/>
          </div>
        </div>

      <div class="table-responsive">
        <table class="table">

          <thead>
            <tr>
              <th>ID</th>

              <th>Job Title</th>
              <th>Company</th>
              <th>Deadline</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr v-if="filteredDrives.length === 0">
              <td colspan="6">No Ongoing Drives</td>
            </tr>

            <tr v-for="drive in filteredDrives" :key="drive.id">
              <th scope="row">{{ drive.id }}</th>

              <td>{{ drive.job_title }}</td>
              <td>{{ drive.company_name }}</td>
              <td style="color: red;">{{formatDate( drive.deadline )}}</td>
        <td class="btn-conatiner btn-action-container">
          <button type="button" class="btn btn-success" title="Mark as Complete" @click="closeDrive(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-check" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                    </svg>
                                  </button>
                                  <button type="button" class="btn btn-outline-primary" title="View Application" @click="viewDrive(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                                      <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                                    </svg>
                                  </button>
        </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>

  </div>

</div>
</div>

<div v-else>
<h1>Please Login</h1>
</div>

</template>
<script>
import axios from "axios"

export default {
  data(){
    return{
      token:"",

      applications:[],
      drives:[],

      applicationQuery:"",
      driveQuery:""
    }
  },

  mounted(){
    this.loadToken()
    this.fetchAdminOverview()
  },
  computed:{
    filteredApplications(){

      if(!this.applicationQuery){
        return this.applications
      }

      const searchQuery = this.applicationQuery.toLowerCase()

      return this.applications.filter(app =>
        String(app.id).includes(searchQuery) ||
        app.student_name.toLowerCase().includes(searchQuery) ||
        app.drive_title.toLowerCase().includes(searchQuery) ||
        app.status.toLowerCase().includes(searchQuery)
      )
    },

    filteredDrives(){

      if(!this.driveQuery){
        return this.drives
      }

      const searchQuery = this.driveQuery.toLowerCase()

      return this.drives.filter(drive =>
        String(drive.id).includes(searchQuery) ||
        drive.drive_code.toLowerCase().includes(searchQuery) ||
        drive.job_title.toLowerCase().includes(searchQuery) ||
        drive.company_name.toLowerCase().includes(searchQuery)
      )
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
    statusBadge(status){
            if(status === "applied"){
                return "primary"
            }
            if(status === "shortlisted"){
                return "warning"
            }
            if(status === "selected"){
                return "success"
            }   
            if(status === "rejected"){
                return "danger"
            }
    },
    fetchAdminOverview(){

  axios.get("http://127.0.0.1:5000/api/admin/drives",{
  headers:{
  Authorization:`Bearer ${this.token}`
  }
  })
  .then(res=>{

  this.applications = res.data.applications
  this.drives = res.data.drives
  console.log(res.data)

  })
  .catch(err=>{
  console.log(err.response || err.message)
  })

    },
    closeDrive(driveId){

    if(!confirm("Close this drive?")){
    return
    }

    axios.post(`http://127.0.0.1:5000/api/admin/drive/close/${driveId}`,{},{
    headers:{
    Authorization:`Bearer ${this.token}`
    }
    })
    .then(res=>{

    alert(res.data.message)

    this.fetchAdminOverview()

    })
    .catch(err=>{
    alert(err.response?.data?.message || "Failed to close drive")
    })

    },
    viewApplication(applicationId){
    this.$router.push(`/company/application/${applicationId}`)
    },
    viewDrive(driveId){
        this.$router.push(`/company/drive/${driveId}`)
      },
    formatDate(date) {
  return new Date(date).toLocaleString("en-IN",{
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit"
})
    },
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
  padding-top: 25px;
}

.upper-div {
  /* flex: 1; */
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
  /* max-height: 45vh; */
    /* overflow-y: auto; */
}
.request-table {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  display: flex;
    flex-direction: column;
  align-items: center;
  padding: 15px 30px;
  /* min-height: 30vh;
  max-height: 100%; */
}
.table-responsive {
  min-width: 100%;
  min-height: 150px;
  max-height: 250px;
  overflow-y: auto;
}

.lower-div .table-responsive{
    max-height: 350px;
}

/* .table-responsive table {         
  overflow-y: auto;           
  margin-top: 12px;           
  width: 100%;
} */

.table-responsive th, .table-responsive td {
  color: #fff;
}

.lower-div {
    flex: 1;
  display: flex;
  gap: 24px;
  padding: 0 24px 24px;
  align-items: flex-start;
}

.card {
  flex: 1;
  min-height: 500px;
  background: rgba(255,255,255,0.06);
  border-radius: 16px;
  display: flex;
  align-items: center;
  padding: 15px;
  flex-direction: column;
  min-height: 0;
}
/* .lower-div .card h1 {
  margin-top: 0;
  font-size: 4rem;
  color: #fff;
} */
.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.btn-success:hover{
    color: black;
    background-color: #037e03d4;
}

.btn-success{
    background-color: transparent;
    color: #008000;
    border: 1px solid #008000;
    margin-right:10px ;
    /* padding: 6px; */
}
.btn-outline-primary:hover{
    color: #000;

}
th,td{
  vertical-align: middle;
  text-align: center;
}
td.success{
  /* background-color: green; */
  color: green;
  font-weight: 700;
}

td.primary{
  /* background-color: blue; */
  color: blue;
  font-weight: 700;
}
td.warning{
  /* background-color: yellow; */
  color: yellow;
  font-weight: 700;
}
td.danger{
  /* background-color: red; */
  color: red;
  font-weight: 700;
}


.search-bar{
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input{
  flex: 1;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.15);
  padding: 7px 12px;
  border-radius: 8px;
  color: white;
}

.search-input::placeholder{
  color: rgba(255,255,255,0.5);
}

.search-input:focus{
  outline: none;
  border-color: #008000;
}



.header-card{
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
</style>