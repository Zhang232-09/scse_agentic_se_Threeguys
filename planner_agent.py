import ollama
import json

def run_planner(requirement):
    prompt = f"""
You are a robot navigation planner agent.
Given validated robot requirements, produce ONLY valid JSON, no markdown, no extra text.
JSON must contain exactly three keys:
1. "strategy": string, overall navigation strategy
2. "decisions": list of strings, possible robot decisions during navigation
3. "stop_condition": string, condition when robot must stop

Robot requirements:
{json.dumps(requirement)}
"""
    resp = ollama.chat(
        model="qwen3:8b",
        messages=[{"role":"user", "content": prompt}]
    )
    raw_text = resp["message"]["content"]
    plan_data = json.loads(raw_text)
    validate_plan(plan_data)
    return plan_data


def validate_plan(data):
    if not isinstance(data, dict):
        raise TypeError("Plan must be a dictionary")

    required_keys = {"strategy", "decisions", "stop_condition"}
    if set(data.keys()) != required_keys:
        raise ValueError("Missing or extra keys in plan")

    if not isinstance(data["strategy"], str):
        raise TypeError("strategy must be string")
    if not isinstance(data["decisions"], list):
        raise TypeError("decisions must be list")
    if not isinstance(data["stop_condition"], str):
        raise TypeError("stop_condition must be string")

    for item in data["decisions"]:
        if not isinstance(item, str):
            raise TypeError("Each decision must be a string")

    return data