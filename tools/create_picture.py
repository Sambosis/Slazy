from typing import Literal
from pathlib import Path
from .base import ToolResult, BaseAnthropicTool
import replicate
import base64
from icecream import ic
from enum import Enum
from dotenv import load_dotenv
load_dotenv()
import os
import PIL
class PictureCommand(str, Enum):
    CREATE = "create"

class PictureGenerationTool(BaseAnthropicTool):
    """Tool for generating pictures using the Flux Schnell model"""
    
    name: Literal["picture_generation"] = "picture_generation"
    api_type: Literal["custom"] = "custom"
    description: str = "Creates pictures based on text prompts. This is how you will create pictures that you need for projects."

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
                        "enum": [cmd.value for cmd in PictureCommand],
                        "description": "Command to execute: create"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Text description of the image to generate"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the generated image will be saved"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Optional width to resize the image"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Optional height to resize the image"
                    }
                },
                "required": ["command", "prompt"]
            }
        }

    async def generate_picture(self, prompt: str, output_path: str, width: int = None, height: int = None) -> dict:
        """Generates a picture using the Flux Schnell model"""
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            input_data = {
                "prompt": prompt
            }
            client = replicate.Client()
            output = client.run(
                "black-forest-labs/flux-schnell",
                input=input_data
            )

            output_files = []
            for index, item in enumerate(output):
                # Read image bytes
                image_data = item.read()
                # Convert the image data to a base64 encoded string
                base64_data = base64.b64encode(image_data).decode("utf-8")
                # Optionally, if you want to save the image as well:
                output_file = f"{output_path}"
                with open(output_file, "wb") as file:
                    file.write(image_data)

                # Resize if dimensions are provided
                if width or height:
                    img = PIL.Image.open(output_file)
                    if width and height:
                        new_size = (width, height)
                    elif width:
                        ratio = width / img.width
                        new_size = (width, int(img.height * ratio))
                    else:
                        ratio = height / img.height
                        new_size = (int(img.width * ratio), height)
                    
                    resized_img = img.resize(new_size, PIL.Image.LANCZOS)
                    resized_img.save(output_file)
                html_message = (
                        "<div>"
                        "<p>Here is your generated image:</p>"
                        f'<img src="data:image/png;base64,{base64_data}" alt="Generated Image" style="max-width:100%;">'
                        "</div>"
                    )
                self.display.add_message("user", html_message)
                self.display.add_message("tool", html_message)
                self.display.add_message("assistant", html_message)
                output_files.append(output_file)

            return {
                "status": "success",
                "output_files": output_files,
                "prompt": prompt
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def format_output(self, data: dict) -> str:
        """Format the output data as a readable string"""
        output_lines = []
        output_lines.append(f"Status: {data['status']}")
        
        if data['status'] == 'success':
            output_lines.append(f"Prompt: {data['prompt']}")
            output_lines.append("Generated files:")
            for file in data['output_files']:
                output_lines.append(f"  - {file}")
        else:
            output_lines.append(f"Error: {data['error']}")
            
        return "\n".join(output_lines)

    async def __call__(
        self,
        *,
        command: PictureCommand,
        prompt: str,
        output_path: str = "output",
        width: int = None,
        height: int = None,
        **kwargs,
    ) -> ToolResult:
        """Executes the picture generation command"""
        try:
            if self.display:
                self.display.add_message("user", f"PictureGenerationTool executing command: {command}")
            
            # output_path = Path(output_path)
            # output_path.mkdir(parents=True, exist_ok=True)

            if command == PictureCommand.CREATE:
                result_data = await self.generate_picture(prompt, output_path, width, height)
            else:
                return ToolResult(error=f"Unknown command: {command}")

            formatted_output = self.format_output(result_data)

            if self.display:
                self.display.add_message("user", f"PictureGenerationTool completed: {formatted_output}")
            
            return ToolResult(output=formatted_output)

        except Exception as e:
            if self.display:
                self.display.add_message("user", f"PictureGenerationTool error: {str(e)}")
            return ToolResult(error=f"Failed to execute {command}: {str(e)}")
