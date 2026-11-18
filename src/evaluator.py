"""
Evaluation harness for VibeFinder 2.0.

Runs a structured set of test cases against the recommender and guardrails,
then outputs a markdown-formatted pass/fail table and a summary line.

Run from project root:
    python -m src.evaluator
"""

try:
    from recommender import load_songs, recommend_songs
    from guardrails import validate_user_profile, confidence_score, flag_low_confidence
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs
    from src.guardrails import validate_user_profile, confidence_score, flag_low_confidence

# ---------------------------------------------------------------------------
# Test-case definitions
# Each case is a dict with:
#   profile_name    : human-readable label
#   user_prefs      : dict passed to validate_user_profile + recommend_songs
#   expected_valid  : True if the profile should pass input validation
#   expected_top_genre : genre string expected at rank #1 (ignored when invalid)
#   expected_min_score : minimum score expected for the #1 result (ignored when invalid)
#   description     : short note shown in the table
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "profile_name": "High-Energy Pop Fan",
        "user_prefs": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "expected_valid": True,
        "expected_top_genre": "pop",
        "expected_min_score": 3.5,
        "description": "Strong genre+mood+energy match should score >= 3.5",
    },
    {
        "profile_name": "Chill Lofi Listener",
        "user_prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35},
        "expected_valid": True,
        "expected_top_genre": "lofi",
        "expected_min_score": 3.9,
        "description": "Perfect lofi match should score >= 3.9",
    },
    {
        "profile_name": "Intense Rock Head",
        "user_prefs": {"genre": "rock", "mood": "intense", "energy": 0.9},
        "expected_valid": True,
        "expected_top_genre": "rock",
        "expected_min_score": 3.5,
        "description": "Rock genre should dominate top result",
    },
    {
        "profile_name": "Jazz Relaxed Fan",
        "user_prefs": {"genre": "jazz", "mood": "relaxed", "energy": 0.37},
        "expected_valid": True,
        "expected_top_genre": "jazz",
        "expected_min_score": 3.5,
        "description": "Jazz catalog has one matching song; should be top result",
    },
    {
        "profile_name": "Edge Case: Conflicting Prefs (high energy + sad mood)",
        "user_prefs": {"genre": "rock", "mood": "sad", "energy": 0.95},
        "expected_valid": True,
        "expected_top_genre": "rock",
        "expected_min_score": 2.0,
        "description": "No rock+sad song exists; top result is genre match only",
    },
    {
        "profile_name": "INVALID: Energy out of range (1.5)",
        "user_prefs": {"genre": "pop", "mood": "happy", "energy": 1.5},
        "expected_valid": False,
        "expected_top_genre": None,
        "expected_min_score": None,
        "description": "Guardrail must reject energy > 1.0",
    },
    {
        "profile_name": "INVALID: Empty genre string",
        "user_prefs": {"genre": "", "mood": "chill", "energy": 0.4},
        "expected_valid": False,
        "expected_top_genre": None,
        "expected_min_score": None,
        "description": "Guardrail must reject blank genre",
    },
    {
        "profile_name": "INVALID: Missing energy key",
        "user_prefs": {"genre": "lofi", "mood": "chill"},
        "expected_valid": False,
        "expected_top_genre": None,
        "expected_min_score": None,
        "description": "Guardrail must reject missing energy field",
    },
]


def run_evaluation(songs: list) -> list:
    """
    Execute every test case and return a list of result dicts.

    Each result dict contains:
        profile_name, description, input_summary, expected, actual, passed
    """
    results = []

    for case in TEST_CASES:
        prefs = case["user_prefs"]
        is_valid, errors = validate_user_profile(prefs)

        input_summary = (
            f"genre='{prefs.get('genre', '<missing>')}', "
            f"mood='{prefs.get('mood', '<missing>')}', "
            f"energy={prefs.get('energy', '<missing>')}"
        )

        if case["expected_valid"]:
            # Should pass guardrail and produce a sensible top result
            if not is_valid:
                results.append({
                    "profile_name": case["profile_name"],
                    "description": case["description"],
                    "input_summary": input_summary,
                    "expected": f"valid | top genre={case['expected_top_genre']}",
                    "actual": f"BLOCKED by guardrail: {'; '.join(errors)}",
                    "passed": False,
                })
                continue

            recs = recommend_songs(prefs, songs, k=1)
            top_song, top_score, _ = recs[0]
            top_genre = top_song.get("genre", "")
            genre_ok = (top_genre == case["expected_top_genre"])
            score_ok = (top_score >= case["expected_min_score"])
            passed = genre_ok and score_ok

            results.append({
                "profile_name": case["profile_name"],
                "description": case["description"],
                "input_summary": input_summary,
                "expected": f"valid | top genre={case['expected_top_genre']} | score>={case['expected_min_score']}",
                "actual": f"valid | top genre={top_genre} | score={top_score:.2f}",
                "passed": passed,
            })

        else:
            # Should be rejected by guardrail
            passed = (not is_valid)
            results.append({
                "profile_name": case["profile_name"],
                "description": case["description"],
                "input_summary": input_summary,
                "expected": "guardrail blocks (invalid)",
                "actual": "blocked" if not is_valid else "passed (UNEXPECTED)",
                "passed": passed,
            })

    return results


def print_markdown_table(results: list) -> None:
    """Print evaluation results as a markdown table to stdout."""
    print("## VibeFinder 2.0 - Evaluation Results\n")
    print("| # | Test Profile | Input | Expected | Actual | Pass/Fail |")
    print("|---|---|---|---|---|---|")

    for i, r in enumerate(results, start=1):
        status = "PASS" if r["passed"] else "FAIL"
        print(
            f"| {i} "
            f"| {r['profile_name']} "
            f"| {r['input_summary']} "
            f"| {r['expected']} "
            f"| {r['actual']} "
            f"| **{status}** |"
        )

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n**Summary:** {passed} out of {total} tests passed.\n")
    if passed < total:
        failed = [r["profile_name"] for r in results if not r["passed"]]
        print(f"**Failed tests:** {', '.join(failed)}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")
    results = run_evaluation(songs)
    print_markdown_table(results)

    # Also write to a file for the README evidence
    import os
    output_path = "evaluation_results.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# VibeFinder 2.0 - Evaluation Results\n\n")
        f.write("Run with: `python -m src.evaluator`\n\n")
        f.write("| # | Test Profile | Input | Expected | Actual | Pass/Fail |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, r in enumerate(results, start=1):
            status = "PASS" if r["passed"] else "FAIL"
            f.write(
                f"| {i} "
                f"| {r['profile_name']} "
                f"| {r['input_summary']} "
                f"| {r['expected']} "
                f"| {r['actual']} "
                f"| **{status}** |\n"
            )
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        f.write(f"\n**Summary:** {passed} out of {total} tests passed.\n")
        if passed < total:
            failed = [r["profile_name"] for r in results if not r["passed"]]
            f.write(f"\n**Failed tests:** {', '.join(failed)}\n")
    print(f"Results also written to: {output_path}")


if __name__ == "__main__":
    main()