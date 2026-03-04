from __future__ import annotations

import json
from pathlib import Path

from .model import Scenario
from .scoring import score_scenario, rank_categories, normalize_scores
from .config import load_weights
from .recommendations import build_recommendations


DATA_PATH = Path("data/scenarios/scenarios.json")


def main():
    cfg = load_weights()
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    scenarios = [Scenario.from_dict(x) for x in raw]

    for s in scenarios:
        scores, reasons, total = score_scenario(s, cfg)

        # Raw ranking
        ranked = rank_categories(scores)

        # Normalized ranking (0–10) for fair comparison across categories
        max_scores = cfg.max_scores
        norm = normalize_scores(scores, max_scores, scale=cfg.normalized_max)
        ranked_norm = sorted(norm.items(), key=lambda kv: kv[1], reverse=True)

        # Use normalized rank for top categories
        top_categories = [c for c, _ in ranked_norm[:3]]
        plan = build_recommendations(top_categories)

        print("\n" + "=" * 80)
        print(f"{s.scenario_id} – {s.name}")
        print(
            f"Industry: {s.industry} | Users: {s.user_count} | IT: {s.it_environment} | Email: {s.cloud_email}"
        )
        print(
            f"Compliance: {s.compliance_pressure} | Reg: {', '.join(s.regulatory_environment) if s.regulatory_environment else 'None'}"
        )
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
                print(f"  • {item}")


if __name__ == "__main__":
    main()
