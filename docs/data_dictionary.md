# Data dictionary

| Field | Meaning | Missing value rule |
| --- | --- | --- |
| `programme_id` | Stable repository identifier | Never missing |
| `university` | NUS, NTU or SMU | Never missing |
| `programme_name` | Official programme name | Never missing |
| `domains` | Search and matching tags separated by `|` | Never missing |
| `study_modes` | `full-time`, `part-time`, or both | Never inferred |
| `duration_ft_months` | Published or normal full-time duration | Blank when unclear |
| `duration_pt_months` | Published or normal part-time duration | Blank when unclear |
| `tuition_sgd` | Published total tuition figure | Blank when not verified |
| `academic_backgrounds` | Broad background guidance | Not treated as admission approval |
| `experience_note` | Work-experience or admissions caveat | Plain text |
| `curriculum` | Compact retrieval text based on official programme information | No invented modules |
| `career_outcomes` | Broad roles related to the curriculum | Decision support only |
| `source_url` | Official university page | Never missing |
| `last_verified_at` | Date on which the row was checked | ISO date |

