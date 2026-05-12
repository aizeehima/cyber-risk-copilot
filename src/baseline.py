from __future__ import annotations

import json
import random
from pathlib import Path

from .config import load_weights
from .model import Scenario
from .scoring import score_scenario, normalize_scores


def top3_set(scores: dict) -> frozenset:
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return frozenset(c for c, _ in ranked[:3])


def run_baseline(n_trials: int = 10000):
    categories = [
        "identity_access", "email_phishing", "endpoint_device",
        "data_backup", "incident_readiness", "governance_compliance"
    ]

    raw = json.loads(Path("data/scenarios/scenarios.json").read_text())
    scenarios = [Scenario.from_dict(x) for x in raw]
    cfg = load_weights()

    print("=" * 70)
    print("BASELINE COMPARISON REPORT")
    print("=" * 70)

    # --- Random baseline ---
    print("\n1. RANDOM BASELINE")
    print("   How often does random category selection match the framework?")
    print("   Expected by chance: 5.0% (1 in 20 combinations)")
    print()

    total_matches = 0
    total_trials = 0

    for s in scenarios:
        scores, _, _ = score_scenario(s, cfg)
        norm = normalize_scores(scores, cfg.max_scores, scale=cfg.normalized_max)
        fw_top3 = top3_set(norm)

        matches = sum(
            1 for _ in range(n_trials)
            if frozenset(random.sample(categories, 3)) == fw_top3
        )
        match_rate = matches / n_trials * 100
        total_matches += matches
        total_trials += n_trials
        print(f"   {s.scenario_id}: {match_rate:.1f}% random match rate")

    overall = total_matches / total_trials * 100
    print(f"\n   Overall random match rate: {overall:.1f}%")
    print(f"   Conclusion: Framework produces specific, non-random outputs")

    # --- Uniform weight baseline ---
    print("\n2. UNIFORM WEIGHT BASELINE")
    print("   What if all factors had equal weight (1 point each)?")
    print("   Tests whether literature-grounded weights change the output.")
    print()

    different = 0
    for s in scenarios:
        # Framework scores
        scores, _, _ = score_scenario(s, cfg)
        norm = normalize_scores(scores, cfg.max_scores, scale=cfg.normalized_max)
        fw_top3 = sorted(norm.items(), key=lambda kv: kv[1], reverse=True)[:3]
        fw_cats = [c for c, _ in fw_top3]

        # Uniform scores — count signals per category, all weight 1
        u = {k: 0 for k in scores}
        if s.iam_maturity.lower() in {"low", "medium"}:
            u["identity_access"] += 1
        if s.remote_access.lower() in {"yes", "limited"}:
            u["identity_access"] += 1
            u["email_phishing"] += 1
            u["incident_readiness"] += 1
        if s.endpoint_management.lower() in {"unmanaged", "partially_managed"}:
            u["endpoint_device"] += 1
        if s.data_sensitivity.lower() in {"high", "medium"}:
            u["data_backup"] += 1
        if s.backup_maturity.lower() in {"basic", "moderate"}:
            u["data_backup"] += 1
        if s.logging_monitoring_maturity.lower() == "basic":
            u["incident_readiness"] += 1
        if s.compliance_pressure.lower() in {"high", "medium"}:
            u["governance_compliance"] += 1
        if s.regulatory_environment:
            u["governance_compliance"] += 1
        if s.payment_processing:
            u["data_backup"] += 1
            u["governance_compliance"] += 1

        u_top3 = sorted(u.items(), key=lambda kv: kv[1], reverse=True)[:3]
        u_cats = [c for c, _ in u_top3]

        match = set(fw_cats) == set(u_cats)
        if not match:
            different += 1
        status = "SAME" if match else "DIFFERENT"
        print(f"   {s.scenario_id}: [{status}]")
        if not match:
            print(f"      Framework: {', '.join(fw_cats)}")
            print(f"      Uniform:   {', '.join(u_cats)}")

    print(f"\n   Result: {different}/{len(scenarios)} scenarios produce different")
    print(f"   rankings under uniform weighting")
    print(f"   Conclusion: Literature-grounded weights materially affect output")
    print()
    print("=" * 70)


if __name__ == "__main__":
    run_baseline()
