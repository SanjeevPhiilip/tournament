#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        db_cursor = db.cursor()
        return db, db_cursor
    except Exception as e:
        print("<eror message> " + str(e))


def deleteMatches():
    """Remove all the match records from the database."""
    db, db_cursor = connect()
    db_cursor.execute("TRUNCATE TABLE matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, db_cursor = connect()
    db_cursor.execute("TRUNCATE TABLE players CASCADE;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, db_cursor = connect()
    db_cursor.execute("SELECT COUNT(*) FROM players;")
    DB = db_cursor.fetchone()
    db.close()
    return DB[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, db_cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    params = (name,)
    db_cursor.execute(query, params)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, db_cursor = connect()
    db_cursor.execute("SELECT * FROM player_standings;")
    DB = db_cursor.fetchall()
    db.close()
    return DB


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, db_cursor = connect()
    query = "INSERT INTO matches(winner, loser) VALUES (%s, %s);"
    params = (winner, loser, )
    db_cursor.execute(query, params)
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
    standings = playerStandings()
    next_round = []
    for i in range(0, len(standings), 2):
        next_round.append((standings[i][0], standings[i][1],
                           standings[i+1][0], standings[i+1][1]))
    return next_round
