from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Forum, Comment, Book, Article, Category


# ======= Users =======

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# ======= Forum / Comment =======

class ForumSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Forum
        fields = ("id", "title", "description", "created_by", "created_at", "updated_at")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "forum", "user", "content", "created_at", "updated_at")


# ======= Books =======

class BookSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "isbn", "published_date", "created_by", "created_at")


# ======= Categories / Articles =======

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "author",
            "category",
            "created_at",
            "updated_at",
        )
