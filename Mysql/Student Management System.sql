CREATE DATABASE student_management;
USE student_management;

CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL
);
SHOW TABLES;

INSERT INTO departments (department_name)
VALUES
('Computer Science'),
('Commerce'),
('Mathematics'),
('Physics'),
('Chemistry');

SELECT * FROM departments;

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    dob DATE,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    city VARCHAR(50),
    department_id INT,
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);

INSERT INTO students
(student_name, gender, dob, email, phone, city, department_id)
VALUES
('Rahul', 'Male', '2005-05-12',
 'rahul@gmail.com', '9876543210', 'Delhi', 1),

('Priya', 'Female', '2005-08-20',
 'priya@gmail.com', '9876543211', 'Rohtak', 2),

('Amit', 'Male', '2004-11-15',
 'amit@gmail.com', '9876543212', 'Palwal', 1),

('Neha', 'Female', '2005-06-15',
 'neha@gmail.com', '9876543213', 'Delhi', 3),

('Rohit', 'Male', '2004-09-10',
 'rohit@gmail.com', '9876543214', 'Panipat', 4);
 
SELECT * FROM students;

SELECT
    s.student_id,
    s.student_name,
    s.city,
    d.department_name
FROM students s
INNER JOIN departments d
ON s.department_id = d.department_id;

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL
);

INSERT INTO courses (course_name, credits)
VALUES
('Database Management System', 4),
('Python Programming', 3),
('Java Programming', 4),
('Computer Networks', 3),
('Mathematics', 4),
('Web Development', 3);

SELECT * FROM courses;

CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE,

    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);

INSERT INTO enrollments
(student_id, course_id, enrollment_date)
VALUES
(1, 1, '2026-11-01'),
(1, 2, '2026-11-01'),
(2, 3, '2026-11-02'),
(2, 5, '2026-11-02'),
(3, 1, '2026-11-03'),
(3, 4, '2026-11-03'),
(4, 6, '2026-11-04'),
(5, 2, '2026-11-04');

SELECT * FROM enrollments;

SELECT
    s.student_name,
    c.course_name,
    e.enrollment_date
FROM enrollments e
INNER JOIN students s
    ON e.student_id = s.student_id
INNER JOIN courses c
    ON e.course_id = c.course_id;
    
SELECT
    c.course_name,
    COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY c.course_id;

SHOW TABLES;

CREATE TABLE marks (
    mark_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    marks_obtained DECIMAL(5,2),
    total_marks DECIMAL(5,2),

    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);

INSERT INTO marks
(student_id, course_id, marks_obtained, total_marks)
VALUES
(1, 1, 85, 100),
(1, 2, 90, 100),
(2, 3, 78, 100),
(2, 5, 88, 100),
(3, 1, 92, 100),
(3, 4, 75, 100),
(4, 6, 95, 100),
(5, 2, 82, 100);

SELECT * FROM marks;

SELECT * FROM marks
ORDER BY mark_id;

SELECT COUNT(*) AS total_records
FROM marks;

SELECT student_id, course_id, COUNT(*) AS occurrences
FROM marks
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (student_id)
    REFERENCES students(student_id)
);

INSERT INTO attendance
(student_id, attendance_date, status)
VALUES
(1, '2026-11-10', 'Present'),
(1, '2026-11-11', 'Present'),
(1, '2026-11-12', 'Absent'),

(2, '2026-11-10', 'Present'),
(2, '2026-11-11', 'Absent'),
(2, '2026-11-12', 'Present'),

(3, '2026-11-10', 'Present'),
(3, '2026-11-11', 'Present'),
(3, '2026-11-12', 'Present'),

(4, '2026-11-10', 'Present'),
(4, '2026-11-11', 'Absent'),
(4, '2026-11-12', 'Present'),

(5, '2026-11-10', 'Absent'),
(5, '2026-11-11', 'Present'),
(5, '2026-11-12', 'Present');

SELECT
    a.attendance_id,
    s.student_name,
    a.attendance_date,
    a.status
FROM attendance a
JOIN students s
ON a.student_id = s.student_id
ORDER BY a.attendance_date, s.student_id;

