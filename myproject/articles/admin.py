from django.contrib import admin

from articles.models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'sub_category', 'created_at', 'updated_at')
    list_filter = ('sub_category', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author', 'sub_category')
    readonly_fields = ('created_at', 'updated_at')