# Лабораторная работа #3

## Задание 

Свой вариант. Реализация серверной части веб сервиса аукционов средствами django, djangorestframework, djoser.

## Реализация

### models.py

Модель `User` используется для авторизации пользователей.
```python
class User(AbstractUser):
	pass
```

Модель `Listing` хранит данные о проходящем аукционе.
```python
class Listing(models.Model):
	title = models.CharField(max_length=64)
	image = models.URLField(max_length=280, blank=True, null=True)
	description = models.CharField(max_length=280, blank=True, null=True)
	category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="listings", blank=True, null=True)
	price = models.IntegerField()
	user = models.ForeignKey("User", on_delete=models.CASCADE)
	status = models.BooleanField(default=True)
	
	def __str__(self):
		return self.title
```

`Category` хранит информацию о категориях на которые разбиваются проходящие аукционы.
```python
class Category(models.Model):
	title = models.CharField(max_length=64)
	image = models.ImageField(upload_to="media/categories")

	def __str__(self):
		return self.title
```

`Bid` хранит информацию о ставках на аукционе.
```python
class Bid(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
	price = models.IntegerField()

	def __str__(self):
		return f"{self.id}. {self.user.username} bid {self.listing.title} for {self.price}"
```

`Comment` хранит данные о комментариях под аукционами, включая рейтинг (1-10).
```python
class Comment(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")
	comment = models.CharField(max_length=280)
	rating = models.IntegerField(
		default=1,
		validators=[
			MaxValueValidator(10),
            MinValueValidator(1)
        ]
	)

	def __str__(self):
		return f"{self.id}. {self.user}"
```

`Watchlist` хранит информацию об отслеживаемых аукционах пользователями.
```python
class Watchlist(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.id}. {self.user.username}: {self.listing.title}"
```


### serializers.py

Для CRUD операций над моделями через API нам необходимо написать `ModelSerializer` для каждой модели.

В `MyUserSerializer` нам необходимо переопределить метод create, так как у нас кастомная модель пользователя и нам нужно сохранять хеш пароля в базу.

```python
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )
    def create(self, validated_data):
        return super().create({**validated_data, "password": make_password(validated_data["password"])})
```

Все остальные классы остаются без переопределений методов и выглядят следующим образом:

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "image")


class ListingSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = MyUserSerializer()
    class Meta:
        model = Listing
        fields = ("id", "title", "image", "description", "category", "price", "user", "status")


class WatchlistSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    listing = ListingSerializer()
    class Meta:
        model = Watchlist
        fields = ("id", "user", "listing")


class BidSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    listing = ListingSerializer()
    class Meta:
        model = Watchlist
        fields = ("id", "user", "listing", "price")


class CommentSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    listing = ListingSerializer()
    class Meta:
        model = Comment
        fields = ("id", "user", "listing", "comment", "rating")
```

В некоторых сериализаторах можно найти обращение к другим сериализаторам для возвращения данных о них.


### views.py

Класс `viewsets.ModelViewSet` из модуля `rest_framework` позволяет нам с легкостью создать представления для наших моделей данных без написания дополнительной логике по обработке запросов.

```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
```


### settings.py

Нам необходимо установить несколько модулей, необходимых для авторизации, создания API и генерации документации.

```python
INSTALLED_APPS = [
	...
    'auctions',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf-yasg',
]
```

Для того, чтобы `djoser` знал о том, какой serializer использовать для модели пользователя, нам необходимо указать путь до класса.

```python
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'auctions.serializers.MyUserSerializer',
    },
}
```

По умолчанию все пути нашего сервера будут доступны без авторизации. Нам необходимо обратное, поэтому укажем права доступа в данном файле.

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Для корректной работы авторизации по токену, указываем настройки для Swagger. При добавлении токена в поле для авторизации, добавляем к началу также `Token <TOKEN>`.

```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
```

### urls.py

Определим пути нашего сервера. Для клиента будут доступны:

- `api/`
- `auth/`
- `admin/`
- `swagger/`

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("auctions.urls")),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.authtoken')),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
```

Более того доступные пути в `api/`

