from __future__ import annotations
import json
import os
import urllib.request
import urllib.error
from typing import Dict, List, Optional
import time


def build_prompt(scenario_name: str, industry: str, user_count: int,
                 top_categories: List[str], scores: Dict[str, float],
                 reasons: Dict[str, List[str]],
                 notes: Optional[Dict[str, str]] = None) -> str:
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

    notes_block = ""
    if notes:
        notes_lines = "\n".join(f"- {k}: {v}" for k, v in notes.items())
        notes_block = f"\nAdditional organisational context:\n{notes_lines}\n"

    return f"""You are a cybersecurity advisor writing a plain-English risk summary for a non-technical business owner.
Organisation: {scenario_name}
Industry: {industry}
Number of users: {user_count}
{notes_block}
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
- Sound like a trusted advisor, not a report
- If organisational context is provided, reference specific details naturally"""


def build_cso_brief_prompt(scenario_name: str, industry: str, user_count: int,
                            company_stage: str, top_categories: List[str],
                            scores: Dict[str, float], reasons: Dict[str, List[str]],
                            regulatory_environment: List[str],
                            notes: Optional[Dict[str, str]] = None) -> str:

    category_labels = {
        "identity_access": "Identity and Access Management",
        "email_phishing": "Email and Phishing",
        "endpoint_device": "Endpoint and Device Security",
        "data_backup": "Data Protection and Backup",
        "incident_readiness": "Incident Readiness",
        "governance_compliance": "Governance and Compliance",
    }

    stage_context = {
        "pre_launch": "This organisation has not yet launched. They are building their product and team and have not yet onboarded real users or processed payments. Security decisions made now will define their baseline posture at launch.",
        "live": "This organisation is live and operating. They have real users, active data, and are potentially processing transactions. Security gaps are active risks, not theoretical ones.",
        "scaling": "This organisation is growing rapidly. They are adding users, staff, and systems. Security controls that worked at a smaller size may no longer be sufficient and governance is becoming critical.",
    }.get(company_stage, "This is an operating SME.")

    reg_block = ""
    if regulatory_environment:
        reg_block = f"\nRegulatory obligations in scope or incoming: {', '.join(regulatory_environment)}"

    notes_block = ""
    if notes:
        notes_lines = "\n".join(f"- {k}: {v}" for k, v in notes.items())
        notes_block = f"\nAdditional organisational context:\n{notes_lines}"

    top_risks = "\n".join(
        f"- {category_labels.get(c, c)}: score {scores.get(c, 0):.1f}/10"
        for c in top_categories
    )

    return f"""You are a virtual Chief Security Officer (CSO) writing a confidential security brief for the founder and leadership team of a small business. You know their organisation well and speak plainly.

Organisation: {scenario_name}
Industry: {industry}
Team size: {user_count} people
Stage: {company_stage.replace('_', ' ').title()}
{stage_context}
{reg_block}
{notes_block}

Top 3 risk areas identified by automated assessment:
{top_risks}

Write a CSO Brief with exactly these four sections. Use the headers exactly as shown.

WHERE YOU STAND
In 2-3 sentences, describe the organisation's current security posture honestly and in plain English. Reference their specific stage, industry, and team size. Be direct — not alarmist, not soft.

WHAT IS COMING AT YOU
In 3-4 sentences, explain the real-world threats and regulatory obligations most relevant to this organisation right now. If regulatory_environment contains incoming obligations, explain in plain English what those regulations will specifically require of this organisation based on the data they will handle. Make it concrete — reference their actual stack and data types if context is available.

YOUR PRIORITY LIST — NEXT 90 DAYS
Write 5 specific, plain-English actions this organisation should take in the next 90 days. Number them 1 to 5. Each action should be one sentence, written as a direct instruction to the founder. Reference their actual tools and systems where context is available. No jargon. No generic advice.

WHAT GOOD LOOKS LIKE
In 2 sentences, describe what a defensible security posture looks like for an organisation at their exact stage. Give them a target to work toward, not just a list of problems.

Rules:
- Write in second person (you, your organisation, your team)
- Sound like a trusted advisor who knows this company, not a compliance officer
- Be specific — reference their industry, stage, tools, and data wherever possible
- Keep total length under 400 words
- No scores or technical metrics — translate everything into plain language"""


def _call_gemini(api_key: str, prompt: str) -> str:
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    req = urllib.request.Request(
        url, data=payload,
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
        return f"[Generation failed: {e.code} — {body[:200]}]"
    except Exception as e:
        return f"[Generation failed: {e}]"


def generate_narrative(scenario_name: str, industry: str, user_count: int,
                       top_categories: List[str], scores: Dict[str, float],
                       reasons: Dict[str, List[str]],
                       notes: Optional[Dict[str, str]] = None) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "[Narrative unavailable — set GOOGLE_API_KEY to enable this feature]"
    prompt = build_prompt(scenario_name, industry, user_count,
                          top_categories, scores, reasons, notes)
    return _call_gemini(api_key, prompt)


def generate_cso_brief(scenario_name: str, industry: str, user_count: int,
                       company_stage: str, top_categories: List[str],
                       scores: Dict[str, float], reasons: Dict[str, List[str]],
                       regulatory_environment: List[str],
                       notes: Optional[Dict[str, str]] = None) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "[CSO Brief unavailable — set GOOGLE_API_KEY to enable this feature]"
    prompt = build_cso_brief_prompt(scenario_name, industry, user_count,
                                     company_stage, top_categories, scores,
                                     reasons, regulatory_environment, notes)
    return _call_gemini(api_key, prompt)
