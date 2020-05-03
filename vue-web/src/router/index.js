import Vue from 'vue';
import VueRouter from 'vue-router';
// import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "newsfeed" */ '../views/Home.vue'),
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/feed',
    name: 'news',
    component: () => import(/* webpackChunkName: "newsfeed" */ '../views/NewsFeed.vue'),
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import(/* webpackChunkName: "settings" */ '../views/Settings.vue'),
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import(/* webpackChunkName: "auth" */ '../components/auth/Auth.vue'),
  },
  {
    path: '/success',
    name: 'success',
    component: () => import(/* webpackChunkName: "authsuccess" */ '../components/auth/AuthSuccess.vue'),
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import(/* webpackChunkName: "authsuccess" */ '../views/Admin.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
