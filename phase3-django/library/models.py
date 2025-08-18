from django.db import models
from django.utils import timezone



class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'author'


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    isbn = models.CharField(unique=True, max_length=20, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    total_copies = models.IntegerField(blank=True, null=True)
    available_copies = models.IntegerField(blank=True, null=True)
    library = models.ForeignKey('Lib', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'book'


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, models.CASCADE, related_name='bookauthor')
    author = models.ForeignKey(Author, models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bookauthor'
        unique_together = (('book', 'author'),)


class BookCategory(models.Model):
    book = models.ForeignKey(Book, related_name='bookcategory', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bookcategory'
        unique_together = (('book', 'category'),)  # Enforce unique pairs instead of composite PK
        managed = True  # Or False if you don t want Django to manage the table



class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    late_fee = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'borrowing'



class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'


class Lib(models.Model):
    library_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    campus_location = models.CharField(max_length=50, blank=True, null=True)
    contact_email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'lib'


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    class MemberType(models.TextChoices):
        STUDENT = 'student', 'Student'
        FACULTY = 'faculty', 'Faculty'


    first_name = models.CharField(max_length=50, blank=True, default='Unknown')
    last_name = models.CharField(max_length=50, blank=True, default='Unknown')
    email = models.EmailField(default='test@example.com')
    phone = models.CharField(max_length=20, blank=True, default='0000000000')
    member_type = models.CharField(
        max_length=10,
        choices=MemberType.choices,
        default=MemberType.STUDENT
    )
    registration_date = models.DateField(default=timezone.now)



    class Meta:
        managed = True
        db_table = 'member'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'review'
        unique_together = (('member', 'book'),)
