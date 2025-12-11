import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomeView from '../components/HomeView.vue';
import ExploreView from '../components/ExploreView.vue';
import MovieDetail from '../components/MovieDetail.vue';
import UserProfile from '../components/UserProfile.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/explore',
    name: 'Explore',
    component: ExploreView,
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: MovieDetail,
    props: true, // This allows the route param 'id' to be passed as a prop to the component
  },
  {
    path: '/profile/:userId',
    name: 'UserProfile',
    component: UserProfile,
    props: true,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  },
});

export default router;
