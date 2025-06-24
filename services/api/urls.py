from rest_framework.routers import DefaultRouter
from .viewsets import ServiceViewSet, ClientViewSet, RequestViewSet, UserViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
