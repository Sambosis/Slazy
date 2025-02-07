PROMPT_FOR_CODE="""I need you to break down a python file in a structured way that concisely describes how to interact with the code.  
It should serve as a basic reference for someone who is unfamiliar with the codebase and needs to understand how to use the functions and classes defined in the file.
It should largely be natural language based.
The breakdown should include the following elements(this will vary based on the codebase, it should cover every class and function in the file including the main function and gloabl variables and imports):

Imports: <list of imports and their purpose>
Global Variables: <list of global variables and their purpose>
Classes: <list of classes and their purpose>
Functions: <list of functions and their purpose>

Class: <class_name>
Purpose: <description of what the class does>
Methods: <list of methods and their purpose>
Attributes: <list of attributes and their purpose>
Summary: <a concise summary of the class's purpose and behavior>
Usage: <How to use, When to use, and and Why you should use this function and any other important information>


Function: <function_name>
Purpose:  <description of what the function does>
Parameters: <list of parameters and their types> 
Returns: <the type of the value returned by the function>
Summary: <a concise summary of the function's purpose and behavior>
Usage: <How to use, When to use, and and Why you should use this function and any other important information>


It should be concise and easy to understand. 
It should abstract away the implementation details and focus on the high-level functionality of the code.
It should give someone everything they need to know to use the function without needing to read the implementation details.
Ensure your response is neatly organized in markdown format.
"""