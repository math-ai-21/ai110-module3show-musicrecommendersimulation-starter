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

My recommender gives each song a score based on how well it matches with the user's profile. The score goes from 0 to 1, with 1 being the best match. It considers five things: the energy, mood, genre, acousticness, and the valence. For energy, acousticness, and valence (how positive a song sounds), the closer a song is to what the user prefers, the more points it gets, and it loses points at a steady rate the further away it is. For example, if someone likes fairly energetic songs, a song with a similar energy level gets more points. Songs that are equally far above or below their preferred energy level get the same points. 
For mood and genre, a song gets points if it matches the user’s choice and no points for that part if it doesn’t. Some parts matter more than others. Energy makes up 30% of the score, mood 25%, genre 20%, acousticness 15%, and valence 10%. I chose these percentages myself and gave energy the most weight because I think it’s one of the main parts of how a song feels. If a user's profile doesn't include a feature, the model ignores that feature and scales the remaining percentages up so the score is still in the range 0 to 1. The recommender adds up the points and shows the five songs with the highest scores. It also shows how much each matching part contributed, so the user can understand why each song was recommended. The starter code didn’t have a way to score or rank songs, so I added that myself.
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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
