from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles.views import (
    ArticleViewSet, ArticleAttachmentUploadView, ArticleCategoryViewSet, ArticleSubCategoryViewSet
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'article-categories', ArticleCategoryViewSet, basename='article-categories')
router.register(r'article-subcategories', ArticleSubCategoryViewSet, basename='article-subcategories')

urlpatterns = [
    path('', include(router.urls)),
    path('file/upload/', ArticleAttachmentUploadView.as_view(), name='file_upload'),
]
