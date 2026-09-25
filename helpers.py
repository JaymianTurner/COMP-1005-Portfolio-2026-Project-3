from collections import defaultdict
from card import Card

def group_by_rank(cards : list[Card]):

	# Put every card into a list keyed by its rank.

	# defaultdict(list) means that there is no need to check
	# if the rank is already a key before appending,
	# as it creates an empty list the first time a new rank appears.
	by_rank = defaultdict(list)

	for card in cards:
		by_rank[card.rank].append(card)

	# Drop the dict keys as they are not important.
	groups = list(by_rank.values())

	# Sort groups by two keys, being length, and rank
	# The groups of highest length should be put first, though if
	# two ranks are the same length, as occours in a Two Pair,
	# the higher value rank is put first.
	groups.sort(key=lambda g: (len(g), g[0].rank), reverse=True)

	return groups


def is_straight(cards : list[Card], run_length : int = 5):
	# Filter list to only distinct ranks, as a straight does not care if there are repeated ranks.
	# e.g. A straight affected by four fingers (run length of 4) would value the hands
	# 5, 5, 4, 3, 2 and 8, 5, 4, 3, 2 the same.
	distinct_ranks = sorted({c.rank for c in cards})

	# If the length of distinct ranks is smaller than run length,
	# then the hand can not possibly be a Straight...
	if len(distinct_ranks) < run_length:
		# ...therefore the method bails out.
		return None

	# If an Ace is within the hand...
	if 14 in distinct_ranks:
		# In Balatro, an ace can count as both a high (14) or low (1).
		# the best solution I can figure out for this is to simply append a "ghost" card of rank 1.
		distinct_ranks = sorted(set(distinct_ranks) | {1})

	for start in distinct_ranks:
		run = list(range(start, start + run_length))
		if all(r in distinct_ranks for r in run):
			wanted = set(run)

			if 1 in wanted:
				wanted.add(14)
				wanted.discard(1)

			return _pick_one_per_rank(cards, wanted)

	return None


def _pick_one_per_rank(cards, ranks):
	picked = []

	remaining = set(ranks)

	for card in cards:
		if card.rank in remaining:
			picked.append(card)
			remaining.discard(card.rank)
	return picked
