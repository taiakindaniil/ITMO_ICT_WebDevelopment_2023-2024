import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({ password: localStorage.getItem("password"), username: localStorage.getItem("username"), token: localStorage.getItem("auth_token") }),
    getters: {
        userData: (state) => state
    },
    actions: {
        login(username, password, token) {
            this.username = username
            this.password = password
            this.token = token
            localStorage.setItem("auth_token", token)
            localStorage.setItem("username", username)
            localStorage.setItem("password", password)
        },
        logout() {
            this.username = ''
            this.password = ''
            this.token = ''
            localStorage.removeItem("auth_token")
            localStorage.removeItem("username")
            localStorage.removeItem("password")
        },
    }
})