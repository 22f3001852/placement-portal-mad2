<template>
  <!-- if user has token -->
  <div v-if="token">
    <!-- ADMIN DASHBOARD -->
    <div class="admin-dashboard canvas" v-if="role === 'admin'">
      <div class="upper-div">
        <div class="bar-chart glass-effect">
          <canvas ref="barChart"></canvas>
        </div>
        <div class="donut-chart glass-effect">
          <canvas ref="donutChart"></canvas>
        </div>
      </div>
      <div class="lower-div">
        <div class="card glass-effect">
          <h2>Total Ongoing Drives</h2>
          <h1>{{ stats.active_drives }}</h1>
        </div>
        <div class="card glass-effect">
          <h2>Total Students</h2>
          <h1>{{ stats.students }}</h1>  
        </div>
        <div class="card glass-effect">
          <h2>Average Package</h2>
          <h1>{{ stats.average_package.toFixed(2) }} LPA</h1>
        </div>
      </div>
    </div>

    <!-- COMPANY DASHBOARD -->
    <div class="company-dashboard canvas" v-else-if="role === 'company'">
          <div class="upper-div">
              <div class="request-table glass-effect">
                  <div class="add_btn">
                      <h1>Ongoing Drives</h1>
                      <button type="button" class="btn btn-add btn-success" title="Create Drive" @click="goToCreatePage()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                      </svg>
                      </button>
                  </div>
                  
                  <div class="table-responsive">
                      <table class="table">
                          <thead>
                              <tr>
                              <th scope="col">Sr No.</th>
                              <th scope="col">Job title</th>
                              <th scope="col">Started On</th>
                              <th scope="col">DeadLine</th>
                              <th scope="col">Action</th>
                              </tr>
                          </thead>
                          <tbody>
                              <tr v-for="drive in ongoing_drives">
                              <th scope="row">{{ drive.drive_code }}</th>
                              <td>{{ drive.job_title }}</td>
                              <td>{{formatDate( drive.created_on )}}</td>
                              <td style="color: red;">{{formatDate( drive.deadline )}}</td>
                              <td class="btn-conatiner btn-action-container">
                                  <button type="button" class="btn btn-outline-primary" title="View Applications" @click="goToViewPage(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                                      <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                                    </svg>
                                  </button>
                                  <button type="button" class="btn btn-success" title="Mark as Complete" @click="closeDrive(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-check" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
                                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1z"/>
                                    </svg>
                                  </button>
                              </td>
                              </tr>

                          </tbody>
                      </table>
                  </div>
              </div>
          </div>
          <div class="upper-div">
              <div class="request-table glass-effect">
                  <h1>Closed Drives</h1>
                  <div class="table-responsive">
                      <table class="table">
                          <thead>
                              <tr>
                              <th scope="col">Sr No.</th>
                              <th scope="col">Job title</th>
                              <th scope="col">Created On</th>
                              <th scope="col">Finished On</th>
                              <th scope="col">Action</th>
                              </tr>
                          </thead>
                          <tbody>
                              <tr v-for="drive in closed_drives">
                              <th scope="row">{{ drive.drive_code }}</th>
                              <td>{{ drive.job_title }}</td>
                              <td>{{formatDate( drive.created_on )}}</td>
                              <td style="color: red;">{{formatDate( drive.deadline )}}</td>
                              <td class="btn-conatiner btn-action-container">
                                <button type="button" class="btn btn-outline-primary" title="View Applications" @click="goToViewPage(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
                                    <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                                      <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                                    </svg>
                                  </button>
                                  <button type="button" class="btn btn-outline-warning btn-update" title="Update" @click="goToUpdatePage(drive.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
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
    
    <!-- STUDNET DASHBOARD -->
    <div class="student-dashboard canvas" v-else-if="role === 'student'">

        <div class="upper-div">
            <div class="request-table glass-effect">
              <div class="header-card">
            <h4>Organizations</h4>
            <div class="search-bar">
            <input type="text" placeholder="Search org (job title, id...)" class="search-input" v-model="organizationQuery" required/>
          </div>
        </div>
                <!-- <h3>Organizations</h3><br> -->
                <!-- <h5>Job Title: Data Analyst</h5><br> -->
                <div class="table-responsive table-card">
                    <table class="table table-bordered">
                        <tbody>
                            <tr v-for="org in filteredOrganizations" :key="org.id">
                              <th scope="row">{{ org.name }}</th>
                            <td>
                                <button type="button" class="btn btn-outline-success" @click="viewCompanyDrives(org.id)" title="View Company Drives">
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
        <div class="upper-div">
            <div class="request-table glass-effect">

                    <h3>Applied Drives</h3>

                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Job Title</th>
                            <th scope="col">Company name</th>
                            <th scope="col">Applied On</th>
                            <th scope="col">Status</th>
                            <th scope="col">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="drive in applied_drives" :key="drive.id">
                            <th scope="row">{{ drive.id }}</th>
                            <td>{{ drive.job_title }}</td>
                            <td>{{ drive.company_name }}</td>
                            <td>{{ formatDate(drive.applied_on) }}</td>
                            <td class="A" :class="statusBadge( drive.status )">{{  drive.status  }}</td>
                            <td>
                                <button type="button" class="btn btn-outline-success" @click="viewDrive(drive.id)">
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
    <h1>Please Login!</h1>
  </div>

