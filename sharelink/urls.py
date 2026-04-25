from django.urls import path
from .views import SharelinkViewSet, public_sharelink_redirect

app_name = "sharelinks"

urlpatterns = [
    path('', SharelinkViewSet.as_view()),
    path('<int:pk>/', SharelinkViewSet.as_view()),
    path("public/<int:pk>/", public_sharelink_redirect, name="public_sharelink"),
]