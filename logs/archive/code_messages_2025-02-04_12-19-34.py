C:\mygit\Slazy\repo\iq\src\App.js
Language detected: javascript
C:\mygit\Slazy\repo\iq\src\questions.js
Language detected: javascript
C:\mygit\Slazy\repo\iq\src\App.js
Language detected: javascript
// File: src/QuizContext.js
import React, { createContext, useReducer } from 'react';
import { QUESTIONS } from './questions';

// Initial State
const initialState = {
  currentQuestionIdx: 0,
  userAnswers: [],
  score: 0,
  categoryProgress: {},
  totalPoints: 0,
  earnedPoints: 0,
  isQuizCompleted: false,
};

// Reducer Function
const quizReducer = (state, action) => {
  switch (action.type) {
    case 'ANSWER_QUESTION':
      const { answer } = action.payload;
      const currentQuestion = QUESTIONS[state.currentQuestionIdx];
      const isCorrect = answer === currentQuestion.correctAnswer;
      const updatedScore = isCorrect ? state.score + currentQuestion.points : state.score;
      const updatedEarnedPoints = isCorrect
        ? state.earnedPoints + currentQuestion.points
        : state.earnedPoints;
      const updatedUserAnswers = [...state.userAnswers, answer];

      // Update category progress
      const category = currentQuestion.type;
      const categoryData = state.categoryProgress[category] || { attempted: 0, correct: 0, points: 0 };
      const updatedCategoryData = {
        attempted: categoryData.attempted + 1,
        correct: categoryData.correct + (isCorrect ? 1 : 0),
        points: categoryData.points + (isCorrect ? currentQuestion.points : 0),
      };

      return {
        ...state,
        currentQuestionIdx: state.currentQuestionIdx + 1,
        userAnswers: updatedUserAnswers,
        score: updatedScore,
        earnedPoints: updatedEarnedPoints,
        categoryProgress: {
          ...state.categoryProgress,
          [category]: updatedCategoryData,
        },
        totalPoints: state.totalPoints + currentQuestion.points,
      };
    case 'SUBMIT_QUIZ':
      return {
        ...state,
        isQuizCompleted: true,
      };
    case 'RESET_QUIZ':
      return initialState;
    default:
      return state;
  }
};

// Create Context
export const QuizContext = createContext();

// Provider Component
export const QuizProvider = ({ children }) => {
  const [state, dispatch] = useReducer(quizReducer, initialState);

  return (
    <QuizContext.Provider value={{ state, dispatch }}>
      {children}
    </QuizContext.Provider>
  );
};
C:\mygit\Slazy\repo\iq\src\App.js
Language detected: javascript
// File: src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, AppBar, Toolbar, Typography, Box, Container, LinearProgress } from '@mui/material';
import { styled } from '@mui/system';
import { QuizProvider, QuizContext } from './QuizContext';
import WelcomeScreen from './WelcomeScreen';
import QuestionScreen from './QuestionScreen';
import ResultsScreen from './ResultsScreen';
import ProgressBar from './components/ProgressBar';
import ScoreDisplay from './components/ScoreDisplay';

// Styled Components
const StyledAppBar = styled(AppBar)({
  backgroundColor: '#1976d2',
});

const ContentContainer = styled(Container)({
  marginTop: '2rem',
  marginBottom: '2rem',
});

function App() {
  return (
    <QuizProvider>
      <Router>
        <CssBaseline />
        <StyledAppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              IQ Test
            </Typography>
            <ScoreDisplay />
          </Toolbar>
        </StyledAppBar>
        <ContentContainer>
          <ProgressBar />
          <Box sx={{ mt: 4 }}>
            <Routes>
              <Route path="/" element={<WelcomeScreen />} />
              <Route path="/questions/:questionIdx" element={<QuestionScreen />} />
              <Route path="/results" element={<ResultsScreen />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Box>
        </ContentContainer>
      </Router>
    </QuizProvider>
  );
}

export default App;
C:\mygit\Slazy\repo\iq\src\components\WelcomeScreen.js
Language detected: javascript
// File: src/WelcomeScreen.jsx

import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Fade,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import { CheckCircle } from '@mui/icons-material';
import { styled } from '@mui/system';
import { QUESTIONS } from './questions';

// Styled Components
const WelcomeContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: theme.spacing(4),
  minHeight: '80vh',
  background: 'linear-gradient(135deg, #ece9e6, #ffffff)',
}));

const Title = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  fontWeight: 'bold',
  color: theme.palette.primary.main,
}));

const Description = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(4),
  textAlign: 'center',
  maxWidth: 600,
}));

const StartButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(4),
  padding: theme.spacing(1.5, 4),
}));

const InfoCard = styled(Card)(({ theme }) => ({
  minWidth: 275,
  margin: theme.spacing(2),
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
}));

const InfoTitle = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(1),
  fontWeight: '600',
}));

const InfoList = styled(List)(({ theme }) => ({
  paddingLeft: theme.spacing(2),
}));

