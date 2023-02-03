<template>
    <news-list :news="news">

    </news-list>
</template>

<script>
import NewsList from '@/components/NewsList.vue'
import axios from 'axios';

export default {
    name: 'Home',
    components: {
        NewsList
    },
    
    data() {
        return {
            news: ''
        }
    },
    methods: {
        getResponse(){
            const path = 'http://0.0.0.0:5000/'
            axios.get(path)
            .then((res) => {
                console.log(res.data)
                this.news = res.data;
            })
            .catch((err) => {
                console.error(err);
            });
            },
        },
        created() {
            this.getResponse();
        }
    }
</script>