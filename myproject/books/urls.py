from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import BookViewSet, BookCategoryViewSet, BookSubCategoryViewSet

router = DefaultRouter()

router.register(r'books', BookViewSet, basename='books')
router.register(r'book-categories', BookCategoryViewSet, basename='book-categories')
router.register(r'book-subcategories', BookSubCategoryViewSet, basename='book-subcategories')

urlpatterns = [
    path('', include(router.urls)),
]