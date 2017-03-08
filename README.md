**Player Wellfare Tracker**

**Author:** Benji Hannam

**Last Updated:** March 1st 2017

**Introductory Notes:**

The idea behind this library is to create an **easy to use** system for coaches and medical trainers on sports teams to use when **tracking the amount of wear and tear** that is being placed on their players' bodies. On top of this there is also the aim to be able to quickly and easily pull up relevant information regarding the injury status of the players, to enable the **coaches and trainers to make more informed decisions** about the fitness of their players.

**Documentation**

*Basic Database Structure:*
	
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
	
	- All dates should be in the form of DD-MM-YYYY
	- 'tiredness' is a personal ranking out of 10 for how the player felt after a session on that date, how that is to be entered is TBD










