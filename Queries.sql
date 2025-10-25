-- 1) INSERT #1
INSERT INTO student (Student_id, Name, Email, Major, Class_year)
VALUES (122700571, 'Sarah Lee', 'sarah@asu.edu', 'Software Engineering', 'Sophomore')
ON CONFLICT (Student_id) DO NOTHING;


SELECT * FROM student WHERE Student_id = 122700571;


-- 2) INSERT #2
INSERT INTO enrolled (Sec_no, Course_id, Student_id)
VALUES (3, 1, 122700571)
ON CONFLICT DO NOTHING;


SELECT * FROM enrolled WHERE Student_id = 122700571;


-- 3) UPDATE
UPDATE section
SET Modality = 'online'
WHERE Sec_no = 2 AND Course_id = 1;


SELECT Sec_no, Course_id, Modality
FROM section
WHERE Sec_no = 2 AND Course_id = 1;


-- 4) DELETE
DELETE FROM enrolled
WHERE Student_id = 2 AND Sec_no = 2 AND Course_id = 1;


SELECT * FROM enrolled WHERE Student_id = 2;


-- 5) SELECT #1
SELECT s.Student_id,
      s.Name AS StudentName,
      c.Title AS CourseTitle,
      se.Sec_no,
      se.Term,
      se.Year
FROM enrolled e
JOIN student s ON e.Student_id = s.Student_id
JOIN section se ON e.Sec_no = se.Sec_no AND e.Course_id = se.Course_id
JOIN course c ON se.Course_id = c.Course_id
WHERE s.Student_id = 122700571;


-- 6) SELECT #2
SELECT se.Sec_no,
      se.Course_id,
      se.Capacity,
      COALESCE(se.Capacity - COUNT(e.Student_id), se.Capacity) AS SeatsAvailable
FROM section se
LEFT JOIN enrolled e
      ON se.Sec_no = e.Sec_no AND se.Course_id = e.Course_id
GROUP BY se.Sec_no, se.Course_id, se.Capacity
ORDER BY se.Sec_no;


