class ScoreContext:
	def __init__(self, hand, jokers):
		self.chips = 0
		self.mult = 0
		self.money = 0

		self.hand = hand
		self.jokers = jokers

	def add_chips(self, n): self.chips += n
	def add_mult(self, n):  self.mult += n
	def x_mult(self, n):    self.mult *= n