#Author: Benji Hannam

from firebase import firebase
import fileinput
from datetime import *
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)


#################################### Adding #############################################
# adds a new player into the data base
def add_player(firebase, first, last, position, num=0):
	#if the player is not in the data base
	if get_player(firebase, first, last) is None:
		# create the json
		data = {'first_name' : first, 
				'last_name' : last, 
				'position' : position,
				'is_injured' : False,
				'non_contact' : [{'Day' : datetime.now().date(), 'Number' : num}], 
				"contact" : [{'Day' : datetime.now().date(), 'Number' : num}],
				'injuries' : [{}],
				'feedback' : [{}]
				}
		#add to the database
		firebase.put("/users", first+"_"+last, data)
		print "Added " + first + " " + last + " to the database."
	else:
		print "user already in the database"

# add an injury recording to a player
def add_injury(firebase, first, last, body_part, type_of):
	data = {'body_part' : body_part, 
			"type" : type_of, 
			'logs' : {'Date' : datetime.now().date(), 'Notes' : "First Recording"}
			}
	injury_name = body_part+ "_" + type_of
	firebase.put("/users/" + first + "_" + last + "/injuries/", injury_name, data)

#add a note to an existing injury
def add_injury_log(firebase, first, last, content):
	pass

#################################### Fetching #############################################
# Gets the player from the database, returns None is they do not exist
def get_player(firebase, first, last):
	return firebase.get('/users/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

#################################### Deleting #############################################
# Deletes a player from the database
def delete_player(firebase, first, last):
	if get_player(firebase, first, last) is not None:
		name = first + "_" + last
		firebase.delete('/users/', name)
		print "Deleted " + name
	else:
		print "Player does not exists anyway."

# Adds contact minutes to the player
def add_contact_session(firebase, first, last, num, day=None, month=None, year=None):
	if day is None:
		date = datetime.now().date()
	else:
		pass

	path = 'users/'+ first + "_" + last
	result = firebase.get(path + "/contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
	#if the player is in the database 
	if result is not None:
		data = {'Day' : datetime.now().date(), 
				'Number' : num
				}
		result.append(data)
		firebase.put(path, "contact/", result)
	else:
		print "Player not found, might not be in the database yet."

# Adds non contact minutes to the player
def add_non_contact_session(firebase, first, last, num):
	path = 'users/'+ first + "_" + last
	result = firebase.get(path + "/non_contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'}) 
	if result is not None:
		firebase.put(path, "non_contact", result + num)
	else:
		print "Player not found, might not be in the database yet."
	pass

add_player(firebase, "Benji", "Hannam", 7)
add_injury(firebase, "Benji", "Hannam", "hip", "strain")
add_injury(firebase, "Benji", "Hannam", "thigh", "strain")
# delete_player(firebase, "Benji", "Hannam")
add_contact_session(firebase, "Benji", "Hannam", 80)

def main():
	dont_quit = True
	while quit:
		pass
