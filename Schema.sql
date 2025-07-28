
create table lib(library_id int primary key, 
name varchar(50) not null, 
campus_location varchar(50),
contact_email varchar(50), 
phone_number varchar(12)); 

create table book (
    book_id int PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_date DATE,
    total_copies INT,
    available_copies INT,
    library_id INT,
    FOREIGN KEY (library_id) REFERENCES lib(library_id)
);

CREATE TABLE author (
    author_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    nationality VARCHAR(50),
    biography TEXT
);
CREATE TABLE category (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE member (
    member_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    member_type VARCHAR(20),
    registration_date DATE
);

CREATE TABLE borrowing (
    borrowing_id INT PRIMARY KEY,
    member_id INT,
    book_id INT,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    late_fee DECIMAL(7,2),
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    review_date DATE NOT NULL,
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES Member(member_id),
    CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES Book(book_id),
    UNIQUE KEY unique_member_book_review (member_id, book_id)
);

CREATE TABLE BookAuthor (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_book_author_book FOREIGN KEY (book_id) REFERENCES Book(book_id),
    CONSTRAINT fk_book_author_author FOREIGN KEY (author_id) REFERENCES Author(author_id)
);

CREATE TABLE BookCategory (
    book_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (book_id, category_id),
    CONSTRAINT fk_bookcategory_book FOREIGN KEY (book_id) REFERENCES Book(book_id),
    CONSTRAINT fk_bookcategory_category FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

ALTER TABLE author 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;


ALTER TABLE Lib
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE category 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE borrowing 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE bookcategory 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE bookauthor 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE book 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;















