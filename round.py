from game import Game
from deck import Deck, Hand
from blind import Blind
from score_context import ScoreContext
from score_context import ScoreEvent
from scoring_engine import ScoringEngine

from time import sleep
import hand_types

from re import compile

STEP_TIME = 0.4
MAX_SELECTED = 5

CLEAR = "\x1b[H\x1b[2J\x1b[3J"
DIM, UNDIM = "\x1b[2m", "\x1b[22m"
REVERSE, UNREVERSE = "\x1b[7m", "\x1b[27m"
BLUE, RED, GOLD, FG = "\x1b[34m", "\x1b[31m", "\x1b[33m", "\x1b[39m"
_ANSI = compile(r"\x1b\[[0-9;]*m")



ante_requirements : dict[int, int] = {
	1 : 300,
	2 : 800,
	3 : 2800,
	4 : 6000,
	5 : 11000,
	6 : 20000,
	7 : 35000,
	8 : 50000
}

def fmt(n) -> str:
	return str(int(n)) if n == int(n) else f"{n:.2f}".rstrip("0")

def popup_text(event) -> str:
	n = fmt(event.amount)
	match event.kind:
		case "chips":     return f"{BLUE}+{n} chips{FG}"
		case "mult":      return f"{RED}+{n} mult{FG}"
		case "xmult":     return f"{RED}x{n} mult{FG}"
		case "money":     return f"{GOLD}+${n}{FG}"
		case "retrigger": return "Again!"
		case _:           return ""

