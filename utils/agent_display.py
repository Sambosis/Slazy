from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich import box
from queue import Queue
import asyncio
from config import USER_LOG_FILE, ASSISTANT_LOG_FILE, TOOL_LOG_FILE, LOGS_DIR
import time
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
    log_file = LOGS_DIR/f"{msg_type}_messages.log"
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(emojitag * 5)
        file.write(f"\n{message}\n\n")

class AgentDisplay:
    """A class for managing and displaying messages in a live terminal interface.
    This class creates a three-panel display layout showing user messages, assistant messages,
    and tool results. It manages message queues and updates the display asynchronously.
    Attributes:
        user_messages (list): List storing user messages.
        assistant_messages (list): List storing assistant responses.
        tool_results (list): List storing tool execution results.
        message_queue (Queue): Queue for managing incoming messages.
        layout (Layout): Rich layout object for terminal display.
    Methods:
        create_layout(): Creates the main three-panel layout.
        create_message_panel(messages, title, style): Creates a panel for displaying messages.
        create_tool_panel(results, title, style): Creates a panel for displaying tool results.
        update_display(live): Asynchronously updates the display with new messages.
        add_message(msg_type, content): Adds a message to the queue for display.
    Example:
        display = AgentDisplay()
        display.add_message("user", "Hello")
        display.add_message("assistant", "Hi there!")
        display.add_message("user", ("calculator", "2 + 2 = 4"))
    """
    def __init__(self):
        self.user_messages = []
        self.assistant_messages = []
        self.tool_results = []
        self.message_queue = Queue()
        self.layout = None
        self.live = None  # Add live attribute

    def create_layout(self):
        """Create the main layout with three panels"""
        layout = Layout()

        layout.split_column(
            Layout(name="upper", ratio=4),
            Layout(name="user", ratio=2)
        )

        layout["upper"].split_row(
            Layout(name="assistant",ratio=3),
            Layout(name="tool",ratio=2)
        )

        user_panel = self.create_message_panel(
            self.user_messages,
            "UserTool Messages",
            "bright_green"
        )

        assistant_panel = self.create_message_panel(
            self.assistant_messages,
            "Assistant Messages",
            "bright_blue"
        )

        tool_panel = self.create_tool_panel(
            self.tool_results,
            "Tool Results",
            "bright_magenta"
        )

        layout["user"].update(user_panel)
        layout["assistant"].update(assistant_panel)
        layout["tool"].update(tool_panel)

        return layout

    def create_message_panel(self, messages, title, style):
        """Create a panel for messages"""
        message_text = Text()
        for msg in messages[-4:]:  # Show last 10 messages
            message_text.append(f"{msg}\n", style=style)

        return Panel(
            message_text,
            title=title,
            border_style=style,
            box=box.ROUNDED
        )

    def create_tool_panel(self, results, title, style):
        """Create a panel for tool results"""
        message_text = Text()
        for result in results[-4:]:  # Show last 5 results
            message_text.append(f"{result}\n", style=style)
                
        return Panel(
            message_text,
            title=title,
            border_style=style,
            box=box.ROUNDED
        )

    async def update_display(self, live, stop_event=None):
        """Update the display with new messages"""
        self.live = live  # Set the live attribute
        while True:
            if stop_event and stop_event.is_set():
                break
            if not self.message_queue.empty():
                msg_type, content = self.message_queue.get()
                if msg_type == "user":
                    self.user_messages.append(content)
                elif msg_type == "assistant":
                    self.assistant_messages.append(content)
                elif msg_type == "tool":
                    self.tool_results.append(content)
                
                # Force an immediate layout update
                live.update(self.create_layout())
                # Smaller sleep time for more responsive updates
                await asyncio.sleep(0.05)
            else:
                await asyncio.sleep(0.1)


    def add_message(self, msg_type, content):
        """
        Adds a message to the queue with specified type and content.

        Args:
            msg_type: Type identifier for the message.
            content: The actual content/payload of the message.

        Returns:
            None
        """
        try:
            log_message(msg_type, content)
            self.message_queue.put((msg_type, content))
            self.live.update(self.create_layout())

        except Exception as e:
            print(f"Error adding message to queue: {e}")
            return e

    # clears the messages from a specified layout panel
    def clear_messages(self, layout_name):
        """
        Clears the messages from a specified layout panel.
        Args:
            layout_name: The name of the layout panel to clear.
            Returns:
            None
        """
        self.live.update(self.create_layout())
        if layout_name == "user" or "all":
            self.user_messages.clear()
        if layout_name == "assistant" or "all":
            self.assistant_messages.clear()
        if layout_name == "tool" or "all":
            self.tool_results.clear()
        # Force an immediate layout update


            