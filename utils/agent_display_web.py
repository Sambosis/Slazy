import threading
import os
from queue import Queue
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from config import USER_LOG_FILE, ASSISTANT_LOG_FILE, TOOL_LOG_FILE, LOGS_DIR
from utils.agent_display import log_message  # assuming you have your log_message function available
# Compute the project root by going up one directory from utils/
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Now point to the templates folder at the root
template_dir = os.path.join(project_root, "templates")


def log_message(msg_type, message):
    """Log a message to a file"""
    if msg_type == "user":
        emojitag = "🤡 "
    elif msg_type == "assistant":
        emojitag = "🧞‍♀️ "
    elif msg_type == "tool":
        emojitag = "📎 "
    else:
        emojitag = "❓ "
    log_file = os.path.join(LOGS_DIR, f"{msg_type}_messages.log")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(emojitag * 5)
        file.write(f"\n{message}\n\n")
class AgentDisplayWeb:
    """
    A class for managing and displaying messages on a web page.
    This version uses Flask and SocketIO to update connected clients
    in real time.
    """
    def __init__(self):
        template_dir = os.path.join(os.getcwd(), "templates")
        self.app = Flask(__name__, template_folder=template_dir)
        self.user_messages = []
        self.assistant_messages = []
        self.tool_results = []
        self.message_queue = Queue()
        # self.app = Flask(__name__, template_folder="utils/templates")

        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(self.app, async_mode='threading')
        self.setup_routes()
    # def __init__(self):
    #     # Assume that templates folder is at the project root.
    #     template_dir = os.path.join(os.getcwd(), "templates")
    #     self.app = Flask(__name__, template_folder=template_dir)
    #     self.app.config['SECRET_KEY'] = 'secret!'
    #     self.app.debug = True  # Enable debug mode to show errors.
    #     self.socketio = SocketIO(self.app, async_mode='threading')
    #     self.user_messages = []
    #     self.assistant_messages = []
    #     self.tool_results = []
    #     self.message_queue = Queue()
    #     self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template("index.html")

        @self.app.route('/messages')
        def get_messages():
            # This route can be used for an AJAX poll if needed
            return jsonify({
                'user': self.user_messages,
                'assistant': self.assistant_messages,
                'tool': self.tool_results
            })

    def broadcast_update(self):
        # Emit an update event to all connected clients
        self.socketio.emit('update', {
            'user': self.user_messages[-8:][::-1],  # Only send the last eight messages in reverse order
            'assistant': self.assistant_messages[-2:][::-1], # Only send the last two messages in reverse order
            'tool': self.tool_results[-5:][::-1] # Only send the last five messages in reverse order
        })

    def add_message(self, msg_type, content):
        """
        Adds a message to the appropriate list and broadcasts an update.
        """
        log_message(msg_type, content)
        if msg_type == "user":
            self.user_messages.append(content)
        elif msg_type == "assistant":
            self.assistant_messages.append(content)
        elif msg_type == "tool":
            self.tool_results.append(content)
        self.broadcast_update()

    def clear_messages(self, panel):
        """
        Clears messages from a given panel (or all panels if 'all').
        """
        if panel in ("user", "all"):
            self.user_messages.clear()
        if panel in ("assistant", "all"):
            self.assistant_messages.clear()
        if panel in ("tool", "all"):
            self.tool_results.clear()
        self.broadcast_update()


    def start_server(self, host='0.0.0.0', port=5000):
        import threading
        thread = threading.Thread(target=self.socketio.run, args=(self.app,), kwargs={'host': host, 'port': port})
        thread.daemon = True
        thread.start()


    # def start_server(self, host='0.0.0.0', port=5000, debug=False):
    #     # Start the Flask-SocketIO server in a background thread.
    #     thread = threading.Thread(target=self.socketio.run, args=(self.app,), kwargs={'host': host, 'port': port, 'debug': debug})
    #     thread.daemon = True
    #     thread.start()