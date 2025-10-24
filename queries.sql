-- 1) INSERT #1
INSERT INTO students (StudentId, Name, Email, Major, ClassYear)
VALUES (122700571, 'Sarah Lee', 'sarah@asu.edu', 'Software Engineering', 'Sophomore')
ON CONFLICT (StudentId) DO NOTHING;

SELECT * FROM students WHERE StudentId = 122700571;

-- 2) INSERT #2
INSERT INTO enrolled (Sec_no, CourseId, StudentId)
VALUES (3, 1, 122700571)
ON CONFLICT DO NOTHING;

SELECT * FROM enrolled WHERE StudentId = 122700571;

-- 3) UPDATE
UPDATE section
SET Modality = 'online'
WHERE Sec_no = 2 AND CourseId = 1;

SELECT Sec_no, CourseId, Modality
FROM section
WHERE Sec_no = 2 AND CourseId = 1;

-- 4) DELETE
DELETE FROM enrolled
WHERE StudentId = 2 AND Sec_no = 2 AND CourseId = 1;

SELECT * FROM enrolled WHERE StudentId = 2;

-- 5) SELECT #1
SELECT s.StudentId,
       s.Name AS StudentName,
       c.Title AS CourseTitle,
       se.Sec_no,
       se.Term,
       se.Year
FROM enrolled e
JOIN students s ON e.StudentId = s.StudentId
JOIN section se ON e.Sec_no = se.Sec_no AND e.CourseId = se.CourseId
JOIN course c ON se.CourseId = c.CourseId
WHERE s.StudentId = 122700571;

-- 6) SELECT #2
SELECT se.Sec_no,
       se.CourseId,
       se.Capacity,
       COALESCE(se.Capacity - COUNT(e.StudentId), se.Capacity) AS SeatsAvailable
FROM section se
LEFT JOIN enrolled e
       ON se.Sec_no = e.Sec_no AND se.CourseId = e.CourseId
GROUP BY se.Sec_no, se.CourseId, se.Capacity
ORDER BY se.Sec_no;
