import django_filters
from .models import Book
from .models import Borrowing


class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='bookauthor__author__first_name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='bookcategory__category__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'category']


class BorrowingFilter(django_filters.FilterSet):
    member_first_name = django_filters.CharFilter(field_name='member__first_name', lookup_expr='icontains')
    member_last_name = django_filters.CharFilter(field_name='member__last_name', lookup_expr='icontains')
    book_title = django_filters.CharFilter(field_name='book__title', lookup_expr='icontains')
    borrow_date = django_filters.DateFromToRangeFilter()
    return_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Borrowing
        fields = ['member_first_name', 'member_last_name', 'book_title', 'borrow_date', 'return_date']

