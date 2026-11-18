"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for three distinct user profiles and prints a clean,
readable list of top-K recommendations with scores and reasons.
"""

import os
import sys

# Allow `python -m src.main` and `python src/main.py` to both find recommender
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from recommender import load_songs, recommend_songs

# ──────────────────────────────────────────────────────
# User Profiles (Phase 2 / Phase 4 definitions)
# ──────────────────────────────────────────────────────

PROFILES = {
    "Happy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "likes_acoustic": False,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "High-Energy Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
        "likes_acoustic": False,
    },
    # Adversarial profile: conflicting high-energy + sad mood; rare genre
    "Conflicted Soul (edge case)": {
        "genre": "folk",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": True,
    },
}

# ──────────────────────────────────────────────────────
# Experimental profile: genre weight halved (energy × 2)
# Used in Phase 4 weight-shift experiment
# ──────────────────────────────────────────────────────

def score_song_experiment(user_prefs: dict, song: dict):
    """Weight-shift experiment: genre=1.0 (halved), energy similarity doubled."""
    score = 0.0
    reasons = []
    if song['genre'] == user_prefs.get('genre'):
        score += 1.0     # halved from 2.0
        reasons.append("genre match (+1.0, halved)")
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
    target_energy = user_prefs.get('energy', 0.5)
    energy_score = 2.0 * (1.0 - abs(song['energy'] - target_energy))  # doubled
    score += energy_score
    reasons.append(f"energy similarity x2 (+{energy_score:.2f})")
    if user_prefs.get('likes_acoustic') and song['acousticness'] > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")
    return score, reasons


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Prints a formatted recommendation list for one user profile."""
    print("=" * 60)
    print(f" Profile: {profile_name}")
    print(f"   genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs['likes_acoustic']}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)

    if not recommendations:
        print("  No recommendations found.\n")
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score : {score:.2f} / 4.50")
        print(f"     Why   : {explanation}")
        print()


def print_experiment(songs: list, user_prefs: dict) -> None:
    """Runs the weight-shift experiment for the Happy Pop Fan profile."""
    print("=" * 60)
    print(" EXPERIMENT: Genre weight halved, Energy weight doubled")
    print(" (Happy Pop Fan profile)")
    print("=" * 60)
    scored = []
    for song in songs:
        score, reasons = score_song_experiment(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    scored.sort(key=lambda x: x[1], reverse=True)
    for rank, (song, score, explanation) in enumerate(scored[:5], start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.csv')
    songs = load_songs(csv_path)
    print(f"\nCatalog size: {len(songs)} songs\n")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)

    # Phase 4 weight-shift experiment
    print_experiment(songs, PROFILES["Happy Pop Fan"])


if __name__ == "__main__":
    main()