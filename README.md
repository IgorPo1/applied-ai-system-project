# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system, similar to what platforms like Spotify or YouTube Music use under the hood. Given a user "taste profile" (favourite genre, mood, and target energy level), the system scores every song in a catalog and returns a personalised, ranked top-K list with a plain-language explanation for each pick.

The core idea: **songs are scored, not searched.** Every track gets a numeric relevance score computed from how closely its attributes match the user's preferences, and the highest-scoring songs bubble to the top.

---

## How The System Works

### Real-World Context

Major streaming platforms blend two main techniques:

1. **Collaborative Filtering** - "People who liked what you liked also enjoyed *X*." The system learns from the collective behaviour of millions of users: plays, skips, likes, and playlist additions. It does not need to know anything about the song's sound; it only needs to know who else liked it.

2. **Content-Based Filtering** - "This song *sounds* like what you already love." The system analyses measurable audio attributes (genre, mood, energy, tempo, valence, danceability, acousticness) and matches them to the user's stated or inferred taste profile. This is what our simulation implements.

Our version is a **weighted content-based recommender**. It does not have access to other users' history, so it relies entirely on song attributes and the user's explicit preferences.

### Data Flow

```
  songs.csv          User Preferences
      │               (genre, mood, target_energy, likes_acoustic)
      ▼                          │
  load_songs()                   │
      │                          │
      ▼                          ▼
      └──────────────────────────┘
                    │
                    ▼
      ┌─────────────────────────────────────┐
      │       FOR EVERY song in catalog     │
      │                                     │
      │   score_song(user_prefs, song)      │
      │   - genre match?    →  +2.0         │
      │   - mood match?     →  +1.0         │
      │   - energy sim.     →  +0.0..+1.0   │
      │   - acoustic bonus? →  +0.5         │
      │              │                      │
      │              ▼                      │
      │   (numeric_score, [reasons])        │
      └─────────────────────────────────────┘
                    │
                    ▼
      sort descending by score
                    │
                    ▼
      top-K (song, score, explanation)
```

### Song Features Used

| Feature | Type | Description |
|---|---|---|
| `genre` | categorical | Musical genre (pop, rock, lofi, jazz, …) |
| `mood` | categorical | Emotional tone (happy, chill, intense, moody, …) |
| `energy` | float 0–1 | How energetic / driving the track feels |
| `tempo_bpm` | int | Beats per minute |
| `valence` | float 0–1 | Musical positivity (high = upbeat, low = dark) |
| `danceability` | float 0–1 | How suited the track is for dancing |
| `acousticness` | float 0–1 | How acoustic (vs. electronic) the track is |

### UserProfile Fields

| Field | Type | Description |
|---|---|---|
| `favorite_genre` | str | Genre the user most wants to hear |
| `favorite_mood` | str | Preferred emotional tone |
| `target_energy` | float 0–1 | Desired energy level |
| `likes_acoustic` | bool | Whether the user prefers acoustic sounds |

### Algorithm Recipe (Scoring Rules)

Each song starts at **0 points**. Four rules are applied in order, and the results are summed:

| # | Rule | Condition | Score Added |
|---|---|---|---|
| 1 | **Genre match** | `song.genre == favorite_genre` | **+2.0** (or +0 if no match) |
| 2 | **Mood match** | `song.mood == favorite_mood` | **+1.0** (or +0 if no match) |
| 3 | **Energy similarity** | *Always applied* - closer is better | `+(1.0 − \|song.energy − target_energy\|)` → range: **+0.0 to +1.0** |
| 4 | **Acoustic bonus** | `likes_acoustic = True` AND `song.acousticness > 0.6` | **+0.5** (or +0 otherwise) |

**Total max score: 4.5 points** (2.0 + 1.0 + 1.0 + 0.5).

**Key things to understand about each rule:**

- **Rules 1 & 2 are binary** - either the labels match exactly and you get the full points, or you get nothing. There is no partial credit for "similar" genres.
- **Rule 3 is always applied** - every song gets an energy score whether or not genre or mood matched. A song at exactly the target energy scores +1.0; a song 0.5 away scores +0.5; a song 1.0 away (the worst possible) scores +0.0.
- **Rule 4 is a bonus axis** - only users with `likes_acoustic = True` can earn it, giving acoustic-preference users a higher possible ceiling (4.5 pts) vs. non-acoustic users (4.0 pts max).

### User Profiles Defined

Three representative taste profiles are used throughout evaluation:

| Profile Name | favorite_genre | favorite_mood | target_energy | likes_acoustic |
|---|---|---|---|---|
| Happy Pop Fan | pop | happy | 0.80 | False |
| Chill Lofi Listener | lofi | chill | 0.38 | True |
| High-Energy Rock Head | rock | intense | 0.90 | False |

### Potential Biases to Watch

