from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lib, Book, Author, Category, Member, Borrowing, Review
from .serializers import *

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Lib.objects.all()
    serializer_class = LibrarySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'location']
    ordering_fields = ['name']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'category']
    search_fields = ['title', 'author__first_name', 'author__last_name']
    ordering_fields = ['title', 'published_date']
    ordering = ['title']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nationality']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name']
    ordering = ['first_name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['member_type']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'registration_date']
    ordering = ['first_name']


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['member', 'book', 'borrow_date', 'return_date']
    search_fields = ['member__first_name', 'member__last_name', 'book__title']
    ordering_fields = ['borrow_date', 'return_date']
    ordering = ['-borrow_date']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'rating']
    search_fields = ['book__title', 'comment']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
