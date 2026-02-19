--Mastering SQL Syntax for HI 5304 
--Edits by Haley Kosker in preparation for class 2/19/26
------------------------------------------------------------
/*
In GitHub Codespaces, the interface looks a little different than traditional SQL interfaces like pgadmin, SSMS, etc.
These traditional interfaces are database applications; Codespaces is a development environment using a terminal
We can think of a terminal as a gateway to PostgreSQL or Python. We must connect to these systems from the terminal
Use the Mastering_SQL file to get started in the terminal and build tables
*/ 

-------------------------------------------------------------
--Basic Syntax in SQL: 
-- two dashes comment out lines of code for documentation and testing
/* similarly, a slash-star, followed by star-slash will comment out 
multiple lines of code without adding the dashes */
--These both turn your text green denoting comments, not SQL you can execute




--Basic Select statement, using the medications table created:  
SELECT * 
FROM medications ;
--Will return all column names and rows of data from the table
--CAUTION with SELECT * 
----This pulls all records. When you have complex queries or many rows of data, it's best practice to limit the number of rows returned:


SELECT * 
FROM medications
LIMIT 10 ;
--This limits to 10 records returned from the table

--ORDER BY
SELECT 
med_id, 
patient_id, 
medication_name
FROM medications
ORDER BY medication_name;
--Returns only the 3 columns listed , with an order by 

SELECT 
med_id, 
patient_id, 
medication_name
FROM medications
ORDER BY medication_name desc; 
--Returns the order by field in descending order (works with numeric, alpha, dates)



SELECT DISTINCT 
medication_name,
patient_id
FROM medications;
--Returns only distinct column combinations



--Filtering: Adding WHERE clauses to the select statements: 

SELECT 
medication_name,
dose, 
frequency
FROM medications
WHERE patient_Id = '1003';
--Returns medications for only patient_id 1003

SELECT 
medication_name,
dose, 
frequency
FROM medications
WHERE frequency like '%daily%'; --'daily%' --'%daily' --try the different variations
--Returns medications that have frequency with "daily" in the name
--a % on the front of a field will search anything + field_name 
----for example: like '%daily' will return all records with '____daily', like 'once daily'
--a % on the end of a field will return all records with field_name + anything
----for example: like 'daily%' will return all records with 'daily_____', like 'daily dose' 

SELECT 
medication_name,
start_date
FROM medications
where start_date > '20240901';
--Returns start date greater than 9/1/24
--Can use >= for greater than or equal or < and <= for less than and less than equal, respectively

SELECT 
medication_name
start_date,
dose,
frequency
FROM medications
WHERE medication_name IS NOT NULL;
--can also use is null



SELECT 
medication_name,
start_date,
dose, 
frequency
FROM medications
WHERE start_date > '20240901' 
and 
frequency like '%daily';
--multiple where statement; can also use OR *if using a combo of and & or, need to use parenthesis around the OR



--Grouping and aggregating using the bloodpressure_log table:

SELECT 
COUNT(patient_id) as count_patients, --renames the column header
source
FROM bloodpressure_log
GROUP BY source;
--Groups how many patients had BP reading with the source

SELECT 
patient_id,
COUNT(source) as count_source --renames column header
FROM bloodpressure_log
GROUP BY patient_id;


SELECT 
Max(heart_rate) as max_heart_rate,
patient_Id
FROM bloodpressure_log
GROUP BY patient_Id;
--Selects the max heart rate recorded per patient; could also use min()

--Adding HAVING clause

SELECT 
Min(heart_rate) as min_heart_rate,
patient_Id,
source
FROM bloodpressure_log
GROUP BY patient_Id, source
HAVING min(heart_rate) < 70;
--HAVING is similar to a where clause, but is specific to the aggregated function

SELECT 
Min(heart_rate) as min_heart_rate,
patient_Id,
source
FROM bloodpressure_log
WHERE source = 'Clinic'
GROUP BY patient_Id, source
HAVING min(heart_rate) < 70;

--Date parts

SELECT
DATE_PART('year', start_date) AS year_start_meds,
patient_id
FROM medications;


--CASE statements

SELECT 
patient_Id, 
CASE WHEN heart_rate < 70 THEN 'low'
else 'high'
END AS heart_rate_high_low
FROM bloodpressure_log;
--case statements help us "flag" items or rename columns; similar to if/then statements


SELECT 
patient_id, 
CASE WHEN source = 'Clinic' then 'c' 
WHEN source = 'Home' then 'h'
ELSE 'unknown'
END AS source_abbrev
FROM bloodpressure_log; 
--fields are case sensitive (ex: 'home' would return unknown) 


--Aliasing table names

SELECT 
bp.patient_id, 
bp.source
FROM bloodpressure_log bp 
--"renaming" the table bp allows us to reference that patient_id and source come from the bloodpressure_log table with a quick reference
--This will be important for joining tables
