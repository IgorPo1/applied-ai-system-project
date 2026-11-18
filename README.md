# VibeFinder 2.0 - Music Recommender with Guardrails

## Original Project

**Base project:** AI110 Module 3 Show What You Know - Music Recommender Simulation

The original VibeFinder 1.0 (Module 3) was a content-based music recommendation simulator. It loaded a 20-song CSV catalog, scored each song against a user's stated genre/mood/energy preferences using a weighted formula (genre +2.0, mood +1.0, energy proximity 0-1.0), and returned the top-K recommendations with plain-language explanations. The system demonstrated how real-world streaming platforms like Spotify translate song attributes and user taste into ranked suggestions.

---

## What's New in VibeFinder 2.0

This version extends the base recommender into a full Applied AI System by adding:

| New Component | What It Does |
|---|---|
| **`src/guardrails.py`** | Validates user profiles before scoring; computes confidence scores; flags weak recommendations |
| **`src/evaluator.py`** | Structured evaluation harness - 8 test cases with pass/fail reporting in markdown format |
| **`tests/test_guardrails.py`** | 16 new unit tests covering all guardrail functions |
| **`diagrams/architecture.mmd`** | Mermaid source diagram showing full system data flow |

---

## System Architecture

See [`diagrams/architecture.mmd`](diagrams/architecture.mmd) for the full Mermaid source diagram.

```
User Input (genre, mood, energy)
        |
        v
[Input Guardrail] -- validate_user_profile()
        |                   |
    invalid              valid
        |                   |
   Error message     [Song Catalog Loader] -- load_songs(data/songs.csv)
                           |
                           v
                    [Scoring Engine] -- score_song()
                      genre +2.0, mood +1.0, energy proximity 0-1
                           |
                           v
                    [Recommender] -- recommend_songs()
                      ranked top-K results
                           |
                           v
                    [Confidence Scorer] -- confidence_score()
                      score / max_score -> 0.0-1.0
                           |
                           v
                    [Output Guardrail] -- flag_low_confidence()
                      warn when confidence < 50%
                           |
                           v
                   Recommendations + Explanations + Confidence Scores

(Parallel branch)
[Evaluator] -- src/evaluator.py
  Runs 8 structured test cases against the full pipeline
  Outputs markdown pass/fail table
  Writes evaluation_results.md
```

**Data flows:**
1. User prefs dict goes through `validate_user_profile` before any scoring happens
2. Songs are loaded from CSV and passed to `recommend_songs` which calls `score_song` for every song
3. Each result is annotated with a confidence score and checked against the 50% threshold
4. The evaluator exercises the full pipeline with known-good and invalid inputs to verify system reliability

---

## Setup Instructions

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd ai110-module3show-musicrecommendersimulation-starter-main
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the recommender (main demo)

```bash
python -m src.main
```

### 5. Run the evaluation harness

```bash
python -m src.evaluator
```

### 6. Run all tests

```bash
python -m pytest
```

---

## Sample Interactions

### Interaction 1: Valid profiles with confidence scores and warnings

Command: `python -m src.main`

