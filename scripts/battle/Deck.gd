extends RefCounted

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
