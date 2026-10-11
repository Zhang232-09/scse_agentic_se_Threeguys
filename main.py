import json
import os
import subprocess
import sys

from analyst_agent import run_analyst
from planner_agent import run_planner
from developer_agent import run_developer


def log_event(agent_name, action):
    log_msg = f"{agent_name}: {action}"
    print(log_msg)
    with open(os.path.join("artifacts", "pipeline_log.txt"), "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")


def main():
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
        log_event("System", f"Created directory {artifacts_dir}")
    else:
        log_event("System", f"Directory {artifacts_dir} already exists")

    with open("brief.txt", "r", encoding="utf-8") as f:
        brief_text = f.read()

    requirements = run_analyst(brief_text)
    req_path = os.path.join(artifacts_dir, "requirements.json")
    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=2)
    log_event("Analyst Agent", "created requirements.json")

    plan = run_planner(requirements)
    plan_path = os.path.join(artifacts_dir, "plan.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    log_event("Planner Agent", "created plan.json")

    nav_code = run_developer(requirements, plan)
    nav_path = os.path.join(artifacts_dir, "navigation_logic.py")
    with open(nav_path, "w", encoding="utf-8") as f:
        f.write(nav_code)
    log_event("Developer Agent", "created navigation_logic.py")

    log_event("System", "Whole pipeline finished successfully")


if __name__ == "__main__":
    main()