SELECT
    s.student_id,
    s.student_name,
    COUNT(a.attendance_id) AS total_classes,
    SUM(
        CASE
            WHEN a.status = 'Present' THEN 1
            ELSE 0
        END
    ) AS present_days,
    SUM(
        CASE
            WHEN a.status = 'Absent' THEN 1
            ELSE 0
        END
    ) AS absent_days,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN a.status = 'Present' THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(a.attendance_id), 0),
        2
    ) AS attendance_percentage
FROM students s
LEFT JOIN attendance a
ON s.student_id = a.student_id
GROUP BY s.student_id, s.student_name
ORDER BY s.student_id;

SELECT
    s.student_name,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN a.status = 'Present' THEN 1
                ELSE 0
            END
        ) / COUNT(a.attendance_id),
        2
    ) AS attendance_percentage
FROM students s
JOIN attendance a
ON s.student_id = a.student_id
GROUP BY s.student_id, s.student_name
HAVING attendance_percentage < 75;

SELECT
    s.student_name,
    c.course_name,
    m.marks_obtained,
    m.total_marks
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN courses c
    ON m.course_id = c.course_id
ORDER BY s.student_id, c.course_id;

SELECT
    s.student_name,
    SUM(m.marks_obtained) AS obtained_marks,
    SUM(m.total_marks) AS total_marks,
    ROUND(
        SUM(m.marks_obtained) * 100 /
        SUM(m.total_marks), 2
    ) AS percentage,
    CASE
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 90 THEN 'A+'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 80 THEN 'A'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 70 THEN 'B'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 60 THEN 'C'
        ELSE 'D'
    END AS grade
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name
ORDER BY percentage DESC;

SELECT
    s.student_name,
    ROUND(
        SUM(m.marks_obtained) * 100 /
        SUM(m.total_marks), 2
    ) AS percentage
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name
ORDER BY percentage DESC
LIMIT 1;

SELECT
    ROUND(
        SUM(m.marks_obtained) * 100 /
        SUM(m.total_marks), 2
    ) AS class_average_percentage
FROM marks m;

CREATE VIEW student_performance AS
SELECT
    s.student_id,
    s.student_name,
    SUM(m.marks_obtained) AS obtained_marks,
    SUM(m.total_marks) AS total_marks,
    ROUND(
        SUM(m.marks_obtained) * 100 /
        SUM(m.total_marks), 2
    ) AS percentage,
    CASE
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 90 THEN 'A+'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 80 THEN 'A'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 70 THEN 'B'
        WHEN SUM(m.marks_obtained) * 100 /
             SUM(m.total_marks) >= 60 THEN 'C'
        ELSE 'D'
    END AS grade
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name;

SELECT * FROM student_performance;

SELECT *
FROM student_performance
WHERE grade = 'A+';

SELECT *
FROM student_performance
ORDER BY percentage DESC;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';

DELIMITER //

CREATE PROCEDURE GetAllStudents()
BEGIN
    SELECT
        student_id,
        student_name,
        gender,
        email,
        city
    FROM students;
END //

DELIMITER ;

CALL GetAllStudents();

DELIMITER //

CREATE PROCEDURE GetStudentByID(
    IN p_student_id INT
)
BEGIN
    SELECT *
    FROM students
    WHERE student_id = p_student_id;
END //

DELIMITER ;

CALL GetStudentByID(3);
CALL GetStudentByID(1);

SHOW PROCEDURE STATUS
WHERE Db = 'student_management';

CREATE TABLE student_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    action_message VARCHAR(100),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM student_log;

DELIMITER //

CREATE TRIGGER after_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log
    (student_id, action_message)
    VALUES
    (NEW.student_id, 'New student added');
END //

DELIMITER ;

INSERT INTO students
(student_name, gender, dob, email, phone, city, department_id)
VALUES
('Karan', 'Male', '2005-12-10',
 'karan@gmail.com', '9876543215', 'Ambala', 1);
 
SELECT * FROM students
WHERE student_id = 6;

SELECT * FROM student_log;
SHOW TRIGGERS
WHERE `Table` = 'students';

SHOW TABLES;
SHOW FULL TABLES
WHERE Table_type = 'VIEW';

SELECT student_id, student_name, city
FROM students
WHERE student_id = 1;

UPDATE students
SET city = 'Ambala'
WHERE student_id = 1;

SELECT student_id, student_name, city
FROM students
WHERE student_id = 1;

UPDATE students
SET
    phone = '9999999999',
    city = 'Chandigarh'
