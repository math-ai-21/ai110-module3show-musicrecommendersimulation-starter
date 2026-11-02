import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file as dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: " + str(len(songs)))
    return songs

NUMERIC_WEIGHTS = {"energy": 0.30, "acousticness": 0.15, "valence": 0.10}
CATEGORY_WEIGHTS = {"mood": 0.25, "genre": 0.20}

# Experiment (not used): double energy (0.30 -> 0.60) and halve genre (0.20 -> 0.10).
# The weights add up to 1.20, which is fine because score_song divides by the
# weights it used. The top song stayed the same for all 4 profiles, but High-Energy
# Pop and Road Trip each moved a weaker fit above a stronger one, so I kept the
# original weights above.
# NUMERIC_WEIGHTS = {"energy": 0.60, "acousticness": 0.15, "valence": 0.10}
# CATEGORY_WEIGHTS = {"mood": 0.25, "genre": 0.10}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song from 0 to 1 against user preferences and return (score, reasons)."""
    weight_used = 0.0
    contributions = []  # (explanation, points toward the score)

    for feature, weight in NUMERIC_WEIGHTS.items():
        if feature not in user_prefs:
            continue
        match = 1 - abs(song[feature] - user_prefs[feature])
        weight_used += weight
        contributions.append((
            f"{feature} {song[feature]:.2f} vs target {user_prefs[feature]:.2f}",
            weight * match,
        ))

    for feature, weight in CATEGORY_WEIGHTS.items():
        if feature not in user_prefs:
            continue
        weight_used += weight
        if song[feature] == user_prefs[feature]:
            contributions.append((f"{feature} match: {song[feature]}", weight))

    # Profiles that leave out a feature are scored out of the weights they use,
    # so the score still runs from 0 to 1 and the reasons add up to it.
    if not weight_used:
        return 0.0, []
    score = sum(points for _, points in contributions) / weight_used
    reasons = [f"{text} (+{points / weight_used:.2f})" for text, points in contributions]
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation), highest score first."""
    scored = ((song, *score_song(user_prefs, song)) for song in songs)
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]
