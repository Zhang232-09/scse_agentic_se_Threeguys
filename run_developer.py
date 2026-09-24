import os
import json
from developer_agent import run_developer

def main():
    with open("artifacts/plan.json","r",encoding="utf-8") as f:
        plan = json.load(f)

    nav_code = run_developer(plan)

    os.makedirs("artifacts", exist_ok=True)
    output_file = os.path.join("artifacts","navigation_logic.py")
    with open(output_file,"w",encoding="utf-8") as fw:
        fw.write(nav_code)

    print(f"Navigation logic code saved to {output_file}")

if __name__ == "__main__":
    main()