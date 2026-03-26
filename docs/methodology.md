# Cyber Risk Copilot – Methodology\

## 1. Overview
Cyber Risk Copilot uses a rule-based scoring model to evaluate cybersecurity risk across multiple categories and generate prioritized recommendations. The methodology is designed to be transparent, explainable, and configurable.

The framework maps organizational characteristics (inputs) to risk categories, computes weighted scores, normalizes those scores, and derives prioritized actions aligned with established cybersecurity standards.

---

## 2. Risk Categories
The model evaluates risk across the following categories:

- Identity and Access Risk
- Email and Phishing Risk
- Endpoint and Device Risk
- Data Protection and Backup Risk
- Incident Readiness
- Governance and Compliance

Each category represents a distinct area of cybersecurity risk relevant to small and medium-sized organizations.

---

## 3. Scoring Model

### 3.1 Weighted Risk Scoring

Each risk category score is computed using a weighted sum of contributing factors:

\[
Score(c) = \sum_{i=1}^{n} w_i \cdot f_i
\]

Where:
- \( c \) = risk category
- \( w_i \) = weight assigned to factor \( i \)
- \( f_i \) = contribution of factor \( i \) based on scenario inputs

Weights are defined in an external configuration file (`weights.yaml`), allowing the model to remain flexible and easily adjustable.

---

### 3.2 Factor Contributions

Each input factor contributes to one or more categories. Examples include:

- Data sensitivity → increases data protection and backup risk
- IAM maturity → influences identity and access risk
- Logging maturity → impacts incident readiness
- Compliance requirements → affect governance and compliance risk

Factor contributions are explicitly recorded to provide explainability for each score.

---

## 4. Score Normalization

To allow comparison across categories, raw scores are normalized:

\[
NormalizedScore(c) = \frac{Score(c)}{MaxScore(c)} \times S
\]

Where:
- \( MaxScore(c) \) = maximum possible score for category \( c \)
- \( S \) = scaling factor (default = 10)
This ensures all categories are comparable on a consistent scale.

---

## 5. Prioritization Strategy

Risk categories are ranked based on their normalized scores. The top three categories are selected as the primary focus areas.

Recommendations are then generated based on these categories and grouped into phases:

- Phase 1: Immediate actions (high impact, low complexity)
- Phase 2: Intermediate improvements
- Phase 3: Advanced or longer-term controls

---

## 6. Explainability

For each category, the model provides a breakdown of contributing factors:

Example:
- +3 data_sensitivity = high
- +2 backup_maturity = basic
- +1 payment_processing = true

This allows users to understand why a category was prioritized, making the model transparent and auditable.

---

## 7. Standards Alignment

All recommendations are mapped to:

- NIST Cybersecurity Framework (CSF)
- CIS Controls v8

This ensures that prioritization decisions are aligned with widely accepted cybersecurity standards and best practices.

---

## 8. Design Principles

The framework is guided by the following principles:

- Explainability over complexity
- Configurability over hardcoded logic
- Prioritization over exhaustive coverage
- Practicality for resource-constrained organizations

---

## 9. Limitations

- The model uses rule-based logic rather than machine learning
- Weight selection is heuristic and requires calibration
- The framework does not directly measure real-world risk reduction 
These limitations are addressed through evaluation, sensitivity analysis, and practitioner feedback.
