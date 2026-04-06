from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Dict, List


def build_prompt(scenario_name: str, industry: str, user_count: int,
                 top_categories: List[str], scores: Dict[str, float],
                 reasons: Dict[str, List[str]]) -> str:

    category_labels = {
        "identity_access": "Identity and Access Management",
        "email_phishing": "Email and Phishing",
        "endpoint_device": "Endpoint and Device Security",
        "data_backup": "Data Protection and Backup",
        "incident_readiness": "Incident Readiness",
        "governance_compliance": "Governance and Compliance",
    }

    top_with_scores = []
    for cat in top_categories:
        label = category_labels.get(cat, cat)
        score = scores.get(cat, 0)
        reason_list = reasons.get(cat, [])
        reason_text = ", ".join(r.lstrip("+0123456789 ") for r in reason_list[:3])
        top_with_scores.append(f"- {label} (score: {score}/10): driven by {reason_text}")

    top_summary = "\n".join(top_with_scores)

    return f"""You are a cybersecurity advisor writing a plain-English risk summary for a non-technical business owner.

Organisation: {scenario_name}
Industry: {industry}
Number of users: {user_count}

The top 3 cybersecurity risk areas identified for this organisation are:
{top_summary}

Write a 3-paragraph plain-English summary for this business owner.
Paragraph 1: Explain what the top risk area is and why it matters for their specific organisation.
Paragraph 2: Briefly mention the second and third risk areas and why they are relevant.
Paragraph 3: Give one encouraging sentence about what addressing these risks will achieve.

Rules:
- Write in second person (you, your organisation)
- No bullet points, no technical jargon, no scores or numbers
- Keep it under 200 words
- Sound like a trusted advisor, not a report
- Do not repeat the organisation name more than once"""


def generate_narrative(scenario_name: str, industry: str, user_count: int,
                       top_categories: List[str], scores: Dict[str, float],
                       reasons: Dict[str, List[str]]) -> str:

    prompt = build_prompt(scenario_name, industry, user_count,
                          top_categories, scores, reasons)

    payload = json.dumps({
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except urllib.error.URLError as e:
        return f"[Narrative unavailable — is Ollama running? Error: {e}]"
    except Exception as e:
        return f"[Narrative generation failed: {e}]"
