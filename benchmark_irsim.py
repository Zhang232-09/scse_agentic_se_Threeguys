import json
import subprocess
import ast
import re
from pathlib import Path

# Load the world files for the IR-SIM benchmark.
# Create a function to run the IR-SIM benchmark for a given world file.
# It should call the test_irsim_with_agent.py script with the world file as an argument, capture the output, and extract the report from the output.
# Create a main function to run the IR-SIM benchmark for all world files and generate a summary report.
# The summary report should include the total number of worlds, the number of worlds where the goal was reached, the success rate, the number of efficient worlds, the number of inefficient but successful worlds, the number of failed worlds, the efficiency rate, and the average steps taken across all worlds. The report should be saved to a JSON file.
# The benchmark report must have the following structure:
# benchmark_report = {
#     "total_worlds": total,
#     "goals_reached": reached_goal_count,
#     "success_rate": reached_goal_count / total,
#     "efficient_worlds": efficient_count,
#     "inefficient_success_worlds": inefficient_success_count,
#     "failed_worlds": failed_count,
#     "efficiency_rate": efficient_count / total,
#     "average_steps_taken": average_steps,
#     "results": results
# }
# Save the benchmark report to a JSON file named "irsim_benchmark_report.json" under the artifacts folder, and print the report to the console in a readable format.

def run_single_world(world_file_path):
    result = subprocess.run(
        ["python", "test_irsim_with_agent.py", world_file_path],
        capture_output=True,
        text=True
    )
    output = result.stdout
    lines = output.strip().splitlines()
    last_line = lines[-1].strip()
    match = re.search(r"\{.*\}", last_line)
    if not match:
        raise RuntimeError(f"No dict found in output for {world_file_path}. Raw output:\n{output}")
    dict_str = match.group(0)
    #AI
    report_dict = ast.literal_eval(dict_str)
    return report_dict

def run_all_benchmark(world_files):
    total = len(world_files)
    reached_goal_count = 0
    efficient_count = 0
    inefficient_success_count = 0
    failed_count = 0
    total_steps = 0
    results = []
    for world_path in world_files:
        world_result = run_single_world(world_path)
        results.append(world_result)
        steps = world_result["steps_taken"]
        total_steps += steps
        if world_result["reached_goal"]:
            reached_goal_count += 1
            if world_result["efficiency_passed"]:
                efficient_count += 1
            else:
                inefficient_success_count += 1
        else:
            failed_count +=1
    success_rate = reached_goal_count / total if total > 0 else 0.0
    efficiency_rate = efficient_count / total if total >0 else 0.0
    average_steps = total_steps / total if total >0 else 0.0
    benchmark_report = {
        "total_worlds": total,
        "goals_reached": reached_goal_count,
        "success_rate": success_rate,
        "efficient_worlds": efficient_count,
        "inefficient_success_worlds": inefficient_success_count,
        "failed_worlds": failed_count,
        "efficiency_rate": efficiency_rate,
        "average_steps_taken": average_steps,
        "results": results
    }
    return benchmark_report

if __name__ == "__main__":
    world_file_list = [
    "irsim_worlds/world_easy.yaml",
    "irsim_worlds/world_medium.yaml",
    "irsim_worlds/world_hard.yaml",
    "irsim_worlds/world_custom.yaml"
    ]
    final_report = run_all_benchmark(world_file_list)
    Path("artifacts").mkdir(exist_ok=True)
    out_path = Path("artifacts") / "irsim_benchmark_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)
    print("IRSIM benchmark finished, benchmark report generated")
    print(json.dumps(final_report, indent=2))
