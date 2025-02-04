C:\mygit\Slazy\repo\iq\index.html
Language detected: html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test Application</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header Section -->
    <header>
        <h1>Welcome to the IQ Test</h1>
    </header>

    <!-- Main Content Section -->
    <main>
        <!-- Welcome Screen -->
        <section id="welcome-screen" class="screen active" aria-labelledby="welcome-heading">
            <h2 id="welcome-heading">Welcome!</h2>
            <p>Click "Start Test" to begin your IQ assessment.</p>
            <button id="start-test" aria-label="Start IQ Test">Start Test</button>
        </section>

        <!-- Question Container -->
        <section id="question-container" class="screen" aria-labelledby="question-heading">
            <h2 id="question-heading">Question 1</h2>
            <p id="question-text">What is the next number in the sequence: 2, 4, 6, 8, ...?</p>
            <div class="options">
                <button class="option" data-value="10">10</button>
                <button class="option" data-value="12">12</button>
                <button class="option" data-value="14">14</button>
                <button class="option" data-value="16">16</button>
            </div>
        </section>

        <!-- Results Section -->
        <section id="results" class="screen" aria-labelledby="results-heading">
            <h2 id="results-heading">Your IQ Score:</h2>
            <p id="iq-score">Calculating...</p>
            <button id="retake-test" aria-label="Retake IQ Test">Retake Test</button>
        </section>
    </main>

    <!-- Footer Section -->
    <footer>
        <p>&copy; 2023 IQ Test Application. All Rights Reserved.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
C:\mygit\Slazy\repo\iq\styles.css
Language detected: css
/* styles.css */

/* General Reset to ensure consistent styling across browsers */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Base Styles */
body {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    background-color: #f0f8ff;
    color: #333;
    line-height: 1.6;
    font-size: 16px;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Container */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    flex: 1;
}

/* Header */
header {
    background-color: #4CAF50;
    color: white;
    padding: 20px 0;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

/* Main Content Section */
main {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* Screen Switching */
.screen {
    display: none; /* Initially hide all screens */
    width: 100%;
}

.active {
    display: block; /* Only show the active screen */
    animation: fadeIn 0.5s ease-in-out;
}

/* Welcome Screen */
#welcome-screen h2 {
    font-size: 2em;
    margin-bottom: 15px;
}

#welcome-screen p {
    font-size: 1.2em;
    margin-bottom: 25px;
}

#welcome-screen button {
    background-color: #ff9800;
    color: white;
    padding: 15px 30px;
    font-size: 1.1em;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

#welcome-screen button:hover {
    background-color: #e68900;
    transform: scale(1.05);
}

/* Question Container */
#question-container {
    margin-top: 20px;
    padding: 25px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    width: 90%;
    max-width: 600px;
}

#question-container h2 {
    font-size: 2em;
    margin-bottom: 15px;
}

#question-text {
    font-size: 1.3em;
    margin-bottom: 25px;
}

.options {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.option {
    background-color: #2196F3;
    color: white;
    padding: 12px 20px;
    font-size: 1.1em;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.option:hover {
    background-color: #1976D2;
    transform: translateY(-2px);
}

/* Results Section */
#results {
    margin-top: 20px;
    padding: 25px;
    background-color: #e8f5e9;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    width: 90%;
    max-width: 600px;
}

#results-heading {
    font-size: 2em;
    margin-bottom: 15px;
}

#iq-score {
    font-size: 1.5em;
    margin-bottom: 25px;
    color: #2e7d32;
}

#retake-test {
    background-color: #f44336;
    color: white;
    padding: 12px 25px;
    font-size: 1.1em;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

#retake-test:hover {
    background-color: #d32f2f;
    transform: translateY(-2px);
}

/* Footer */
footer {
    background-color: #333;
    color: white;
    padding: 15px 0;
    text-align: center;
    font-size: 0.9em;
}

/* Transitions */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Responsive Design */
@media (max-width: 768px) {
    body {
        font-size: 14px;
    }

    header h1 {
        font-size: 2em;
    }

    #welcome-screen button,
    #retake-test {
        width: 80%;
        padding: 12px 0;
        font-size: 1em;
    }

    #question-container,
    #results {
        padding: 20px;
    }

    .option {
        font-size: 1em;
        padding: 10px 15px;
    }
}

@media (max-width: 480px) {
    header h1 {
        font-size: 1.8em;
    }

    #welcome-screen h2,
    #question-container h2,
    #results-heading {
        font-size: 1.8em;
    }

    #question-text {
        font-size: 1.1em;
    }

    .option {
        font-size: 0.95em;
    }
}
C:\mygit\Slazy\repo\iq\script.js
Language detected: javascript
