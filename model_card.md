# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed to generate personalized music recommendations for a single user based on their stated genre, mood, and energy preferences. It is intended as a classroom simulation of content-based filtering, the same core technique used by Spotify and YouTube Music, for educational exploration and experimentation.

**Assumptions:**
- The user can clearly state a preferred genre, mood, and energy level
- The song catalog is small (20 songs) and covers a range of genres
- All recommendations are explainable: every suggestion includes a reason

**Not intended for:**
- Production music services with real users
- Personalization based on listening history or behavioral data
- Multi-user or collaborative filtering scenarios

---

## 3. How the Model Works

VibeFinder compares a user's stated taste preferences to the attributes of every song in the catalog and assigns each song a numeric score. Songs are then ranked from highest to lowest score, and the top results are returned as recommendations.

The scoring works like this:

- If a song's **genre** matches the user's favorite genre, it earns 2 points. Genre is weighted highest because it is the strongest signal of musical taste.
- If a song's **mood** matches the user's preferred mood, it earns 1 additional point. Mood captures the emotional vibe within a genre.
- The song's **energy level** (0.0–1.0) is compared to the user's target energy. The closer the match, the more points earned, up to 1 point for a perfect match. This creates a smooth, proportional reward instead of a binary pass/fail.

The maximum possible score is 4.0 (genre match + mood match + perfect energy). Songs are sorted from highest to lowest score, and the top 5 are recommended with their reasons listed plainly.

---

## 4. Data

The catalog contains **20 songs** loaded from `data/songs.csv`. Each song has the following attributes:

| Attribute | Description |
|-----------|-------------|
| genre | Musical category (pop, rock, lofi, jazz, hip-hop, electronic, metal, etc.) |
| mood | Emotional vibe (happy, chill, intense, moody, relaxed, focused, sad, peaceful, energetic) |
| energy | Float 0.0–1.0 indicating intensity |
| tempo_bpm | Beats per minute |
| valence | Musical positivity (0 = dark, 1 = bright) |
| danceability | How suitable for dancing (0.0–1.0) |
| acousticness | How acoustic vs. electronic (0.0–1.0) |

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, metal, electronic, acoustic, classical, country

**Limitations of the dataset:**
- 20 songs is extremely small for a real recommender; most genres have only 1–3 songs
- Mood labels are subjective and not standardized
- The dataset does not include lyrics, language, instrumentation detail, or cultural context
- Songs were generated for this simulation and do not represent real-world listening patterns

---

## 5. Strengths

- **Explainability:** Every recommendation comes with a plain-language reason (e.g., "genre match (+2.0); energy proximity (+0.95)"). Users always know why a song was suggested.
- **Differentiated profiles:** The system produces meaningfully different results for different user types. A chill lofi listener gets very different songs than a high-energy pop fan.
- **No cold start problem:** Because recommendations are based purely on song attributes and stated preferences, the system works even for a brand-new user with no listening history.
- **Perfect matches are rewarded:** Songs that match on all three criteria (genre + mood + energy) score near 4.0 and rise clearly to the top.

---

## 6. Limitations and Bias

**Genre dominance:** The genre weight of 2.0 is the single biggest driver of recommendations. If your favorite genre has only 1–2 songs in the catalog, the system quickly fills remaining slots with unrelated songs that merely have high energy proximity. For the "Intense Rock Head" profile, position 1 (Storm Runner) is a perfect rock match, but positions 2–5 are pop, metal, and electronic songs that only share the mood or energy level.

**Filter bubble:** The system can only recommend music from genres that exist in the catalog. A hip-hop fan will always see the same 2 hip-hop songs at the top, regardless of how diverse their energy or mood preferences are. Real-world recommenders solve this with collaborative filtering or catalog diversity rules.

**Energy bias toward extremes:** Songs with very high or very low energy scores (near 0.0 or 1.0) always earn close-to-maximum energy proximity when the user also wants extreme energy. This makes extreme-energy users easier to please than moderate-energy users (who sit in the 0.4–0.6 band where many songs cluster).

