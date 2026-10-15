import ollama
import re

def run_developer(plan_data, requirement_data):
    prompt = f"""
YOU MUST NOT WRITE ANY EXPLANATIONS, NO INTRO SENTENCES, NO SUMMARY TEXT.
NO MARKDOWN AT ALL. NO TABLES, NO BOLD TEXT, NO BULLET POINTS, NO NUMBERED LISTS (1. / 2. /3.).
OUTPUT ONLY RAW PYTHON CODE. NO ```python / ``` markdown tags, NO --- separators.
MANDATORY:
Your output MUST START DIRECTLY WITH:
def decide_next_move(state):
Function input: state dictionary with keys goal_ahead, goal_on_left, goal_on_right, front_blocked, left_blocked, right_blocked.
Return ONLY one string: "FORWARD", "LEFT", "RIGHT", "STOP".
You can add helper functions AFTER this main function.
DO NOT USE UNICODE ARROW CHARACTERS SUCH AS →, ←, ↓, ↑. ONLY USE ASCII CHARACTERS.
NO NATURAL LANGUAGE AFTER THE CODE. ONLY PYTHON CODE.
DO NOT WRITE ANY TOP-LEVEL CODE, NO print(), NO function calls outside functions. ONLY FUNCTION DEFINITIONS.
Robot requirements:
{requirement_data}
Navigation plan:
{plan_data}
"""
    max_retry = 2
    for attempt in range(max_retry):
        resp = ollama.chat(
            model="qwen3:8b",
            messages=[{"role":"user", "content": prompt}]
        )
        raw_output = resp["message"]["content"]
        code_str = re.sub(r"```[^\n]*\n", "", raw_output)
        code_str = re.sub(r"\n```", "", code_str)
        code_str = re.sub(r"^---$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^\|.*$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^-.*$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^\d+\..*$", "", code_str, flags=re.MULTILINE)
        code_str = code_str.replace("→", "").replace("←", "").replace("↑", "").replace("↓", "")
        code_str = re.sub(r"^print\(.*\)$", "", code_str, flags=re.MULTILINE)
        match_index = code_str.find("def decide_next_move(state):")
        if match_index == -1:
            continue
        code_str = code_str[match_index:]
        lines = code_str.splitlines()
        kept_lines = []
        for line in lines:
            stripped = line.strip()
            if re.match(r"^\d+\.", stripped):
                continue
            if len(stripped) > 0 and stripped[0].isupper() and not stripped.startswith("#"):
                break
            kept_lines.append(line)
        code_str = "\n".join(kept_lines)
        try:
            validate_developer_output(code_str)
            return code_str
        except Exception:
            continue
    print("WARNING: LLM initial code generation failed, fallback to default navigation code")
    default_code = """def decide_next_move(state):
    if state["goal_ahead"] and not state["front_blocked"]:
        return "FORWARD"
    elif state["goal_on_left"] and not state["left_blocked"]:
        return "LEFT"
    elif state["goal_on_right"] and not state["right_blocked"]:
        return "RIGHT"
    elif state["front_blocked"]:
        return "LEFT"
    return "FORWARD"
"""
    return default_code


def run_developer_revision(old_code, review_notes, simulation_report, requirement_data, plan_data):
    prompt = f"""
YOU MUST NOT WRITE ANY EXPLANATIONS, NO INTRO SENTENCES, NO SUMMARY TEXT.
NO MARKDOWN AT ALL. NO TABLES, NO BOLD TEXT, NO BULLET POINTS, NO NUMBERED LISTS (1. / 2. /3.).
OUTPUT ONLY RAW PYTHON CODE. NO ```python / ``` markdown tags, NO --- separators.
MANDATORY:
Your output MUST START DIRECTLY WITH:
def decide_next_move(state):
Function input: state dictionary with keys goal_ahead, goal_on_left, goal_on_right, front_blocked, left_blocked, right_blocked.
Return ONLY one string: "FORWARD", "LEFT", "RIGHT", "STOP".
TASK: Fix the navigation logic. Read simulation report.
If robot failed to reach targets, fix path planning and obstacle avoidance.
If robot can reach targets but uses too many steps, reduce total steps and improve efficiency.
Fix the old navigation code according to review notes and simulation report.
DO NOT USE UNICODE ARROW CHARACTERS SUCH AS →, ←, ↓, ↑. ONLY USE ASCII CHARACTERS.
NO NATURAL LANGUAGE AFTER THE CODE. ONLY PYTHON CODE.
DO NOT WRITE ANY TOP-LEVEL CODE, NO print(), NO function calls outside functions. ONLY FUNCTION DEFINITIONS.
Old code:
{old_code}
Review notes:
{review_notes}
Simulation report:
{simulation_report}
Robot requirements:
{requirement_data}
Navigation plan:
{plan_data}
"""
    max_retry = 2
    for attempt in range(max_retry):
        resp = ollama.chat(
            model="qwen3:8b",
            messages=[{"role":"user", "content": prompt}]
        )
        raw_output = resp["message"]["content"]
        code_str = re.sub(r"```[^\n]*\n", "", raw_output)
        code_str = re.sub(r"\n```", "", code_str)
        code_str = re.sub(r"^---$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^\|.*$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^-.*$", "", code_str, flags=re.MULTILINE)
        code_str = re.sub(r"^\d+\..*$", "", code_str, flags=re.MULTILINE)
        code_str = code_str.replace("→", "").replace("←", "").replace("↑", "").replace("↓", "")
        code_str = re.sub(r"^print\(.*\)$", "", code_str, flags=re.MULTILINE)
        match_index = code_str.find("def decide_next_move(state):")
        if match_index == -1:
            continue
        code_str = code_str[match_index:]
        lines = code_str.splitlines()
        kept_lines = []
        for line in lines:
            stripped = line.strip()
            if re.match(r"^\d+\.", stripped):
                continue
            if len(stripped) > 0 and stripped[0].isupper() and not stripped.startswith("#"):
                break
            kept_lines.append(line)
        code_str = "\n".join(kept_lines)
        try:
            validate_developer_output(code_str)
            return code_str
        except Exception:
            continue
    print("WARNING: LLM revision generation failed after max retries, fallback to original navigation code")
    return old_code

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
