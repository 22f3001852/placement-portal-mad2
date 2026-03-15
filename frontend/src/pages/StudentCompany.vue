<template>
    <div class="canvas">
        <div class="upper-div">
       
          <!-- <div class="request-table glass-effect Ucard" >
              <h5>Company Name: {{ company_name }}</h5>
          </div> -->
        </div>
        <div class="upper-div">
            <div class="request-table glass-effect">
                 <div class="header-card">
            <h4>Current Drives</h4>
            <div class="search-bar">
            <input type="text" placeholder="Search drives (job title, id...)" class="search-input" v-model="driveQuery" required/>
          </div>
        </div><br>

                <div class="table-responsive table-card">
                    <table class="table table-bordered">
                        <tbody>
                            <tr v-for="drive in filteredDrives" :key="drive.id">
                                <th scope="row">{{ drive.job_title }}</th>
                            <td>
                                <button type="button" class="btn btn-outline-success" @click="goToDriveDetails(drive.id)">View Details</button>
                            </td>
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

name:"StudentCompanyDrives",

data(){
return{

token:"",
companyId:null,

company_name:"",
drives:[],

driveQuery:""

}
},

mounted(){

this.token = localStorage.getItem("token")

this.companyId = this.$route.params.companyId

this.fetchCompanyDrives()

},
computed:{

filteredDrives(){

if(!this.driveQuery){
return this.drives
}

const searchQuery = this.driveQuery.toLowerCase()

return this.drives.filter(drive =>
String(drive.id).includes(searchQuery) ||
drive.job_title.toLowerCase().includes(searchQuery)
)

}

},

methods:{

fetchCompanyDrives(){

axios.get(`http://127.0.0.1:5000/api/student/company-drives/${this.companyId}`,{

headers:{
Authorization:`Bearer ${this.token}`
}

})

.then(res=>{

console.log(res.data)

this.company_name = res.data.company_name
this.drives = res.data.drives

})

.catch(err=>{

console.log(err.response || err.message)

})

},

goToDriveDetails(driveId){

this.$router.push(`/company/drive/${driveId}`)

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
  align-items: center;
}

.upper-div {
  display: flex;
  gap: 24px;
  padding: 20px 0px 0px 0px;
  align-items: flex-start;
  width: 90%;
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
  /* max-height: 250px; */
  /* overflow-y: auto; */
}

.table-responsive th, .table-responsive td {
  color: #fff;
}

.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}

.table-card .table {
  border-collapse: separate !important;
  border-spacing: 0 6px;
}

.table-card .table tbody tr {
  background: rgba(255,255,255,0.05);
}

.table-card .table tbody th{
    border-right: none;
    border-left: 1px solid rgba(255, 255, 255, 0.3);
    vertical-align: middle;
}
.table-card .table tbody td{
    border-left: none;
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    text-align: right;
    padding: 7px !important;
}
.table-card .table tbody td,
.table-card .table tbody th {
    border-top: 1px solid rgba(255, 255, 255, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-outline-success{
    color: #008000;
    border: 1px solid #008000;
    /* height: 35px; */
}

.btn-outline-success:hover{
    color: #000;
    background-color: #008000;
}

.Ucard{
    align-items: start;
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