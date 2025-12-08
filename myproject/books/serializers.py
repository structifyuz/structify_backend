from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from base.serializers import PDFBase64File
from books.models import Book, BookCategory, BookSubCategory
from users.serializers import UserSerializer


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ['id', 'name']


class BookSubCategorySerializer(serializers.ModelSerializer):
    category = BookCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BookCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = BookSubCategory
        fields = ['id', 'name', 'category', 'category_id']


class BookSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "author",
            "pdf_file",
            "cover",
            "isbn",
            "published_date",
            "created_by",
            "created_at"
        )


class BookCreateSerializer(serializers.ModelSerializer):
    pdf_file = PDFBase64File(allow_empty_file=False, allow_null=False, required=True)
    cover = Base64ImageField(allow_empty_file=False, allow_null=False, required=False)

    class Meta:
        model = Book
        fields = (
            "title",
            "description",
            "author",
            "isbn",
            "pdf_file",
            "cover",
            "published_date",
            "created_by",
            "created_at"
        )
        extra_kwargs = {
            "created_by": {"read_only": True},
            "created_at": {"read_only": True},
        }