WHERE student_id = 1;

SELECT
    student_id,
    student_name,
    phone,
    city
FROM students
WHERE student_id = 1;

INSERT INTO students
(student_name, gender, dob, email, phone, city, department_id)
VALUES
('Test Student', 'Male', '2005-01-01',
 'teststudent@gmail.com', '9000000000', 'Delhi', 1);
 
SELECT *
FROM students
WHERE email = 'teststudent@gmail.com';

DELETE FROM students
WHERE email = 'teststudent@gmail.com';

SELECT *
FROM students
WHERE email = 'teststudent@gmail.com';

DELETE FROM students
WHERE student_id = 5;

SELECT
    student_id,
    student_name,
    phone,
    city
FROM students
ORDER BY student_id;

SELECT COUNT(*) AS total_students
FROM students;

SELECT
    d.department_name,
    COUNT(s.student_id) AS total_students
FROM departments d
LEFT JOIN students s
    ON d.department_id = s.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id;

SELECT COUNT(*) AS total_courses
FROM courses;

SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS total_enrollments
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY c.course_id;

SELECT
    COUNT(*) AS total_attendance_records,
    SUM(status = 'Present') AS present_records,
    SUM(status = 'Absent') AS absent_records
FROM attendance;

SELECT
    student_name,
    obtained_marks,
    total_marks,
    percentage,
    grade
FROM student_performance
ORDER BY percentage DESC;


SELECT
    (SELECT COUNT(*) FROM students)
        AS total_students,

    (SELECT COUNT(*) FROM departments)
        AS total_departments,

    (SELECT COUNT(*) FROM courses)
        AS total_courses,

    (SELECT COUNT(*) FROM enrollments)
        AS total_enrollments,

    (SELECT COUNT(*) FROM attendance)
        AS total_attendance_records,

    (SELECT COUNT(*) FROM marks)
        AS total_marks_records;
        
SHOW TABLES;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';

SHOW TRIGGERS;

SHOW PROCEDURE STATUS
WHERE Db = 'student_management';

SELECT AVG(marks_obtained) AS average_marks
FROM marks;

SELECT
    s.student_name,
    c.course_name,
    m.marks_obtained
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN courses c
    ON m.course_id = c.course_id
WHERE m.marks_obtained >
    (SELECT AVG(marks_obtained) FROM marks)
ORDER BY m.marks_obtained DESC;

SELECT AVG(marks_obtained) FROM marks;

SELECT
    s.student_name,
    c.course_name,
    m.marks_obtained
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN courses c
    ON m.course_id = c.course_id
WHERE m.marks_obtained = (
    SELECT MAX(marks_obtained)
    FROM marks
);

SELECT
    s.student_name,
    c.course_name,
    m.marks_obtained
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
JOIN courses c
    ON m.course_id = c.course_id
WHERE m.marks_obtained > (
    SELECT AVG(m2.marks_obtained)
    FROM marks m2
    WHERE m2.student_id = s.student_id
)
ORDER BY s.student_id;

WITH student_totals AS (
    SELECT
        s.student_id,
        s.student_name,
        SUM(m.marks_obtained) AS obtained_marks,
        SUM(m.total_marks) AS total_marks
    FROM students s
    JOIN marks m
        ON s.student_id = m.student_id
    GROUP BY s.student_id, s.student_name
)
SELECT
    student_name,
    obtained_marks,
    total_marks,
    ROUND(
        obtained_marks * 100 / total_marks, 2
    ) AS percentage
FROM student_totals
ORDER BY percentage DESC;

SELECT VERSION();

SELECT
    s.student_name,
    m.marks_obtained,
    ROW_NUMBER() OVER (
        ORDER BY m.marks_obtained DESC
    ) AS row_num
FROM students s
JOIN marks m
    ON s.student_id = m.student_id;
    
SELECT
    s.student_name,
    m.marks_obtained,
    RANK() OVER (
        ORDER BY m.marks_obtained DESC
    ) AS student_rank
FROM students s
JOIN marks m
    ON s.student_id = m.student_id;
    
SELECT
    student_name,
    marks_obtained,
    RANK() OVER (
        ORDER BY marks_obtained DESC
    ) AS normal_rank,
    DENSE_RANK() OVER (
        ORDER BY marks_obtained DESC
    ) AS dense_rank_value
