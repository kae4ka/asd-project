from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EtlTaskManagerViewSet

router = DefaultRouter()
router.register(r'etl-task', EtlTaskManagerViewSet, basename='etl-task')

urlpatterns = [
    path('', include(router.urls)),
]
