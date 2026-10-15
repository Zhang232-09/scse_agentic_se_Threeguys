import json
from pathlib import Path

Path("artifacts").mkdir(exist_ok=True)

from artifacts.navigation_logic import decide_next_move

def run_simulation():
    scenarios = [
        {
            "state": {"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
                      "front_blocked": False, "left_blocked": False, "right_blocked": False},
            "expected": "FORWARD"
        },
        {
            "state": {"goal_ahead": False, "goal_on_left": True, "goal_on_right": False,
                      "front_blocked": True, "left_blocked": False, "right_blocked": False},
            "expected": "LEFT"
        },
        {
            "state": {"goal_ahead": False, "goal_on_left": False, "goal_on_right": True,
                      "front_blocked": True, "left_blocked": False, "right_blocked": False},
            "expected": "RIGHT"
        },
        {
            "state": {"goal_ahead": False, "goal_on_left": False, "goal_on_right": False,
                      "front_blocked": True, "left_blocked": True, "right_blocked": True},
            "expected": "STOP"
        }
    ]

    results = []
    passed = 0
    failed = 0

    for s in scenarios:
        state = s["state"]
        expected = s["expected"]
        actual = decide_next_move(state)
        is_pass = (actual == expected)
        if is_pass:
            passed += 1
        else:
            failed += 1
        results.append({
            "state": state,
            "expected": expected,
            "actual": actual,
            "pass": is_pass
        })

    total = len(scenarios)
    success_rate = passed / total if total > 0 else 0.0

    report = {
        "total_scenarios": total,
        "passed_scenarios": passed,
        "failed_scenarios": failed,
        "success_rate": success_rate,
        "scenario_details": results
    }
    return report

if __name__ == "__main__":
    sim_report = run_simulation()
    out_path = Path("artifacts") / "simulation_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sim_report, f, indent=2)
    print("Simulation completed, simulation_report.json saved")
