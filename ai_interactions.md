# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to extend the recommender with five new song attributes: popularity (0–100), release decade, language, vocal type (vocals or instrumental), and detailed mood tags with more than one tag per song. It had to update both `data/songs.csv` and the scoring logic in `src/recommender.py`

**Prompts used:**

1. "Can you help me extend my music recommender by adding five new song attributes: popularity (0–100), release decade, language, vocal type (vocals or instrumental), and detailed mood tags that allow more than one tag per song? Some mood tags I was thinking of were nostalgic, euphoric, dreamy, melancholic, aggressive, hopeful, reflective, tense, and confident. Make sure to update both data/songs.csv to include these new types and the scoring logic in src/recommender.py. Make a note that the current README and model_card do not account for the challenge changes that we do."

**What did the agent generate or change?**

- The agent read `src/recommender.py`, `data/songs.csv`, `src/main.py`.
- `data/songs.csv`: It updated the The CSV columns to make sure all 18 songs have `popularity`, `release_decade`, `language`, `vocal_type` and `mood_tags`, with multiple tags separated by `|`.
- `src/recommender.py`: It made sure `load_songs` parses the new columns (optional, so older CSVs still load).  Also, `score_song` noew scores popularity and decade by closeness (decade drops to 0 at 50 years apart), language and vocal type as exact matches, and mood tags by the share of the user's tags that the song has. Weights are 0.05 for popularity, decade, language and vocal type, and 0.15 for mood tags. Features that a profile leaves out are skipped, and the score is divided by the weights actually used so it still runs 0–1.
- `src/main.py`: It added a "Nostalgic Dreamer" profile that uses all the new features.
- `README.md` and `model_card.md`: it included the short note at the top of each saying they do not account for the challenge changes.

**What did you verify or fix manually?**

- I ran `python -m src.main` and 18 songs loaded. The Nostalgic Dreamer output shows popularity, decade and mood-tag reasons, and the four original profiles still run.
- I also made sure that the first agent-drafted README note was accurate and appropriate to the changes made.

---
