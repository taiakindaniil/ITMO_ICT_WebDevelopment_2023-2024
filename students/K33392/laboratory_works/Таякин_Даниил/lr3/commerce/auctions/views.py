from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def create(self, request: Request):
        request.data["user_id"] = request.user.pk
        listing = Listing()
        listing.__dict__.update(request.data)
        listing.save()
        serializer = ListingSerializer(listing)
        return Response(serializer.data)


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    def create(self, request: Request):
        request.data["user_id"] = request.user.pk
        watchlist = Watchlist()
        watchlist.__dict__.update(request.data)
        watchlist.save()
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def create(self, request: Request):
        request.data["user_id"] = request.user.pk
        bid = Bid()
        bid.__dict__.update(request.data)
        bid.save()
        serializer = BidSerializer(bid)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request: Request):
        request.data["user_id"] = request.user.pk
        comment = Comment()
        comment.__dict__.update(request.data)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class ListingCommentsViewSet(viewsets.ViewSet):
    def retrieve(self, req: Request, pk=None):
        queryset = Comment.objects.all().filter(listing=pk)
        if (page := req.query_params.get("page")) is not None:
            page, per_page = int(page), int(req.query_params.get("perPage", 2))
            queryset = queryset[page*per_page:page*per_page+per_page]
        serializer = ListingCommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request: Request):
        comment = Comment()
        comment.user = request.user
        comment.listing = get_object_or_404(Listing.objects.all(), pk=request.data["listing"])
        comment.comment = request.data["comment"]
        comment.rating = request.data["rating"]
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)