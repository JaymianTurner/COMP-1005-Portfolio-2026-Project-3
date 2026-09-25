from card import Card

import helpers

class HandType:
	name = ""

	base_chips = 0
	base_mult = 0

	level_chips = 0
	level_mult = 0

	def __init__(self):
		self.level = 1

	def chips(self): return self.base_chips + (self.level_chips * (self.level - 1))

	def mult(self): return self.base_mult + (self.level_mult * (self.level - 1))

	@staticmethod
	def evaluate(cards : list[Card]) -> list[Card] | None:
		"""Returns the scoring cards if this type matches, else None."""
		raise NotImplementedError

	
class HighCard(HandType):
	name, base_chips, base_mult = "High Card" , 5, 1
	level_chips, level_mult = 10, 1

	def evaluate(cards : list[Card]) -> list[Card] | None:
		sorted_cards = sorted(cards, key=lambda c: c.rank)
		return sorted_cards[0]

class Pair(HandType):
	name, base_chips, base_mult = "Pair", 10, 2
	level_chips, level_mult = 15, 1

	def evaluate(cards : list[Card]) -> list[Card] | None:
		groups = helpers.group_by_rank(cards)

		if groups and len(groups[0]) >= 2:
			return groups[0][:2] 
		else: return None

class TwoPair(HandType):
	name, base_chips, base_mult = "Two Pair", 20, 2
	level_chips, level_mult = 20, 1

	def evaluate(cards : list[Card]) -> list[Card] | None:
		groups = helpers.group_by_rank(cards)
		pairs = [g for g in groups if len(g) >= 2]

		if len(pairs) < 2:
			return None
		
		return pairs[0][:2] + pairs[1][:2]

class ThreeOfAKind(HandType):
	name, base_chips, base_mult = "Three Of A Kind", 30, 3
	level_chips, level_mult = 20, 2

	def evaluate(cards : list[Card]) -> list[Card] | None:
		groups = helpers.group_by_rank(cards)

		if groups and len(groups[0]) >= 3:
			return groups[0][:3] 
		else: return None

class Straight(HandType):
	name, base_chips, base_mult = "Straight", 30, 4
	level_chips, level_mult = 30, 3

	def evaluate(cards : list[Card], run_length=5) -> list[Card] | None:
		return helpers.is_straight(cards, run_length)

class Flush(HandType):
	name, base_chips, base_mult = "Flush", 35, 4
	level_chips, level_mult = 15, 2

	def evaluate(cards : list[Card], run_length : int = 5) -> list[Card] | None:
		pass

class FullHouse(HandType):
	name, base_chips, base_mult = "Full House", 40, 4
	level_chips, level_mult = 25, 2

	def evaluate(cards : list[Card]) -> list[Card] | None:
		groups = helpers.group_by_rank(cards)

		if groups and len(groups[0]) >= 3 and len(groups[1]) >= 2:
			return groups[0][:3] + groups[1][:2] 
		else: return None

class FourOfAKind(HandType):
	name, base_chips, base_mult = "Four Of A Kind", 60, 7
	level_chips, level_mult = 30, 3

	def evaluate(cards : list[Card]) -> list[Card] | None:
		groups = helpers.group_by_rank(cards)

		if groups and len(groups[0]) >= 4:
			return groups[0][:4] 
		else: return None

class StraightFlush(HandType):
	name, base_chips, base_mult = "Straight Flush", 100, 8
	level_chips, level_mult = 40, 4

	def evaluate(cards : list[Card], run_length : int = 5) -> list[Card] | None:
		pass

class FiveOfAKind(HandType): pass
class FlushHouse(HandType): pass
class FlushFive(HandType): pass

# testing
cards = [Card(10, Card.SPADES), Card(9, Card.CLUBS), Card(7, Card.SPADES), Card(8, Card.HEARTS), Card(6, Card.SPADES)]
for card in Straight.evaluate(cards) or []:
	print(card)