const WelcomeScreen = () => {
  const navigate = useNavigate();

  // Calculate test details
  const testDuration = 30; // in minutes
  const numberOfQuestions = QUESTIONS.length;
  const categories = Array.from(new Set(QUESTIONS.map((q) => q.type)));
  const scoringSystem = `
    - Easy questions: 3 points
    - Medium questions: 5 points
    - Hard questions: 7 points
  `;

  const handleStart = () => {
    navigate('/questions/0');
  };

  return (
    <Fade in timeout={1000}>
      <WelcomeContainer>
        <Title variant="h3">Welcome to the IQ Test</Title>
        <Description variant="body1">
          Test your cognitive abilities across various categories including Pattern Recognition, Mathematical Reasoning, Verbal Comprehension, Spatial Reasoning, Logical Reasoning, and Verbal Analogies. This test is designed to challenge and assess your IQ comprehensively.
        </Description>

        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} sm={6} md={3}>
            <InfoCard>
              <CardContent>
                <InfoTitle variant="h6">Test Duration</InfoTitle>
                <Typography variant="body2">{testDuration} minutes</Typography>
              </CardContent>
            </InfoCard>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <InfoCard>
              <CardContent>
                <InfoTitle variant="h6">Number of Questions</InfoTitle>
                <Typography variant="body2">{numberOfQuestions} questions</Typography>
              </CardContent>
            </InfoCard>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <InfoCard>
              <CardContent>
                <InfoTitle variant="h6">Categories</InfoTitle>
                <InfoList>
                  {categories.map((category, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircle color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={category.replace(/-/g, ' ')} />
                    </ListItem>
                  ))}
                </InfoList>
              </CardContent>
            </InfoCard>
          </Grid>
        </Grid>

        <Card sx={{ maxWidth: 600, marginTop: 4, padding: 2, backgroundColor: '#f9f9f9' }}>
          <CardContent>
            <InfoTitle variant="h6">Scoring System</InfoTitle>
            <Typography variant="body2" component="pre">
              {scoringSystem}
            </Typography>
          </CardContent>
        </Card>

        <StartButton variant="contained" color="primary" onClick={handleStart}>
          Start Test
        </StartButton>
      </WelcomeContainer>
    </Fade>
  );
};

export default WelcomeScreen;
C:\mygit\Slazy\repo\iq\src\components\QuestionScreen.js
Language detected: javascript
// File: src/QuestionScreen.jsx

import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  LinearProgress,
  Card,
  CardContent,
  RadioGroup,
  FormControlLabel,
  Radio,
  Grid,
  Alert,
} from '@mui/material';
import { styled } from '@mui/system';
import { QuizContext } from './QuizContext';
import ProgressBar from './components/ProgressBar';
import ScoreDisplay from './components/ScoreDisplay';
import Timer from './components/Timer'; // Assuming a Timer component exists

// Styled Components
const QuestionContainer = styled(Card)(({ theme }) => ({
  maxWidth: 800,
  margin: 'auto',
  padding: theme.spacing(4),
  backgroundColor: '#ffffff',
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
  borderRadius: theme.spacing(1),
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
  },
}));

const QuestionHeader = styled(Box)(({ theme }) => ({
  marginBottom: theme.spacing(3),
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
}));

const AnswerOptions = styled(RadioGroup)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const NavigationButtons = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(4),
  display: 'flex',
  justifyContent: 'space-between',
}));

