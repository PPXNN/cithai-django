from django.urls import path
from .views import SongViewSet

app_name = "song"

urlpatterns = [
    path('', SongViewSet.as_view()),
    path('<int:pk>/', SongViewSet.as_view())
]