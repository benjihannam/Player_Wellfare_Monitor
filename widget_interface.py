#Author: Benji Hannam

from dartmouthrugby import *
# firebase import
from firebase import firebase

# file system import
from Tkinter import *
from tkFileDialog import askopenfilename
#the server
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)

########################################### WIDGET TESTING ###########################################
def player_buttons(action):
	master = Tk()

	#get all the player in the database
	players = get_players(firebase)

	#for each player create a button and place appropriately in the grim
	x = 0
	for name in sorted(players):
		new_button = Button(master, text=name, command=lambda name=name: action(name, master), bg= "blue")
		new_button.grid(row = x % 10, column = (x / 10))
		x += 1

	exit_button = Button(master, text="Go back", command=lambda root=master: go_home(root), bg= "blue")
	exit_button.grid(row = x % 10 + 2, column = (x / 20))

	mainloop()

def get_player_stats(name, root):
	# root.destroy()
	curr_root = Tk()
	name_parts = name.split("_")
	T0 = Text(curr_root, height=10, width=200)
	T0.grid(row = 0)
	player_string = get_player(firebase, name_parts[0], name_parts[1])
	T0.insert(END, player_string)


def home_page():
	root = Tk()
	root.title("Player Tracker")
	# root.geometry("500x400")
	T0 = Text(root, height=1, width=70)
	T1 = Text(root, height=1, width=70)

	T0.grid(row = 0)
	T1.grid(row = 1)

	T0.insert(END, "Welcome to the Player Welfare Tracker (PWT).")
	T1.insert(END, "What would you like do to?")
	b1 = Button(root, text="1. Add players.", command=lambda name="test": action(name), bg= "blue")
	b2 = Button(root, text="2. Add a session.", command=lambda name="test": action(name), bg= "blue")
	b3 = Button(root, text="3. Add an injury.", command=lambda name="test": action(name), bg= "blue")
	b4 = Button(root, text="4. Get the stats for a player.", command=lambda name=get_player_stats: player_buttons(name), bg= "blue")

	b1.grid(row = 2, sticky=W)
	b2.grid(row = 3, sticky=W)
	b3.grid(row = 4, sticky=W)
	b4.grid(row = 5, sticky=W)

	exit_button = Button(root, text="Quit", command=lambda root=root: close_window(root), bg= "blue")
	exit_button.grid(sticky = S)

	mainloop()

def close_window(root):
	root.destroy()

def go_home(root):
	root.destroy()
	home_page()

home_page()
# player_buttons(get_player_stats)