```
Loaded songs: 20
VibeFinder 2.0 - Music Recommender with Guardrails

=======================================================
  Profile : High-Energy Pop Fan
  Prefs   : genre=pop, mood=happy, energy=0.8
=======================================================
  1. Sunrise City by Neon Echo
     Score      : 3.98 / 4.00  |  Confidence: 100%
     Why        : genre match (+2.0); mood match (+1.0); energy proximity (+0.98)
  2. Gym Hero by Max Pulse
     Score      : 2.87 / 4.00  |  Confidence: 72%
     Why        : genre match (+2.0); energy proximity (+0.87)
  3. Rooftop Lights by Indigo Parade
     Score      : 1.96 / 4.00  |  Confidence: 49%
     Why        : mood match (+1.0); energy proximity (+0.96)
  4. Golden Hour by Cleo & The Band
     Score      : 1.88 / 4.00  |  Confidence: 47%
     Why        : mood match (+1.0); energy proximity (+0.88)
  5. Night Drive Loop by Neon Echo
     Score      : 0.95 / 4.00  |  Confidence: 24%
     Why        : energy proximity (+0.95)

  -- Low-Confidence Warnings --
  [WARN] Rank #3 'Rooftop Lights' - low confidence (49%); this song has weak feature alignment with your profile.
  [WARN] Rank #4 'Golden Hour' - low confidence (47%); this song has weak feature alignment with your profile.
  [WARN] Rank #5 'Night Drive Loop' - low confidence (24%); this song has weak feature alignment with your profile.

=======================================================
  Profile : Chill Lofi Listener
  Prefs   : genre=lofi, mood=chill, energy=0.35
=======================================================
  1. Library Rain by Paper Lanterns
     Score      : 4.00 / 4.00  |  Confidence: 100%
     Why        : genre match (+2.0); mood match (+1.0); energy proximity (+1.0)
  2. Midnight Coding by LoRoom
     Score      : 3.93 / 4.00  |  Confidence: 98%
     Why        : genre match (+2.0); mood match (+1.0); energy proximity (+0.93)
  3. Focus Flow by LoRoom
     Score      : 2.95 / 4.00  |  Confidence: 74%
     Why        : genre match (+2.0); energy proximity (+0.95)
  4. Spacewalk Thoughts by Orbit Bloom
     Score      : 1.93 / 4.00  |  Confidence: 48%
     Why        : mood match (+1.0); energy proximity (+0.93)
  5. Coffee Shop Stories by Slow Stereo
     Score      : 0.98 / 4.00  |  Confidence: 24%
     Why        : energy proximity (+0.98)

  -- Low-Confidence Warnings --
  [WARN] Rank #4 'Spacewalk Thoughts' - low confidence (48%); ...
  [WARN] Rank #5 'Coffee Shop Stories' - low confidence (24%); ...

=======================================================
  Profile : Intense Rock Head
  Prefs   : genre=rock, mood=intense, energy=0.9
=======================================================
  1. Storm Runner by Voltline
     Score      : 3.99 / 4.00  |  Confidence: 100%
     Why        : genre match (+2.0); mood match (+1.0); energy proximity (+0.99)
  2. Gym Hero by Max Pulse
     Score      : 1.97 / 4.00  |  Confidence: 49%
     Why        : mood match (+1.0); energy proximity (+0.97)
  3. Overdrive by Shatter Point
     Score      : 1.93 / 4.00  |  Confidence: 48%
     Why        : mood match (+1.0); energy proximity (+0.93)
  4. Neon Pulse by Circuit Dreams
     Score      : 0.98 / 4.00  |  Confidence: 24%
     Why        : energy proximity (+0.98)
  5. Concrete Jungle by BeatForge
     Score      : 0.95 / 4.00  |  Confidence: 24%
     Why        : energy proximity (+0.95)

  -- Low-Confidence Warnings --
  [WARN] Rank #2 'Gym Hero' - low confidence (49%); ...
  [WARN] Rank #3 'Overdrive' - low confidence (48%); ...
  [WARN] Rank #4 'Neon Pulse' - low confidence (24%); ...
  [WARN] Rank #5 'Concrete Jungle' - low confidence (24%); ...
```

### Interaction 2: Guardrail blocking invalid inputs

```
=======================================================
  Profile : Invalid Profile (energy=1.5)
  Prefs   : genre=jazz, mood=relaxed, energy=1.5
=======================================================
  [INVALID] Profile blocked by guardrails -- cannot generate recommendations:
       - 'energy' must be between 0.0 and 1.0, got 1.5

=======================================================
  Profile : Invalid Profile (no genre)
  Prefs   : genre=, mood=chill, energy=0.4
=======================================================
  [INVALID] Profile blocked by guardrails -- cannot generate recommendations:
       - 'genre' must be a non-empty string (e.g. 'pop', 'rock', 'lofi')
```

### Interaction 3: Evaluation harness output

Command: `python -m src.evaluator`

```
Loaded 20 songs from catalog.

## VibeFinder 2.0 - Evaluation Results

| # | Test Profile | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| 1 | High-Energy Pop Fan | genre='pop', mood='happy', energy=0.8 | valid | top genre=pop | score>=3.5 | valid | top genre=pop | score=3.98 | PASS |
| 2 | Chill Lofi Listener | genre='lofi', mood='chill', energy=0.35 | valid | top genre=lofi | score>=3.9 | valid | top genre=lofi | score=4.00 | PASS |
| 3 | Intense Rock Head | genre='rock', mood='intense', energy=0.9 | valid | top genre=rock | score>=3.5 | valid | top genre=rock | score=3.99 | PASS |
| 4 | Jazz Relaxed Fan | genre='jazz', mood='relaxed', energy=0.37 | valid | top genre=jazz | score>=3.5 | valid | top genre=jazz | score=4.00 | PASS |
| 5 | Edge Case: Conflicting Prefs | genre='rock', mood='sad', energy=0.95 | valid | top genre=rock | score>=2.0 | valid | top genre=rock | score=2.96 | PASS |
| 6 | INVALID: Energy out of range (1.5) | energy=1.5 | guardrail blocks | blocked | PASS |
| 7 | INVALID: Empty genre string | genre='' | guardrail blocks | blocked | PASS |
| 8 | INVALID: Missing energy key | energy=<missing> | guardrail blocks | blocked | PASS |

**Summary:** 8 out of 8 tests passed.
```

---

## Design Decisions

### Why Guardrails + Evaluation over RAG or Fine-Tuning?

The base recommender is a deterministic, rule-based system (no LLM, no external API). The most meaningful extension was to make it **reliably safe to run** - ensuring bad inputs fail loudly and good results are annotated with a confidence measure. A RAG system would have required an LLM API key and external data sources, adding complexity without improving the core reliability of the scoring algorithm.

The **evaluation harness** is the most important addition: it transforms the system from "run it and hope" into "run it and prove it works." The 8-case test table (5 valid, 3 invalid guardrail tests) provides verifiable, reproducible evidence that the system behaves correctly.

### Confidence Score Design

