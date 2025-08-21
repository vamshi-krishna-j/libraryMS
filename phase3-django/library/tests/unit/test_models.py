import pytest
from datetime import date, timedelta
from library.models import (
    Author, Book, Category, Lib, Member, Borrowing, Review
)

@pytest.mark.django_db
def test_create_author():
    author = Author.objects.create(
        first_name="Jane",
        last_name="Doe",
        birth_date="1980-01-01",
        nationality="American"
    )
    assert author.author_id is not None
    assert author.first_name == "Jane"

@pytest.mark.django_db
def test_create_book():
    library = Lib.objects.create(name="Main Library")
    book = Book.objects.create(
        title="Django Testing",
        isbn="1234567890123",
        publication_date="2022-01-01",
        total_copies=10,
        available_copies=5,
        library=library
    )
    assert book.book_id is not None
    assert book.available_copies <= book.total_copies

@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(
        category_id=1,
        name="Programming",
        description="Books about programming"
    )
    assert category.category_id == 1
    assert category.name == "Programming"

@pytest.mark.django_db
def test_create_member():
    member = Member.objects.create(
        first_name="Alice",
        last_name="Smith",
        email="alice@gmail.com",
        phone="1234567890",
        member_type=Member.MemberType.STUDENT
    )
    assert member.member_id is not None
    assert member.email.endswith("@gmail.com")

@pytest.mark.django_db
def test_create_borrowing():
    lib = Lib.objects.create(name="Science Library")
    book = Book.objects.create(
        title="Science Book",
        total_copies=5,
        available_copies=3,
        library=lib
    )
    member = Member.objects.create(
        first_name="Bob",
        last_name="Brown",
        email="bob@gmail.com",
        phone="9876543210"
    )
    borrowing = Borrowing.objects.create(
        book=book,
        member=member,
        borrow_date=date.today(),
        due_date=date.today() + timedelta(days=14)
    )
    assert borrowing.borrowing_id is not None
    assert borrowing.due_date > borrowing.borrow_date

@pytest.mark.django_db
def test_create_review():
    lib = Lib.objects.create(name="Review Library")
    book = Book.objects.create(
        title="Review Book",
        total_copies=3,
        available_copies=2,
        library=lib
    )
    member = Member.objects.create(
        first_name="Chris",
        last_name="Green",
        email="chris@gmail.com",
        phone="1112223333"
    )
    review = Review.objects.create(
        member=member,
        book=book,
        rating=4,
        comment="Great book!"
    )
    assert review.review_id is not None
    assert 1 <= review.rating <= 5
