#Author: Benji Hannam

from firebase import firebase
import fileinput
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)


# adds a new player into the data base
def add_player(firebase, first, last, position, num=0):

	if get_player(firebase, first, last) is None:
		data = {'first_name' : first, 'last_name' : last, 'position' : position, 'non_contact' : 0, "contact" : num}
		firebase.put("/users", first+"_"+last, data)
		print "Added " + first + " " + last + " to the database."
	else:
		print "user already in the database"


def get_player(firebase, first, last):
	return firebase.get('/users/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})

def add_contact_minutes(firebase, first, last, num):
	path = 'users/'+ first + "_" + last
	result = firebase.get(path + "/contact", None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'}) 
	if result is not None:
		firebase.put(path, "contact", result + num)
	else:
		print "User not found, might not be in the database yet."


def add_non_contact_minutes(firebase, first, last, num):
	pass

add_contact_minutes(firebase, "Steve", 'Hinshaw', 80)

def main():
	dont_quit = True
	while quit:
		pass
