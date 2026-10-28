from score_context import ScoreContext
from card import Card

class ScoringEngine:
	@staticmethod
	def score_hand(ctx : ScoreContext) -> int:

		ctx.source = None
		ctx.emit("hand")

		for card in ctx.scoring_cards:
			ScoringEngine.__trigger(ctx, card, ScoringEngine.__score_card, "retriggers")

		for card in ctx.held_cards:
			ScoringEngine.__trigger(ctx, card, ScoringEngine.__hold_card, "held_retriggers")

		for j in ctx.jokers:
			ctx.source = j
			j.on_hand_scored(ctx)

		ctx.source = None
		return int(ctx.chips * ctx.mult)

		

	@staticmethod
	def __trigger(ctx, card, effect, retrigger_method : str):
		retriggers = []
		for m in card.modifiers():
			retriggers += [card] * getattr(m, retrigger_method)(ctx, card)
		for j in ctx.jokers:
			retriggers += [j] * getattr(j, retrigger_method)(ctx, card)

		effect(ctx, card)
		for i in retriggers:
			ctx.source = i
			ctx.emit("retrigger")
			effect(ctx, card)

	@staticmethod
	def __score_card(ctx : ScoreContext, card : Card):

		ctx.source = card
		ctx.add_chips(card.base_chips)

		for m in card.modifiers():
			ctx.source = card
			m.on_card_scored(ctx, card)

		for j in ctx.jokers:
			ctx.source = j
			j.on_card_scored(ctx, card)

	@staticmethod
	def __hold_card(ctx : ScoreContext, card):
		for m in card.modifiers():
			ctx.source = card
			m.on_card_held(ctx, card)
		for j in ctx.jokers:
			ctx.source = j
			j.on_card_held(ctx, card)