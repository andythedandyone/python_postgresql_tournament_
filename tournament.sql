-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- DROP TABLE players;
-- DROP TABLE matches;

CREATE TABLE players(id serial PRIMARY KEY, name text);

CREATE TABLE matches(id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                     opponent_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
                     win INTEGER DEFAULT 0,
                     loss INTEGER DEFAULT 0,
                     draw BOOLEAN,
                     points INTEGER DEFAULT 0,
                     UNIQUE (id, opponent_id)
                     );


create view winlist
            as select id, sum(win) as wins
               from matches
               group by id
               order by wins desc;


create view rounds
            as select id, count(id) as t_rounds
               from matches
               group by id
               order by t_rounds desc;


create view player_stat
            as select players.id, players.name, winlist.wins, rounds.t_rounds
               from players, winlist, rounds
               where players.id = winlist.id and players.id = rounds.id
               order by wins desc;


create view match_by_id
            as select id, count(id) as matches
               from matches
               where points=0
               group by id;


create view match_by_op
            as select opponent_id, count(opponent_id) as matches
               from matches
               where points=0
               group by opponent_id;


create view matches_merged
            as select *
               from match_by_id
               union
               select *
               from match_by_op;