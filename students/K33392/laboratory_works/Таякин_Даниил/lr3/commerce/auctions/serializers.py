from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
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
    category = CategorySerializer(read_only=True)
    user = MyUserSerializer(read_only=True)
    class Meta:
        model = Listing
        fields = ("id", "title", "image", "description", "category", "price", "user", "status")


class WatchlistSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    class Meta:
        model = Watchlist
        fields = ("id", "user", "listing")


class BidSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ("id", "user", "listing", "price")


class CommentSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("id", "user", "listing", "comment", "rating")


class ListingCommentSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("id", "user", "comment", "rating")