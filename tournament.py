#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import pandas as pd


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname = tournament")
    db_cursor = db.cursor()
    db_cursor.execute("DELETE FROM matches *;")
    db_cursor.execute("UPDATE players SET matches = 0")
    db_cursor.execute("UPDATE players SET wins = 0")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("DELETE FROM players *")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("SELECT COUNT(*) FROM players;")
    DB = db_cursor.fetchall()
    db.close()
    return DB[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("INSERT INTO players (name) VALUES (%s);",(name,))
    db.commit()
    db.close()


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
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("SELECT id,name,wins,matches FROM players ORDER BY wins DESC")
    DB = db_cursor.fetchall()
    db.close()
    return DB


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("UPDATE players SET matches = matches + 1 WHERE ID = %s;",(winner,))
    db_cursor.execute("UPDATE players SET matches = matches + 1 WHERE ID = %s;",(loser,))
    db_cursor.execute("UPDATE players SET wins = wins + 1 WHERE ID = %s;",(winner,))
    db_cursor.execute("INSERT INTO matches(winner, loser) VALUES (%s, %s);",(winner,loser,))
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
    db = psycopg2.connect("dbname=tournament")
    db_cursor = db.cursor()
    db_cursor.execute("select * from players order by wins DESC")
    DB = db_cursor.fetchall()
    db.close()
    df = pd.DataFrame(DB, columns= ['names','id','wins','matches'])
    pair = []
    for i in range(0,len(df),2):
        pair.append((df.iloc[i]['id'],df.iloc[i]['names'],df.iloc[i+1]['id'],df.iloc[i+1]['names']))
    return pair
    


