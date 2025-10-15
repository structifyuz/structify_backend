"""
URL configuration for the API layer of myapp.
This file defines API endpoints using Django REST Framework router and custom views.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapp.views import (
    ForumViewSet,
    CommentViewSet,
    BookViewSet,
    ArticleViewSet,
    UserViewSet,
    RegisterView,
    CategoryViewSet,
    ArticlesReportJSON,
    ArticlesReportCSV,
    serve_protected_file, ArticleAttachmentUploadView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Инициализация роутера для автоматической генерации URL
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'forums', ForumViewSet, basename='forum')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'articles', ArticleViewSet, basename='article')

# Определение URL-паттернов
urlpatterns = [
    # Включение автоматически сгенерированных маршрутов из роутера
    path('', include(router.urls)),
    # Регистрация нового пользователя
    path('register/', RegisterView.as_view(), name='register'),
    # JWT токены: получение и обновление
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Обслуживание защищенных файлов (должен поддерживать GET, но не вмешиваться в POST админки)
    path('protected-file/<path:file_path>/', serve_protected_file, name='serve_protected_file'),
    # Отчеты
    path('file/upload/', ArticleAttachmentUploadView.as_view(), name='file_upload'),
    path('reports/articles/', ArticlesReportJSON.as_view(), name='articles_report_json'),
    path('reports/articles.csv', ArticlesReportCSV.as_view(), name='articles_report_csv'),
]

# Примечание: Убедитесь, что функция serve_protected_file в views.py поддерживает только GET-запросы
# и не конфликтует с маршрутами админки (обычно /admin/).