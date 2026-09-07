-- Core analytical queries used in the supplied SQL notebook.
SELECT DISTINCT Launch_Site FROM SPACEXTBL;

SELECT * FROM SPACEXTBL
WHERE Launch_Site LIKE 'CCA%'
LIMIT 5;

SELECT SUM(PAYLOAD_MASS__KG_)
FROM SPACEXTBL
WHERE Customer LIKE '%NASA (CRS)%';

SELECT AVG(PAYLOAD_MASS__KG_)
FROM SPACEXTBL
WHERE Booster_Version LIKE 'F9 v1.1%';

SELECT Date
FROM SPACEXTBL
WHERE Landing_Outcome = 'Success (ground pad)'
ORDER BY Date
LIMIT 1;

SELECT Booster_Version
FROM SPACEXTBL
WHERE Landing_Outcome = 'Success (drone ship)';

SELECT Landing_Outcome, COUNT(*)
FROM SPACEXTBL
GROUP BY Landing_Outcome
ORDER BY COUNT(*) DESC;
