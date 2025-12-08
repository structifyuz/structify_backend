# myproject/myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # OpenAPI schema + Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('myproject.api_urls')),

    # CKEditor uploader
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Добавляем маршруты для загрузки файлов CKEditor
]

# Раздача медиа и статических файлов только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)