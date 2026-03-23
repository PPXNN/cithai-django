from rest_framework.routers import DefaultRouter
from .views import SongViewSet

router = DefaultRouter()
router.register(r"songs", SongViewSet)

urlpatterns = router.urls