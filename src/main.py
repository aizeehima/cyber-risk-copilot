from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import load_weights
from .model import Scenario
from .recommendations import build_recommendations
from .scoring import normalize_scores, rank_categories, score_scenario, validate_max_scores, compute_theoretical_max
from .narrator import generate_narrative


DATA_PATH = Path("data/scenarios/scenarios.json")


def run_sensitivity(s: Scenario, cfg) -> None:
    """
    For each ordinal input, toggle it one tier and show the score delta.
    Helps demonstrate scoring robustness for evaluation purposes.
    """
    baseline_scores, _, _ = score_scenario(s, cfg)
    baseline_norm = normalize_scores(baseline_scores, cfg.max_scores, scale=cfg.normalized_max)
    baseline_ranked = sorted(baseline_norm.items(), key=lambda kv: kv[1], reverse=True)
    baseline_top3 = [c for c, _ in baseline_ranked[:3]]

    toggle_tests = [
        ("iam_maturity",               "medium", s, lambda sc: Scenario(**{**sc.__dict__, "iam_maturity": "low"}),    "medium→low"),
        ("iam_maturity",               "medium", s, lambda sc: Scenario(**{**sc.__dict__, "iam_maturity": "high"}),   "medium→high"),
        ("backup_maturity",            "moderate", s, lambda sc: Scenario(**{**sc.__dict__, "backup_maturity": "basic"}),    "moderate→basic"),
        ("backup_maturity",            "moderate", s, lambda sc: Scenario(**{**sc.__dict__, "backup_maturity": "strong"}),   "moderate→strong"),
        ("logging_monitoring_maturity","basic", s, lambda sc: Scenario(**{**sc.__dict__, "logging_monitoring_maturity": "moderate"}), "basic→moderate"),
        ("endpoint_management",        s.endpoint_management, s, lambda sc: Scenario(**{**sc.__dict__, "endpoint_management": "unmanaged"}), f"{s.endpoint_management}→unmanaged"),
    ]

    print("\n  Sensitivity analysis (single-factor perturbations):")
    print(f"  {'Factor':<30} {'Change':<22} {'Affected cat delta':>22}  {'Top-3 stable?'}")
    print("  " + "-" * 85)

    for factor, baseline_val, orig_s, mutate_fn, label in toggle_tests:
        mutated = mutate_fn(orig_s)
        mut_scores, _, _ = score_scenario(mutated, cfg)
        mut_norm = normalize_scores(mut_scores, cfg.max_scores, scale=cfg.normalized_max)
        mut_ranked = sorted(mut_norm.items(), key=lambda kv: kv[1], reverse=True)
        mut_top3 = [c for c, _ in mut_ranked[:3]]

        # Find the category most affected
        max_delta_cat = max(mut_norm.keys(), key=lambda c: abs(mut_norm[c] - baseline_norm[c]))
        delta = mut_norm[max_delta_cat] - baseline_norm[max_delta_cat]
        stable = "YES" if mut_top3 == baseline_top3 else f"NO → {', '.join(mut_top3[:3])}"

        print(f"  {factor:<30} {label:<22} {max_delta_cat}: {delta:+.2f}  {stable}")


def main():
    report_mode = "--report" in sys.argv
    sensitivity_mode = "--sensitivity" in sys.argv
    narrative_mode = "--narrative" in sys.argv

    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    scenarios = [Scenario.from_dict(x) for x in raw]
    cfg = load_weights()

    # Startup validation — catches weight/max_scores drift immediately
    validate_max_scores(cfg)

    for s in scenarios:
        scores, reasons, total = score_scenario(s, cfg)

        ranked = rank_categories(scores)
        max_scores = cfg.max_scores
        norm = normalize_scores(scores, max_scores, scale=cfg.normalized_max)
        ranked_norm = sorted(norm.items(), key=lambda kv: kv[1], reverse=True)

        top_categories = [c for c, _ in ranked_norm[:3]]
        plan = build_recommendations(top_categories)

        print("\n" + "=" * 80)
        print(f"{s.scenario_id} – {s.name}")
        print(f"Industry: {s.industry} | Users: {s.user_count} | IT: {s.it_environment} | Email: {s.cloud_email}")
        print(f"Compliance: {s.compliance_pressure} | Reg: {', '.join(s.regulatory_environment) if s.regulatory_environment else 'None'}")
        print("-" * 80)

        print("Risk category scores (raw → normalized/10):")
        for cat, raw_score in ranked:
            print(f"  - {cat:22s} {raw_score} → {norm[cat]}")
            for r in reasons.get(cat, []):
                print(f"      {r}")

        print(f"\nTotal score: {total}")
        print("-" * 80)
        print("Prioritized plan (Top 3 categories):", ", ".join(top_categories))

        for phase in ["phase1", "phase2", "phase3"]:
            print(f"\n{phase.upper()}:")
            for item in plan[phase]:
                print(f"  • {item['text']}")
                if report_mode:
                    print(f"      NIST CSF: {item['nist']}")
                    print(f"      CIS v8:   {item['cis']}")

        if sensitivity_mode:
            run_sensitivity(s, cfg)
        if narrative_mode:
            print("\n--- Plain-English Risk Summary ---")
            narrative = generate_narrative(
                s.name, s.industry, s.user_count,
                top_categories, norm, reasons
            )
            print(narrative)
            print("-" * 80)


if __name__ == "__main__":
    main()
