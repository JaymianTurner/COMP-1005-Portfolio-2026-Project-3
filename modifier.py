from score_context import ScoreContext
from card import Card

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
	name =""
	def __str__(self): return self.name
	pass

class GreedyJoker(Joker):
	name = "Greedy Joker"
	def on_card_scored(self, context, card):
		if card.suit == card.DIAMONDS: context.add_mult(3)