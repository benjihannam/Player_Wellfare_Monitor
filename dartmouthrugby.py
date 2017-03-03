#Author: Benji Hannam

from firebase import firebase
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)


def add_player(firebase, first, last, position):
	data = {'first_name' : first, 'last_name' : last, 'position' : position}
	firebase.put("/users", first+"_"+last, data)


def get_player(firebase, first, last):
	return firebase.get('/users/'+ first + "_" + last, None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})



add_player(firebase, "Benji", "Hannam", "Flanker")
add_player(firebase, "Steve", "Hinshaw", "Lock")
print firebase.get('/users', None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'very fancy'})
print get_player(firebase, "Benji", "Hannam")