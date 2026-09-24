import ollama

def run_developer(plan_data):
    prompt = f"""
You are a robot software developer agent.
Given robot navigation plan, output ONLY complete runnable Python source code.
Do NOT add ```python markdown markers, do not add explanation text outside code.
The generated code must contain at least one robot‑navigation related function.

Navigation plan:
{plan_data}
"""
    resp = ollama.chat(
        model="qwen3:8b",
        messages=[{"role":"user", "content": prompt}]
    )
    code_str = resp["message"]["content"]
    validate_developer_output(code_str)
    return code_str


def validate_developer_output(code_str):
    if not isinstance(code_str, str):
        raise TypeError("Output must be code string")
    # 仅语法检查，不执行代码
    try:
        compile(code_str, filename="<generated_code>", mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Generated python code has syntax error: {e}")

    # 简单检查：至少出现def函数定义，确保存在导航函数
    if "def " not in code_str:
        raise ValueError("Generated code must contain at least one function definition")

    return code_str