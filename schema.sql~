DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS platforms CASCADE;
DROP TABLE IF EXISTS game_genres CASCADE;
DROP TABLE IF EXISTS game_platforms CASCADE;

CREATE TABLE games(
id serial PRIMARY KEY,
title text,
score text
);
CREATE TABLE genres(
genre text PRIMARY KEY
);
CREATE TABLE platforms(
platform text PRIMARY KEY
);
CREATE TABLE game_genres(
game_id integer,
genre text,
primary key (game_id, genre),
foreign key (game_id) references games(id),
foreign key (genre) references genres(genre)
);
CREATE TABLE game_platforms(
game_id integer,
platforn text,
primary key (game_id, platforn),
foreign key (game_id) references games(id),
foreign key (platform) references platforms(genre)
);


