AI:
1. Prompt text
2. `subprocess.run()` calls an external script
3. a complete multi-agent conditional iterative closed-loop pipeline
4. `compile()` dynamically compiles Python code in string format for syntax verification.
5. Multiple sets of regular expressions are used to clean the dirty output of the LLM (Markdown, lists, special symbols filtering).
6. Retry + fallback fallback mechanism to prevent the pipeline from crashing.
7. Revision logic, passing in the review report to allow the large model to fix the code.
8. Generate pytest test code automatically by a large model
9. A hybrid review method that combines deterministic hard-coded rules with LLM rewriting of text
10. `subprocess` is used to call external scripts to capture the stdout output.
11. `ast.literal_eval()` is used to parse string dictionaries.
12. Iris simulation library, numpy, matplotlib for visualization
13. Fallback default_code - Backup navigation code