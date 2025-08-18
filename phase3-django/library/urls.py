from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import BorrowBookView

from .views import (
    LibraryViewSet,
    BookViewSet,
    AuthorViewSet,
    CategoryViewSet,
    MemberViewSet,
    BorrowingViewSet,
    ReviewViewSet,
    BookSearchView,
    MemberBorrowingHistoryView,
    BookAvailabilityView,
    BorrowBookView,
    ReturnBookView,
    StatisticsView,
)

router = DefaultRouter()
router.register(r'libraries', LibraryViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'members', MemberViewSet)
router.register(r'borrowings', BorrowingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Custom API endpoints
    path('api/books/search/', BookSearchView.as_view(), name='book-search'),
    path('api/members/<int:member_id>/borrowings/', MemberBorrowingHistoryView.as_view(), name='member-borrowing-history'),
    path('api/books/<int:book_id>/availability/', BookAvailabilityView.as_view(), name='book-availability'),
    path('api/books/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('api/books/return/', ReturnBookView.as_view(), name='return-book'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics')

]
