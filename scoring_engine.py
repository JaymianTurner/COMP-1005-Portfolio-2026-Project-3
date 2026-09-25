from score_context import ScoreContext

class ScoringEngine:
	@staticmethod
	def score_hand(context : ScoreContext) -> int:

		# Loop through all scoring cards in hand dealt from left -> right.
		for card in context.hand.scoring_cards:

			# Loop through all jokers to find if any activate retriggers for selected card.
			# e.g. Hanging Chad retriggers first card 2 times.
			triggers = 1 + sum(j.retriggers(context, card) for j in context.jokers)

			# Score card for amount of triggers.
			for _ in range(triggers):
				# Add base card chips.
				context.add_chips(card.base_chips)

				# Loop through modifiers that card has. 
				# (enhancement -> edition -> seal)
				for m in card.modifiers():
					# TODO: Figure out elegant implementation for red seals.
					# Also, try and figure out how planet/tarot cards can be created.
					m.on_card_scored(context, card)

				# Loop through all jokers to check if they trigger from
				# this card being scored (left -> right).
				for j in context.jokers:
					j.on_card_scored(context, card)

		for card in context.hand.held_cards:
			for m in card.modifiers():
				m.on_card_held(context, card)
			for j in context.jokers:
				j.on_card_held(context, card)

		for j in context.jokers:
			j.on_hand_scored(context)

		return context.chips * context.mult
				