const QuestionScreen = () => {
  const navigate = useNavigate();
  const { questionIdx } = useParams();
  const currentQuestionIndex = parseInt(questionIdx, 10);

  const { questions, userAnswers, setUserAnswers, totalPoints, setTotalPoints, startTime, setStartTime, timeLimit } = useContext(QuizContext);

  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [error, setError] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(timeLimit * 60); // timeLimit in minutes

  useEffect(() => {
    if (!startTime) {
      setStartTime(Date.now());
    }
  }, [startTime, setStartTime]);

  useEffect(() => {
    const timerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      const remaining = timeLimit * 60 - elapsed;
      setTimeRemaining(remaining);

      if (remaining <= 0) {
        clearInterval(timerInterval);
        finishQuiz();
      }
    }, 1000);

    return () => clearInterval(timerInterval);
  }, [startTime, timeLimit]);

  useEffect(() => {
    if (currentQuestionIndex >= questions.length) {
      finishQuiz();
    } else {
      const existingAnswer = userAnswers.find((ans) => ans.id === questions[currentQuestionIndex].id);
      if (existingAnswer) {
        setSelectedAnswer(existingAnswer.answer);
      } else {
        setSelectedAnswer('');
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentQuestionIndex, questions]);

  const finishQuiz = () => {
    navigate('/results');
  };

  const currentQuestion = questions[currentQuestionIndex];

  if (!currentQuestion) {
    return (
      <Box textAlign="center" mt={10}>
        <Typography variant="h5">Question not found.</Typography>
      </Box>
    );
  }

  const handleAnswerChange = (event) => {
    setSelectedAnswer(event.target.value);
    if (error) setError('');
  };

  const handleNext = () => {
    if (!selectedAnswer) {
      setError('Please select an answer before proceeding.');
      return;
    }

    const isCorrect = selectedAnswer === currentQuestion.correctAnswer;
    const earnedPoints = isCorrect ? currentQuestion.points : 0;

    const updatedAnswers = [...userAnswers];
    const existingIndex = updatedAnswers.findIndex((ans) => ans.id === currentQuestion.id);

    if (existingIndex >= 0) {
      updatedAnswers[existingIndex] = {
        ...updatedAnswers[existingIndex],
        answer: selectedAnswer,
        isCorrect,
        points: earnedPoints,
      };
    } else {
      updatedAnswers.push({
        id: currentQuestion.id,
        question: currentQuestion.question,
        selectedAnswer,
        correctAnswer: currentQuestion.correctAnswer,
        isCorrect,
        points: earnedPoints,
        type: currentQuestion.type,
        difficulty: currentQuestion.difficulty,
      });
    }

    setUserAnswers(updatedAnswers);
    setTotalPoints(totalPoints + earnedPoints);

    if (currentQuestionIndex + 1 < questions.length) {
      navigate(`/questions/${currentQuestionIndex + 1}`);
    } else {
      finishQuiz();
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      navigate(`/questions/${currentQuestionIndex - 1}`);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
      .toString()
      .padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  };

  return (
    <Box>
      <QuestionContainer>
        <QuestionHeader>
          <Box>
            <Typography variant="h6">
              Question {currentQuestionIndex + 1} of {questions.length}
            </Typography>
            <Typography variant="subtitle2" color="textSecondary">
              Category: {currentQuestion.type.replace(/-/g, ' ')} | Difficulty: {currentQuestion.difficulty.charAt(0).toUpperCase() + currentQuestion.difficulty.slice(1)}
            </Typography>
          </Box>
          <Box textAlign="right">
            <Timer time={formatTime(timeRemaining)} />
          </Box>
        </QuestionHeader>
        <Box>
          <Typography variant="h5" gutterBottom>
            {currentQuestion.instruction}
          </Typography>
          {currentQuestion.question && (
            <Typography variant="h6" gutterBottom>
              {currentQuestion.question}
            </Typography>
          )}
          <RadioGroup value={selectedAnswer} onChange={handleAnswerChange}>
            {currentQuestion.options.map((option, index) => (
              <FormControlLabel
                key={index}
                value={option}
                control={<Radio />}
                label={option}
              />
            ))}
          </RadioGroup>
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </Box>
        <NavigationButtons>
          <Button
            variant="outlined"
            color="primary"
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </Button>
          <Button variant="contained" color="primary" onClick={handleNext}>
            {currentQuestionIndex + 1 === questions.length ? 'Submit' : 'Next'}
          </Button>
        </NavigationButtons>
      </QuestionContainer>
      <Box mt={4}>
        <ProgressBar current={currentQuestionIndex + 1} total={questions.length} />
      </Box>
      <Box mt={2}>
        <ScoreDisplay />
      </Box>
    </Box>
  );
};

export default QuestionScreen;
C:\mygit\Slazy\repo\iq\src\components\Timer.js
Language detected: javascript
// File: src/components/Timer.jsx

import React, { useEffect, useState } from 'react';
import { Box, Typography, LinearProgress, styled, useTheme } from '@mui/material';
import { keyframes } from '@mui/system';
import PropTypes from 'prop-types';

// Define keyframes for smooth color transition
const colorChange = keyframes`
  from {
    background-color: #4caf50;
  }
  to {
    background-color: #f44336;
  }
`;

// Styled Components
const TimerContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  flexDirection: 'column',
  padding: theme.spacing(2),
  borderRadius: theme.spacing(1),
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[3],
  transition: 'background-color 0.5s ease',
}));

const TimeDisplay = styled(Typography)(({ theme, low }) => ({
  fontSize: '2rem',
  fontWeight: 'bold',
  color: low ? theme.palette.error.main : theme.palette.text.primary,
  animation: low
    ? `${colorChange} 0.5s infinite alternate`
    : 'none',
}));

const ProgressBar = styled(LinearProgress)(({ theme, low }) => ({
  width: '100%',
  height: '10px',
  borderRadius: '5px',
  '& .MuiLinearProgress-bar': {
    backgroundColor: low ? theme.palette.error.main : theme.palette.primary.main,
    transition: 'width 1s linear, background-color 0.5s ease',
  },
}));

const Timer = ({ secondsRemaining, totalTime }) => {
  const theme = useTheme();
  const [progress, setProgress] = useState(100);
  const [isLow, setIsLow] = useState(false);

  useEffect(() => {
    if (totalTime <= 0) return;

    const calculateProgress = () => {
      const percentage = (secondsRemaining / totalTime) * 100;
      setProgress(percentage);
      setIsLow(percentage <= 20); // Change color when remaining time is 20% or less
    };

    calculateProgress();
  }, [secondsRemaining, totalTime]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
      .toString()
      .padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  };

  return (
    <TimerContainer>
      <TimeDisplay low={isLow}>
        {formatTime(secondsRemaining)}
      </TimeDisplay>
      <ProgressBar variant="determinate" value={progress} low={isLow} />
    </TimerContainer>
  );
};

Timer.propTypes = {
  secondsRemaining: PropTypes.number.isRequired,
  totalTime: PropTypes.number.isRequired,
};

export default Timer;
C:\mygit\Slazy\repo\iq\src\components\ProgressBar.js
Language detected: javascript
// File: src/components/ProgressBar.jsx

