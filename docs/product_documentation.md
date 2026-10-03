# Product documentation

## Product purpose

SGGradMatch helps an international applicant form an initial shortlist from 21 selected Singapore master's programmes. It provides programme-fit decision support and does not predict admission.

## Persona

The primary persona is a final-year student, early-career professional or career switcher comparing technology-related programmes at NUS, NTU and SMU. The user knows their academic background, interests and constraints but may not know how programme terminology maps to a career goal.

An education adviser is a secondary persona who can use the output as a consistent first-pass shortlist before a detailed consultation.

## Input

The command-line interface accepts a JSON profile, while the local web interface accepts the same fields through a form:

| Field | Purpose |
|---|---|
| Academic background | Soft comparison with published background guidance |
| Career goal | Main retrieval and interest-matching query |
| Interests | Additional subject and career terms |
| Maximum tuition | Hard filter when a verified fee is available |
| Preferred study mode | Hard filter for full-time or part-time availability |
| Maximum duration | Hard filter when the selected mode's duration is known |
| Years of experience | Retained for explanation and future rules; not used as an admission decision |

The product does not request a name, email, passport number, transcript or application account.

## Output

For an eligible profile, the product returns three ranked programme records. Each record contains:

- programme ID, name and university;
- ranking score;
- reasons derived from constraints and matching signals;
- warnings for unknown or unresolved fields;
- official programme URL; and
- catalogue verification date.

The response states that programme fit is not an admission prediction. When fewer than two programmes survive hard filtering, the system abstains and asks the user to verify or relax a constraint.

## Product architecture

```text
Student JSON or web form
          |
          v
Input normalisation
          |
          v
Deterministic constraint checks
study mode, known tuition, known duration
          |
          v
Local TF-IDF retrieval and overlap scores
          |
          v
Rule-only or hybrid ranking
          |
          v
Fixed Top 3 programme IDs
          |
          +---------------------------+
          |                           |
          v                           v
Offline grounded template       Optional hosted LLM
                                      |
                               Structured explanation only
          |                           |
          +-------------+-------------+
                        v
Official sources, verification dates, warnings and disclaimer
```

The hosted language model is optional external intelligence. It receives only the fixed recommendations and may explain them; it does not choose programme IDs or bypass the constraint engine. No external tools are available to the model.

## Metrics targeted and reached

| Metric | Target | Current hybrid result | Status |
|---|---:|---:|---|
| Profile Success Rate at 3 | at least 0.80 | 1.0000 | Met on reviewed labels |
| Precision at 3 | at least 0.75 | 0.9667 | Met on reviewed labels |
| Improvement over rule-only success rate | at least 0.15 | 0.0333 | Not met |
| Known hard-constraint violation rate | 0.00 | 0.0000 | Met |
| Citation support rate | at least 0.95 | Not yet audited | Pending |
| Shortlisting-time reduction | at least 0.50 | Not yet tested | Pending |

The final results use completed second-pass labels reviewed by the project author. They are self-evaluation results, not independent performance claims, and no weights or labels were changed after the final run. See `eval/README.md` for the completed single-author protocol and limitations.

## Product boundaries

- Catalogue coverage is limited to 21 selected programmes.
- Missing tuition and duration remain unknown and generate warnings.
- Academic-background matching is a relevance signal, not an eligibility decision.
- The system does not provide scholarship, visa, immigration or application advice.
- Official university pages remain the source of truth.

## Run the product

See the repository `README.md` for installation, command-line, web-demo, test and evaluation commands.
