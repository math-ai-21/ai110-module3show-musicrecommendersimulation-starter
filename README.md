# 🎵 Music Recommender Simulation

> **Note:** This README and `model_card.md` do not account for the challenge changes (new song attributes: popularity, release decade, language, vocal type, mood tags, and their scoring in `src/recommender.py`).
> Everything below describes the project as it was before that extension.

## Project Summary
This is a small music recommender system that compares a listener's music taste profile (favorite genre and mood, target energy, and whether they like acoustic songs, plus an optional target valence) to 18 songs and gives each song a score from 0 to 1. Energy, acousticness and valence score higher the closer a song is to the target, and mood and genre score only when they match exactly, with energy weighted most heavily. The system returns the top five songs, each with reasons that show how much every feature added to its score. I tested it with four different profiles and ran one weight experiment, and I found that it works best for listeners whose favorite genre has several songs in the catalog.

---

## How The System Works
- Real-world recommenders like Spotify or YouTube mostly use two approaches. Collaborative filtering looks at what similar users listened to, skipped, or saved. Content-based filtering compares the specific attributes (such as genre, artist, etc) of the songs themselves to what a user already likes. The version I am building is content-based only, as it has no other
users and can't learn from anyone else's behavior. It prioritizes matching a song's energy first, then mood, then genre, because I believe those best show how people feel about the song. The tradeoff here is that such a system will mostly recommend songs that look like what the user already asked for, so it won't give them new types of songs in a way a real system may have.

- What features does each `Song` use in your system
  - Each song in my system uses energy, mood, genre, acousticness and valence. The variables id, title, and artist are just identifiers, not characteristics of a song. I left out tempo_bpm and danceability as they mostly repeat what energy already shows. 
- What information does your `UserProfile` store
  - UserProfile stores the user's favorite genre, favorite mood, target energy and whether they like acoustic songs, which is turned into a target acousticness of 0.8 (likes acoustic) or 0.2 (does not). Target valence is not stored in UserProfile, but the scorer uses it when a preferences dict includes it, as the sample profiles below do.

- How does your `Recommender` compute a score for each song
  - My `Recommender` class gives each song a score from 0 to 1 based on how well the song fits the user's profile. For every feature, it compares the song's value to the user's preference and works out a match score (1 = perfect match, 0 = no match). It multiplies each match score by that feature's weight, adds the results, and divides by the total weight of the features used, so the score always runs from 0 to 1.

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
1. The system takes in the user's taste profile, including favorite genre, favorite mood, target energy, target acousticness and (optionally) target valence.
2. Each song is compared against the user's preferences. For each feature a match score is calculated: `1 - |song - target|` for energy, acousticness and valence, and 1 or 0 for mood and genre.
3. Each match score is multiplied by its assigned weight (listed above) and they are all added up and divided by the total weight of the features used to get the song's score.
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

Road Trip
User profile: genre=indie pop, mood=uplifting, energy=0.7, acousticness=0.3, valence=0.85
Recommendations:
  1. Island Drift - Score: 0.74
       - energy 0.58 vs target 0.70 (+0.26)
       - acousticness 0.45 vs target 0.30 (+0.13)
       - valence 0.88 vs target 0.85 (+0.10)
       - mood match: uplifting (+0.25)
  2. Rooftop Lights - Score: 0.72
       - energy 0.76 vs target 0.70 (+0.28)
       - acousticness 0.35 vs target 0.30 (+0.14)
       - valence 0.81 vs target 0.85 (+0.10)
       - genre match: indie pop (+0.20)
  3. Sunrise City - Score: 0.49
       - energy 0.82 vs target 0.70 (+0.26)
       - acousticness 0.18 vs target 0.30 (+0.13)
       - valence 0.84 vs target 0.85 (+0.10)
  4. Night Drive Loop - Score: 0.49
       - energy 0.75 vs target 0.70 (+0.28)
       - acousticness 0.22 vs target 0.30 (+0.14)
       - valence 0.49 vs target 0.85 (+0.06)
  5. Concrete Crown - Score: 0.48
       - energy 0.78 vs target 0.70 (+0.28)
       - acousticness 0.12 vs target 0.30 (+0.12)
       - valence 0.62 vs target 0.85 (+0.08)
```

```
High-Energy Pop
User profile: genre=pop, mood=happy, energy=0.9, acousticness=0.1, valence=0.8
Recommendations:
  1. Sunrise City - Score: 0.96
       - energy 0.82 vs target 0.90 (+0.28)
       - acousticness 0.18 vs target 0.10 (+0.14)
       - valence 0.84 vs target 0.80 (+0.10)
       - mood match: happy (+0.25)
       - genre match: pop (+0.20)
  2. Gym Hero - Score: 0.73
       - energy 0.93 vs target 0.90 (+0.29)
       - acousticness 0.05 vs target 0.10 (+0.14)
       - valence 0.77 vs target 0.80 (+0.10)
       - genre match: pop (+0.20)
  3. Rooftop Lights - Score: 0.72
       - energy 0.76 vs target 0.90 (+0.26)
       - acousticness 0.35 vs target 0.10 (+0.11)
       - valence 0.81 vs target 0.80 (+0.10)
       - mood match: happy (+0.25)
  4. Neon Overdrive - Score: 0.52
       - energy 0.96 vs target 0.90 (+0.28)
       - acousticness 0.03 vs target 0.10 (+0.14)
       - valence 0.80 vs target 0.80 (+0.10)
  5. Storm Runner - Score: 0.52
       - energy 0.91 vs target 0.90 (+0.30)
       - acousticness 0.10 vs target 0.10 (+0.15)
       - valence 0.48 vs target 0.80 (+0.07)