import React, { useContext, useMemo } from 'react';
import { Box, LinearProgress, Tooltip, Typography, Grid } from '@mui/material';
import { styled } from '@mui/system';
import { QuizContext } from '../QuizContext';
import PropTypes from 'prop-types';

// Styled Components
const ProgressWrapper = styled(Box)(({ theme }) => ({
  width: '100%',
  padding: theme.spacing(2),
}));

const ProgressHeader = styled(Typography)(({ theme }) => ({
  fontWeight: 'bold',
  marginBottom: theme.spacing(1),
  fontSize: '1.2rem',
  color: theme.palette.text.primary,
}));

const CategoryContainer = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const CategoryLabel = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(0.5),
  fontWeight: 500,
  color: theme.palette.text.secondary,
}));

const PercentageLabel = styled(Typography)(({ theme }) => ({
  marginLeft: theme.spacing(1),
  fontWeight: 500,
  color: theme.palette.text.primary,
}));

const StyledLinearProgress = styled(LinearProgress)(({ theme, categorycolor }) => ({
  height: 10,
  borderRadius: 5,
  [`&.${LinearProgress.name}-colorPrimary`]: {
    backgroundColor: theme.palette.grey[300],
  },
  [`& .${LinearProgress.name}-bar`]: {
    borderRadius: 5,
    backgroundColor: categorycolor || theme.palette.primary.main,
    transition: 'width 0.5s ease-in-out',
  },
}));

const OverallProgressBar = styled(LinearProgress)(({ theme }) => ({
  height: 15,
  borderRadius: 7.5,
  [`&.${LinearProgress.name}-colorPrimary`]: {
    backgroundColor: theme.palette.grey[300],
  },
  [`& .${LinearProgress.name}-bar`]: {
    borderRadius: 7.5,
    backgroundColor: theme.palette.primary.main,
    transition: 'width 0.5s ease-in-out',
  },
}));

const ProgressBar = () => {
  const { questions, userAnswers } = useContext(QuizContext);

  // Extract unique categories
  const categories = useMemo(() => {
    const uniqueTypes = [...new Set(questions.map((q) => q.type))];
    return uniqueTypes.map((type) => ({
      type,
      label: type
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' '),
    }));
  }, [questions]);

  // Calculate overall progress
  const totalQuestions = questions.length;
  const answeredQuestions = userAnswers.length;
  const overallProgress = Math.min(
    (answeredQuestions / totalQuestions) * 100,
    100
  );

  // Calculate progress per category
  const categoryProgress = useMemo(() => {
    const progress = {};
    categories.forEach(({ type }) => {
      const totalInCategory = questions.filter((q) => q.type === type).length;
      const answeredInCategory = userAnswers.filter(
        (ans) => ans.type === type
      ).length;
      progress[type] = {
        completed: answeredInCategory,
        total: totalInCategory,
        percentage: Math.min(
          (answeredInCategory / totalInCategory) * 100,
          100
        ),
      };
    });
    return progress;
  }, [categories, questions, userAnswers]);

  return (
    <ProgressWrapper>
      <ProgressHeader>Overall Progress</ProgressHeader>
      <Tooltip
        title={`${answeredQuestions} out of ${totalQuestions} questions completed`}
        arrow
        placement="top"
      >
        <Box display="flex" alignItems="center">
          <Box width="100%" mr={1}>
            <OverallProgressBar variant="determinate" value={overallProgress} />
          </Box>
          <Box minWidth={35}>
            <Typography variant="body2" color="textSecondary">{`${Math.round(
              overallProgress
            )}%`}</Typography>
          </Box>
        </Box>
      </Tooltip>

      <CategoryContainer>
        <ProgressHeader>Progress by Category</ProgressHeader>
        <Grid container spacing={2}>
          {categories.map(({ type, label }, index) => {
            const { completed, total, percentage } = categoryProgress[type];
            // Assign a unique color for each category
            const categoryColors = [
              '#1976d2',
              '#388e3c',
              '#f57c00',
              '#d32f2f',
              '#7b1fa2',
              '#0288d1',
            ];
            const color = categoryColors[index % categoryColors.length];

            return (
              <Grid item xs={12} sm={6} md={4} key={type}>
                <Tooltip
                  title={`${completed} out of ${total} questions completed`}
                  arrow
                  placement="top"
                >
                  <Box display="flex" alignItems="center">
                    <Box width="100%" mr={1}>
                      <StyledLinearProgress
                        variant="determinate"
                        value={percentage}
                        categorycolor={color}
                      />
                    </Box>
                    <PercentageLabel variant="body2">
                      {`${Math.round(percentage)}%`}
                    </PercentageLabel>
                  </Box>
                </Tooltip>
                <CategoryLabel variant="subtitle2">{label}</CategoryLabel>
              </Grid>
            );
          })}
        </Grid>
      </CategoryContainer>
    </ProgressWrapper>
  );
};

ProgressBar.propTypes = {
  // No props required as it uses context
};

export default ProgressBar;
C:\mygit\Slazy\repo\iq\src\components\ScoreDisplay.js
Language detected: javascript
// File: src/components/ScoreDisplay.jsx

import React, { useContext, useEffect, useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import { styled, keyframes } from '@mui/system';
import { QuizContext } from '../QuizContext';
import PropTypes from 'prop-types';

// Define keyframes for animations
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

// Styled Components
const ScoreContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  margin: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[3],
  borderRadius: theme.spacing(1),
  animation: `${fadeIn} 0.6s ease-out`,
}));

