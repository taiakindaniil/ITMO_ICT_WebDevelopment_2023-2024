<script>

export default {
  props: ['comment'],
}

</script>

<template>
    <div>
        <b>{{ comment.user.username }}:</b>
        <br>
        {{ comment.comment }}
    </div>
</template>