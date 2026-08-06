import json

FILENAME = 'high_score.json'

def save_high_score(score, username="default"):
    """Save the high score for a specific user."""
    scores = load_all_scores()
    # Only update if the new score is higher than the existing high score for that user
    if username not in scores or score > scores[username]:
        scores[username] = score
        with open(FILENAME, 'w') as f:
            json.dump(scores, f)

def load_all_scores():
    """Load all high scores from the file."""
    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                # Handle the case where it's just a single number (old format)
                return {"default": data}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_high_score():
    """Load the global top score from the file."""
    scores = load_all_scores()
    return max(scores.values(), default=0)

def load_user_high_score(username):
    """Load a specific user's high score, or 0 if they have none."""
    return load_all_scores().get(username, 0)
