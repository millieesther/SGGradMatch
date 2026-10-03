# Data explainer

## Purpose and scope

The catalogue supports the SGGradMatch course prototype. It contains 21 selected master's programmes: seven each from NUS, NTU and SMU. The selection covers artificial intelligence, computing, data science, analytics, fintech and adjacent quantitative programmes. It is a balanced demonstration dataset, not an exhaustive list of Singapore master's programmes.

## Files

- `processed/programmes.csv` is the application-ready catalogue.
- `sources/source_registry.csv` lists the official programme URL and verification date for every programme ID.
- `docs/data_dictionary.md` defines every field and its missing-value rule.

## Collection and provenance

Programme facts were manually curated from the official university pages recorded in the source registry. Each row has a stable repository ID and a `last_verified_at` date. The dataset does not copy application documents, student records or personal data.

The compact `domains`, `curriculum` and `career_outcomes` fields support retrieval. They summarise the relevant official programme information for matching; they are not admissions decisions or employment guarantees.

## Missing values

A blank tuition or duration value means that the value was not verified in a stable, comparable form. It does not mean zero. The constraint engine keeps a programme with an unknown value and adds a warning. It rejects a programme only when a known value conflicts with the user's limit.

This policy preserves potentially useful options, but it means that the reported constraint-violation metric covers known catalogue values only.

## Validation

Run the schema and balance checks from the repository root:

```bash
PYTHONPATH=src python scripts/validate_data.py
```

The validator checks required IDs, university balance, source URLs, verification dates, study modes and duplicate records.

## Refresh procedure

Before final submission or a recorded demo:

1. Open every URL in `sources/source_registry.csv`.
2. Confirm the programme still exists and check name, mode, duration, tuition and background guidance.
3. Update only information supported by the official page.
4. Leave an unclear or cohort-specific value blank and retain a warning.
5. Update `last_verified_at` for each reviewed row.
6. Rerun validation, unit tests and evaluation.

University information changes over time. This repository should therefore be described as a dated snapshot, with official pages remaining the source of truth.
