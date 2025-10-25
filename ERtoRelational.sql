

CREATE TABLE Course (
  course_id UUID PRIMARY KEY,
  title     VARCHAR(200) NOT NULL,
  code      VARCHAR(20)  NOT NULL,
  level     INT          NOT NULL,
  credits   INT          NOT NULL CHECK (credits > 0),
  UNIQUE (code)
);



CREATE TABLE Instructor (
  instructor_id UUID PRIMARY KEY,
  name          VARCHAR(120) NOT NULL,
  email         VARCHAR(254) NOT NULL UNIQUE
);




CREATE TABLE Student (
  student_id UUID PRIMARY KEY,
  name       VARCHAR(120) NOT NULL,
  email      VARCHAR(254) NOT NULL UNIQUE,
  major      VARCHAR(80),
  class_year VARCHAR(20)
);



CREATE TABLE Room (
  room_id  UUID PRIMARY KEY,
  room_no  INT         NOT NULL,
  capacity INT         NOT NULL CHECK (capacity >= 0),
  building VARCHAR(80) NOT NULL,
  UNIQUE (building, room_no)
);




CREATE TABLE TimeSlot (
  slot_id    UUID PRIMARY KEY,
  days       VARCHAR(10) NOT NULL,   
  start_time TIME        NOT NULL,
  end_time   TIME        NOT NULL,
  CHECK (end_time > start_time)
);




CREATE TABLE Section (
  course_id     UUID   NOT NULL,         -- owner key
  sec_no        BIGINT NOT NULL,         -- partial key
  session       CHAR(1) NOT NULL,
  capacity      INT     NOT NULL CHECK (capacity >= 0),
  year          INT     NOT NULL,
  modality      VARCHAR(20) NOT NULL CHECK (modality IN ('in_person','online','hybrid')),
  term          VARCHAR(10) NOT NULL CHECK (term IN ('Fall','Spring','Summer')),

  instructor_id UUID   NOT NULL,         -- exactly one instructor
  slot_id       UUID   NOT NULL,         -- exactly one timeslot
  room_id       UUID       NULL,         -- optional room (online allowed)

  PRIMARY KEY (course_id, sec_no),


  FOREIGN KEY (course_id)     REFERENCES Course(course_id)         ON DELETE CASCADE,
  FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id) ON DELETE RESTRICT,
  FOREIGN KEY (slot_id)       REFERENCES TimeSlot(slot_id)         ON DELETE RESTRICT,
  FOREIGN KEY (room_id)       REFERENCES Room(room_id)             ON DELETE SET NULL
);



-- Avoid double-booking a room in a slot: a partial unique index to ignore NULL room_id
CREATE UNIQUE INDEX uq_section_room_slot
  ON Section(room_id, slot_id)
  WHERE room_id IS NOT NULL;




-- M:N relationship between Student and Section
CREATE TABLE Enrollment (
  student_id UUID   NOT NULL,
  course_id  UUID   NOT NULL,
  sec_no     BIGINT NOT NULL,
  enrolled_at TIMESTAMP NOT NULL DEFAULT now(),

  PRIMARY KEY (student_id, course_id, sec_no),
  FOREIGN KEY (student_id)             REFERENCES Student(student_id)           ON DELETE CASCADE,
  FOREIGN KEY (course_id, sec_no)      REFERENCES Section(course_id, sec_no)    ON DELETE CASCADE
);




-- Offered_as (Course — Section)
CREATE OR REPLACE VIEW Offered_as AS
SELECT course_id, sec_no
FROM Section;


-- Teaches (Instructor — Section)
CREATE OR REPLACE VIEW Teaches AS
SELECT instructor_id, course_id, sec_no
FROM Section;


-- Scheduled_at (TimeSlot — Section)
CREATE OR REPLACE VIEW Scheduled_at AS
SELECT slot_id, course_id, sec_no
FROM Section;


-- Located_at (Room — Section)
CREATE OR REPLACE VIEW Located_at AS
SELECT room_id, course_id, sec_no
FROM Section
WHERE room_id IS NOT NULL;














