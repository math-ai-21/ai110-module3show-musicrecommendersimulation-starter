# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
**TuneMatcher 1.0**  

---

## 2. Intended Use  

This recommender suggests up to five songs from a small catalog that best fit a listener's taste profile. The profile gives a favorite genre and mood, plus target levels for energy, acousticness and valence, and the system ranks the songs by how closely they match, with a short list of reasons for each one. It assumes that the listener knows what they want and can describe it in those terms, and that the genre and mood labels in the catalog mean the same thing to them as they do to the system. It is more of a classroom exploration of how recommenders turn data into suggestions, not a complete system for real listeners, since the catalog has only 18 songs and the scoring has not been tested with actual listeners. With a bigger catalog, profiles that listeners can create themselves, and a user interface, it could become a full recommender.

---

## 3. How the Model Works  

- The recommender gives each song a score based on how well it matches with the user's profile. The score goes from 0 to 1, with 1 being the best match. It considers five things: the energy, mood, genre, acousticness, and the valence. For energy, acousticness, and valence (how positive a song sounds), the closer a song is to what the user prefers, the more points it gets, and it loses points at a steady rate the further away it is. For example, if someone likes fairly energetic songs, a song with a similar energy level gets more points. Songs that are equally far above or below their preferred energy level get the same points. 
- For mood and genre, a song gets points if it matches the user’s choice and no points for that part if it doesn’t. Some parts matter more than others. Energy makes up 30% of the score, mood 25%, genre 20%, acousticness 15%, and valence 10%. These percentages were chosen by hand, with energy given the most weight because it is one of the main parts of how a song feels. If a user's profile doesn't include a feature, the model ignores that feature and scales the remaining percentages up so the score is still in the range 0 to 1. The recommender adds up the points and shows the five songs with the highest scores. It also shows how much each matching part contributed, so the user can understand why each song was recommended. The starter code did not have a way to score or rank songs, so that logic was added for this project.
---

## 4. Data  
The catalog has 18 songs in data/songs.csv. Each song has a title, artist, genre, mood and five numbers (energy, tempo, valence, danceability and acousticness). The songs cover 15 genres and 14 moods, but most appear only once. Only lofi (3 songs) and pop (2 songs) have more than one, and only chill, happy and intense appear for more than one song. The starter file had 10 songs, and 8 more were added to bring in genres and moods that were missing, such as hip hop, classical, country, r&b, EDM, reggae, metal and folk. None of the songs were removed. Many parts of musical taste are still missing: there are no lyrics, languages, release years or popularity, and the energy values skip the range 0.58 to 0.75, so listeners who want medium-high energy have few options.

---

## 5. Strengths  

The system works best for listeners with one consistent taste, especially in a genre with several songs in the catalog. For the Chill Lofi profile, Library Rain (0.99) and Midnight Coding (0.96) were strong matches. The scoring also separates listeners well: Chill Lofi shares no songs with the other profiles, and High-Energy Pop and Deep Intense Rock both want energy around 0.9 but get different top songs (Sunrise City vs. Storm Runner) because of their genre, mood and valence. The results matched what is expected: Deep Intense Rock gets loud, dark songs like Storm Runner and Iron Requiem, and Chill Lofi gets quiet, acoustic ones like Library Rain. Also, every recommendation lists the reasons behind its score, so it is easy to see why a song was chosen.
---

## 6. Limitations and Bias

The system gives better recommendations to listeners whose favorite genres have more songs in the catalog. The catalog has only 18 songs, and most genres appear just once. Since a song only gets credit for genre if it matches exactly, some listeners have fewer good options.

For example, a jazz profile (jazz, relaxed, energy 0.38, acousticness 0.8, valence 0.6) gets one strong match, Coffee Shop Stories, with a score of 0.97, and the rest of its top five score only around 0.5. Those songs are mostly lofi and country songs with similar energy and acousticness, because there are no other jazz songs in the catalog. A lofi profile with the same numbers (lofi, chill) gets two matches near 0.97 and two more around 0.75.

This means the system might favor listeners whose favorite genres are more common in the catalog.

---

## 7. Evaluation

Four profiles were tested: Road Trip (indie pop, uplifting, energy 0.70), High-Energy Pop (pop, happy, energy 0.90), Chill Lofi (lofi, chill, energy 0.35), and Deep Intense Rock (rock, intense, energy 0.92). For each profile, the top five songs were checked for whether they fit its preferences and whether the reasons given added up to the score.

Each of the four profiles asked for a different kind of music, and the five songs recommended for each one fit what it asked for. Chill Lofi shares no songs with any of the other three profiles, which makes sense because its low energy (0.35) and high acousticness (0.8) are very different from the rest, and it gets more quiet songs like Library Rain. The other three profiles all want fairly high energy, so their lists overlap a little: Road Trip and High-Energy Pop both include Sunrise City and Rooftop Lights, High-Energy Pop and Deep Intense Rock share Gym Hero, Neon Overdrive and Storm Runner, and Road Trip and Deep Intense Rock share only Concrete Crown. What distinguishes these three is their labels and valence. High-Energy Pop's pop genre and happy mood put Sunrise City first, Road Trip's high valence (0.85) gives it brighter songs like Island Drift, and Deep Intense Rock's low valence (0.45) gives it darker songs like Storm Runner and Iron Requiem.

It was surprising how closely some songs matched in a small catalog. Library Rain scored 0.99 for Chill Lofi, and Storm Runner scored 0.99 for Deep Intense Rock. Each matched the requested genre and mood, and was close to the preferred values for all three number-based features.

Gym Hero kept showing up for the High-Energy Pop profile even though its mood is “intense” and not “happy." A mood that does not match means a song misses a bonus, and nothing is taken away, so Gym Hero still ranks high. It also appears for Deep Intense Rock, where its intense mood and high energy count in its favor, so one song can look like a good fit for two very different listeners.

One experiment changed how much energy and genre mattered in the score. Energy’s weight was doubled from 0.30 to 0.60 and genre’s weight was halved from 0.20 to 0.10. The top song stayed the same for all four profiles, but some songs in the middle changed places for two profiles.

In the experiment, for High-Energy Pop, Rooftop Lights (energy 0.76) moved above Gym Hero (energy 0.93). For Road Trip, Night Drive Loop moved above Sunrise City by a small margin (0.64 compared to 0.63). In both cases, the song that moved up seemed like a weaker fit for the profile. Some weaker matches also received higher scores. For example, Coffee Shop Stories went from 0.52 to 0.68.
The changes made the recommendations different, but they did not seem better, so the original weights were kept.

---

## 8. Future Work  

Future versions could let listeners create their own profiles and use sliders to choose their preferred energy, acousticness, and valence. Features like tempo and danceability could also help with recommendations, along with lyrics and artists. Another improvement would be to give some credit to related moods or genres, such as “chill” and “relaxed,” instead of requiring an exact match. Scores could also drop differently as a song gets further from the listener’s preferences, rather than always decreasing at a steady rate. Clearer explanations would make the recommendations easier to understand, and avoiding songs that are too similar would give the top five more variety. Adding more songs to each genre would give listeners more choices, especially those whose favorite genres currently have very few songs.

---

## 9. Personal Reflection  
Through this project, I learned how a recommender system can compare songs with a listener’s preferences and use scores to decide which songs to suggest. Something I found interesting was how well some songs matched the profiles, even with such a small catalog. It also made me think more about the recommendations I see on YouTube or Spotify. I usually listen without thinking much about why a particular song was suggested, but building this system helped me understand how song features and listening preferences can help create recommendations.