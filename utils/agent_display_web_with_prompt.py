import os
import threading
from flask import render_template, request, redirect, url_for
from utils.agent_display_web import AgentDisplayWeb
from config import PROMPTS_DIR, set_constant, set_project_dir

import asyncio
class AgentDisplayWebWithPrompt(AgentDisplayWeb):
    def __init__(self):
        super().__init__()
        self.setup_prompt_routes()

    def setup_prompt_routes(self):
        @self.app.route('/select_prompt', methods=['GET', 'POST'])
        def select_prompt():
            if request.method == 'POST':
                # Process the form submission.
                choice = request.form.get('choice')
                if choice == 'new':
                    filename = request.form.get('filename')
                    prompt_text = request.form.get('prompt_text')
                    new_prompt_path = PROMPTS_DIR / f"{filename}.md"
                    with open(new_prompt_path, 'w', encoding='utf-8') as f:
                        f.write(prompt_text)
                    task = prompt_text
                else:
                    prompt_path = PROMPTS_DIR / choice
                    filename = prompt_path.stem
                    with open(prompt_path, 'r', encoding='utf-8') as f:
                        task = f.read()
                # Set up project directory information.
                # Replace 'your_project_module' with the actual module name where these functions are defined.
                project_dir = set_project_dir(filename)
                set_constant("PROJECT_DIR", str(project_dir))
                task += f"Your project directory is {project_dir}. You need to make sure that all files you create and work you do is done in that directory.\n"
                # Start the sampling loop in a background thread.
                def run_loop():
                    from main import run_sampling_loop
                    asyncio.run(run_sampling_loop(task, self))
                threading.Thread(target=run_loop, daemon=True).start()
                return redirect(url_for('index'))
            else:
                # On GET, list available prompt files.
                prompt_files = list(PROMPTS_DIR.glob("*.md"))
                options = [file.name for file in prompt_files]
                return render_template('select_prompt.html', options=options)

        # (The /messages route is already defined in the base class.)
