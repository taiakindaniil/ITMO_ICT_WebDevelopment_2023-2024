<script>
import router from '../router'
import api from '../api'

export default {
    data() {
        return { listingId: this.$route.params.id, content: '' }
    },
    methods: {
        publish() {
        api
            .post('api/comments/', {
                comment: this.content,
                listing_id: this.listingId,
            })
            .then((_) => router.push({ path: `/listings/${this.listingId}` }))
            .catch((_) => alert('Failed to create a comment'))
        },
    },
}
</script>

<template>
    <h2>New comment</h2>
    <label for="content">Content</label>
    <br />
    <textarea name="content" cols="30" rows="10" v-model="content"></textarea>
    <br /><br />
    <button v-on:click="publish">Create</button>
</template>
