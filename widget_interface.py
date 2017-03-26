#Author: Benji Hannam

from dartmouthrugby import *
# firebase import
from firebase import firebase

# file system import
from Tkinter import *
from tkFileDialog import askopenfilename
import time
import csv
#the server
firebase = firebase.FirebaseApplication('https://drfc-tracker.firebaseio.com', None)

########################################### WIDGET TESTING ###########################################
def player_buttons(action, root):
	if root != None:
		root.destroy()
	curr_root = Tk()
	curr_root.title("Player Select")

	#get all the player in the database
	players = get_players(firebase)

	#for each player create a button and place appropriately in the grim
	x = 0
	for name in sorted(players):
		new_button = Button(curr_root, text=name, command=lambda name=name: action(name, curr_root), bg= "blue")
		new_button.grid(row = x % 10, column = (x / 10), sticky =W)
		x += 1

	exit_button = Button(curr_root, text="Go back", command=lambda root=curr_root: go_home(root), bg= "blue")
	exit_button.grid(sticky=S+E, column = (x / 10))

	mainloop()

##############################################################################################################################
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

	free_row = 6
	if 'injuries' in player_string:
		injuries = player_string['injuries']
		T4 = Label(curr_root, text="Injuries : ", anchor = "w")
		T4.grid(row = 4, sticky = W)
		for injury in injuries:
			new_injury = Button(curr_root, text=injury, command=lambda injury=injury: get_injury(), bg= "blue")
			new_injury.grid(row = free_row, columnspan=2)
			free_row += 1 

	if 'sessions' in player_string:
		sessions = player_string['sessions']
		T5 = Label(curr_root, text="Sessions : ", anchor = "w")
		T5.grid(row = free_row, sticky = W)
		free_row += 1
		for session_type in sessions:
			new_session = Button(curr_root, text=session_type, command=lambda session=session_type: get_injury(), bg= "blue")
			new_session.grid(row = free_row, columnspan=2)
			free_row += 1

	exit_button = Button(curr_root, text="Close", command=lambda root=root: close_window(curr_root), bg= "blue")
	exit_button.grid(sticky=S+E, column = 2)

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

	def change_value(name, curr_root, field, value, base_root):
		base_root.destroy()
		path = '/players/'+ name
		firebase.put(path,field, value)
		# get_player_stats(name, curr_root)
		player_buttons(get_player_stats, curr_root)

	# def display_injury()

##############################################################################################################################

def add_player_menu(root):
	root.destroy()
	curr_root = Tk()
	curr_root.title("Add Players")


	# Field Labels
	T0 = Label(curr_root, text="First: ", anchor = "w")
	T1 = Label(curr_root, text="Last: ", anchor = "w")
	T2 = Label(curr_root, text="Position: ", anchor = "w")

	T0.grid(row = 0, column = 0, sticky = W)
	T1.grid(row = 0, column = 1, sticky = W)
	T2.grid(row = 0, column = 2, sticky = W)

	players = []
	# Entry fields
	for i in range(5):	

		first = Entry(curr_root)
		last = Entry(curr_root)
		position = Entry(curr_root)

		first.grid(row = i+1, column = 0, sticky=W)
		last.grid(row = i+1, column = 1, sticky=W)
		position.grid(row = i+1, column = 2, sticky=W)

		new_player = [first, last, position]
		players.append(new_player)

	b = Button(curr_root, text="Add", command=lambda players=players: add_manual_players(players, curr_root), bg= "blue")
	b.grid(row = 6, column = 0, sticky = W)

	or_label = Label(curr_root, text="Or add from a file:")
	or_label.grid(row = 7, column = 0, sticky = W)

	file_entry = Entry(curr_root)
	file_entry.grid(row = 9, column = 0, sticky = W)
	choose_button = Button(curr_root, text="Choose File", command=lambda file_entry=file_entry: file_path(file_entry), bg= "blue")
	choose_button.grid(row = 8, column = 0, sticky = W)

	def file_path(file_entry):
		file_name = askopenfilename()
		file_entry.insert(0, file_name)

	b1 = Button(curr_root, text="Add", command=lambda file_entry=file_entry: add_file_players(file_entry, curr_root), bg= "blue")
	b1.grid(row = 10, column = 0, sticky = W)

	exit_button = Button(curr_root, text="Go back", command=lambda root=curr_root: go_home(root), bg= "blue")
	exit_button.grid(sticky=S+E, column = 2) 

	def add_manual_players(players, root):
		for i in range(len(players)):
			if players[i][0].get() != "" and players[i][1].get() != "" and players[i][2].get() != "":
				add_player(firebase, players[i][0].get(), players[i][1].get(), players[i][2].get())
				players[i][0].delete(0, END)
				players[i][1].delete(0, END)
				players[i][2].delete(0, END)
		
		root.destroy()
		home_page()

	def add_file_players(file_entry, root):
		add_players_from_file(firebase, file_entry.get())
		file_entry.delete(0, END)
		root.destroy()
		home_page()

