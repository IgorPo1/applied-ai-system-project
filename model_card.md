# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed to suggest songs from a small hand-crafted catalog to a user whose taste is described by four preferences: favourite genre, favourite mood, desired energy level, and whether they enjoy acoustic sounds. It is intended for classroom exploration of how content-based filtering works - not for use as a real product.

**Assumptions about the user:**
- The user can articulate a single favourite genre and mood.
- Preferences are static - the system has no memory of what the user actually played or skipped.

**Not intended for:**
- Production music platforms - the catalog is too small (20 songs) and the algorithm is too simple.
- Discovering songs across genres the user does not already know they like (it will not surprise a pop fan with a great jazz track).

---

## 3. How the Model Works

Every song in the catalog is given a relevance score by comparing its attributes to the user's stated preferences. Think of it like a judge at a competition who awards points:

- **2 points** if the song's genre matches the user's favourite genre - genre is the biggest signal.
- **1 point** if the mood label matches (happy, chill, intense, moody, etc.).
- **Up to 1 point** for energy closeness - a song at exactly the user's preferred energy gets the full point; the further away it is, the fewer points it earns. This is a smooth scale, not a yes/no check.
- **0.5 bonus points** if the user likes acoustic music *and* the song is highly acoustic (acousticness > 0.6).

The maximum possible score is **4.5 points**. Once every song has a score, they are sorted from highest to lowest and the top five are returned with a short explanation showing which rules contributed to the score.

**Changes from the starter logic:** The starter code had all three scoring functions as empty stubs. The weighting scheme above was designed from scratch based on the reasoning that genre is the strongest signal of musical taste, followed by mood, then energy fit.

---

## 4. Data

The catalog contains **20 songs** loaded from `data/songs.csv`.

Each song has the following attributes:
- `genre` - 10 distinct genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, country, r&b, folk, hip-hop
- `mood` - 7 labels: happy, chill, intense, moody, relaxed, focused, (sad - not present in catalog)
- `energy` - float 0.22–0.96
- `tempo_bpm` - integer 55–152
- `valence`, `danceability`, `acousticness` - float 0–1 (loaded but not used in scoring)

**What is missing:**
- Lyrics, cultural context, and language.
- User play history - the model has no collaborative signal whatsoever.
- Release year, artist popularity, or social trends.
- Songs with `mood=sad` - any user requesting sad songs will never get a mood bonus.
- Genre balance: pop (3 songs), lofi (3 songs), rock (2 songs) are over-represented relative to folk (1 song), hip-hop (1 song), country (1 song).

---

## 5. Strengths

- **Transparent:** Every recommendation comes with a plain-language reason showing exactly which scoring rules fired.
- **Consistent:** Given the same profile twice, the same ranked list is always returned - no randomness.
- **Handles acoustic preference well:** Users who want acoustic music get a meaningful bonus that pushes highly-acoustic songs up the list even when genre does not match perfectly.
- **Intuitive for mainstream tastes:** Profiles that match the dominant genres (pop, lofi, rock) in the catalog receive strong, recognisable recommendations. Testing the "Happy Pop Fan" profile consistently returns upbeat pop songs as expected.

---

## 6. Limitations and Bias

**Genre imbalance / filter bubble:** The catalog contains 3 pop songs, 3 lofi songs, and 2 rock songs, but only 1 folk, 1 hip-hop, and 1 country song. Users whose favourite genre is a minority genre will almost always find genre-match songs at the top of a very short list, while the rest of the recommendations default to energy-sorting across unrelated genres. The system effectively traps users inside genres that are well-represented.

**Missing moods:** No song in the catalog is tagged `mood=sad`. A user profile with `mood=sad` never gets the +1.0 mood bonus, making their results purely genre + energy - potentially misleading.

**Energy-gap blindness for edge cases:** The energy score formula (`1 − |song.energy − target_energy|`) always produces a positive value, so even a song with completely wrong energy still gets *some* score. A song at energy=0.22 scores 0.27 on energy for a user who wants energy=0.95 - it is not filtered out, just ranked lower.

**Static preferences:** The model assumes the user's taste is fixed. It cannot learn that a user usually likes pop but today is in a chill lofi mood.

