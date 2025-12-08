from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from base.api_views import MultiSerializerViewSetMixin, DefaultPagination
from base.helpers import extract_first_page_of_pdf_as_image
from books.models import Book, BookCategory, BookSubCategory
from books.serializers import BookSerializer, BookCreateSerializer, BookCategorySerializer, BookSubCategorySerializer
from utils.drf_spectacular_utils import ordering_parameter


class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer


class BookSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookSubCategory.objects.select_related('category').all()
    serializer_class = BookSubCategorySerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('category',)

@extend_schema(parameters=[ordering_parameter(['created_at', 'title'])])
class BookViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    serializer_action_classes = {
        'create': BookCreateSerializer,
    }
    pagination_class = DefaultPagination
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = ('sub_category', 'created_by')
    ordering_fields = ('created_at', 'title')

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        book = serializer.save(created_by=self.request.user)

        if not book.cover and book.pdf_file:
            try:
                filename, content = extract_first_page_of_pdf_as_image(book.pdf_file.path)
                book.cover.save(filename, content, save=True)
            except Exception:
                pass
