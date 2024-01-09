from rest_framework import serializers
from auctions.models import *
from django.contrib.auth.hashers import make_password


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
        model = Bid
        fields = ("id", "user", "listing", "price")


class CommentSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    listing = ListingSerializer()
    class Meta:
        model = Comment
        fields = ("id", "user", "listing", "comment", "rating")
