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

#######################CLASS DECLARATIONS NEED TO COME FIRST##################
class Game:
    def __init__(self, title, platform, score, genres):
        self.title = title
        self.platform = platform
        self.score = float(score)
        self.genres = genres


#############################################################################

#########################################FUNCTIONS#############################################
# The games variable is already populated with key = game_id and value = game object which contains all of the data you should need.

# Should return a dictionary (map) with each word in the titles with it's corrisponding score. We can then average the scores of the words in a game title to get it's expected score based on name.
def weightNames():
    result = dict()
    for key, value in games.iteritems():
        words = value.title.split(' ')
        for g in words:
            if g in result:
                result[g].append(value.score)
            else:
                result[g] = list()
                result[g].append(value.score)
    return result
    
# Should return a dictionary with each genre and it's corisponding average score.
def weightGenres():
    result = dict()
    for key, value in games.iteritems():
        for g in value.genres:
            if g in result:
                result[g].append(value.score)
            else:
                result[g] = list()
                result[g].append(value.score)
    return result
    
# Should return a dictionary with each platform and it's corisponding average score.
def weightPlatforms():
    result = dict()
    for key, value in games.iteritems():
        if value.platform in result:
            result[value.platform].append(value.score)
        else:
            result[value.platform] = list()
            result[value.platform].append(value.score)
    return result
    
# Should return a dictionary with the keys being a tuple of (genre, platform) and values being the score. This gives us a much better prediction then just averaging the genres and platforms.
# It is a little weird to have a tuple as a key but Python suports this and it will make lookup really easy. An example of thie I got to work:
# weightPG[('Action', 'Wii')] = "Woot"
def weightPlatGenre():
    result = dict()
    for key, value in games.iteritems():
        for g in value.genres:
            if (g, value.platform) in result:
                result[(g, value.platform)].append(value.score)
            else:
                result[g, value.platform] = list()
                result[g, value.platform].append(value.score)
    return result

# Should return a float based on the expected score of a game given the name.
def scoreName(name):
    words = name.split(' ')
    nameScores = weightNames()
    wordScores = list()
    nameSum = 0
    
    for word in words:
        if word in nameScores:
            #wordScores = wordScores + nameScores[word]
            for n in nameScores[word]:
                nameSum = nameSum + float(n);
            wordScores.append(nameSum / len(nameScores[word]))
            
    if len(wordScores) == 0:
        print("Error, no names similar")
        return -1
    
    scoreSum = 0
    for s in wordScores:
        scoreSum = scoreSum + float(s);
    result = scoreSum / len(wordScores)
    return result

# Should return a float based on the expected score of a game given the genre.
def scoreGenre(genre):
    scores = weightGenres()
    scoreSum = 0
    for s in scores[genre]:
        scoreSum = scoreSum + float(s);
    result = scoreSum / len(scores[genre])
    return result

# Should return a float based on the expected score of a game given the platform.
def scorePlatform(platform):
    scores = weightPlatforms()
    scoreSum = 0
    for s in scores[platform]:
        scoreSum = scoreSum + float(s);
    result = scoreSum / len(scores[platform])
    return result

# Should return a float based on the expected score of a game given the genre and platform.
def scorePlatGenre(genre, platform):
    scores = weightPlatGenre()
    scoreSum = 0
    for s in scores[genre, platform]:
        scoreSum = scoreSum + float(s);
    result = scoreSum / len(scores[genre, platform])
    return result
    
    
############################################################################################
	
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

	
print("Connection Established, fetching data...")
# uncomment next line if you want every insert/update/delete to immediately
# be applied; you can remove all db.commit() and db.rollback() statements
cursor = db.cursor()

# Dictionary object that maps id's to their game object. This is usefull for 
games = dict()


# query database for game info
query = """SELECT games.id, games.title, games.platform, games.score
               FROM games;"""

cursor.execute(query)

results = cursor.fetchall()
for row in results:
    game_id, title, platform, score = row
    #print(game_id, title, platform, score)
    games[game_id] = Game(title, platform, score, list())

# query database for genre info
query = """SELECT game_id, genre
               FROM game_genres
               ORDER BY game_id;"""  

cursor.execute(query)

results = cursor.fetchall()
for row in results:
    game_id, gen = row
    #print(game_id, gen)
    games[game_id].genres.append(gen)
    #print(str(game_id) + " -- " + gen)

    
#for key, value in games.iteritems():
#    print("\n" + value.title + "Generes:")
#    print(len(value.genres))
#    for j in value.genres:
#        print(j)

boo = 1
while boo == 1:
    choice = raw_input("\n1.New Game\n2. Quit\nData loaded, Enter Choice: ")
    nameScore = 0
    gpScore = 0
    if choice == "1":
        title = raw_input("\nEnter the name of your game: ")
        platform = raw_input("Enter platform of your game: ")
        genre = raw_input("Enter genre for your game: ")
        if title in weightNames():
            nameScore = scoreName(title)
        else:
            nameScore = 5
            print "Name was not found in database"
			
        if (genre, platform) in weightPlatGenre():
            gpScore = scorePlatGenre(genre, platform)
        else:
            gpScore = 5
            print "Platform and Genre combination was not found in database"
			
        print "Your game's score will probably be", str((nameScore + gpScore) / 2)
        
    if choice == "2":
        boo = 2
cursor.close()
db.close()
