# Лабораторная работа #2

## Задание
Свой вариант. Реализовать веб сервис аукционов. Необходимо реализовать следующий функционал:

- Регистрация новых пользоватлей.
- Просмотр активных аукионов.
- Создание аукицона пользователями.
- Написание отзывов к ацкуионам.
- Создание watchlist'а.

## Реализация

### Создание проекта
Для начала создаем виртуальную среду, устанавливаем Django и создаем проект.
```python
python3 -m venv commerce-venv
pip3 install django
django-admin starproject commerce
```

После создания, добавляем в проект приложение auctions.
```python
./manage.py startapp auctions
```

### Создание базы данных
Модель `User` используется для авторизации пользователей.
```python
class User(AbstractUser):
	pass
```

Для того, чтобы Django использовал данную модель для регистрации и входа необходимо в `settings.py` добавить строку:
```python
AUTH_USER_MODEL = 'auctions.User'
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

### url конфигурация

Создаем файл `urls.py` со следующим кодом в папке нашего приложения `auctions`. Помимо указаний всех `path`, прописываем путь к статичным файлам (медиа файлам).
```python
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/create", views.create_listing, name="create_listing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Для того, чтобы работала данная url конфигурация, в файле `commerce/urls.py` прописываем urlpatterns так:
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auctions.urls"))
]
```