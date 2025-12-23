import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomeView from '../components/HomeView.vue';
import ExploreView from '../components/ExploreView.vue';
import MovieDetail from '../components/MovieDetail.vue';
import UserProfile from '../components/UserProfile.vue';
import ExploreFullView from '../components/ExploreFullView.vue';
import CommunityView from '../components/community/CommunityView.vue';
import PostDetail from '../components/community/PostDetail.vue';
import PostCreate from '../components/community/PostCreate.vue';
import FollowedMoviesView from '../components/community/FollowedMoviesView.vue';

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
    path: '/explore/full',
    name: 'ExploreFull',
    component: ExploreFullView,

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
  },
  {
    path: '/community',
    name: 'Community',
    component: CommunityView,
  },
  {
    path: '/community/post/:id',
    name: 'PostDetail',
    component: PostDetail,
    props: true,
  },
  {
    path: '/community/create',
    name: 'PostCreate',
    component: PostCreate,
  },
  {
    path: '/community/following',
    name: 'FollowedMovies',
    component: FollowedMoviesView,
    meta: { requiresAuth: true } // 로그인 필요 시
  },
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
