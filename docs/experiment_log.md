# Experiment and tuning log

## Baseline

The first comparison method applies the same hard constraints as the final system and ranks eligible programmes with a weighted overlap score. Interest and career-goal overlap contributes 0.8, while academic-background overlap contributes 0.2. This provides a reproducible non-retrieval baseline.

## Hybrid configuration

The hybrid method adds local TF-IDF relevance across programme domains, curriculum and career outcomes. Its fixed weights are:

- retrieval relevance 0.7;
- interest and career overlap 0.2; and
- academic-background overlap 0.1.

The development workflow favoured retrieval because open-text career goals contain more information than a short background label. The weights were fixed before the current 30-profile test run. No exhaustive grid search or test-set optimisation was performed.

## Current comparison

| Method | Success Rate at 3 | Precision at 3 | Known violations |
|---|---:|---:|---:|
| Rule only | 0.9667 | 0.9333 | 0.0000 |
| Hybrid | 1.0000 | 0.9667 | 0.0000 |

The hybrid method improved both relevance metrics, but its 0.0333 increase in success rate did not meet the 0.15 target. These are the final second-pass author-reviewed self-evaluation results. The broad reviewed label sets and strong baseline may partly explain the small measured difference and high absolute scores.

## Final evaluation execution

The first attempted evaluation stopped before metric calculation because the reviewed label file used a field name that did not match the evaluation script's expected schema. The file structure was corrected without changing the reviewed label sets, programme data, ranking weights or code logic. The frozen benchmark then completed once and produced the results above. No label or weight changed after that effective run.

## Decisions retained

- Keep hard filtering identical across methods so the ranking comparison is fair.
- Keep the language model outside ranking so repeated evaluation remains deterministic.
- Keep an offline explanation path so API availability does not affect the demo.
- Represent missing programme values explicitly instead of imputing them.

## Post-test rule

Do not tune weights or labels on the frozen test results. Any later experiment must use the development profiles or a newly defined benchmark and must report its results separately from this final run.
