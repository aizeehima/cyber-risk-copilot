# Cyber Risk Copilot – Standards Mapping (NIST CSF + CIS Controls)

This document maps Cyber Risk Copilot recommendations to:
- NIST Cybersecurity Framework (CSF) functions/categories
- CIS Controls v8 (Control families)

## Mapping notes
- Mapping is approximate and intended to provide traceability, not a full compliance audit.
- If multiple mappings apply, the primary mapping is listed first.

---

## Identity & Access recommendations
**Enable MFA for all users (prioritize admin accounts first)**  
NIST CSF: PR.AC (Identity Management, Authentication and Access Control)  
CIS v8: Control 6 (Access Control Management)

**Remove unused/stale accounts and enforce least privilege**  
NIST CSF: PR.AC  
CIS v8: Control 5 (Account Management), Control 6 (Access Control Management)

**Separate admin accounts from daily-use accounts**  
NIST CSF: PR.AC  
CIS v8: Control 5, Control 6

**Adopt SSO where feasible and enforce strong password policy**  
NIST CSF: PR.AC  
CIS v8: Control 6

**Implement basic privileged access practices (approvals, role separation)**  
NIST CSF: PR.AC  
CIS v8: Control 6

---

## Email & phishing recommendations
**Enable phishing protections and safe link/attachment controls**  
NIST CSF: PR.PT (Protective Technology), DE.CM (Security Continuous Monitoring)  
CIS v8: Control 9 (Email and Web Browser Protections)

**Implement SPF/DKIM/DMARC and tighten forwarding rules**  
NIST CSF: PR.PT  
CIS v8: Control 9

**Set up alerting for suspicious sign-ins and mailbox rule changes**  
NIST CSF: DE.CM  
CIS v8: Control 8 (Audit Log Management)

**Run phishing awareness + reporting process**  
NIST CSF: PR.AT (Awareness and Training)  
CIS v8: Control 14 (Security Awareness and Skills Training)

---

## Endpoint & device recommendations
**Ensure endpoint protection enabled; apply patching policy**  
NIST CSF: PR.IP (Information Protection Processes and Procedures), PR.PT  
CIS v8: Control 7 (Continuous Vulnerability Management), Control 10 (Malware Defenses)

**Adopt centralized endpoint management (MDM)**  
NIST CSF: PR.PT  
CIS v8: Control 1 (Inventory and Control of Enterprise Assets), Control 4 (Secure Configuration of Enterprise Assets)

**Enable disk encryption; enforce screen lock**  
NIST CSF: PR.DS (Data Security)  
CIS v8: Control 3 (Data Protection), Control 4 (Secure Configuration)

---

## Data protection & backup recommendations
**Confirm backups exist and test one restore**  
NIST CSF: PR.IP, RC.RP (Recovery Planning)  
CIS v8: Control 11 (Data Recovery)

**Encrypt sensitive data at rest and in transit**  
NIST CSF: PR.DS  
CIS v8: Control 3 (Data Protection)

**Implement data classification basics; restrict sensitive files**  
NIST CSF: PR.DS  
CIS v8: Control 3

**Add offline/immutable backups**  
NIST CSF: RC.RP  
CIS v8: Control 11

**Introduce DLP and retention policies**  
NIST CSF: PR.DS  
CIS v8: Control 3

---

## Incident readiness recommendations
**Centralize basic logs and define alert owners**  
NIST CSF: DE.CM  
CIS v8: Control 8 (Audit Log Management)

**Incident contact list + response checklist**  
NIST CSF: RS.RP (Response Planning)  
CIS v8: Control 17 (Incident Response Management)

**Define playbooks for phishing/ransomware/account takeover**  
NIST CSF: RS.RP, RS.MI (Mitigation)  
CIS v8: Control 17

**Run tabletop exercise with leadership**  
NIST CSF: RS.IM (Improvements)  
CIS v8: Control 17

**Track MTTD/MTTR + improve detection rules**  
NIST CSF: DE.CM, RS.IM  
CIS v8: Control 8, Control 17

---

## Governance & compliance recommendations
**Confirm regulatory obligations and minimum required controls**  
NIST CSF: ID.GV (Governance), ID.RA (Risk Assessment)  
CIS v8: Control 18 (Penetration Testing is not primary here), Control 17 (process), plus org governance mapping

**Assign security ownership + define risk register**  
NIST CSF: ID.GV, ID.RM (Risk Management Strategy)  
CIS v8: Control 17 (program/process), plus governance alignment

**Review third-party vendors and security expectations**  
NIST CSF: ID.SC (Supply Chain Risk Management)  
CIS v8: Control 15 (Service Provider Management)
