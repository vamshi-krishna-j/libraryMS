insert into lib (library_id, name, campus_location, contact_email, phone_number)
values
(1, 'cis library', 'south campus', 'cislibrary@gmail.com', 9876543210),
(2, 'lgm library', 'north campus', 'lgmlibrary@gmail.com', 7410852963),
(3, 'admin library', 'west campus', 'adminlibrary@gmail.com', 9638527410);

insert into book (book_id, title, isbn, publication_date, total_copies, available_copies, library_id)
values
(1, '1984', '9780451524935', '1949-06-08', 10, 10, 1),
(2, 'Brave New World', '9780060850524', '1932-08-01', 8, 8, 1),
(3, 'Fahrenheit 451', '9781451673319', '1953-10-19', 12, 12, 2),
(4, 'To Kill a Mockingbird', '9780061120084', '1960-07-11', 7, 7, 2),
(5, 'The Great Gatsby', '9780743273565', '1925-04-10', 6, 6, 3),
(6, 'Animal Farm', '9780451526342', '1945-08-17', 9, 9, 1),
(7, 'Lord of the Flies', '9780399501487', '1954-09-17', 10, 10, 1),
(8, 'Of Mice and Men', '9780140177398', '1937-11-23', 6, 6, 2),
(9, 'Catch-22', '9781451626650', '1961-11-10', 8, 8, 2),
(10, 'Slaughterhouse-Five', '9780440180296', '1969-03-31', 5, 5, 3),
(11, 'The Catcher in the Rye', '9780316769488', '1951-07-16', 10, 10, 3),
(12, 'A Clockwork Orange', '9780393312836', '1962-02-01', 7, 7, 1),
(13, 'The Hobbit', '9780547928227', '1937-09-21', 15, 15, 2),
(14, 'Dune', '9780441172719', '1965-08-01', 12, 12, 3),
(15, 'The Handmaid''s Tale', '9780385490818', '1985-09-01', 9, 9, 1);

insert into author (author_id, first_name, last_name, birth_date, nationality, biography)
values 
(1, 'George', 'Orwell', '1903-06-25', 'British', 'Author of dystopian classics including 1984 and Animal Farm.'),
(2, 'Aldous', 'Huxley', '1894-07-26', 'British', 'Best known for Brave New World.'),
(3, 'Ray', 'Bradbury', '1920-08-22', 'American', 'Famous for Fahrenheit 451 and other science fiction works.'),
(4, 'Harper', 'Lee', '1926-04-28', 'American', 'Author of To Kill a Mockingbird.'),
(5, 'F. Scott', 'Fitzgerald', '1896-09-24', 'American', 'Known for The Great Gatsby and Jazz Age fiction.'),
(6, 'William', 'Golding', '1911-09-19', 'British', 'Author of Lord of the Flies.'),
(7, 'J.D.', 'Salinger', '1919-01-01', 'American', 'Wrote The Catcher in the Rye.'),
(8, 'Anthony', 'Burgess', '1917-02-25', 'British', 'Best known for A Clockwork Orange.');

insert into Category (category_id, name, description)
values
(1, 'Dystopian', 'Books set in oppressive or totalitarian societies'),
(2, 'Science Fiction', 'Speculative fiction with futuristic or technological elements'),
(3, 'Political Fiction', 'Books with political themes or commentary'),
(4, 'Classic Literature', 'Timeless works recognized for literary significance'),
(5, 'Fantasy', 'Books featuring magical or supernatural elements');

insert into Member (member_id, first_name, last_name, email, phone, member_type, registration_date)
values
(1, 'Alice', 'Johnson', 'alice.johnson@example.com', '5551234567', 'student', '2023-01-15'),
(2, 'Bob', 'Smith', 'bob.smith@example.com', '5552345678', 'faculty', '2022-08-23'),
(3, 'Carol', 'Williams', 'carol.williams@example.com', '5553456789', 'student', '2023-03-10'),
(4, 'David', 'Brown', 'david.brown@example.com', '5554567890', 'faculty', '2021-11-05'),
(5, 'Eva', 'Davis', 'eva.davis@example.com', '5555678901', 'student', '2023-02-20'),
(6, 'Frank', 'Miller', 'frank.miller@example.com', '5556789012', 'faculty', '2020-06-12'),
(7, 'Grace', 'Wilson', 'grace.wilson@example.com', '5557890123', 'student', '2023-04-01'),
(8, 'Henry', 'Moore', 'henry.moore@example.com', '5558901234', 'faculty', '2022-12-15'),
(9, 'Ivy', 'Taylor', 'ivy.taylor@example.com', '5559012345', 'student', '2023-05-08'),
(10, 'Jack', 'Anderson', 'jack.anderson@example.com', '5550123456', 'faculty', '2021-09-30'),
(11, 'Kara', 'Thomas', 'kara.thomas@example.com', '5551230987', 'student', '2023-01-25'),
(12, 'Leo', 'Jackson', 'leo.jackson@example.com', '5552341098', 'faculty', '2019-10-22'),
(13, 'Mia', 'White', 'mia.white@example.com', '5553452109', 'student', '2023-03-14'),
(14, 'Nate', 'Harris', 'nate.harris@example.com', '5554563210', 'faculty', '2022-07-18'),
(15, 'Olivia', 'Martin', 'olivia.martin@example.com', '5555674321', 'student', '2023-02-05'),
(16, 'Paul', 'Lee', 'paul.lee@example.com', '5556785432', 'faculty', '2021-05-29'),
(17, 'Quinn', 'Walker', 'quinn.walker@example.com', '5557896543', 'student', '2023-04-12'),
(18, 'Rachel', 'Hall', 'rachel.hall@example.com', '5558907654', 'faculty', '2020-08-11'),
(19, 'Sam', 'Allen', 'sam.allen@example.com', '5559018765', 'student', '2023-05-20'),
(20, 'Tina', 'Young', 'tina.young@example.com', '5550129876', 'faculty', '2022-11-03');


