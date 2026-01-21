from typing import Literal
from transformers import pipeline


# Load sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")


def update_emotion(judgment: str, regret: int, factual_accuracy: int = 5, emotional_impact: int = 5, response_text: str = "") -> Literal["angry", "sad", "happy", "neutral", "anxious", "confident"]:
    """Determine the current emotion based on judgment, regret, scores, and sentiment analysis of response."""
    # Use sentiment analysis if response_text is provided
    sentiment_score = 0.5  # Neutral default
    if response_text:
        try:
            result = sentiment_analyzer(response_text[:512])  # Limit length
            label = result[0]['label']
            if label == 'LABEL_2':  # Positive
                sentiment_score = 0.8
            elif label == 'LABEL_0':  # Negative
                sentiment_score = 0.2
            else:  # Neutral
                sentiment_score = 0.5
        except Exception:
            pass  # Fallback to logic
    
    # Combine with existing logic
    if judgment == "bad":
        if regret > 5 or sentiment_score < 0.4:
            return "angry"
        else:
            return "anxious"
    elif regret > 7:
        return "sad"
    elif regret < 3 and factual_accuracy > 7 and emotional_impact > 7 and sentiment_score > 0.6:
        return "confident"
    elif regret < 3 or sentiment_score > 0.6:
        return "happy"
    else:
        return "neutral"


def update_mood(avg_regret: float, mood_threshold: int = 5) -> int:
    """Calculate overall mood from average regret, with threshold."""
    if avg_regret > mood_threshold:
        return max(1, min(10, 11 - int(avg_regret)))
    else:
        return max(1, min(10, 6 + int(avg_regret)))
