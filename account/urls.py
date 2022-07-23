from django.urls import path
from account import views

urlpatterns = [
    path("register", views.RegisterAPIView.as_view(), name="register"),
]
