from __future__ import annotations

from typing import Dict


RECOMMENDATION_MAPPINGS: Dict[str, Dict[str, str]] = {
    # Identity & Access
    "Enable MFA for all users (prioritize admin accounts first)": {
        "nist": "PR.AA / PR.AC",
        "cis": "CIS Control 6 (Access Control Management)"
    },
    "Remove unused/stale accounts and enforce least privilege": {
        "nist": "PR.AC",
        "cis": "CIS Control 5 (Account Management), CIS Control 6"
    },
    "Separate admin accounts from daily-use accounts": {
        "nist": "PR.AC",
        "cis": "CIS Control 5, CIS Control 6"
    },
    "Adopt SSO where feasible and enforce strong password policy": {
        "nist": "PR.AC",
        "cis": "CIS Control 6"
    },
    "Implement basic privileged access practices (admin approvals, role separation)": {
        "nist": "PR.AC",
        "cis": "CIS Control 6"
    },
    "Introduce privileged access management and regular access reviews": {
        "nist": "PR.AC",
        "cis": "CIS Control 6"
    },

    # Email & Phishing
    "Enable phishing protections and safe link/attachment controls (where available)": {
        "nist": "PR.PT / DE.CM",
        "cis": "CIS Control 9 (Email and Web Browser Protections)"
    },
    "Run a basic phishing awareness push and reporting process": {
        "nist": "PR.AT",
        "cis": "CIS Control 14 (Security Awareness and Skills Training)"
    },
    "Implement SPF/DKIM/DMARC and tighten email forwarding rules": {
        "nist": "PR.PT",
        "cis": "CIS Control 9"
    },
    "Set up alerting for suspicious sign-ins and mailbox rule changes": {
        "nist": "DE.CM",
        "cis": "CIS Control 8 (Audit Log Management)"
    },
    "Automate phishing simulations and training metrics": {
        "nist": "PR.AT",
        "cis": "CIS Control 14"
    },

    # Endpoint & Device
    "Ensure all devices have basic endpoint protection enabled": {
        "nist": "PR.PT",
        "cis": "CIS Control 10 (Malware Defenses)"
    },
    "Apply OS and browser patching policy (minimum monthly updates)": {
        "nist": "PR.IP",
        "cis": "CIS Control 7 (Continuous Vulnerability Management)"
    },
    "Adopt centralized endpoint management (MDM) for key devices": {
        "nist": "PR.PT",
        "cis": "CIS Control 1 (Inventory and Control of Enterprise Assets), CIS Control 4"
    },
    "Enable disk encryption on laptops and enforce screen lock policies": {
        "nist": "PR.DS",
        "cis": "CIS Control 3 (Data Protection), CIS Control 4"
    },
    "Add device compliance checks and conditional access policies": {
        "nist": "PR.AC / PR.PT",
        "cis": "CIS Control 4, CIS Control 6"
    },

    # Data & Backup
    "Confirm backups exist for critical systems and test one restore": {
        "nist": "PR.IP / RC.RP",
        "cis": "CIS Control 11 (Data Recovery)"
    },
    "Encrypt sensitive data at rest and in transit where applicable": {
        "nist": "PR.DS",
        "cis": "CIS Control 3 (Data Protection)"
    },
    "Implement data classification basics and restrict access to sensitive files": {
        "nist": "PR.DS",
        "cis": "CIS Control 3"
    },
    "Improve backup cadence and add offline/immutable backup where possible": {
        "nist": "RC.RP",
        "cis": "CIS Control 11"
    },
    "Introduce DLP controls and automated data retention policies": {
        "nist": "PR.DS",
        "cis": "CIS Control 3"
    },

    # Incident Readiness
    "Centralize basic logs (auth, email, endpoints) and define alert owners": {
        "nist": "DE.CM",
        "cis": "CIS Control 8 (Audit Log Management)"
    },
    "Create an incident contact list and a simple response checklist": {
        "nist": "RS.RP",
        "cis": "CIS Control 17 (Incident Response Management)"
    },
    "Define playbooks for phishing, ransomware, and account takeover": {
        "nist": "RS.RP / RS.MI",
        "cis": "CIS Control 17"
    },
    "Run a tabletop exercise with leadership": {
        "nist": "RS.IM",
        "cis": "CIS Control 17"
    },
    "Improve detection rules and incident metrics (MTTD/MTTR tracking)": {
        "nist": "DE.CM / RS.IM",
        "cis": "CIS Control 8, CIS Control 17"
    },

    # Governance & Compliance
    "Confirm regulatory obligations and document minimum required controls": {
        "nist": "ID.GV / ID.RA",
        "cis": "Governance alignment / control scoping"
    },
    "Assign security ownership and define a basic risk register": {
        "nist": "ID.GV / ID.RM",
        "cis": "Program governance / risk management support"
    },
    "Map key controls to NIST CSF / CIS Controls and track progress": {
        "nist": "ID.GV / ID.RM",
        "cis": "Cross-framework control alignment"
    },
    "Review third-party vendors and document security expectations": {
        "nist": "ID.SC",
        "cis": "CIS Control 15 (Service Provider Management)"
    },
    "Formalize policies (access, backups, incident response) and audit readiness": {
        "nist": "ID.GV / PR.IP / RS.RP",
        "cis": "Governance and operational policy alignment"
    },
}


def get_mapping(recommendation: str) -> Dict[str, str]:
    return RECOMMENDATION_MAPPINGS.get(
        recommendation,
        {
            "nist": "Not mapped yet",
            "cis": "Not mapped yet",
        },
    )
