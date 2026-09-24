from planner_agent import run_planner
import json
import os

def main():
    with open("artifacts/requirements.json","r",encoding="utf-8") as f:
        req_data = json.load(f)

    plan_result = run_planner(req_data)

    os.makedirs("artifacts", exist_ok=True)
    out_path = os.path.join("artifacts","plan.json")
    with open(out_path,"w",encoding="utf-8") as fw:
        json.dump(plan_result, fw, indent=4)

    print("==== test_planner finished ====")
    print(json.dumps(plan_result,indent=2))

if __name__ == "__main__":
    main()