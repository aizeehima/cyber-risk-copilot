from __future__ import annotations
from typing import Dict, Tuple
from .model import Scenario


RiskScores = Dict[str, int]


def _level_score(value: str, low: int = 1, medium: int = 2, high: int = 3) -> int:
    v = (value or "").strip().lower()
    if v in {"high"}:
        return high
    if v in {"medium", "moderate"}:
        return medium
    return low


def _yes_score(value: str) -> int:
    v = (value or "").strip().lower()
    return 2 if v in {"yes", "true"} else 0


def score_scenario(s: Scenario) -> Tuple[RiskScores, int]:
    """
    Returns:
      - category scores (higher = higher risk/priority)
      - total score
    Categories:
      identity_access, email_phishing, endpoint_device,
      data_backup, incident_readiness, governance_compliance
    """
    scores: RiskScores = {
        "identity_access": 0,
        "email_phishing": 0,
        "endpoint_device": 0,
        "data_backup": 0,
        "incident_readiness": 0,
        "governance_compliance": 0,
    }

    # --- Governance / compliance ---
    scores["governance_compliance"] += _level_score(s.compliance_pressure)
    if s.regulatory_environment:
        scores["governance_compliance"] += 2  # any named regulation increases priority

    # --- Identity & access ---
    # Lower IAM maturity => higher identity risk
    iam = (s.iam_maturity or "").lower()
    if iam == "low":
        scores["identity_access"] += 4
    elif iam == "medium":
        scores["identity_access"] += 2
    else:
        scores["identity_access"] += 1

    scores["identity_access"] += _yes_score(s.remote_access)  # remote access increases access risk

    if s.user_count >= 25:
        scores["identity_access"] += 2
    elif s.user_count >= 10:
        scores["identity_access"] += 1

    # --- Email & phishing ---
    scores["email_phishing"] += _yes_score(s.remote_access)
    # Cloud email is common phishing surface (treat as baseline risk)
    if s.cloud_email in {"microsoft_365", "google_workspace"}:
        scores["email_phishing"] += 2
    else:
        scores["email_phishing"] += 1

    if s.third_party_vendors in {"high"}:
        scores["email_phishing"] += 1

    # --- Endpoint & device ---
    ep = (s.endpoint_management or "").lower()
    if ep == "unmanaged":
        scores["endpoint_device"] += 4
    elif ep == "partially_managed":
        scores["endpoint_device"] += 2
    else:
        scores["endpoint_device"] += 1

    # --- Data protection & backup ---
    scores["data_backup"] += _level_score(s.data_sensitivity)
    scores["data_backup"] += _level_score(s.data_protection_maturity, low=2, medium=1, high=0)  # inverted-ish
    scores["data_backup"] += _level_score(s.backup_maturity, low=3, medium=2, high=1)  # lower maturity = higher risk

    if s.customer_data_volume == "high":
        scores["data_backup"] += 1

    # --- Incident readiness ---
    scores["incident_readiness"] += _level_score(s.logging_monitoring_maturity, low=3, medium=2, high=1)
    scores["incident_readiness"] += 1  # baseline: SMEs often underprepared

    # --- Business exposure modifiers ---
    if s.payment_processing:
        scores["governance_compliance"] += 1
        scores["data_backup"] += 1

    if s.third_party_vendors == "high":
        scores["governance_compliance"] += 1

    total = sum(scores.values())
    return scores, total


def rank_categories(scores: RiskScores):
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
