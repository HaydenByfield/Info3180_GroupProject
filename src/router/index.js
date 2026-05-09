import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import CreateProfileView from "../views/CreateProfileView.vue";
import EditProfileView from "../views/EditProfileView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // Login View

      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      // route level code-splitting
      // Register View
  
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/messages',
      name: 'messages',

      component: () => import('../views/MessageView.vue')
    },
    {
      path: '/matches',
      name: 'matches',

      component: () => import('../views/MatchesView.vue')
    },
    {
      path: '/favourites',
      name: 'favourites',

      component: () => import('../views/FavouritesView.vue')
    },
    {
      path: "/profile/create",
      name: "create-profile",
      component: CreateProfileView
    },
    {
      path: "/profile/edit",
      name: "edit-profile",
      component: EditProfileView
    }

  ]
})

export default router