The confidence score is `score / 4.0` - a simple linear mapping. A song matching on all three criteria (genre + mood + perfect energy) scores 4.0 and gets 100% confidence. A song matching only on energy proximity scores ~0.9 and gets ~24% confidence. The 50% threshold (score < 2.0) was chosen because below that point the top-matching criterion (genre, worth 2.0 points) has not been met at all.

### Trade-offs

| Decision | Alternative | Why This Choice |
|---|---|---|
| Input validation in separate module | Inline checks in main.py | Testable independently; reusable by evaluator |
| Confidence = score/4.0 (linear) | Sigmoid or percentile-based | Simple, explainable, directly tied to the scoring formula |
| Evaluation writes to .md file | Writes to .json or .csv | Markdown is directly readable in GitHub without tooling |
| 50% confidence threshold for warnings | Higher (70%) or lower (25%) | 50% means "at least one strong feature matched"; a useful semantic boundary |

---

## Testing Summary

### Automated Unit Tests (pytest)

```
pytest tests/ -v
```

```
18 passed in 0.19s

tests/test_guardrails.py::test_validate_valid_profile_returns_true_and_no_errors   PASSED
tests/test_guardrails.py::test_validate_empty_genre_returns_error                  PASSED
tests/test_guardrails.py::test_validate_energy_above_1_returns_error               PASSED
tests/test_guardrails.py::test_validate_energy_below_0_returns_error               PASSED
tests/test_guardrails.py::test_validate_missing_energy_key_returns_error           PASSED
tests/test_guardrails.py::test_validate_multiple_errors_reported_together          PASSED
tests/test_guardrails.py::test_validate_boundary_energy_0_is_valid                 PASSED
tests/test_guardrails.py::test_validate_boundary_energy_1_is_valid                 PASSED
tests/test_guardrails.py::test_confidence_score_perfect_returns_1                  PASSED
tests/test_guardrails.py::test_confidence_score_zero_returns_0                     PASSED
tests/test_guardrails.py::test_confidence_score_half_returns_half                  PASSED
tests/test_guardrails.py::test_confidence_score_clamped_above_1                    PASSED
tests/test_guardrails.py::test_confidence_score_uses_default_max                   PASSED
tests/test_guardrails.py::test_flag_no_warnings_when_all_above_threshold           PASSED
tests/test_guardrails.py::test_flag_returns_warnings_for_low_scores                PASSED
tests/test_guardrails.py::test_flag_warning_mentions_song_title                    PASSED
tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score            PASSED
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string    PASSED
```

### Evaluator Results

**8 out of 8 evaluator tests passed.** See [`evaluation_results.md`](evaluation_results.md) for the full table.

**Key findings:**
- All 5 valid profiles returned the expected top genre with scores >= their thresholds
- The edge case (rock + sad mood) correctly returned the only rock song at rank 1 even without a mood match, with a score of 2.96 (energy proximity padded the genre score)
- All 3 invalid inputs were caught by the guardrail before any scoring ran
- The lofi and jazz profiles both achieved 4.00/4.00 (perfect match exists in the catalog)

**What didn't work initially:** The confidence threshold warning triggers for *all three* rock profile recommendations after rank 1, because the catalog has only one rock song. This is expected behavior - it correctly surfaces that the rock fan is receiving poor matches after position 1, which is exactly what the guardrail is designed to tell them.

---

## Reflection

Extending VibeFinder 1.0 into a full applied AI system taught me that reliability infrastructure (validation, confidence scoring, evaluation harnesses) is often more valuable than adding new algorithmic features. The original recommender already worked correctly - but it had no way to communicate *how well* it worked on any given input. Adding guardrails made that visible.

> Full reflection on AI collaboration, biases, and system limitations is documented in [`model_card.md`](model_card.md).

---

## Project Structure

```
.
+-- src/
|   +-- recommender.py      # Core: load_songs, score_song, recommend_songs, Song, UserProfile, Recommender
|   +-- guardrails.py       # NEW: validate_user_profile, confidence_score, flag_low_confidence
|   +-- evaluator.py        # NEW: structured 8-case evaluation harness
|   +-- main.py             # CLI runner (updated to use guardrails)
+-- tests/
|   +-- test_recommender.py # Original 2 recommender tests
|   +-- test_guardrails.py  # NEW: 16 guardrail unit tests
+-- data/
|   +-- songs.csv           # 20-song catalog
+-- diagrams/
|   +-- architecture.mmd   # NEW: Mermaid system architecture diagram
+-- assets/                 # Reserved for supplementary images
+-- evaluation_results.md   # NEW: auto-generated evaluator output
+-- model_card.md           # AI system documentation and reflection
+-- requirements.txt
+-- README.md
```

---

## Original Project Goals (Module 3)

For reference, the original VibeFinder 1.0 goals from the Module 3 assignment:

- Explain the transformation of data into predictions
- Design a weighted-score recommender using genre, mood, and energy attributes
- Identify and document algorithmic bias (filter bubbles, genre dominance)
- Communicate technical reasoning through a Model Card

All of these are preserved in the current system and documented in [`model_card.md`](model_card.md).