from developer_agent import run_developer
import json
import os

def main():
    with open("artifacts/plan.json","r",encoding="utf-8") as f:
        plan_data = json.load(f)

    nav_code = run_developer(plan_data)

    os.makedirs("artifacts", exist_ok=True)
    out_path = os.path.join("artifacts","navigation_logic.py")
    with open(out_path,"w",encoding="utf-8") as fw:
        fw.write(nav_code)

    print("==== test_developer finished ====")
    print("Generated code saved to artifacts/navigation_logic.py")
    if "def decide_next_move(state):" in nav_code:
        print(" Found required function decide_next_move(state):")
    else:
        print(" WARNING: decide_next_move(state): is missing! Rerun to regenerate code.")

if __name__ == "__main__":
    main()