from __future__ import annotations
import json
from pathlib import Path

from .model import Scenario
from .scoring import score_scenario, rank_categories
from .recommendations import build_recommendations


DATA_PATH = Path("data/scenarios/scenarios.json")


def main():
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    scenarios = [Scenario.from_dict(x) for x in raw]

    for s in scenarios:
        scores, total = score_scenario(s)
        ranked = rank_categories(scores)
        top_categories = [c for c, _ in ranked[:3]]  # top 3 risk areas drive plan
        plan = build_recommendations(top_categories)

        print("\n" + "=" * 80)
        print(f"{s.scenario_id} – {s.name}")
        print(f"Industry: {s.industry} | Users: {s.user_count} | IT: {s.it_environment} | Email: {s.cloud_email}")
        print(f"Compliance: {s.compliance_pressure} | Reg: {', '.join(s.regulatory_environment) if s.regulatory_environment else 'None'}")
        print("-" * 80)
        print("Risk category scores:")
        for cat, val in ranked:
            print(f"  - {cat:22s} {val}")
        print(f"\nTotal score: {total}")
        print("-" * 80)
        print("Prioritized plan (Top 3 categories):", ", ".join(top_categories))

        for phase in ["phase1", "phase2", "phase3"]:
            print(f"\n{phase.upper()}:")
            for item in plan[phase]:
                print(f"  • {item}")


if __name__ == "__main__":
    main()
