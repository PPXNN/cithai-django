from rest_framework.routers import DefaultRouter
from .views import SongGenerationRequestViewSet

router = DefaultRouter()
router.register(r"song-generation-requests", SongGenerationRequestViewSet)

urlpatterns = router.urls