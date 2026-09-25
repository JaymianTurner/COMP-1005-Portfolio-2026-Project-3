class Card:

	# Suit constants for instantiating cards.
	# e.g. card = Card(1, Card.SPADES)
	SPADES, CLUBS, HEARTS, DIAMONDS = 1, 2, 3, 4

	# Convert numeric values of card's rank to string.
	RANK_NAME : dict[int, str] = {
		# Number ranks
		1 : "Ace", 2 : "Two", 3 : "Three", 4 : "Four", 5 : "Five",
		6 : "Six", 7 : "Seven", 8 : "Eight", 9 : "Nine", 10 : "Ten",
		# Face ranks
		11 : "Jack", 12 : "Queen", 13 : "King"
	}

	# Convert numeric values of card's suit to string.
	SUIT_NAME : dict[int, str] = {
		1 : "Spades", 2 : "Clubs", # Black suites
		3 : "Hearts", 4 : "Diamonds" # Red suites
	}



	def __init__(self, rank : int, suit : int, enhancement = None, edition = None, seal = None):
		self.rank = rank
		self.suit = suit
		self.enhancement = enhancement
		self.edition = edition
		self.seal = seal

	def __str__(self):
		return f"{self.RANK_NAME[self.rank]} of {self.SUIT_NAME[self.suit]}"

	def get_rank_name(self) -> str:
		# Get name of card's rank.
		# e.g. 'Ace', 'Ten', 'King'.
		return self.RANK_NAME[self.rank]
	rank_name = property(get_rank_name)

	def get_suit_name(self) -> str:
		# Get name of card's suit.
		# e.g. 'Spades', 'Clubs', 'Hearts', 'Diamonds'.
		return self.SUIT_NAME[self.suit]
	suit_name = property(get_suit_name)

	def modifiers(self):
		return [m for m in (self.enhancement, self.edition, self.seal) if m]


ten_of_spades = Card(10, Card.SPADES)
print(ten_of_spades)

king_of_hearts = Card(13, Card.HEARTS)
print(king_of_hearts)