<script>
import router from '../router'

export default {
    name: 'listing',
    props: ['listing'],
    methods: {
        openListing() {
            router.push({ path: `/listings/${this.listing.id}` })
        },
    },
}
</script>

<template>
    <div class="listing-block" @click="openListing">
        <div style="margin: 10px 20px;">
            <img class="img" :src="listing.image" />
            <div class="title">{{ listing.title }}</div>
			<div><b>Price:</b> ${{ listing.price }}</div>
            <div>by {{ listing.user.username }}</div>
        </div>
    </div>
</template>

<style>

.img {
    width: 100px;
}

</style>