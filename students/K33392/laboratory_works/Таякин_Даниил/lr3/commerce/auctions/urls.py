from rest_framework.routers import DefaultRouter
from djoser.views import *
from .views import *


r = DefaultRouter()
r.register('users', UserViewSet)
r.register('categories', CategoryViewSet)
r.register('listings', ListingViewSet)
r.register('watchlists', WatchlistViewSet)
r.register('bids', BidViewSet)
r.register('comments', CommentViewSet)

urlpatterns = r.urls
