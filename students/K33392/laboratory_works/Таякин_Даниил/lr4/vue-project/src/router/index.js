import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import ListingsView from '../views/ListingsView.vue'
import ListingDetailView from '../views/ListingDetailView.vue'
import WatchlistView from '../views/WatchlistView.vue'
import NewCommentView from '../views/NewCommentView.vue'
import NewListingView from '../views/NewListingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/sign-up',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/watchlist',
      name: 'watchlist',
      component: WatchlistView
    },
    {
      path: '/listings',
      name: 'listings',
      component: ListingsView
    },
    {
      path: '/listings/:id',
      name: 'listing',
      component: ListingDetailView
    },
    {
      path: '/listings/:id/new-comment',
      name: 'newcomment',
      component: NewCommentView
    },
    {
      path: '/listings/new',
      name: 'newlisting',
      component: NewListingView
    },
  ]
})

export default router
