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
def player_buttons(action, root):
	if root != None:
		root.destroy()
	master = Tk()
	master.title("Player Select")

	#get all the player in the database
	players = get_players(firebase)

	#for each player create a button and place appropriately in the grim
	x = 0
	for name in sorted(players):
		new_button = Button(master, text=name, command=lambda name=name: action(name, master), bg= "blue")
		new_button.grid(row = x % 10, column = (x / 10), sticky =W)
		x += 1

	exit_button = Button(master, text="Go back", command=lambda root=master: go_home(root), bg= "blue")
	exit_button.grid(row = x % 10 + 2, column = (x / 20))

	mainloop()

def get_player_stats(name, root):
	old_root = root
	# root.destroy()
	curr_root = Tk()
	curr_root.title(name)

	name_parts = name.split("_")
	player_string = get_player(firebase, name_parts[0], name_parts[1])

	first = player_string['first_name']
	last = player_string['last_name']
	position = str(player_string["position"])
	minutes = str(player_string["total_minutes"])

	# Field Labels
	T0 = Label(curr_root, text="First: ", anchor = "w")
	T1 = Label(curr_root, text="Last : ", anchor = "w")
	T2 = Label(curr_root, text="Position: ", anchor = "w")
	T3 = Label(curr_root, text="Total Minutes : ", anchor = "w")

	# Field value
	first_label = Label(curr_root, text=first, anchor = "w")
	last_label = Label(curr_root, text=last, anchor = "w")
	position_label = Label(curr_root, text=position, anchor = "w")
	minutes_label = Label(curr_root, text=minutes, anchor = "w")

	# Edit Buttons
	b3 = Button(curr_root, text="Edit", command=lambda field="position": edit_field(field, name, curr_root, old_root), bg= "blue")
	b4 = Button(curr_root, text="Edit", command=lambda field="total_minutes": edit_field(field, name, curr_root, old_root), bg= "blue")

	# Add to Grid

	T0.grid(row = 0, sticky = W)
	T1.grid(row = 1, sticky = W)
	T2.grid(row = 2, sticky = W)
	T3.grid(row = 3, sticky = W)

	first_label.grid(row = 0, column = 1, sticky = W)
	last_label.grid(row = 1, column = 1, sticky = W)
	position_label.grid(row = 2, column = 1, sticky = W)
	minutes_label.grid(row = 3, column = 1, sticky = W)

	b3.grid(row = 2, sticky=W, column = 2)
	b4.grid(row = 3, sticky=W, column = 2)

def edit_field(field, name, old_root, base_root):
	base_root = base_root
	old_root.destroy()
	curr_root = Tk()
	curr_root.title("Update Player")

	string = "Enter a new " + field + ": "

	label = Label(curr_root, text=string)
	e = Entry(curr_root)
	b = Button(curr_root, text="Update", command=lambda name=name: change_value(name, curr_root, field, e.get(), base_root), bg= "blue")

	label.grid(row = 0)
	e.grid(row = 0, column = 1)
	b.grid(row = 0, column = 2)
	pass

def change_value(name, curr_root, field, value, base_root):
	base_root.destroy()
	path = '/players/'+ name
	firebase.put(path,field, value)
	# get_player_stats(name, curr_root)
	player_buttons(get_player_stats, curr_root)

def add_player_menu(root):
	root.destroy()
	curr_root = Tk()

	# Field Labels
	T0 = Label(curr_root, text="First: ", anchor = "w")
	T1 = Label(curr_root, text="Last : ", anchor = "w")
	T2 = Label(curr_root, text="Position: ", anchor = "w")
	T3 = Label(curr_root, text="Total Minutes : ", anchor = "w")

	first = Entry(curr_root)
	last = Entry(curr_root)
	position = Entry(curr_root)

	T0.grid(row = 0, sticky = W)
	T1.grid(row = 1, sticky = W)
	T2.grid(row = 2, sticky = W)
	T3.grid(row = 3, sticky = W)

def home_page():
	root = Tk()
	root.title("Player Tracker")
	# root.geometry("500x400")

	T0 = Label(root, text="Welcome to the Player Welfare Tracker (PWT).")
	T1 = Label(root, text="What would you like do to?")
	T0.grid(row = 0, sticky = W)
	T1.grid(row = 1, sticky = W)

	b1 = Button(root, text="1. Add players.", command=lambda name="test": action(name), bg= "blue")
	b2 = Button(root, text="2. Add a session.", command=lambda name="test": action(name), bg= "blue")
	b3 = Button(root, text="3. Add an injury.", command=lambda name="test": action(name), bg= "blue")
	b4 = Button(root, text="4. Get the stats for a player.", command=lambda name=get_player_stats: player_buttons(name, root), bg= "blue")

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