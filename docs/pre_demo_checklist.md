# Pre-demo checklist

## Completed in the repository

- [x] Twenty-one programme records with official source URLs and verification dates
- [x] Rule-only baseline and hybrid retrieval implementation
- [x] Offline recommendation path and optional hosted-model explanation path
- [x] Command-line interface and local web demo
- [x] Data validator and eleven automated tests
- [x] Thirty-profile evaluation pipeline with per-case output
- [x] Data, evaluation, product, architecture, tuning and limitation explainers
- [x] Module-level documentation for application, evaluation and validation code
- [x] Pre-demo final report within the permitted word range

## Completed human checks

- [x] Reopened all 21 official source URLs and froze `last_verified_at` at 2026-10-02
- [x] Froze the code, scoring weights and 30 test profiles before final evaluation
- [x] Hid the existing labels and predictions during the second labeling pass
- [x] Applied the written suitability rubric to all 30 profiles
- [x] Recorded all 153 additions and 25 deletions with reasons
- [x] Replaced the seed labels only after completing the full second pass
- [x] Passed catalogue validation and all eleven automated tests
- [x] Completed one effective final evaluation without later tuning
- [x] Updated the reached metrics in the report, README and product documentation
- [x] Reviewed the per-profile evaluation output; Hybrid had no failed profiles and Rule-only had one
- [x] Rechecked recommendation evidence against the 21 official programme sources

## Optional single author timing check

- [ ] Select two matched profiles not used for tuning
- [ ] Time a manual shortlist for one profile and a tool-assisted shortlist for the other
- [ ] Record the procedure and treat the result as a workflow smoke test, not a user study

The timing check remains optional and is not included in the reported performance claims.

## Final technical check

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/validate_data.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
python -m json.tool eval/results/evaluation_results.json >/dev/null
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m sggradmatch.cli examples/student_profile.json --method hybrid
```

Do not rerun the frozen benchmark during the recording check. Inspect the stored final result instead so the repository preserves the documented single effective final run.

Start the local demo with:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m sggradmatch.webapp
```

Open `http://127.0.0.1:8000` and test both a normal case and an abstention case before recording.
