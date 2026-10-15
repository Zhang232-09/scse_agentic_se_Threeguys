from ollama import chat
import json

system_prompt = """
You are Benchmark Reviewer Agent. Analyze IR-SIM benchmark report.
Output ONLY valid JSON with keys:
"issue", "likely_cause", "recommendation", "safety_passed", "goal_completion_passed", "efficiency_passed", "needs_revision".
- safety_passed, goal_completion_passed, efficiency_passed, needs_revision: boolean
- Others: string
No explanation, no markdown, only pure JSON.
"""

def validate_benchmark_review(data: dict) -> bool:
    required_keys = {
        "issue", "likely_cause", "recommendation",
        "safety_passed", "goal_completion_passed",
        "efficiency_passed", "needs_revision"
    }
    if not isinstance(data, dict):
        return False
    if not required_keys.issubset(data.keys()):
        return False
    bool_fields = ["safety_passed", "goal_completion_passed", "efficiency_passed", "needs_revision"]
    for f in bool_fields:
        if not isinstance(data[f], bool):
            return False
    str_fields = ["issue", "likely_cause", "recommendation"]
    for f in str_fields:
        if not isinstance(data[f], str):
            return False
    return True

def build_deterministic_review(bench_report: dict) -> dict:
    safety_passed = True
    goal_completion_passed = True
    efficiency_passed = True
    issue = ""
    likely_cause = ""
    recommendation = ""
    needs_revision = False

    worlds = bench_report.get("world_results", [])
    for w in worlds:
        if w.get("collision_or_done") and not w.get("reached_goal"):
            safety_passed = False
            issue = "Unsafe benchmark behavior detected"
            likely_cause = "Robot collided with obstacle before reaching destination."
            recommendation = "Add obstacle avoidance logic in decide_next_move."
            needs_revision = True

    success_rate = bench_report.get("success_rate", 1.0)
    if success_rate < 1.0:
        goal_completion_passed = False
        issue = "Goal completion failure"
        likely_cause = "Some environments failed to reach target."
        recommendation = "Tune navigation logic to reliably reach goals."
        needs_revision = True

    inefficient = bench_report.get("inefficient_success_worlds", 0)
    eff_rate = bench_report.get("efficiency_rate", 1.0)
    if inefficient > 0 or eff_rate < 1.0:
        efficiency_passed = False
        issue = "Successful but inefficient navigation"
        likely_cause = "Robot took extra steps to reach goal."
        recommendation = "Shorten path planning logic."
        needs_revision = True

    return {
        "issue": issue,
        "likely_cause": likely_cause,
        "recommendation": recommendation,
        "safety_passed": safety_passed,
        "goal_completion_passed": goal_completion_passed,
        "efficiency_passed": efficiency_passed,
        "needs_revision": needs_revision
    }

def run_benchmark_reviewer(benchmark_report: dict) -> dict:
    deterministic = build_deterministic_review(benchmark_report)
    user_msg = f"""
Benchmark report:
{json.dumps(benchmark_report, indent=2)}
Deterministic pass/fail result:
{json.dumps(deterministic, indent=2)}
Keep all boolean values from deterministic result, rewrite the text description.
"""
    resp = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )
    raw = resp["message"]["content"]
    result = json.loads(raw)
    result["safety_passed"] = deterministic["safety_passed"]
    result["goal_completion_passed"] = deterministic["goal_completion_passed"]
    result["efficiency_passed"] = deterministic["efficiency_passed"]
    result["needs_revision"] = deterministic["needs_revision"]
    if not validate_benchmark_review(result):
        raise ValueError("Benchmark reviewer output schema invalid")
    return result
