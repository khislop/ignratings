CREATE TABLE global_ign
(NAME varchar, PLATFORM varchar, RATING double precision, GENRE varchar);

\copy global_ign FROM 'your path to csv here' DELIMITER ',' CSV;