**Experiment, Genre Weight 2.0 vs. 0.5 (Pop/Happy profile):**
- At weight 2.0: Top 5 = `Sunrise City, Gym Hero, Rooftop Lights, Golden Hour, Night Drive Loop`
- At weight 0.5: Top 5 = `Sunrise City, Rooftop Lights, Golden Hour, Gym Hero, Night Drive Loop`
- Key change: "Gym Hero" (pop but wrong mood) drops from #2 to #4 when genre weight is reduced. The happy-mood indie pop songs rise above it because their mood match (+1.0) now outweighs the genre advantage. This confirms that genre weight controls whether "same genre, wrong mood" beats "different genre, right mood."

---

## 7. Evaluation

Three distinct user profiles were tested to evaluate whether the recommender produces sensible, differentiated results.

### Profile 1: High-Energy Pop Fan
`genre=pop, mood=happy, energy=0.8`

```
  1. Sunrise City by Neon Echo       Score: 3.98  Why: genre match (+2.0); mood match (+1.0); energy proximity (+0.98)
  2. Gym Hero by Max Pulse           Score: 2.87  Why: genre match (+2.0); energy proximity (+0.87)
  3. Rooftop Lights by Indigo Parade Score: 1.96  Why: mood match (+1.0); energy proximity (+0.96)
  4. Golden Hour by Cleo & The Band  Score: 1.88  Why: mood match (+1.0); energy proximity (+0.88)
  5. Night Drive Loop by Neon Echo   Score: 0.95  Why: energy proximity (+0.95)
```

### Profile 2: Chill Lofi Listener
`genre=lofi, mood=chill, energy=0.35`

```
  1. Library Rain by Paper Lanterns  Score: 4.00  Why: genre match (+2.0); mood match (+1.0); energy proximity (+1.0)
  2. Midnight Coding by LoRoom       Score: 3.93  Why: genre match (+2.0); mood match (+1.0); energy proximity (+0.93)
  3. Focus Flow by LoRoom            Score: 2.95  Why: genre match (+2.0); energy proximity (+0.95)
  4. Spacewalk Thoughts by Orbit Bloom Score: 1.93 Why: mood match (+1.0); energy proximity (+0.93)
  5. Coffee Shop Stories by Slow Stereo Score: 0.98 Why: energy proximity (+0.98)
```

### Profile 3: Intense Rock Head
`genre=rock, mood=intense, energy=0.9`

```
  1. Storm Runner by Voltline        Score: 3.99  Why: genre match (+2.0); mood match (+1.0); energy proximity (+0.99)
  2. Gym Hero by Max Pulse           Score: 1.97  Why: mood match (+1.0); energy proximity (+0.97)
  3. Overdrive by Shatter Point      Score: 1.93  Why: mood match (+1.0); energy proximity (+0.93)
  4. Neon Pulse by Circuit Dreams    Score: 0.98  Why: energy proximity (+0.98)
  5. Concrete Jungle by BeatForge   Score: 0.95  Why: energy proximity (+0.95)
```

### Profile Comparisons

**Pop Fan vs. Lofi Listener:** The pop fan gets energetic songs clustered around 0.8 energy, while the lofi listener gets very low-energy songs (0.28–0.42). Both profiles show that genre match is the dominant factor: the top results always share the user's genre. The lofi profile achieves a perfect 4.00 score (Library Rain matches on all three criteria), confirming the scoring formula is working correctly.

**Lofi Listener vs. Rock Head:** The lofi profile returns calm, soft catalog entries, while the rock profile shifts entirely to high-intensity songs. Interestingly, "Gym Hero" (pop/intense) appears in position 2 for the rock fan because it matches on mood ("intense") even though the genre is wrong. This shows that when there is only one rock song in the catalog, mood and energy proximity can pull in cross-genre songs.

