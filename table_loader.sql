DROP TABLE IF EXISTS global_ign CASCADE;

CREATE TABLE global_ign
(NAME varchar, PLATFORM varchar, RATING double precision, GENRE varchar);

\copy global_ign FROM '~/csci403/project6/ignratings/global_table.csv' DELIMITER ',' CSV;
