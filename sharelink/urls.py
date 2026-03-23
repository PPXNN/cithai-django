from rest_framework.routers import DefaultRouter
from .views import SharelinkViewSet

router = DefaultRouter()
router.register(r"sharelinks", SharelinkViewSet)

urlpatterns = router.urls