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
	
login = raw_input('login: ')
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

# Dictionary object that maps id's to their game object. This is usefull for 
games = dict()


# query database for game info
query = """SELECT games.id games.title, games.platform, games.score
               FROM games"""

cursor.execute(query)

results = cursor.fetchall()
print("\nResult:")
for row in results:
    game_id, title, platform, score = row
    print(game_id, title, platform, score)
    games[game_id] = Game(title, platform, score)

# query database for genre info
query = """SELECT game_id, genre
               FROM genre"""  

cursor.execute(query)

results = cursor.fetchall()
print("\nResult:")
for row in results:
    game_id, gen = row
    print(game_id, genre)
    games[game_id].genre.append(gen)

    

    
cursor.close()
db.close()


#########################################TO DO#############################################
# The games variable is already populated with key = game_id and value = game object which contains all of the data you should need.

# Should return a dictionary (map) with each word in the tiltes with it's corisponding score. We can then average the scores of the words in a game title to get it's expected score based on name.
def weightNames():
    return
    
# Should return a dictionary with each genre and it's corisponding average score.
def weightGenres():
    return
    
# Should return a dictionary with each platform and it's corisponding average score.
def weightPlatforms():
    return
    
# Should return a dictionary with the keys being a tuple of (genre, platform) and values being the score. This gives us a much better prediction then just averaging the genres and platforms.
# It is a little weird to have a tuple as a key but Python suports this and it will make lookup really easy. An example of thie I got to work:
# weightPG[('Action', 'Wii')] = "Woot"
def weightPlatGenre():
    return
    
    
############################################################################################
    




class Game:
    def __init__(self, title, platform, score, genres=list()):
        self.title = title
        self.platfrom = platform
        self.score = float(score)
        self.genres = genres

