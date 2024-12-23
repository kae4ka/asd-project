from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="ETL-TASK Manager API",
      default_version='v1',
      description="API документация для ETL-TASK Manager",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@etl.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('etl-express-project/etl_task_manager/admin/', admin.site.urls),
    path('etl-express-project/etl_task_manager/api/', include('api.urls')),
    path('etl-express-project/etl_task_manager/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('etl-express-project/etl_task_manager/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]