- `users/`
- `categories/`
- `listings/`
- `watchlists/`
- `bids/`
- `comments/`

```python
r = DefaultRouter()
r.register('users', UserViewSet)
r.register('categories', CategoryViewSet)
r.register('listings', ListingViewSet)
r.register('watchlists', WatchlistViewSet)
r.register('bids', BidViewSet)
r.register('comments', CommentViewSet)

urlpatterns = r.urls
```


### Endpoints

### Bids

**URL** : `/api/bids/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content POST** :

```json
{
	"id": 1,
	"user": {
		"id": 2,
		"username": "admin",
		"email": "daniel@pewpee.com",
		"first_name": "",
		"last_name": ""
	},
	"listing": {
		"id": 1,
		"title": "Broomstick",
		"image": "https://static.wikia.nocookie.net/harrypotter/images/2/29/Nimbus_200.jpg/revision/latest/scale-to-width-down/540?cb=20170721202204&path-prefix=pl",
		"description": "Nimbus 2000 Broomstick",
		"category": {
			"id": 5,
			"title": "Sports",
			"image": "http://127.0.0.1:8000/media/categories/sports-categoty3x.png"
		},
		"price": 50,
		"user": {
			"id": 1,
			"username": "daniel",
			"email": "daniel@pewpee.com",
			"first_name": "",
			"last_name": ""
		},
		"status": false
	},
	"price": 56
}
```

**Content GET** :
```json
[
	{
		"id": 1,
		"user": {
			"id": 2,
			"username": "admin",
			"email": "daniel@pewpee.com",
			"first_name": "",
			"last_name": ""
		},
		"listing": {
			"id": 1,
			"title": "Broomstick",
			"image": "https://static.wikia.nocookie.net/harrypotter/images/2/29/Nimbus_200.jpg/revision/latest/scale-to-width-down/540?cb=20170721202204&path-prefix=pl",
			"description": "Nimbus 2000 Broomstick",
			"category": {
				"id": 5,
				"title": "Sports",
				"image": "http://127.0.0.1:8000/media/categories/sports-categoty3x.png"
			},
			"price": 50,
			"user": {
				"id": 1,
				"username": "daniel",
				"email": "daniel@pewpee.com",
				"first_name": "",
				"last_name": ""
			},
			"status": false
		},
		"price": 56
	},
]
```

**URL** : `/api/bids/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 1,
	"user": {
		"id": 2,
		"username": "admin",
		"email": "daniel@pewpee.com",
		"first_name": "",
		"last_name": ""
	},
	"listing": {
		"id": 1,
		"title": "Broomstick",
		"image": "https://static.wikia.nocookie.net/harrypotter/images/2/29/Nimbus_200.jpg/revision/latest/scale-to-width-down/540?cb=20170721202204&path-prefix=pl",
		"description": "Nimbus 2000 Broomstick",
		"category": {
			"id": 5,
			"title": "Sports",
			"image": "http://127.0.0.1:8000/media/categories/sports-categoty3x.png"
		},
		"price": 50,
		"user": {
			"id": 1,
			"username": "daniel",
			"email": "daniel@pewpee.com",
			"first_name": "",
			"last_name": ""
		},
		"status": false
	},
	"price": 56
}
```

### Categories
**URL** : `/api/categories/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :
```json
[
	{
		"id": 0,
		"title": "string",
		"image": "string"
	}
]
```

**URL** : `/api/categories/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 0,
	"title": "string",
	"image": "string"
}
```

