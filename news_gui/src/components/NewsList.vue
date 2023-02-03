<template>
    <div>
        <h3>
            News
        </h3>
        <div v-for="new_item in news" :key="new_item.id">
            <a :href="new_item.source_link"
            target="_blank">{{ new_item.header_original }}</a>
        </div>
    </div>
</template>
<script>

export default {
    props: {
        news: {
          type: Array,
          required: true,
        }
    }

}
</script>

<style scoped>
</style>