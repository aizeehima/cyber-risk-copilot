# Cyber Risk Copilot

A decision-support framework for cybersecurity risk prioritisation in small and medium-sized enterprises (SMEs).

## What it does

Cyber Risk Copilot ingests a structured organisational profile and produces:
- A normalised risk score across 6 cybersecurity categories
- A per-factor reasoning breakdown explaining every score
- A phased remediation plan (Phase 1 / 2 / 3) mapped to NIST CSF v2.0 and CIS Controls v8
- A sensitivity analysis showing how rankings change under input variation

## Risk categories

- Identity and Access Management
- Email and Phishing
- Endpoint and Device Security
- Data Protection and Backup
- Incident Readiness
- Governance and Compliance

## Scoring approach

Weights are grounded in published industry data including Verizon DBIR 2023, FBI IC3 Report 2023, NIST SP 800-30 Rev 1, and CIS RAM v2.1. Every weight is documented with a specific source and finding.

## Usage
```bash
# Setup
./run.sh setup

# Run scoring engine
python -m src.main

# Full report with NIST/CIS tags
python -m src.main --report

# With sensitivity analysis
python -m src.main --sensitivity

# With natural language narrative (requires Ollama)
python -m src.main --narrative
```

## Evaluation scenarios

9 SME profiles covering healthcare, fintech, ecommerce, legal, nonprofit, hospitality, agriculture, technology, and prediction market sectors.

## Research context

Master's thesis project — M.S. Cybersecurity, University of Georgia, 2026.

Supervisor: Dr. Kyu Lee, CSCI 7200
