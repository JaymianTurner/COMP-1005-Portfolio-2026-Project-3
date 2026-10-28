from card import Card
import hand_types
import random

class Deck:
	def __init__(self):
		self.cards : list[Card] = []

		for suit in [Card.SPADES, Card.CLUBS, Card.HEARTS, Card.DIAMONDS]:
			for rank in range(2,15):
				self.cards.append(Card(rank, suit))

		self.__full_deck : list[Card] = list(self.cards)
		self.__played_pile : list[Card] = []
		self.__discard_pile : list[Card] = []

	def __str__(self):
		string = f"[{len(self.cards)} cards]"
		for card in self.cards:
			string += f"[{card}]"
		return string

	def get_played_pile(self):
		return self.__played_pile
	played_pile = property(get_played_pile)
	
	def get_discard_pile(self):
		return self.__discard_pile
	discard_pile = property(get_discard_pile)

	def shuffle(self) -> None:
		random.shuffle(self.cards)

	def deal_card(self) -> Card:
		card = self.cards.pop()
		return card	

	def restore(self) -> None:
		self.cards = self.__full_deck

class Hand:
	def __init__(self, deck : Deck):
		self.__cards : list[Card] = []
		self.__hand_size = 8

		self.deck = deck

	def __str__(self):
		string = f""
		for card in self.__cards:
			string += f"{card} "
		return string

	def get_cards(self) -> list[Card]: return self.__cards
	cards = property(get_cards)

	def get_scoring_cards(self) -> list[Card]: return self.__scoring_cards
	scoring_cards = property(get_scoring_cards)

	def get_hand_size(self) -> int: return self.__hand_size
	hand_size = property(get_hand_size)
	

	def discard(self, index):
		if index < 0 or index > len(self.__cards):
			return
		self.deck.discard_pile.append(self.__cards.pop(index))

		self.fill_hand()

	def fill_hand(self):
		for i in range(8 - len(self.__cards)):
			self.__cards.append(self.deck.deal_card())

	def sort_rank(self):
		self.__cards.sort(key=lambda x: x.rank, reverse=True)

	def empty(self):
		self.__cards = []

	def evaluate(self):

		if self.__cards == []: return

		scoring_cards = None
		best_hand_type = None
		for hand_type in hand_types.HandType.__subclasses__():
			eval = hand_type.evaluate(self.__cards)
			if eval != None:
				scoring_cards = eval
				best_hand_type = hand_type

		print(scoring_cards)
		print(best_hand_type)