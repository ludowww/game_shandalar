extends RefCounted

func choose_card_index(combatant, card_database: Dictionary = {}) -> int:
	if combatant.hand.is_empty():
		return -1
	for i in range(combatant.hand.size()):
		var card_id: String = combatant.hand[i]
		var card: Dictionary = card_database.get(card_id, {})
		if card.is_empty():
			continue
		if combatant.can_play_card(card):
			return i
	return -1
