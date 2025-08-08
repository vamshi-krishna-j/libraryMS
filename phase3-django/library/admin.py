from django.contrib import admin
from .models import (
    Lib,
    Author,
    Category,
    Book,
    Member,
    Borrowing,
    Review,
    BookAuthor,    # Correct casing here
    BookCategory   # Correct casing here
)

admin.site.register(Lib)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Borrowing)
admin.site.register(Review)
admin.site.register(BookAuthor)     # Use correct model name here too
admin.site.register(BookCategory)   # And here
