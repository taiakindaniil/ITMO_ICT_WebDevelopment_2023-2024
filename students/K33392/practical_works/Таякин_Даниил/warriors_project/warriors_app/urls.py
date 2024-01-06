from django.urls import path
from .views import *


app_name = "warriors_app"


urlpatterns = [
    path('warriors/', WarriorsAPIView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    path("skills/<int:warrior_pk>", SkillOfWarriorAPIView.as_view()),
    path("warrior/<int:pk>", WarriorAPIView.as_view()),
]