from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# ======= Форумы / Комментарии =======

class Forum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.forum.title}"


# ======= Книги =======

def book_pdf_upload_to(instance, filename: str) -> str:
    # Сохраняем PDF-файлы в media/books/pdfs/<book_id|new>/filename
    return f"books/pdfs/{instance.id or 'new'}/{filename}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)  # Сделано необязательным
    published_date = models.DateField()
    pdf_file = models.FileField(upload_to=book_pdf_upload_to, null=True, blank=True)  # Добавлено поле для PDF
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ======= Категории и Статьи =======

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


def article_upload_to(instance, filename: str) -> str:
    # Сохраняем файлы в media/articles/<article_id|new>/filename
    return f"articles/{instance.id or 'new'}/{filename}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ArticleFileAttachment(models.Model):
    file = models.FileField(upload_to='article_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        path = self.file.path
        super().delete(*args, **kwargs)
        if storage.exists(path):
            storage.delete(path)