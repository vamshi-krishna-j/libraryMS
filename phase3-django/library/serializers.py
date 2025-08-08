from rest_framework import serializers
from .models import Lib, Book, Author, Category, Member, Borrowing, Review
from django.utils import timezone


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lib
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        total = data.get('total_copies')
        available = data.get('available_copies')
        if total is not None and available is not None and available > total:
            raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def validate_birth_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only Gmail addresses are accepted.")
        return value


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'

    def validate(self, data):
        if data['due_date'] <= data['borrow_date']:
            raise serializers.ValidationError("Due date must be after borrow date.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
