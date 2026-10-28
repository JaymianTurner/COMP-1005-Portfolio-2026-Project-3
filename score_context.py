from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class ScoreEvent:
	kind: str
	amount: float
	source: object

ScoreListener = Callable[["ScoreContext", ScoreEvent], None]

class ScoreContext:
	def __init__(self, game, scoring_cards : list, held_cards : list, h_type, h_type_lvl : int,
	             jokers : list, hands : int, discards : int, on_event : ScoreListener | None = None):
		
		self.scoring_cards = scoring_cards
		self.held_cards = held_cards

		self.hand_type = h_type

		self.jokers = list(jokers)
		self.joker_max = game.joker_max

		self.hands = hands
		self.discards = discards

		self.on_event = on_event

		extra_levels = h_type_lvl - 1
		self.chips = h_type.base_chips + h_type.level_chips * extra_levels
		self.mult = h_type.base_mult + h_type.level_mult * extra_levels

		self.money = 0

		self.source = None

	def emit(self, kind : str, amount : float = 0):
		if self.on_event:
			self.on_event(self, ScoreEvent(kind, amount, self.source))

	def add_chips(self, n):
		self.chips += n
		self.emit("chips", n)

	def add_mult(self, n):
		self.mult += n
		self.emit("mult", n)

	def x_mult(self, n):
		self.mult *= n
		self.emit("xmult", n)

	def add_money(self, n):
		self.money += n
		self.emit("money", n)