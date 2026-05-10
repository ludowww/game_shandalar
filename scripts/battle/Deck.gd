extends RefCounted

const ZONE_LIBRARY := "Bibliothèque"
const ZONE_GRAVEYARD := "Cimetière"

# T017: this pile is still named Deck for compatibility with existing data,
# but in duel rules it represents the Magic library. The discard buffer is
# the recycle source used by the prototype before a full cemetery model exists.
var cards: Array = []
var discard_pile: Array = []

func setup(card_ids: Array) -> void:
	cards = card_ids.duplicate()
	discard_pile = []
	cards.shuffle()

func draw():
	if cards.is_empty():
		reshuffle_discard_into_deck()
	if cards.is_empty():
		return null
	return cards.pop_front()

func discard(card_id: String) -> void:
	if card_id != "":
		discard_pile.append(card_id)

func reshuffle_discard_into_deck() -> void:
	if discard_pile.is_empty():
		return
	cards = discard_pile.duplicate()
	discard_pile = []
	cards.shuffle()

func draw_many(count: int) -> Array:
	var drawn: Array = []
	for i in range(count):
		var card = draw()
		if card == null:
			break
		drawn.append(card)
	return drawn

func library_size() -> int:
	return cards.size()

func graveyard_buffer_size() -> int:
	return discard_pile.size()
