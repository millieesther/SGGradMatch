# Evaluation explainer

## Evaluation question

The benchmark tests whether the hybrid rule-and-retrieval method produces a more relevant Top 3 than the rule-only baseline while maintaining zero known hard-constraint violations. Both methods use the same programme catalogue, profiles and constraint engine.

## Files

- `dev_profiles.jsonl` contains six profiles used during development.
- `test_profiles.jsonl` contains 30 fixed benchmark profiles.
- `ground_truth.jsonl` maps each test profile to a set of suitable programme IDs.
- `solo_review_template.csv` contains the completed second-pass review and reasons.
- `solo_review_change_log_zh.md` records every change from the seed labels.
- `suitability_rubric.md` defines the fixed inclusion rule for that pass.
- `run_evaluation.py` runs both ranking methods and calculates the metrics.
- `results/evaluation_results.json` stores aggregate metrics and per-profile outcomes.

Each profile varies academic background, career goal, interests, tuition limit, study mode, duration and experience. The checked-in labels are the completed rubric-based second pass. Because the project author also performed the review, they remain self-evaluation judgements rather than independent ground truth.

## Compared methods

The rule-only baseline applies the same hard constraints as the hybrid system and then scores interest overlap at 0.8 and academic-background overlap at 0.2.

The hybrid method first applies the hard constraints and then combines local TF-IDF retrieval relevance at 0.7, interest overlap at 0.2 and background overlap at 0.1. These weights were fixed before the current test run. They were selected through limited development comparison rather than an exhaustive search.

## Metrics

**Profile Success Rate at 3** is the fraction of test profiles for which at least two of the three returned programme IDs appear in the profile's suitable-programme set.

**Precision at 3** is the number of returned programme IDs in the suitable-programme sets divided by the total number returned.

**Known hard-constraint violation rate** is the fraction of returned programmes that fail the deterministic check for study mode, known tuition or known duration. An unknown catalogue value cannot be counted as a violation, so this metric does not establish real-world affordability when tuition is blank.

## Targets and current result

| Metric | Target | Rule only | Hybrid |
|---|---:|---:|---:|
| Profile Success Rate at 3 | at least 0.80 | 0.9667 | 1.0000 |
| Precision at 3 | at least 0.75 | 0.9333 | 0.9667 |
| Improvement in Profile Success Rate | at least 0.15 | reference | 0.0333 |
| Known hard-constraint violation rate | 0.00 | 0.0000 | 0.0000 |

The results show that the software distinguishes the two ranking methods and respects stored constraints. The hybrid method did not meet the planned 15-percentage-point improvement target: its success-rate gain was 3.33 percentage points. These are final second-pass author-reviewed self-evaluation results, not independent performance evidence. No weights or labels were changed after this run.

## Reproduce the benchmark

From the repository root, run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python eval/run_evaluation.py
```

The command rewrites `results/evaluation_results.json`. Each method's `cases` list records the recommendations, number of hits and success status for every profile, which supports failed-case review.

## Completed single-author review protocol

The same person built the system and labelled the benchmark. This completed protocol improves separation between development and evaluation but does not create independent ground truth.

1. Write and freeze the suitability rubric before opening the review template.
2. Freeze the code, ranking weights and 30 test profiles.
3. Move the current `ground_truth.jsonl` and evaluation result out of view during labeling.
4. Review `test_profiles.jsonl`, the catalogue and data dictionary in profile order, without running either ranking method.
5. Record all suitable programme IDs in `solo_review_template.csv` and complete all 30 rows before comparison.
6. Compare the second pass with the seed labels and log every change with a reason such as factual correction, inconsistent rubric application or transcription error.
7. Freeze the revised ground-truth file, run the benchmark once and do not tune on the final test result.
8. Update the report and identify the numbers as author-labelled self-evaluation.

## Limitations

The benchmark is small and uses constructed profiles. The same author created the system, profiles and relevance labels, so confirmation bias cannot be removed. Relevance is subjective, and a reasonable programme may be absent from the label set. The labels do not measure admission probability, explanation quality, source freshness or whether a real user completes shortlisting faster. The final report should present these as self-evaluation results and pair them with a source audit and failed-case analysis.
