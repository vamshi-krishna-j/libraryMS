import pytest
from library.serializers import (
    BorrowingSerializer,
    CategorySerializer,
    AuthorSerializer,
)
from datetime import timedelta
from library.models import Book, Member
from django.utils import timezone
from datetime import date



@pytest.mark.django_db
def test_borrowing_serializer_valid_dates():
    member = Member.objects.create(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    book = Book.objects.create(title="Sample", total_copies=5, available_copies=2)

    data = {
        "book": book.book_id,
        "member": member.member_id,
        "borrow_date": str(date.today()),
        "due_date": str(date.today() + timedelta(days=7))
    }

    serializer = BorrowingSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_borrowing_serializer_invalid_dates():
    member = Member.objects.create(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    book = Book.objects.create(title="Sample", total_copies=5, available_copies=2)

    data = {
        "book": book.book_id,
        "member": member.member_id,
        "borrow_date": str(date.today()),
        "due_date": str(date.today() - timedelta(days=1))  # Invalid: due before borrow
    }

    serializer = BorrowingSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_category_serializer_valid():
    data = {
        "category_id": 1,
        "name": "Fiction",
        "description": "Fiction books"
    }
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_author_serializer_invalid_birth_date():
    future_date = date.today() + timedelta(days=10)
    data = {
        "first_name": "Mark",
        "last_name": "Twain",
        "birth_date": future_date,
        "nationality": "American"
    }
    serializer = AuthorSerializer(data=data)
    assert not serializer.is_valid()
    assert "birth_date" in serializer.errors
