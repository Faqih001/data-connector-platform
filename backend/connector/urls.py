from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatabaseConnectionViewSet, ExtractDataView, submit_data

router = DefaultRouter()
router.register(r'connections', DatabaseConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('extract/', ExtractDataView.as_view(), name='extract_data'),
    path('submit/', submit_data, name='submit_data'),
]
