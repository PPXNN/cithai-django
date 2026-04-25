from django.urls import path
from .views import AuthSignInAPIView, AuthSignUpAPIView, UserAPIView

app_name = "user"

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<int:pk>/', UserAPIView.as_view()),
    path("auth/signup/", AuthSignUpAPIView.as_view()),
    path("auth/signin/", AuthSignInAPIView.as_view()),
]