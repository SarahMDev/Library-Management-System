from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Book, Author, Category
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'published_date', 'created_at']
    ordering = ['id']

    def get_queryset(self):
        queryset = Book.objects.select_related(
            'author', 'category'
        ).all()

        author_id = self.request.query_params.get('author')
        category_id = self.request.query_params.get('category')

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'birth_date']
    ordering = ['id']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['id']
