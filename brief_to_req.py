import ollama

with open("brief.txt", "r", encoding="utf-8") as f:
    brief_content = f.read()

prompt = f"""
You are a requirements analyst agent.
Convert the robot navigation brief into pure JSON output.
Do NOT add any extra text, explanations or markdown.
Strictly follow this JSON structure:
{{
    "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
    "goal": "string",
    "safe_stop": boolean,
    "avoid_obstacles": boolean
}}

allowed_actions can only contain FORWARD, LEFT, RIGHT, STOP.

Brief text:
{brief_content}
"""

response = ollama.chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": prompt}]
)

result_text = response["message"]["content"]

with open("robot_requirements.txt", "w", encoding="utf-8") as outfile:
    outfile.write(result_text)

print("Output saved to robot_requirements.txt")
print(result_text)