const AnimatedTypography = styled(Typography)(({ animate }) => ({
  transition: 'transform 0.5s ease-in-out',
  transform: animate ? 'scale(1.1)' : 'scale(1)',
}));

const CategoryBox = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const ScoreDisplay = () => {
  const { totalPoints, pointsEarnedByCategory } = useContext(QuizContext);
  const [previousTotalPoints, setPreviousTotalPoints] = useState(0);
  const [currentTotalPoints, setCurrentTotalPoints] = useState(0);
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    if (totalPoints !== currentTotalPoints) {
      setPreviousTotalPoints(currentTotalPoints);
      setCurrentTotalPoints(totalPoints);
      setAnimate(true);
      const timer = setTimeout(() => setAnimate(false), 500);
      return () => clearTimeout(timer);
    }
  }, [totalPoints, currentTotalPoints]);

  const calculatePercentage = (earned, total) => {
    if (total === 0) return '0%';
    return `${((earned / total) * 100).toFixed(2)}%`;
  };

  return (
    <ScoreContainer>
      <Typography variant="h5" gutterBottom>
        Your Score
      </Typography>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={6}>
          <Box display="flex" alignItems="center">
            <Typography variant="subtitle1">Total Points:</Typography>
            <Box ml={1}>
              <AnimatedTypography variant="h4" animate={animate ? 1 : 0}>
                {currentTotalPoints} / {totalPoints}
              </AnimatedTypography>
            </Box>
          </Box>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Box display="flex" alignItems="center">
            <Typography variant="subtitle1">Percentage:</Typography>
            <Box ml={1}>
              <AnimatedTypography variant="h4" animate={animate ? 1 : 0}>
                {calculatePercentage(currentTotalPoints, totalPoints)}
              </AnimatedTypography>
            </Box>
          </Box>
        </Grid>
      </Grid>

      <CategoryBox>
        <Typography variant="h6" gutterBottom>
          Points by Category
        </Typography>
        <Grid container spacing={2}>
          {Object.entries(pointsEarnedByCategory).map(([category, details]) => (
            <Grid item xs={12} sm={6} md={4} key={category}>
              <Tooltip
                title={`${details.earned} out of ${details.total} points earned (${calculatePercentage(
                  details.earned,
                  details.total
                )})`}
                arrow
                placement="top"
              >
                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    {category.replace(/-/g, ' ')}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={(details.earned / details.total) * 100}
                    color="primary"
                  />
                  <Typography variant="body2" align="right">
                    {calculatePercentage(details.earned, details.total)}
                  </Typography>
                </Box>
              </Tooltip>
            </Grid>
          ))}
        </Grid>
      </CategoryBox>
    </ScoreContainer>
  );
};

ScoreDisplay.propTypes = {
  // No props required as it uses context
};

export default ScoreDisplay;
C:\mygit\Slazy\repo\iq\src\components\ResultsScreen.js
Language detected: javascript
C:\mygit\Slazy\repo\iq\package.json
Language detected: json
{
  "name": "iq-test",
  "version": "1.0.0",
  "description": "An interactive IQ test application built with React, Material-UI, and React Router.",
  "main": "src/index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src --ext .js,.jsx",
    "format": "prettier --write src/**/*.{js,jsx}"
  },
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.0",
    "@mui/material": "^5.14.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.1",
    "recharts": "^2.6.2"
  },
  "devDependencies": {
    "@babel/core": "^7.22.20",
    "eslint": "^8.50.0",
    "eslint-config-react-app": "^7.0.1",
    "prettier": "^3.0.0",
    "react-scripts": "^5.0.1"
  },
  "keywords": ["iq", "test", "react", "material-ui", "recharts"],
  "author": "Your Name",
  "license": "ISC",
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 2 chrome versions",
      "last 2 firefox versions",
      "last 2 safari versions",
      "last 1 edge version"
    ]
  }
}
C:\mygit\Slazy\repo\iq\src\index.js
Language detected: javascript
// File: src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Global styles
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import theme from './theme'; // Custom Material-UI theme
import ErrorBoundary from './ErrorBoundary';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
C:\mygit\Slazy\repo\iq\src\theme.js
Language detected: javascript
// src/theme.js

import { createTheme } from '@mui/material/styles';
import { red } from '@mui/material/colors';

// Define custom color palette
const customPalette = {
  primary: {
    light: '#6ec6ff',
    main: '#2196f3',
    dark: '#0069c0',
    contrastText: '#ffffff',
  },
  secondary: {
    light: '#ff7961',
    main: '#f44336',
    dark: '#ba000d',
    contrastText: '#ffffff',
  },
  error: {
    main: red.A400,
  },
  background: {
    default: '#f4f6f8',
    paper: '#ffffff',
  },
  text: {
    primary: '#333333',
    secondary: '#757575',
  },
};

