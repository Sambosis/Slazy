import asyncio
from pathlib import Path
from typing import ClassVar, Literal
from anthropic.types.beta import BetaToolBash20241022Param
import re
import os
import subprocess
import sys
import io
import traceback
from datetime import datetime
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from .base import BaseAnthropicTool, ToolError, ToolResult
from utils.agent_display import AgentDisplay  # Add this line
from load_constants import  write_to_file, ICECREAM_OUTPUT_FILE
from icecream import ic
from config import BASH_PROMPT_FILE, get_constant

ic.configureOutput(includeContext=True, outputFunction=write_to_file)



def read_prompt_from_file(file_path: str, bash_command: str) -> str:
    """Read the prompt template from a file and format it with the given bash command."""
    project_dir = Path(get_constant("PROJECT_DIR"))
    try:
        with open(file_path, "r", encoding='utf-8', errors='replace') as file:
            prompt_string = file.read()
        prompt_string += f"Your project directory is {project_dir}. You need to make sure that all files you create and work you do is done in that directory. \n"
        prompt_string += f"Your bash command is: {bash_command}\n"
        return prompt_string
    except Exception as e:
        return f"Error reading prompt file: {str(e)}"

def extract_code_block(text: str) -> tuple[str, str]:
    """
    Extract code from a markdown code block, detecting the language if specified.
    Returns tuple of (code, language).
    If no code block is found, returns the original text and empty string for language.
    """
    # Find all code blocks in the text
    code_blocks = []
    lines = text.split('\n')
    in_block = False
    current_block = []
    current_language = ''
    
    for line in lines:
        if line.startswith('```'):
            if in_block:
                # End of block
                in_block = False
                code_blocks.append((current_language, '\n'.join(current_block)))
                current_block = []
                current_language = ''
            else:
                # Start of block
                in_block = True
                # Extract language if specified
                current_language = line.strip('`').strip()
                if current_language == '':
                    current_language = 'unknown'
        elif in_block:
            current_block.append(line)
    
    # If we found code blocks, return the most relevant one
    # (currently taking the first non-empty block)
    for language, code in code_blocks:
        if code.strip():
            return code.strip(), language
            
    # If no code blocks found or all empty, return original text
    return text.strip(), ''

