# Architecture

```text
Student JSON or web form
          |
          v
Input normalisation
          |
          v
Deterministic constraints
study mode, known tuition and known duration
          |
          v
Local TF-IDF retrieval
          |
          v
Hybrid score
semantic relevance, interest overlap and background overlap
          |
          v
Fixed Top 3 programme IDs
          |
          +---------------------------+
          |                           |
          v                           v
Offline grounded template       Optional OpenAI explanation
          |                           |
          +-------------+-------------+
                        v
Sources, verification dates, warnings and non-admission notice
```

The model never selects from the entire catalogue. Local code fixes the ranking first, and the optional model receives only the selected records. This reduces the chance that a fluent explanation changes the underlying decision.

