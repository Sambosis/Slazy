C:\mygit\Slazy\repo\iq\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test for Young Minds</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <style>
        body {
            background-color: #f0f8ff;
        }
        header {
            background-color: #4CAF50;
            padding: 20px 0;
            color: white;
            margin-bottom: 30px;
        }
        #start-screen, #questions-container, #results-section {
            max-width: 600px;
            margin: auto;
        }
        .question {
            margin-bottom: 20px;
        }
        #progress-bar {
            width: 100%;
            height: 20px;
            margin-bottom: 20px;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <h1 class="text-center">IQ Test for Young Minds</h1>
    </header>

    <!-- Start Screen -->
    <div id="start-screen" class="container text-center">
        <h2>Instructions:</h2>
        <p>Welcome to our IQ test! Please read the instructions carefully and select your answers for each question.</p>
        <button id="start-btn" class="btn btn-primary mt-3">Start Test</button>
    </div>

    <!-- Questions Container -->
    <div id="questions-container" class="container d-none">
        <div id="progress-container" class="mb-3">
            <progress id="progress-bar" value="0" max="100"></progress>
        </div>
        <ol id="questions-list" class="list-group mb-3">
            <!-- Questions will be dynamically inserted here -->
        </ol>
        <button id="submit-btn" class="btn btn-success">Submit Answers</button>
    </div>

    <!-- Results Section -->
    <div id="results-section" class="container d-none text-center">
        <h2>Results</h2>
        <p>Your score is: <span id="score">0%</span></p>
        <button id="retake-btn" class="btn btn-secondary mt-3">Retake Test</button>
    </div>

    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <!-- Custom JavaScript -->
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const startScreen = document.getElementById('start-screen');
            const questionsContainer = document.getElementById('questions-container');
            const resultsSection = document.getElementById('results-section');
            const startBtn = document.getElementById('start-btn');
            const submitBtn = document.getElementById('submit-btn');
            const progressBar = document.getElementById('progress-bar');
            const retakeBtn = document.getElementById('retake-btn');
            const questionsList = document.getElementById('questions-list');
            const scoreDisplay = document.getElementById('score');

            const totalQuestions = 5; // Example number of questions
            let answeredCorrectly = 0;

            const questions = [
                {
                    question: "What number comes next in the sequence: 2, 4, 6, 8, __?",
                    options: ["9", "10", "12", "11"],
                    answer: "10"
                },
                {
                    question: "Which shape has four equal sides and four right angles?",
                    options: ["Rectangle", "Square", "Triangle", "Circle"],
                    answer: "Square"
                },
                {
                    question: "If you have 3 apples and you take away 2, how many do you have?",
                    options: ["1", "2", "3", "0"],
                    answer: "2"
                },
                {
                    question: "What is the color of the sky on a clear day?",
                    options: ["Green", "Blue", "Red", "Yellow"],
                    answer: "Blue"
                },
                {
                    question: "How many legs does a spider have?",
                    options: ["6", "8", "10", "4"],
                    answer: "8"
                }
            ];

            // Initialize progress bar
            progressBar.value = 0;

            // Function to load questions
            function loadQuestions() {
                questions.forEach((q, index) => {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item', 'question');

                    const qText = document.createElement('p');
                    qText.textContent = `${index + 1}. ${q.question}`;
                    li.appendChild(qText);

                    q.options.forEach(option => {
                        const div = document.createElement('div');
                        div.classList.add('form-check');

                        const input = document.createElement('input');
                        input.classList.add('form-check-input');
                        input.type = 'radio';
                        input.name = `question${index}`;
                        input.id = `q${index}_${option}`;
                        input.value = option;

                        const label = document.createElement('label');
                        label.classList.add('form-check-label');
                        label.htmlFor = `q${index}_${option}`;
                        label.textContent = option;

                        div.appendChild(input);
                        div.appendChild(label);
                        li.appendChild(div);
                    });

                    questionsList.appendChild(li);
                });
            }

            // Update progress bar based on answered questions
            function updateProgress() {
                const answered = document.querySelectorAll('input[type="radio"]:checked').length;
                const percentage = (answered / totalQuestions) * 100;
                progressBar.value = percentage;
            }

            // Event listener for starting the test
            startBtn.addEventListener('click', () => {
                startScreen.classList.add('d-none');
                questionsContainer.classList.remove('d-none');
                loadQuestions();
            });

            // Event listener for answering questions
            questionsList.addEventListener('change', updateProgress);

            // Event listener for submitting answers
            submitBtn.addEventListener('click', () => {
                answeredCorrectly = 0;
                questions.forEach((q, index) => {
                    const selected = document.querySelector(`input[name="question${index}"]:checked`);
                    if (selected && selected.value === q.answer) {
                        answeredCorrectly++;
                    }
                });
                displayResults();
            });

            // Function to display results
            function displayResults() {
                questionsContainer.classList.add('d-none');
                resultsSection.classList.remove('d-none');
                progressBar.value = 100;
                const scorePercentage = Math.round((answeredCorrectly / totalQuestions) * 100);
                scoreDisplay.textContent = `${scorePercentage}%`;
            }

            // Event listener for retaking the test
            retakeBtn.addEventListener('click', () => {
                resetTest();
            });

            // Function to reset the test
            function resetTest() {
                resultsSection.classList.add('d-none');
                startScreen.classList.remove('d-none');
                questionsList.innerHTML = '';
                progressBar.value = 0;
                answeredCorrectly = 0;
            }
        });
    </script>
