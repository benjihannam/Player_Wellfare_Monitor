#Author: Benji Hannam

from dartmouthrugby import *
# firebase import
from firebase import firebase

# file system import
from Tkinter import *
from tkFileDialog import askopenfilename
#the server
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)

def startup():
	print "Welcome to the Player Welfare Tracker (PWT)."
	while True:
		print "----------------------------------------"
		print "What would you like do to?"
		print "1. Add players."
		print "2. Add a session."
		print "3. Add an injury."
		print "99. Quit"
		answer = raw_input("\nChoose a number: ")
		if answer == "1":
			load_players()
		elif answer == "2":
			load_session()
		elif answer == "3":
			load_injury()
		elif answer == "99":
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
			Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
			file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
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

	else:
		return

def load_session():
	print "----------------------------------------"
	type_of = raw_input("What type of session? (contact/non-contact/match): ")
	day = None
	month = None
	year = None
	while True:
		reply = raw_input("Do you want to manually set the date (default is today)? (y/n): ")
		if reply.lower() == "y":
			day = raw_input("Day (DD): ")
			month = raw_input("Month (MM): ")
			year = raw_input("Year (YYYY): ")
			break
		elif reply.lower() == "n":
			break
		else:
			print "Please enter only y or n."

	# Determine how to load the session
	print "How would you like to load the session:"
	print "1. From file."
	print "2. Manual Input."
	print "3. Go back."
	answer = raw_input("\nChoose a number: ")

	if answer == "1":
		# get the file location
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
		file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
		add_session_from_file(firebase, type_of, file, day, month, year)

	elif answer == "2":
		num_minutes = int(raw_input("How long? (minutes): "))
		add_session_to_players(firebase, type_of, num_minutes, day, month, year)
	else:
		return

def load_injury():
	print "----------------------------------------"
	# high level injury details
	body_part = raw_input("What body part? (calf/thigh/ACL etc..): ")
	type_of = raw_input("What type of injury? (break/concussion/tear etc..): ")
	first = raw_input("First name of player?: ")
	last = raw_input("Last name of player?: ")
	# Get the date of the injury
	day = None
	month = None
	year = None
	# get the date
	while True:
		reply = raw_input("Do you want to manually set the date (default is today)? (y/n): ")
		if reply.lower() == "y":
			day = raw_input("Day (DD): ")
			month = raw_input("Month (MM): ")
			year = raw_input("Year (YYYY): ")
			break
		elif reply.lower() == "n":
			break
		else:
			print "Please enter only y or n."

	# get the comment
	content = raw_input("Injury Notes: ")

	add_injury(firebase, first, last, body_part, type_of, content, day, month, year)



# startup()

########################################### WIDGET TESTING ###########################################
def test():
	master = Tk()

	e = Entry(master)
	c = Entry(master)
	e.pack()
	c.pack()

	e.focus_set()
	c.focus_set()

	def callback():
	    print e.get()
	    print c.get()
	    master.destroy()

	b = Button(master, text="get", width=10, command=callback)
	b.pack()

	mainloop()

def home_page():
	pass

test()
