from src.libraryMS.member import UserBookData
from src.data.userbook_sample import sample_user_book_data

for i, entry in enumerate(sample_user_book_data, start=1):
    try:
        user = UserBookData(**entry)
        print(f"UserBookData #{i}: {user}\n")
    except Exception as e:
        print(f"Validation error in entry #{i}: {e}\n")
