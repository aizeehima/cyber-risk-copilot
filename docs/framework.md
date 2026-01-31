# Cyber Risk Copilot – Framework Design

## 1. Overview
The Cyber Risk Copilot is a lightweight decision-support framework designed to help small and medium-sized organizations prioritize cybersecurity actions based on organizational context, exposure, and resource constraints. The framework emphasizes transparency and explainability by using explicit rules and scoring logic rather than opaque automation.

## 2. Model Inputs
The framework evaluates organizational risk using a structured set of inputs. To keep scoring practical and repeatable, inputs are normalized to simple values where possible (e.g., yes/no, low/medium/high, or small sets of categories).

### Organizational Profile
- Organization size (micro / small / medium)
- Industry type
- Number of users
- Compliance pressure (low / medium / high)
- Regulatory environment (e.g., HIPAA, PCI-DSS, GDPR, NDPR)

### Technical Environment
- IT environment (on-prem / cloud / hybrid)
- Cloud email platform (Microsoft 365 / Google Workspace / other)
- Remote access usage (yes / no)
- Endpoint management maturity (managed / unmanaged)
- Network architecture maturity (optional)

### Security Posture
- IAM maturity (e.g., MFA coverage, SSO adoption, privileged access practices)
- Data sensitivity (low / medium / high)
- Data classification / protection maturity (basic / moderate / strong)
- Backup maturity (optional)
- Logging / monitoring maturity (optional)

### Business Exposure
- Payment processing (yes / no)
- Customer data volume (low / medium / high)
- Third-party vendor dependency (optional)

## 3. Risk Categories
Based on the inputs, the framework evaluates risk across the following categories:
- Identity and access risk
- Email and phishing risk
- Endpoint and device risk
- Data protection and backup risk
- Incident response readiness
- Governance and compliance risk

## 4. Scoring Logic
Each input contributes to one or more risk categories using a rule-based scoring approach. Risk scores are calculated by assigning weights to input factors and aggregating their contributions within each category. Higher scores indicate higher relative risk and higher prioritization.

## 5. Prioritization Strategy
Risk categories are ranked based on their aggregated scores. Cybersecurity actions are mapped to the highest-risk categories and grouped into phased recommendations:
- Phase 1: Immediate actions (highest risk, lowest effort)
- Phase 2: Near-term improvements
- Phase 3: Longer-term enhancements

## 6. Standards Mapping
Recommended actions are mapped to relevant functions and categories within the NIST Cybersecurity Framework (CSF) and corresponding CIS Critical Security Controls (v8) to ensure alignment with established best practices.

## 7. Design Principles
The framework is guided by the following principles:
- Simplicity over completeness
- Explainability over automation
- Prioritization over exhaustive coverage
- Practicality for resource-constrained organizations
