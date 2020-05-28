import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "newsfeed" */ '../views/Home.vue'),
  },
  {
    path: '/feed',
    name: 'feed',
    component: () => import(/* webpackChunkName: "newsfeed" */ '../views/Feed.vue'),
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
    component: () => import(/* webpackChunkName: "admin" */ '../views/Admin.vue'),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
