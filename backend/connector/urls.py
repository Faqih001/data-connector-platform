from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DatabaseConnectionViewSet, StoredFileViewSet, extract_data_endpoint,
    login_view, logout_view, current_user, csrf_token_view, search_users
)

router = DefaultRouter()
router.register(r'connections', DatabaseConnectionViewSet)
router.register(r'files', StoredFileViewSet, basename='storedfile')

urlpatterns = [
    path('', include(router.urls)),
    path('extract/', extract_data_endpoint, name='extract-data'),
    path('csrf-token/', csrf_token_view, name='csrf-token'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', current_user, name='current-user'),
    path('search-users/', search_users, name='search-users'),
]
