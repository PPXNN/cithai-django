from django.urls import path
from .views import UserAPIView

app_name = "user"

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<int:pk>/', UserAPIView.as_view())
]