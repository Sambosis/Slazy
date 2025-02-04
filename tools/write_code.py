import asyncio
from enum import Enum
from typing import Literal, Optional, List
from pathlib import Path
from .base import ToolResult, BaseAnthropicTool
import os
import subprocess
from icecream import ic
from rich import print as rr
import json
from pydantic import BaseModel
import tempfile
from load_constants import write_to_file, ICECREAM_OUTPUT_FILE
from tenacity import retry, stop_after_attempt, wait_fixed
from config import get_constant, set_constant, PROJECT_DIR, LOGS_DIR
from openai import OpenAI
from utils.file_logger import log_file_operation, get_all_current_code
import time
from dotenv import load_dotenv
load_dotenv()
ic.configureOutput(includeContext=True, outputFunction=write_to_file)
class CodeCommand(str, Enum):
    WRITE_CODE_TO_FILE = "write_code_to_file"
    WRITE_AND_EXEC = "write_and_exec"

import time
import json

def write_chat_completion_to_file(response, filepath):
    """Appends an OpenAI ChatCompletion object to a file in a human-readable format."""

    try:
        with open(filepath, 'a', encoding='utf-8') as f:


            f.write(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(response.get('created', 0)))}\n")
            f.write(f"Model: {response.get('model', 'N/A')}\n")

            f.write("\nUsage:\n")
            usage = response.get("usage", {})
            for key, value in usage.items():
                if isinstance(value, dict):  # Nested details
                    f.write(f"  {key}:\n")
                    for k, v in value.items():
                        f.write(f"    {k}: {v}\n")
                else:
                    f.write(f"  {key}: {value}\n")

            f.write("\nChoices:\n")
            for i, choice in enumerate(response.get("choices", [])):
                f.write(f"  Choice {i+1}:\n")
                f.write(f"    Index: {choice.get('index', 'N/A')}\n")
                f.write(f"    Finish Reason: {choice.get('finish_reason', 'N/A')}\n")

                message = choice.get('message', {})
                if message:
                    f.write("    Message:\n")
                    f.write(f"      Role: {message.get('role', 'N/A')}\n")
                    f.write(f"      Content: {message.get('content', 'None')}\n")
                    
                    if 'refusal' in message:
                        f.write(f"      Refusal: {message['refusal']}\n")


                f.write("\n")

    except Exception as e:
        print(f"Error writing to file: {e}")


