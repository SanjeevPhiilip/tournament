-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


create table players (
id serial primary key,
name text
);

create table matches(
id serial primary key,
winner int references players(id),
loser int references players(id)
);


CREATE VIEW player_standings AS
SELECT players.id,players.name,
(SELECT count(matches.winner) FROM matches WHERE players.id = matches.winner) as wins_no,
(SELECT count(matches.id) FROM matches
WHERE players.id  = matches.winner
OR players.id = matches.loser) AS matches_no
FROM players
ORDER BY wins_no, matches_no DESC;