### Comments
**URL** : `/api/comments/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :
```json
[
	{
		"id": 0,
		"user": {
			"id": 0,
			"username": "0BqHODclHpFVnTrDzBz9MNN2b@H11+Im6Ytz@iJQQ3COGDRj-HbyufS4BjDsICYBiDcxxSbx5",
			"email": "user@example.com",
			"first_name": "string",
			"last_name": "string"
		},
		"listing": {
			"id": 0,
			"title": "string",
			"image": "string",
			"description": "string",
			"category": {
				"id": 0,
				"title": "string",
				"image": "string"
			},
			"price": 9223372036854776000,
			"user": {
				"id": 0,
				"username": "Sy5hibMB3B3gK+JOQKsWx-qJLSYHhVEOJlYHDR3u1qR4TKv64hcdg2VUuaGKuyRtS@y4Hq5HQ7CmXfQ4LJ1XriR.xmPVERkKS",
				"email": "user@example.com",
				"first_name": "string",
				"last_name": "string"
			},
			"status": true
		},
		"comment": "string",
		"rating": 10
	}
]
```

**URL** : `/api/comments/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 0,
	"user": {
		"id": 0,
		"username": "m+qFQUC.L0PNb+Lmn@IRCqj54Y",
		"email": "user@example.com",
		"first_name": "string",
		"last_name": "string"
	},
	"listing": {
		"id": 0,
		"title": "string",
		"image": "string",
		"description": "string",
		"category": {
			"id": 0,
			"title": "string",
			"image": "string"
		},
		"price": 9223372036854776000,
		"user": {
			"id": 0,
			"username": "6pZ",
			"email": "user@example.com",
			"first_name": "string",
			"last_name": "string"
		},
		"status": true
	},
	"comment": "string",
	"rating": 10
}
```

### Listings
**URL** : `/api/listings/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :
```json
[
	{
		"id": 0,
		"title": "string",
		"image": "string",
		"description": "string",
		"category": {
			"id": 0,
			"title": "string",
			"image": "string"
		},
		"price": 9223372036854776000,
		"user": {
			"id": 0,
			"username": "Wy",
			"email": "user@example.com",
			"first_name": "string",
			"last_name": "string"
		},
		"status": true
	}
]
```

**URL** : `/api/listings/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 0,
	"title": "string",
	"image": "string",
	"description": "string",
	"category": {
		"id": 0,
		"title": "string",
		"image": "string"
	},
	"price": 9223372036854776000,
	"user": {
		"id": 0,
		"username": "Srmhuqrn_pLRu@_lOvuKs5.s1v7Wac4HbQMAx33bn-xttlaEu7FK300vac+EqSXXH1qvt",
		"email": "user@example.com",
		"first_name": "string",
		"last_name": "string"
	},
	"status": true
}
```