</template>

<script>
import axios from 'axios';
import {
  Chart,
  ArcElement,
  BarElement,
  BarController,
  DoughnutController,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale
} from 'chart.js'

Chart.register(
  ArcElement,
  BarElement,
  BarController,
  DoughnutController,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale
)

export default {
  name: "DashboardPage",

  data() {
    return {
      token: "",
      role:"",

      // admin data
      stats: {
        students: 0,
        companies: 0,
        active_drives: 0,
        average_package: 0
      },
      charts: {
        labels: [],
        applied: [],
        shortlisted: [],
        approved_company: 0,
        pending_company: 0        
      },
      barChartInstance: null,
      donutChartInstance: null,
      
      // company data
      ongoing_drives:[],
      closed_drives:[],
      company:[],

      // student data
      organizations: [],
      applied_drives: [],
      organizationQuery:""

    }
  },

  mounted() {
    this.loadToken();
    this.loadUser();

    if (this.role === 'admin'){
      this.fetchAdminDashboard()
    }else if(this.role === 'company'){
      this.fetchCompanyDashboard()
    } else if (this.role === "student") {
    this.fetchStudentDashboard()
  }
  },
  computed:{
    filteredOrganizations(){
      if(!this.organizationQuery){
        return this.organizations
      }

      const searchQuery = this.organizationQuery.toLowerCase()

      return this.organizations.filter(org =>
        String(org.id).includes(searchQuery) ||
        org.name.toLowerCase().includes(searchQuery)
        )

      }
  },

  methods: {
    loadToken(){
        const token = localStorage.getItem("token")
        if(token){
            this.token = token
        }else{
            this.$router.push("/login")
        }
    },
    loadUser(){
      const role = localStorage.getItem("role")
      if(role){
        this.role = role;
      }
      const response = axios.get(`http://127.0.0.1:5000/api/auth/dashboard`,{
                headers: {
                "Content-Type":"application/json",
                "Authorization": `Bearer ${this.token}`
                }
            })
            response
            .then(res => {
                    console.log(res)
            }).catch(
                err => 
                // this.error = err.response.data)
                 console.log(err.response))
    },

    // admin methods 
    fetchAdminDashboard() {
      const response = axios.get("http://127.0.0.1:5000/api/auth/dashboard", {
                  headers: {
                    Authorization: `Bearer ${this.token}`
                  }
      })
      response
      .then(res => {
        this.stats = res.data.stats;

        this.charts.labels = res.data.charts.labels;
        this.charts.applied = res.data.charts.applied_data;
        this.charts.shortlisted = res.data.charts.shortlisted_data;
        this.charts.approved_company = res.data.charts.approved_company;
        this.charts.pending_company = res.data.charts.pending_company;

        this.$nextTick(() => {
          this.createCharts();
        });
      })
      .catch(err => {
        console.log(err.response || err.message);
      });
    },
    createCharts() {
        const barEl = this.$refs.barChart
        const donutEl = this.$refs.donutChart

        if (this.barChartInstance) {
          this.barChartInstance.destroy()
        }
        if (this.donutChartInstance) {
          this.donutChartInstance.destroy()
        }
        
        // Bar Chart
        new Chart(barEl.getContext('2d'), {
          type: 'bar',
          data: {
            labels: this.charts.labels,
            datasets: [{
              label: 'Applied',
              data: this.charts.applied,
              backgroundColor: 'rgba(255, 99, 132, 0.3)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1,
              borderRadius: 5
            },
            {
              label: 'Shortlisted',
              data: this.charts.shortlisted,
              backgroundColor: 'rgba(75, 192, 192, 0.3)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              borderRadius: 5
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,

          plugins: {
            legend: {
              labels: { color: 'white' }
            },
            tooltip: {
              callbacks: {
                footer: (items) => {
                  const total = items.reduce((sum, item) => sum + item.raw, 0)
                  return `Total: ${total}`
                }
              }
            }
          },

          scales: {
            x: {
              stacked: true,
              ticks: { color: 'white' },
            },
            y: {
              stacked: true,
              ticks: { color: 'white' },
              grid: { color: 'rgba(255,255,255,0.1)' }
            }
          }
        }
        })

        // Donut Chart
        new Chart(donutEl.getContext('2d'), {
          type: 'doughnut',
          data: {
            labels: [
              'Requested for approval', 
              'Approved Companies'
            ],
            datasets: [{
              label: 'Dataset',
              data: [
                this.charts.pending_company, 
                this.charts.approved_company
              ],
              backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)'
              ],
              hoverOffset: 4,
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: "#fff" } }
            }
          }
        })
    },

    // company methods 
    fetchCompanyDashboard(){
      const response = axios.get("http://127.0.0.1:5000/api/auth/dashboard", {
                  headers: {
                    Authorization: `Bearer ${this.token}`
                  }
      })
      response
      .then(res => {
        console.log("Company Dashboard:", res.data);
        this.ongoing_drives = res.data.drives.ongoing
        this.closed_drives = res.data.drives.closed

        this.company = res.data.company
      })
      .catch(err => 
        console.log(err.response || err.message)
      )
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
    goToCreatePage(){
      this.$router.push(`/company/create-drive`)
    },
    closeDrive(driveId){
      axios.post(`http://127.0.0.1:5000/api/company/close-drive/${driveId}`, {}, {
        headers:{
          Authorization: `Bearer ${this.token}`
        }
      })
      .then(res=>{
        alert(res.data.message)

        this.ongoing_drives = this.ongoing_drives.filter(d => d.id !== driveId)

        this.fetchCompanyDashboard()
      })
      .catch(err=>{
        console.log(err.response || err.message)
      })
    },
    goToViewPage(driveId){
      this.$router.push(`/company/view/applications/${driveId}`)
    },
    goToUpdatePage(driveId){
      this.$router.push(`/company/update-drive/${driveId}`)
    },

    // student methods 
    fetchStudentDashboard(){
      axios.get("http://127.0.0.1:5000/api/auth/dashboard",{
        headers:{
          Authorization:`Bearer ${this.token}`
        }
      })
      .then(res=>{
        console.log("Student Dashboard:",res.data)

        this.organizations = res.data.organizations
        this.applied_drives = res.data.applied_drives
      })
      .catch(err=>{
        console.log(err.response || err.message)
      })
    },
    applyDrive(driveId){

      axios.post(`http://127.0.0.1:5000/api/student/apply/${driveId}`,{},{
        headers:{
          Authorization:`Bearer ${this.token}`
        }
      })

      .then(res=>{
        alert(res.data.message)
        this.fetchStudentDashboard()
      })

      .catch(err=>{
        console.log(err.response || err.message)
      })
    },
    viewDrive(driveId){
      this.$router.push(`/company/drive/${driveId}`)
    },
    viewCompanyDrives(companyId){
      this.$router.push(`/student/company-drives/${companyId}`)
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
  }
}
</script>

<style scoped>
.admin-dashboard.canvas {
  width: 100%;
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.admin-dashboard .upper-div {
  flex: 1;
  display: flex;
  gap: 24px;
  padding: 24px;
  min-height: 420px;
}

.admin-dashboard .lower-div {
  display: flex;
  gap: 24px;
  padding: 0 24px 24px;
}

.admin-dashboard .bar-chart,
.admin-dashboard .donut-chart {
  position: relative;
  /* flex: 1; */
  min-height: 340px;
  min-width: 0;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  /* overflow: hidden; */
  padding: 10px;
}

.admin-dashboard .bar-chart{
  width: 65%;
}

.admin-dashboard .donut-chart {
  width: 30%;
}

.admin-dashboard .donut-chart canvas{
  width: 90% !important;
  height: 95% !important;
}
.admin-dashboard .bar-chart canvas,
.admin-dashboard .donut-chart canvas {
  position: absolute !important;
  /* inset: 0 !important; */
  /* width: 90% !important; */
  /* height: 90% !important; */
  display: block;
}

.admin-dashboard .card {
  flex: 1;
  min-height: 180px;
  background: rgba(255,255,255,0.06);
  border-radius: 16px;
  display: flex;
  align-items: center;
  padding: 15px;
  flex-direction: column;
}
.admin-dashboard .lower-div .card h1 {
  margin-top: 0;
  font-size: 4rem;
  color: #fff;
}
.admin-dashboard .glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}


/* company styles */
.company-dashboard.canvas {
  width: 100%;
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.company-dashboard .upper-div {
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
}

.company-dashboard .request-table {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  display: flex;
    flex-direction: column;
  align-items: center;
  padding: 15px 30px;
}

.company-dashboard .table-responsive {
  min-width: 100%;
  min-height: 150px;
  max-height: 250px;
  overflow-y: auto;
}

.company-dashboard .table-responsive th, .company-dashboard .table-responsive td {
  color: #fff;
}

.company-dashboard .glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.company-dashboard .add_btn{
    /* border: 1px solid red; */
    display: flex;
    width: 100%;
    justify-content: space-between;
    margin-bottom: 10px;
}
.company-dashboard .btn-add{
    height: 40px;
    width: 40px;
    border-radius: 7px;
}
.company-dashboard .btn-success{
    background-color: #008000;
    color: #000;
    border: 1px solid #008000;
    margin-left:15px ;
    /* padding: 6px; */
}

.company-dashboard .btn-success:hover{
    color: #000;
    background-color: #037e03d4;
}

.company-dashboard .btn-outline-primary:hover{
    color: #000;
    /* background-color: ; */
}


.company-dashboard .table thead th{
    text-align: center;
}
.company-dashboard .table tbody td{
    text-align: center;
}
.company-dashboard .table tbody td,
.company-dashboard .table tbody th {
    /* border-to: 1px solid rgba(255, 255, 255, 0.3); */
    text-align: center;
    vertical-align: middle;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.company-dashboard .btn-conatiner{
    /* border:1px solid red; */
    width: 40%;
}
.company-dashboard .btn-conatiner.btn-action-container{
  width: 20%;
}
.company-dashboard .btn-update{
  margin-left: 15px;
}
.company-dashboard .btn-update:hover{
  color: black;
  border-color: 1px solid yellow;
  
}
.student-dashboard.canvas {
  width: 100%;
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.student-dashboard .upper-div {
  display: flex;
  gap: 24px;
  padding: 24px;
  align-items: flex-start;
}

.student-dashboard .request-table {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  display: flex;
    flex-direction: column;
  align-items: center;
  padding: 15px 30px;
}

.student-dashboard .table-responsive {
  min-width: 100%;
  min-height: 150px;
  max-height: 250px;
  overflow-y: auto;
}

.student-dashboard .table-responsive th, .table-responsive td {
  color: #fff;
}

.student-dashboard .glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.student-dashboard .add_btn{
    /* border: 1px solid red; */
    display: flex;
    width: 100%;
    justify-content: space-between;
    margin-bottom: 10px;
}
.student-dashboard .btn-success{
    background-color: #008000;
    height: 40px;
    width: 40px;
    border-radius: 10px;
    /* font-size: 2rem; */
    /* padding: 0px 0px 20px 0px; */
    /* align-items: center; */
}


.student-dashboard .table thead th{
    vertical-align: middle;
    text-align: center;   
}

.student-dashboard .table tbody td,
.student-dashboard .table tbody th {
    vertical-align: middle;
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}


.student-dashboard .table-card .table {
  border-collapse: separate !important;
  border-spacing: 0 6px;
}

.student-dashboard .table-card .table tbody tr {
  background: rgba(255,255,255,0.05);
}

.student-dashboard .table-card .table tbody th{
    border-right: none;
    border-left: 1px solid rgba(255, 255, 255, 0.3);
    vertical-align: middle;
}
.student-dashboard .table-card .table tbody td{
    border-left: none;
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    text-align: right;
    padding: 7px !important;
}
.student-dashboard .table-card .table tbody td,
.student-dashboard .table-card .table tbody th {
    border-top: 1px solid rgba(255, 255, 255, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.student-dashboard .btn-outline-success{
    color: #008000;
    border: 1px solid #008000;
    /* height: 35px; */
}

.student-dashboard .btn-outline-success:hover{
    color: #000;
    background-color: #008000;
}

.student-dashboard td.success{
  /* background-color: green; */
  color: green;
  font-weight: 700;
}

.student-dashboard td.primary{
  /* background-color: blue; */
  color: blue;
  font-weight: 700;
}
.student-dashboard td.warning{
  /* background-color: yellow; */
  color: yellow;
  font-weight: 700;
}
.student-dashboard td.danger{
  /* background-color: red; */
  color: red;
  font-weight: 700;
}

.student-dashboard .search-bar{
  display: flex;
  align-items: center;
  gap: 10px;
}

.student-dashboard .search-input{
  flex: 1;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.15);
  padding: 7px 12px;
  border-radius: 8px;
  color: white;
}

.student-dashboard .search-input::placeholder{
  color: rgba(255,255,255,0.5);
}

.student-dashboard .search-input:focus{
  outline: none;
  border-color: #008000;
}

.student-dashboard .header-card{
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
</style>