- **Genre over-weight**: if the catalog has many songs of one genre, those songs dominate results regardless of other attributes.
- **Filter bubble**: a user with `genre=pop` will almost never see jazz or rock, even if those songs have a perfect mood/energy match.
- **Small dataset**: with 20 songs, a single genre imbalance has an outsized effect on diversity.
- **Mood granularity**: "focused" and "relaxed" are rare moods in the catalog - users who prefer them may never get a mood match bonus.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

```
Catalog size: 20 songs

============================================================
 Profile: Happy Pop Fan
   genre=pop, mood=happy, energy=0.8, acoustic=False
============================================================
  1. Electric Dream - Starfield
     Score : 4.00 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+1.00)

  2. Sunrise City - Neon Echo
     Score : 3.98 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

  3. Gym Hero - Max Pulse
     Score : 2.87 / 4.50
     Why   : genre match (+2.0), energy similarity (+0.87)

  4. Rooftop Lights - Indigo Parade
     Score : 1.96 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.96)

  5. Golden Afternoon - The Velvet Keys
     Score : 1.68 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.68)

============================================================
 Profile: Chill Lofi Listener
   genre=lofi, mood=chill, energy=0.38, acoustic=True
============================================================
  1. Library Rain - Paper Lanterns
     Score : 4.47 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.97), acoustic bonus (+0.5)

  2. Midnight Coding - LoRoom
     Score : 4.46 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.96), acoustic bonus (+0.5)

  3. Focus Flow - LoRoom
     Score : 3.48 / 4.50
     Why   : genre match (+2.0), energy similarity (+0.98), acoustic bonus (+0.5)

  4. Porch Swing Rain - Hollow Oak
     Score : 2.42 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.92), acoustic bonus (+0.5)

  5. Spacewalk Thoughts - Orbit Bloom
     Score : 2.40 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.90), acoustic bonus (+0.5)

============================================================
 Profile: High-Energy Rock Head
   genre=rock, mood=intense, energy=0.9, acoustic=False
============================================================
  1. Storm Runner - Voltline
     Score : 3.99 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.99)

  2. Iron Curtain - The Breakers
     Score : 3.98 / 4.50
     Why   : genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

  3. Gym Hero - Max Pulse
     Score : 1.97 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.97)

  4. Bass Alley - Dropout Kings
     Score : 1.95 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.95)

  5. Neon Pulse - Circuit Drift
     Score : 1.94 / 4.50
     Why   : mood match (+1.0), energy similarity (+0.94)
```

---

## Explained Recommendations

The following explanations are generated directly by the scoring logic in [`score_song()`](src/recommender.py). Each reason names the rule that fired and the points it contributed.

### Happy Pop Fan profile (genre=pop, mood=happy, energy=0.80)

1. **Electric Dream** - *genre match (+2.0), mood match (+1.0), energy similarity (+1.00)* - this song is a pop track tagged happy with energy=0.80, an exact match on all three primary rules, making it the highest scorer.
2. **Sunrise City** - *genre match (+2.0), mood match (+1.0), energy similarity (+0.98)* - also pop and happy, with energy=0.82 just 0.02 above target, so nearly perfect.
3. **Gym Hero** - *genre match (+2.0), energy similarity (+0.87)* - pop genre matches but mood is "intense" not "happy", so only two rules fire; still ranks third due to the strong genre bonus.

### Chill Lofi Listener profile (genre=lofi, mood=chill, energy=0.38, likes_acoustic=True)

1. **Library Rain** - *genre match (+2.0), mood match (+1.0), energy similarity (+0.97), acoustic bonus (+0.5)* - lofi, chill, energy=0.35 (very close to 0.38), and acousticness=0.86 - all four rules fire.
2. **Midnight Coding** - *genre match (+2.0), mood match (+1.0), energy similarity (+0.96), acoustic bonus (+0.5)* - lofi, chill, energy=0.42, acousticness=0.71 - same four rules, fractionally lower energy match.
3. **Focus Flow** - *genre match (+2.0), energy similarity (+0.98), acoustic bonus (+0.5)* - lofi genre and high acousticness match, but mood is "focused" not "chill" so the mood rule does not fire.

### High-Energy Rock Head profile (genre=rock, mood=intense, energy=0.90)

1. **Storm Runner** - *genre match (+2.0), mood match (+1.0), energy similarity (+0.99)* - rock, intense, energy=0.91, nearly perfect across all three rules.
2. **Iron Curtain** - *genre match (+2.0), mood match (+1.0), energy similarity (+0.98)* - rock, intense, energy=0.88, same three rules, slightly lower energy fit.
3. **Gym Hero** - *mood match (+1.0), energy similarity (+0.97)* - intense mood and very high energy (0.93) are both a match, but it is a pop song not rock, so the genre bonus (+2.0) never fires; it lands at #3 purely on mood + energy.

---

## Experiments You Tried

### Experiment 1 - Weight Shift (Genre halved, Energy doubled) for Happy Pop Fan

