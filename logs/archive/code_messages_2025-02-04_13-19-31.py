C:\mygit\Slazy\repo\iq\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test Application</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Welcome/Instruction Screen -->
    <header id="welcome-screen" class="active">
        <h1>Welcome to the IQ Test</h1>
        <p>Please read the instructions carefully before starting the test.</p>
        <button id="start-button">Start Test</button>
    </header>

    <!-- Main Content Area -->
    <main>
        <!-- Question Container -->
        <section id="question-container" class="hidden">
            <div id="progress-indicator">Question 1 of 10</div>
            <div id="question-content">
                <h2 id="question-text">Question will appear here</h2>
                <form id="answer-form">
                    <!-- Answer choices will be dynamically inserted here -->
                </form>
            </div>
            <div class="navigation-buttons">
                <button id="prev-button" disabled>Previous</button>
                <button id="next-button">Next</button>
            </div>
        </section>

        <!-- Results Section -->
        <section id="results-section" class="hidden">
            <h2>Your Results</h2>
            <p id="score">You scored X out of Y.</p>
            <button id="restart-button">Retake Test</button>
        </section>
    </main>

    <footer>
        <p>&copy; 2023 IQ Test Application</p>
    </footer>

    <script src="script.js" defer></script>
</body>
</html>
