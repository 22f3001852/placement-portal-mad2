<template>
    <div class="canvas">
        <div class="upper-div">
          <div class="request-table glass-effect Ucard" >
            <div>              
              <h5>Studnet Name: {{ student.name }}</h5>
              <h5>Department: {{ student.department }}</h5>
            </div>

              <div class="btn-dwn-div">
                <h6>Download Application History</h6>
                <button class="btn-download" title="Download CSV" @click="downloadCSV">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
                  </svg>
                </button>
              </div>

          </div>
        </div>
        <div class="upper-div">
            <div class="request-table glass-effect">
                <h3>Application History</h3>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">Drive ID</th>
                            <th scope="col">Company</th>
                            <th scope="col">Job Title</th>
                            <th scope="col">Salary</th>
                            <th scope="col">Result</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="applications.length === 0">
                              <td colspan="5">No applications yet</td>
                            </tr>
                            <tr v-for="app in applications" :key="app.drive_id">
                            <th scope="row">{{ app.drive_id }}</th>
                            <td>{{ app.company_name }}</td>
                            <td>{{ app.job_title }}</td>
                            <td>{{ app.salary }} LPA</td>
                            <td class="A" :class="statusBadge(app.status)">{{ app.status }}</td>
                            
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios"

export default{

data(){
return{
token:"",

student:{},
applications:[]
}
},

mounted(){
this.loadToken()
this.fetchHistory()
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
fetchHistory(){

axios.get("http://127.0.0.1:5000/api/student/history",{
headers:{
Authorization:`Bearer ${this.token}`
}
})

.then(res=>{

this.student = res.data.student
this.applications = res.data.applications

})

.catch(err=>{
console.log(err.response || err.message)
})

},
downloadCSV(){

axios.get(`http://127.0.0.1:5000/api/student/export_csv/${this.student.id}`,{
headers:{
Authorization:`Bearer ${this.token}`
}
})

.then(res=>{

const task_id = res.data.task_id

// wait 3 seconds for celery to generate file
setTimeout(()=>{

window.open(`http://127.0.0.1:5000/api/student/csv_result/${task_id}`)

},3000)

})

.catch(err=>{
console.log(err)
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
  gap: 24px;
  padding: 20px 24px 0px 24px;
  align-items: flex-start;
}

.request-table {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border-radius: 15px;
  display: flex;
    flex-direction: column;
  align-items: center;
  padding: 15px 30px;
}

.table-responsive {
  min-width: 100%;
  min-height: 150px;
  max-height: 500px;
  overflow-y: auto;
}

.table-responsive th, .table-responsive td {
  color: #fff;
}

.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.Ucard{
  display: flex;
  align-items: start;
  flex-direction: row;
  justify-content: space-between;
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

th,td{
  vertical-align: middle;
  text-align: center;
}

.btn-download{
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
  height: 40px;
  width: 40px;
  padding: 0;
  margin-left: 10px;
  display: flex;
  align-items: center;
  justify-content: center;

  color: #fdf000;     
  border: 1px solid rgba(192, 190, 54, 0.313);

  transition: all 0.25s ease;
}

.btn-download:hover{
  background: rgba(255, 216, 77, 0.15);
  border-color: #fdf000;
  color: #ffe66b;
  transform: scale(1.05);
}

.btn-dwn-div{
  display: flex;
  align-items: center;
}
</style>