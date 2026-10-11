import json
import os
import subprocess
from analyst_agent import run_analyst
from planner_agent import run_planner
from developer_agent import run_developer, run_developer_revision
from test_agent import run_test_agent
from reviewer_agent import run_reviewer
from reviewer_benchmark_agent import run_benchmark_reviewer

def log_event(log_file, agent_name, action):
    msg = f"{agent_name}: {action}"
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def main():
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    log_path = os.path.join(artifacts_dir, "trace.log")
    log_event(log_path, "System", "Initialising pipeline and creating artifacts folder")

    # Load brief
    with open("brief.txt", "r", encoding="utf-8") as f:
        brief_text = f.read()
    log_event(log_path, "System", "Loaded brief.txt")

    # Run Analyst agent
    requirements = run_analyst(brief_text)
    req_path = os.path.join(artifacts_dir, "requirements.json")
    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(requirements, f, indent=2)
    log_event(log_path, "Analyst Agent", "Generated requirements.json")

    # Run Planner agent
    plan = run_planner(requirements)
    plan_path = os.path.join(artifacts_dir, "plan.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    log_event(log_path, "Planner Agent", "Generated plan.json")

    # Run Developer agent (original first version)
    nav_code = run_developer(requirements, plan)
    nav_path = os.path.join(artifacts_dir, "navigation_logic.py")
    with open(nav_path, "w", encoding="utf-8") as f:
        f.write(nav_code)
    log_event(log_path, "Developer Agent", "Generated navigation_logic.py")

    # Run Test Agent
    test_code = run_test_agent(requirements, plan, nav_code)
    test_script_path = os.path.join(artifacts_dir, "test_decide_next_move.py")
    with open(test_script_path, "w", encoding="utf-8") as f:
        f.write(test_code)
    log_event(log_path, "Test Agent", "Generated pytest test script test_decide_next_move.py")

    # Run Simulation runner (runner.py, outputs simulation_report.json)
    subprocess.run(["python", "runner.py"], check=True)
    log_event(log_path, "Simulation Runner", "Simulation completed, simulation_report.json saved")

    # Run Reviewer Agent
    sim_report_path = os.path.join(artifacts_dir, "simulation_report.json")
    with open(sim_report_path, "r", encoding="utf-8") as f:
        sim_report_data = json.load(f)
    review_result = run_reviewer(sim_report_data)
    review_path = os.path.join(artifacts_dir, "review_report.json")
    with open(review_path, "w", encoding="utf-8") as f:
        json.dump(review_result, f, indent=2)
    log_event(log_path, "Reviewer Agent", "Generated review_report.json from simulation report")

    # Run IRSIM benchmark
    subprocess.run(["python", "benchmark_irsim.py"], check=True)
    log_event(log_path, "IRSIM Benchmark", "IRSIM benchmark finished, benchmark report generated")

    # Run Benchmark Reviewer
    bench_report_path = os.path.join(artifacts_dir, "irsim_benchmark_report.json")
    with open(bench_report_path, "r", encoding="utf-8") as f:
        bench_report_data = json.load(f)
    bench_review_result = run_benchmark_reviewer(bench_report_data)
    bench_review_path = os.path.join(artifacts_dir, "benchmark_review_report.json")
    with open(bench_review_path, "w", encoding="utf-8") as f:
        json.dump(bench_review_result, f, indent=2)
    log_event(log_path, "Benchmark Reviewer", "Generated benchmark_review_report.json")


    # Read benchmark result to decide whether we need revision
    with open(os.path.join(artifacts_dir, "irsim_benchmark_report.json"), "r", encoding="utf-8") as f:
        bench_data_check = json.load(f)

    if bench_data_check["efficiency_rate"] == 1.0:
        log_event(log_path, "System", "Benchmark result already fully efficient, skip revision iteration")
    else:
        log_event(log_path, "System", "Starting revision iteration based on benchmark review")

        # Load all required inputs for revision
        with open(os.path.join(artifacts_dir, "navigation_logic.py"), "r", encoding="utf-8") as f:
            old_nav_code = f.read()
        with open(os.path.join(artifacts_dir, "review_report.json"), "r", encoding="utf-8") as f:
            sim_review_notes = json.load(f)
        with open(os.path.join(artifacts_dir, "simulation_report.json"), "r", encoding="utf-8") as f:
            sim_report = json.load(f)
        with open(os.path.join(artifacts_dir, "irsim_benchmark_report.json"), "r", encoding="utf-8") as f:
            benchmark_report = json.load(f)
        with open(os.path.join(artifacts_dir, "benchmark_review_report.json"), "r", encoding="utf-8") as f:
            benchmark_review_notes = json.load(f)

        # Call developer revision function
        revised_nav_code = run_developer_revision(
            old_code=old_nav_code,
            review_notes=benchmark_review_notes,
            simulation_report=sim_report,
            requirement_data=requirements,
            plan_data=plan
        )

        # Overwrite navigation_logic with revised version
        with open(nav_path, "w", encoding="utf-8") as f:
            f.write(revised_nav_code)
        log_event(log_path, "Developer Agent", "Saved revised navigation_logic.py from run_developer_revision")

        # Re-run Test Agent on revised code
        revised_test_code = run_test_agent(requirements, plan, revised_nav_code)
        revised_test_path = os.path.join(artifacts_dir, "test_decide_next_move_revised.py")
        with open(revised_test_path, "w", encoding="utf-8") as f:
            f.write(revised_test_code)
        log_event(log_path, "Test Agent", "Generated revised pytest test_decide_next_move_revised.py")

        # Re-run simulation runner and save revised report
        subprocess.run(["python", "runner.py"], check=True)
        # rename to preserve original simulation report
        os.rename(
            os.path.join(artifacts_dir, "simulation_report.json"),
            os.path.join(artifacts_dir, "simulation_report_revised.json")
        )
        log_event(log_path, "Simulation Runner", "Re-run simulation completed, simulation_report_revised.json saved")

        # Re-run IRSIM benchmark and save revised benchmark report
        subprocess.run(["python", "benchmark_irsim.py"], check=True)
        os.rename(
            os.path.join(artifacts_dir, "irsim_benchmark_report.json"),
            os.path.join(artifacts_dir, "irsim_benchmark_report_revised.json")
        )
        log_event(log_path, "IRSIM Benchmark", "Re-run IRSIM benchmark finished, revised benchmark report generated")

        # Re-run Benchmark Reviewer for revised benchmark
        revised_bench_data_path = os.path.join(artifacts_dir, "irsim_benchmark_report_revised.json")
        with open(revised_bench_data_path, "r", encoding="utf-8") as f:
            revised_bench_data = json.load(f)
        revised_bench_review = run_benchmark_reviewer(revised_bench_data)
        revised_bench_review_path = os.path.join(artifacts_dir, "benchmark_review_report_revised.json")
        with open(revised_bench_review_path, "w", encoding="utf-8") as f:
            json.dump(revised_bench_review, f, indent=2)
        log_event(log_path, "Benchmark Reviewer", "Generated benchmark_review_report_revised.json")

        log_event(log_path, "System", "Revision iteration pipeline finished")


    log_event(log_path, "System", "Full end-to-end pipeline completed successfully")

if __name__ == "__main__":
    main()
