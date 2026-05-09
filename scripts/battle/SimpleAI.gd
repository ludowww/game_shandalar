extends RefCounted

func choose_card_index(combatant) -> int:
	if combatant.hand.is_empty():
		return -1
	return 0
