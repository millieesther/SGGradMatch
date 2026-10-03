# Suitability labeling rubric

## Purpose

Use this rubric for the author's second labeling pass. Apply it to every programme for every test profile without viewing the system's rankings or existing labels.

## Step one check known constraints

Exclude a programme when the catalogue contains a known conflict with the profile's required study mode, maximum tuition or maximum duration.

Do not exclude a programme solely because tuition or duration is blank. Mark the uncertainty in the review notes.

## Step two score relevance

Score each eligible programme using the catalogue fields only.

| Criterion | Score |
|---|---:|
| Career goal directly matches a listed outcome or central programme domain | 2 |
| Career goal is adjacent but not central | 1 |
| Career goal has no meaningful support | 0 |
| Two or more interests match programme domains or curriculum | 2 |
| One interest matches | 1 |
| No interest matches | 0 |
| Background appears in the programme guidance or the guidance accepts broad backgrounds | 1 |
| Background support is unclear | 0 |

Label a programme suitable when the total relevance score is at least 3 and there is no known hard-constraint conflict.

## Step three record judgement

Enter every suitable programme ID in `solo_review_template.csv`, separated by `|`. Do not limit the label set to three programmes. Use `author_review_notes` for unknown constraints or borderline decisions.

Complete all 30 profiles before comparing the second pass with `ground_truth.jsonl`. Record any later correction and its reason; do not change a label merely because a system recommendation missed it.
