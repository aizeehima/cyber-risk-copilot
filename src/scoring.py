from __future__ import annotations
from typing import Dict, List, Tuple
from .model import Scenario


RiskScores = Dict[str, int]
RiskReasons = Dict[str, List[str]]


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


def _add(scores: RiskScores, reasons: RiskReasons, cat: str, points: int, reason: str) -> None:
    if points <= 0:
        return
    scores[cat] += points
    reasons[cat].append(f"+{points} {reason}")


def score_scenario(s: Scenario) -> Tuple[RiskScores, RiskReasons, int]:
    """
    Returns:
      - category scores (higher = higher risk/priority)
      - category reasons (explainability)
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
    reasons: RiskReasons = {k: [] for k in scores.keys()}

    # --- Governance / compliance ---
    cp = _level_score(s.compliance_pressure)
    _add(scores, reasons, "governance_compliance", cp, f"compliance_pressure={s.compliance_pressure}")

    if s.regulatory_environment:
        _add(
            scores,
            reasons,
            "governance_compliance",
            2,
            f"regulated_environment={','.join(s.regulatory_environment)}",
        )

    # --- Identity & access ---
    iam = (s.iam_maturity or "").lower()
    if iam == "low":
        _add(scores, reasons, "identity_access", 4, "iam_maturity=low")
    elif iam == "medium":
        _add(scores, reasons, "identity_access", 2, "iam_maturity=medium")
    else:
        _add(scores, reasons, "identity_access", 1, "iam_maturity=high/other")

    ra = _yes_score(s.remote_access)
    _add(scores, reasons, "identity_access", ra, f"remote_access={s.remote_access}")

    if s.user_count >= 25:
        _add(scores, reasons, "identity_access", 2, "user_count>=25")
    elif s.user_count >= 10:
        _add(scores, reasons, "identity_access", 1, "10<=user_count<25")

    # --- Email & phishing ---
    _add(scores, reasons, "email_phishing", ra, f"remote_access={s.remote_access}")

    if s.cloud_email in {"microsoft_365", "google_workspace"}:
        _add(scores, reasons, "email_phishing", 2, f"cloud_email={s.cloud_email}")
    else:
        _add(scores, reasons, "email_phishing", 1, f"cloud_email={s.cloud_email}")

    if s.third_party_vendors in {"high"}:
        _add(scores, reasons, "email_phishing", 1, "third_party_vendors=high")

    # --- Endpoint & device ---
    ep = (s.endpoint_management or "").lower()
    if ep == "unmanaged":
        _add(scores, reasons, "endpoint_device", 4, "endpoint_management=unmanaged")
    elif ep == "partially_managed":
        _add(scores, reasons, "endpoint_device", 2, "endpoint_management=partially_managed")
    else:
        _add(scores, reasons, "endpoint_device", 1, "endpoint_management=managed")

    # --- Data protection & backup ---
    ds = _level_score(s.data_sensitivity)
    _add(scores, reasons, "data_backup", ds, f"data_sensitivity={s.data_sensitivity}")

    # data_protection_maturity: basic -> higher risk, strong -> lower risk
    dpm = (s.data_protection_maturity or "").lower()
    if dpm in {"basic", "low"}:
        _add(scores, reasons, "data_backup", 2, "data_protection_maturity=basic")
    elif dpm in {"moderate", "medium"}:
        _add(scores, reasons, "data_backup", 1, "data_protection_maturity=moderate")
    else:
        _add(scores, reasons, "data_backup", 0, "data_protection_maturity=strong")

    bm = (s.backup_maturity or "").lower()
    if bm in {"basic", "low"}:
        _add(scores, reasons, "data_backup", 3, "backup_maturity=basic")
    elif bm in {"moderate", "medium"}:
        _add(scores, reasons, "data_backup", 2, "backup_maturity=moderate")
    else:
        _add(scores, reasons, "data_backup", 1, "backup_maturity=strong")

    if s.customer_data_volume == "high":
        _add(scores, reasons, "data_backup", 1, "customer_data_volume=high")

    # --- Incident readiness ---
    lmm = (s.logging_monitoring_maturity or "").lower()
    if lmm in {"basic", "low"}:
        _add(scores, reasons, "incident_readiness", 3, "logging_monitoring_maturity=basic")
    elif lmm in {"moderate", "medium"}:
        _add(scores, reasons, "incident_readiness", 2, "logging_monitoring_maturity=moderate")
    else:
        _add(scores, reasons, "incident_readiness", 1, "logging_monitoring_maturity=strong")

    _add(scores, reasons, "incident_readiness", 1, "baseline SME readiness risk")

    # --- Business exposure modifiers ---
    if s.payment_processing:
        _add(scores, reasons, "governance_compliance", 1, "payment_processing=true")
        _add(scores, reasons, "data_backup", 1, "payment_processing=true")

    if s.third_party_vendors == "high":
        _add(scores, reasons, "governance_compliance", 1, "third_party_vendors=high")

    total = sum(scores.values())
    return scores, reasons, total


def rank_categories(scores: RiskScores):
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

def normalize_scores(scores: RiskScores, max_scores: Dict[str, int], scale: int = 10) -> Dict[str, float]:
    """
    Normalize each category to a common scale (default 0–10).
    normalized = (raw / max_possible) * scale
    """
    out: Dict[str, float] = {}
    for cat, raw in scores.items():
        m = max_scores.get(cat, 0)
        out[cat] = round((raw / m) * scale, 2) if m > 0 else 0.0
    return out


def default_max_scores() -> Dict[str, int]:
    """
    Max scores based on current V1 scoring rules.
    Update this if scoring rules change.
    """
    return {
        "identity_access": 8,         # iam(4) + remote(2) + users(2)
        "email_phishing": 5,          # remote(2) + cloud_email(2) + vendors(1)
        "endpoint_device": 4,         # unmanaged(4)
        "data_backup": 10,            # data_sens(3) + protect(2) + backup(3) + custvol(1) + pay(1)
        "incident_readiness": 4,      # logging(3) + baseline(1)
        "governance_compliance": 7,   # compliance(3) + regulated(2) + pay(1) + vendors(1)
    }
