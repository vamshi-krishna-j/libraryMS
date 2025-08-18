from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .filter import BorrowingFilter
from rest_framework.decorators import api_view
from rest_framework import status
from django.views import View
from datetime import date, timedelta
from .models import Lib, Book, Author, Category, Member, Borrowing, Review
from .serializers import (
    LibrarySerializer,
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    MemberSerializer,
    BorrowingSerializer,
    ReviewSerializer,

)
from .filter import BookFilter
# Swagger decorators and tools
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom request serializers
from .serializers import BorrowBookSerializer, ReturnBookSerializer



# ------------------ Standard CRUD ViewSets ------------------

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Lib.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'campus_location']
    ordering_fields = ['name']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'bookauthor__author__first_name', 'bookcategory__category__name']
    ordering_fields = ['title', 'publication_date']
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
    filterset_class = BorrowingFilter
    search_fields = ['member__first_name', 'member__last_name', 'book__title']
    ordering_fields = ['borrow_date', 'return_date']
    ordering = ['borrow_date']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'rating']
    search_fields = ['book__title', 'comment']
    ordering_fields = ['rating', 'review_date']
    ordering = ['-review_date']


# ------------------ Custom API Views ------------------

# class BookSearchView(generics.ListAPIView):
#     serializer_class = BookSerializer
#
#     def get_queryset(self):
#         query = self.request.query_params.get("q", "")
#         return Book.objects.filter(
#             Q(title__icontains=query) |
#             Q(author__first_name__icontains=query) |
#             Q(author__last_name__icontains=query) |
#             Q(category__name__icontains=query)
#         )
class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Search by title or ISBN",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.query_params.get("search", "")
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(isbn__icontains=query)
            )
        else:
            return Book.objects.all()
# class MemberBorrowingHistoryView(generics.ListAPIView):
#     serializer_class = BorrowingSerializer
#
#     def get_queryset(self):
#         member_id = self.kwargs['id']
#         return Borrowing.objects.filter(member_id=member_id).order_by('-borrow_date')
#
class MemberBorrowingHistoryView(generics.ListAPIView):
    serializer_class = BorrowingSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'member_id', openapi.IN_PATH, description="Member ID", type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get_queryset(self):
        member_id = self.kwargs['member_id']
        return Borrowing.objects.filter(member_id=member_id).order_by('-borrow_date')




# class BookAvailabilityView(APIView):
#     def get(self, request, book_id):
#         book = get_object_or_404(Book, book_id=book_id)
#         available_copies = max(book.available_copies or 0, 0)  # safer to use available_copies field
#         available = available_copies > 0
#         return Response({
#             'available': available,
#             'available_copies': available_copies
#         })

class BookAvailabilityView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('book_id', openapi.IN_PATH, description="Book ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: "Availability info"}
    )
    def get(self, request, book_id):
        book = get_object_or_404(Book, book_id=book_id)
        available_copies = max(book.available_copies or 0, 0)
        available = available_copies > 0
        return Response({
            'available': available,
            'available_copies': available_copies
        })


# class BorrowBookView(APIView):
#     def post(self, request):
#         book_id = request.data.get('book_id')
#         member_id = request.data.get('member_id')
#
#         if not book_id or not member_id:
#             return Response({'error': 'Missing book_id or member_id'}, status=status.HTTP_400_BAD_REQUEST)
#
#         book = get_object_or_404(Book, book_id=book_id)  # Fix here
#         member = get_object_or_404(Member, member_id=member_id)  # Fix here if needed
#
#         if book.available_copies <= 0:
#             return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if Borrowing.objects.filter(book=book, member=member, return_date__isnull=True).exists():
#             return Response({'error': 'This member already borrowed this book and has not returned it.'}, status=HTTP_400_BAD_REQUEST)
#
#         borrow_date = date.today()
#         due_date = borrow_date + timedelta(days=14)
#
#         Borrowing.objects.create(
#             book=book,
#             member=member,
#             borrow_date=borrow_date,
#             due_date=due_date
#         )
#
#         book.available_copies -= 1
#         book.save()
#
#         return Response({'message': 'Book borrowed successfully', 'available_copies': book.available_copies}, status=status.HTTP_200_OK)

class BorrowBookView(APIView):

    @swagger_auto_schema(
        request_body=BorrowBookSerializer,
        responses={
            200: "Book borrowed successfully",
            400: "Validation or availability error"
        }
    )
    def post(self, request):
        serializer = BorrowBookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        book_id = serializer.validated_data['book_id']
        member_id = serializer.validated_data['member_id']

        book = get_object_or_404(Book, book_id=book_id)
        member = get_object_or_404(Member, member_id=member_id)

        if book.available_copies <= 0:
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)

        if Borrowing.objects.filter(book=book, member=member, return_date__isnull=True).exists():
            return Response({'error': 'This member already borrowed this book and has not returned it.'}, status=status.HTTP_400_BAD_REQUEST)

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14)

        Borrowing.objects.create(
            book=book,
            member=member,
            borrow_date=borrow_date,
            due_date=due_date
        )

        book.available_copies -= 1
        book.save()

        return Response({'message': 'Book borrowed successfully', 'available_copies': book.available_copies}, status=status.HTTP_200_OK)



