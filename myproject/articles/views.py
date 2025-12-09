import os

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import parsers, status, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import ArticleFileAttachment, Article, ArticleSubCategory, ArticleCategory
from articles.serializers import ArticleSerializer, ArticleCategorySerializer, ArticleSubCategorySerializer
from articles.services import mark_article_attachment_files_as_used
from base.api_views import DefaultPagination
from utils.drf_spectacular_utils import ordering_parameter


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer


class ArticleSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArticleSubCategory.objects.select_related('category').all()
    serializer_class = ArticleSubCategorySerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('category',)

@extend_schema(parameters=[ordering_parameter(['created_at', 'title'])])
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("sub_category", "author").all().order_by("-created_at")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = ('sub_category', 'author')
    ordering_fields = ('created_at', 'title')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.save(author=request.user)
        mark_article_attachment_files_as_used(article.content)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        article = serializer.save()
        mark_article_attachment_files_as_used(article.content)


class ArticleAttachmentUploadView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file-0')
        if not uploaded_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        attachment = ArticleFileAttachment.objects.create(file=uploaded_file)

        return Response({
            "errorMessage": "",
            "result": [
                {
                    # "id": attachment.id,
                    "url": attachment.file.url,
                    "name": os.path.basename(attachment.file.name),
                    "size": f"{attachment.file.size}",
                }
            ]
        }, status=status.HTTP_201_CREATED)