// Define typography scales
const typography = {
  fontFamily: [
    'Roboto',
    '"Helvetica Neue"',
    'Arial',
    'sans-serif',
    '"Apple Color Emoji"',
    '"Segoe UI Emoji"',
    '"Segoe UI Symbol"',
  ].join(','),
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 700,
    lineHeight: 1.3,
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 700,
    lineHeight: 1.4,
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 700,
    lineHeight: 1.5,
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 700,
    lineHeight: 1.6,
  },
  h6: {
    fontSize: '1rem',
    fontWeight: 700,
    lineHeight: 1.7,
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.75,
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.57,
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.43,
  },
  button: {
    fontSize: '0.875rem',
    fontWeight: 500,
    textTransform: 'uppercase',
  },
  caption: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.66,
  },
  overline: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 2.66,
    textTransform: 'uppercase',
  },
};

// Define spacing
const spacing = 8;

// Define breakpoints for responsiveness
const breakpoints = {
  values: {
    xs: 0,    // Mobile devices
    sm: 600,  // Small screens
    md: 900,  // Medium screens
    lg: 1200, // Large screens
    xl: 1536, // Extra large screens
  },
};

// Base theme configuration
const baseTheme = createTheme({
  palette: {
    mode: 'light', // Default mode
    ...customPalette,
  },
  typography,
  spacing,
  breakpoints,
  shape: {
    borderRadius: 8, // Consistent border radius
  },
  shadows: [
    'none',
    '0px 1px 3px rgba(0,0,0,0.2)',
    '0px 1px 5px rgba(0,0,0,0.2)',
    '0px 3px 5px rgba(0,0,0,0.2)',
    '0px 2px 4px rgba(0,0,0,0.2)',
    '0px 3px 5px rgba(0,0,0,0.3)',
    '0px 4px 6px rgba(0,0,0,0.3)',
    // Add more shadows as needed
  ],
  transitions: {
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          textTransform: 'none',
          fontWeight: 600,
          padding: `${spacing * 1}px ${spacing * 3}px`,
          transition: 'background-color 0.3s ease, transform 0.2s ease',
          '&:hover': {
            backgroundColor: customPalette.primary.dark,
            transform: 'translateY(-2px)',
          },
        },
        contained: {
          boxShadow: 'none',
          '&:active': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: 'none',
          borderBottom: `1px solid ${customPalette.grey[300]}`,
          transition: 'background-color 0.3s ease',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
          transition: 'transform 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0px 6px 25px rgba(0, 0, 0, 0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: customPalette.background.paper,
          color: customPalette.text.primary,
        },
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: customPalette.text.primary,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            '& fieldset': {
              borderColor: customPalette.grey[400],
            },
            '&:hover fieldset': {
              borderColor: customPalette.primary.main,
            },
            '&.Mui-focused fieldset': {
              borderColor: customPalette.primary.dark,
            },
          },
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          width: 50,
          height: 28,
          padding: 0,
          margin: 8,
        },
        switchBase: {
          padding: 4,
          '&.Mui-checked': {
            transform: 'translateX(22px)',
            color: customPalette.primary.contrastText,
            '& + .MuiSwitch-track': {
              backgroundColor: customPalette.primary.main,
              opacity: 1,
            },
          },
        },
        thumb: {
          width: 20,
          height: 20,
          boxShadow: 'none',
        },
        track: {
          borderRadius: 14,
          backgroundColor: customPalette.grey[400],
          opacity: 1,
          transition: 'background-color 0.3s ease',
        },
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          borderRadius: 4,
          padding: `${spacing / 2}px ${spacing}px`,
          backgroundColor: customPalette.grey[900],
          color: customPalette.grey[50],
          fontSize: '0.875rem',
        },
        arrow: {
          color: customPalette.grey[900],
        },
      },
    },
    MuiSnackbar: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 12,
        },
      },
    },
    // Add more component overrides as needed
  },
});

// Extend the theme to include dark mode
const getTheme = (mode) =>
  createTheme({
    ...baseTheme,
    palette: {
      ...baseTheme.palette,
      mode,
      ...(mode === 'dark' && {
        primary: {
          ...customPalette.primary,
          main: '#90caf9',
        },
        secondary: {
          ...customPalette.secondary,
          main: '#f48fb1',
        },
        background: {
          default: '#121212',
          paper: '#1e1e1e',
        },
        text: {
          primary: '#ffffff',
          secondary: '#bdbdbd',
        },
        grey: {
          ...baseTheme.palette.grey,
          300: '#424242',
          500: '#616161',
          700: '#9e9e9e',
        },
      }),
    },
    components: {
      ...baseTheme.components,
      MuiPaper: {
        ...baseTheme.components.MuiPaper,
        styleOverrides: {
          ...baseTheme.components.MuiPaper.styleOverrides,
          root: {
            ...baseTheme.components.MuiPaper.styleOverrides.root,
            backgroundColor:
              mode === 'dark'
                ? baseTheme.palette.background.paper
                : customPalette.background.paper,
          },
        },
      },
    },
  });

export default getTheme;
C:\mygit\Slazy\repo\iq\src\ErrorBoundary.js
Language detected: javascript
// File: src/ErrorBoundary.jsx

import React, { Component } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  useTheme,
} from '@mui/material';
import { styled } from '@mui/system';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import ReplayIcon from '@mui/icons-material/Replay';
import PropTypes from 'prop-types';

// Styled Components
const ErrorContainer = styled(Paper)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(6),
  minHeight: '100vh',
  backgroundColor: theme.palette.background.paper,
  textAlign: 'center',
}));

