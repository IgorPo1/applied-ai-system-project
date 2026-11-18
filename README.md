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