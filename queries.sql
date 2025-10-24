-- 1) Insert
INSERT INTO students (StudentId, Name, Email, Major, ClassYear)
VALUES (122700570, 'Daniel Park', 'daniel@asu.edu', 'Computer Science', 'Freshman');

-- 2) Update
UPDATE section
SET Modality = 'online'
WHERE Sec_no = 2 AND CourseId = 1;

-- 3) Delete
DELETE FROM enrolled
WHERE StudentId = 122700570 AND Sec_no = 3 AND CourseId = 1;

-- 4) Select #1
SELECT s.StudentId, s.Name AS StudentName, c.Title AS CourseTitle, se.Sec_no, se.Term, se.Year
FROM enrolled e
JOIN students s ON e.StudentId = s.StudentId
JOIN section se ON e.Sec_no = se.Sec_no AND e.CourseId = se.CourseId
JOIN course c ON se.CourseId = c.CourseId
WHERE s.StudentId = 122700567;

-- 5) Select #2
SELECT se.Sec_no, se.CourseId, se.Capacity,
       COALESCE(se.Capacity - COUNT(e.StudentId), se.Capacity) AS SeatsAvailable
FROM section se
LEFT JOIN enrolled e ON se.Sec_no = e.Sec_no AND se.CourseId = e.CourseId
GROUP BY se.Sec_no, se.CourseId, se.Capacity
ORDER BY se.Sec_no;
