# **Player Wellfare Tracker**

**Author:** Benji Hannam

**Last Updated:** March 1st 2017

**Introductory Notes:**

The idea behind this library is to create an **easy to use** system for coaches and medical trainers on sports teams to use when **tracking the amount of wear and tear** that is being placed on their players' bodies. On top of this there is also the aim to be able to quickly and easily pull up relevant information regarding the injury status of the players, to enable the **coaches and trainers to make more informed decisions** about the fitness of their players.

##**Installation:**

1. Download/clone the repository into the desired location
2. using the command line cd into the repository
3. (RECOMMENDED) install virtualenv, https://virtualenv.pypa.io/en/stable/ and create a virtual environment folder (I callend mine venv) inside the directory,
   E.g Player_Welfare_Tracker/venv

4. On the command line call:
	
		source venv/bin/activate
   
	This should set up the virtual environment which will allow you to install libraries without affecting your other files. A (venv) should appear on the command line before the path to show that it worked, E.g:

   		(venv) [machine name]:Player_Wellfare_Monitor [username]$

5. On the command line call:
	
		pip install -r requirements.txt

##**Running:**
Once the user is inside the directory and has activated the virtual environment (source venv/bin/activate) then the call to run the program is:

		python interface.py

## **Documentation**

####**Basic Database Structure:**
	
The database is as of this moment planned to be structured as follows, the braces () will indicate an example of each field:

	- User(Benji_Hannam)

		- first_name: ('Benji')

		- last_name: ('Hannam')

		- is_injured: (False)

		- position: (7)

		- sessions

			- type of session (contact)

				- Date (03-03-2017) : Number of minutes (80)

			- type of session (non-contact)

					- Date (02-03-2017) :  Number of minutes (120) 

		- injuries

			- injury name (thing_strain)

				- body_part : ('thigh')

				- type : ('strain')

				- is_current : (True)

				-logs:
						- Date (25-02-2017) : Notes ('Initial recording of injury.')

						- Date (27-02-2017) : Notes ('Strain has subsided considerably but still bothers the player. Will monitor over the coming weeks.')

		- feedback

				- Date (03-03-2017) : tiredness (8)

				- Date (04-03-2017) : tiredness (5)

Notes:
	
1. All dates should be in the form of DD-MM-YYYY
2. 'tiredness' is a personal ranking out of 10 for how the player felt after a session on that date, how that is to be entered is TBD


####**Adding Players:**

There are two main ways to add players to the database as of this moment. They are:

1. **Import from a .csv file.** 
	A .csv file can be created as an excel file except when it is saved ensure that is is saved in the .csv format (similar to saving a word doc as a pdf). The format of the rows should be: [first] [last] [position]. E.g:

		     A      B        C
		(1) John   Smith     7
		(2) Owen   Farrel	 10
		(3) Elliot Daly      13

		Notes:
			1.There should be no title row with column headers
			2.The position should be given as a number not the name, E.g 7 instead of "Flanker".

2. **Manually import via stdin.**
	The user will be prompted to fill out fields for the first name, last name and position of the player as a number (E.g 7 instead of Flanker).



####**Adding A Session:**

When first trying to add a sessiom the user will be prompted to fill in what type of session (contact/non-contact/match) and will be given the chance to manually chose the date of the session. If the user opts to manually enter the date then they will be asked to fill in the day, month and year is the following formats: DD, MM, YYYY. E.g 01-03-2018. If they opt to not do it manually then the current date will be used.

Once the preliminary information has been filled there will be two main options to add a session to the database as of this moment. They are:

1. **Import from a .csv file.** 
A .csv file can be created as an excel file except when it is saved ensure that is is saved in the .csv format (similar to saving a word doc as a pdf). The format of the rows should be: [first] [last] [minutes]. E.g:

		     A      B        C
		(1) John   Smith     80
		(2) Owen   Farrel	 40
		(3) Elliot Daily     60

		Notes:
			1.There should be no title row with column headers
			2.The position should be given as a number not the name, E.g 7 instead of "Flanker".

2. **Manually import via stdin.** 
	The user will be prompted to enter the number of minutes that the session was and then will be asked for each player in the database whether they want to add the minutes to them or not.










