from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScriptManagerViewSet

router = DefaultRouter()
router.register(r'scripts', ScriptManagerViewSet, basename='scripts')

urlpatterns = [
    path('', include(router.urls)),
]
