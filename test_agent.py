from ollama import chat
import re

system_prompt = """
You are the Test Agent. Generate pytest-style tests for the decide_next_move(state) function.
Input: requirements, plan, source code of decide_next_move.
Output ONLY raw python test code. No markdown ``` fences.
The test code must:
1. Import decide_next_move from navigation_logic
2. Include multiple test cases with assert statements
3. Cover all possible scenarios (forward, left, right, stop)
4. No extra explanation text, only python code.
"""

def validate_test_code(code: str) -> bool:
    if not isinstance(code, str) or len(code.strip()) == 0:
        return False
    if "```" in code:
        return False
    if "import" not in code or "assert" not in code:
        return False
    return True

def run_test_agent(requirements: dict, plan: dict, nav_code: str) -> str:
    user_msg = f"""
Requirements:
{requirements}

Plan:
{plan}

navigation_logic source code:
{nav_code}
"""
    resp = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )
    generated_code = resp["message"]["content"]
    if not validate_test_code(generated_code):
        raise ValueError("Generated test code failed validation")
    return generated_code
