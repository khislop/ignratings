#!/usr/bin/python3.5

# example.py
#
# CSCI 403 example Python script
#
# Author: C. Painter-Wakefield
# Modified: 10/31/2015
#
# This script does a couple of SELECT queries against tables in public, then
# creates a table and attempts some modification queries on it.  Examples are
# given of prepared queries using parameters, exception handling, and 
# very basic input/output.

import getpass
import pg8000
	
login = input('login: ')
secret = getpass.getpass('password: ')

credentials = {'user'    : login, 
               'password': secret, 
               'database': 'csci403',
               'host'    : 'flowers.mines.edu'}

try:
    db = pg8000.connect(**credentials)
except pg8000.Error as e:
    print('Database error: ', e.args[2])
    #exit()

# uncomment next line if you want every insert/update/delete to immediately
# be applied; you can remove all db.commit() and db.rollback() statements
db.autocommit = True
cursor = db.cursor()

boo = 1
while boo == 1:
    
	# prompt user for inputs
    title = input('\nEnter title of your game: ')
    platform = input('Enter platform for your game: ')
    genres = input('Enter genres for your game in the form of: genre, genre, ...: ')
	
	#query database for 
    query = """SELECT games.title, games.platform, games.score
		   FROM games
		   WHERE games.title LIKE %s"""  

    cursor.execute(query, ('%%' + title + '%%',))

    results = cursor.fetchall()
    for row in results:
        print("\nResult:")
        title, platform, score = row
        print(title, platform, score)
    
        print("\n1.Create New Game\n2.Quit\n")
        choice = input('Enter Choice: ')
    
        if choice == "2":
            boo = 0;
cursor.close()
db.close()
 