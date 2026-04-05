from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatabaseConnectionViewSet, StoredFileViewSet

router = DefaultRouter()
router.register(r'connections', DatabaseConnectionViewSet)
router.register(r'files', StoredFileViewSet, basename='storedfile')

urlpatterns = [
    path('', include(router.urls)),
]
