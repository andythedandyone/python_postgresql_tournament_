#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def error():
    #return data in case of error, for debug purpose
    db = connect()
    c = db.cursor()
    c.execute("Select * from players, matches")
    data = c.fetchall()
    print data


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(id) FROM players")
    data = c.fetchone()
    return data[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players(name) values(%s);", (name,))
    db.commit()
    db.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query = ("select winlistview.id, winlistview.name, winlistview.a_win, "
             "coalesce(matches_merged.matches, 0) "
             "from winlistview "
             "left join matches_merged "
             "on  winlistview.id=matches_merged.id;")

    db = connect()
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    c = db.cursor()
    c.execute("insert into matches(id, opponent_id, win, loss) values(%s, %s, 1, 0)", (winner, loser))
    db.commit()
    db.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    #pull query and return tuple back to code pairing by wins
    query = ("select * from winlistview order by a_win desc")

    db = connect()
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    pairs = list()
    x = 0

    while x < len(data):
        id1 = data[x][0]
        name1 = data[x][1]
        id2 = data[x + 1][0]
        name2 = data[x + 1][1]
        pairs.append((id1, name1, id2, name2))
        x += 2

    return pairs