##############################################################################################################################
def delete_players_widget(name, root):
	root.destroy()
	curr_root = Tk()
	curr_root.title("Check Delete")
	check_label = Label(curr_root, text="Are you sure you want to delete " + name + "?")
	check_label.grid(row=0, columnspan = 2)

	yes_button = Button(curr_root, text = "Yes", command=lambda name=name: delete_and_return(name), bg= 'blue')
	no_button = Button(curr_root, text="No", command=lambda name=name: player_buttons(delete_players_widget, curr_root), bg= 'blue')

	yes_button.grid(row = 1, column = 0)
	no_button.grid(row=1, column = 1)
	def delete_and_return(name):
		delete_player(firebase, name)
		player_buttons(delete_players_widget, curr_root)
	pass
##############################################################################################################################
def add_session_menu(root):
	root.destroy()
	curr_root = Tk()
	curr_root.title("Add Session")

	# Get the date of the session
	date_label = Label(curr_root, text="Enter Date of session(DD/MM/YYYY), if left empty will default to today: ")
	date_label.grid(row = 0, sticky=W, columnspan = 3)
	day = Entry(curr_root)
	month = Entry(curr_root)
	year = Entry(curr_root)
	day.grid(row = 1, column = 0, sticky = W)
	month.grid(row = 1, column = 1, sticky = W)
	year.grid(row = 1, column = 2, sticky = W)

	# Get the type of the session
	type_label = Label(curr_root, text="Enter type of session(contact, non-contact, match): ")
	type_label.grid(row = 2, sticky=W, columnspan = 3)
	type_entry = Entry(curr_root)
	type_entry.insert(0, "")
	type_entry.grid(row = 3, column = 0)

	beginning_row = 4
	### Adding manually

	# Field Labels
	T0 = Label(curr_root, text="First: ", anchor = "w")
	T1 = Label(curr_root, text="Last: ", anchor = "w")
	T2 = Label(curr_root, text="Num Minutes: ", anchor = "w")

	T0.grid(row = beginning_row, column = 0, sticky = W)
	T1.grid(row = beginning_row, column = 1, sticky = W)
	T2.grid(row = beginning_row, column = 2, sticky = W)

	players = []
	# Entry fields
	for i in range(5):	

		first = Entry(curr_root)
		last = Entry(curr_root)
		minutes = Entry(curr_root)

		first.grid(row = i+beginning_row + 1, column = 0, sticky=W)
		last.grid(row = i+beginning_row + 1, column = 1, sticky=W)
		minutes.grid(row = i+beginning_row + 1, column = 2, sticky=W)

		new_player = [first, last, minutes]
		players.append(new_player)

	# Add Button
	b = Button(curr_root, text="Add", command=lambda players=players: add_manual_sessions(players, curr_root), bg= "blue")
	b.grid(row = 7 + beginning_row, column = 0, sticky = W)

	#Error label
	error_label1 = Label(curr_root, text="")
	error_label1.grid(row = 6+beginning_row)


	### Add from file
	or_label = Label(curr_root, text="Or add from a file:")
	or_label.grid(row = 8+beginning_row, column = 0, sticky = W)

	file_entry = Entry(curr_root)
	file_entry.grid(row = 10+beginning_row, column = 0, sticky = W)
	choose_button = Button(curr_root, text="Choose File", command=lambda file_entry=file_entry: file_path(file_entry), bg= "blue")
	choose_button.grid(row = 9+beginning_row, column = 0, sticky = W)

	# Get the file path as a string
	def file_path(file_entry):
		file_name = askopenfilename()
		file_entry.insert(0, file_name)

	# Add button
	b1 = Button(curr_root, text="Add", command=lambda file_entry=file_entry: add_file_session(file_entry, curr_root), bg= "blue")
	b1.grid(row = 13+ beginning_row, column = 0, sticky = W)

	# Second error label
	error_label2 = Label(curr_root, text="")
	error_label2.grid(row = 12+beginning_row)

	#quit button
	exit_button = Button(curr_root, text="Go back", command=lambda root=curr_root: go_home(root), bg= "blue")
	exit_button.grid(sticky=S+E, column = 2) 

	def add_manual_sessions(players, root):
		if type_entry.get() == "":
			error_label1.config(text="Error: no session type specified.")
		else:
			error_label1.config(text="Adding in players.")
			for i in range(len(players)):
				if players[i][0].get() != "" and players[i][1].get() != "" and players[i][2].get() != "":
					day_str = None
					month_str = None
					year_str = None
					if day.get() != "":
						day_str = day.get()
					if month.get() != "":
						month_str = month.get()
					if year.get() != "":
						year_str = year.get()
					add_session(firebase, type_entry.get(), players[i][0].get(), players[i][1].get(), players[i][2].get(), day_str, month_str, year_str)
					players[i][0].delete(0, END)
					players[i][1].delete(0, END)
					players[i][2].delete(0, END)
			
			root.destroy()
			home_page()

	def add_file_session(file_entry, root):
		if type_entry.get() == "":
			error_label2.config(text="Error: no session type specified.")
		else:
			error_label2.config(text="Adding from file.")
			day_str = None
			month_str = None
			year_str = None
			if day.get() != "":
				day_str = day.get()
			if month.get() != "":
				month_str = month.get()
			if year.get() != "":
				year_str = year.get()
			add_session_from_file(firebase, type_entry.get(), file_entry.get(), day_str, month_str, year_str)
			file_entry.delete(0, END)
			root.destroy()
			home_page()
