import uuid

from django.db import models


def book_pdf_upload_to(instance, filename: str) -> str:
    ext = filename.split(".")[-1]
    return f"books/pdfs/{uuid.uuid4()}.{ext}"


def book_cover_upload_to(instance, filename: str) -> str:
    ext = filename.split(".")[-1]
    return f"books/covers/{uuid.uuid4()}.{ext}"


class BookCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Book categories"

    def __str__(self):
        return self.name


class BookSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Book subcategories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    published_date = models.DateField()
    pdf_file = models.FileField(upload_to=book_pdf_upload_to, null=True, blank=True)
    cover = models.ImageField(upload_to=book_cover_upload_to, null=True, blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sub_category = models.ForeignKey(
        BookSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )

    def __str__(self):
        return self.title
