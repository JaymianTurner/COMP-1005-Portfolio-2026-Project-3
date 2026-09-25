from score_context import ScoreContext
from card import Card

# Base class for anything that reacts to scoring.
# Card enhancements or jokers, etc...

# For this base class, all hooks will default to a no-op.
# Objects that inherit from this can choose to override any of the hooks depending on the effect.

class Modifier:

	# Trigger for card scored while in played hand.
	def on_card_scored(self, context : ScoreContext, card : Card): pass
	# Trigger for card held in played hand.
	def on_card_held(self, context : ScoreContext, card : Card): pass
	# Trigger for when hand itself is scored.
	def on_hand_scored(self, context : ScoreContext): pass

	# Return how many triggers the class will have.
	def retriggers(self, context : ScoreContext, card : Card) -> int: return 0