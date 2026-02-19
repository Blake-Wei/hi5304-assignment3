--Mastering SQL JOINS for HI 5304 
--Edits by Haley Kosker in preparation for class 2/19/26
------------------------------------------------------------
/*
Use the Mastering_SQL file to get started in the terminal and build tables
Use the Mastering_SQL_Syntax to learn how to pull SQL queries from one table
In this file, we will pull multiple tables with examples
*/ 


/*JOINS
Definitions: 
Primary Key: Unique identifier in the table; all tables should have a primary key
Foreign Key: A column in a table that links to the primary key in another table, creating a relationship between the two tables
Most common Joins: 
--INNER JOIN: Returns only matching elements
--LEFT JOIN: Returns all values from Left (or first) table, and matching elements from the second table

Less common: 
--RIGHT JOIN: Returns all values from Right (or second) table, and matching elements from the first table
--FULL OUTER JOIN: Returns all values from both tables, even if no matches are found on common ID/key
*/

--Using the example of Patients and Medications tables

SELECT 
p.patient_id,
p.first_name,
p.last_name,
m.medication_name,
m.patient_id
FROM patients p --table alias as p
INNER JOIN medications m on m.patient_id = p.patient_id;



SELECT 
p.patient_id,
p.first_name,
p.last_name,
m.medication_name,
m.patient_id
FROM patients p --table alias as p
LEFT JOIN medications m on m.patient_id = p.patient_id;


SELECT 
p.patient_id,
p.first_name,
p.last_name,
m.medication_name,
m.patient_id
FROM patients p --table alias as p
RIGHT JOIN medications m on m.patient_id = p.patient_id;
--Returns the same as an inner join in this scenario 
----what if we start with the medication table?

SELECT 
p.patient_id,
p.first_name,
p.last_name,
m.medication_name,
m.patient_id
FROM patients p --table alias as p
FULL OUTER JOIN medications m on m.patient_id = p.patient_id;
--Returns the same as the left join in this scenario
---what if we start with the medication table? 

--Multiple JOINS: 

SELECT 
p.patient_id,
p.last_name,
m.patient_id,
m.med_id,
m.medication_name,
b.patient_id,
b.bp_id,
b.heart_rate
FROM patients p 
LEFT JOIN medications m on m.patient_id = p.patient_id
LEFT JOIN bloodpressure_log b on b.patient_id = p.patient_id;
--Returns all patients and medications and blood pressure log
----effectively just combined all 3 tables, but what is duplicating and WHY


--How do we return distinct patients, medication, and BP? 
----We need to define granularity: 
----Patients can have more than one medication
----Patients can have more than one bp reading
----when we try to combine this into one table, we duplicate records, because there's no direct relationship between bp and medication


--Instead, we could return distinct count of medications, distinct reading of BP, or last BP reading taken: 

--All 3 tables with distinct count of meds per patients and BP readings: 
SELECT 
p.patient_id,
p.last_name,
count(m.med_id) as Count_Medications,
b.patient_id,
count(b.bp_id) as Count_bp_readings
FROM patients p 
LEFT JOIN medications m on m.patient_id = p.patient_id
LEFT JOIN bloodpressure_log b on b.patient_id = p.patient_id
GROUP BY 
p.patient_id,
p.last_name,
b.patient_id
ORDER BY p.patient_Id;

--Last BP reading
SELECT 
p.patient_id,
p.last_name,
count(m.med_id) as Count_Medications,
b.patient_id,
max(reading_date)
FROM patients p 
LEFT JOIN medications m on m.patient_id = p.patient_id
LEFT JOIN bloodpressure_log b on b.patient_id = p.patient_id
GROUP BY 
p.patient_id,
p.last_name,
b.patient_id
ORDER BY p.patient_Id;
