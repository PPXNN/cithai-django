from django.urls import path
from .views import SongGenerationRequestViewSet, SongGenerationRequestStatusViewSet

app_name = "song_generation_requests"

urlpatterns = [
    path('', SongGenerationRequestViewSet.as_view()),
    path('<int:pk>/', SongGenerationRequestViewSet.as_view()),
    path('status/<str:taskId>/<int:userId>', SongGenerationRequestStatusViewSet.as_view()),
]