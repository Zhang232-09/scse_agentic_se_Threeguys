from ollama import chat
import json

system_prompt = """
You are Reviewer Agent. Analyze simulation report.
Output ONLY valid JSON with keys: "issue", "likely_cause", "recommendation", "needs_revision".
Rules:
- issue: string
- likely_cause: string
- recommendation: string
- needs_revision: boolean true/false
No extra text, no markdown, only pure JSON.
"""

def validate_reviewer_output(data: dict) -> bool:
    required_keys = {"issue", "likely_cause", "recommendation", "needs_revision"}
    if not isinstance(data, dict):
        return False
    if not required_keys.issubset(data.keys()):
        return False
    if not isinstance(data["needs_revision"], bool):
        return False
    if not all(isinstance(data[k], str) for k in ["issue", "likely_cause", "recommendation"]):
        return False
    return True

def run_reviewer(simulation_report: dict) -> dict:
    resp = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(simulation_report, indent=2)}
        ]
    )
    raw = resp["message"]["content"]
    result = json.loads(raw)
    if not validate_reviewer_output(result):
        raise ValueError("Reviewer output schema invalid")
    return result
