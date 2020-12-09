USE data;

--DELETE FROM patients;
--DELETE FROM appointments;
--ALTER TABLE patients AUTO_INCREMENT=1;
--ALTER TABLE appointments AUTO_INCREMENT=1;

INSERT INTO patients (firstname,lastname,date_of_birth,consulting_staff)
VALUES 
("Mark","Reilly","1949-06-25",2),
("Jay","Ramsey","1961-02-28",1),
("Hannah","Holt","1964-08-01",2),
("Tyrone","Middleton","1966-03-03",3),
("Lyra","Kennedy","1968-05-11",1),
("Charlotte","Hopkins","1983-05-16",NULL),
("Myles","Bernard","1985-02-21",NULL),
("Laura","Griffith","1997-04-09",3),
("David","McCoy","1999-06-01",3),
("David","Rodriguez","2002-06-10",3),
("Hannah","Anniston","1975-09-15",NULL),
("David","Freeman","1954-03-21",2);

INSERT INTO appointments (date, time, patient_id, consulting_staff)
VALUES
('2020-12-20','16:00',1,2),
('2020-12-20','17:00',3,1),
('2020-12-20','17:30',2,4),
('2020-12-20','18:00',6,1),
('2020-12-21','12:00',3,1),
('2020-12-21','18:00',2,4),
('2020-12-21','18:30',7,2),
('2020-12-22','13:00',9,NULL),
('2020-12-23','14:30',5,NULL),
('2021-01-15','17:00',3,1),
('2021-01-16','16:30',12,4),
('2021-01-16','18:30',11,8),
('2021-01-16','16:30',10,4),
('2021-01-20','12:30',4,1),
('2021-01-25','16:30',12,4),
('2021-01-10','10:30',1,2),
('2021-01-28','11:00',7,4);