import { createRouter, createWebHistory } from 'vue-router'

const  routes = [
    { path: '/', component: () => import('@/pages/HomePage.vue') 
    },
    { path: '/login', component: () => import('@/pages/LoginPage.vue') 
    },
    { path: '/register', component: () => import('@/pages/RegisterPage.vue') 
    },
    { path: '/auth/dashboard', component: () => import('@/pages/Dashboard.vue') 
    },
    { path: "/admin/users" ,component: () => import('@/pages/AdminUserPage.vue') 
    },
    { path: '/admin/drives', component: () => import('@/pages/AdminDrivesPage.vue') 
    },
    { path: "/company/create-drive" ,component: () => import('@/pages/CompanyCreateDrive.vue')
    },
    { path: "/company/update-drive/:driveId" ,component: () => import('@/pages/CompanyCreateDrive.vue')
    },
    { path: '/company/view/applications/:driveId', component: () => import('@/pages/CompanyStudentApplication.vue')
    },
    { path: "/student/company-drives/:companyId" ,component: () => import('@/pages/StudentCompany.vue')
    },
    { path: '/student/history', component: () => import('@/pages/StudentHistory.vue')
    }, 
    { path: '/company/drive/:driveId', component: () => import('@/pages/Drive.vue') 
    },
    { path: '/company/application/:applicationId', component: () => import('@/pages/Student.vue') 
    },
    { path: '/auth/profile', component: () => import('@/pages/Profile.vue') 
    },
  ]


export const router = createRouter({
  history: createWebHistory(),
  routes // same as routes: routes
})
