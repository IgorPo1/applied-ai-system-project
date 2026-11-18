"""
Guardrails for VibeFinder 2.0.

Provides input validation and output confidence scoring so the recommender
can surface warnings rather than silently returning poor results.

Functions
---------
validate_user_profile  -- check that a user prefs dict is well-formed
confidence_score       -- convert a raw recommendation score to 0-1 confidence
flag_low_confidence    -- return warning strings for weak recommendations
"""

from typing import Dict, List, Tuple


def validate_user_profile(user_prefs: Dict) -> Tuple[bool, List[str]]:
    """
    Validate a user preference dictionary before passing it to the recommender.

    Checks:
    - 'genre' is a non-empty string
    - 'mood' is a non-empty string
    - 'energy' is a float or int in [0.0, 1.0]

    Returns
    -------
    (is_valid, errors)
        is_valid : bool  -- True when all checks pass
        errors   : list  -- Human-readable error messages (empty when valid)
    """
    errors: List[str] = []

    genre = user_prefs.get("genre", "")
    if not isinstance(genre, str) or not genre.strip():
        errors.append("'genre' must be a non-empty string (e.g. 'pop', 'rock', 'lofi')")

    mood = user_prefs.get("mood", "")
    if not isinstance(mood, str) or not mood.strip():
        errors.append("'mood' must be a non-empty string (e.g. 'happy', 'chill', 'intense')")

    energy = user_prefs.get("energy")
    if energy is None:
        errors.append("'energy' is required (float between 0.0 and 1.0)")
    elif not isinstance(energy, (int, float)):
        errors.append(f"'energy' must be a number, got {type(energy).__name__!r}")
    elif not (0.0 <= float(energy) <= 1.0):
        errors.append(f"'energy' must be between 0.0 and 1.0, got {energy}")

    return (len(errors) == 0, errors)


def confidence_score(score: float, max_score: float = 4.0) -> float:
    """
    Convert a raw recommendation score into a 0.0–1.0 confidence value.

    Parameters
    ----------
    score     : raw score returned by score_song (0.0–max_score)
    max_score : theoretical maximum score (default 4.0 for genre+mood+energy)

    Returns
    -------
    float in [0.0, 1.0] representing how confidently this song was recommended
    """
    if max_score <= 0:
        return 0.0
    return round(min(max(score / max_score, 0.0), 1.0), 3)


def flag_low_confidence(
    recommendations: List[Tuple],
    threshold: float = 0.5,
    max_score: float = 4.0,
) -> List[str]:
    """
    Scan a list of (song_dict, score, explanation) tuples and return warning
    strings for any recommendation whose confidence is below *threshold*.

    Parameters
    ----------
    recommendations : list of (song, score, explanation) from recommend_songs
    threshold       : confidence below this value triggers a warning (default 0.5)
    max_score       : theoretical max score used to compute confidence

    Returns
    -------
    list of warning strings (empty if all recommendations meet the threshold)
    """
    warnings: List[str] = []
    for rank, (song, score, _explanation) in enumerate(recommendations, start=1):
        conf = confidence_score(score, max_score)
        if conf < threshold:
            title = song.get("title", "Unknown") if isinstance(song, dict) else getattr(song, "title", "Unknown")
            warnings.append(
                f"  [WARN] Rank #{rank} '{title}' - low confidence ({conf:.0%});"
                " this song has weak feature alignment with your profile."
            )
    return warnings