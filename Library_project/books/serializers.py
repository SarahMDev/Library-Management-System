from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(
        source='author',
        read_only=True
    )

    category_details = CategorySerializer(
        source='category',
        read_only=True
    )

    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_details',
            'category',
            'category_details',
            'isbn',
            'description',
            'published_date',
            'available_copies',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
   
    def validate_isbn(self, value):
        book = Book.objects.filter(isbn=value)

        if self.instance:
            book = book.exclude(pk=self.instance.pk)

        if book.exists():
            raise serializers.ValidationError(
                "A book with this isbn already exists."
            )

        return value


    def validate_available_copies(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Available copies must be greater than zero."
            )
        return value



        