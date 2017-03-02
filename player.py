import injury

class player():

	def __init__(self, first, last, pos):

		self.first = first
		self.last = last
		self.pos = pos
		self.minutes = 0
		self.injuries = set([])

	def __str__(self):

		main_str = "First : " + self.first + ", Last : " + self.last + ", Position: " + self.pos + "\n\n"

		injury_str = ""
		for injury in self.injuries:
			injury_str += str(injury)


		return main_str