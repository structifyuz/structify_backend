from rest_framework import serializers

from articles.models import ArticleCategory, Article, ArticleSubCategory
from users.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "name")


class ArticleSubCategorySerializer(serializers.ModelSerializer):
    category = ArticleCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ArticleCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = ArticleSubCategory
        fields = ("id", "name", "category", "category_id")


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    sub_category = ArticleSubCategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",
            "sub_category",
        )
