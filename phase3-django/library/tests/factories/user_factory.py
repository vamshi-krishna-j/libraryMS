import factory
from library.models import Member, Book, Lib, Category, Author
from faker import Faker

fake = Faker()

class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda _: fake.email().replace("@", "@gmail.com"))
    phone = "1234567890"
    member_type = "student"


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    isbn = factory.Faker("isbn13")
    total_copies = 5
    available_copies = 3


class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lib

    name = factory.Faker("company")
    campus_location = factory.Faker("city")
    contact_email = factory.Faker("email")
    phone_number = "1112223333"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("word")
    description = factory.Faker("sentence")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth")
    nationality = factory.Faker("country")
