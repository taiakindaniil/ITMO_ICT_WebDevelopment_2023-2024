# Лабораторная работа #4

## Задание 

Реализация клиентской части приложения средствами vue.js.

## Реализация 

### main.js

Создадим наше приложение, подключив к нему роутер и pinia для state management.

```js
import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

```

### stores/index.js

Создадим глобальное хранилище для пользовательских данных. Нам они понадобятся для реализации входа, регистрации и профиля пользователя.

Для данной лабораторной работы нам понадобится хранение и получение пароля, имени пользователя и электронной почты.

```js
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
```

### api/index.js

Для нашего бекенда, который использует авторизацию с помощью токенов, нам нужно создать функцию, которая будет добавлять заголовок Authorization с токеном пользователя перед отправкой HTTP запроса. Мы решили использовать библиотеку axios для выполнения HTTP запросов в этой лабораторной работе.

### views/LoginView.vue

Реализуем необходимый метод входа в предсталвении страницы логина, который делает post-запрос на API.

```js
<script>
import api from '../api'
import router from '../router'
import { useAuthStore } from '../stores/auth'

export default {
    data() {
        this.authStore = useAuthStore()
        return {
            loginData: {
                email: '',
                username: '',
                password: '',
            },
        }
    },
    methods: {
        login() {
        api
            .post('auth/token/login', {
                username: this.loginData.username,
                password: this.loginData.password,
            })
            .then((resp) => resp.data)
            .then((data) => {
                this.authStore.login(
                    this.loginData.username,
                    this.loginData.password,
                    data.auth_token
                )
                router.push({ path: '/listings' })
            })
        },
    },
}
</script>

<template>
    <div>
        <div class="login">
        <h3>Login</h3>
        <label for="username">Username</label>
        <input type="text" name="username" v-model="loginData.username" />
        <br />
        <br />
        <label for="password">Password</label>
        <input type="password" name="password" v-model="loginData.password" />
        <br />
        <br />
        <button v-on:click="login">Login</button>
    </div>
</div>
</template>
```

### views/SignupView.vue

Реализуем необходимый метод регистрации в предсталвении страницы, который делает post-запрос на API.

```js
<script>
import api from '../api'
import router from '../router'
import { useAuthStore } from '../stores/auth'

export default {
    data() {
        this.authStore = useAuthStore()
        return {
            signupData: {
                email: '',
                username: '',
                password: '',
            },
        }
    },
    methods: {
        signup() {
        api
            .post('api/users/', {
                email: this.signupData.email,
                username: this.signupData.username,
                password: this.signupData.password,
            })
            .then((resp) => resp.data)
            .then((data) => {
                this.authStore.login(
                    this.signupData.username,
                    this.signupData.password,
                    data.auth_token
                )
                router.push({ path: '/listings' })
            })
        },
    },
}

</script>

<template>
    <div class="signup">
        <h3>Sign Up</h3>
        <label for="email">Email</label>
        <input type="text" name="email" v-model="signupData.email" />
        <br />
        <br />
        <label for="username">Username</label>
        <input type="text" name="username" v-model="signupData.username" />
        <br />
        <br />
        <label for="password">Password</label>
        <input type="password" name="password" v-model="signupData.password" />
        <br />
        <br />
        <button v-on:click="signup">Sign Up</button>
    </div>
</template>
```

### views/ListingsView.vue

Данное предсталвение является первым экраном, что видит пользователь после входа в свою учетную запись в данном приложении.

```js
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
```

### view/ListingDetailView.vue

Данное представление ялвяется развернутой странице с полной информацией о листинге, включая комментарии, последнюю ставку.

```js
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
```

### views/CommentsView.vue

Данное представление реализует постраничный просмотр комментариев под листингом. 

```js
<script>
import api from '../api'
import router from '../router'
import Comment from '../components/Comment.vue'
import { RouterLink } from 'vue-router'

export default {
    props: ['listing'],
    data() {
        return { post: this.$props.listing, comments: [], currentPage: 0, perPage: 2 }
    },
    methods: {
        newComment() {
            router.push({ path: `/listings/${this.listing.id}/new-comment` })
        },
        prevPage() {
        if (this.currentPage - 1 >= 0) {
            this.currentPage--
            this.fetchComments()
        }
        },
        nextPage() {
            this.currentPage++
            this.fetchComments()
        },
        fetchComments() {
            console.log('fetching ', this.currentPage)
            api
                .get(`api/listing_comments/${this.listing.id}`, {
                    params: { page: this.currentPage, perPage: this.perPage },
                })
                .then((resp) => resp.data)
                .then((data) => (this.comments = data))
                .catch((_) => alert('Failed to fetch comments'))
        },
    },
    beforeMount() {
        this.currentPage = 0
        this.fetchComments()
    },
    components: [Comment],
    components: { Comment, RouterLink },
}
</script>

<template>
    <h3>Comments</h3>
    <button v-on:click="newComment">New comment</button>
    <Comment v-for="comment in comments" :comment="comment" :key="comment.id" />
    <div class="pagination">
        <button v-on:click="prevPage">&lt; Prev</button>
        <button v-on:click="nextPage">Next &gt;</button>
    </div>
</template>
```

### views/NewCommentView.vue

Данное представление отвечает за создание новых комментариев под листингом.

```js
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
```

### views/NewListingView.vue

Данное представление предназначено для создания новыйх листингов на платформе.

```js
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

```