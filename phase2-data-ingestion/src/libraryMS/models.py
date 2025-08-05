from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, UniqueConstraint, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    member_type = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

    __table_args__ = (
        Index("ix_member_email", "email"),
    )


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    biography = Column(String(1000), nullable=True)
    nationality = Column(String(100), nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("name", "birth_date", name="uq_author_name_birth"),
        Index("ix_author_name", "name"),
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    publication_date = Column(Date, nullable=True)
    pages = Column(Integer, default=0)
    price = Column(Float, default=0.00)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    __table_args__ = (
        Index("ix_book_isbn", "isbn"),
    )


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "email", name="uq_library_name_email"),
        Index("ix_library_email", "email"),
    )
