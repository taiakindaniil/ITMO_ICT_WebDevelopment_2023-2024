from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)

    return render(request, "auctions/categories.html", {
        "category": category,
        "listings": category.listings.all()
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user

    if request.method == "POST" and request.POST.get("submit", False) != False:
        current_bid = int(request.POST["current_bid"] or listing.price)
        bid = int(request.POST["bid"])

        if current_bid < bid:
            new_bid = Bid(user=user, listing=listing, price=bid)
            new_bid.save()
    elif request.method == "POST" and request.POST.get("watchlist_button", False) != False:
        watchlist_value = request.POST.get("watchlist_button", False)
        if watchlist_value == "Add to Watchlist":
            watchlist = Watchlist(user=user, listing=listing)
            watchlist.save()
        else:
            for watch_listing in user.watchlist.all():
                if watch_listing.listing == listing:
                    watch_listing.delete()
    elif request.method == "POST" and request.POST.get("close_listing_button", False) != False:
        listing.status = False
        listing.save()
    elif request.method == "POST":
        comment_text = request.POST["comment"]
        rating = request.POST["rating"]
        comment = Comment(user=user, listing=listing, comment=comment_text, rating=rating)
        comment.save()

    added = None
    for watch_listing in user.watchlist.all():
        if watch_listing.listing == listing:
            added = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "added": "Remove from Watchlist" if added else "Add to Watchlist",
        "comments": listing.comments.all()
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc", None)
        url = request.POST.get("url", None)
        category_id = request.POST.get("category", None)
        price = request.POST.get("price")

        if category_id:
            category = Category.objects.get(pk=category_id)
            new_listing = Listing(title=title, description=desc, image=url, category=category, price=price, user=request.user)
            new_listing.save()
        else:
            new_listing = Listing(title=title, description=desc, image=url, price=price, user=request.user)
            new_listing.save()

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })

