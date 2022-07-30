from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register", views.RegisterAPIView.as_view(), name="register"),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("detail", views.DetailAPIView.as_view(), name="user_detail"),
    path("update", views.UpdateAPIView.as_view(), name="user_update"),
    path("change-auth", views.ChangeAuthView.as_view(), name="change_auth")
]
