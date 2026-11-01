# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
- Real-world recommenders like Spotify or YouTube mostly use two approaches. Collaborative filtering looks at what similar users listened to, skipped, or saved. Content-based filtering compares the specific attributes (such as genre, artist, etc) of the songs themselves to what a user already likes. The version I am building is content-based only, as it has no other
users and can't learn from anyone else's behavior. It first prioritizes matching a song's energy first, then mood, then genre, because I believe those best show how people feel about the song. The tradeoff here is that such a system will mostly recommend songs that look like what the user already asked for, so it won't give them new types of songs in a way a real system may have.

- What features does each `Song` use in your system
  - Each song in my system uses energy, mood, genre, acousticness and valence. The variables id, title, and artist are just identifiers, not characteristics of a song. I left out tempo_bpm and danceability as they mostly repeat what energy already shows. 
- What information does your `UserProfile` store
  - UserProfile stores the user's favorite genre, favorite mood, target energy, target acousticness and target valence.

- How does your `Recommender` compute a score for each song
  - My recommender gives each song a score from 0 to 1 based on how well the song fits the user's profile. For every feature, it compares the song's value to the user's preference and works out a match score (1 = perfect match, 0 = no match). It multiplies each match score by that feature's weight and adds the results.

- How each match score is calculated:
  - Energy, acousticness, and valence use a linear closeness score: `1 - |song - target|`. The target is the value stored in the user's profile, so the closer a song's value is to what the user wants, the higher it scores. For example, if the user's target energy is 0.80, a song with energy 0.82 scores 0.98 and a song with energy 0.42 scores 0.62.
  - Mood and genre use an exact match where the score is 1 if the song's value is the same as the user's favorite, otherwise it is 0.

  The weights are:
  - energy: 0.30
  - mood: 0.25
  - genre: 0.20
  - acousticness: 0.15
  - valence: 0.10

  These weights are my own judgment, and not from the data. I chose energy to be the highest because it separates calm songs from intense ones best and also reflects tempo and danceability. Mood is second because it decides whether a song fits the moment. Genre is lower because most genres appear only once in the catalog. Acousticness adds a little beyond energy, and valence is lowest because it varies the least.

- How do you choose which songs to recommend
  - The ranking rule scores every song in the catalog, sorts them from highest to lowest score, and returns the top 5.

Algorithm Recipe:
1. The system takes in the user's taste profile, including favorite genre, favorite mood, target energy, target acousticness, target valence.
2. Each song is compared against the user's prefernces. For each feature a match score is calculated: `1 - |song - target|` for energy, acousticness and valence, and 1 or 0 for mood and genre.
3. Each match score is multiplied by its assigned weight (listed above) and they are all added up to get the song's score.
4. The songs are sorted from highest to lowest score and the top 5 recommendations are returned.

Expected biases:
- The system mainly recommends songs similar to the stated profile, so it may not introduce much new music which the user could like.
- This system might over-prioritize mood and genre, which together are worth 0.45. This could cause songs with near-perfect energy match but different mood or genre label to be ranked lower.
- The system only gives points when a song's genre or mood exactly matches the user's preferences. Similar labels, such as "chill" and "relaxed," receive no points even though they have similar meanings.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loading songs from data/songs.csv...
Loaded songs: 18

User profile: genre=pop, mood=happy, energy=0.8
Recommendations:
  1. Sunrise City - Score: 0.99
       - energy 0.82 vs target 0.80 (+0.39)
       - mood match: happy (+0.33)
       - genre match: pop (+0.27)
  2. Rooftop Lights - Score: 0.72
       - energy 0.76 vs target 0.80 (+0.38)
       - mood match: happy (+0.33)
  3. Gym Hero - Score: 0.61
       - energy 0.93 vs target 0.80 (+0.35)
       - genre match: pop (+0.27)
  4. Concrete Crown - Score: 0.39
       - energy 0.78 vs target 0.80 (+0.39)
  5. Night Drive Loop - Score: 0.38
       - energy 0.75 vs target 0.80 (+0.38)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



