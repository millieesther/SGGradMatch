# SGGradMatch

SGGradMatch is a course-project prototype that recommends three programmes from a curated catalogue of 21 technology, AI, data, analytics and quantitative master's programmes at NUS, NTU and SMU. It combines deterministic constraints with local TF-IDF retrieval and an optional OpenAI explanation layer.

The system provides programme-fit decision support. It does not predict admission and does not replace the universities' formal assessment.

## Product at a glance

- **Persona:** an international student, early-career professional or career switcher comparing technology-related master's programmes in Singapore
- **Input:** academic background, career goal, interests, budget, study mode, duration and work experience
- **Output:** a grounded Top 3 with fit reasons, warnings, official links and verification dates, or an abstention when too few options remain
- **Method:** deterministic constraints followed by rule-only or hybrid TF-IDF ranking; an optional hosted model explains but does not select results

See [`docs/product_documentation.md`](docs/product_documentation.md) for the complete persona, input, output, architecture and target-versus-reached metrics.

## What is included

- 21 programme records with official source URLs and verification dates
- rule-only baseline
- hybrid rule and retrieval ranking
- grounded template explanations that work offline
- optional OpenAI Structured Output explanations
- dependency-free command-line interface and local web demo
- six development profiles and 30 completed author-reviewed test profiles
- repeatable evaluation script and results
- standard-library unit tests
- data dictionary, architecture and limitations documentation

## Quick start

Python 3.10 or later is required.

After downloading or cloning the repository, open Terminal in the repository root. On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
sggradmatch examples/student_profile.json
```

The command-line demo can also run without installing the package:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sggradmatch.cli examples/student_profile.json
```

If the computer exposes Python as `python` rather than `python3`, replace `python3` in these commands with `python`.

## Run the web demo

The default offline web demo needs no API key or external service. From the repository root, run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sggradmatch.webapp
```

A successful start displays:

```text
SGGradMatch running at http://127.0.0.1:8000
```

Keep this Terminal window open. In a regular Chrome or Safari window, manually open:

```text
http://localhost:8000/
```

Use `http://`, not `https://`. Enter a profile and select **Generate recommendations**. The page returns a grounded Top 3 or an abstention when fewer than two programmes remain. Stop the server by returning to Terminal and pressing `Control+C`.

### Web demo troubleshooting

- If the browser cannot connect, confirm that Terminal still shows the running server and has not returned to the command prompt.
- Try `http://127.0.0.1:8000/` if `localhost` does not open.
- If the browser shows an older interface, press `Command+Shift+R` on macOS or `Ctrl+Shift+R` on Windows/Linux.
- If Terminal reports that port 8000 is already in use, stop the earlier server with `Control+C` before restarting it.
- Do not open the address through an HTTPS-only preview. Use a normal local browser window.

## Compare the baseline and hybrid method

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sggradmatch.cli examples/student_profile.json --method rule
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sggradmatch.cli examples/student_profile.json --method hybrid
```

## Optional OpenAI explanations

The ranking is fixed locally before the model is called. The model may explain the selected programmes but cannot replace their IDs.

```bash
cp .env.example .env
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-6-luna"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sggradmatch.cli examples/student_profile.json --use-openai
```

Never commit `.env` or an API key. The request uses `store: false` and Structured Outputs. Model access and pricing depend on the API account and may change.

## Validation and tests

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/validate_data.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m json.tool eval/results/evaluation_results.json >/dev/null
```

The repository contains 11 automated tests. The third command checks that the submitted final evaluation file is valid JSON without rerunning the frozen benchmark.

Final second-pass self-evaluation results (30 author-reviewed profiles):

| Method | Profile Success Rate@3 | Precision@3 | Known constraint violation rate |
|---|---:|---:|---:|
| Rule-only | 0.9667 | 0.9333 | 0.0000 |
| Hybrid | 1.0000 | 0.9667 | 0.0000 |

These values use a completed rubric-based second pass by the project author. They are self-evaluation results, not independent performance evidence; no weights or labels were changed after the final run.

To reproduce the deterministic benchmark, optionally run the following command. It rewrites `eval/results/evaluation_results.json`, so it is not required to launch or inspect the submitted demo.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 eval/run_evaluation.py
```

## Important evaluation note

The bundled ground-truth file contains the completed second-pass labels created by the project author. The review froze the catalogue and weights, hid existing labels and predictions, applied the written rubric, recorded every change, and ran the benchmark once. See `eval/solo_review_change_log_zh.md`; the result remains author-labelled rather than independent ground truth.

## Data maintenance

University fees, deadlines and admission requirements change. The submitted dataset is frozen at 2 October 2026 and records unknown values rather than inferring them. For future reuse after submission:

1. revisit every URL in `data/sources/source_registry.csv`;
2. update changed values and `last_verified_at`;
3. leave unpublished fields blank;
4. rerun validation and tests;
5. create a new evaluation version rather than silently replacing the submitted frozen result; and
6. report the updated catalogue date and scope.

## Repository structure

```text
data/       curated programme data and source registry
docs/       architecture, data dictionary, report and limitations
eval/       profiles, author-reviewed labels, evaluation code and results
examples/   runnable student profile
scripts/    dataset validation
src/        application source code
tests/      unit tests
```

## Documentation map

- [`data/README.md`](data/README.md): data scope, provenance, missing values, validation and refresh process
- [`eval/README.md`](eval/README.md): methods, metric definitions, current results and single-author review procedure
- [`docs/product_documentation.md`](docs/product_documentation.md): persona, input, output, architecture and metrics
- [`docs/architecture.md`](docs/architecture.md): compact transformation diagram
- [`docs/experiment_log.md`](docs/experiment_log.md): baseline, hybrid weights and tuning decisions
- [`docs/pre_demo_checklist.md`](docs/pre_demo_checklist.md): completed work and remaining human checks
- [`docs/solo_review_guide_zh.md`](docs/solo_review_guide_zh.md): Chinese source-audit and single-author labeling guide with all 21 official programme links
- [`docs/data_dictionary.md`](docs/data_dictionary.md): field definitions
- [`docs/limitations.md`](docs/limitations.md): known product and evidence limits
- [`docs/project_report.md`](docs/project_report.md): concise pre-demo final report

## Responsible use

- no admission probability or guarantee
- no collection of names, contact details, passport data or transcripts
- hard constraints are applied before semantic ranking
- missing fees and durations remain unknown and generate warnings
- all recommendations link to an official university source
- the system abstains when fewer than two programmes remain
