# src/libraryMS/schemas.py

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, date
import re

# Utility functions
def normalize_name(name: str) -> str:
    return name.strip().title()

def clean_phone(phone: str) -> Optional[str]:
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f'+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}'
    elif len(digits) > 10:
        return f'+{digits[:-10]}-{digits[-10:-7]}-{digits[-7:-4]}-{digits[-4:]}'
    return None

def validate_isbn(isbn: str) -> Optional[str]:
    isbn = re.sub(r'[-\s]', '', str(isbn))
    if re.match(r'^\d{13}$', isbn):
        return isbn
    return None

def parse_date_safe(value: str) -> Optional[date]:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None

# Pydantic Schemas

class MemberSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    member_type: str
    age: int

    @field_validator('name')
    @classmethod
    def normalize_name_field(cls, v): return normalize_name(v)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        cleaned = clean_phone(v)
        if not cleaned:
            raise ValueError('Invalid phone number')
        return cleaned

class AuthorSchema(BaseModel):
    name: str
    birth_date: Optional[str] = None
    biography: str = ""
    nationality: str = ""

    @field_validator('name')
    @classmethod
    def normalize_name_field(cls, v): return normalize_name(v)

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, v): return parse_date_safe(v)

class BookSchema(BaseModel):
    title: str
    isbn: str
    publication_date: Optional[str] = None
    author: str
    pages: int = 0
    price: str = "0.00"

    @field_validator('title', 'author')
    @classmethod
    def normalize_text(cls, v): return normalize_name(v)

    @field_validator('isbn')
    @classmethod
    def validate_isbn_field(cls, v):
        isbn = validate_isbn(v)
        if not isbn:
            raise ValueError("Invalid ISBN")
        return isbn

    @field_validator('publication_date', mode='before')
    @classmethod
    def parse_date(cls, v): return parse_date_safe(v)

class LibrarySchema(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name_field(cls, v): return normalize_name(v)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        cleaned = clean_phone(v)
        if not cleaned:
            raise ValueError("Invalid phone number")
        return cleaned
