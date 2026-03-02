# Cyber Risk Copilot – Scoring Methodology (V1)

## 1. Why these risk categories?
The Cyber Risk Copilot scores risk across six categories that represent common control domains emphasized in widely used security frameworks (e.g., NIST CSF and CIS Controls) and in typical SME threat exposure:

- Identity and Access: account takeover, privilege misuse, weak authentication
- Email and Phishing: phishing-based initial access and business email compromise
- Endpoint and Device: malware/ransomware entry points and unmanaged devices
- Data Protection and Backup: impact severity and recoverability
- Incident Readiness: detection/response gaps and operational resilience
- Governance and Compliance: policy/ownership gaps and regulatory obligations

These categories are intended to be broad enough to cover most SME environments while remaining explainable and actionable.

## 2. How are weights determined?
In V1, scoring weights are derived using a simplified likelihood × impact framing inspired by standard risk assessment thinking:

- Factors that increase the probability of compromise primarily contribute to *likelihood* (e.g., weak IAM maturity, remote access exposure, unmanaged endpoints).
- Factors that increase severity of harm primarily contribute to *impact* (e.g., high data sensitivity, large customer data volume, payment processing).
- Factors that increase required control rigor contribute to *governance/compliance* (e.g., high compliance pressure, presence of regulatory obligations, high third-party dependency).

Weights are intentionally coarse-grained to keep the model transparent. For example, “high data sensitivity” is weighted higher because it increases the impact of a breach, while “remote access = yes” raises likelihood due to larger attack surface.

## 3. Weight calibration and refinement plan
V1 weights represent initial, explainable assumptions. In V2, weights will be refined using:
1) **Normalization** to ensure category scores are comparable (avoid bias from categories with more contributing factors).
2) **Sensitivity analysis** by varying key weights (e.g., ±20%) to measure stability of the top-ranked categories and recommendations.
3) **Optional expert elicitation** by asking practitioners to rank top risks and actions for each scenario, then adjusting weights to improve agreement with practitioner priorities.

## 4. Transparency and explainability
The model prints a reason breakdown for each category score (e.g., “+3 high data sensitivity” or “+2 remote access”). This makes the scoring auditable and easier to critique and improve.
