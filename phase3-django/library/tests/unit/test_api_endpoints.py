from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, Member, Borrowing
from datetime import date, timedelta

class BookAPITest(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890123",
            total_copies=5,
            available_copies=5,
            publication_date=date(2020, 1, 1),
        )
        self.member = Member.objects.create(
            member_id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_borrow_book_success(self):
        url = reverse('borrow-book')
        data = {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 4)

    def test_borrow_book_unavailable(self):
        self.book.available_copies = 0
        self.book.save()
        url = reverse('borrow-book')
        data = {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_return_book_success(self):
        borrowing = Borrowing.objects.create(
            book=self.book,
            member=self.member,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14)
        )
        self.book.available_copies -= 1
        self.book.save()

        url = reverse('return-book')
        data = {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 5)

    def test_return_book_no_active_borrowing(self):
        url = reverse('return-book')
        data = {
            "book_id": self.book.book_id,
            "member_id": self.member.member_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_book_availability(self):
        url = reverse('book-availability', args=[self.book.book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('available', response.data)
        self.assertIn('available_copies', response.data)

    def test_member_borrowing_history(self):
        Borrowing.objects.create(
            book=self.book,
            member=self.member,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14)
        )
        url = reverse('member-borrowing-history', args=[self.member.member_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_book_search(self):
        url = reverse('book-search')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_statistics(self):
        url = reverse('statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_books', response.data)
        self.assertIn('total_members', response.data)
        self.assertIn('total_borrowings', response.data)
        self.assertIn('currently_borrowed', response.data)

