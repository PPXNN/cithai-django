from django.urls import path
from .views import SharelinkViewSet

app_name = "sharelinks"

urlpatterns = [
    path('', SharelinkViewSet.as_view()),
    path('<int:pk>/', SharelinkViewSet.as_view())
]