```

```
Chill Lofi
User profile: genre=lofi, mood=chill, energy=0.35, acousticness=0.8, valence=0.58
Recommendations:
  1. Library Rain - Score: 0.99
       - energy 0.35 vs target 0.35 (+0.30)
       - acousticness 0.86 vs target 0.80 (+0.14)
       - valence 0.60 vs target 0.58 (+0.10)
       - mood match: chill (+0.25)
       - genre match: lofi (+0.20)
  2. Midnight Coding - Score: 0.96
       - energy 0.42 vs target 0.35 (+0.28)
       - acousticness 0.71 vs target 0.80 (+0.14)
       - valence 0.56 vs target 0.58 (+0.10)
       - mood match: chill (+0.25)
       - genre match: lofi (+0.20)
  3. Spacewalk Thoughts - Score: 0.75
       - energy 0.28 vs target 0.35 (+0.28)
       - acousticness 0.92 vs target 0.80 (+0.13)
       - valence 0.65 vs target 0.58 (+0.09)
       - mood match: chill (+0.25)
  4. Focus Flow - Score: 0.73
       - energy 0.40 vs target 0.35 (+0.28)
       - acousticness 0.78 vs target 0.80 (+0.15)
       - valence 0.59 vs target 0.58 (+0.10)
       - genre match: lofi (+0.20)
  5. Coffee Shop Stories - Score: 0.52
       - energy 0.37 vs target 0.35 (+0.29)
       - acousticness 0.89 vs target 0.80 (+0.14)
       - valence 0.71 vs target 0.58 (+0.09)
```

```
Deep Intense Rock
User profile: genre=rock, mood=intense, energy=0.92, acousticness=0.08, valence=0.45
Recommendations:
  1. Storm Runner - Score: 0.99
       - energy 0.91 vs target 0.92 (+0.30)
       - acousticness 0.10 vs target 0.08 (+0.15)
       - valence 0.48 vs target 0.45 (+0.10)
       - mood match: intense (+0.25)
       - genre match: rock (+0.20)
  2. Gym Hero - Score: 0.76
       - energy 0.93 vs target 0.92 (+0.30)
       - acousticness 0.05 vs target 0.08 (+0.15)
       - valence 0.77 vs target 0.45 (+0.07)
       - mood match: intense (+0.25)
  3. Iron Requiem - Score: 0.51
       - energy 0.97 vs target 0.92 (+0.29)
       - acousticness 0.06 vs target 0.08 (+0.15)
       - valence 0.25 vs target 0.45 (+0.08)
  4. Neon Overdrive - Score: 0.50
       - energy 0.96 vs target 0.92 (+0.29)
       - acousticness 0.03 vs target 0.08 (+0.14)
       - valence 0.80 vs target 0.45 (+0.06)
  5. Concrete Crown - Score: 0.48
       - energy 0.78 vs target 0.92 (+0.26)
       - acousticness 0.12 vs target 0.08 (+0.14)
       - valence 0.62 vs target 0.45 (+0.08)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Weight shift: Energy's weight was doubled (0.30 to 0.60) and genre's weight was halved (0.20 to 0.10). The top song stayed the same for all four profiles, but the middle of the list changed for two of them. For High-Energy Pop, Rooftop Lights moved above Gym Hero, and for Road Trip, Night Drive Loop moved above Sunrise City by a small margin (0.64 vs. 0.63). Weaker matches also scored higher, for example Coffee Shop Stories went from 0.52 to 0.68. The results were different but not better, so the original weights were kept. The experiment is saved as commented-out lines in `src/recommender.py`.

---

## Limitations and Risks

The catalog has only 18 songs, and most genres appear just once. Since a song only gets genre credit when the genre matches exactly, if a listener's favorite genre has more songs, like lofi, then they get better recommendations than listeners of a less common genre like jazz. See the model_card.md for more details.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender made me see how songs can be matched to a listener’s preferences using numbers and labels, even though the system does not actually understand the music. When I tried changing the weights, the top song stayed the same for all four profiles, but some of the other recommendations changed places. I also noticed how the small catalog affected the results, since it has only 18 songs and most genres appear just once. A lofi listener had several good matches to choose from, while a jazz listener got one strong match followed by weaker ones, which showed how the available songs could favor some listeners’ tastes over others.
