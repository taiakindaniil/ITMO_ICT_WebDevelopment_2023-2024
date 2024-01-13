<script>
import api from '../api'
import router from '../router'
import { useAuthStore } from '../stores/auth'

export default {
    data() {
        this.authStore = useAuthStore()
        return {
            loginData: {
                email: '',
                username: '',
                password: '',
            },
        }
    },
    methods: {
        login() {
        api
            .post('auth/token/login', {
                username: this.loginData.username,
                password: this.loginData.password,
            })
            .then((resp) => resp.data)
            .then((data) => {
                this.authStore.login(
                    this.loginData.username,
                    this.loginData.password,
                    data.auth_token
                )
                router.push({ path: '/listings' })
            })
        },
    },
}
</script>

<template>
    <div>
        <div class="login">
        <h3>Login</h3>
        <label for="username">Username</label>
        <input type="text" name="username" v-model="loginData.username" />
        <br />
        <br />
        <label for="password">Password</label>
        <input type="password" name="password" v-model="loginData.password" />
        <br />
        <br />
        <button v-on:click="login">Login</button>
    </div>
</div>
</template>