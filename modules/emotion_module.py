from typing import Literal

def update_emotion(judgment: str, regret: int) -> Literal["angry", "sad", "happy", "neutral"]:
	"""Determine the current emotion based on judgment and regret."""
	if judgment == "bad":
		return "angry"
	elif regret > 7:
		return "sad"
	elif regret < 3:
		return "happy"
	else:
		return "neutral"

def update_mood(avg_regret: float) -> int:
	"""Calculate overall mood from average regret."""
	return max(1, min(10, 11 - int(avg_regret)))