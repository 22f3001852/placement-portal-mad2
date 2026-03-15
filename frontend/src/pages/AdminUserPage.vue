<template>
  <div class="canvas">
    <div class="upper-div" v-if="requested_companies.length > 0" >
      <div class="request-table glass-effect">
        
        <h1>Requested Companies</h1>
        <div class="table-responsive">
          <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Email</th>
        <th scope="col">HR Contact</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="company in requested_companies" :key="company.id">
        <th scope="row">{{ company.company_code }}</th>
        <td>{{ company.name }}</td>
        <td>{{ company.email }}</td>
        <td>{{ company.hr_contact }}</td>
<td class="btn-conatiner btn-action-container">
<button
type="button"
class="btn btn-outline-danger btn-danger"
title="Reject Company"
@click="companyAction(company.user_id,'reject')"
>
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-x" viewBox="0 0 16 16">
  <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m.256 7a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z"/>
  <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m-.646-4.854.646.647.646-.647a.5.5 0 0 1 .708.708l-.647.646.647.646a.5.5 0 0 1-.708.708l-.646-.647-.646.647a.5.5 0 0 1-.708-.708l.647-.646-.647-.646a.5.5 0 0 1 .708-.708"/>
</svg>
</button>
<button
type="button"
class="btn btn-outline-success btn-success"
title="Approve Company"
@click="companyAction(company.user_id,'approve')"
>
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-plus-fill" viewBox="0 0 16 16">
  <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
  <path fill-rule="evenodd" d="M13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5"/>
</svg>

</button>



</td>
      </tr>


    </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="lower-div">
      <div class="card student-table glass-effect">
        <div class="header-card">
                <h4>Registered Students</h4>
          <div class="search-bar">
            <input type="text" placeholder="Search student (ID, Name, Department...)" class="search-input" v-model="studentQuery" title="ID, Name, Department, CGPA" required/>
          </div>
        </div>
        
        <div class="table-responsive">
          <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Department</th>
        <th scope="col">CGPA</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="filteredStudents.length === 0">
              <td colspan="5">No Students</td>
      </tr>
      <tr v-for="student in filteredStudents" :key="student.id">
        <th scope="row">{{ student.student_code }}</th>
        <td>{{ student.name }}</td>
        <td>{{ student.department }}</td>
        <td>{{ student.cgpa }}</td>
        <td class="btn-conatiner btn-action-container">
          <button type="button" class="btn btn-outline-primary btn-danger" title="Blacklist Student" @click="blacklistUser(student.user_id)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill-slash" viewBox="0 0 16 16">
          <path d="M13.879 10.414a2.501 2.501 0 0 0-3.465 3.465zm.707.707-3.465 3.465a2.501 2.501 0 0 0 3.465-3.465m-4.56-1.096a3.5 3.5 0 1 1 4.949 4.95 3.5 3.5 0 0 1-4.95-4.95ZM11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-9 8c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4"/>
        </svg>
        </button>
        </td>
      </tr>
    </tbody>
          </table>
        </div>
      </div>
      <div class="card company-table glass-effect">
          <div class="header-card">
            <h4>Registered Companies</h4>
            <div class="search-bar">
            <input type="text" placeholder="Search company (ID, Name, hr, email...)" class="search-input" v-model="companyQuery" title="ID, Name, hr, email" required/>
          </div>
        </div>
        <div class="table-responsive">
          <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Email</th>
        <th scope="col">Hr Contact</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="filteredCompanies.length === 0">
        <td colspan="5">No Companies</td>
      </tr>
      <tr v-for="company in filteredCompanies" :key="company.id">
        <th scope="row">{{ company.company_code }}</th>
        <td>{{ company.name }}</td>
        <td>{{ company.email }}</td>
        <td>{{ company.hr_contact }}</td>
        <td class="btn-conatiner btn-action-container">
          <button type="button" class="btn btn-outline-primary btn-danger" title="Blacklist Company" @click="blacklistUser(company.user_id)">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-person-fill-slash" viewBox="0 0 18 18">
          <path d="M13.879 10.414a2.501 2.501 0 0 0-3.465 3.465zm.707.707-3.465 3.465a2.501 2.501 0 0 0 3.465-3.465m-4.56-1.096a3.5 3.5 0 1 1 4.949 4.95 3.5 3.5 0 0 1-4.95-4.95ZM11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0m-9 8c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4"/>
        </svg>
        </button>
        </td>
      </tr>
    </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="lower-div">
      <div class="card student-table glass-effect">
        <h1>Blacklisted Students</h1>
        <div class="table-responsive">
          <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Department</th>
        <th scope="col">CGPA</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="blacklisted_students.length === 0">
        <td colspan="5">No Blacklisted Student</td>
      </tr>
      <tr v-for="student in blacklisted_students" :key="student.id">
        <th scope="row">{{ student.student_code }}</th>
        <td>{{ student.name }}</td>
        <td>{{ student.department }}</td>
        <td>{{ student.cgpa }}</td>
        <td class="btn-conatiner btn-action-container">
          <button type="button" class="btn btn-outline-primary btn-success" title="Permit Student" @click="permitUser(student.user_id)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-check-fill" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
  <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
