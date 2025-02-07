from enum import Enum
from typing import Literal, List
from pathlib import Path
from .base import ToolResult, BaseAnthropicTool
import os
import subprocess
from icecream import ic
from rich import print as rr
import json
from pydantic import BaseModel
from config import get_constant, set_constant

class ProjectCommand(str, Enum):
    SETUP_PROJECT = "setup_project"
    ADD_DEPENDENCIES = "add_additional_depends"
    RUN_APP = "run_app"

class ProjectSetupTool(BaseAnthropicTool):
    """
    A tool that sets up various project environments and manages script execution.
    """

    name: Literal["project_setup"] = "project_setup"
    api_type: Literal["custom"] = "custom"
    description: str = ("A tool for project management: setup projects, add dependencies, and run applications. "
                        "Supports Python, Node.js, and Ruby environments.")

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
                        "enum": [cmd.value for cmd in ProjectCommand],
                        "description": "Command to execute: setup_project, add_additional_depends, or run_app"
                    },
                    "environment": {
                        "type": "string",
                        "enum": ["python", "node", "ruby"],
                        "description": "Type of project environment to setup"
                    },
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of packages/gems to install"
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Path to the project directory"
                    },
                    "entry_filename": {
                        "type": "string",
                        "description": "Name of the file to run (e.g., app.py, app.js, or app.rb)"
                    }
                },
                "required": ["command", "project_path", "environment"]
            }
        }

    def run_command(self, cmd: str, cwd=None, capture_output=True) -> subprocess.CompletedProcess:
        """Helper method to run shell commands safely"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                cwd=cwd,
                capture_output=capture_output,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            ic(f"Error executing command: {cmd}")
            ic(f"Error details: {e}")
            raise

    def format_output(self, data: dict) -> str:
        """Format the output data as a readable string"""
        output_lines = []
        output_lines.append(f"Command: {data['command']}")
        output_lines.append(f"Status: {data['status']}")
        output_lines.append(f"Project Path: {data['project_path']}")
        if 'packages_installed' in data:
            output_lines.append("Packages Installed:")
            for package in data['packages_installed']:
                output_lines.append(f"  - {package}")
        if 'run_output' in data and data['run_output']:
            output_lines.append("\nApplication Output:")
            output_lines.append(data['run_output'])
        if 'errors' in data and data['errors']:
            output_lines.append("\nErrors:")
            output_lines.append(data['errors'])
        return "\n".join(output_lines)

    # === Python Environment Methods ===
    async def setup_project(self, project_path: Path, packages: List[str]) -> dict:
        project_path.mkdir(parents=True, exist_ok=True)
        os.chdir(project_path)
        ic("Creating Python virtual environment...")
        self.run_command("uv venv")
        try:
            self.run_command("uv init --no-config")
        except:
            pass
        ic("Installing Python packages...")
        for package in packages:
            self.run_command(f"uv add {package}")
        return {
            "command": "setup_project",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def add_dependencies(self, project_path: Path, packages: List[str]) -> dict:
        os.chdir(project_path)
        ic("Installing additional Python packages...")
        for package in packages:
            self.run_command(f"uv add {package}")
        return {
            "command": "add_additional_depends",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def run_app(self, project_path: Path, filename: str) -> dict:
        os.chdir(project_path)
        try:
            result = subprocess.run(
                ["uv", "run", filename],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "command": "run_app",
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

    # === Node.js Environment Methods ===
    async def setup_project_node(self, project_path: Path, packages: List[str]) -> dict:
        project_path.mkdir(parents=True, exist_ok=True)
        os.chdir(project_path)
        ic("Initializing Node.js project...")
        self.run_command("npm init -y")
        ic("Installing Node.js packages...")
        for package in packages:
            self.run_command(f"npm install {package}")
        return {
            "command": "setup_project",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def add_dependencies_node(self, project_path: Path, packages: List[str]) -> dict:
        os.chdir(project_path)
        ic("Installing additional Node.js packages...")
        for package in packages:
            self.run_command(f"npm install {package}")
        return {
            "command": "add_additional_depends",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def run_app_node(self, project_path: Path, filename: str) -> dict:
        os.chdir(project_path)
        try:
            result = subprocess.run(
                ["node", filename],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "command": "run_app",
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

    # === Ruby Environment Methods ===
    async def setup_project_ruby(self, project_path: Path, packages: List[str]) -> dict:
        project_path.mkdir(parents=True, exist_ok=True)
        os.chdir(project_path)
        ic("Setting up Ruby project...")
        # Create a basic Gemfile
        gemfile_content = "source 'https://rubygems.org'\n"
        for package in packages:
            gemfile_content += f"gem '{package}'\n"
        gemfile_path = project_path / "Gemfile"
        with open(gemfile_path, "w") as f:
            f.write(gemfile_content)
        self.run_command("bundle install")
        return {
            "command": "setup_project",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def add_dependencies_ruby(self, project_path: Path, packages: List[str]) -> dict:
        os.chdir(project_path)
        ic("Adding additional Ruby gems...")
        for package in packages:
            self.run_command(f"bundle add {package}")
        return {
            "command": "add_additional_depends",
            "status": "success",
            "project_path": str(project_path),
            "packages_installed": packages
        }

    async def run_app_ruby(self, project_path: Path, filename: str) -> dict:
        os.chdir(project_path)
        try:
            result = subprocess.run(
                ["ruby", filename],
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "command": "run_app",
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

    async def __call__(
        self,
        *,
        command: ProjectCommand,
        project_path: str,
        environment: str = "python",
        packages: List[str] = None,
        entry_filename: str = "app.py",
        **kwargs,
    ) -> ToolResult:
        """
        Executes the specified command for project management depending on the environment.
        """
        if packages is None:
            packages = []

        try:
            if self.display:
                self.display.add_message("user", f"ProjectSetupTool executing command: {command} in {environment} environment")
            
            # Convert project_path string to Path object (using constant if needed)
            project_path = Path(get_constant("PROJECT_DIR")) if get_constant("PROJECT_DIR") else Path(project_path)
            
            # Dispatch based on environment and command
            if environment == "python":
                if command == ProjectCommand.SETUP_PROJECT:
                    result_data = await self.setup_project(project_path, packages)
                elif command == ProjectCommand.ADD_DEPENDENCIES:
                    result_data = await self.add_dependencies(project_path, packages)
                elif command == ProjectCommand.RUN_APP:
                    result_data = await self.run_app(project_path, entry_filename)
                else:
                    return ToolResult(error=f"Unknown command: {command}")
            elif environment == "node":
                if command == ProjectCommand.SETUP_PROJECT:
                    result_data = await self.setup_project_node(project_path, packages)
                elif command == ProjectCommand.ADD_DEPENDENCIES:
                    result_data = await self.add_dependencies_node(project_path, packages)
                elif command == ProjectCommand.RUN_APP:
                    result_data = await self.run_app_node(project_path, entry_filename)
                else:
                    return ToolResult(error=f"Unknown command: {command}")
            elif environment == "ruby":
                if command == ProjectCommand.SETUP_PROJECT:
                    result_data = await self.setup_project_ruby(project_path, packages)
                elif command == ProjectCommand.ADD_DEPENDENCIES:
                    result_data = await self.add_dependencies_ruby(project_path, packages)
                elif command == ProjectCommand.RUN_APP:
                    result_data = await self.run_app_ruby(project_path, entry_filename)
                else:
                    return ToolResult(error=f"Unknown command: {command}")
            else:
                return ToolResult(error=f"Unsupported environment: {environment}")

            formatted_output = self.format_output(result_data)
            if self.display:
                self.display.add_message("user", f"ProjectSetupTool completed: {formatted_output}")
            return ToolResult(output=formatted_output)

        except Exception as e:
            if self.display:
                self.display.add_message("user", f"ProjectSetupTool error: {str(e)}")
            error_msg = f"Failed to execute {command}: {str(e)}"
            return ToolResult(error=error_msg)