class WriteCodeTool(BaseAnthropicTool):
    """
    A tool that sets up Python projects with virtual environments and manages script execution.
    """

    name: Literal["write_code"] = "write_code"
    api_type: Literal["custom"] = "custom"
    description: str = "A tool that takes a description of code that needs to be written and provides the actual programming code in the specified language. It can either execute the code or write it to a file depending on the command."

    def __init__(self, display=None):
        super().__init__(display)

    def to_params(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "type": self.api_type,
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": [cmd.value for cmd in CodeCommand],
                        "description": "Command of what to do with the code: write_code_to_file or write_and_exec"
                    },
                    "code_description": {
                        "type": "string",
                        "description": "A detailed description of the code to be written. First speify the programming language that the code must be written in.  Then you must specify any additional imports, classes, functions, etc. that should be included in the code. If it needs to call functions from outside of the file requested, be specific and detailed about how they should be called. It also will need to know what files it may need to interact with, their paths and the directory structure. It should also give a brief description of the project as a whole, while being clear about the scope of the code that it needs to write."
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Path to the project directory"
                    },
                    "python_filename": {
                        "type": "string",
                        "description": "The filename of the file to write the code to.  This is only needed if the command is write_code_to_file, but if write_code_to_file is the command, this is required."
                    }
                },
                "required": ["command", "code_description", "project_path"]
            }
        }

    async def __call__(
        self,
        *,
        command: CodeCommand,
        code_description: str,
        project_path: str = PROJECT_DIR,
        python_filename: str = "you_need_to_name_me.py",
        **kwargs,
        ) -> ToolResult:
        """
        Executes the specified command for project management.
        """
        ic()
        try:
            if self.display is not None:
                self.display.add_message("tool", f"WriteCodeTool Instructions: {code_description}")
                await asyncio.sleep(0.2)

            # Convert path string to Path object
            project_path = Path(get_constant("PROJECT_DIR"))
            # Execute the appropriate command
            if command == CodeCommand.WRITE_CODE_TO_FILE:
                result_data = await self.write_code_to_file(code_description, project_path, python_filename)
                ic(f"result_data: {result_data}")
            elif command == CodeCommand.WRITE_AND_EXEC:
                result_data = await self.write_and_exec(code_description, project_path)
                ic(f"result_data: {result_data}")

            else:
                ic(f"Unknown command: {command}")
                return ToolResult(error=f"Unknown command: {command}")


            # Convert result_data to formatted string   
            formatted_output = self.format_output(result_data)
            ic(f"formatted_output: {formatted_output}")
            if self.display is not None:
                self.display.add_message("tool", f"WriteCodeTool completed: {formatted_output}")
                await asyncio.sleep(0.2)
            return ToolResult(output=formatted_output)

        except Exception as e:
            await asyncio.sleep(0.2)
            if self.display is not None:
                self.display.add_message("tool", f"WriteCodeTool error: {str(e)}")
            await asyncio.sleep(0.2)
            error_msg = f"Failed to execute {command}: {str(e)}"
            
            return ToolResult(error=error_msg)

    def extract_code_block(self, text: str) -> tuple[str, str]:
        """
        Extracts the first code block in the text with its language.
        If no code block is found, returns the full text and language "code".
        If text is empty, returns "No Code Found" and language "Unknown".
        """
        if not text.strip():
            return "No Code Found", "Unknown"
        
        start_marker = text.find("```")
        if start_marker == -1:
            return text, "code"
        
        # Determine language (text immediately after opening delimiter)
        language_line_end = text.find("\n", start_marker)
        if language_line_end == -1:
            language_line_end = start_marker + 3
        language = text[start_marker+3:language_line_end].strip()
        if not language:
            language = "code"
        
        end_marker = text.find("```", language_line_end)
        if end_marker == -1:
            code_block = text[language_line_end:].strip()
        else:
            code_block = text[language_line_end:end_marker].strip()
        
        return code_block if code_block else "No Code Found", language


    async def _call_llm_to_generate_code(self, code_description: str, research_string: str, file_path) -> str:
        """Call LLM to generate code based on the code description"""
        code_string="no code created"
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        current_code_base = get_all_current_code()
        ic(f"current_code_base: {current_code_base}")

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        
        # Prepare messages
        messages = [
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Your are an expert with software engineer and proud coder.  You are make carefully designed programs that work on the first try and take the whole scope of the program into consideration when creating a piece of code. You are well versed in many programming lanaguages"
                },
                ],
            "role": "user",
            "content": 
            [
                {
                "type": "text",
                "text": f"""At the bottom is a detailed description of code that you need to write. Flollow up by an expert review that gives some valuable suggestions. 
                Make sure you provide your response in the requested programming lanaguage. Your response should include everything needed in order to run the file including imports that will be needed.
                All of the code that you provide needs to be enclosed in a single markdown style code block with the language specified.
                Here is an example of what your response should look like:
                ```python
                # Your code goes here
                ```
                If it was javascript it would look like this:
                ```javascript
                // Your code goes here
                ```
                Here is all of the code that has been created for the project so far:
                {current_code_base}
                
                Here is the description of the code:
                {code_description}
                Here is the research that was done:
                {research_string}
                """
                },
            ]
            }
        ]
        ic(messages)
        
        try:
            completion = client.chat.completions.create(
            # model="deepseek/deepseek-r1:nitro",
            model = "openai/o1-mini",
            messages=messages)
        except Exception as e:
            ic(f"error: {e}")
            return code_description
            
        ic(completion)

        code_string = completion.choices[0].message.content

        # Extract code using the new function
        try:
            code_string, detected_language = self.extract_code_block(code_string)
            ic(f"Code String: {code_string}\nLanguage: {detected_language}")
        except Exception as parse_error:
            error_msg = f"Failed to parse code block: {str(parse_error)}"
            if self.display is not None:
                try:
                    self.display.add_message("tool", error_msg)
                except Exception as display_error:
                    return ToolResult(error=f"{error_msg}\nFailed to display error: {str(display_error)}")

            raise ToolResult(code_string)
        
        # Log the extraction
        try:
            CODE_FILE = Path(get_constant("CODE_FILE"))
            with open(CODE_FILE, "a") as f:
                f.write(str(file_path))
                f.write("\n")
                f.write(f"Language detected: {detected_language}\n")
                f.write(code_string)
                f.write("\n")
        except Exception as file_error:
            # Log failure but don't stop execution
            if self.display is not None:
                try:
                    self.display.add_message("warning", f"Failed to log code: {str(file_error)}")
                except Exception:
                    pass
        
        return code_string

  

    async def _call_llm_to_review_code(self, code_description: str, file_path) -> str:
        """Call LLM to generate code based on the code description"""

        code_string="no code created"
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        current_code_base = get_all_current_code()
        ic(f"current_code_base: {current_code_base}")
        
        client2 = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        ic()
        
        # Prepare messages
        messages=[
                {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": """Your are an expert with software engineer and proud researcher.  You review code projects for Programmers and try to help them by giving them insight into the best approaches to accomplish their task.
                    You try to anticipate common bugs, inefficiencies and suggest improvements to the origninal specs to add advanced performance and functionality.
                    by  carefully reviewing programs that submittied you and sending them back a detailed report with suggesions of the best ways to accomplish their task.
                    
                    Youd take the whole scope of the program into consideration when reviewing their task description."""
                    },
                    ],
                "role": "user",
                "content": [
                    {
                        
                    "type": "text",
                    "text": f"""At the bottom is a detailed description of code of the code the programmer needs to write.
                    you will review it and help them by giving them insight into the best approaches to accomplish their task.
                    You try to anticipate common bugs, inefficiencies and suggest improvements to the origninal specs to add advanced performance and functionality.
                    by  carefully reviewing programs that submittied you and sending them back a detailed report with suggesions of the best ways to accomplish their task.
                    
                    Youd take the whole scope of the program into consideration when reviewing their task description                    ```python
                    Here is all of the code that has been created for the project so far:
                    {current_code_base}
                    
                    Here is the requeste:
                    {code_description}"""
                    },
                ]
                }
            ]
        ic(messages)

        try:
            completion = client2.chat.completions.create(
            # model="perplexity/sonar-reasoning",
            model="perplexity/sonar",
            messages=messages)
        except Exception as e:
            ic(f"error: {e}")
            return code_description   
        ic(completion)

        # Append messages to a file called ages.log
        # CODE_FILE = Path(get_constant("CODE_FILE"))
        # write_chat_completion_to_file(completion, CODE_FILE)

        research_string = completion.choices[0].message.content
        ic(research_string)
        
        return research_string


    def format_output(self, data: dict) -> str:

        """Format the output data as a readable string"""
        output_lines = []
        
        # Add command type
        output_lines.append(f"Command: {data['command']}")
        
        # Add status
        output_lines.append(f"Status: {data['status']}")
        
        # Add project path
        output_lines.append(f"Project Path: {data['project_path']}")

        # Add filename if present
        if 'filename' in data:
            output_lines.append(f"Filename: {data['filename']}")

        # Add code string if present
        if 'code_string' in data:
            output_lines.append("Code:")
            output_lines.append(data['code_string'])
        
        # Add packages if present
        if 'packages_installed' in data:
            output_lines.append("Packages Installed:")
            for package in data['packages_installed']:
                output_lines.append(f"  - {package}")
        
        # Add run output if present
        if 'run_output' in data and data['run_output']:
            output_lines.append("\nApplication Output:")
            output_lines.append(data['run_output'])
        
        if 'errors' in data and data['errors']:
            output_lines.append("\nErrors:")
            output_lines.append(data['errors'])
        
        # Join all lines with newlines
        return "\n".join(output_lines)


    async def write_code_to_file(self, code_description: str,  project_path: Path, filename) -> dict:
        """write code to a permanent file"""
        file_path = project_path / filename
        code_research_string = await self._call_llm_to_review_code(code_description, file_path)
        ic(code_research_string)
        code_string = await self._call_llm_to_generate_code(code_description, code_research_string, file_path)

        
        # Create the directory if it does not exist
        try:
            os.makedirs(file_path.parent, exist_ok=True)
        except Exception as dir_error:
            return {
                "command": "write_code_to_file",
                "status": "error",
                "project_path": str(project_path),
                "filename": filename,
                "error": f"Failed to create directory: {str(dir_error)}"
            }
        
        # Write the file
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code_string)
        except Exception as write_error:
            return {
                "command": "write_code_to_file",
                "status": "error",
                "project_path": str(project_path),
                "filename": filename,
                "error": f"Failed to write file: {str(write_error)}"
            }
        
        # Log the file creation
        try:
            log_file_operation(file_path, "create")
        except Exception as log_error:
            if self.display is not None:
                try:
                    self.display.add_message("warning", f"Failed to log file operation: {str(log_error)}")
                except Exception:
                    pass
            
        return {
            "command": "write_code_to_file",
            "status": "success",
            "project_path": str(project_path),
            "filename": filename,
            "code_string": code_string
        }

           
    async def write_and_exec(self, code_description: str,  project_path: Path) -> dict:
        """Write code to a temp file and execute it"""
        os.chdir(project_path)    

        code_string = await self._call_llm_to_generate_code(code_description)
        

        
        # Create temp file with .py extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code_string)
            temp_path = temp_file.name
        try:
            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "command": "write_and_exec",
                "status": "success",
                "project_path": str(project_path),
                "run_output": result.stdout,
                "errors": result.stderr
            }
        except subprocess.CalledProcessError as e:
            return {
                "command": "run_app",
                "status": "error",
                "project_path": str(project_path),
                "errors": f"Failed to run app: {str(e)}\nOutput: {e.stdout}\nError: {e.stderr}"
            }
