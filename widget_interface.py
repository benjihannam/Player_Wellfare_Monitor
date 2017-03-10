########################################### WIDGET TESTING ###########################################
def test():
	master = Tk()

	players = get_players(firebase)
	i = 0

	for name in sorted(players):
		new_button = Button(master, text=name, command=lambda name=name: action(name))
		new_button.grid(row = i)
		i += 1

	# b = Button(master, text="get", width=10, command=callback)
	# b.grid(row = 2, columnspan=2)

	mainloop()

def action(name):
    # print e.get()
    # print c.get()
    print name
    # master.destroy()
    # test()

def home_page():
	root = Tk()
	T0 = Text(root, height=1, width=70)
	T1 = Text(root, height=1, width=70)

	T0.grid(row = 0)
	T1.grid(row = 1)

	T0.insert(END, "Welcome to the Player Welfare Tracker (PWT).")
	T1.insert(END, "What would you like do to?")
	b1 = Button(root, text="1. Add players.", command=lambda name="test": action(name))
	b2 = Button(root, text="2. Add a session.", command=lambda name="test": action(name))
	b3 = Button(root, text="3. Add an injury.", command=lambda name="test": action(name))

	b1.grid(row = 2, sticky=W)
	b2.grid(row = 3, sticky=W)
	b3.grid(row = 4, sticky=W)

	mainloop()


# home_page()
test()