-- Er to Realtional DDL Mapping for University Course Management System

CREATE TABLE course (
  courseid int PRIMARY KEY,
  title     VARCHAR(200) NOT NULL,
  code      VARCHAR(20)  NOT NULL,
  level     VARCHAR(3)   NOT NULL,
  credits   INT          NOT NULL CHECK (credits > 0)
  --UNIQUE (code)
);



CREATE TABLE instructor (
  instructorid int PRIMARY KEY,
  name          VARCHAR(120) NOT NULL,
  email         VARCHAR(254) NOT NULL UNIQUE
);




CREATE TABLE students (
  studentid int PRIMARY KEY,
  name       VARCHAR(120) NOT NULL,
  email      VARCHAR(254) NOT NULL UNIQUE,
  major      VARCHAR(80),
  classyear VARCHAR(20)
);



CREATE TABLE room (
  roomid  int PRIMARY KEY,
  room_no  INT,
  capacity INT         NOT NULL CHECK (capacity >= 0),
  building VARCHAR(80)
);




CREATE TABLE timeslot (
  slotid    int PRIMARY KEY,
  days       VARCHAR(10),   
  start_time TIME,
  end_time   TIME,
  CHECK (end_time > start_time)
);




CREATE TABLE section (
  courseid     int   NOT NULL,         -- owner key
  sec_no        BIGINT NOT NULL,         -- partial key
  session       CHAR(1) NOT NULL,
  capacity      INT     NOT NULL CHECK (capacity >= 0),
  year          INT     NOT NULL,
  modality      VARCHAR(20) NOT NULL CHECK (modality IN ('in_person','online','hybrid')),
  term          VARCHAR(10) NOT NULL CHECK (term IN ('Fall','Spring','Summer')),

  PRIMARY KEY (courseid, sec_no),

  FOREIGN KEY (courseid)     REFERENCES course(courseid)         ON DELETE CASCADE
);




-- M:N relationship between Student and Section
CREATE TABLE enrolled (
  studentid int   NOT NULL,
  courseid  int   NOT NULL,
  sec_no     BIGINT NOT NULL,

  PRIMARY KEY (studentid, courseid, sec_no),
  FOREIGN KEY (studentid)             REFERENCES students(studentid)           ON DELETE CASCADE,
  FOREIGN KEY (courseid, sec_no)      REFERENCES section(courseid, sec_no)    ON DELETE CASCADE
);




-- Teaches (Instructor — Section) - Junction Table
CREATE TABLE teaches (
  sec_no      BIGINT NOT NULL,
  courseid    int   NOT NULL,
  instructorid int   NOT NULL,

  PRIMARY KEY (sec_no, courseid, instructorid),
  FOREIGN KEY (courseid, sec_no)      REFERENCES section(courseid, sec_no)    ON DELETE CASCADE,
  FOREIGN KEY (instructorid)          REFERENCES instructor(instructorid)     ON DELETE RESTRICT
);


-- Scheduled_at (TimeSlot — Section) - Junction Table
CREATE TABLE scheduled_at (
  sec_no   BIGINT NOT NULL,
  courseid int   NOT NULL,
  slotid   int   NOT NULL,

  PRIMARY KEY (sec_no, courseid, slotid),
  FOREIGN KEY (courseid, sec_no)   REFERENCES section(courseid, sec_no)   ON DELETE CASCADE,
  FOREIGN KEY (slotid)             REFERENCES timeslot(slotid)            ON DELETE RESTRICT
);


-- Located_at (Room — Section) - Junction Table
CREATE TABLE located_at (
  sec_no   BIGINT NOT NULL,
  courseid int   NOT NULL,
  roomid   int       NULL,

  PRIMARY KEY (sec_no, courseid, roomid),
  FOREIGN KEY (courseid, sec_no)   REFERENCES section(courseid, sec_no)   ON DELETE CASCADE,
  FOREIGN KEY (roomid)             REFERENCES room(roomid)                ON DELETE SET NULL
);














