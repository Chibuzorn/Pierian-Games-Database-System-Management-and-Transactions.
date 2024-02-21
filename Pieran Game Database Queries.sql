Create Schema "PIERAN_GAME_DATABASE";
Set SEARCH_PATH to "PIERAN_GAME_DATABASE", public;

-----Creating event table
CREATE TABLE event(
    ecode        CHAR(4)PRIMARY KEY not null,
    edesc        VARCHAR(20) not null,
    elocation    VARCHAR(20) not null,
    edate        DATE check (edate >= '2024-07-01' and edate<='2024-07-31') NOT NULl,
    etime        TIME check (etime >= '9:00:00') NOT NULL,
    emax         SMALLINT check (emax >= 1 and emax<=1000) NOT NULL);
----To see that event table has been created
select* from event;
-----Creating spectator table
CREATE TABLE spectator (
    sno          INTEGER  primary key,
    sname        VARCHAR(20) not null check (sname<>'  '),
    semail       VARCHAR(20)unique not null);
	
----To see that spectator table has been created
select* from spectator;

-----Creating ticket table
CREATE TABLE ticket (
   tno          INTEGER primary key not null,
   ecode        CHAR(4) ,
   sno          INTEGER,
FOREIGN KEY (ecode) REFERENCES event (ecode)  ON DELETE set null,
FOREIGN KEY (sno) REFERENCES spectator(sno)  ON DELETE set null);

----To see that ticket table has been created
select* from ticket;

-----Creating cancel table
CREATE TABLE cancel (
    tno          INTEGER unique not null,
    ecode        CHAR(4),
    sno          INTEGER ,
    cdate        TIMESTAMP default CURRENT_TIMESTAMP not null,
    cuser        VARCHAR(128) default 'Esther123' not null, 
	PRIMARY KEY (tno, cdate));

----To see that cancel table has been created
select* from cancel;

---Sample records for the event table
INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES
 ('E001','Game Launch Party','City Convention','2024-07-01','10:00:00',1000),
 ('E002','Tennis','Tennis Court','2024-07-05','12:00:00',500 ),
 ('E003','Basketball','Sportspark','2024-07-08','9:00:00',650),
 ('E004','football','Arena Stadium','2024-07-18','9:00:00',1000),
 ('E005','VR Gaming Experience','Co-Working Space','2024-07-23','11:00:00',450),
 ('E006','martial arts','Arena Stadium','2024-07-28','12:00:00',1000),
 ('E007','Game Awards Ceremony','Grand Theater','2024-07-31','10:00:00',1000);
 
---Selecting the event table to see the records
Select * from event;

---Sample records for the Spectator table
INSERT INTO spectator (sno,sname,semail) VALUES
 (1001,'Alice Johnson','alice.j@gmail.com'),
 (1002,'Bob Smith','bob.smith@yahoo.com'),
 (1003,'Carla Davis','carla.d@gmail.com'),
 (1004,'David Miller','david.m@gmail.com'),
 (1005,'Emily Wilson','emily.w@yahoo.com'),
 (1006,'Frank Brown','frank.b@yahoo.com'),
 (1007,'Grace Martinez','grace.m@yahoo.com'),
 (1008,'Joy Madu','joy.m@yahoo.com'),
 (1009,'Tomisin Okuns','Tomisin.o@gmail.com'),
 (1010,'neringa chioma','neringa.c@yahoo.com');
 
---Selecting the spectator table to see the records
Select * from spectator;

-- Sample records for the ticket table ectator 
INSERT INTO ticket VALUES 
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E001',  1001);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E002',  1002);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E003',  1003);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E003',  1004);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E004',  1005);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E005',  1006);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E006',  1007);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1,'E007',  1008);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E004',  1009);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E001',  1010);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E003',  1001);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E005',  1004);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E006',  1004);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1,'E001',  1003);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E001',  1002);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E001',  1004);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E007',  1004);
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1,  'E002',  1008);
  
----Selecting the ticket table to see the records
Select * from ticket;
 
-----records for cancel should be done with a function
-----creating function for ticket cancellation
CREATE OR REPLACE FUNCTION log_ticket_cancellation()
RETURNS TRIGGER AS $$
BEGIN
       INSERT INTO cancel (tno,ecode,sno,cdate,cuser)
       VALUES (OLD.tno,OLD.ecode,OLD.sno,DEFAULT,DEFAULT);
    RETURN new;
END;
$$ LANGUAGE plpgsql;

-- Creating the "ticket delete" trigger
CREATE TRIGGER TICKET_DELETES
AFTER  DELETE
ON ticket
FOR EACH ROW
EXECUTE FUNCTION log_ticket_cancellation();



--Transaction of interest for Data Manipulation

--A. Inserting a new spectator into the spectator table
INSERT INTO spectator (sno,sname,semail) VALUES
 (1011,'Nnedu Esther','nnedu.E@gmail.com');

--To show that the values were inserted into the spectator table
Select*from spectator where sno=1011;




--B. Inserting a new event into the event table
INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES
 ('E008','ricket','ricket court','2024-07-24','10:00:00',750);
 
--To show that the values were inserted into the event table
Select*from event where ecode='E008';






--C. Delete a spectator. 
--The spectator must not have any valid (i.e. not cancelled) tickets,
--before it can be deleted.
--A function has to be created to check for valid tickets,
--before a spectator can be deleted
CREATE OR REPLACE FUNCTION delete_spectator(sno_be_be_deleted INT)
returns void as $$
begin
     if exists (select from ticket where sno=sno_be_be_deleted) then
	   raise exception 'This Spectator has valid tickets ';
     else
	 delete from spectator where sno=sno_be_be_deleted;
     end if;
