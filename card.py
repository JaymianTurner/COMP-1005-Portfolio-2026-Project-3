class Card:

	# Suit constants for instantiating cards.
	# e.g. card = Card(1, Card.SPADES)
	SPADES, CLUBS, HEARTS, DIAMONDS = 1, 2, 3, 4

	# Convert numeric values of card's rank to string.
	RANK_NAME : dict[int, str] = {
		11 : "J", 12 : "Q", 13 : "K", 14 : "A",
	}

	# Convert numeric values of card's suit to string.
	SUIT_NAME : dict[int, str] = {
		1 : "♠", 2 : "♣", # Black suites
		3 : "♥", 4 : "♦" # Red suites
	}



	def __init__(self, rank : int, suit : int, enhancement = None, edition = None, seal = None):
		self.rank = rank
		self.suit = suit
		self.enhancement = enhancement
		self.edition = edition
		self.seal = seal

	def __str__(self):
		rank_name = self.rank if self.rank < 11 else self.RANK_NAME[self.rank]
		return f"{rank_name}{self.SUIT_NAME[self.suit]}"

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