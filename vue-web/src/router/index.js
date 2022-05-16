import Vue from 'vue';
import VueRouter from 'vue-router';
// import store from '../store/index';

Vue.use(VueRouter);

const routes = [
  // route level code-splitting
  // this generates a separate chunk (about.[hash].js) for this route
  // which is lazy-loaded when the route is visited.
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
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "entry" */ '../views/Pipelines.vue'),
  },
  {
    path: '/topic',
    name: 'topic',
    component: () => import(/* webpackChunkName: "entry" */ '../views/Topic.vue'),
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import(/* webpackChunkName: "auth" */ '../components/auth/Auth.vue'),
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import(/* webpackChunkName: "admin" */ '../views/Admin.vue'),
  },
  {
    path: '/summaries',
    name: 'summaries',
    component: () => import(/* webpackChunkName: "admin" */ '../views/Summaries.vue'),
  },
  {
    path: '/articles',
    name: 'articles',
    component: () => import(/* webpackChunkName: "admin" */ '../views/Articles.vue'),
  },
  {
    path: '/pipelines',
    name: 'pipelines',
    component: () => import(/* webpackChunkName: "admin" */ '../views/Pipelines.vue'),
  },
];

const router = new VueRouter({
  routes,
});

// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.getters.user !== undefined;
//   debugger;
//   console.log('router before each');
//   if (!isAuthenticated && to.name !== 'auth') {
//     console.log('go');
//     next({ name: 'auth' });
//   } else next();
// });

export default router;
