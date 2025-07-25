#Book with their author and categories

SELECT 
    b.book_id,
    b.title AS book_title,
    CONCAT(a.first_name, ' ', a.last_name) AS author_name,
    c.name AS category_name
FROM 
    Book b
JOIN BookAuthor ba ON b.book_id = ba.book_id
JOIN Author a ON ba.author_id = a.author_id
JOIN BookCategory bc ON b.book_id = bc.book_id
JOIN Category c ON bc.category_id = c.category_id
ORDER BY b.book_id;


#Most borrowed books in between 2023-06-10 and 2023-07-10

SELECT 
    b.book_id,
    bk.title,
    COUNT(*) AS borrow_count
FROM 
    Borrowing b
JOIN 
    Book bk ON b.book_id = bk.book_id
WHERE 
    b.borrow_date BETWEEN '2023-06-10' AND '2023-07-10'
GROUP BY 
    b.book_id, bk.title
ORDER BY 
    borrow_count DESC
LIMIT 1;


#Members with overdue books and calculated late fees

SELECT
  m.member_id,
  m.first_name,
  m.last_name,
  bk.book_id,
  bk.title,
  br.due_date,
  br.return_date,
  DATEDIFF(br.return_date , br.due_date) * 1.00 AS calculated_late_fee,
  DATEDIFF( br.return_date , br.due_date) AS days_overdue
FROM
  Member m
JOIN
  Borrowing br ON m.member_id = br.member_id
JOIN
  Book bk ON br.book_id = bk.book_id
WHERE
  br.return_date IS NULL
  AND br.due_date < br.return_date;

#Average rating per book with author information

SELECT
  b.book_id,
  b.title,
  CONCAT(a.first_name, ' ', a.last_name) AS author,
  AVG(r.rating) AS average_rating
FROM book b
JOIN BookAuthor ba ON b.book_id = ba.book_id
JOIN author a ON ba.author_id = a.author_id
LEFT JOIN Review r ON b.book_id = r.book_id
GROUP BY b.book_id, b.title, a.author_id, a.first_name, a.last_name
ORDER BY average_rating DESC;


#Books available in each library with stock level


SELECT
  l.library_id,
  l.name AS library_name,
  b.book_id,
  b.title,
  b.total_copies,
  b.available_copies
FROM lib l
JOIN book b ON l.library_id = b.library_id
ORDER BY l.library_id, b.book_id;


