</body>
</html>
C:\mygit\Slazy\repo\iq\script.js
Language detected: javascript
// iqTest.js

document.addEventListener("DOMContentLoaded", function() {
    const startScreen = document.getElementById('start-screen');
    const questionsContainer = document.getElementById('questions-container');
    const resultsSection = document.getElementById('results-section');
    const startBtn = document.getElementById('start-btn');
    const submitBtn = document.getElementById('submit-btn');
    const progressBar = document.getElementById('progress-bar');
    const retakeBtn = document.getElementById('retake-btn');
    const questionsList = document.getElementById('questions-list');
    const scoreDisplay = document.getElementById('score');
    const estimatedIq = document.getElementById('estimated-iq');

    const totalQuestions = 12;
    let answeredCorrectly = 0;

    const questions = [
        {
            question: "What word means 'to move quickly'?",
            options: ["Slow", "Quick", "Jump", "Run"],
            answer: "Run",
            category: "Verbal Reasoning"
        },
        {
            question: "Complete the sequence: A, B, __, D, E, F",
            options: ["A", "B", "C", "D"],
            answer: "C",
            category: "Logical Reasoning"
        },
        {
            question: "Pick the odd one out: Circle, Square, Triangle, Apple",
            options: ["Circle", "Square", "Triangle", "Apple"],
            answer: "Apple",
            category: "Logical Reasoning"
        },
        {
            question: "Which number is not even? 4, 7, 10, 12",
            options: ["4", "7", "10", "12"],
            answer: "7",
            category: "Mathematical Reasoning"
        },
        {
            question: "Arrange the following words to make a sentence: 'dogs play the often'.",
            options: [
                "The dogs often play",
                "Often the dogs play",
                "Dogs often the play",
                "The often dogs play"
            ],
            answer: "The dogs often play",
            category: "Verbal Reasoning"
        },
        {
            question: "How many sides does a pentagon have?",
            options: ["3", "4", "5", "6"],
            answer: "5",
            category: "Mathematical Reasoning"
        },
        {
            question: "Which shape would you see more often if you look at a house?",
            options: ["Cube", "Sphere", "Cylinder", "Pyramid"],
            answer: "Cube",
            category: "Spatial Reasoning"
        },
        {
            question: "How many months have 30 days?",
            options: ["4", "5", "6", "7"],
            answer: "7",
            category: "Logical Reasoning"
        },
        {
            question: "Complete the pattern: 1, 4, 7, 10, __",
            options: ["11", "12", "13", "14"],
            answer: "13",
            category: "Mathematical Reasoning"
        },
        {
            question: "A cube has how many vertices?",
            options: ["4", "6", "8", "12"],
            answer: "8",
            category: "Spatial Reasoning"
        },
        {
            question: "If a bus leaves every 5 minutes and you arrive 10 minutes late, how many buses have left since the first one?",
            options: ["1", "2", "3", "4"],
            answer: "2",
            category: "Logical Reasoning"
        },
        {
            question: "Select the word that describes 'a type of bird':",
            options: ["Frog", "Dog", "Eagle", "Fish"],
            answer: "Eagle",
            category: "Verbal Reasoning"
        }
    ];

    // Initialize progress bar
    progressBar.value = 0;

    // Function to load questions
    function loadQuestions() {
        questions.forEach((q, index) => {
            const li = document.createElement('li');
            li.classList.add('list-group-item', 'question');

            const qText = document.createElement('p');
            qText.textContent = `${index + 1}. ${q.question}`;
            li.appendChild(qText);

            q.options.forEach(option => {
                const div = document.createElement('div');
                div.classList.add('form-check');

                const input = document.createElement('input');
                input.classList.add('form-check-input');
                input.type = 'radio';
                input.name = `question${index}`;
                input.id = `q${index}_${option}`;
                input.value = option;

                const label = document.createElement('label');
                label.classList.add('form-check-label');
                label.htmlFor = `q${index}_${option}`;
                label.textContent = option;

                div.appendChild(input);
                div.appendChild(label);
                li.appendChild(div);
            });

            questionsList.appendChild(li);
        });
    }

    // Update progress bar based on answered questions
    function updateProgress() {
        const answered = document.querySelectorAll('input[type="radio"]:checked').length;
        const percentage = (answered / totalQuestions) * 100;
        progressBar.value = percentage;
    }

    // Event listener for starting the test
    startBtn.addEventListener('click', () => {
        startScreen.classList.add('d-none');
        questionsContainer.classList.remove('d-none');
        loadQuestions();
        updateProgress();  // Trigger initial progress update
    });

    // Event listener for answering questions
    questionsList.addEventListener('change', updateProgress);

    // Event listener for submitting answers
    submitBtn.addEventListener('click', () => {
        answeredCorrectly = 0;
        questions.forEach((q, index) => {
            const selected = document.querySelector(`input[name="question${index}"]:checked`);
            if (selected && selected.value === q.answer) {
                answeredCorrectly++;
            }
        });
        displayResults(answeredCorrectly);
    });

    // Function to display results
    function displayResults(userScore) {
        questionsContainer.classList.add('d-none');
        resultsSection.classList.remove('d-none');
        progressBar.value = 100;
        const percentage = Math.round((userScore / totalQuestions) * 100);
        scoreDisplay.textContent = `${percentage}%`;

        // Estimate IQ score
        estimatedIq.textContent = estimateIqScore(percentage);
    }

    // Function to estimate IQ score based on test performance
    function estimateIqScore(scorePercentage) {
        let iqEstimation;
        if (scorePercentage >= 90) {
            iqEstimation = 130;
        } else if (scorePercentage >= 75) {
            iqEstimation = 120;
        } else if (scorePercentage >= 60) {
            iqEstimation = 100;
        } else if (scorePercentage >= 45) {
            iqEstimation = 80;
        } else {
            iqEstimation = 60;
        }
        return iqEstimation;
    }

    // Event listener for retaking the test
    retakeBtn.addEventListener('click', () => {
        resetTest();
    });

    // Function to reset the test
    function resetTest() {
        resultsSection.classList.add('d-none');
        startScreen.classList.remove('d-none');
        questionsList.innerHTML = '';
        progressBar.value = 0;
        answeredCorrectly = 0;
    }
});
C:\mygit\Slazy\repo\iq\styles.css
Language detected: css
/* styles.css */

