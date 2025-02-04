C:\mygit\Slazy\repo\iq\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IQ Test</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <main>
        <section id="welcome-screen" aria-label="Welcome Screen">
            <h1>Welcome to the IQ Test</h1>
            <button id="start-button">Start Test</button>
        </section>

        <section id="question-screen" aria-label="Question Screen" hidden>
            <div id="progress" aria-readonly="true">
                Question <span id="current-question">1</span> of <span id="total-questions">10</span>
            </div>
            <form id="question-form" aria-labelledby="question-heading">
                <h2 id="question-heading">Question text here</h2>
                <ul id="answer-options">
                    <li>
                        <label>
                            <input type="radio" name="answer" value="A">
                            Option A
                        </label>
                    </li>
                    <li>
                        <label>
                            <input type="radio" name="answer" value="B">
                            Option B
                        </label>
                    </li>
                    <li>
                        <label>
                            <input type="radio" name="answer" value="C">
                            Option C
                        </label>
                    </li>
                    <li>
                        <label>
                            <input type="radio" name="answer" value="D">
                            Option D
                        </label>
                    </li>
                </ul>
                <div class="navigation-buttons">
                    <button type="button" id="prev-button">Previous</button>
                    <button type="button" id="next-button">Next</button>
                </div>
            </form>
        </section>

        <section id="results-screen" aria-label="Results Screen" hidden>
            <h2>Your Score</h2>
            <p>You scored <span id="score">0</span> out of <span id="total-score">10</span></p>
            <button id="restart-button">Restart Test</button>
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>
C:\mygit\Slazy\repo\iq\styles.css
Language detected: css
/* styles.css */

body {
    font-family: 'Arial Rounded MT Bold', Arial, sans-serif;
    color: #333;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f0f8ff;
}

main {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

section {
    margin-bottom: 40px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.5s ease-in-out;
}

h1, h2 {
    color: #007BFF;
    text-align: center;
    margin-bottom: 20px;
}

button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    margin: 10px;
}

button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
}

button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

#welcome-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 70vh;
}

#question-screen {
    display: flex;
    flex-direction: column;
}

#progress {
    font-size: 18px;
    margin-bottom: 20px;
    text-align: center;
}

form {
    display: flex;
    flex-direction: column;
    align-items: stretch;
}

#question-heading {
    font-size: 24px;
    margin-bottom: 20px;
    text-align: center;
}

#answer-options {
    list-style: none;
    padding: 0;
    margin-bottom: 20px;
}

#answer-options li {
    margin-bottom: 15px;
}

#answer-options label {
    display: flex;
    align-items: center;
    background-color: #e6f7ff;
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

#answer-options input[type="radio"] {
    margin-right: 10px;
    transform: scale(1.2);
}

#answer-options label:hover {
    background-color: #d0ebff;
}

.navigation-buttons {
    display: flex;
    justify-content: space-between;
}

#results-screen {
    text-align: center;
}

#score {
    font-size: 48px;
    color: #28a745;
}

