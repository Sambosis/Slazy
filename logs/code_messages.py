C:\mygit\Slazy\repo\iq\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <main class="test-container" aria-label="IQ Test Container">
        <section class="welcome-screen" id="welcome">
            <h1>Welcome to the IQ Test!</h1>
            <button id="start-btn">Start Test</button>
        </section>

        <section class="test-section" id="test" aria-hidden="true" hidden>
            <div class="progress-indicator" aria-label="Progress Indicator">
                <span id="progress-text">Question 1 of 10</span>
                <div id="progress-bar">
                    <div id="progress-tracker" style="width: 10%;"></div>
                </div>
            </div>

            <div class="question-container">
                <h2 id="question-text">Question will appear here</h2>
                <div id="answers" role="radiogroup" aria-label="Answers">
                    <!-- Dynamically insert radio buttons here -->
                </div>
                <nav class="navigation-buttons">
                    <button id="prev-btn" disabled>Previous</button>
                    <button id="next-btn">Next</button>
                    <button id="submit-btn" hidden>Submit</button>
                </nav>
            </div>

            <div class="score-display" id="score-display" aria-hidden="true" hidden>
                <h2>Your Score: <span id="score-text"></span></h2>
            </div>
        </section>

        <section class="results-section" id="results" aria-hidden="true" hidden>
            <h2>Your Final Score</h2>
            <p id="final-score"></p>
            <button id="retake-btn">Retake Test</button>
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>
C:\mygit\Slazy\repo\iq\styles.css
Language detected: css
/* General Styles */
body {
  font-family: 'Open Sans', sans-serif;
  margin: 0;
  background-color: #f9f9f9;
}

.test-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

/* Welcome Screen Styles */
.welcome-screen {
  background-color: #2c3e50;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: white;
  text-align: center;
}

.welcome-screen h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
}

.welcome-screen #start-btn {
  width: 150px;
  font-size: 1.2em;
  background-color: #f1c40f;
  color: #2c3e50;
  border: none;
  padding: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.welcome-screen #start-btn:hover {
  background-color: #d4ac0d;
}

.welcome-screen #start-btn:focus {
  outline: 2px solid #f39c12;
}

/* Question Container Styles */
#test {
  width: 100%;
  max-width: 800px;
}

#question-text {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #2c3e50;
}

#answers {
  display: flex;
  flex-direction: column;
}

#answers label {
  font-size: 1.2em;
  margin: 10px 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.3s, border-radius 0.3s;
  padding: 10px;
  border-radius: 5px;
}

#answers label:hover {
  background-color: #ecf0f1;
}

input[type="radio"] {
  margin-right: 10px;
  transform: scale(1.2);
  cursor: pointer;
}

input[type="radio"]:focus {
  outline: 2px solid #f1c40f;
}

/* Progress Bar Styles */
.progress-indicator {
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
}

#progress-text {
  font-size: 1em;
  margin-bottom: 5px;
  color: #2c3e50;
}

#progress-bar {
  background: lightgray;
  width: 100%;
  height: 15px;
  border-radius: 10px;
  overflow: hidden;
}

#progress-tracker {
  background-color: #f1c40f;
  height: 100%;
  width: 10%;
  transition: width 0.5s ease-in-out;
}

/* Navigation Buttons Styles */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.navigation-buttons button {
  font-size: 1em;
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.navigation-buttons button:hover {
  background-color: #4f606d;
}

.navigation-buttons button:disabled {
  background-color: #7f8c8d;
  cursor: not-allowed;
}

.navigation-buttons button:focus {
  outline: 2px solid #f1c40f;
}

/* Submit Button Specific */
#submit-btn {
  background-color: #27ae60;
}

#submit-btn:hover {
  background-color: #1e8449;
}

/* Score Display Styles */
.score-display {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

#score-text {
  font-size: 2em;
  color: #27ae60;
}

/* Results Section Styles */
#results {
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

#results h2 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

#final-score {
  font-size: 2em;
  margin-bottom: 30px;
}

#retake-btn {
  width: 150px;
  font-size: 1.2em;
  background-color: #f1c40f;
  color: #2c3e50;
  border: none;
  padding: 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

#retake-btn:hover {
  background-color: #d4ac0d;
}

#retake-btn:focus {
  outline: 2px solid #f39c12;
}

/* Transition Effects */
.question-container {
  opacity: 1;
  transition: opacity 0.5s ease-in-out;
}

.fade-out {
  opacity: 0;
}

.fade-in {
  opacity: 1;
}

/* Accessible Contrast */
.score-display {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
}

#score-text {
  font-size: 2em;
  color: #2c3e50;
}

/* Responsive Design Media Queries */
@media screen and (max-width: 768px) {
  .welcome-screen h1 {
    font-size: 2em;
  }

  .welcome-screen #start-btn,
  #retake-btn {
    width: 120px;
    padding: 12px;
    font-size: 1em;
  }

  #question-text {
    font-size: 1.5em;
  }

  #answers label {
    font-size: 1em;
    padding: 8px;
  }

  .navigation-buttons button {
    padding: 8px 16px;
    font-size: 0.9em;
  }

  #progress-bar {
    height: 10px;
  }

  #progress-tracker {
    height: 10px;
  }
}

@media screen and (max-width: 480px) {
  .welcome-screen {
    padding: 10px;
  }

  .welcome-screen h1 {
    font-size: 1.8em;
  }

  .welcome-screen #start-btn,
  #retake-btn {
    width: 100px;
    padding: 10px;
    font-size: 1em;
  }

  #question-text {
    font-size: 1.3em;
  }

  #answers label {
    font-size: 0.9em;
    padding: 6px;
  }

  .navigation-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .navigation-buttons button {
    width: 100%;
    margin: 5px 0;
  }

  #progress-bar {
    height: 8px;
  }

  #progress-tracker {
    height: 8px;
  }
}
C:\mygit\Slazy\repo\iq\script.js
Language detected: javascript
