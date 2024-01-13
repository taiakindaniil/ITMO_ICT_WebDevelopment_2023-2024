<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

let authStore = useAuthStore()

</script>

<template>
  <nav class="header">
    <template v-if="authStore.userData.username === ''">
      <RouterLink to="/login">Login</RouterLink>
      <RouterLink to="/sign-up">Sign Up</RouterLink>
    </template>
    <template v-else>
      <RouterLink to="/listings">Active Listings</RouterLink>
      <RouterLink to="/watchlist">Watchlist</RouterLink>
      <button @click="authStore.logout()">Log out</button>
    </template>
  </nav>
  <RouterView />
</template>

<style scoped>
.header {
  background-color: #29bfff;
  font-weight: 600;
  padding: 10px;
  display: flex;
  gap: 15px;
}
</style>