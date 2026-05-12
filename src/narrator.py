from __future__ import annotations
import json
import os
import urllib.request
import urllib.error
from typing import Dict, List
import time


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
Paragraph 3: One encouraging sentence about what addressing these risks will achieve.

Rules:
- Write in second person (you, your organisation)
- No bullet points, no technical jargon, no scores or numbers
- Keep it under 200 words
- Sound like a trusted advisor, not a report"""


def generate_narrative(scenario_name: str, industry: str, user_count: int,
                       top_categories: List[str], scores: Dict[str, float],
                       reasons: Dict[str, List[str]]) -> str:

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "[Narrative unavailable — set GOOGLE_API_KEY to enable this feature]"

    prompt = build_prompt(scenario_name, industry, user_count,
                          top_categories, scores, reasons)

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        time.sleep(5)
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return f"[Narrative generation failed: {e.code} — {body[:200]}]"
    except Exception as e:
        return f"[Narrative generation failed: {e}]"
