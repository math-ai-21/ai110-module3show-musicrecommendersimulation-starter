"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "Road Trip": {
        "genre": "indie pop", "mood": "uplifting",
        "energy": 0.70, "acousticness": 0.30, "valence": 0.85,
    },
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy",
        "energy": 0.90, "acousticness": 0.10, "valence": 0.80,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill",
        "energy": 0.35, "acousticness": 0.80, "valence": 0.58,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense",
        "energy": 0.92, "acousticness": 0.08, "valence": 0.45,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
        print(f"\n{name}")
        print(f"User profile: {profile}")
        print("Recommendations:")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  {rank}. {song['title']} - Score: {score:.2f}")
            for reason in explanation.split("; "):
                print(f"       - {reason}")


if __name__ == "__main__":
    main()
