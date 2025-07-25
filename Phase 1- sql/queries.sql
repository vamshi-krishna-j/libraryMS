SELECT 
    b.book_id,
    b.title,
    a.first_name,
    a.last_name
FROM 
    Book b
JOIN BookAuthor ba ON b.book_id = ba.book_id
JOIN Author a ON ba.author_id = a.author_id;


SELECT 
    m.member_id,
    m.first_name,
    m.last_name,
    b.title,
    br.borrow_date,
    br.due_date,
    br.return_date,
    br.late_fee
FROM 
    Borrowing br
JOIN Member m ON br.member_id = m.member_id
JOIN Book b ON br.book_id = b.book_id;



SELECT 
    l.name AS library_name,
    b.title AS book_title,
    CONCAT(a.first_name, ' ', a.last_name) AS author,
    c.name AS category
FROM 
    Lib l
JOIN Book b ON l.library_id = b.library_id
JOIN BookAuthor ba ON b.book_id = ba.book_id
JOIN Author a ON ba.author_id = a.author_id
LEFT JOIN BookCategory bc ON b.book_id = bc.book_id
LEFT JOIN Category c ON bc.category_id = c.category_id;

#count

SELECT 
    l.name AS library_name,
    COUNT(b.book_id) AS total_books
FROM 
    Lib l
LEFT JOIN Book b ON l.library_id = b.library_id
GROUP BY l.library_id;

#avg

SELECT 
    b.title,
    AVG(r.rating) AS average_rating
FROM 
    Book b
JOIN Review r ON b.book_id = r.book_id
GROUP BY b.book_id;

#sum


SELECT 
    m.first_name,
    m.last_name,
    SUM(br.late_fee) AS total_late_fees
FROM 
    Member m
JOIN Borrowing br ON m.member_id = br.member_id
GROUP BY m.member_id;


#Get books with average rating greater than 4

SELECT 
    b.title,
    (SELECT AVG(r.rating) 
     FROM Review r 
     WHERE r.book_id = b.book_id) AS avg_rating
FROM Book b
WHERE 
    (SELECT AVG(r.rating) 
     FROM Review r 
     WHERE r.book_id = b.book_id) > 4;


#Members who borrowed more books than the average

SELECT 
    m.member_id,
    m.first_name,
    m.last_name,
    (SELECT COUNT(*) FROM Borrowing b WHERE b.member_id = m.member_id) AS total_borrowed
FROM Member m
WHERE 
    (SELECT COUNT(*) FROM Borrowing b WHERE b.member_id = m.member_id) >
    (SELECT AVG(borrow_count) 
     FROM (
         SELECT COUNT(*) AS borrow_count 
         FROM Borrowing 
         GROUP BY member_id
     ) AS member_borrows);


#CTE for Average Late Fee Per Member

WITH LateFees AS (
    SELECT 
        member_id,
        SUM(late_fee) AS total_late_fee
    FROM Borrowing
    GROUP BY member_id
)
SELECT 
    m.first_name,
    m.last_name,
    lf.total_late_fee
FROM Member m
JOIN LateFees lf ON m.member_id = lf.member_id;

#Top 3 Most Borrowed Books

WITH BookBorrowCount AS (
    SELECT 
        book_id,
        COUNT(*) AS borrow_count
    FROM Borrowing
    GROUP BY book_id
)
SELECT 
    b.title,
    bbc.borrow_count
FROM Book b
JOIN BookBorrowCount bbc ON b.book_id = bbc.book_id
ORDER BY bbc.borrow_count DESC
LIMIT 3;

#window function

#ROW_NUMBER() – Number books within each library

SELECT 
    l.name AS library_name,
    b.title,
    ROW_NUMBER() OVER (PARTITION BY l.library_id ORDER BY b.title) AS row_num
FROM 
    Book b
JOIN 
    Lib l ON b.library_id = l.library_id;

# RANK() – Rank books based on available stock per library

SELECT 
    l.name AS library_name,
    b.title,
    b.available_copies,
    RANK() OVER (PARTITION BY l.library_id ORDER BY b.available_copies DESC) AS stock_rank
FROM 
    Book b
JOIN 
    Lib l ON b.library_id = l.library_id;


#AVG() OVER – Average rating of all reviews per book without grouping

SELECT 
    r.review_id,
    b.title,
    r.rating,
    AVG(r.rating) OVER (PARTITION BY r.book_id) AS avg_book_rating
FROM 
    Review r
JOIN 
    Book b ON r.book_id = b.book_id;










