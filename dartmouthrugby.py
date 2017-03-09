#Author: Benji Hannam

from firebase import firebase
import fileinput
from datetime import *
import csv
import os
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)


#################################### Adding #############################################
# adds a new player into the data base
def add_player(firebase, first, last, position):
	#if the player is not in the data base
	if get_player(firebase, first, last) is None:
		# create the json
		data = {'first_name' : first, 
				'last_name' : last, 
				'position' : position,
				'is_injured' : False,
				'non_contact' : [], 
				"contact" : [],
				'injuries' : [],
				'feedback' : [],
				'total_minutes' : 0
				}
		#add to the database
		firebase.put("/players", first+"_"+last, data)
		print "Added " + first + " " + last + " to the database."
	else:
		print "user already in the database"


def add_players_from_file(firebase, file):
	if os.path.exists(file):
		f = open(file, 'rU')
		csv_f = csv.reader(f)
		for row in csv_f:
			add_player(firebase, row[0], row[1], row[2])

	else:
		print "File not found"

# add an injury recording to a player
def add_injury(firebase, first, last, body_part, type_of, day=None, month=None, year=None):
	# if not date given, use today
	if day is None:
		date = datetime.now().date()
	else:
		date_string = str(year) + "-" + str(month) + "-" + str(day)
		date = datetime.strptime(date_string, "%Y-%m-%d").date()

	#if the player is in the database
	if get_player(firebase, first, last) is not None:
		# create the json
		data = {'body_part' : body_part, 
				"type" : type_of, 
				'logs' : [],
				'is_active' : True
				}
		#the name of the injury
		injury_name = body_part+ "_" + type_of
		# put it in the db
		firebase.put("/players/" + first + "_" + last + "/injuries", injury_name, data)
		firebase.put("/players/" + first + "_" + last + "/injuries/" + injury_name + "/logs", date, "First Recording")
	else:
		print "Player not found, might not be in the database yet."

#add a log to an existing injury
def add_injury_log(firebase, first, last, content):
	pass

# Adds contact minutes to the player
def add_session(firebase, type_of, first, last, num, day=None, month=None, year=None):
	type_of = "/"+ type_of
	#if a day is given
	if day is None:
		date = datetime.now().date()
	else:
		date_string = str(year) + "-" + str(month) + "-" + str(day)
		date = datetime.strptime(date_string, "%Y-%m-%d").date()

	#if the player is in the database 
	if get_player(firebase, first, last) is not None:
		firebase.put("/players/" + first + "_" + last + "/sessions" + type_of, date, num)
	else:
		print "Player not found, might not be in the database yet."

#################################### Fetching #############################################
# Gets the player from the database, returns None is they do not exist
def get_player(firebase, first, last):
	return firebase.get('/players/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def get_injuries(firebase, first, last):
	return firebase.get('/players/'+ first + "_" + last +"/injuries", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def get_contact_sessions(firebase, first, last):
	return firebase.get('/players/'+ first + "_" + last +"/contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

#################################### Deleting #############################################
# Deletes a player from the database
def delete_player(firebase, first, last):
	if get_player(firebase, first, last) is not None:
		name = first + "_" + last
		firebase.delete('/players/', name)
		print "Deleted " + name
	else:
		print "Player does not exists anyway."


#################################### Custom Printing #############################################
# A human readable print function for JSON database take from:
# http://stackoverflow.com/questions/15275766/printing-dictionaries-json-human-readable
def prettyPrint(dictionary, ident = '', braces=1):
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' % (ident, braces*'[', key, braces*']') 
            prettyPrint(value, ident+'  ', braces+1)
        elif isinstance(value, list):
            ndict=0
            for v in value:
                if isinstance(v, dict):
                    ndict += 1
            if ndict:
                print '- %s%s' % (ident, key) 
                for e in value:
                    if isinstance(e, dict):
                        prettyPrint(e, ident+'  ', braces+1)
                    else: 
                         print ident+'- %s : %s' %(key, e)
            else:
                print ident+'- %s : %s' %(key, value)
        else:
            print ident+'- %s : %s' %(key, value)

def print_player(firebase, first, last):
	json = get_player(firebase, first, last)
	print "First : " + json['first_name']
	print "Last : " + json['last_name']
	print "Position : " + str(json['position'])


#################################### main function for testing #############################################
def main():
	# add_player(firebase, "Benji", "Hannam", 7)
	# add_injury(firebase, "Benji", "Hannam", "hip", "strain")
	# add_session(firebase, 'contact', "Benji", "Hannam", 60, "09", "03", "2017")
	# # prettyPrint(get_injuries(firebase,"Benji", "Hannam"))
	# # prettyPrint(get_player(firebase, "Benji", "Hannam"))
	# # print get_contact_sessions(firebase, "Benji", "Hannam")
	# print_player(firebase, "Benji", "Hannam")
	add_players_from_file(firebase, "test/player.csv")
	pass

main()
