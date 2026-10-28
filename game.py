from deck import Deck
import modifier as j
import hand_types

class Game:
	def __init__(self):
		self.round = 1
		self.ante = 1
		self.money = 0

		self.deck = Deck()

		self.__jokers : list = [j.Jimbo(), j.BusinessCard(), j.StencilJoker()]
		self.joker_max : int = 5

		self.__consumables : list = []
		self.consumable_max : int = 2

		self.hand_type_levels : dict[str, int] = {h.name: 2 for h in hand_types.HandType.__subclasses__()}

	def get_jokers(self): return self.__jokers
	jokers = property(get_jokers)

	def add_joker(self, joker):
		if len(self.__jokers) >= self.joker_max: return

		self.__jokers.append(joker)

	def remove_joker(self, i : int, sell = True):
		try:
			if sell: self.__money += self.__jokers[i].value / 2
			del self.__jokers[i]
		except: return

	def move_joker(self, i: int, move: int):
		if (i + move) < 0 or (i + move) > len(self.__jokers): return

		joker = self.__jokers.pop(i)
		self.__jokers.insert(i + move, joker)

	def get_consumables(self): return self.__consumables
	consumables = property(get_consumables)

	def add_consumable(self, consumable):
		if len(self.__consumables) >= self.consumable_max: return

		self.__consumables.append(consumable)

	def use_consumable(self, i: int):
		pass

	def remove_consumable(self, i : int, sell = True):
		try:
			if sell: self.__money += self.__consumables[i].value / 2
			del self.__consumables[i]
		except: return

