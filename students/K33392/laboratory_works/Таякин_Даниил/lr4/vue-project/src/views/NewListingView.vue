<script>
import router from '../router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

export default {
    data() {
        this.authStore = useAuthStore()
        return {
            title: '',
            description: '',
            image: '',
            price: 0,
        }
    },
    methods: {
        publish() {
        api
            .post('api/listings/', {
                title: this.title,
                description: this.description,
                user: this.authStore.userData.username,
                price: this.price,
                image: this.image,
                status: true,
            })
            .then((_) => router.push({ path: '/listings' }))
            .catch((_) => alert('Failed to create a listing'))
        },
    },
}
</script>

<template>
    <h2>Create Listing</h2>
    
    <label for="title">Title</label>
    <br />
    <input type="text" name="title" v-model="title" />
    
    <br /><br />
    
    <label for="description">Description (optional)</label>
    <br />
    <textarea name="description" cols="30" rows="10" v-model="description"></textarea>
    
    <br /><br />
    
    <label for="image">Image URL (optional)</label>
    <br />
    <input type="text" name="image" v-model="image" />
    
    <br /><br />

    <label for="image">Starting price $</label>
    <br />
    <input type="number" name="price" v-model="price" />
    
    <br /><br />

    <button v-on:click="publish">Create</button>
</template>
