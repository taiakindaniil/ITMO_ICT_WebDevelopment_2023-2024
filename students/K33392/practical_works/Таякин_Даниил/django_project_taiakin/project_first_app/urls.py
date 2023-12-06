from django.urls import path 
from . import views
urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail),
    path('owners/', views.owner_list),
    path('car/<int:pk>/', views.CarRetrieveView.as_view()),
    path('cars/', views.CarList.as_view())
]