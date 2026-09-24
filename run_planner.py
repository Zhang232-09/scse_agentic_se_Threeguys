import json
import os
from planner_agent import run_planner

def main():
    
    with open("artifacts/requirements.json", "r", encoding="utf-8") as f:
        req_data = json.load(f)

    plan_result = run_planner(req_data)

    os.makedirs("artifacts", exist_ok=True)
    out_path = os.path.join("artifacts", "plan.json")
    with open(out_path, "w", encoding="utf-8") as f_out:
        json.dump(plan_result, f_out, indent=4)

    print(f"Plan saved to {out_path}")

if __name__ == "__main__":
    main()