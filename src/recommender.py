import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

NUMERIC_WEIGHTS = {"energy": 0.30, "acousticness": 0.15, "valence": 0.10}
CATEGORY_WEIGHTS = {"mood": 0.25, "genre": 0.20, "language": 0.05, "vocal_type": 0.05}

# Extra features, only scored when the user profile includes them.
# popularity: closeness on a 0-100 scale; release_decade: closeness that drops to 0
# at DECADE_SPAN years apart; mood_tags: share of the user's tags the song has.
POPULARITY_WEIGHT = 0.05
DECADE_WEIGHT = 0.05
MOOD_TAGS_WEIGHT = 0.15
DECADE_SPAN = 50

# Experiment (not used): double energy (0.30 -> 0.60) and halve genre (0.20 -> 0.10).
# The weights add up to 1.20, which is fine because score_song divides by the
# weights it used. The top song stayed the same for all 4 profiles, but High-Energy
# Pop and Road Trip each moved a weaker fit above a stronger one, so I kept the
# original weights above.
# NUMERIC_WEIGHTS = {"energy": 0.60, "acousticness": 0.15, "valence": 0.10}
# CATEGORY_WEIGHTS = {"mood": 0.25, "genre": 0.10}

@dataclass
class Song:
    """A song and its attributes."""
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
    popularity: int = 0
    release_decade: int = 0
    language: str = ""
    vocal_type: str = ""
    mood_tags: Tuple[str, ...] = ()

    def to_dict(self) -> Dict:
        """Return the song as the dict that score_song expects."""
        return asdict(self)


@dataclass
class UserProfile:
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

    def to_prefs(self) -> Dict:
        """Return the preferences as the dict that score_song expects.

        likes_acoustic is turned into an acousticness target: 0.8 if True, 0.2 if False.
        """
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "acousticness": 0.8 if self.likes_acoustic else 0.2,
        }


class Recommender:
    """Loads songs, scores them against user preferences, and ranks recommendations."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def load_songs(csv_path: str) -> List[Dict]:
        """Load songs from a CSV file as dicts, converting numeric columns to int/float."""
        print(f"Loading songs from {csv_path}...")
        songs = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])
                for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                    row[field] = float(row[field])
                # Newer columns are optional so older CSVs without them still load.
                if "popularity" in row:
                    row["popularity"] = int(row["popularity"])
                    row["release_decade"] = int(row["release_decade"])
                    row["mood_tags"] = [t for t in row["mood_tags"].split("|") if t]
                songs.append(row)
        print(f"Loaded songs: " + str(len(songs)))
        return songs

    @staticmethod
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

        if "popularity" in user_prefs:
            match = 1 - abs(song["popularity"] - user_prefs["popularity"]) / 100
            weight_used += POPULARITY_WEIGHT
            contributions.append((
                f"popularity {song['popularity']} vs target {user_prefs['popularity']}",
                POPULARITY_WEIGHT * match,
            ))

        if "release_decade" in user_prefs:
            gap = abs(song["release_decade"] - user_prefs["release_decade"])
            match = max(0.0, 1 - gap / DECADE_SPAN)
            weight_used += DECADE_WEIGHT
            contributions.append((
                f"decade {song['release_decade']}s vs target {user_prefs['release_decade']}s",
                DECADE_WEIGHT * match,
            ))

        if user_prefs.get("mood_tags"):
            wanted = set(user_prefs["mood_tags"])
            shared = sorted(wanted & set(song["mood_tags"]))
            weight_used += MOOD_TAGS_WEIGHT
            if shared:
                contributions.append((
                    f"mood tags match: {', '.join(shared)}",
                    MOOD_TAGS_WEIGHT * len(shared) / len(wanted),
                ))

        # Profiles that leave out a feature are scored out of the weights they use,
        # so the score still runs from 0 to 1 and the reasons add up to it.
        if not weight_used:
            return 0.0, []
        score = sum(points for _, points in contributions) / weight_used
        reasons = [f"{text} (+{points / weight_used:.2f})" for text, points in contributions]
        return score, reasons

    @classmethod
    def recommend(cls, user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
        """Return the top k songs as (song, score, explanation), highest score first."""
        scored = ((song, *cls.score_song(user_prefs, song)) for song in songs)
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
        return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song scores the way it does for the user."""
        score, reasons = self.score_song(user.to_prefs(), song.to_dict())
        if not reasons:
            return f"No features matched (score {score:.2f})"
        return f"Score {score:.2f}: " + "; ".join(reasons)
