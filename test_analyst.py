from analyst_agent import run_analyst
import json
import os

def main():
    with open("brief.txt","r",encoding="utf-8") as f:
        brief_text = f.read()

    req_result = run_analyst(brief_text)

    os.makedirs("artifacts", exist_ok=True)
    out_path = os.path.join("artifacts","requirements.json")
    with open(out_path,"w",encoding="utf-8") as fw:
        json.dump(req_result, fw, indent=4)

    print("==== test_analyst finished ====")
    print(json.dumps(req_result,indent=2))

if __name__ == "__main__":
    main()