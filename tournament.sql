-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players(
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches(
	mid SERIAL PRIMARY KEY,
    winner SERIAL,
    loser SERIAL,
    FOREIGN KEY (winner) REFERENCES players(id),
    FOREIGN KEY (loser) REFERENCES players(id)
);

--Using left join to make sure players without matches will appear on standing
--Temp table A is used for counting win matches
--Temp table B is used for counting total matches
CREATE VIEW playerStandings AS
SELECT P.id, P.name, count(A.winner) wins, count(B.winner) matches
FROM players P, (players LEFT JOIN matches ON players.id = matches.winner) A,
    (players LEFT JOIN matches ON players.id = matches.winner OR players.id = matches.loser) B
WHERE P.id = A.id AND P.id = B.id
GROUP BY P.id
ORDER BY wins;
