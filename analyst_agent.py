import ollama
import json

def run_analyst(brief_text: str) -> dict:
    prompt = f"""
You are a requirements analyst.
Convert the given brief into pure JSON only.
No extra words, markdown or explanation.
Schema:
{{
    "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
    "goal": "string",
    "safe_stop": boolean,
    "avoid_obstacles": boolean
}}
allowed_actions can only contain FORWARD, LEFT, RIGHT, STOP.

Brief:
{brief_text}
"""
    response = ollama.chat(
        model="qwen3:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    json_text = response["message"]["content"]
    python_data = json.loads(json_text)
    validated_result = validate_requirements(python_data)
    return validated_result


def validate_requirements(data: dict) -> dict:
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    required_keys = {"allowed_actions", "goal", "safe_stop", "avoid_obstacles"}
    if set(data.keys()) != required_keys:
        raise ValueError("Missing required keys or contains extra keys")

    if not isinstance(data["allowed_actions"], list):
        raise TypeError("allowed_actions must be a list")
    if not isinstance(data["goal"], str):
        raise TypeError("goal must be a string")
    if not isinstance(data["safe_stop"], bool):
        raise TypeError("safe_stop must be boolean")
    if not isinstance(data["avoid_obstacles"], bool):
        raise TypeError("avoid_obstacles must be boolean")

    valid_action_set = {"FORWARD", "LEFT", "RIGHT", "STOP"}
    for action in data["allowed_actions"]:
        if action not in valid_action_set:
            raise ValueError(f"Invalid action value: {action}")

    return data