import dotenv
from openai import OpenAI
import os
# Load environment variables from .env file if it exists
dotenv.load_dotenv()
from system_prompt.code_helpers import PROMPT_FOR_CODE
# Verify that required environment variables are set
required_vars = ['OPENAI_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"Warning: The following environment variables are missing: {', '.join(missing_vars)}")
else:
    print("All required environment variables are set!")
client = OpenAI()

system_prompt = PROMPT_FOR_CODE
filename="tools/write_code"
mycode = ""
with open(f"{filename}.py", "r", encoding="utf-8") as file:
    mycode = file.read()
user_prompt = f"{system_prompt}\nNow provide the breakdown for the given python file:\n{mycode}"

model = "o3-mini"#,"o1-mini"]
efforts = ["low","medium","high"]
for effort in efforts:
    response = client.chat.completions.create(
        model=  model,
        reasoning_effort=effort,
        messages=[
            # {"role": "developer", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    # print the number of output tokens

    code_string = response.choices[0].message.content   # Extract just the Python code from markdown code block if present
    # write to markdown file
    with open(f"{filename}_{model}_{effort}.md", "w" ,encoding="utf-8") as file:
        file.write(code_string)
    print(f"Model: {model}")
    print(f"Tokens: {response.usage.completion_tokens}")
