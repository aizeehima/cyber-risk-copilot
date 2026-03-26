from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import load_weights
from .model import Scenario
from .recommendations import build_recommendations
from .scoring import normalize_scores, rank_categories, score_scenario


DATA_PATH = Path("data/scenarios/scenarios.json")


def main():
    report_mode = "--report" in sys.argv

    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    scenarios = [Scenario.from_dict(x) for x in raw]
    cfg = load_weights()

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
                print(f"  • {item['text']}")
                if report_mode:
                    print(f"      NIST CSF: {item['nist']}")
                    print(f"      CIS v8:   {item['cis']}")


if __name__ == "__main__":
    main()
