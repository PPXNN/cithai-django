from django.urls import path
from .views import AuthGoogleAPIView, AuthGoogleRedirectAPIView, AuthMeAPIView, AuthSignInAPIView, AuthSignOutAPIView, AuthSignUpAPIView, UserAPIView

app_name = "user"

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<int:pk>/', UserAPIView.as_view()),
    path("auth/signup/", AuthSignUpAPIView.as_view()),
    path("auth/me/", AuthMeAPIView.as_view()),
    path("auth/signin/", AuthSignInAPIView.as_view()),
    path("auth/signout/", AuthSignOutAPIView.as_view()),
    path("auth/google/", AuthGoogleAPIView.as_view()),
    path("auth/google/redirect/", AuthGoogleRedirectAPIView.as_view()),
]