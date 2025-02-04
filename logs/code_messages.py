C:\mygit\Slazy\repo\storytime\open_story.py
Language detected: python
import os
import webbrowser
import urllib.request

def open_html_file(file_path):
    """
    Open an HTML file in the default web browser
    
    Args:
        file_path (str): Full path to the HTML file
    """
    # Validate file existence
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return False
    
    # Ensure the file has a .html extension
    if not file_path.lower().endswith('.html'):
        print("Warning: File may not be an HTML file")
    
    # Convert file path to URL (use absolute path to ensure cross-platform compatibility)
    try:
        # Use os.path.abspath to resolve any relative path issues
        absolute_path = os.path.abspath(file_path)
        
        # Use urllib to properly escape file paths with special characters
        file_url = 'file:' + urllib.request.pathname2url(absolute_path)
        
        # Open the file in default browser
        webbrowser.open(file_url)
        print(f"Opened {file_path} in default browser")
        return True
    
    except Exception as e:
        print(f"Error opening file: {e}")
        return False

def main():
    # Specific file path
    html_file_path = r'C:\mygit\Slazy\repo\storytime\farmer_story.html'
    
    # Call the function to open the file
    open_html_file(html_file_path)

if __name__ == "__main__":
    main()
