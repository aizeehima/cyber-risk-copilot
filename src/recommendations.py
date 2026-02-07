from __future__ import annotations
from typing import Dict, List


ACTIONS_BY_CATEGORY: Dict[str, Dict[str, List[str]]] = {
    "identity_access": {
        "phase1": [
            "Enable MFA for all users (prioritize admin accounts first)",
            "Remove unused/stale accounts and enforce least privilege",
            "Separate admin accounts from daily-use accounts",
        ],
        "phase2": [
            "Adopt SSO where feasible and enforce strong password policy",
            "Implement basic privileged access practices (admin approvals, role separation)",
        ],
        "phase3": [
            "Introduce privileged access management and regular access reviews",
        ],
    },
    "email_phishing": {
        "phase1": [
            "Enable phishing protections and safe link/attachment controls (where available)",
            "Run a basic phishing awareness push and reporting process",
        ],
        "phase2": [
            "Implement SPF/DKIM/DMARC and tighten email forwarding rules",
            "Set up alerting for suspicious sign-ins and mailbox rule changes",
        ],
        "phase3": [
            "Automate phishing simulations and training metrics",
        ],
    },
    "endpoint_device": {
        "phase1": [
            "Ensure all devices have basic endpoint protection enabled",
            "Apply OS and browser patching policy (minimum monthly updates)",
        ],
        "phase2": [
            "Adopt centralized endpoint management (MDM) for key devices",
            "Enable disk encryption on laptops and enforce screen lock policies",
        ],
        "phase3": [
            "Add device compliance checks and conditional access policies",
        ],
    },
    "data_backup": {
        "phase1": [
            "Confirm backups exist for critical systems and test one restore",
            "Encrypt sensitive data at rest and in transit where applicable",
        ],
        "phase2": [
            "Implement data classification basics and restrict access to sensitive files",
            "Improve backup cadence and add offline/immutable backup where possible",
        ],
        "phase3": [
            "Introduce DLP controls and automated data retention policies",
        ],
    },
    "incident_readiness": {
        "phase1": [
            "Centralize basic logs (auth, email, endpoints) and define alert owners",
            "Create an incident contact list and a simple response checklist",
        ],
        "phase2": [
            "Define playbooks for phishing, ransomware, and account takeover",
            "Run a tabletop exercise with leadership",
        ],
        "phase3": [
            "Improve detection rules and incident metrics (MTTD/MTTR tracking)",
        ],
    },
    "governance_compliance": {
        "phase1": [
            "Confirm regulatory obligations and document minimum required controls",
            "Assign security ownership and define a basic risk register",
        ],
        "phase2": [
            "Map key controls to NIST CSF / CIS Controls and track progress",
            "Review third-party vendors and document security expectations",
        ],
        "phase3": [
            "Formalize policies (access, backups, incident response) and audit readiness",
        ],
    },
}


def build_recommendations(top_categories: List[str]) -> Dict[str, List[str]]:
    """
    Returns a phased plan aggregated from the top categories.
    """
    plan = {"phase1": [], "phase2": [], "phase3": []}
    for cat in top_categories:
        block = ACTIONS_BY_CATEGORY.get(cat, {})
        for phase in plan:
            plan[phase].extend(block.get(phase, []))
    # de-duplicate while preserving order
    for phase in plan:
        seen = set()
        deduped = []
        for item in plan[phase]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        plan[phase] = deduped
    return plan