insert into Borrowing (borrowing_id, member_id, book_id, borrow_date, due_date, return_date, late_fee)
VALUES
(1, 1, 1, '2023-06-01', '2023-06-15', '2023-06-14', 0),
(2, 2, 2, '2023-06-03', '2023-06-17', '2023-06-20', 5),
(3, 3, 3, '2023-06-05', '2023-06-19', NULL, 0),
(4, 4, 4, '2023-05-20', '2023-06-03', '2023-06-01', 0),
(5, 5, 5, '2023-05-22', '2023-06-05', '2023-06-07', 3),
(6, 6, 6, '2023-06-10', '2023-06-24', NULL, 0),
(7, 7, 7, '2023-06-12', '2023-06-26', '2023-06-25', 0),
(8, 8, 8, '2023-06-01', '2023-06-15', '2023-06-18', 4),
(9, 9, 9, '2023-05-28', '2023-06-11', '2023-06-10', 0),
(10, 10, 10, '2023-06-02', '2023-06-16', NULL, 0),
(11, 11, 11, '2023-06-04', '2023-06-18', '2023-06-19', 2),
(12, 12, 12, '2023-05-25', '2023-06-08', '2023-06-08', 0),
(13, 13, 13, '2023-06-06', '2023-06-20', NULL, 0),
(14, 14, 14, '2023-06-07', '2023-06-21', '2023-06-25', 6),
(15, 15, 15, '2023-06-08', '2023-06-22', NULL, 0),
(16, 16, 1, '2023-06-09', '2023-06-23', '2023-06-23', 0),
(17, 17, 2, '2023-06-10', '2023-06-24', '2023-06-30', 10),
(18, 18, 3, '2023-06-11', '2023-06-25', NULL, 0),
(19, 19, 4, '2023-06-12', '2023-06-26', '2023-06-27', 2),
(20, 20, 5, '2023-06-13', '2023-06-27', NULL, 0),
(21, 1, 6, '2023-06-14', '2023-06-28', '2023-06-28', 0),
(22, 2, 7, '2023-06-15', '2023-06-29', '2023-07-02', 7),
(23, 3, 8, '2023-06-16', '2023-06-30', NULL, 0),
(24, 4, 9, '2023-06-17', '2023-07-01', '2023-07-01', 0),
(25, 5, 10, '2023-06-18', '2023-07-02', '2023-07-05', 5);

insert into  Review (review_id, member_id, book_id, rating, comment, review_date)
values
(1, 1, 1, 5, 'A chilling and timeless dystopian novel.', '2023-06-15'),
(2, 2, 2, 4, 'Thought-provoking and unsettling.', '2023-06-18'),
(3, 3, 3, 5, 'A masterpiece of science fiction.', '2023-06-20'),
(4, 4, 4, 4, 'Powerful story with deep social themes.', '2023-06-10'),
(5, 5, 5, 3, 'Classic, but not my favorite.', '2023-06-12'),
(6, 6, 6, 5, 'Animal Farm is a brilliant allegory.', '2023-06-25'),
(7, 7, 7, 4, 'Engaging and thought-provoking.', '2023-06-26'),
(8, 8, 8, 5, 'A moving and tragic story.', '2023-06-30'),
(9, 9, 9, 4, 'Witty and clever satire.', '2023-07-01'),
(10, 10, 10, 3, 'Interesting concepts but slow at times.', '2023-07-02'),
(11, 11, 11, 5, 'A timeless coming-of-age story.', '2023-07-03'),
(12, 12, 12, 4, 'Challenging but rewarding read.', '2023-07-04');

INSERT INTO BookAuthor (book_id, author_id) VALUES
(1, 1),
(6, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(7, 6),
(11, 7),
(12, 8);

INSERT INTO BookCategory (book_id, category_id, created_at, updated_at) VALUES
(1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(8, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(9, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(9, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(10, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(11, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(12, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(12, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(13, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(13, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(14, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(14, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(15, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(15, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


UPDATE book SET available_copies = 7 WHERE book_id = 1;
UPDATE book SET available_copies = 5 WHERE book_id = 2;
UPDATE book SET available_copies = 12 WHERE book_id = 3;
UPDATE book SET available_copies = 4 WHERE book_id = 4;
UPDATE book SET available_copies = 6 WHERE book_id = 5;


UPDATE book SET available_copies = 8 WHERE book_id = 6;
UPDATE book SET available_copies = 9 WHERE book_id = 7;
UPDATE book SET available_copies = 3 WHERE book_id = 8;
UPDATE book SET available_copies = 8 WHERE book_id = 9;
UPDATE book SET available_copies = 2 WHERE book_id = 10;
UPDATE book SET available_copies = 7 WHERE book_id = 11;
UPDATE book SET available_copies = 5 WHERE book_id = 12;
UPDATE book SET available_copies = 15 WHERE book_id = 13;
UPDATE book SET available_copies = 10 WHERE book_id = 14;
UPDATE book SET available_copies = 6 WHERE book_id = 15;
