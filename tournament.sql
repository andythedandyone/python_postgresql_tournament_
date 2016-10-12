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


CREATE TABLE players(id serial PRIMARY KEY, name text);

CREATE TABLE matches(id INTEGER PRIMARY KEY REFERENCES players(id) ON DELETE CASCADE,
                     opponent_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                     win INTEGER DEFAULT 0,
                     UNIQUE (id, opponent_id)
                     );


create view winlistview
            as select players.id, players.name, sum(coalesce(matches.win, 0)) as a_win
               from players
                 left join matches on players.id=matches.id
               group by players.id, players.name;


create view match_by_id
            as select id, count(id) as matches
               from matches
               group by id;


create view match_by_op
            as select opponent_id, count(opponent_id) as matches
               from matches
               group by opponent_id;


create view matches_merged
            as select *
               from match_by_id
               union
               select *
               from match_by_op;