def generate_script_with_llm(prompt: str) -> str:
    """Send a prompt to the LLM and return its response."""

    try:
        ic(prompt)
        # 1. Create a client with custom endpoint
        client = OpenAI()

        # 2. Use it like normal OpenAI calls
        response = client.chat.completions.create(
            model="gpt-4o",  # Use model name your endpoint expects
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        ic(response)
        response_message = response.choices[0].message.content
        ic(response_message)
        return response_message
    except Exception as e:
        raise ToolError(f"Error during LLM API call: {e}")


def parse_llm_response(response: str):
    """Parse the LLM response to extract the script."""
    script_code, script_type = extract_code_block(response)
    # In case there is inconsistent capitalization we will convert to all lowercase
    script_type = script_type.lower()
    if script_type == 'python':
        script_type = 'Python Script'
    elif script_type == 'powershell':
        script_type = 'PowerShell Script'
    return script_type, script_code


def execute_script(script_type: str, script_code: str, display: AgentDisplay = None):
    """Execute the extracted script and capture output and errors."""
    output = ""

    if script_type == "Python Script":
        if display:
            display.add_message("user", "Executing Python script...")

        # Write the Python script to a temporary file with UTF-8 encoding
        script_file = "temp_script.py"
        try:
            with open(script_file, "w", encoding="utf-8", errors='replace') as f:
                f.write(script_code)

            # Use subprocess with UTF-8 encoding
            result = subprocess.run(
                ["python", script_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                check=False  # Don't automatically raise CalledProcessError
            )
            output_out = result.stdout
            error_out = result.stderr

            # Decide success based on return code
            success = (result.returncode == 0)

            # Send output to the display
            if display:
                if output_out:
                    display.add_message("user", f"Output:\n{output_out}")
                if error_out:
                    display.add_message("user", f"Error Message:\n{error_out}")

        except Exception as e:
            # Catch any unexpected Python-level errors from subprocess itself
            output_out = ""
            error_out = f"Error: {str(e)}\n{traceback.format_exc()}"
            success = False
            if display:
                display.add_message("user", f"Execution Error:\n{error_out}")
        finally:
            # Clean up the temporary file
            if os.path.exists(script_file):
                os.remove(script_file)

        return {
            "success": success,
            "output": output_out,
            "error": error_out
        }

    elif script_type == "PowerShell Script":
        if display:
            display.add_message("user", "Executing PowerShell script...")

        script_file = "temp_script.ps1"
        with open(script_file, "w", encoding="utf-8", errors='replace') as f:
            f.write(script_code)

        try:
            result = subprocess.run(
                ["powershell.exe", "-File", script_file],
                capture_output=True,
                text=True,
                check=False
            )
            output = result.stdout
            error = result.stderr
            success = (result.returncode == 0)

            if display and output:
                display.add_message("user", f"PowerShell Output:\n{output}")
            if display and error:
                display.add_message("user", f"PowerShell Errors:\n{error}")

        except Exception as e:
            output = ""
            error = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
            success = False
            if display:
                display.add_message("user", f"Unexpected Error:\n{error}")
        finally:
            if os.path.exists(script_file):
                os.remove(script_file)

        return {
            "success": success,
            "output": output,
            "error": error
        }

    else:
        error_msg = f"Unsupported script type: {script_type}"
        if display:
            display.add_message("user", f"Error: {error_msg}")
        raise ValueError(error_msg)


class BashTool(BaseAnthropicTool):
    def __init__(self, display: AgentDisplay = None):
        self.display = display
        super().__init__()

        
    description = """
        A tool that allows the agent to run bash commands. On Windows it uses PowerShell
        The tool parameters are defined by Anthropic and are not editable.
        """

    name: ClassVar[Literal["bash"]] = "bash"
    api_type: ClassVar[Literal["bash_20241022"]] = "bash_20241022"

    async def __call__(self, command: str | None = None, **kwargs):
        if command is not None:
            return await self._run_command(command)
        raise ToolError("no command provided.")

    async def _run_command(self, command: str):
        """Execute a command in the shell."""
        BASH_PROMPT_FILE= get_constant("BASH_PROMPT_FILE")
        output = ""
        try:
            if self.display:
                self.display.add_message("user", f"Processing command: {command}")
                await asyncio.sleep(0.2)

            prompt = read_prompt_from_file(BASH_PROMPT_FILE, command)
            response = generate_script_with_llm(prompt)
            self.display.add_message("user", f"response: {response}")
            await asyncio.sleep(0.2)
            script_type, script_code = parse_llm_response(response)

            # Pass the display to execute_script
            result = execute_script(script_type, script_code, self.display)

            if isinstance(result, dict):
                output = f"output: {result['output']}\nerror: {result['error']}"
            else:
                output = result
            return ToolResult(output=output)
        except Exception as e:
            if self.display:
                self.display.add_message("user", f"Error: {str(e)}")
            return ToolError(str(e))

    def to_params(self) -> BetaToolBash20241022Param:
        return {
            "type": self.api_type,
            "name": self.name,
        }


def save_successful_code(script_code: str) -> str:
    """Save successfully executed Python code to a file."""
    # Create directory if it doesn't exist
    llm_gen_code_dir = Path(get_constant("LLM_GEN_CODE_DIR"))
    save_dir = llm_gen_code_dir
    save_dir.mkdir(exist_ok=True)
    ic(script_code)
    # Extract first line of code for filename (cleaned)
    first_line = script_code.split("\n")[0].strip()
    # Clean the first line to create a valid filename
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", first_line)[:30]

    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{clean_name}_{timestamp}.py"

    # Save the code with UTF-8 encoding
    file_path = save_dir / filename
    with open(file_path, "w", encoding='utf-8', errors='replace') as f:
        f.write(script_code)

    return str(file_path)
