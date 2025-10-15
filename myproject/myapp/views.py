from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse, FileResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
import os
from rest_framework import viewsets, parsers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from myapp.models import Forum, Comment, Book, Article, Category, ArticleFileAttachment
from myapp.serializers import (
    ForumSerializer, CommentSerializer, BookSerializer, ArticleSerializer,
    UserSerializer, RegisterSerializer, CategorySerializer
)
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv

from myapp.services import mark_article_attachment_files_as_used


# ======= Пользователи =======

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======= Форумы / Комментарии =======

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all().order_by("-created_at")
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ======= Книги =======

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]  # Только администраторы могут создавать, обновлять или удалять
        return [IsAuthenticatedOrReadOnly()]  # Чтение доступно всем авторизованным

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ======= Категории =======

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ======= Статьи (с файлом и категорией) =======

class ArticleAttachmentUploadView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file-0')
        if not uploaded_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        attachment = ArticleFileAttachment.objects.create(file=uploaded_file)

        return Response({
            "errorMessage": "",
            "result": {
                "id": attachment.id,
                "url": attachment.file.url,
                "name": os.path.basename(attachment.file.name),
                "size": attachment.file.size,
            }
        }, status=status.HTTP_201_CREATED)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("category", "author").all().order_by("-created_at")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.save()
        mark_article_attachment_files_as_used(article.content)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        article = serializer.save()
        mark_article_attachment_files_as_used(article.content)


# ======= Отчёты =======

class ArticlesReportJSON(APIView):
    """
    Сводка: всего статей, сколько с прикреплённым файлом,
    и разрез по категориям.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        by_cat = (
            Category.objects
            .annotate(
                total=Count("articles"),
                with_file=Count("articles", filter=Q(articles__file__isnull=False))
            )
            .values("id", "name", "total", "with_file")
            .order_by("name")
        )
        summary = {
            "total_articles": Article.objects.count(),
            "with_file": Article.objects.filter(file__isnull=False).count(),
        }
        return JsonResponse({"summary": summary, "by_category": list(by_cat)})


class ArticlesReportCSV(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="articles_report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Category", "Total", "With File"])
        rows = Category.objects.annotate(
            total=Count("articles"),
            with_file=Count("articles", filter=Q(articles__file__isnull=False))
        ).order_by("name")
        for r in rows:
            writer.writerow([r.name, r.total, r.with_file])
        return response


# ======= Защищённое обслуживание файлов =======

def serve_protected_file(request, file_path):
    if not request.user.is_authenticated or not request.user.is_staff:
        raise PermissionDenied("Доступ запрещен")
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        # Отправка файла как вложения для предотвращения прямого просмотра
        return FileResponse(open(full_path, 'rb'), as_attachment=True)
    raise FileNotFoundError("Файл не найден")
