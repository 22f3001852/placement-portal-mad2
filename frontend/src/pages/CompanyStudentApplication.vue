<template>
    <div v-if="token">
    <div class="canvas">

        <div class="upper-div">
            <div class="request-table glass-effect">
            <div class="header-card">
                <div>
                <h3>Student Applications</h3>
                <h5>Job Title: {{ job_title }}</h5>
                </div>
                
                <div class="search-bar">
                    <input type="text" placeholder="Search applications (name, id...)" class="search-input" v-model="applicationQuery" title="name, id" required/>
                </div>
            </div>

                <div class="table-responsive table-card">
                    <table class="table table-bordered">
                        <tbody>
                            <tr v-if="filteredApplications.length > 0" v-for="each_application in filteredApplications" :key="each_application.application_id">
                                <th class="left-border" scope="row">{{ each_application.student_id }}</th>
                                <td class="boder-none"> {{ each_application.student_name }} </td>

                                <td class="boder-none applied-color" v-if="each_application.status === 'applied'">
                                    {{ each_application.status }}</td>
                                <td class="boder-none shortlisted-color" v-else-if="each_application.status === 'shortlisted'">{{ each_application.status }}</td>
                                <td class="boder-none selected-color" v-else-if="each_application.status === 'selected'">{{ each_application.status }}</td>
                                <td class="boder-none rejected-color" v-else-if="each_application.status === 'rejected'">{{ each_application.status }}</td>
                                <!-- <td class="boder-none " :class="statusBadge"> {{ each_application.status }} </td> -->
                                <td class="right-border">
                                <button class="btn btn-outline-success"@click="reviewApplication(each_application.application_id)">
                                Review Application
                                </button>
                                </td>
                            </tr>
                            <tr v-else>
                                <td colspan="2" class="text-center">
                                        No One Applied Yet!
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
import axios from 'axios'

export default {
    data(){
        return{
            token:"",
            applications:[],
            job_title:"",

            applicationQuery:""
        }
    },

    mounted(){
        this.token = localStorage.getItem("token")
        this.viewStudent()
    },
    computed:{

filteredApplications(){

if(!this.applicationQuery){
return this.applications
}

const searchQuery = this.applicationQuery.toLowerCase()

return this.applications.filter(app =>
String(app.student_id).includes(searchQuery) ||
app.student_name.toLowerCase().includes(searchQuery) ||
String(app.application_id).includes(searchQuery) ||
app.status.toLowerCase().includes(searchQuery)
)

}

},
    methods:{
        
        viewStudent(){
            const driveId = this.$route.params.driveId
            axios.get(`http://127.0.0.1:5000/api/company/view/applications/${driveId}`,{
            headers:{
            Authorization:`Bearer ${this.token}`
            }
            })
            .then(res=>{
            console.log(res.data)
            this.applications = res.data.applications
            this.job_title = res.data.job_title
            })
            .catch(err=>{
            console.log(err.response || err.message)
            })

            },
            reviewApplication(application_id){
                this.$router.push(`/company/application/${application_id}`)
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
  padding: 24px;
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
    /* border-right: none; */
    border-left: 1px solid rgba(255, 255, 255, 0.3);
    vertical-align: middle;
}
.table-card .table tbody td{
    text-align: right;
    padding: 7px !important;
    vertical-align: middle;
    font-weight: 700;
}
.table-card .table tbody td,
.table-card .table tbody th {
    border-top: 1px solid rgba(255, 255, 255, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.left-border{
    border-right: none;
}
.right-border{
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    border-left: none;
} 
 .boder-none{
    border-left: none;
    border-right: none;
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
.table-bordered .applied-color{
    color: blue;
}
.table-bordered .shortlisted-color{
    color: yellow;
}
.table-bordered .selected-color{
    color: green;
}
.table-bordered .rejected-color{
    color: red;
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