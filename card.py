class Card:

	# Suit constants for instantiating cards.
	# e.g. card = Card(1, Card.SPADES)
	SPADES, CLUBS, HEARTS, DIAMONDS = 1, 2, 3, 4

	# Convert numeric values of card's rank to string.
	RANK_NAME : dict[int, str] = {
		11 : "J", 12 : "Q", 13 : "K", 14 : "A",
	}

	RANK_NAME_LONG : dict[int, str] = {
		1 : "One", 2 : "Two", 3 : "Three", 4 : "Four",
		5 : "Five", 6 : "Six", 7 : "Seven", 8 : "Eight",
		9 : "Nine", 10 : "Ten", 11 : "Jack", 12 : "Queen",
		13 : "King", 14 : "Ace"
	}

	# Convert numeric values of card's suit to string.
	SUIT_NAME : dict[int, str] = {
		1 : "♠", 2 : "♣", # Black suites
		3 : "♥", 4 : "♦" # Red suites
	}

	SUIT_NAME_LONG : dict[int, str] = {
		1 : "Spades", 2 : "Clubs", # Black suites
		3 : "Hearts", 4 : "Diamonds" # Red suites
	}



	def __init__(self, rank : int, suit : int, enhancement = None, edition = None, seal = None):
		self.rank = rank
		self.suit = suit
		self.enhancement = enhancement
		self.edition = edition
		self.seal = seal

		self.base_chips = rank if rank < 11 else 10
		if rank == 14: self.base_chips == 11

	def __str__(self):
		rank_name = self.rank if self.rank < 11 else self.RANK_NAME[self.rank]
		return f"{rank_name}{self.SUIT_NAME[self.suit]}"

	def get_long_name(self) -> str:
		return f"{self.RANK_NAME_LONG[self.rank]} of {self.SUIT_NAME_LONG[self.suit]}"
	long_name = property(get_long_name)

	def modifiers(self):
		return [m for m in (self.enhancement, self.edition, self.seal) if m]