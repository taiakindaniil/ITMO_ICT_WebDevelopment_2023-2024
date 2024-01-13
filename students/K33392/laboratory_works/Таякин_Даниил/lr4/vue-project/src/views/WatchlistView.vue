<script>
import api from '../api'
import Listing from '../components/Listing.vue'

export default {
    data() {
        return { listings: [] }
    },
    components: {
        Listing,
    },
    methods: {
        getMyWatchlist() {
        api
            .get('api/watchlists/my')
            .then((resp) => resp.data)
            .then((data) => (this.listings = data.map( function(l) { return l.listing } )))
            .catch(() => alert('Failed to fetch listings'))
        },
    },
    beforeMount() {
        this.getMyWatchlist()
    },
}
</script>

<template>
    <br />
    <div class="listings">
        <Listing v-for="listing in listings" :listing="listing" :key="listing.id" />
    </div>
</template>