Original weights: genre=2.0, energy similarity=1×.
Experiment weights: genre=1.0, energy similarity=2×.

**Before:** #1 Electric Dream (4.00), #2 Sunrise City (3.98), #3 Gym Hero (2.87)
**After:**  #1 Electric Dream (4.00), #2 Sunrise City (3.96), #3 Rooftop Lights (2.92)

*What changed:* "Rooftop Lights" (indie pop, happy, energy=0.76) jumped from #4 to #3, overtaking "Gym Hero". When energy becomes more important, songs that are *very close* in energy but lack a genre match can overtake songs that *have* the genre match but a worse energy fit. The overall top-2 stayed the same because those songs happened to be near-perfect matches on all dimensions.

### Experiment 2 - Adversarial / Edge Case: "Conflicted Soul"

Profile: `genre=folk, mood=sad, energy=0.95, likes_acoustic=True`

This is a deliberately contradictory profile - folk music is almost never high-energy or sad. The dataset has zero songs tagged `mood=sad`, so the mood bonus never fires. Only one folk song exists ("Porch Swing Rain"), which ranks first on genre match alone despite being a terrible energy fit.

```
============================================================
 Profile: Conflicted Soul (edge case)
   genre=folk, mood=sad, energy=0.95, acoustic=True
============================================================
  1. Porch Swing Rain - Hollow Oak
     Score : 2.85 / 4.50
     Why   : genre match (+2.0), energy similarity (+0.35), acoustic bonus (+0.5)

  2. Desert Highway - Cactus Road
     Score : 1.10 / 4.50
     Why   : energy similarity (+0.60), acoustic bonus (+0.5)

  3. Golden Afternoon - The Velvet Keys
     Score : 1.03 / 4.50
     Why   : energy similarity (+0.53), acoustic bonus (+0.5)

  4. Neon Pulse - Circuit Drift
     Score : 0.99 / 4.50
     Why   : energy similarity (+0.99)

  5. Gym Hero - Max Pulse
     Score : 0.98 / 4.50
     Why   : energy similarity (+0.98)
```

Notice that the mood bonus (+1.0) never fires for any song - `mood=sad` does not exist in the catalog. The genre bonus fires only once (Porch Swing Rain), and the remaining 4 slots are filled entirely by energy sorting across random genres. This reveals the **filter bubble problem**: when a genre is rare and the mood does not exist in the catalog, the recommender becomes an energy-only sorter.

### Experiment 3 - Profile Comparison Summary

The table below shows how the #1 recommendation and scoring pattern changes across all four profiles:

| Profile | #1 Song | Score | Rules that fired |
|---|---|---|---|
| Happy Pop Fan | Electric Dream | 4.00 | genre + mood + energy |
| Chill Lofi Listener | Library Rain | 4.47 | genre + mood + energy + acoustic |
| High-Energy Rock Head | Storm Runner | 3.99 | genre + mood + energy |
| Conflicted Soul (edge) | Porch Swing Rain | 2.85 | genre + energy + acoustic (mood never fired) |

**What changed across profiles and why:**

- **Pop Fan vs. Rock Head**: Both profiles hit 3 matching rules and score similarly (~4.0 and ~3.99). The gap is negligible because both genres have at least 2 well-matched songs in the catalog. Recommendations stay firmly within the user's genre.
- **Rock Head vs. Chill Lofi**: The Lofi listener scores *higher* (4.47 vs. 3.99) because `likes_acoustic=True` unlocks a fourth scoring dimension. The lofi profile also benefits from 3 lofi songs in the catalog vs. only 2 rock songs, giving it more top-slot candidates.
- **Any well-matched profile vs. Conflicted Soul**: The Conflicted Soul's #1 song scores only 2.85 - nearly 1.6 points lower - because the genre is rare (1 song), the mood is missing from the catalog entirely, and the one genre match has terrible energy alignment. This makes the system's filter-bubble weakness visible: minority genres and missing mood labels are silently penalised.

---

## Limitations and Risks

- Works only on a tiny hand-crafted catalog - real platforms have millions of tracks
- Does not understand lyrics, language, or cultural context
- May over-favour the dominant genre in the CSV
- Cannot adapt over time - it has no memory of what the user actually played
- Does not account for song popularity, release date, or social trends

---

## Reflection

See [**Model Card**](model_card.md) for a full discussion of limitations, biases, and future improvements.

Building this recommender made two things very clear. First, turning raw data into predictions is deceptively simple at a mechanical level - it really is just arithmetic - but the *choices* embedded in that arithmetic (which features to use, how much to weight genre vs. energy) determine whether the output is useful or misleading. Second, bias in AI systems often comes not from malicious design but from gaps in the data: the moment "sad" did not exist as a mood label in the catalog, any user who wanted sad songs was silently penalised. Real platforms solve this with enormous catalogs and continuous feedback loops; our simulation makes the underlying mechanics legible precisely because it is so small.