</svg>
        </button>
        </td>
      </tr>
    </tbody>
          </table>
        </div>
      </div>
      <div class="card company-table glass-effect">
        <h1>Blacklisted Companies</h1>
        <div class="table-responsive">
          <table class="table">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Name</th>
        <th scope="col">Email</th>
        <th scope="col">Hr Contact</th>
        <th scope="col">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="blacklisted_companies.length === 0">
        <td colspan="5">No Blacklisted Company</td>
      </tr>
      <tr v-for="company in blacklisted_companies" :key="company.id">
        <th scope="row">{{ company.company_code }}</th>
        <td>{{ company.name }}</td>
        <td>{{ company.email }}</td>
        <td>{{ company.hr_contact }}</td>
        <td class="btn-conatiner btn-action-container">
          <button type="button" class="btn btn-outline-primary btn-success" title="Permit Company" @click="permitUser(company.user_id)">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-check-fill" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0"/>
  <path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
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
</template>
<script>
import axios from "axios"

export default{
  data(){
    return{

      token:"",

      requested_companies:[],
      students:[],
      companies:[],

      blacklisted_students:[],
      blacklisted_companies:[],

      studentQuery:"",
      companyQuery:""

    }
  },

  mounted(){

    this.loadToken()
    this.fetchUsers()

  },
  computed:{

    filteredStudents(){

      if(!this.studentQuery){
        return this.students
      }

      const searchQuery = this.studentQuery.toLowerCase()

      // if(this.studentSearchType === "id"){
      //   return this.students.filter(student => String(student.student_code).includes(searchQuery))
      // }

      // if(this.studentSearchType === "name"){
      //   return this.students.filter(student => student.name.toLowerCase().includes(searchQuery))
      // }
      return this.students.filter(student =>
        String(student.student_code).toLowerCase().includes(searchQuery) ||
        student.name.toLowerCase().includes(searchQuery) ||
        student.department.toLowerCase().includes(searchQuery) ||
        String(student.cgpa).includes(searchQuery)
      )

      // return this.students
    },

    filteredCompanies(){

      if(!this.companyQuery){
        return this.companies
      }

      const searchQuery = this.companyQuery.toLowerCase()

      // if(this.companySearchType === "company_name"){
      //   return this.companies.filter(company => company.name.toLowerCase().includes(searchQuery))
      // }

      // if(this.companySearchType === "id"){
      //   return this.companies.filter(company => String(company.company_code).includes(searchQuery))
      // }

      // return this.companies

      return this.companies.filter(company =>
        String(company.company_code).includes(searchQuery) ||
        company.name.toLowerCase().includes(searchQuery) ||
        company.email.toLowerCase().includes(searchQuery) ||
        company.hr_contact.toLowerCase().includes(searchQuery)
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
    fetchUsers(){

      axios.get("http://127.0.0.1:5000/api/admin/users",{
        headers:{
          Authorization:`Bearer ${this.token}`
        }
      })
      .then(res=>{
        this.requested_companies = res.data.requested_companies
        this.students = res.data.students
        this.companies = res.data.companies
        this.blacklisted_students = res.data.blacklisted_students
        this.blacklisted_companies = res.data.blacklisted_companies
      })
      .catch(err=>{
        console.log(err.response || err.message)
      })
    },
    blacklistUser(userId){
      if(!confirm("Are you sure you want to blacklist this user?")){
        return
      }
        axios.post(`http://127.0.0.1:5000/api/admin/blacklist/${userId}`,{},{
          headers:{
            Authorization:`Bearer ${this.token}`
          }
        })
        .then(res=>{
          alert(res.data.message)

          this.fetchUsers()
        })
        .catch(err=>{
          alert(err.response?.data?.message || "Blacklist failed")
        })
    },
    permitUser(user_id){

  if(!confirm("Permit this user?")){
  return
  }

  axios.post(`http://127.0.0.1:5000/api/admin/permit-user/${user_id}`,{},{
  headers:{
  Authorization:`Bearer ${this.token}`
  }
  })

  .then(res=>{
  alert(res.data.message)

  // refresh list
  this.fetchUsers()
  })

  .catch(err=>{
  console.log(err.response || err.message)
  alert(err.response?.data?.message || "Failed to permit user")
  })

    },
    companyAction(userId, action){

  if(!confirm(`Are you sure you want to ${action} this company?`)){
  return
  }

  axios.post(`http://127.0.0.1:5000/api/admin/action/${userId}`,
  {
  action: action
  },
  {
  headers:{
  Authorization:`Bearer ${this.token}`
  }
  })
  .then(res=>{

  alert(res.data.message)

  this.fetchUsers()

  })
  .catch(err=>{

  alert(err.response?.data?.message || "Action failed")

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
  /* flex: 1; */
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
  max-height: 250px;
  overflow-y: auto;
}

.lower-div .table-responsive{
    max-height: 350px;
}

.table-responsive th, .table-responsive td {
  vertical-align: middle;
  text-align: center;
  color: #fff;
}

.lower-div {
    flex: 1;
  display: flex;
  gap: 24px;
  padding: 0 24px 24px;
  align-items: flex-start;
  margin-top: 20px;
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

.glass-effect {
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
}
.btn-danger{
    background-color: transparent;
    color: red;
    border: 1px solid red;
    margin-left:15px ;
    /* font-size: 1.; */
    /* padding: 6px; */
}

.btn-danger:hover{
    color: #000;
    background-color: red;
}

.btn-success:hover{
    color: black;
    background-color: #037e03d4;
}

.btn-success{
    background-color: transparent;
    color: #008000;
    border: 1px solid #008000;
    margin-left:15px ;
    /* padding: 6px; */
}

/* .search-wrapper{
  width: 100%;
  height: 50px;
  padding: 4px 9px;
  border-radius: 7px;
  margin-bottom: 15px;
  background: rgba(255, 255, 255, 0.016);
} */

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