from django.urls import path

from authentication.views import (CurrentUserView, CustomTokenObtainPairView,
                                  CustomTokenRefreshView, RegisterView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('current_user', CurrentUserView.as_view(), name="current_user"),
]
