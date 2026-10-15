from card import Card
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
		self.cards : list[Card] = []
		self.hand_size = 8

		self.deck = deck

	def __str__(self):
		string = f""
		for card in self.cards:
			string += f"{card} "
		return string

	def discard(self, index):
		if index < 0 or index > len(self.cards):
			return
		self.deck.discard_pile.append(self.cards.pop(index))

		self.fill_hand()


	def fill_hand(self):
		for i in range(8 - len(self.cards)):
			self.cards.append(self.deck.deal_card())

	def empty(self):
		self.cards = []

deck = Deck()

print(deck)

deck.shuffle()

hand = Hand(deck)

hand.fill_hand()

print(hand)

hand.discard(3)
print(hand)

print(deck)
hand.empty()
deck.restore()
print(deck)