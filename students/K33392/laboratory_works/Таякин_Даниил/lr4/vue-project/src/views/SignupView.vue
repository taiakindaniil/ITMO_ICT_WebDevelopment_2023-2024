<script>
import api from '../api'
import router from '../router'
import { useAuthStore } from '../stores/auth'

export default {
    data() {
        this.authStore = useAuthStore()
        return {
            signupData: {
                email: '',
                username: '',
                password: '',
            },
        }
    },
    methods: {
        signup() {
        api
            .post('api/users/', {
                email: this.signupData.email,
                username: this.signupData.username,
                password: this.signupData.password,
            })
            .then((resp) => resp.data)
            .then((data) => {
                this.authStore.login(
                    this.signupData.username,
                    this.signupData.password,
                    data.auth_token
                )
                router.push({ path: '/listings' })
            })
        },
    },
}

</script>

<template>
    <div class="signup">
        <h3>Sign Up</h3>
        <label for="email">Email</label>
        <input type="text" name="email" v-model="signupData.email" />
        <br />
        <br />
        <label for="username">Username</label>
        <input type="text" name="username" v-model="signupData.username" />
        <br />
        <br />
        <label for="password">Password</label>
        <input type="password" name="password" v-model="signupData.password" />
        <br />
        <br />
        <button v-on:click="signup">Sign Up</button>
    </div>
</template>