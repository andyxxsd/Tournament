#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Get connection and cursor at the same time"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cur = connect()
    cur.execute("truncate matches cascade")
    conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("truncate players cascade")
    conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    cur.execute("select count(*) from players")
    return cur.fetchone()[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
        name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    # No injection will happen
    cur.execute("insert into players (name) values( %s )", (name,))
    conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    cur.execute("select * from playerStandings")
    return cur.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
        winner:  the id number of the player who won
        loser:  the id number of the player who lost
    """
    conn, cur = connect()
    # No injection will happen
    cur.execute("""
        insert into matches (winner, loser) values( %s, %s )
    """, (winner, loser,))
    conn.commit()


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
    conn, cur = connect()
    # Temp table A & B are used for self joining
    # Use where & order by to make sure correct pairing
    cur.execute("""
        select A.id id1, A.name name1, B.id id2, B.name name2
        from (select row_number() over () i, id, name from playerStandings)A,
            (select row_number() over () i, id, name from playerStandings)B
        where mod(A.i, 2) = 1 and A.i+1 = B.i
        order by A.i
    """)
    return cur.fetchall()
