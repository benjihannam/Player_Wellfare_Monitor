class injury():

	def __init__(self, initial_date, body_part, type_of, time_left, notes):

		self.initial_date = initial_date
		self.body_part = body_part
		self.type_of = type_of
		self.notes = notes
		self.time_left = time_left

	def __str__(self):
		return "Type : " + self.type_of + ", Location : " + self.body_part + ", Date Occured : " + self.initial_date + ", Time Left : " + str(self.time_left) + ", Additional Notes : " + self.notes


