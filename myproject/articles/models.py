from django.db import models


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Article categories"

    def __str__(self):
        return self.name

class ArticleSubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Article subcategories"

    def __str__(self):
        return self.name


def article_upload_to(instance, filename: str) -> str:
    # Сохраняем файлы в media/articles/<article_id|new>/filename
    return f"articles/{instance.id or 'new'}/{filename}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        ArticleSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles"
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