**Pop Fan vs. Rock Head:** Both want high energy (~0.8–0.9), so their rank 3–5 results converge on similar non-genre songs. The difference is at the top: the pop fan gets pop-genre songs first, the rock head gets rock-genre songs first. This confirms that genre weight (2.0) correctly dominates the top of the ranking.

### What Surprised Me

The rock profile has only one true rock song ("Storm Runner") in the dataset. As a result, positions 2–5 are filled by songs that match on mood ("intense") or energy proximity but belong to other genres. This revealed a real limitation of a small catalog: the system runs out of genre-matched options quickly.

---

## 8. Future Work

1. **Add collaborative filtering:** Combine content-based scoring with user listening history, "users who liked Storm Runner also liked these songs", to break out of the genre filter bubble and surface unexpected discoveries.

2. **Expand the catalog and add a diversity rule:** With only 20 songs, genre-scarce profiles get poor results. A catalog of 500+ songs plus a "max 2 songs per genre" diversity rule would prevent the top-5 from being dominated by one genre.

3. **Include valence and danceability in scoring:** The dataset already has these features but they are not used in scoring. Adding `valence` (musical positivity) as a fourth scoring factor would better capture the difference between "energetic and happy" vs. "energetic and angry", two profiles that currently produce nearly identical results.

---

## 9. Personal Reflection

Building VibeFinder 1.0 made the idea of "turning data into predictions" concrete in a way that reading about it never quite did. Before this project, a music recommendation felt like magic, somehow the app just *knows*. After building the scoring function, I understand it is simply math: compare features, assign weights, sort. The "magic" is in choosing which features to weight and how much.

The biggest surprise was discovering how much the **genre weight** controls the system's personality. Changing it from 2.0 to 0.5 reshuffled the rankings visibly, songs that matched the right mood but wrong genre climbed above same-genre songs with the wrong mood. This taught me that a single number in a scoring formula can flip a system from "genre-loyal" to "vibe-based." In a real product, that choice would require user research, not just intuition.

Using AI tools accelerated the implementation significantly, generating the CSV expansion, scoring logic, and CLI formatting would have taken much longer alone. However, I had to stay critical: the AI's first instinct for the import path in `main.py` needed a workaround for how Python resolves modules when run with `-m`. That kind of detail the AI doesn't always get right, and it reinforced that human review of generated code is essential.

What I would try next: add a "diversity penalty" that prevents more than 2 songs from the same artist appearing in the top results, and experiment with weighting `valence` to better capture emotional nuance beyond just happy vs. sad.

---

## 10. Reflection and Ethics (VibeFinder 2.0 - Applied AI System Extension)

### 10.1 Limitations and Biases in the System

VibeFinder 2.0 inherits all limitations from VibeFinder 1.0 and introduces one new consideration:

**Small catalog bias:** 20 songs means that genre-scarce profiles (e.g., rock fans) exhaust genre-matched songs after position 1. Positions 2-5 fall back to mood and energy proximity across unrelated genres. The confidence scores now make this visible: the rock profile shows four low-confidence warnings, correctly communicating that the catalog does not have enough rock songs to fill a meaningful top-5.

**Binary mood matching:** Mood matching is all-or-nothing. "Intense" and "energetic" are close concepts but score 0 overlap. This creates an invisible ceiling: a user wanting "energetic" will never see a song labeled "intense" in their top results, even if the energy and genre align perfectly.

**Confidence score linearity:** The confidence formula (`score / 4.0`) is linear. A song matching only on energy proximity (score ~ 0.9) earns 22% confidence, which may feel too low to users. A real system would use a percentile rank against the full catalog to express "this is in the top 10% of matches," which is more meaningful than an absolute fraction.

**Guardrail coverage:** The current guardrail only validates genre, mood, and energy. It does not check for nonsensical combinations (e.g., genre="electro-jazz-fusion" which has no catalog match). Invalid genre strings pass validation but return only energy-proximity results, which may silently mislead users.

