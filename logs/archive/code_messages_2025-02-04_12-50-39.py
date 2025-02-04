C:\mygit\Slazy\repo\iq\app.py
Language detected: python
from flask import Flask, render_template

# Create a Flask instance
app = Flask(__name__)

# Define a route for the main page that renders the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Main execution block with debug mode enabled
if __name__ == '__main__':
    app.run(debug=True)
