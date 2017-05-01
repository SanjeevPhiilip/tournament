Introduction
------------------
Tournament is a project to keep track of records for a swiss style tournament.
For information on Swiss syle tournaments, got to: https://en.wikipedia.org/wiki/Swiss-system_tournament
The project contains three files:
	1. tournament.py
	2. tournament.sql
	3. tournament_test.py

tournament.py
-----------------
This is the python code to get the pairings and to interact with the postgres databse.
To run this file you will need to install the psycopg2 python package.
It has the following functions:
	1. connect(database_name="tournament")
		It connects to the tournament db and returns the database and cursor object
	2. deleteMatches():
		This function deletes all records of matches from the database.
	3. deletePlayers()
		This fuction deletes all records of the players from the database.
	4. countPlayers()
		This function returs the count of unique players from the database.
	5. registerPlayer(name)
		This function accepts players names as arguements and updates them with unique id in players table.
	6. playerStandings():
		This returns the list of players in DESCENDING order based upon the number of their wins.
	7. reportMatch(winner, loser)
		This function takes the ids of both the winners and losers as arguements and updates them in matches table.
	8. swissPairings()
		This function pairs players against each other based upon their number of wins.

tournament.sql
----------------
This file is used to inititalize the tables required for storing the records of players and matches.
	players
	---------
	This table contains informatiuon about the players, i.e. their name and their unique id. The unique id is an integer value that is incremented when a new player is added to the table.

	matches
	---------
	This table contains information about the the matches, i.e. the winner, loser, and the unique match id.

	player_standings
	------------------
	This is view containing the players and the number of matches they have played and the number of matches they have won.

tournament_test.py
--------------------
This file contains the tests to verify if the project is worj=king currectly.


