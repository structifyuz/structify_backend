from django.contrib import admin

from books.models import Book, BookSubCategory, BookCategory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "created_by", "created_at")
    list_filter = ("created_at", "created_by")
    search_fields = ("title", "author", "isbn")
    raw_id_fields = ("created_by",)
    readonly_fields = ("created_at",)


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(BookSubCategory)
class BookSubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
