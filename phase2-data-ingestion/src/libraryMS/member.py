from pydantic import BaseModel, EmailStr, field_validator
import re


class UserBookData(BaseModel):
    name: str
    email: EmailStr
    phone: str
    isbn: str

    # Name Normalization:
    # - Standardize capitalization (Title Case)
    # - Remove extra whitespace between names
    # - Trim leading/trailing spaces
    # - Ensure consistent formatting for same person
    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        v = v.strip()
        v = re.sub(r"\s+", " ", v)  # Replace multiple spaces with single space
        return v.title()  # Convert to Title Case (e.g., "john doe" → "John Doe")

    # Email is validated automatically by EmailStr

    # Phone Number Normalization
    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)  # Remove all non-digit characters
        if len(digits) == 10:
            return f"+1-{digits[0:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits.startswith("1"):
            return f"+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
        elif len(digits) > 11:
            # International format: +CountryCode-NNN-NNN-NNNN
            country_code = digits[:-10]
            return f"+{country_code}-{digits[-10:-7]}-{digits[-7:-4]}-{digits[-4:]}"
        else:
            raise ValueError("Invalid phone number format")

    # ISBN Validation & Normalization
    @field_validator("isbn")
    @classmethod
    def validate_and_clean_isbn(cls, v: str) -> str:
        isbn = re.sub(r"[-\s]", "", v)  # Remove hyphens and spaces
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
        total = sum((10 - i) * (10 if ch.upper() == 'X' else int(ch)) for i, ch in enumerate(isbn))
        return total % 11 == 0

    @staticmethod
    def is_valid_isbn13(isbn: str) -> bool:
        if not re.fullmatch(r"\d{13}", isbn):
            return False
        total = sum((int(ch) * (1 if i % 2 == 0 else 3)) for i, ch in enumerate(isbn))
        return total % 10 == 0