##############################################################################################################################
def match_timer_setup(root):
	running = True
	root.destroy()
	curr_root = Tk()
	curr_root.title("Set Up the Players")
	pos_label = Label(curr_root, text="Pos:")
	pos_label.grid(row=0, sticky = W)
	main_first_label = Label(curr_root, text="First:")
	main_first_label.grid(row=0, column = 1, sticky = W)
	main_last_label = Label(curr_root, text="Last:")
	main_last_label.grid(row=0, column = 2, sticky = W)

	first_names = []
	last_names = []
	position_labels = []
	for i in range(23):
		position_label = Label(curr_root, text=str(i+1) + ".")
		first_entry = Entry(curr_root)
		first_names.append(first_entry)
		last_entry = Entry(curr_root)
		last_names.append(last_entry)
		position_label.grid(row=1+i)
		position_labels.append(position_label)
		first_entry.grid(row=1+i, column = 1)
		last_entry.grid(row=1+i, column = 2)

		first_entry.insert(0, "Default")
		last_entry.insert(0, "Default")

	# Add button
	b1 = Button(curr_root, text="Start Timer", command=lambda file_entry=last_entry: match_timer(), bg= "blue")
	b1.grid(row = i+2, column = 1, columnspan = 2)

	#quit button
	exit_button = Button(curr_root, text="Go back", command=lambda root=curr_root: go_home(root), bg= "blue")
	exit_button.grid(sticky=S+E, column = 2) 

	# The page for starting the match timer
	def match_timer():

		def stop_timer(position, timer_list, label_list, start_timer):
			seconds = (datetime.now() - timer_list[position]).seconds % 60
			minutes = (datetime.now() - timer_list[position]).seconds / 60
			time_string = str(minutes) + " mins " + str(seconds) + " secs."
			label_list[position].config(text = time_string)

			seconds_played[position] = (datetime.now() - timer_list[position]).seconds
			print str(position) + ":" + str(seconds_played[position])
			timer_list[position] = None
			show_timer(start_timer)

		def stop_all(timer_list, label_list, start_timer):
			pass

		def start_all(timer_list, label_list, start_timer):
			pass

		def start_player_timer(position, timer_list, label_list, start_timer):
			print str(position) + ":" + str(seconds_played[position])
			if seconds_played[position] == 0:
				timer_list[position] = datetime.now()
			else:
				timer_list[position] = datetime.now() - timedelta(seconds=seconds_played[position])
			show_timer(start_timer)

		def end_and_record(root, start_timer, csv_first_names, csv_last_names, mins_played):
			show_timer(start_timer)
			f = open("import_files/UCLA.csv", 'w')
			try:
				writer = csv.writer(f)
				for i in range(len(csv_first_names)):
					# print csv_first_names[i] + ", " + csv_last_names[i] + ", " + str(mins_played[i] % 60)
					writer.writerow((csv_first_names[i], csv_last_names[i], mins_played[i] / 60))
		 	finally:
		 		f.close()
			

			root.destroy()
			

		start_timer = datetime.now()
		player_start_times = []
		player_timers = []
		seconds_played = []
		csv_first_names = []
		csv_last_names = []

		for i in range(len(first_names)):
			if first_names[i].get() != "":
				first_label = Label(curr_root, text=first_names[i].get())
				last_label = Label(curr_root, text = last_names[i].get())
				first_label.grid(row = 1+i, column = 1, sticky = W)
				last_label.grid(row = 1+i, column = 2, sticky = W)

				player_timer = Label(curr_root, text = "0 mins 0 secs.")
				player_timer.grid(row = 1+i, column = 5)
				player_timers.append(player_timer)

				pause_button = Button(curr_root, text = "Stop", command=lambda position=i: stop_timer(position, player_start_times, player_timers, start_timer), bg= "blue")
				pause_button.grid(row = 1+i, column = 3, sticky = W)
				resume_button = Button(curr_root, text = "Start", command=lambda position=i: start_player_timer(position, player_start_times, player_timers, start_timer), bg= "blue")
				resume_button.grid(row = 1+i, column = 4, sticky = W)

				seconds_played.append(0)
				if i < 15:
					player_start_times.append(start_timer)
				else:
					player_start_times.append(None)

				csv_first_names.append(first_names[i].get())
				csv_last_names.append(last_names[i].get())

			else:
				position_labels[i].destroy()

			first_names[i].destroy()
			last_names[i].destroy()
			

		b1.destroy()
		pos_label.destroy()
		main_last_label.destroy()
		main_first_label.destroy()

		exit_button.destroy()
		#quit button
		new_exit_button = Button(curr_root, text="End and record", command=lambda root=curr_root: end_and_record(root, start_timer, csv_first_names, csv_last_names, seconds_played), bg= "blue")
		new_exit_button.grid(sticky=S+E, column = 5) 

		time_elapsed = Label(curr_root, text="0 mins 0 secs.")
		time_elapsed.grid(row = i+3, column = 2)

		start_button = Button(curr_root, text="Update Elapsed Time",  command=lambda root=curr_root: show_timer(start_timer))
		start_button.grid(row = i + 3)

		def show_timer(start_timer):
			seconds = (datetime.now() - start_timer).seconds % 60
			minutes = (datetime.now() - start_timer).seconds / 60
			time_string = str(minutes) + " mins " + str(seconds) + " secs."
			time_elapsed.config(text = time_string)
			for i in range(len(player_start_times)):
				if player_start_times[i] is not None:
					seconds = (datetime.now() - player_start_times[i]).seconds % 60
					minutes = (datetime.now() - player_start_times[i]).seconds / 60
					time_string = str(minutes) + " mins " + str(seconds) + " secs. (Playing)"
					player_timers[i].config(text = time_string)
					seconds_played[i] = (datetime.now() - player_start_times[i]).seconds

		curr_root.mainloop()



