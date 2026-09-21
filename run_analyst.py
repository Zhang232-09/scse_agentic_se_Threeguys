from analyst_agent import run_analyst, validate_requirements
import os
import json

def main():
    with open("brief.txt", "r", encoding="utf-8") as f:
        brief = f.read()
    raw_response = run_analyst(brief)
    validated_data = validate_requirements(raw_response)
    os.makedirs("artifacts", exist_ok=True)
    output_path = os.path.join("artifacts", "requirements.json")
    with open(output_path, "w", encoding="utf-8") as file_out:
        json.dump(validated_data, file_out, indent=4)
    print("Saved validated requirements to artifacts/requirements.json")

if __name__ == "__main__":
    main()