/* General Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f8ff; /* Alice Blue */
    color: #333;
    margin: 0;
    padding: 0;
}

/* Header Styles */
header {
    background-color: #4CAF50; /* Green */
    padding: 20px 0;
    color: white;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Container Styles */
.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
}

/* Start Screen Styles */
#start-screen {
    text-align: center;
}

#start-screen h2 {
    font-size: 1.8em;
    margin-top: 10px;
}

#start-screen p {
    font-size: 1.2em;
    margin: 20px 0;
}

/* Questions Container Styles */
#questions-container {
    display: none;
}

.question {
    margin-bottom: 20px;
}

.question p {
    font-weight: bold;
    font-size: 1.1em;
    margin-bottom: 10px;
}

.form-check {
    margin-bottom: 10px;
}

.form-check-input {
    margin-right: 10px;
}

.form-check-label {
    font-size: 1em;
    cursor: pointer;
}

.form-check-label:hover {
    color: #4CAF50;
}

/* Buttons Styles */
.btn {
    padding: 10px 20px;
    border-radius: 25px;
    border: none;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-primary {
    background-color: #4CAF50;
    color: white;
}

.btn-primary:hover {
    background-color: #45a049;
    transform: scale(1.05);
}

.btn-success {
    background-color: #28a745;
    color: white;
}

.btn-success:hover {
    background-color: #218838;
    transform: scale(1.05);
}

.btn-secondary {
    background-color: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background-color: #5a6268;
    transform: scale(1.05);
}

/* Progress Bar Styles */
#progress-container {
    margin-bottom: 20px;
}

progress {
    width: 100%;
    height: 25px;
    appearance: none;
    -webkit-appearance: none;
    border: none;
    border-radius: 5px;
    background-color: #ddd;
    overflow: hidden;
}

progress::-webkit-progress-bar {
    background-color: #ddd;
    border-radius: 5px;
}

progress::-webkit-progress-value {
    background-color: #4CAF50;
    border-radius: 5px;
}

progress::-moz-progress-bar {
    background-color: #4CAF50;
    border-radius: 5px;
}

/* Question List Styles */
.list-group-item {
    padding: 15px 20px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 15px;
    transition: transform 0.2s ease;
}

.list-group-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Results Section Styles */
#results-section {
    display: none;
    text-align: center;
}

#results-section h2 {
    font-size: 2em;
    margin-bottom: 20px;
    color: #4CAF50;
}

#results-section p {
    font-size: 1.5em;
    margin-bottom: 15px;
}

#results-section span {
    font-weight: bold;
    color: #333;
}

#estimated-iq {
    font-size: 1.2em;
    color: #6c757d;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }

    header {
        padding: 15px 0;
    }

    .btn {
        width: 100%;
        margin-bottom: 10px;
    }

    .list-group-item {
        padding: 10px 15px;
    }
}
