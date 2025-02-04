import asyncio
from tools.write_code import WriteCodeTool
from pathlib import Path
from openai import OpenAI
import os
def call_llm_to_generate_code(code_description: str) -> str:
    """Call LLM to generate code based on the code description"""
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    # current_code_base = get_all_current_code()
    current_code_base = "No code has been written yet"
    messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Your are an expert with software engineer and proud coder.  You are make carefully designed programs that work on the first try and take the whole scope of the program into consideration when creating a piece of code."
                },
                ],
            "role": "user",
            "content": 
            [
                {
                "type": "text",
                "text": f"""At the bottom is a detailed description of code that you need to write.  Your response should include everything needed in order to run the file including imports that will be needed. All of the code that you provide needs to be enclosed in a single markdown style code block like this:
                ```python 
                your code here
                ```
                Here is all of the code that has been created for the project so far:
                {current_code_base}
                
                Here is the description of the code:
                {code_description}"""
                },
            ]
            }
        ]
    model = "gpt-4o"

    completion = client.chat.completions.create(
    model=model,
    messages=messages
    )
    print(completion)
    code_string = completion.choices[0].message.content
            # Extract just the Python code from markdown code block if present
    if "```python" in code_string:
        code_string = code_string.split("```python")[1].split("```")[0].strip()
    return code_string




import os
import libcst as cst

def scan_and_create_cst_for_py_files():
    # List all files in the current directory
    files = os.listdir('.')

    # Filter out non-Python files
    python_files = [f for f in files if f.endswith('.py')]

    for py_file in python_files:
        try:
            # Read the contents of the Python file
            with open(py_file, 'r', encoding='utf-8') as file:
                source_code = file.read()

            # Parse the source code into a CST
            cst_tree = cst.parse_module(source_code)

            # Print the CST to the console
            print(f"CST for {py_file}:\
")
            print(cst_tree)
           
        except Exception as e:
            print(f"Error processing {py_file}: {e}")
if __name__ == "__main__":
    scan_and_create_cst_for_py_files()



#     def main():
#     call_llm_to_generate_code("write python code that scans the currentdirectory to crate a cst  with libcst and print the output",)

# if __name__ == "__main__":
#     main()
#   return runner.run(main)