const ErrorIcon = styled(ErrorOutlineIcon)(({ theme }) => ({
  fontSize: 80,
  color: theme.palette.error.main,
  marginBottom: theme.spacing(2),
}));

const ErrorMessage = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  fontWeight: 600,
  color: theme.palette.error.dark,
}));

const ErrorDetails = styled(Box)(({ theme }) => ({
  maxWidth: 600,
  width: '100%',
  marginTop: theme.spacing(2),
  padding: theme.spacing(2),
  backgroundColor: theme.palette.grey[100],
  borderRadius: theme.shape.borderRadius,
  overflowX: 'auto',
}));

const RetryButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(4),
}));

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
    this.handleRetry = this.handleRetry.bind(this);
  }

  static getDerivedStateFromError(error) {
    // Update state to display fallback UI on next render
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can log the error to an error reporting service here
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({ error, errorInfo });
    // Example: Log to external service
    // logErrorToService(error, errorInfo);
  }

  handleRetry() {
    // Reset the error state and attempt to re-render children
    this.setState({ hasError: false, error: null, errorInfo: null });
    // Optionally, you can implement additional logic to reset application state
  }

  render() {
    const { hasError, error, errorInfo } = this.state;
    const theme = this.props.theme || useTheme();

    if (hasError) {
      return (
        <ErrorContainer elevation={3}>
          <ErrorIcon />
          <ErrorMessage variant="h4">
            Oops! Something went wrong.
          </ErrorMessage>
          <Typography variant="body1">
            An unexpected error has occurred. Please try reloading the page or contact support if the problem persists.
          </Typography>
          {process.env.NODE_ENV !== 'production' && error && errorInfo && (
            <React.Fragment>
              <ErrorDetails>
                <Typography variant="h6">Error Details:</Typography>
                <Typography variant="body2" color="textSecondary">
                  {error.toString()}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {errorInfo.componentStack}
                </Typography>
              </ErrorDetails>
            </React.Fragment>
          )}
          <RetryButton
            variant="contained"
            color="primary"
            startIcon={<ReplayIcon />}
            onClick={this.handleRetry}
          >
            Try Again
          </RetryButton>
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
  theme: PropTypes.object,
};

export default ErrorBoundary;
C:\mygit\Slazy\repo\iq\src\index.css
Language detected: css
/*--------------------------------------------------------------
  1. RESET Default Browser Styles (CSS Reset)
--------------------------------------------------------------*/
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
  display: block;
}

body {
  line-height: 1.6;
  font-family: 'Roboto', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  font-size: 16px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

ol, ul {
  list-style: none;
}

a {
  text-decoration: none;
  color: inherit;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

button {
  cursor: pointer;
  border: none;
  background: none;
  font: inherit;
}

/*--------------------------------------------------------------
  2. SETUP Base Styles
--------------------------------------------------------------*/
:root {
  /* Color Palette */
  --primary-color: #1976d2;
  --secondary-color: #ff5722;
  --background-color: #f4f6f8;
  --background-color-dark: #121212;
  --text-color: #333333;
  --text-color-dark: #e0e0e0;
  --border-color: #dddddd;
  
  /* Typography */
  --font-size-base: 16px;
  --font-size-lg: 1.25rem; /* 20px */
  --font-size-sm: 0.875rem; /* 14px */
  
  /* Spacing */
  --spacing-unit: 8px;
  
  /* Border Radius */
  --border-radius: 4px;
  
  /* Shadows */
  --shadow-light: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-dark: 0 2px 4px rgba(0, 0, 0, 0.2);
}

body.dark-mode {
  --background-color: var(--background-color-dark);
  --text-color: var(--text-color-dark);
}

/* Base Typography */
h1, h2, h3, h4, h5, h6 {
  margin-bottom: calc(var(--spacing-unit) / 2);
  font-weight: 700;
  line-height: 1.2;
}

p {
  margin-bottom: var(--spacing-unit);
}

a:hover {
  color: var(--primary-color);
}

/* Utility Classes */
.u-text-center {
  text-align: center;
}

.u-text-right {
  text-align: right;
}

.u-mb-small {
  margin-bottom: var(--spacing-unit);
}

.u-mt-small {
  margin-top: var(--spacing-unit);
}

.u-p-1 {
  padding: var(--spacing-unit);
}

.u-p-2 {
  padding: calc(var(--spacing-unit) * 2);
}

.u-border {
  border: 1px solid var(--border-color);
}

.u-rounded {
  border-radius: var(--border-radius);
}

.u-shadow {
  box-shadow: var(--shadow-light);
}

.u-transition {
  transition: all 0.3s ease;
}

/*--------------------------------------------------------------
  3. GLOBAL ANIMATIONS
--------------------------------------------------------------*/
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out forwards;
}

.animate-slide-in-up {
  animation: slideInUp 0.7s ease-out forwards;
}

/*--------------------------------------------------------------
  4. SCROLLBAR STYLING
--------------------------------------------------------------*/
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: var(--background-color);
}

::-webkit-scrollbar-thumb {
  background-color: var(--primary-color);
  border-radius: var(--border-radius);
  border: 3px solid var(--background-color);
}

::-webkit-scrollbar-thumb:hover {
  background-color: darken(var(--primary-color), 10%);
}

/* Firefox Scrollbar */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--primary-color) var(--background-color);
}