**No artist diversity:** If an artist has many songs in the catalog (e.g., Neon Echo appears three times), they can dominate the top recommendations, which feels repetitive.

---

## 7. Evaluation

**Profiles tested:**

1. **Happy Pop Fan** (pop/happy/energy=0.80): Results were exactly as expected - the two highest-energy happy pop songs ranked first and second. Makes intuitive sense.

2. **Chill Lofi Listener** (lofi/chill/energy=0.38/acoustic=True): All three lofi tracks appeared in the top three. The acoustic bonus pushed highly acoustic non-lofi songs (Porch Swing Rain, Spacewalk Thoughts) into positions 4 and 5, which also felt right - those tracks genuinely have a "chill acoustic" vibe.

3. **High-Energy Rock Head** (rock/intense/energy=0.90): The two rock songs ranked 1st and 2nd. Positions 3–5 went to intense non-rock songs (Gym Hero, Bass Alley, Neon Pulse) - all high energy and intense, which is reasonable when the genre catalog is limited to two rock tracks.

4. **Conflicted Soul - edge case** (folk/sad/energy=0.95): Revealed a critical limitation. The single folk song ranked #1 despite being a terrible energy match, purely on the genre bonus. The mood "sad" never matched anything. This demonstrates the filter-bubble and missing-mood biases clearly.

**Weight-shift experiment:**
Halving the genre weight and doubling the energy weight for the Happy Pop Fan profile moved "Rooftop Lights" from #4 to #3, overtaking "Gym Hero". The top-2 were unchanged because those songs scored high on *all* dimensions simultaneously. The experiment confirmed that genre weight is currently the dominant differentiator between songs with similar energy.

**Surprises:**
- The Chill Lofi Listener achieved the highest absolute scores (4.47, 4.46) because `likes_acoustic=True` adds a fourth scoring axis that other profiles do not use.
- "Gym Hero" (pop/intense/energy=0.93) consistently appeared in the top-5 for the Rock Head profile even though it is not rock - purely because it is very intense and high-energy. This could mislead a user who specifically dislikes pop.

---

## 8. Future Work

1. **Add artist-diversity penalty.** If the same artist already appears in the top-K list, reduce a new song's score by 0.3. This prevents Neon Echo from dominating for certain profiles.

2. **Expand the catalog and add missing moods.** Add at least 5 songs with `mood=sad`, `mood=nostalgic`, and `mood=euphoric` to ensure the mood axis is always meaningful for diverse users.

3. **Introduce a collaborative signal.** Track simulated "play counts" per profile and use those to bias the score slightly toward popular-for-similar-users songs. Even a simple co-occurrence table would make recommendations feel more personalised.

4. **Use more audio features in scoring.** `valence`, `danceability`, and `tempo_bpm` are currently loaded but ignored. Adding valence (musical positivity) to the score would better differentiate sad vs. happy songs with the same energy level.

---

## 9. Personal Reflection

**Biggest learning moment:** Building the scoring function made it immediately obvious why content-based systems create filter bubbles. The moment genre gets the highest weight, the system essentially sorts within a genre first and then everything else second. A user who loves a niche genre is stuck in a small pool regardless of how nuanced their other preferences are.

**How AI tools helped - and when I had to double-check:** AI assistance helped generate the expanded song catalog in CSV format quickly and ensured the numerical values were realistic (e.g., ambient tracks really do cluster around low energy and high acousticness). However, I had to verify the scoring logic manually - the AI initially suggested using `max(0, ...)` clipping for energy scores, which would have made the formula needlessly complex since the absolute-difference formula already stays within [0, 1].

**What surprised me about simple algorithms:** A 4-rule scoring function with hard-coded weights produced recommendations that *felt right* for mainstream profiles. It was striking how much "intelligence" came not from the algorithm itself but from the structure of the data - well-labelled songs and clear genre/mood tags did most of the work.

**What I would try next:** I would implement a diversity penalty to prevent artist repetition, add a user-feedback loop (simulate skips and likes to shift weights over time), and experiment with a hybrid score that blends 70% content-based with 30% collaborative filtering using simulated play history.