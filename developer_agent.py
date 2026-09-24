import ollama
import re

def run_developer(plan_data):
    prompt = f"""
YOU MUST NOT WRITE ANY EXPLANATIONS, NO INTRO SENTENCES, NO SUMMARY TEXT.
OUTPUT ONLY RAW PYTHON CODE. NO ```python / ``` markdown tags.

MANDATORY:
Your output MUST START DIRECTLY WITH:
def decide_next_move(state):
Function input: state dictionary with keys goal_ahead, goal_on_left, goal_on_right, front_blocked, left_blocked, right_blocked.
Return ONLY one string: "FORWARD", "LEFT", "RIGHT", "STOP".
You can add helper functions AFTER this main function.

Navigation plan:
{plan_data}
"""
    resp = ollama.chat(
        model="qwen3:8b",
        messages=[{"role":"user", "content": prompt}]
    )
    raw_output = resp["message"]["content"]

    # 清除markdown标记
    code_str = re.sub(r"```[^\n]*\n", "", raw_output)
    code_str = re.sub(r"\n```", "", code_str)

    # 关键修复：找到 def decide_next_move(state): 这一行，丢弃它前面所有废话
    match_index = code_str.find("def decide_next_move(state):")
    if match_index != -1:
        code_str = code_str[match_index:]

    validate_developer_output(code_str)
    return code_str


def validate_developer_output(code_str):
    if not isinstance(code_str, str):
        raise TypeError("Output must be code string")
    try:
        compile(code_str, filename="<generated_code>", mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Generated python code has syntax error: {e}")
    if "def decide_next_move(state):" not in code_str:
        raise ValueError("Missing required function: def decide_next_move(state):")
    return code_str