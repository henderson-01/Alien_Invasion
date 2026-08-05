import json


def save_high_score(high_score):
    """Save the high score to a file."""
    with open('high_score.json', 'w') as f:
        json.dump(high_score, f)

def load_high_score():
    """Load the high score from a file."""
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
