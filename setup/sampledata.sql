USE data;

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
("David","Mccoy","1999-06-01",3);

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
('2021-01-15','17:00',3,1);