class Round:
	def __init__(self, game : Game, blind):
		self.__game = game
		self.__round = game.round
		self.__ante = game.ante
		self.__blind = blind
		self.__deck = game.deck
		self.__hand = Hand(self.__deck)

		self.__round_score = 0

		self.__hands = 3
		self.__discards = 3

		self.__selected_indexes : list[int] = []

		self.__info_select_card : int = -1

		self.__goal = ante_requirements[self.__ante] * blind.requirement_multiplier

	def display(self, ctx: ScoreContext | None = None, event = None):

		hand = self.__hand
		game = self.__game

		active = event.source if event else None

		card_str = [str(c) for c in hand.cards]
		card_str_len = [len(c) for c in card_str]

		top_card_row, bottom_card_row = [], []
		for i, (card, text, width) in enumerate(zip(hand.cards, card_str, card_str_len)):
			shown = f"{REVERSE}{text}{UNREVERSE}" if card is active else text
			blank = " " * width
			if i in self.__selected_indexes:
				top_card_row.append(shown)
				bottom_card_row.append(blank)
			else:
				top_card_row.append(blank)
				bottom_card_row.append(shown)

		jokers_str = []

		for j in game.jokers:
			text = f"[{str(j)}]"
			jokers_str.append(f"{REVERSE}{text}{UNREVERSE}" if j is active else text)
		jokers_str += ["[]" for _ in range(game.joker_max - len(jokers_str))]



		consumables_str = [f"[{str(c)}]" for c in game.consumables]
		consumables_str += ["[]" for _ in range(game.consumable_max - len(consumables_str))]

		_, h_type = self.eval_selection()

		hand_name = ""
		if h_type:
			hand_name = f"{h_type.name} {DIM}lvl.{game.hand_type_levels[h_type.name]}{UNDIM}"

		if ctx:
			chips_mult = f"{BLUE}{fmt(ctx.chips)}{FG} {DIM}x{UNDIM} {RED}{fmt(ctx.mult)}{FG}"
		else:
			h_type_name = getattr(h_type, 'name', '')
			h_type_lvl = game.hand_type_levels[h_type_name] if h_type_name != '' else 1
			chips_mult = f"{BLUE}{getattr(h_type, 'base_chips', '0') + getattr(h_type, 'level_chips', '0') * (h_type_lvl - 1)}{FG} {DIM}x{UNDIM} {RED}{getattr(h_type, 'base_mult', '0') + getattr(h_type, 'level_mult', '0') * (h_type_lvl - 1)}{FG}"

		popup = ""
		if event and (text := popup_text(event)):
			popup = f"{event.source} : {text}" if event.source is not None else text 

		blind = self.__blind
		lines = [
			f"Round {self.__round} {DIM}|{UNDIM} Ante {self.__ante}/8",
			"",
			f"{blind.name} {DIM}({blind.desc}){UNDIM}",
			f"Score at least : 𖥕 {int(self.__goal)} {DIM}|{UNDIM} Reward : {("$" * self.__blind.reward)}",
			"",
			f"Round Score : 𖥕 {self.__round_score} {DIM}|{UNDIM} ${game.money}",
			"",
			f"Jokers : {" ".join(jokers_str)} {DIM}({len(game.jokers)}/{game.joker_max}){UNDIM} {DIM}|{UNDIM} Consum. : {" ".join(consumables_str)} {DIM}({len(game.consumables)}/{game.consumable_max}){UNDIM}",
			"",
			hand_name,
			chips_mult,
			"",
			"",
			popup,
			"",
			"",
			" ".join(top_card_row),
			" ".join(bottom_card_row)
		]

		i = self.__info_select_card
		if 0 <= i < len(card_str):
			total_len = sum(card_str_len) + (len(card_str_len) - 1)

			offset = sum(w + 1 for w in card_str_len[:i])
			after = max(total_len - offset - 1, 0)

			info = hand.cards[i]
			lines.append(f"{DIM}{'─' * offset}↑{'─' * after}")
			lines.append(f"{info.long_name}")
			lines.append(f"Base Chips : 𖥕 {info.base_chips}{UNDIM}")

		lines.append(f"Hands : {BLUE}{self.__hands}{FG} {DIM}|{UNDIM} Discards : {RED}{self.__discards}{FG}")

		print(CLEAR + "\n".join(lines), flush=True)

	def start(self):

		self.__deck.shuffle()

		self.__hand.fill_hand()
		self.__hand.sort_rank()

		return self.selection_loop()

	def selection_loop(self):
		while True:
			if self.__round_score >= self.__goal:
				return True
			if self.__hands <= 0:
				return False

			self.display()

			if self.__round == 1:
				print(f"\n{DIM}(Hint: select multiple cards with spaces. 'play' / 'discard' to act, 'info N' for card info){UNDIM}")
			card_select = input("Select card(s)/jokers index - ")
			parts = card_select.split()
			if not parts:
				continue

			command = parts[0].lower()

			if command in ("play", "p"):
				if self.__selected_indexes:
					self.play_hand()

			elif command in ("discard", "d"):
				if self.__selected_indexes and self.__discards > 0:
					self.discard_selected()

			elif command == "info":
				if len(parts) == 1:
					self.__info_select_card = -1
				else:
					try:
						info_card = int(parts[1]) - 1
						self.__info_select_card = -1 if info_card == self.__info_select_card else info_card
					except ValueError:
						continue

			else:
				for part in parts:
					try:
						index = int(part) - 1
					except ValueError:
						continue

					if not 0 <= index < len(self.__hand.cards):
						continue

					if index in self.__selected_indexes:
						self.__selected_indexes.remove(index)
					elif len(self.__selected_indexes) < MAX_SELECTED:
						self.__selected_indexes.append(index)


	def play_hand(self):
		scoring, h_type = self.eval_selection()
		if h_type is None:
			return

		cards = self.__hand.cards
		played = [cards[i] for i in sorted(self.__selected_indexes)]
		held = [c for i, c in enumerate(cards) if i not in self.__selected_indexes]

		level = self.__game.hand_type_levels[h_type.name]
		ctx = ScoreContext(scoring, held, h_type, level, self.__game.jokers, on_event=self.__on_score_event)

		self.__hands -= 1
		self.__info_select_card = -1

		score = ScoringEngine.score_hand(ctx)

		self.__tally(score, ctx)

		self.__game.money += ctx.money

		for c in played:
			cards.remove(c)

		self.__selected_indexes.clear()

		self.__hand.fill_hand()
		self.__hand.sort_rank()

	def discard_selected(self):
		cards = self.__hand.cards
		for c in [cards[i] for i in sorted(self.__selected_indexes)]:
			cards.remove(c)
		self.__selected_indexes.clear()
		self.__info_select_card = -1
		self.__discards -= 1
		self.__hand.fill_hand()
		self.__hand.sort_rank()

	def __on_score_event(self, ctx : ScoreContext, event : ScoreEvent, ):
		self.display(ctx, event)
		sleep(STEP_TIME)

	def __tally(self, score : int, ctx : ScoreContext):
		start, steps = self.__round_score, 15
		for k in range(1, steps + 1):
			self.__round_score = start + round(score * k / steps)
			self.display(ctx)
			sleep(0.03)
		sleep(STEP_TIME)


	def eval_selection(self):

		cards = [self.__hand.cards[i] for i in self.__selected_indexes]

		scoring, h_type = [], None

		for hand_type in hand_types.HandType.__subclasses__():
			eval = hand_type.evaluate(cards)
			if eval != None:
				scoring = eval
				h_type = hand_type

		return scoring, h_type

blind = Blind()

game = Game()

round_1 = Round(game, blind)

round_1.start()

