from score_context import ScoreContext
from card import Card

import hand_types
import random

from abc import ABC, abstractmethod

# Base class for anything that reacts to scoring.
# Card enhancements or jokers, etc...

# Objects that inherit from this can choose to override any of the hooks depending on the effect.

class Modifier(ABC):

	# Trigger for card scored while in played hand.
	def on_card_scored(self, context : ScoreContext, card : Card): pass

	# Trigger for card held in played hand.
	def on_card_held(self, context : ScoreContext, card : Card): pass

	# Trigger for when hand itself is scored.
	def on_hand_scored(self, context : ScoreContext): pass

	# Return how many triggers the class will have.
	def retriggers(self, context : ScoreContext, card : Card) -> int: return 0

	def held_retriggers(self, context : ScoreContext, card : Card) -> int: return 0

class Joker(Modifier, ABC):
	name, cost = "", 0

	def __str__(self): return self.name
	pass

class Jimbo(Joker):
	name, cost = "Jimbo", 2
	def retriggers(self, context, card):
		if card == context.scoring_cards[0]:
			return 3
		return 0
		
	def on_hand_scored(self, context):
		context.add_mult(4)

class WrathfulJoker(Joker):
	name, cost = "Wrathful", 5
	def on_card_scored(self, context, card):
		if card.suit == card.SPADES: context.add_mult(3)
class GluttonousJoker(Joker):
	name, cost = "Gluttonous", 5
	def on_card_scored(self, context, card):
		if card.suit == card.CLUBS: context.add_mult(3)
class LustyJoker(Joker):
	name, cost = "Lusty", 5
	def on_card_scored(self, context, card):
		if card.suit == card.HEARTS: context.add_mult(3)
class GreedyJoker(Joker):
	name, cost = "Greedy", 5
	def on_card_scored(self, context, card):
		if card.suit == card.DIAMONDS: context.add_mult(3)


class JollyJoker(Joker):
	name, cost = "Jolly J.", 3
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.Pair): context.add_mult(8)
class ZanyJoker(Joker):
	name, cost = "Zany J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.ThreeOfAKind): context.add_mult(12)
class MadJoker(Joker):
	name, cost = "Mad J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.TwoPair): context.add_mult(10)
class CrazyJoker(Joker):
	name, cost = "Crazy J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.Straight): context.add_mult(12)
class DrollJoker(Joker):
	name, cost = "Droll J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.Flush): context.add_mult(10)


class SlyJoker(Joker):
	name, cost = "Sly J.", 3
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.Pair): context.add_chips(50)
class WilyJoker(Joker):
	name, cost = "Wily J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.ThreeOfAKind): context.add_chips(100)
class CleverJoker(Joker):
	name, cost = "Clever J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.TwoPair): context.add_chips(80)
class DeviousJoker(Joker):
	name, cost = "Devious J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_type, hand_types.Straight): context.add_chips(100)
class CraftyJoker(Joker):
	name, cost = "Crafty J.", 4
	def on_hand_scored(self, context):
		if isinstance(context.hand_typem, hand_types.Flush): context.add_chips(80)

	
class HalfJoker(Joker):
	name, cost = "Half J.", 5
	def on_hand_scored(self, context):
		if len(context.scoring_cards) <= 3: context.add_mult(20)

class StencilJoker(Joker):
	name, cost = "Stencil J.", 8
	def on_hand_scored(self, context):
		context.x_mult(context.joker_max - len(context.jokers) + 1)

class BusinessCard(Joker):
	name, cost = "Business Card", 4
	def on_card_scored(self, context, card):
		if random.choice([True, False]) and card.is_face_card():
			context.add_money(2)

# class FourFingers(Joker):
# 	#TODO
# 	name, cost = "4 Fingers", 7

class Mime(Joker):
	name, cost = "Mime", 5
	def held_retriggers(self, context, card):
		return 1

# class CreditCard(Joker):
# 	#TODO
# 	name, cost = "Credit Card", 1

# class CeremonialDagger(Joker):
# 	#TODO
# 	name, cost = "Dagger", 6

class Banner(Joker):
	name, cost = "Banner", 5
	def on_hand_scored(self, context):
		context.add_chips(30 * context.discards)

class MysticSummit(Joker):
	name, cost = "M. Summit", 5
	def on_hand_scored(self, context):
		if context.discards <= 0: context.add_mult(15)

# class MarbleJoker(Joker):
# 	name, cost = "Marble J.", 6
# 	#TODO

class LoyaltyCard(Joker):
	name, cost = "Loyalty C.", 5
	def __init__(self):
		self.__hands_played = 0

	def __str__(self):
		return f"{self.name} ({self.__hands_played}/6){"!!" if self.__hands_played == 6 else ""}"

	def on_hand_scored(self, context):
		self.__hands_played += 1
		if self.__hands_played == 6:
			context.x_mult(4)
			self.__hands_played = 0

# class EightBall(Joker):
# 	name, cost = "8Ball", 5
# 	#TODO

class Misprint(Joker):
	name, cost = "Misprint", 4
	def on_hand_scored(self, context):
		context.add_mult(random.randint(0,23))

class Dusk(Joker):
	name, cost = "Dusk", 5
	def retriggers(self, context, card):
		return 1 if context.hands == 1 else 0

class RaisedFist(Joker):
	name, cost = "Raised Fist", 5
	def on_hand_scored(self, context):
		if context.held_cards == []: return
		lowest_card = sorted(context.held_cards, lambda c: c.rank)[0]
		context.add_mult(lowest_card.rank * 2)

# class ChaosClown(Joker):
# 	name, cost = "Chaos Clown", 4
# 	#TODO

class Fibonacci(Joker):
	name, cost = "Fibonacci", 8
	def on_card_scored(self, context, card):
		if card.rank in [14, 2, 3, 5, 8]:
			context.add_mult(8)