### 10.2 Potential Misuse and Prevention

**Filter bubble reinforcement:** If this system were deployed as a real music platform, its genre-dominant scoring would actively narrow users' exposure over time. A user who states "pop" as their favorite genre would only ever see pop songs at the top, regardless of whether they might enjoy adjacent genres. Prevention: add a diversity bonus that rewards cross-genre results in positions 3-5, and implement a user feedback loop (thumbs up/down) to recalibrate weights over time.

**False confidence display:** The confidence score could be misinterpreted by users as "the AI is 100% sure this is a great song," when it actually means "this song matches your stated preferences on all three criteria." A user with unusual or niche preferences (e.g., "classical + energetic + intense") might receive a 100% confidence score for the closest match in the catalog even if that match is a poor fit. Prevention: add a caveat label explaining what the confidence score means (preference alignment, not quality) and a catalog-coverage note ("only N songs available in your genre").

**Bypassing guardrails with valid but nonsensical input:** A user could input `energy=0.5, genre="zzz", mood="zzz"` and pass validation while getting meaningless results. Prevention: add a catalog-lookup check that warns if no songs in the catalog match the given genre.

### 10.3 What Surprised Me While Testing Reliability

The most surprising finding was how informative the confidence scores became for the **rock profile**. Before adding guardrails, the rock profile looked successful: it returned 5 songs with scores ranging from 0.95 to 3.99. But after adding confidence scoring, it became immediately clear that only 1 song (Storm Runner, 100%) was actually a good match. All 4 remaining results were below 50% confidence, meaning the system was filling slots with songs that shared only one attribute (mood or energy), not a genuine genre match.

This revealed that the system was previously "succeeding" on a metric (returning 5 results) while failing on a more meaningful metric (returning 5 relevant results). The guardrail turned a silent, plausible-looking failure into a visible, documented one. This is exactly the kind of reliability improvement that evaluation harnesses are designed to surface.

I also expected the evaluator's edge case (rock + sad mood, high energy) to fail, predicting that no rock song in the catalog would score above 2.0. It actually scored 2.96 because Storm Runner's rock genre match (+2.0) plus energy proximity (+0.96) exceeded the 2.0 threshold even without a mood match. This showed me that the genre weight is strong enough to carry a result even when mood is completely wrong.

### 10.4 AI Collaboration During This Project

**How I used AI:** I used an AI coding assistant throughout this extension project for:
- Structuring the guardrails module (deciding what to validate and how to represent errors)
- Designing the evaluation harness test case format
- Writing the unit tests for boundary conditions
- Drafting documentation sections in the README and model card

**One helpful AI suggestion:** When designing the `flag_low_confidence` function, the AI suggested making it accept the full `(song, score, explanation)` tuple list from `recommend_songs` directly, rather than requiring me to extract scores first. This kept the function's interface aligned with the rest of the pipeline and made it easier to reference the song title in warning messages without a second lookup. It was a clean design suggestion that I adopted unchanged.

**One flawed AI suggestion:** When writing the test for `validate_user_profile` with multiple simultaneous errors (both empty genre AND energy out of range), the AI initially suggested asserting `len(errors) >= 1` instead of `len(errors) == 2`. The reasoning given was "the validator might short-circuit on the first error." This was incorrect, the validator is explicitly designed to collect all errors in a single pass and return them together, which is more useful behavior. I rewrote the assertion to `== 2`, which is the correct and more precise test. The AI's instinct to hedge with `>= 1` would have left the test weaker and masked a potential bug where only one error was reported.

**Limitations and future improvements:**
- Add semantic mood similarity so "intense" and "energetic" score partial overlap instead of 0
- Expand the catalog to 100+ songs so genre-scarce profiles receive more relevant results
- Add a diversity penalty (maximum 2 songs per genre in top-5) to break filter bubbles
- Replace the linear confidence score with a percentile rank across the full catalog