end;
$$ language plpgsql;
---executiong the query
select delete_spectator(1001);
---output shows it has ticket so it prevents the deletion of the spectator
 
--D. Delete an event.
---All the tickets for the event must be cancelled before an event can be deleted.
--to confirm that the event I want to delete has a ticket.
Select * from ticket where ecode='E006'
--i can see it has  tickets, now i will delete the tickets and the event.
---using two queries,making the first query a temporary table using the 'with' clause,
WITH DeletedTickets AS (
    DELETE FROM ticket
    WHERE ecode = 'E006'
	returning *
)
DELETE FROM event
WHERE ecode = 'E006'
  AND EXISTS (SELECT * FROM DeletedTickets);

--To confirm the ecode deleted is not in the event and spectator table;
select* from event where ecode='E006';
select* from ticket where ecode='E006';

---E.Issue a ticket for an event. A spectator may have only one ticket for a given event.
--function for checking multiple tickets and Trigger before inserting ticket has been created,
--refer to DDl text file please 

--checking my functions by issuing  ticket to a spectator for same event
INSERT INTO ticket VALUES
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E003',  1004);
		
--error shows spectator has ticket for the event, so inserting another ticket
--so lets issue the spectator ticket for another event
INSERT INTO ticket (tno, ecode, sno) 
VALUES 
  ((SELECT COALESCE(MAX(tno), 0) FROM ticket)+ 1, 'E004',  1004);
--To see the inserted ticket
select*from ticket where ecode='E004';

---F. Produce a report showing the total number of spectators liable to travel to a 
---location. The table should show the total number of spectators that could travel to a 
---location on each date an event is held at a location
----create view here
CREATE VIEW "Report_for_spectators" AS 
select count(distinct sno) as total_spectators,e.elocation,e.edate from event e
left join
ticket t on e.ecode=t.ecode
group by e.elocation,e.edate;
---to see the report we then select the view
select* from "Report_for_spectators";







---G. Produce a report showing the total number of tickets issued for each event. 
---Present the data in event description sequence.
----create view here
CREATE VIEW "Report_for_tickets" AS 
select count(tno) as total_tickets,e.edesc from event e
left join
ticket t on e.ecode=t.ecode
group by e.edesc
Order by e.edesc;
---to see the report we then select the view
select* from "Report_for_tickets";



---H As task G but only for a given event which is specified by the event code
select count(tno) as total_tickets,e.edesc from event e
LEFT join
ticket t on e.ecode=t.ecode
where e.ecode='E001'
group by e.edesc;

--- i.Produce a report showing the schedule for a given spectator. The spectator is 
---specified by his/her spectator number. The schedule should contain the spectator's 
---name and the date, location, time and event description of each event for which the 
---spectator has been issued a ticket.
select s.sname,e.edate,e.elocation,e.etime,e.edesc from spectator s, ticket t, event e
where e.ecode=t.ecode and s.sno=t.sno and s.sno=1002
group by e.edesc,s.sname,e.edate,e.elocation,e.etime;

---J. Given a specific ticket reference number, display the name of the spectator and 
---the event code for the ticket and indicate if the ticket is valid or is cancelled.
------using a ticket number that is valid
select  sname,
COALESCE(t.ecode, c.ecode) AS ecode,
case
when c.tno is not null then 'cancelled'
else'valid'
end as indication
from spectator s
full outer join
ticket t on s.sno=t.sno
full outer join 
cancel c on t.tno=c.tno and t.ecode=c.ecode and t.sno=
c.sno
where t.tno=2 or c.tno=2; 

------using a ticket number that is cancelled
select* from cancel;
--selecting query
select  sname,
COALESCE(t.ecode, c.ecode) AS ecode,
case
when c.tno is not null then 'cancelled'
else'valid'
end as indication
from spectator s
full outer join
ticket t on s.sno=t.sno
full outer join 
cancel c on t.tno=c.tno and t.ecode=c.ecode and t.sno=c.sno
where t.tno=7 or c.tno=7; 
		
---k.. View the details of all cancelled tickets for a specific event.
select * from Cancel
where ecode='E006';

---Checking constarints of my own data
1.--check constarints of time, date and emax.
--(i)
INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES
 ('E011','Game Launch ','City Convention','2024-08-01','9:00:00',100);
--(ii) 
 INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES
 ('E011','Game Launch ','City Convention','2024-07-01','8:00:00',100);
--(iii)
INSERT INTO event (ecode, edesc, elocation,edate,etime,emax) VALUES
 ('E011','Game Launch ','City Convention','2024-07-01','9:00:00',1050);
 
2.--checking foriegn key constarints 
INSERT INTO ticket VALUES 
    ((SELECT COALESCE(MAX(tno),0) FROM ticket) + 1, 'E001',  1015);

3.--checking unique constraints
--checking sno unique constarint
INSERT INTO spectator (sno,sname,semail) VALUES
 (1005,'Alice John','alice.jo@gmail.com');
 
--checking semail unique constarint
INSERT INTO spectator (sno,sname,semail) VALUES
 (1015,'Alice John','alice.j@gmail.com');

---L.Delete the content of the database table
--deleting content of event table
delete from event;
---to see that all the content has been deleted from the tables
select * from event;

--deleting content of spectator table
delete from spectator;
---to see that all the content has been deleted from the tables
select * from spectator;

--deleting content of ticket table
delete from ticket;
---to see that all the content has been deleted from the tables
select * from ticket;

--deleting content of cancel table
delete from cancel;
---to see that all the content has been deleted from the tables
select * from cancel;

 

 
	

	

