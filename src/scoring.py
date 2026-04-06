from __future__ import annotations

from typing import Dict, List, Tuple

from .config import WeightsConfig
from .model import Scenario

RiskScores = Dict[str, int]
RiskReasons = Dict[str, List[str]]


def _add(scores: RiskScores, reasons: RiskReasons, cat: str, points: int, reason: str) -> None:
    if points <= 0:
        return
    scores[cat] += points
    reasons[cat].append(f"+{points} {reason}")


def score_scenario(s: Scenario, cfg: WeightsConfig) -> Tuple[RiskScores, RiskReasons, int]:
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

    w = cfg.weights

    # ---------------------------
    # Governance / Compliance
    # ---------------------------
    cp_map = w["compliance_pressure"]
    cp_points = int(cp_map.get((s.compliance_pressure or "low").lower(), cp_map.get("low", 1)))
    _add(scores, reasons, "governance_compliance", cp_points, f"compliance_pressure={s.compliance_pressure}")

    if s.regulatory_environment:
        _add(
            scores,
            reasons,
            "governance_compliance",
            int(w["regulated_environment_present"]),
            f"regulated_environment={','.join(s.regulatory_environment)}",
        )

    # ---------------------------
    # Identity & Access
    # ---------------------------
    iam_map = w["iam_maturity"]
    iam_points = int(iam_map.get((s.iam_maturity or "low").lower(), iam_map.get("low", 4)))
    _add(scores, reasons, "identity_access", iam_points, f"iam_maturity={s.iam_maturity}")

    remote_val = str(s.remote_access).strip().lower()
    remote_yes = remote_val in {"yes", "true"}
    remote_limited = remote_val == "limited"
    ra_points = int(w["remote_access_present"]) if remote_yes else (int(w["remote_access_limited"]) if remote_limited else 0)
    _add(scores, reasons, "identity_access", ra_points, f"remote_access={s.remote_access}")

    uc_map = w["user_count"]
    if s.user_count >= 25:
        _add(scores, reasons, "identity_access", int(uc_map["ge_25"]), "user_count>=25")
    elif s.user_count >= 10:
        _add(scores, reasons, "identity_access", int(uc_map["ge_10"]), "10<=user_count<25")

    # Third-party vendors increase credential exposure surface
    if (s.third_party_vendors or "").lower() == "high":
        _add(scores, reasons, "identity_access", int(w["third_party_vendors_high_iam"]), "third_party_vendors=high increases credential exposure")

    # Regulated environments with medium/low IAM face higher credential breach consequences
    if s.regulatory_environment and (s.iam_maturity or "").lower() in {"low", "medium"}:
        _add(scores, reasons, "identity_access",
             int(w["regulated_high_iam_risk"]), "regulated environment amplifies IAM risk")

    # ---------------------------
    # Email & Phishing
    # ---------------------------
    # remote access increases email compromise likelihood
    _add(scores, reasons, "email_phishing", ra_points, f"remote_access={s.remote_access}")

    ce_map = w["cloud_email"]
    ce_key = (s.cloud_email or "other").lower()
    ce_points = int(ce_map.get(ce_key, ce_map.get("other", 1)))
    _add(scores, reasons, "email_phishing", ce_points, f"cloud_email={s.cloud_email}")

    if (s.third_party_vendors or "").lower() == "high":
        _add(scores, reasons, "email_phishing", int(w["third_party_vendors_high_email"]), "third_party_vendors=high")

    # ---------------------------
    # Endpoint / Device
    # ---------------------------
    ep_map = w["endpoint_management"]
    ep_key = (s.endpoint_management or "managed").lower()
    ep_points = int(ep_map.get(ep_key, ep_map.get("managed", 1)))
    _add(scores, reasons, "endpoint_device", ep_points, f"endpoint_management={s.endpoint_management}")

    # ---------------------------
    # Data Protection & Backup
    # ---------------------------
    ds_map = w["data_sensitivity"]
    ds_key = (s.data_sensitivity or "low").lower()
    ds_points = int(ds_map.get(ds_key, ds_map.get("low", 1)))
    _add(scores, reasons, "data_backup", ds_points, f"data_sensitivity={s.data_sensitivity}")

    dpm_map = w["data_protection_maturity"]
    dpm_key = (s.data_protection_maturity or "basic").lower()
    dpm_points = int(dpm_map.get(dpm_key, dpm_map.get("basic", 2)))
    _add(scores, reasons, "data_backup", dpm_points, f"data_protection_maturity={s.data_protection_maturity}")

    bm_map = w["backup_maturity"]
    bm_key = (s.backup_maturity or "basic").lower()
    bm_points = int(bm_map.get(bm_key, bm_map.get("basic", 3)))
    _add(scores, reasons, "data_backup", bm_points, f"backup_maturity={s.backup_maturity}")

    if (s.customer_data_volume or "").lower() == "high":
        _add(scores, reasons, "data_backup", int(w["customer_data_volume_high"]), "customer_data_volume=high")

    # ---------------------------
    # Incident Readiness
    # ---------------------------
    lm_map = w["logging_monitoring_maturity"]
    lm_key = (s.logging_monitoring_maturity or "basic").lower()
    lm_points = int(lm_map.get(lm_key, lm_map.get("basic", 3)))
    _add(scores, reasons, "incident_readiness", lm_points, f"logging_monitoring_maturity={s.logging_monitoring_maturity}")

    _add(
        scores,
        reasons,
        "incident_readiness",
        int(w["baseline_incident_readiness"]),
        "baseline SME readiness risk",
    )

    # Remote access expands detection surface — harder to monitor distributed sessions
    if remote_yes or remote_limited:
        _add(scores, reasons, "incident_readiness",
             int(w["remote_access_incident"]), "remote_access increases detection complexity")

    # Cloud-only or hybrid environments require cloud-native log integration
    if (s.it_environment or "").lower() in {"cloud", "hybrid"}:
        _add(scores, reasons, "incident_readiness",
             int(w["cloud_environment_incident"]), f"it_environment={s.it_environment} requires cloud log integration")

    if bool(s.payment_processing):
        _add(scores, reasons, "incident_readiness",
             int(w["payment_processing_incident"]), "payment_processing increases incident impact")

    # Low IAM maturity increases likelihood of incidents occurring
    if (s.iam_maturity or "").lower() == "low":
        _add(scores, reasons, "incident_readiness",
             int(w["low_iam_incident_risk"]), "low IAM maturity increases incident likelihood")

    # Unmanaged endpoints increase incident surface
    if (s.endpoint_management or "").lower() == "unmanaged":
        _add(scores, reasons, "incident_readiness",
             int(w["unmanaged_endpoint_incident_risk"]), "unmanaged endpoints increase incident surface")

    # ---------------------------
    # Business exposure modifiers
    # ---------------------------
    if bool(s.payment_processing):
        _add(scores, reasons, "data_backup", int(w["payment_processing_data"]), "payment_processing=true")
        _add(scores, reasons, "governance_compliance", int(w["payment_processing_governance"]), "payment_processing=true")

    if (s.third_party_vendors or "").lower() == "high":
        _add(
            scores,
            reasons,
            "governance_compliance",
            int(w["third_party_vendors_high_governance"]),
            "third_party_vendors=high",
        )

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
        m = int(max_scores.get(cat, 0) or 0)
        out[cat] = round((raw / m) * scale, 2) if m > 0 else 0.0
    return out

