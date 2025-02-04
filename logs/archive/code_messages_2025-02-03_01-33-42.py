C:\mygit\BLazy\repo\promptwebview\loop_webview.py
Language detected: python
import webview
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Optional

# HTML template with basic styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; margin: 20px; }
        .tool-output { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        .api-response { background: #e6f3ff; padding: 10px; margin: 10px 0; }
        .conversation { background: #f5f5f5; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div id="output"></div>
    <script>
        function updateOutput(content) {
            var outputDiv = document.getElementById("output");
            outputDiv.innerHTML += content;
            outputDiv.scrollTop = outputDiv.scrollHeight;
        }
    </script>
</body>
</html>
'''

class OutputWindow:
    # Window class to handle displaying output
    def __init__(self):
        self.window = None
        self.output_buffer = []
    
    def initialize(self):
        self.window = webview.create_window('Loop Output', html=HTML_TEMPLATE)
        webview.start(http_server=False)
        
    def update_output(self, content, type='text'):
        # Format and display new content
        if type == 'tool-output':
            formatted_content = f'<div class="tool-output">{content}</div>'
        elif type == 'api-response':
            formatted_content = f'<div class="api-response">{content}</div>'
        elif type == 'conversation':
            formatted_content = f'<div class="conversation">{content}</div>'
        else:
            formatted_content = f'<div>{content}</div>'
        
        if self.window:
            self.window.evaluate_js(f'updateOutput("{formatted_content}")')
        else:
            self.output_buffer.append(formatted_content)

# Modified OutputManager class that sends output to webview
class OutputManager:
    def __init__(self, window: OutputWindow, image_dir: Optional[Path] = None):
        self.window = window
        self.image_dir = image_dir
    
    def print_tool_output(self, output):
        self.window.update_output(output, 'tool-output')
    
    def print_api_response(self, response):
        self.window.update_output(json.dumps(response, indent=4), 'api-response')
    
    def print_conversation(self, conversation):
        self.window.update_output(conversation, 'conversation')

def main():
    output_window = OutputWindow()
    output_window.initialize()
    
    output_manager = OutputManager(output_window)
    
    # Example usage:
    output_manager.print_tool_output("This is a tool output.")
    output_manager.print_api_response({"key": "value"})
    output_manager.print_conversation("This is a conversation.")

if __name__ == "__main__":
    main()
