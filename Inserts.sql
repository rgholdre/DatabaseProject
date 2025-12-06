-- INSERT STATEMENTS TO POPULATE THE TABLES WITH AT LEAST 10 TUPLES PER TABLE 

-- Instructors
INSERT INTO instructor (instructorid, name, email) VALUES
(1, 'Soumya Indela', 'soumyai@university.edu'),
(2, 'Ryan Meuth', 'ryan.meuth@university.edu'),
(3, 'Erik Trickel', 'erik.trickel@university.edu'),
(4, 'James Gordon', 'james.gordon@university.edu'),
(5, 'Xuerong Feng', 'xuerong.feng@university.edu'),
(6, 'Janaka Balasooriya', 'janaka.balasooriya@university.edu'),
(7, 'Bharatesh Chakravarthi', 'bharatesh.chakravarthi@university.edu'),
(8, 'Swathi Punathumkandi', 'swathi.punathumkandi@university.edu'),
(9, 'Yoshihiro Kobayashi', 'yoshihiro.kobayashi@university.edu'),
(10, 'Ozgur Ozmen', 'ozgur.ozmen@university.edu'),
(11, 'Ming Zhao', 'ming.zhao@university.edu'),
(12, 'David Claveau', 'david.claveau@university.edu');



-- Courses
INSERT INTO course (courseid, title, credits, level, code) VALUES
(1, 'Principles of Programming with C++', 3, '1XX', 'CSE100'),
(2, 'Principles of Programming', 3, '1XX', 'CSE110'),
(3, 'Object-Oriented Programming and Data Structures', 3, '2XX', 'CSE205'),
(4, 'Introduction to Programming Languages', 3, '2XX', 'CSE240'),
(5, 'Introduction to Programming Languages', 3, '2XX', 'CSE240'),
(6, 'Data Structures and Algorithms', 3, '3XX', 'CSE310'),
(7, 'Data Structures and Algorithms', 3, '3XX', 'CSE310'),
(8, 'Database Management', 3, '4XX', 'CSE412'),
(9, 'Applied Cryptography', 3, '5XX', 'CSE539'),
(10, 'Engineering Blockchain Applications', 3, '5XX', 'CSE540'),
(11, 'Principles of Programming with C++', 3, '1XX', 'CSE100'),
(12, 'Computer Organization & Assembly Language Program', 3, '2XX', 'CSE230'),
(13, 'Operating Systems', 3, '3XX', 'CSE330'),
(14, 'Introduction to Theoretical Computer Science', 3, '3XX', 'CSE330');



-- Students
INSERT INTO students (studentid, name, email, major, classyear) VALUES
(1,'Alice Kim','alice.kim@university.edu','Computer Science','Sophomore'),
(2,'John Rivera','john.rivera@university.edu','Software Engineering','Junior'),
(3,'Maria Lopez','maria.lopez@university.edu','Computer Science','Senior'),
(4,'David Chen','david.chen@university.edu','Information Systems','Freshman'),
(5,'Emily Zhang','emily.zhang@university.edu','Computer Science','Sophomore'),
(6,'Michael Brown','michael.brown@university.edu','Software Engineering','Junior'),
(7,'Sarah Patel','sarah.patel@university.edu','Information Systems','Senior'),
(8,'James Lee','james.lee@university.edu','Computer Science','Freshman'),
(9,'Olivia Davis','olivia.davis@university.edu','Software Engineering','Sophomore'),
(10,'Daniel Wilson','daniel.wilson@university.edu','Computer Science','Junior'),
(11,'Sophia Martinez','sophia.martinez@university.edu','Information Systems','Senior'),
(12,'Anthony Garcia','anthony.garcia@university.edu','Computer Science','Sophomore'),
(13,'Isabella Hernandez','isabella.hernandez@university.edu','Software Engineering','Junior'),
(14,'Ethan Moore','ethan.moore@university.edu','Computer Science','Senior'),
(15,'Mia Clark','mia.clark@university.edu','Information Systems','Freshman'),
(16,'Alexander Lewis','alex.lewis@university.edu','Computer Science','Sophomore'),
(17,'Charlotte Walker','charlotte.walker@university.edu','Software Engineering','Junior'),
(18,'Benjamin Hall','benjamin.hall@university.edu','Computer Science','Senior'),
(19,'Amelia Allen','amelia.allen@university.edu','Information Systems','Freshman'),
(20,'Lucas Young','lucas.young@university.edu','Computer Science','Sophomore');



-- Rooms
INSERT INTO room (roomid, capacity, building, room_no) VALUES
(1,125,'PSH',152),
(2,400,NULL,NULL),
(3,75,'LIBC',5),
(4,150,'MUR',201),
(5,180,'COOR',170),
(6,150,NULL,NULL),
(7,150,'CDN',60),
(8,150,'SCOB',210),
(9,185,'LSE',104),
(10,166,'PSH',153),
(11,80,'HLMK',351),
(12,160,'PSH',152),
(13,150,'EDC',117);




