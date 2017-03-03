#Author: Benji Hannam

from firebase import firebase
import fileinput
from datetime import *
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)

# adds a new player into the data base
def add_player(firebase, first, last, position, num=0):
	#if the player is not in the data base
	if get_player(firebase, first, last) is None:
		# create the json
		data = {'first_name' : first, 'last_name' : last, 'position' : position, 'non_contact' : {'Day' : datetime.now().date(), 'Number' : num}, "contact" : {'Day' : datetime.now().date(), 'Number' : num}}
		print data
		#add to the database
		firebase.put("/users", first+"_"+last, data)
		print "Added " + first + " " + last + " to the database."
	else:
		print "user already in the database"

# Gets the player from the database, returns None is they do not exist
def get_player(firebase, first, last):
	return firebase.get('/users/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

# Deletes a player from the database
def delete_player(firebase, first, last):
	if get_player(firebase, first, last) is not None:
		name = first + "_" + last
		firebase.delete('/users/', name)
		print "Deleted " + name
	else:
		print "Player does not exists anyway."

# Adds contact minutes to the player
def add_contact_minutes(firebase, first, last, num):
	path = 'users/'+ first + "_" + last
	result = firebase.get(path + "/contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
	#if the player is in the database 
	if result is not None:
		data = {'Day' : datetime.datetime.now().date(), 'Number' : num}
		firebase.put(path, "contact", result + num)
	else:
		print "User not found, might not be in the database yet."

# Adds non contact minutes to the player
def add_non_contact_minutes(firebase, first, last, num):
	path = 'users/'+ first + "_" + last
	result = firebase.get(path + "/non_contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'}) 
	if result is not None:
		firebase.put(path, "non_contact", result + num)
	else:
		print "User not found, might not be in the database yet."
	pass

add_player(firebase, "Benji", "Hannam", 7)
# delete_player(firebase, "Benji", "Hannam")
# add_contact_minutes(firebase, first, last, 80)

def main():
	dont_quit = True
	while quit:
		pass
