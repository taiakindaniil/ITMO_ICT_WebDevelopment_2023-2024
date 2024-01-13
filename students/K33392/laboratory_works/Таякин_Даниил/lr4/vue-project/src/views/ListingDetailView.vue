<script>
import api from '../api'
import { useAuthStore } from '../stores/auth'
import CommentsView from './CommentsView.vue'

export default {
    data() {
        this.authStore = useAuthStore();
        return { listing: { id: this.$route.params.id, title: '', description: '' }, bids: [] };
    },
    beforeMount() {
        api
            .get(`api/listings/${this.listing.id}`)
            .then((resp) => resp.data)
            .then((data) => (this.listing = data))
            .catch((_) => alert('Failed to fetch listing'));

        api
            .get(`api/listings/${this.listing.id}/bids`)
            .then((resp) => resp.data)
            .then((data) => (this.bids = data))
            .catch((_) => alert('Failed to fetch listing\'s bids'));
    },
    components: { CommentsView }
}
</script>

<template>
    <h2>Listing: {{ listing.title }}</h2>

	<h2 v-if="listing.status == false" style="color:red">Closed</h2>

    <div>
		<img v-if="listing.image" class="listing-image" :src="listing.image" />
		<div v-if="listing.description" class="listing-desc">{{ listing.description }}</div>
	</div>

    <div style="margin: 40px 0">
		<div><b>Starting Price:</b> ${{ listing.price }}</div>
        
        <br />

        <template v-if="bids.length != 0">
            <div v-if="bids[bids.length - 1].price" class="listing-price"><b>Current Price:</b> ${{ bids[bids.length - 1].price }}</div>
            <div v-if="this.authStore.username == bids[bids.length - 1].user.username">Your bid is the current bid.</div>
        </template>
	</div>

	<div style="margin: 40px 0">
		<h3>Details</h3>
		<ul>
			<li>Listed by: <b>{{ listing.user.username }}</b></li>
			<li v-if="listing.category">Category: {{ listing.category.title }}</li>
		</ul>
	</div>
    <CommentsView :listing="listing"/>
</template>

<style>

.listing-image {
    max-width: 400px;
    max-height: 400px;
}

</style>