# class ReturnBookView(APIView):
#     def post(self, request):
#         book_id = request.data.get('book_id')
#         member_id = request.data.get('member_id')
#
#         if not book_id or not member_id:
#             return Response({'error': 'Missing book_id or member_id'}, status=400)
#
#         borrowing = Borrowing.objects.filter(
#             book_id=book_id,
#             member_id=member_id,
#             return_date__isnull=True
#         ).first()
#
#         if not borrowing:
#             return Response({'error': 'No active borrowing found'}, status=400)
#
#         borrowing.return_date = timezone.now()
#         borrowing.save()
#
#         book = borrowing.book
#         book.available_copies +=1
#         book.save()
#
#         return Response({'message': 'Book returned successfully', 'available_copies': book.available_copies}, status=status.HTTP_200_OK)


class ReturnBookView(APIView):

    @swagger_auto_schema(
        request_body=ReturnBookSerializer,
        responses={
            200: "Book returned successfully",
            400: "Validation or borrowing not found"
        }
    )
    def post(self, request):
        serializer = ReturnBookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        book_id = serializer.validated_data['book_id']
        member_id = serializer.validated_data['member_id']

        borrowing = Borrowing.objects.filter(
            book_id=book_id,
            member_id=member_id,
            return_date__isnull=True
        ).first()

        if not borrowing:
            return Response({'error': 'No active borrowing found'}, status=400)

        borrowing.return_date = timezone.now()
        borrowing.save()

        book = borrowing.book
        book.available_copies += 1
        book.save()

        return Response({'message': 'Book returned successfully', 'available_copies': book.available_copies}, status=status.HTTP_200_OK)


# class StatisticsView(APIView):
#     def get(self, request):
#         total_books = Book.objects.count()
#         total_members = Member.objects.count()
#         total_borrowings = Borrowing.objects.count()
#         currently_borrowed = Borrowing.objects.filter(return_date__isnull=True).count()
#
#         return Response({
#             'total_books': total_books,
#             'total_members': total_members,
#             'total_borrowings': total_borrowings,
#             'currently_borrowed': currently_borrowed
#         })

class StatisticsView(APIView):

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Library statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_books': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Total number of books',
                            example=100
                        ),
                        'total_members': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Total number of members',
                            example=50
                        ),
                        'total_borrowings': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Total number of borrowings',
                            example=120
                        ),
                        'currently_borrowed': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Currently borrowed books count',
                            example=30
                        ),
                    }
                )
            )
        }
    )
    def get(self, request):
        total_books = Book.objects.count()
        total_members = Member.objects.count()
        total_borrowings = Borrowing.objects.count()
        currently_borrowed = Borrowing.objects.filter(return_date__isnull=True).count()

        return Response({
            'total_books': total_books,
            'total_members': total_members,
            'total_borrowings': total_borrowings,
            'currently_borrowed': currently_borrowed
        })

# @api_view(['POST'])
# def borrow_book(request):
#     book_id = request.data.get('book_id')
#     member_id = request.data.get('member_id')
#
#     try:
#         book = Book.objects.get(pk=book_id)
#         member = Member.objects.get(pk=member_id)
#     except (Book.DoesNotExist, Member.DoesNotExist):
#         return Response({"error": "Book or Member not found."}, status=status.HTTP_404_NOT_FOUND)
#
#     # Check if book is already borrowed (no return date)
#     if Borrowing.objects.filter(book=book, return_date__isnull=True).exists():
#         return Response({"error": "Book is currently not available."}, status=status.HTTP_400_BAD_REQUEST)
#
#     borrowing = Borrowing.objects.create(
#         book=book,
#         member=member,
#         borrow_date=timezone.now().date(),
#         due_date=timezone.now().date() + timezone.timedelta(days=14)  # due in 2 weeks
#     )
#     return Response({"message": "Book borrowed successfully", "borrowing_id": borrowing.borrowing_id})

# @api_view(['POST'])
# def return_book(request):
#     borrowing_id = request.data.get('borrowing_id')
#
#     try:
#         borrowing = Borrowing.objects.get(pk=borrowing_id)
#     except Borrowing.DoesNotExist:
#         return Response({"error": "Borrowing record not found."}, status=status.HTTP_404_NOT_FOUND)
#
#     if borrowing.return_date:
#         return Response({"error": "Book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)
#
#     borrowing.return_date = timezone.now().date()
#
#     # Calculate late fee if any
#     if borrowing.return_date > borrowing.due_date:
#         late_days = (borrowing.return_date - borrowing.due_date).days
#         borrowing.late_fee = late_days * 1.0  # $1 per late day (example)
#     else:
#         borrowing.late_fee = 0.0
#
#     borrowing.save()
#     return Response({"message": "Book returned successfully", "late_fee": borrowing.late_fee})
#
# from rest_framework.decorators import api_view
# from django.db.models import Count, Q
#
# @api_view(['GET'])
# def library_statistics(request):
#     total_books = Book.objects.count()
#     total_members = Member.objects.count()
#     borrowed_books = Borrowing.objects.filter(return_date__isnull=True).count()
#     late_returns = Borrowing.objects.filter(return_date__gt=F('due_date')).count()
#
#     return Response({
#         "total_books": total_books,
#         "total_members": total_members,
#         "currently_borrowed_books": borrowed_books,
#         "late_returns": late_returns
#     })
