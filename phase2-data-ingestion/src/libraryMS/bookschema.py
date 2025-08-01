from pydantic import BaseModel, field_validator
import re
from typing import Optional
from datetime import date

class BookData(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: Optional[date] = None
    genre: Optional[str] = None
    price: Optional[float] = None

    # Normalize title to UPPERCASE
    @field_validator("title")
    @classmethod
    def normalize_title(cls, v: str) -> str:
        return v.strip().upper()

    # Normalize author name to UPPERCASE
    @field_validator("author")
    @classmethod
    def normalize_author(cls, v: str) -> str:
        return v.strip().upper()

    # ISBN validation
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        isbn = re.sub(r"[-\s]", "", v)
        if len(isbn) == 10:
            if not cls.is_valid_isbn10(isbn):
                raise ValueError("Invalid ISBN-10")
        elif len(isbn) == 13:
            if not cls.is_valid_isbn13(isbn):
                raise ValueError("Invalid ISBN-13")
        else:
            raise ValueError("ISBN must be 10 or 13 digits long")
        return isbn

    @staticmethod
    def is_valid_isbn10(isbn: str) -> bool:
        if not re.fullmatch(r"\d{9}[\dXx]", isbn):
            return False
        total = sum((10 - i) * (10 if ch.upper() == "X" else int(ch)) for i, ch in enumerate(isbn))
        return total % 11 == 0

    @staticmethod
    def is_valid_isbn13(isbn: str) -> bool:
        if not re.fullmatch(r"\d{13}", isbn):
            return False
        total = sum((int(ch) * (1 if i % 2 == 0 else 3)) for i, ch in enumerate(isbn))
        return total % 10 == 0

    # Validate price if provided
    @field_validator("price")
    @classmethod
    def check_price_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Price must be non-negative")
        return v



