extends RefCounted

var cards: Array = []

func setup(card_ids: Array) -> void:
	cards = card_ids.duplicate()
	cards.shuffle()

func draw():
	if cards.is_empty():
		return null
	return cards.pop_front()

func draw_many(count: int) -> Array:
	var drawn: Array = []
	for i in range(count):
		var card = draw()
		if card == null:
			break
		drawn.append(card)
	return drawn
