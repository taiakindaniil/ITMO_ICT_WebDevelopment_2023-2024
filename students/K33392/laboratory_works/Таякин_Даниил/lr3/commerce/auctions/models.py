from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
	pass


class Category(models.Model):
	title = models.CharField(max_length=64)
	image = models.ImageField(upload_to="media/categories", blank=True, null=True)

	def __str__(self):
		return self.title


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


class Watchlist(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist")
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.id}. {self.user.username}: {self.listing.title}"


class Bid(models.Model):
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
	listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")
	price = models.IntegerField()

	def __str__(self):
		return f"{self.id}. {self.user.username} bid {self.listing.title} for {self.price}"


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