##############################################################################################################################

def home_page():
	root = Tk()
	root.title("Player Tracker")
	# root.geometry("500x400")

	T0 = Label(root, text="Welcome to the Player Welfare Tracker (PWT).")
	T1 = Label(root, text="What would you like do to?")
	T0.grid(row = 0, sticky = W)
	T1.grid(row = 1, sticky = W)

	b1 = Button(root, text="1. Add players.", command=lambda name="test": add_player_menu(root), bg= "blue")
	b2 = Button(root, text="2. Add a session.", command=lambda name="test": add_session_menu(root), bg= "blue")
	b3 = Button(root, text="3. Add an injury.", command=lambda name="test": player_buttons(name), bg= "blue")
	b4 = Button(root, text="4. View/Edit Player.", command=lambda action=get_player_stats: player_buttons(action, root), bg= "blue")
	b5 = Button(root, text="5. Delete Player.", command=lambda action=delete_players_widget: player_buttons(action, root), bg= "blue")
	b6 = Button(root, text="6. Start a match timer.", command=lambda action=delete_players_widget: match_timer_setup(root), bg= "blue")

	b1.grid(row = 2, sticky=W)
	b2.grid(row = 3, sticky=W)
	b3.grid(row = 4, sticky=W)
	b4.grid(row = 5, sticky=W)
	b5.grid(row = 6, sticky=W)
	b6.grid(row = 7, sticky=W)


	exit_button = Button(root, text="Quit", command=lambda root=root: close_window(root), bg= "blue")
	exit_button.grid(sticky = S+E)

	mainloop()

def close_window(root):
	root.destroy()

def go_home(root):
	root.destroy()
	home_page()

home_page()
# player_buttons(get_player_stats)