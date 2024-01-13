<script>
import api from '../api'
import Listing from '../components/Listing.vue'
import router from '../router'

export default {
    data() {
        return { listings: [] }
    },
    components: {
        Listing,
    },
    methods: {
        getListings() {
        api
            .get('api/listings/')
            .then((resp) => resp.data)
            .then((data) => (this.listings = data))
            .catch(() => alert('Failed to fetch listings'))
        },
        newListing() {
            router.push({ path: '/listings/new' })
        },
    },
    beforeMount() {
        this.getListings()
    },
}
</script>

<template>
    <br />
    <button @click="newListing">New listing</button>
    <div class="listings">
        <Listing v-for="listing in listings" :listing="listing" :key="listing.id" />
    </div>
</template>