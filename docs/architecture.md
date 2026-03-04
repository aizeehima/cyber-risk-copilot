# Cyber Risk Copilot – System Architecture

```mermaid
flowchart LR
  A[Scenario JSON Profiles<br/>data/scenarios/*.json] --> B[Scenario Parser<br/>Scenario.from_dict]
  B --> C[Risk Scoring Engine<br/>score_scenario(cfg)]
  C --> D[Explainability Trace<br/>reasons per category]
  C --> E[Normalization<br/>normalize_scores(max_scores)]
  E --> F[Prioritization<br/>ranked categories (Top 3)]
  F --> G[Recommendation Generator<br/>Phase 1/2/3 actions]
  G --> H[Standards Mapper<br/>NIST CSF + CIS Controls]
  H --> I[Outputs<br/>CLI report / JSON report]
  I --> J[Evaluation Layer<br/>baseline + sensitivity + practitioner review]
