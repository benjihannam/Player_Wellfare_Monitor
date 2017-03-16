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
				'position' : int(position),
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
		print first + " " + last + " is already in the database."

# add from a .csv file that is stored at location path "file"
def add_players_from_file(firebase, file):
	# if the file exists
	if os.path.exists(file):
		# open it
		f = open(file, 'rU')
		csv_f = csv.reader(f)
		# add the player
		for row in csv_f:
			add_player(firebase, row[0], row[1], row[2])

		f.close()
		return True

	else:
		print "File not found"
		return False

# add players by manually typing them in from stdin
def add_players_from_input(firebase):
	print "Please enter the information of the players you want to add."
	exit = True
	while exit:
		first = raw_input("First Name: ")
		last = raw_input("Last Name: ")
		position = int(raw_input("Position (number): "))
		add_player(firebase, first, last, position)
		answer = raw_input("Add another player (y/n): ")
		if answer.lower() == "y":
				pass
		elif answer.lower() == "n":
			exit = False
		else:
			print "Please enter only y or n."

# add an injury recording to a player
def add_injury(firebase, first, last, body_part, type_of, content, day=None, month=None, year=None):

	if last is not None:
		name = first + "_" + last
	else:
		name = first

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
		# the name of the injury
		injury_name = body_part+ "_" + type_of
		# put it in the db
		firebase.put("/players/" + name + "/injuries", injury_name, data)
		firebase.put("/players/" + name + "/injuries/" + injury_name + "/logs", date, content)
		print "Added " + injury_name + " to " + name + "."
	else:
		print "Player, " + name + ", not found, might not be in the database yet."

#add a log to an existing injury
def add_injury_log(firebase, first, last, content):
	if last is not None:
		name = first + "_" + last
	else:
		name = first
	if get_player(firebase, first, last) is not None:
		pass
	else:
		print "Player, " + name + ", not found, might not be in the database yet."

# Adds a session to the player
def add_session(firebase, type_of, first, last, num, day=None, month=None, year=None):
	type_of = "/"+ type_of
	#if a day is given set it on that date, otherwise set it as today
	if day is None:
		date = datetime.now().date()
	else:
		date_string = str(year) + "-" + str(month) + "-" + str(day)
		date = datetime.strptime(date_string, "%Y-%m-%d").date()

	if last is not None:
		name = first + "_" + last
	else:
		name = first

	#if the player is in the database 
	if get_player(firebase, first, last) is not None:
		firebase.put("/players/" + name + "/sessions" + type_of, date, num)
		# get the old total
		num_minutes = firebase.get('/players/'+ name +"/total_minutes", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
		#add on the new minutes
		new_total = int(num_minutes) + int(num)
		# update the total
		firebase.put("/players/" + name, "total_minutes", new_total)

	else:
		print "Player, " + name + ", not found, might not be in the database yet."

def add_session_to_players(firebase, type_of, num_minutes, day=None, month=None, year=None):
	players = firebase.get("/players", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
	# for each player in the database
	people_to_add = []
	for name in sorted(players):
		move_on = False
		while not move_on:
			answer = raw_input("Add session for " + name + "? (y/n): ")
			if answer.lower() == "y":
				people_to_add.append(name)
				move_on = True
			elif answer.lower() == "n":
				move_on = True
			else:
				print "Please enter only y or n."

	print "Adding session into the database..."
	for name in people_to_add:
		print "Added session to " + name + "."
		add_session(firebase, type_of, players[name]['first_name'], players[name]['last_name'], num_minutes, day, month, year)

	print "Added session."

def add_session_from_file(firebase, type_of, file, day, month, year):
	# if the file exists
	if os.path.exists(file):
		# open it
		f = open(file, 'rU')
		csv_f = csv.reader(f)
		# add the session to each player
		print "Adding session to players..."
		for row in csv_f:
			add_session(firebase, type_of, row[0], row[1], int(row[2]), day, month, year)

		print "Added session"
		f.close()
		return True

	else:
		print "File not found"
		return False

#################################### Fetching #############################################
# Gets the player from the database, returns None is they do not exist
def get_player(firebase, first, last=None):
	if last is not None:
		name = first + "_" + last
	else:
		name = first
	return firebase.get('/players/'+ name, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def get_injuries(firebase, first, last=None):
	if last is not None:
		name = first + "_" + last
	else:
		name = first
	return firebase.get('/players/'+ name +"/injuries", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def get_sessions(firebase, first, last=None):
	if last is not None:
		name = first + "_" + last
	else:
		name = first
	return firebase.get('/players/'+ name +"/sessions", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def get_players(firebase):
	return firebase.get("/players", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

#################################### Deleting #############################################
# Deletes a player from the database
def delete_player(firebase, first, last=None):
	if get_player(firebase, first, last) is not None:
		if last is not None:
			name = first + "_" + last
		else:
			name = first
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
	pass
