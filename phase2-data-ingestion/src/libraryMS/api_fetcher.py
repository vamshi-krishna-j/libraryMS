import argparse
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Author, Book
from api_client import OpenLibraryApi
from schemas import AuthorSchema, BookSchema
from datetime import date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', required=True, help="Author name to search for")
    parser.add_argument('--limit', type=int, default=10, help="Number of books to fetch")
    parser.add_argument('--db', required=True, help="Database connection URL")
    parser.add_argument('--output', help="Optional JSON file to save raw API data")
    args = parser.parse_args()

    # Database setup
    engine = create_engine(args.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    client = OpenLibraryApi()

    try:
        # Step 1: Search author
        author_result = client.search_author(args.author)
        author_doc = author_result.get('docs', [])[0]
        author_key = author_doc['key'].split('/')[-1]

        # Step 2: Validate Author
        author_data = {
            "name": author_doc.get("name", ""),
            "birth_date": author_doc.get("birth_date", None),
            "biography": author_doc.get("bio") if isinstance(author_doc.get("bio"), str) else "",
            "nationality": ""
        }

        try:
            validated_author = AuthorSchema(**author_data)
        except Exception as e:
            print(f"[ERROR] Author validation failed: {e}")
            return

        # Step 3: Store or retrieve author
        db_author = session.query(Author).filter_by(
            name=validated_author.name,
            birth_date=validated_author.birth_date
        ).first()

        if not db_author:
            db_author = Author(
                name=validated_author.name,
                birth_date=validated_author.birth_date,
                biography=validated_author.biography,
                nationality=validated_author.nationality
            )
            session.add(db_author)
            session.commit()
            print(f"[INFO] Author saved: {db_author.name}")
        else:
            print(f"[INFO] Author exists: {db_author.name}")

        # Step 4: Fetch books
        works = client.get_author_works(author_key).get("entries", [])[:args.limit]
        raw_books = []

        for work in works:
            try:
                work_key = work.get("key")
                title = work.get("title", "")
                work_details = client.get_work_details(work_key)

                # Step 1: Try getting ISBN from work details
                identifiers = work_details.get("identifiers", {})
                isbn = None
                for key in ["isbn_13", "isbn_10"]:
                    if key in identifiers and identifiers[key]:
                        isbn = identifiers[key][0]
                        break

                # Step 2: If not found, try editions
                if not isbn:
                    editions = client.get_work_editions(work_key)
                    edition_list = editions.get("entries", [])
                    for ed in edition_list:
                        # Check both `identifiers` and top-level keys in edition
                        for key in ["isbn_13", "isbn_10"]:
                            # First try identifiers
                            id_from_identifiers = ed.get("identifiers", {}).get(key, [])
                            if id_from_identifiers:
                                isbn = id_from_identifiers[0]
                                break

                            # Then try top-level
                            id_from_top_level = ed.get(key, [])
                            if id_from_top_level:
                                isbn = id_from_top_level[0]
                                break

                        if isbn:
                            break

                if not isbn:
                    print(f"[WARN] Skipping book '{title}': No ISBN in editions.")
                    continue

                pub_date = work_details.get("created", {}).get("value")
                print(f"[DEBUG] Raw pub_date from API for '{title}': {pub_date}")

                pages = work_details.get("number_of_pages", 0)
                if not pages:
                    editions = client.get_work_editions(work_key)
                    edition_list = editions.get("entries", [])
                    for ed in edition_list:
                        pages = ed.get("number_of_pages")
                        if pages:
                            break

                if not pages:
                    pages = 0

                    print(f"[DEBUG] Pages found for '{title}': {pages}")

                book_data = {
                    "title": title,
                    "isbn": isbn,
                    "publication_date": pub_date,
                    "author": validated_author.name,
                    "pages": pages or 0,
                    "price": "0.00"
                }

                raw_books.append(book_data)

                # Step 5: Validate book
                validated_book = BookSchema(**book_data)

                # Step 6: Check for duplicates
                exists = session.query(Book).filter_by(isbn=validated_book.isbn).first()
                if exists:
                    print(f"[INFO] Skipped duplicate: {validated_book.title}")
                    continue

                # Step 7: Save book
                book = Book(
                    title=validated_book.title,
                    isbn=validated_book.isbn,
                    publication_date=validated_book.publication_date,
                    pages=validated_book.pages,
                    price=float(validated_book.price),
                    author_id=db_author.id
                )
                session.add(book)
                session.commit()
                print(f"[INFO] Book saved: {book.title}")

            except Exception as e:
                session.rollback()
                print(f"[ERROR] Failed to process book: {title}. Reason: {e}")

        # Step 8: Optional raw output save
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(raw_books, f, indent=2)
            print(f"[INFO] Raw output saved to {args.output}")

    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
    finally:
        session.close()
        print("[INFO] Database session closed.")


if __name__ == "__main__":
    main()
