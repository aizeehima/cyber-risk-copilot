# Cyber Risk Copilot – Evaluation Plan

## 1. Evaluation Goal
The goal of evaluation is to determine whether Cyber Risk Copilot produces reasonable, explainable, and useful cybersecurity prioritization for small and medium-sized organizations. Since the system is a decision-support framework rather than a real-time security tool, evaluation focuses on the quality, relevance, and stability of the recommendations rather than direct measurement of breach reduction.

## 2. Evaluation Questions
The evaluation is designed to answer the following questions:

1. Does the framework produce different priorities for different organizational scenarios?
2. Are the recommended actions aligned with established cybersecurity standards?
3. Are the results stable when scoring weights are adjusted?
4. Do practitioners consider the recommendations reasonable and useful?

## 3. Evaluation Components

### 3.1 Scenario-Based Evaluation
The framework will be evaluated using multiple structured SME scenarios represented as JSON profiles. These scenarios vary by industry, compliance exposure, organizational size, technical environment, and security maturity.

Current scenario set includes:
- healthcare
- fintech
- ecommerce
- prediction market
- agriculture

For each scenario, the framework produces:
- raw category scores
- normalized category scores
- top 3 prioritized risk categories
- phased recommendations
- explainability traces
- NIST CSF and CIS Controls mappings

### 3.2 Baseline Comparison
To demonstrate that Cyber Risk Copilot adds value beyond a generic checklist, the framework will be compared against a static baseline.

#### Baseline Definition
The baseline approach will apply the same generic best-practice priorities to all scenarios, without adapting to organizational context.

Example baseline:
- Enable MFA
- Improve backups
- Patch systems
- Train users on phishing
- Centralize logs

#### Comparison Goal
The purpose of this comparison is to show that Cyber Risk Copilot:
- adapts recommendations to scenario-specific context
- changes the ordering of priorities depending on risk profile
- provides more targeted recommendations than a one-size-fits-all checklist

### 3.3 Sensitivity Analysis
Because the framework relies on weighted scoring, sensitivity analysis will be used to assess how stable the recommendations remain when the weights are adjusted.

The plan is to vary selected high-impact weights (for example IAM maturity, data sensitivity, backup maturity, and compliance pressure) by a fixed percentage, such as ±20%, and observe:

- whether the top 3 risk categories remain stable
- which categories are most sensitive to weight changes
- whether recommendation shifts are reasonable and explainable

This helps determine whether the framework is robust or overly dependent on specific weight settings.

### 3.4 Practitioner Validation
If feasible, a small number of security practitioners will be asked to review selected scenarios and compare their own priorities to the framework output.

Practitioners will be asked:
- what their top priorities would be for the first 30 days
- whether they agree with the framework’s top categories
- which factors they believe should weigh more heavily

The purpose of practitioner validation is not to prove perfect correctness, but to assess whether the framework’s recommendations are reasonable and aligned with real-world security judgment.

## 4. Evaluation Metrics

### 4.1 Differentiation Across Scenarios
Measure whether different scenarios produce different prioritized categories and action plans.

### 4.2 Standards Traceability
Verify that generated actions map to relevant NIST CSF categories and CIS Controls.

### 4.3 Stability Under Weight Variation
Measure whether top-priority categories remain consistent when weights are adjusted within a reasonable range.

### 4.4 Practitioner Agreement
If practitioner feedback is collected, compare framework output with practitioner-ranked priorities using:
- overlap in top actions
- qualitative agreement/disagreement themes
- perceived usefulness

## 5. Expected Evaluation Output
The final evaluation section of the project will include:
- scenario-by-scenario results
- comparison with the baseline approach
- summary of sensitivity findings
- summary of practitioner feedback (if available)
- discussion of strengths, limitations, and future refinements

## 6. Limitations
This evaluation does not directly measure real-world reduction in cyber incidents. Instead, it evaluates whether the framework provides explainable, standards-aligned, and context-sensitive prioritization. Because the framework is intended as a decision-support tool, usefulness and alignment are more appropriate evaluation targets than direct operational effectiveness at this stage.