FROM (
    SELECT 'Rahul' AS student_name, 90 AS marks_obtained
    UNION ALL
    SELECT 'Priya', 90
    UNION ALL
    SELECT 'Amit', 85
    UNION ALL
    SELECT 'Neha', 80
) AS sample_marks;

DELIMITER //

CREATE PROCEDURE SearchStudent(
    IN p_id INT
)
BEGIN
    SELECT
        student_id,
        student_name,
        email,
        city
    FROM students
    WHERE student_id = p_id;
END //

DELIMITER ;

CALL SearchStudent(3);

DELIMITER //

CREATE PROCEDURE GetStudentCount(
    OUT total INT
)
BEGIN
    SELECT COUNT(*)
    INTO total
    FROM students;
END //

DELIMITER ;

CALL GetStudentCount(@student_total);

SELECT @student_total AS total_students;

DELIMITER //

CREATE PROCEDURE AddTen(
    INOUT num INT
)
BEGIN
    SET num = num + 10;
END //

DELIMITER ;

SET @number = 50;
CALL AddTen(@number);
SELECT @number AS updated_number;

DELIMITER //

CREATE PROCEDURE CheckStudentGrade(
    IN p_marks INT,
    OUT p_grade VARCHAR(10)
)
BEGIN
    IF p_marks >= 90 THEN
        SET p_grade = 'A+';

    ELSEIF p_marks >= 80 THEN
        SET p_grade = 'A';

    ELSEIF p_marks >= 70 THEN
        SET p_grade = 'B';

    ELSEIF p_marks >= 60 THEN
        SET p_grade = 'C';

    ELSE
        SET p_grade = 'D';
    END IF;
END //

DELIMITER ;

CALL CheckStudentGrade(95, @grade);
SELECT @grade AS grade;

CALL CheckStudentGrade(85, @grade);
SELECT @grade AS grade;

CALL CheckStudentGrade(65, @grade);
SELECT @grade AS grade;

DELIMITER //

CREATE PROCEDURE SafeInsertStudent(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error: Student could not be inserted' AS message;
    END;

    INSERT INTO students
    (student_name, email)
    VALUES
    (p_name, p_email);

    SELECT 'Student inserted successfully' AS message;
END //

DELIMITER ;

CALL SafeInsertStudent(
    'Test User',
    'testuser123@gmail.com'
);

CALL SafeInsertStudent(
    'Test User',
    'testuser123@gmail.com'
);

SHOW PROCEDURE STATUS
WHERE Db = 'student_management';

CREATE TABLE transaction_demo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    city VARCHAR(50)
) ENGINE = InnoDB;

INSERT INTO transaction_demo (student_name, city)
VALUES
('Demo Rahul', 'Delhi'),
('Demo Priya', 'Rohtak');

SELECT * FROM transaction_demo;

START TRANSACTION;

UPDATE transaction_demo
SET city = 'Ambala'
WHERE id = 1;

SELECT * FROM transaction_demo;
ROLLBACK;
SELECT * FROM transaction_demo;

START TRANSACTION;

UPDATE transaction_demo
SET city = 'Chandigarh'
WHERE id = 2;

COMMIT;
SELECT * FROM transaction_demo;

SHOW TABLE STATUS
WHERE Name = 'transaction_demo';

SELECT * FROM transaction_demo;

START TRANSACTION;

UPDATE transaction_demo
SET city = 'Ambala'
WHERE id = 1;

SAVEPOINT first_savepoint;

UPDATE transaction_demo
SET city = 'Panipat'
WHERE id = 2;

SELECT * FROM transaction_demo;

ROLLBACK TO SAVEPOINT first_savepoint;

SELECT * FROM transaction_demo;

COMMIT;

SELECT * FROM transaction_demo;

USE student_management;

SHOW INDEX FROM students;

CREATE INDEX idx_student_city
ON students(city);

SELECT student_id, student_name, city
FROM students
WHERE city = 'Delhi';

SHOW INDEX FROM students
WHERE Key_name = 'idx_student_city';

EXPLAIN
SELECT student_id, student_name, city
FROM students
WHERE city = 'Delhi';

CREATE INDEX idx_city_gender
ON students(city, gender);

EXPLAIN
SELECT *
FROM students
WHERE city = 'Delhi'
AND gender = 'Female';


CALL StudentDashboard();