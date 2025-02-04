C:\mygit\Slazy\repo\iq\src\components\IQTest.js
Language detected: javascript
C:\mygit\Slazy\repo\iq\src\App.js
Language detected: javascript
C:\mygit\Slazy\repo\iq\src\index.js
Language detected: javascript
// filepath: C:\mygit\Slazy\repo\iq\src\index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { ThemeProvider } from 'styled-components';

// Base styles (create src/index.css if needed)
import './index.css';

// Theme configuration for styled-components
const theme = {
  colors: {
    primary: '#4CAF50',
    secondary: '#2c3e50',
    background: '#f5f7f8'
  },
  fonts: {
    main: "'Poppins', sans-serif",
    secondary: "'Arial', sans-serif"
  }
};

// Get root element and create root
const container = document.getElementById('root');
const root = createRoot(container);

// Render application with theme provider and strict mode
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
C:\mygit\Slazy\repo\iq\src\index.css
Language detected: css
/* filepath: C:\mygit\Slazy\repo\iq\src\index.css */

/* 1. Reset CSS Rules */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: inherit;
}

/* 2. Global Font Settings */
html {
  font-size: 62.5%; /* 1rem = 10px */
}

body {
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
    Oxygen-Sans, Ubuntu, Cantarell, sans-serif;
  font-weight: 400;
  line-height: 1.6;
  color: #333;
}

/* 3. Box-sizing Rules */
html {
  box-sizing: border-box;
}

/* 4. Color Scheme Variables */
:root {
  --color-primary: #4CAF50;
  --color-secondary: #2c3e50;
  --color-background: #f5f7f8;
  --color-text: #34495e;
  --color-text-light: #666;
  --color-success: #4CAF50;
  --color-error: #e74c3c;
  --shadow-light: 0 2px 4px rgba(0, 0, 0, 0.1);
  --shadow-medium: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 5. Default Margins/Padding Reset */
h1, h2, h3, h4, h5, h6 {
  margin: 0;
  padding: 0;
}

ul, ol {
  list-style: none;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  border: none;
  background: none;
  cursor: pointer;
}

/* 6. Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Accessibility Enhancements */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Base Typography */
h1 { font-size: 3.2rem; line-height: 1.2; }
h2 { font-size: 2.8rem; }
h3 { font-size: 2.4rem; }
p { font-size: 1.6rem; margin-bottom: 1.5rem; }

/* Utility Classes */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Base Interactive Elements */
button:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

input, textarea, select {
  font: inherit;
  color: inherit;
}

/* Image Base */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Scroll Behavior */
@media (prefers-reduced-motion: no-preference) {
  html {
    scroll-behavior: smooth;
  }
}

/* Form Element Reset */
textarea {
  resize: vertical;
  min-height: 8rem;
}
C:\mygit\Slazy\repo\iq\package.json
Language detected: json
{
  "name": "cognitive-assessment",
  "version": "1.0.0",
  "description": "A comprehensive React application for assessing cognitive abilities",
  "main": "index.js",
  "private": true,
  "author": "Slazy Team",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "prettier:format": "prettier --write \"src/**/*.{js,jsx,css}\"",
    "lint": "eslint src --ext .js,.jsx",
    "security:audit": "npm audit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "styled-components": "^6.0.0",
    "web-vitals": "^2.1.4"
  },
  "devDependencies": {
    "react-scripts": "^5.0.1",
    "eslint": "^8.55.0",
    "eslint-config-react-app": "^7.0.1",
    "prettier": "^2.7.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/user-event": "^14.4.3",
    "browserslist": "^4.23.0"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
C:\mygit\Slazy\repo\iq\public\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0" />
  <meta name="theme-color" content="#4CAF50" />
  <meta name="description" content="Comprehensive cognitive assessment evaluating verbal, logical, and spatial reasoning abilities through standardized questions" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <title>Cognitive Ability Assessment - Slazy Research</title>
</head>
<body>
  <div id="root" 
       role="main" 
       aria-live="polite" 
       aria-label="Cognitive assessment interface" 
       aria-busy="false"
  ></div>
  <noscript>
    <h1 style="color: #2c3e50; text-align: center; padding: 2rem">
      JavaScript is required to run this cognitive assessment.<br />
      Please enable JavaScript to continue.
    </h1>
  </noscript>
</body>
</html>
C:\mygit\Slazy\repo\iq\app.py
Language detected: python
from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import os
import urllib.parse
from datetime import datetime
import time

class ReactSPARequestHandler(BaseHTTPRequestHandler):
    # Security headers configuration
    security_headers = {
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

    def apply_headers(self, content_type='text/html', cache_control='no-cache'):
        """Set common security and caching headers"""
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', cache_control)
        for key, value in self.security_headers.items():
            self.send_header(key, value)
        self.send_header('Date', self.date_time_string(time.time()))
        self.end_headers()

    def do_GET(self):
        """Handle GET requests with SPA routing and static file serving"""
        parsed_path = urllib.parse.urlparse(self.path).path
        cleaned_path = parsed_path.lstrip('/') or 'index.html'
        
        # Security: Path traversal protection
        if '//' in cleaned_path or '..' in cleaned_path or '~' in cleaned_path:
            self.send_error(403, "Forbidden path pattern detected")
            return

        # Handle static files
        if os.path.isfile(cleaned_path):
            self.serve_static_file(cleaned_path)
        elif os.path.isdir(cleaned_path):
            self.handle_directory(cleaned_path)
        else:
            self.serve_spa_fallback()

    def serve_static_file(self, file_path):
        """Serve static files with proper caching and MIME types"""
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            
            mime_type, _ = mimetypes.guess_type(file_path)
            cache_control = 'public, max-age=31536000' if mime_type and mime_type.startswith('image/') else 'no-cache'
            
            self.send_response(200)
            self.apply_headers(mime_type or 'text/plain', cache_control)
            self.wfile.write(content)
        except PermissionError:
            self.send_error(403, "Access forbidden")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def serve_spa_fallback(self):
        """Serve index.html for SPA client-side routing"""
        if os.path.isfile('index.html'):
            try:
                with open('index.html', 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.apply_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"SPA fallback error: {str(e)}")
        else:
            self.send_error(404, "File not found - SPA entry point missing")

    def handle_directory(self, path):
        """Handle directory requests with redirect"""
        if not path.endswith('/'):
            self.send_response(301)
            self.send_header('Location', f'/{path}/')
            self.end_headers()
            return
        index_path = os.path.join(path, 'index.html')
        if os.path.isfile(index_path):
            self.serve_static_file(index_path)
        else:
            self.send_error(403, "Directory listing forbidden")

def run_server(port=8000):
    """Start the HTTP server with configuration"""
    port = int(os.environ.get('PORT', port))
    server_address = ('', port)
    httpd = HTTPServer(server_address, ReactSPARequestHandler)
    
    print(f"""
    Running development server at http://localhost:{port}/
    Quit with CTRL-C
    SPA Mode: {'Enabled' if os.path.exists('index.html') else 'Disabled'}
    Static files directory: {os.path.abspath(os.getcwd())}
    Security headers: {list(ReactSPARequestHandler.security_headers.keys())}
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == '__main__':
    mimetypes.init()
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('image/svg+xml', '.svg')
    run_server()
C:\mygit\Slazy\repo\iq\index.html
Language detected: html
C:\mygit\Slazy\repo\iq\app.js
Language detected: python
# Updated IQTest component with key improvements
