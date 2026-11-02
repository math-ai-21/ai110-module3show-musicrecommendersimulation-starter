from pathlib import Path

from src.recommender import Song, UserProfile, Recommender

SONGS_CSV = Path(__file__).resolve().parent.parent / "data" / "songs.csv"


def make_songs():
    return [
        {
            "id": 1, "title": "Test Pop Track", "artist": "Test Artist",
            "genre": "pop", "mood": "happy", "energy": 0.8, "tempo_bpm": 120,
            "valence": 0.9, "danceability": 0.8, "acousticness": 0.2,
            "popularity": 80, "release_decade": 2020, "language": "english",
            "vocal_type": "vocals", "mood_tags": ["euphoric", "hopeful"],
        },
        {
            "id": 2, "title": "Chill Lofi Loop", "artist": "Test Artist",
            "genre": "lofi", "mood": "chill", "energy": 0.4, "tempo_bpm": 80,
            "valence": 0.6, "danceability": 0.5, "acousticness": 0.9,
            "popularity": 40, "release_decade": 2010, "language": "none",
            "vocal_type": "instrumental", "mood_tags": ["dreamy"],
        },
    ]


def test_load_songs_converts_types():
    songs = Recommender.load_songs(str(SONGS_CSV))
    assert songs
    first = songs[0]
    assert isinstance(first["id"], int)
    assert isinstance(first["energy"], float)
    assert isinstance(first["popularity"], int)
    assert isinstance(first["mood_tags"], list)


def test_score_song_perfect_match_scores_one():
    pop = make_songs()[0]
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = Recommender.score_song(prefs, pop)
    assert score == 1.0
    assert reasons


def test_score_song_is_between_zero_and_one():
    lofi = make_songs()[1]
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.9, "acousticness": 0.0}
    score, _ = Recommender.score_song(prefs, lofi)
    assert 0.0 <= score < 1.0


def test_score_song_empty_prefs_returns_zero():
    assert Recommender.score_song({}, make_songs()[0]) == (0.0, [])


def test_score_song_mood_tags_share_of_wanted_tags():
    pop = make_songs()[0]
    score, reasons = Recommender.score_song({"mood_tags": ["euphoric", "dark"]}, pop)
    assert score == 0.5
    assert "euphoric" in reasons[0]


def test_score_song_decade_and_popularity_closeness():
    pop = make_songs()[0]
    score, _ = Recommender.score_song({"popularity": 80, "release_decade": 2020}, pop)
    assert score == 1.0
    far, _ = Recommender.score_song({"popularity": 0, "release_decade": 1970}, pop)
    assert far < score


def test_recommend_returns_sorted_by_score():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    results = Recommender.recommend(prefs, make_songs(), k=2)

    assert len(results) == 2
    assert results[0][0]["genre"] == "pop"
    assert results[0][1] > results[1][1]


def test_recommend_respects_k():
    prefs = {"genre": "pop", "energy": 0.8}
    assert len(Recommender.recommend(prefs, make_songs(), k=1)) == 1


def test_recommend_explanation_is_non_empty_string():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    _, _, explanation = Recommender.recommend(prefs, make_songs(), k=1)[0]
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def make_small_recommender() -> Recommender:
    songs = [
        Song(id=1, title="Test Pop Track", artist="Test Artist", genre="pop",
             mood="happy", energy=0.8, tempo_bpm=120, valence=0.9,
             danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist", genre="lofi",
             mood="chill", energy=0.4, tempo_bpm=80, valence=0.6,
             danceability=0.5, acousticness=0.9),
    ]
    return Recommender(songs)


def make_user() -> UserProfile:
    return UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False)


def test_song_optional_fields_have_defaults():
    song = make_small_recommender().songs[0]
    assert song.popularity == 0
    assert song.mood_tags == ()
    assert song.to_dict()["title"] == "Test Pop Track"


def test_user_profile_to_prefs():
    prefs = make_user().to_prefs()
    assert prefs == {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    assert UserProfile("pop", "happy", 0.8, True).to_prefs()["acousticness"] == 0.8


def test_explain_recommendation_returns_non_empty_string():
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(make_user(), rec.songs[0])
    assert isinstance(explanation, str)
    assert "genre match: pop" in explanation