-- TimeSlots
INSERT INTO timeslot (slotid, start_time, end_time, days) VALUES
(1,'15:00:00','16:15:00','T TH'),
(2,'12:00:00','13:15:00','M'),
(3,'09:00:00','10:15:00','M W'),
(4,NULL,NULL,NULL), -- for online/hybrid without time
(5,'12:00:00','13:15:00','T TH'),
(6,'12:00:00','13:15:00','M W'),
(7,'15:00:00','16:15:00','M W'),
(8,'12:20:00','13:10:00','M W F'),
(9,'10:30:00','11:45:00','TH'),
(10,'16:30:00','17:45:00','M W'),
(11,'09:00:00','10:15:00','T TH');




-- Sections
INSERT INTO section (courseid, sec_no, session, capacity, year, modality, term) VALUES
  (1, 12440, 'C', 125, 2026, 'in_person', 'Spring'),
  (2, 13452, 'A', 400, 2026, 'online',    'Spring'),
  (3, 10944, 'C', 900, 2026, 'hybrid',    'Spring'),
  (4, 28757, 'C',  75, 2026, 'hybrid',    'Spring'),
  (5, 12431, 'C', 150, 2026, 'in_person', 'Spring'),
  (6, 11251, 'C', 180, 2026, 'in_person', 'Spring'),
  (7, 26859, 'C', 150, 2026, 'online',    'Spring'),
  (8, 19439, 'C', 150, 2026, 'in_person', 'Spring'),
  (9, 39019, 'B', 150, 2026, 'hybrid',    'Spring'),
  (10,34956, 'B', 185, 2026, 'in_person', 'Spring'),
  (11,64018, 'C', 166, 2025, 'in_person', 'Fall'),
  (12,79248, 'C',  80, 2025, 'hybrid',    'Fall'),
  (13,76906, 'C', 160, 2025, 'in_person', 'Fall'),
  (14,75974, 'C', 150, 2025, 'in_person', 'Fall');

-- Teaches (link instructors to sections)
INSERT INTO teaches (sec_no, courseid, instructorid) VALUES
  (12440, 1, 1),
  (13452, 2, 2),
  (10944, 3, 2),
  (28757, 4, 3),
  (12431, 5, 4),
  (11251, 6, 5),
  (26859, 7, 6),
  (19439, 8, 7),
  (39019, 9, 8),
  (34956, 10, 8),
  (64018, 11, 9),
  (79248, 12, 10),
  (76906, 13, 11),
  (75974, 14, 12);

-- Scheduled_at (link sections to timeslots)
INSERT INTO scheduled_at (sec_no, courseid, slotid) VALUES
  (12440, 1, 1),
  (13452, 2, 4),
  (10944, 3, 4),
  (28757, 4, 2),
  (12431, 5, 1),
  (11251, 6, 3),
  (26859, 7, 4),
  (19439, 8, 5),
  (39019, 9, 6),
  (34956, 10, 7),
  (64018, 11, 8),
  (79248, 12, 9),
  (76906, 13, 10),
  (75974, 14, 11);

-- Located_at (link sections to rooms)
INSERT INTO located_at (sec_no, courseid, roomid) VALUES
  (12440, 1, 1),
  (10944, 3, 3),
  (28757, 4, 3),
  (12431, 5, 4),
  (11251, 6, 5),
  (19439, 8, 7),
  (39019, 9, 8),
  (34956, 10, 9),
  (64018, 11, 10),
  (79248, 12, 11),
  (76906, 13, 12),
  (75974, 14, 13);

-- Enrolled (randomly assigns 1–3 courses per student)
INSERT INTO enrolled (sec_no, courseid, studentid) VALUES
(12440,1,1),(13452,2,1),(11251,6,1),
(10944,3,2),(12431,5,2),
(28757,4,3),(39019,9,3),(34956,10,3),
(12440,1,4),(11251,6,4),
(13452,2,5),(12431,5,5),(19439,8,5),
(10944,3,6),(34956,10,6),
(12440,1,7),(39019,9,7),
(11251,6,8),(12431,5,8),
(13452,2,9),(12440,1,9),(10944,3,9),
(19439,8,10),
(34956,10,11),(75974,14,11),
(64018,11,12),(76906,13,12),
(12440,1,13),(28757,4,13),
(11251,6,14),
(12431,5,15),(39019,9,15),
(13452,2,16),(10944,3,16),
(12440,1,17),(34956,10,17),
(11251,6,18),(75974,14,18),
(64018,11,19),(12431,5,19),
(12440,1,20),(13452,2,20),(10944,3,20);
