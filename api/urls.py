from django.urls import path

from api.views import RegisterView
from expense import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("transactions/", views.TransactionList.as_view(), name="transactions-list"),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetail.as_view(),
        name="transactions-detail",
    ),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