@media (max-width: 600px) {
    main {
        padding: 10px;
    }

    h1, h2 {
        font-size: 1.5em;
    }

    button {
        width: 100%;
        padding: 15px;
    }

    .navigation-buttons {
        flex-direction: column;
    }

    .navigation-buttons button {
        margin: 5px 0;
    }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
C:\mygit\Slazy\repo\iq\script.js
Language detected: javascript
// script.js

// IQ Test Questions Data
const questions = [
  // Question 1
  {
    question: "Which word is the smallest?",
    options: ["Cat", "Mouse", "Elephant", "Ant"],
    answer: "Ant",
    selectedAnswer: null
  },
  // Question 2
  {
    question: "Which number comes next in the sequence? 1, 4, 7, 10, ...",
    options: ["12", "13", "14", "15"],
    answer: "13",
    selectedAnswer: null
  },
  // Question 3
  {
    question: "What is the opposite of 'North'?",
    options: ["West", "East", "South", "Up"],
    answer: "South",
    selectedAnswer: null
  },
  // Question 4
  {
    question: "If 3 + 5 = 12 and 4 + 4 = 16, what is 6 + 2?",
    options: ["8", "12", "16", "24"],
    answer: "24",
    selectedAnswer: null
  },
  // Question 5
  {
    question: "How many sides does an octagon have?",
    options: ["5", "6", "7", "8"],
    answer: "8",
    selectedAnswer: null
  },
  // Question 6
  {
    question: "If you add the first and last letter of the alphabet, what do you get?",
    options: ["A", "Z", "AA", "AZ"],
    answer: "AZ",
    selectedAnswer: null
  },
  // Question 7
  {
    question: "Which letter comes next in the pattern? A, E, I, O, ...",
    options: ["U", "L", "Q", "Y"],
    answer: "U",
    selectedAnswer: null
  },
  // Question 8
  {
    question: "What is 5 cubed?",
    options: ["15", "50", "125", "250"],
    answer: "125",
    selectedAnswer: null
  },
  // Question 9
  {
    question: "Which of these words does not belong? Plane, Helicopter, Drone, Bird",
    options: ["Plane", "Helicopter", "Drone", "Bird"],
    answer: "Bird",
    selectedAnswer: null
  },
  // Question 10
  {
    question: "If a car is 60 miles away and traveling at 60 miles per hour, how many hours will it take to reach you?",
    options: ["1", "2", "3", "4"],
    answer: "1",
    selectedAnswer: null
  }
];

// DOM Elements
const welcomeScreen = document.getElementById("welcome-screen");
const questionScreen = document.getElementById("question-screen");
const resultsScreen = document.getElementById("results-screen");
const questionHeading = document.getElementById("question-heading");
const answerOptions = document.getElementById("answer-options");
const prevButton = document.getElementById("prev-button");
const nextButton = document.getElementById("next-button");
const scoreDisplay = document.getElementById("score");
const totalScoreDisplay = document.getElementById("total-score");
const startButton = document.getElementById("start-button");
const restartButton = document.getElementById("restart-button");
const currentQuestionDisplay = document.getElementById("current-question");
const totalQuestionsDisplay = document.getElementById("total-questions");

// State Management
let currentQuestionIndex = 0;
let score = 0;

// Initialize total questions display
totalQuestionsDisplay.textContent = questions.length;

// Event Listener: Start Test Button
startButton.addEventListener("click", () => {
  welcomeScreen.hidden = true;
  questionScreen.hidden = false;
  showQuestion(currentQuestionIndex);
  updateProgress();
});

// Event Listener: Previous Button
prevButton.addEventListener("click", () => {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    showQuestion(currentQuestionIndex);
    updateProgress();
  }
});

// Event Listener: Next Button
nextButton.addEventListener("click", () => {
  // Check if an answer is selected
  const selectedOption = document.querySelector('input[name="answer"]:checked');
  if (!selectedOption) {
    alert("Please select an answer before proceeding.");
    return;
  }

  // Save the selected answer
  questions[currentQuestionIndex].selectedAnswer = selectedOption.value;

  // If last question, submit the test
  if (currentQuestionIndex === questions.length - 1) {
    calculateScore();
    showResults();
  } else {
    // Move to next question
    currentQuestionIndex++;
    showQuestion(currentQuestionIndex);
    updateProgress();
  }
});

// Event Listener: Restart Test Button
restartButton.addEventListener("click", () => {
  resetTest();
});

// Function to Show a Specific Question
function showQuestion(index) {
  const question = questions[index];
  questionHeading.textContent = question.question;
  clearAnswerOptions();

  question.options.forEach((option) => {
    const li = document.createElement("li");
    const label = document.createElement("label");
    const radioInput = document.createElement("input");

    radioInput.type = "radio";
    radioInput.name = "answer";
    radioInput.value = option;
    radioInput.checked = question.selectedAnswer === option;

    label.appendChild(radioInput);
    label.appendChild(document.createTextNode(option));
    li.appendChild(label);
    answerOptions.appendChild(li);
  });

  updateNavigationButtons();
}

// Function to Clear Answer Options
function clearAnswerOptions() {
  answerOptions.innerHTML = "";
}

// Function to Update Navigation Buttons
function updateNavigationButtons() {
  prevButton.disabled = currentQuestionIndex === 0;
  nextButton.textContent = currentQuestionIndex === questions.length - 1 ? "Submit" : "Next";
}

// Function to Update Progress Display
function updateProgress() {
  currentQuestionDisplay.textContent = currentQuestionIndex + 1;
}

// Function to Calculate the Score
function calculateScore() {
  score = 0;
  questions.forEach((question) => {
    if (question.selectedAnswer === question.answer) {
      score++;
    }
  });
}

// Function to Show Results Screen
function showResults() {
  questionScreen.hidden = true;
  resultsScreen.hidden = false;
  scoreDisplay.textContent = score;
  totalScoreDisplay.textContent = questions.length;
}

// Function to Reset the Test
function resetTest() {
  currentQuestionIndex = 0;
  score = 0;
  questions.forEach((question) => {
    question.selectedAnswer = null;
  });
  resultsScreen.hidden = true;
  welcomeScreen.hidden = false;
}