### Users
**URL** : `/api/users/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :
```json
[
	{
		"id": 0,
		"username": "80e7ark.tL",
		"email": "user@example.com",
		"first_name": "string",
		"last_name": "string"
	}
]
```

**URL** : `/api/users/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 0,
	"username": "JEybMILwBEZST0_-@HnnxKtPHqIaLkLNT0bUjUwkKcX0eIiM3-5G2EUcZlmxRO+_ZXSbez7n7cect@RcGDac",
	"email": "user@example.com",
	"first_name": "string",
	"last_name": "string"
}
```

### Watchlists
**URL** : `/api/watchlists/`

**Method** : `GET, POST`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :
```json
[
	{
		"id": 0,
		"user": {
			"id": 0,
			"username": "Lh4B-xt0F_KN-BsIavPH.t0nF2",
			"email": "user@example.com",
			"first_name": "string",
			"last_name": "string"
		},
		"listing": {
			"id": 0,
			"title": "string",
			"image": "string",
			"description": "string",
			"category": {
				"id": 0,
				"title": "string",
				"image": "string"
			},
			"price": 9223372036854776000,
			"user": {
				"id": 0,
				"username": "RAG2e7xhIqs@LdnXksJADfqspqRLyM-PLXCUvwV-+F99r795wc7VkjIvs5@g_inqxK37eR",
				"email": "user@example.com",
				"first_name": "string",
				"last_name": "string"
			},
			"status": true
		}
	}
]
```

**URL** : `/api/watchlists/<int:pk>`

**Method** : `GET, PUT, PATCH, DELETE`

**Auth required** : YES

**Permissions required** : IsAuthenticated

#### Success Responses

**Code** : `200 OK`

**Content** :

```json
{
	"id": 0,
	"user": {
		"id": 0,
		"username": "TLtKUAW9u@WDTHOvyrX8",
		"email": "user@example.com",
		"first_name": "string",
		"last_name": "string"
	},
	"listing": {
		"id": 0,
		"title": "string",
		"image": "string",
		"description": "string",
		"category": {
			"id": 0,
			"title": "string",
			"image": "string"
		},
		"price": 9223372036854776000,
		"user": {
			"id": 0,
			"username": "t.9a7Nusbrsa4o35z-ZoYgWiaQfddQF2G9p9oHZN9xoqv1_I@TLpmvd4Qk@Gcf17DK+nEPgMmFLCkE",
			"email": "user@example.com",
			"first_name": "string",
			"last_name": "string"
		},
		"status": true
	}
}
```

### Пример

Попробуем получить список всех листингов аукионов.

```sh
curl -LX GET http://127.0.0.1:8000/api/listings/  
```

У нас не получится это сделать, так как мы не предоставили токен дорступа.

```json
{ "detail": "Authentication credentials were not provided." }
```

Так как наше приложение использует djoser для реализации аутентификации, то сначала запросим токен доступа.

```sh
curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'username=daniel2&password=NgYjjr@3bJxFRsR'
```

Ответ от сервера с токеном.

```json
{ "auth_token": "7350939e63742af46f5f07682c6ba6f526580481" }
```

Посмотрим все существующие листинги с нашим токеном.

```sh
curl -LX GET http://127.0.0.1:8000/api/listings/ -H 'Authorization: Token <TOKEN>'
```

Ответ от сервера таким.
```json
[
  {
    "id": 1,
    "title": "Broomstick",
    "image": "https://static.wikia.nocookie.net/harrypotter/images/2/29/Nimbus_200.jpg/revision/latest/scale-to-width-down/540?cb=20170721202204&path-prefix=pl",
    "description": "Nimbus 2000 Broomstick",
    "category": {
      "id": 5,
      "title": "Sports",
      "image": "http://127.0.0.1:8000/media/categories/sports-categoty3x.png"
    },
    "price": 50,
    "user": {
      "id": 1,
      "username": "daniel",
      "email": "daniel@pewpee.com",
      "first_name": "",
      "last_name": ""
    },
    "status": false
  },
  {
    "id": 2,
    "title": "iPhone 12",
    "image": "https://cdn.tmobile.com/content/dam/t-mobile/en-p/cell-phones/apple/Apple-iPhone-12-mini/Blue/Apple-iPhone-12-mini-Blue-frontimage.png",
    "description": null,
    "category": {
      "id": 1,
      "title": "Electronics",
      "image": "http://127.0.0.1:8000/media/categories/electronics-categoty.png"
    },
    "price": 1000,
    "user": {
      "id": 1,
      "username": "daniel",
      "email": "daniel@pewpee.com",
      "first_name": "",
      "last_name": ""
    },
    "status": true
  },
  {
    "id": 3,
    "title": "New Test",
    "image": null,
    "description": null,
    "category": null,
    "price": 10,
    "user": {
      "id": 2,
      "username": "admin",
      "email": "daniel@pewpee.com",
      "first_name": "",
      "last_name": ""
    },
    "status": false
  },
  {
    "id": 4,
    "title": "Quadra 66",
    "image": "https://static3.hotcarsimages.com/wordpress/wp-content/uploads/2020/10/Quadra-Type-66-1-e1603386447228.jpg",
    "description": "A car from Cyberpunk 2077",
    "category": {
      "id": 2,
      "title": "Motors",
      "image": "http://127.0.0.1:8000/media/categories/motors-categoty3x.png"
    },
    "price": 60000,
    "user": {
      "id": 1,
      "username": "daniel",
      "email": "daniel@pewpee.com",
      "first_name": "",
      "last_name": ""
    },
    "status": true
  },
  {
    "id": 7,
    "title": "Test",
    "image": "",
    "description": "",
    "category": {
      "id": 5,
      "title": "Sports",
      "image": "http://127.0.0.1:8000/media/categories/sports-categoty3x.png"
    },
    "price": 123,
    "user": {
      "id": 3,
      "username": "test",
      "email": "test@pewpee.com",
      "first_name": "",
      "last_name": ""
    },
    "status": false
  }
]
```