def compute_theoretical_max(cfg: WeightsConfig) -> Dict[str, int]:
    """
    Computes the theoretical maximum raw score for each category
    by summing all worst-case weight values from config.
    Used to verify that max_scores in weights.yaml are accurate.
    """
    w = cfg.weights

    identity_access = (
        int(w["iam_maturity"]["low"])
        + int(w["remote_access_present"])
        + int(w["user_count"]["ge_25"])
	+ int(w["third_party_vendors_high_iam"])
	+ int(w["regulated_high_iam_risk"])
    )

    email_phishing = (
        int(w["remote_access_present"])
        + max(int(v) for v in w["cloud_email"].values())
        + int(w["third_party_vendors_high_email"])
    )

    endpoint_device = max(int(v) for v in w["endpoint_management"].values())

    data_backup = (
        int(w["data_sensitivity"]["high"])
        + int(w["data_protection_maturity"]["basic"])
        + int(w["backup_maturity"]["basic"])
        + int(w["customer_data_volume_high"])
        + int(w["payment_processing_data"])
    )

    incident_readiness = (
        max(int(v) for v in w["logging_monitoring_maturity"].values())
        + int(w["baseline_incident_readiness"])
        + int(w["remote_access_incident"])
        + int(w["cloud_environment_incident"])
	+ int(w["payment_processing_incident"])
	+ int(w["low_iam_incident_risk"])
        + int(w["unmanaged_endpoint_incident_risk"])
    )

    governance_compliance = (
        int(w["compliance_pressure"]["high"])
        + int(w["regulated_environment_present"])
        + int(w["payment_processing_governance"])
        + int(w["third_party_vendors_high_governance"])
    )

    return {
        "identity_access": identity_access,
        "email_phishing": email_phishing,
        "endpoint_device": endpoint_device,
        "data_backup": data_backup,
        "incident_readiness": incident_readiness,
        "governance_compliance": governance_compliance,
    }


def validate_max_scores(cfg: WeightsConfig) -> None:
    """
    Asserts that weights.yaml max_scores match the computed theoretical maxima.
    Raises ValueError on mismatch so misconfiguration is caught at startup.
    """
    computed = compute_theoretical_max(cfg)
    declared = cfg.max_scores
    mismatches = []
    for cat, computed_max in computed.items():
        declared_max = int(declared.get(cat, 0))
        if declared_max != computed_max:
            mismatches.append(
                f"  {cat}: weights.yaml says {declared_max}, computed max is {computed_max}"
            )
    if mismatches:
        raise ValueError(
            "max_scores in weights.yaml do not match computed theoretical maxima:\n"
            + "\n".join(mismatches)
        )
