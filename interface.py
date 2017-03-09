from dartmouthrugby import *
from firebase import firebase
#the server
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)

def startup():
	print "Welcome to the Player Welfare Tracker (PWT)."
	while True:
		print "----------------------------------------"
		print "What would you like do to?"
		print "1. Add players."
		print "2. Add a session."
		print "3. Quit"
		answer = raw_input("\nChoose a number: ")
		if answer == "1":
			load_players()
		elif answer == "2":
			load_session()
		elif answer == "3":
			break
		else:
			print "Invalid input, please try again."

	print "Goodbye."
	print "----------------------------------------"

		
def load_players():
	print "----------------------------------------"
	print "How would you like to load the players:"
	print "1. From file."
	print "2. Manual Input."
	print "3. Go back."
	answer = raw_input("\nChoose a number: ")
	# load from file
	if answer == "1":
		exit = True
		while exit:
			# get the file location
			file = raw_input("Please insert the file location, E.g 'import_files/players.csv' :")
			# if it did not find the file
			if not add_players_from_file(firebase, file):
				# ask if they want to try again
				while True:
					reply = raw_input("Would you like to try again (y/n):")

					if reply.lower() == "y":
						break
					elif reply.lower() == "n":
						exit = False
						break
					else:
						print "Please enter only y or n."
			else:
				exit = False

	elif answer == "2":
		add_players_from_input(firebase)


def load_session():
	print "----------------------------------------"
	type_of = raw_input("What type of session? (contact/non-contact/match): ")
	num_minutes = int(raw_input("How long? (minutes): "))
	day = None
	month = None
	year = None
	while True:
		reply = raw_input("Do you want to manuall set the date (default is today)? (y/n): ")
		if reply.lower() == "y":
			day = raw_input("Day (DD): ")
			month = raw_input("Day (MM): ")
			year = raw_input("Day (YYYY): ")
			break
		elif reply.lower() == "n":
			break
		else:
			print "Please enter only y or n."

	add_session_to_players(firebase, type_of, num_minutes, day, month, year)


startup()
