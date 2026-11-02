# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

- The recommender gives each song a score based on how well it matches with the user's profile. The score goes from 0 to 1, with 1 being the best match. It considers five things: the energy, mood, genre, acousticness, and the valence. For energy, acousticness, and valence (how positive a song sounds), the closer a song is to what the user prefers, the more points it gets, and it loses points at a steady rate the further away it is. For example, if someone likes fairly energetic songs, a song with a similar energy level gets more points. Songs that are equally far above or below their preferred energy level get the same points. 
- For mood and genre, a song gets points if it matches the user’s choice and no points for that part if it doesn’t. Some parts matter more than others. Energy makes up 30% of the score, mood 25%, genre 20%, acousticness 15%, and valence 10%. These percentages were chosen by hand, with energy given the most weight because it is one of the main parts of how a song feels. If a user's profile doesn't include a feature, the model ignores that feature and scales the remaining percentages up so the score is still in the range 0 to 1. The recommender adds up the points and shows the five songs with the highest scores. It also shows how much each matching part contributed, so the user can understand why each song was recommended. The starter code did not have a way to score or rank songs, so that logic was added for this project.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
