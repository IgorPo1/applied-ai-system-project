# VibeFinder 2.0 - Evaluation Results

Run with: `python -m src.evaluator`

| # | Test Profile | Input | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|
| 1 | High-Energy Pop Fan | genre='pop', mood='happy', energy=0.8 | valid | top genre=pop | score>=3.5 | valid | top genre=pop | score=3.98 | **PASS** |
| 2 | Chill Lofi Listener | genre='lofi', mood='chill', energy=0.35 | valid | top genre=lofi | score>=3.9 | valid | top genre=lofi | score=4.00 | **PASS** |
| 3 | Intense Rock Head | genre='rock', mood='intense', energy=0.9 | valid | top genre=rock | score>=3.5 | valid | top genre=rock | score=3.99 | **PASS** |
| 4 | Jazz Relaxed Fan | genre='jazz', mood='relaxed', energy=0.37 | valid | top genre=jazz | score>=3.5 | valid | top genre=jazz | score=4.00 | **PASS** |
| 5 | Edge Case: Conflicting Prefs (high energy + sad mood) | genre='rock', mood='sad', energy=0.95 | valid | top genre=rock | score>=2.0 | valid | top genre=rock | score=2.96 | **PASS** |
| 6 | INVALID: Energy out of range (1.5) | genre='pop', mood='happy', energy=1.5 | guardrail blocks (invalid) | blocked | **PASS** |
| 7 | INVALID: Empty genre string | genre='', mood='chill', energy=0.4 | guardrail blocks (invalid) | blocked | **PASS** |
| 8 | INVALID: Missing energy key | genre='lofi', mood='chill', energy=<missing> | guardrail blocks (invalid) | blocked | **PASS** |

**Summary:** 8 out of 8 tests passed.