/*--------------------------------------------------------------
  5. RESPONSIVE FONT SIZING
--------------------------------------------------------------*/
html {
  font-size: 100%; /* 16px */
}

@media (max-width: 1200px) {
  html {
    font-size: 93.75%; /* 15px */
  }
}

@media (max-width: 992px) {
  html {
    font-size: 87.5%; /* 14px */
  }
}

@media (max-width: 768px) {
  html {
    font-size: 81.25%; /* 13px */
  }
}

@media (max-width: 576px) {
  html {
    font-size: 75%; /* 12px */
  }
}

/*--------------------------------------------------------------
  6. TRANSITIONS AND TRANFORMS
--------------------------------------------------------------*/
.transition {
  transition: all 0.3s ease;
}

.transform-scale-up {
  transform: scale(1.05);
}

.transform-scale-down {
  transform: scale(0.95);
}

/* Smooth Hover Effects */
.button-hover:hover,
.card-hover:hover {
  background-color: var(--primary-color);
  color: #fff;
  box-shadow: var(--shadow-dark);
}

/*--------------------------------------------------------------
  7. ACCESSIBILITY
--------------------------------------------------------------*/
:focus {
  outline: 2px dashed var(--primary-color);
  outline-offset: 4px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

/*--------------------------------------------------------------
  8. OPTIMIZATIONS
--------------------------------------------------------------*/
/* Reduce motion preference */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
C:\mygit\Slazy\repo\iq\public\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">

<head>
  <!-- 1. Meta Tags -->
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- 2. SEO Meta Tags -->
  <meta name="description" content="Take our comprehensive IQ test to assess and enhance your cognitive abilities across various categories.">
  <meta name="keywords" content="IQ Test, Cognitive Abilities, Pattern Recognition, Mathematical Reasoning, Verbal Comprehension, Spatial Reasoning, Logical Reasoning, Verbal Analogies">
  <meta name="author" content="Your Name">
  <meta name="robots" content="index, follow">

  <!-- 3. Open Graph Meta Tags for Social Sharing -->
  <meta property="og:title" content="IQ Test - Assess Your Cognitive Abilities">
  <meta property="og:description" content="Engage with our interactive IQ test covering multiple reasoning categories to evaluate and improve your intelligence quotient.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.yourdomain.com/iq-test">
  <meta property="og:image" content="https://www.yourdomain.com/images/iq-test-og-image.jpg">
  <meta property="og:site_name" content="Your Website Name">

  <!-- 4. Twitter Card Meta Tags -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="IQ Test - Assess Your Cognitive Abilities">
  <meta name="twitter:description" content="Engage with our interactive IQ test covering multiple reasoning categories to evaluate and improve your intelligence quotient.">
  <meta name="twitter:image" content="https://www.yourdomain.com/images/iq-test-twitter-image.jpg">

  <!-- 5. Favicon and Icons -->
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16x16.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="mask-icon" href="/images/safari-pinned-tab.svg" color="#5bbad5">
  <meta name="msapplication-TileColor" content="#da532c">
  <meta name="theme-color" content="#ffffff">

  <!-- 6. External Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- 7. CSS Stylesheets -->
  <link rel="stylesheet" href="/css/main.css">
  <link rel="stylesheet" href="/css/app.css">

  <!-- 8. PWA Meta Tags -->
  <meta name="application-name" content="IQ Test App">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="IQ Test">
  
  <!-- 9. Twitter and Facebook Integration -->
  <meta name="twitter:site" content="@yourtwitterhandle">
  <meta name="twitter:creator" content="@yourtwitterhandle">

  <!-- 10. Preconnect for Performance Optimization -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- 11. Structured Data for SEO -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "IQ Test",
    "url": "https://www.yourdomain.com/iq-test",
    "applicationCategory": "Education",
    "operatingSystem": "All",
    "description": "An interactive IQ test application to assess and enhance cognitive abilities across various reasoning categories.",
    "author": {
      "@type": "Person",
      "name": "Your Name"
    },
    "image": "https://www.yourdomain.com/images/iq-test-logo.png"
  }
  </script>

  <!-- 12. Performance Optimizations -->
  <link rel="preload" href="/fonts/Roboto-Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/Roboto-Bold.woff2" as="font" type="font/woff2" crossorigin>
  
  <!-- 13. Analytics (Optional) -->
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID');
  </script>

  <!-- 14. Service Worker for PWA -->
  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
          console.log('ServiceWorker registration successful with scope:', registration.scope);
        }, function(err) {
          console.log('ServiceWorker registration failed:', err);
        });
      });
    }
  </script>

  <!-- 15. Accessibility Enhancements -->
  <style>
    .visually-hidden {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      border: 0;
    }
  </style>

  <!-- 16. Page Title -->
  <title>IQ Test - Assess and Enhance Your Cognitive Abilities</title>
</head>

<body>
  <!-- 17. Content Placeholder -->
  <div id="root"></div>

  <!-- 18. JavaScript Files -->
  <script src="/js/app.js" defer></script>
  <script src="/js/helper.js" defer></script>
</body>

</html>
