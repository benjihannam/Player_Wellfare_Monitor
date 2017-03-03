#Author: Benji Hannam

from firebase import firebase
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)


# adds a new player into the data base
def add_player(firebase, first, last, position):

	if get_player(firebase, first, last) is None:
		data = {'first_name' : first, 'last_name' : last, 'position' : position, 'Non Contact' : 0, "Contact" : 0}
		firebase.put("/users", first+"_"+last, data)
		print "Added " + first + " " + last + " to the database."
	else:
		print "user already in the database"


def get_player(firebase, first, last):
	return firebase.get('/users/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})



add_player(firebase, "Benji", "Hannam", "Flanker")
add_player(firebase, "Steve", "Hinshaw", "Lock")
add_player(firebase, "Steve", "Hinshaw", "Lock")
print firebase.get('/users', None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
print get_player(firebase, "Benji", "Hannam")