DROP TABLE IF EXISTS global2 CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
--DROP TABLE IF EXISTS platforms CASCADE;
DROP TABLE IF EXISTS game_genres CASCADE;
--DROP TABLE IF EXISTS game_platforms CASCADE;

CREATE TABLE global2(
name text,
platform text,
rating text,
genre text
);
CREATE TABLE games(
id serial PRIMARY KEY,
platform text,
title text,
score text
);
CREATE TABLE genres(
genre text PRIMARY KEY
);

CREATE TABLE game_genres(
game_id integer,
genre text,
primary key (game_id, genre),
foreign key (game_id) references games(id),
foreign key (genre) references genres(genre)
);

INSERT INTO global2 (name, platform, rating, genre) SELECT gi.name, gi.platform, gi.rating, split_part(gi.genre,', ',1) FROM global_ign gi WHERE genre LIKE '%, %';
INSERT INTO global2 (name, platform, rating, genre) SELECT gi.name, gi.platform, gi.rating, split_part(gi.genre,', ',2) FROM global_ign gi WHERE genre LIKE '%, %';
INSERT INTO global2 (name, platform, rating, genre) SELECT gi.name, gi.platform, gi.rating, gi.genre FROM global_ign gi WHERE genre NOT LIKE '%, %';
INSERT INTO games (title, platform, score) SELECT DISTINCT name, platform, rating FROM global2 ORDER BY name;
INSERT INTO genres SELECT DISTINCT genre FROM global2;
INSERT INTO game_genres (game_id, genre) SELECT DISTINCT games.id, g2.genre FROM games, global2 g2 WHERE games.title = g2.name;

--SELECT * FROM global_ign WHERE genre LIKE '%, %';
--SELECT DISTINCT name, AVG(rating) FROM global_ign GROUP BY name ORDER BY name;
