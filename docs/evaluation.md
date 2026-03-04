# Cyber Risk Copilot – Evaluation Plan (V1 → V2)

## 1. Evaluation goal
The objective of evaluation is to determine whether Cyber Risk Copilot produces (a) reasonable risk prioritization and (b) actionable, scenario-appropriate recommendations for resource-constrained SMEs. Because the tool is decision-support (not a real-time detection system), evaluation focuses on validity of prioritization and perceived utility, rather than direct measurement of breach reduction.

## 2. Scenario-based evaluation dataset
The tool will be evaluated across multiple realistic SME profiles represented as structured JSON scenarios (e.g., healthcare, fintech, ecommerce, agriculture). Each scenario includes organizational, technical, and security posture inputs.

For each scenario, the tool outputs:
- raw category scores
- normalized category scores (0–10)
- top 3 prioritized risk categories
- phased action plan (Phase 1/2/3)
- explainability trace (reason breakdown per category)

## 3. Baseline comparison
To demonstrate utility beyond generic guidance, Cyber Risk Copilot will be compared to a baseline approach:

**Baseline A (Generic checklist baseline):**
- A fixed “starter set” of controls (e.g., general best practices) applied equally to every scenario.

**Comparison method:**
- Measure whether Cyber Risk Copilot produces scenario-specific prioritization (changes in top categories and actions across scenarios).
- Qualitatively assess whether Copilot recommendations are more tailored than baseline.

Outcome:
- Evidence that the model adapts recommendations to context, rather than outputting a static checklist.

## 4. Sensitivity and stability analysis
To test robustness, weights will be varied within a defined range (e.g., ±20% for key weights such as IAM maturity, backup maturity, data sensitivity). The analysis will measure:

- Stability of the top 3 ranked categories under weight perturbation
- Frequency of rank-order changes
- Identification of “swing factors” that cause major prioritization shifts

Outcome:
- Evidence that the model is not overly fragile and that changes in recommendations are explainable.

## 5. Practitioner validation (optional but recommended)
If feasible, a small set of practitioners (e.g., 3–5 IT/security professionals) will be asked to review selected scenarios and rank top priorities.

Protocol:
- Provide 2–3 fictional SME scenarios and the tool’s top actions.
- Ask practitioners to:
  1) rank their top 5 actions for the first 30 days
  2) identify disagreements with the tool output
  3) indicate which factors should weigh more and why

Metrics:
- Overlap@5: how many actions match between practitioner and tool top-5
- Qualitative feedback themes (e.g., missing controls, wrong ordering, unclear assumptions)

Outcome:
- Evidence that recommendations align with practitioner expectations and highlight areas for calibration.

## 6. Reporting evaluation results
Evaluation results will be summarized in tables and short narrative analysis:
- Scenario → Top categories → Phase 1 actions
- Baseline vs Copilot differences
- Sensitivity findings
- Practitioner alignment results (if performed)

## 7. Limitations
- Scenario-based evaluation cannot directly measure real-world breach reduction.
- Practitioner feedback may be limited in sample size.
- The model emphasizes explainability and prioritization rather than complete coverage of all security controls.
