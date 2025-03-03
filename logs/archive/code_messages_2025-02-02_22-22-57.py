C:\mygit\BLazy\repo\glbj\config.py
Language detected: python
import yaml
from dataclasses import dataclass, asdict, field
from typing import Any

@dataclass
class Config:
    # Game Settings
    initial_bankroll: int = 1000
    min_bet: int = 5
    max_bet: int = 100
    num_decks: int = 6
    
    # RL Parameters
    learning_rate: float = 0.01
    epsilon: float = 0.9
    gamma: float = 0.95
    
    # Display Settings
    display_game: bool = False
    display_results: bool = True
    display_policy: bool = True
    
    def to_yaml(self, filepath: str):
        with open(filepath, 'w') as f:
            yaml.dump(asdict(self), f, default_flow_style=False)
    
    def from_yaml(self, filepath: str):
        with open(filepath, 'r') as f:
            loaded_config = yaml.safe_load(f)
        self.__dict__.update(loaded_config)

# Example usage
if __name__ == "__main__":
    config = Config()
    print("Default Config:", asdict(config))
    
    # Save configuration to a YAML file
    config_filepath = "config.yaml"
    config.to_yaml(config_filepath)
    
    # Load configuration from the YAML file
    config.from_yaml(config_filepath)
    print("Loaded Config:", asdict(config))
C:\mygit\BLazy\repo\glbj\game_engine.py
Language detected: python
"""
blackjack_core.py: This module handles all core game logic for the blackjack game.
It includes card/Deck management, hand evaluation, basic strategy implementation,
and game state management.
"""

import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from config import Config


class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()


class Value(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11


@dataclass
class Card:
    suit: Suit
    value: Value

    def __repr__(self):
        return f"{self.value.name.capitalize()} of {self.suit.name.capitalize()}"


@dataclass
class Deck:
    cards: List[Card] = field(init=False)

    def __post_init__(self):
        self.cards = [Card(suit, value) for suit in Suit for value in Value]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)


@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    bets: float = 0.0
    is_split: bool = False
    is_double_down: bool = False

    def add_card(self, card: Card):
        self.cards.append(card)

    def get_value(self):
        total = sum(card.value.value for card in self.cards)
        num_aces = sum(card.value is Value.ACE for card in self.cards)

        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1

        return total

    def clear_hand(self):
        self.cards.clear()
        self.bets = 0.0
        self.is_split = False
        self.is_double_down = False

    def __repr__(self):
        return f"Hand({[str(card) for card in self.cards]}, bets={self.bets}, split={self.is_split}, double={self.is_double_down})"


class GameState:
    def __init__(self, config: Config):
        self.config = config
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.hands = [self.player_hand]
        self.running_count = 0
        self.true_count = 0
        self.decks_used = 0

    def new_round(self):
        if len(self.deck) < (len(self.deck) * 0.25):  # Refill and shuffle the deck when less than 25% of cards remain
            self.deck = Deck()
            self.decks_used += 1

        self.player_hand.clear_hand()
        self.dealer_hand.clear_hand()
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def update_running_count(self, value: int):
        self.running_count += value

    def update_true_count(self):
        self.true_count = self.running_count / (self.deck.num_decks * 52 - self.deck.num_decks * 0.75 * len(self.deck))

    def get_game_state(self) -> dict:
        return {
            "player_hand": self.player_hand.get_value(),
            "dealer_upcard": self.dealer_hand.cards[0].value.value,
            "running_count": self.running_count,
            "true_count": self.true_count,
            "decks_used": self.decks_used
        }

    def __repr__(self):
        return (
            f"GameState(deck_cards={len(self.deck)}, player_hand={self.player_hand!r}, dealer_hand={self.dealer_hand!r}, "
            f"running_count={self.running_count}, true_count={self.true_count}, decks_used={self.decks_used})"
        )


def basic_strategy(state: dict, config: Config) -> int:
    """
    Basic strategy implementation based on current game state.
    """
    player_value = state["player_hand"]
    dealer_upcard = state["dealer_upcard"]

    # Simple decision logic based on the Blackjack basic strategy
    if 5 <= dealer_upcard <= 6:
        return 1  # Stand
    elif player_value >= 17:
        return 1  # Stand
    elif 8 <= player_value <= 11:
        return 2  # Hit
    else:
        return 3  # Stand or other actions if you want it more complex

# Example Usage
if __name__ == "__main__":
    config = Config()
    state = GameState(config)

    state.new_round()
    print(f"Initial State: {state}")
    action = basic_strategy(state.get_game_state(), config)
    print(f"Action based on basic strategy: {action}")
C:\mygit\BLazy\repo\glbj\rl_agent.py
Language detected: python
# Your code goes here

import numpy as np
import torch
import random
from collections import deque
from typing import Tuple
from config import Config
from game_engine import GameState

# Define constants
LEARNING_RATE = 0.01
GAMMA = 0.95
EPSILON = 0.9
EPS_DECAY = 0.99
MIN_EPSILON = 0.1
BATCH_SIZE = 32
TARGET_UPDATE_FREQ = 10
MEMORY_SIZE = 10000

# Define the neural network for Q-learning
class BetSizingNetwork(torch.nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super(BetSizingNetwork, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 64)
        self.fc2 = torch.nn.Linear(64, 64)
        self.fc3 = torch.nn.Linear(64, output_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Experience Replay Buffer
class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch)
        return np.array(state), np.array(action), np.array(reward), np.array(next_state), np.array(done)

# Agent class for Q-learning
class BetSizingAgent:
    def __init__(self, config: Config):
        self.config = config
        self.input_size = 3  # Bankroll, True Count, Bet Size
        self.output_size = config.max_bet - config.min_bet + 1  # Action space
        
        self.policy_net = BetSizingNetwork(self.input_size, self.output_size)
        self.target_net = BetSizingNetwork(self.input_size, self.output_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(), lr=LEARNING_RATE)
        self.memory = ReplayBuffer(MEMORY_SIZE)
        self.steps_done = 0
    
    def select_action(self, state: Tuple[int, float, int], epsilon: float):
        sample = random.random()
        if sample > epsilon:
            with torch.no_grad():
                return self.policy_net(torch.tensor([state], dtype=torch.float)).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.output_size)]], dtype=torch.long)
    
    def optimize_model(self):
        if len(self.memory.buffer) < BATCH_SIZE:
            return
        states, actions, rewards, next_states, dones = self.memory.sample(BATCH_SIZE)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.ByteTensor(dones)
        
        current_q_values = self.policy_net(states).gather(1, actions)
        next_max_q_values = self.target_net(next_states).max(1)[0].detach()
        expected_q_values = rewards + (GAMMA * next_max_q_values * (1 - dones))
        
        loss = torch.nn.functional.mse_loss(current_q_values, expected_q_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.steps_done += 1
        if self.steps_done % TARGET_UPDATE_FREQ == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

# Save/load functionality
class BetSizingModel:
    def __init__(self, agent: BetSizingAgent):
        self.agent = agent

    def save_model(self, filepath: str):
        torch.save(self.agent.policy_net.state_dict(), filepath)

    def load_model(self, filepath: str):
        self.agent.policy_net.load_state_dict(torch.load(filepath))
        self.agent.target_net.load_state_dict(self.agent.policy_net.state_dict())
        self.agent.target_net.eval()

# Initialize configurations and agents
def main():
    config = Config()
    agent = BetSizingAgent(config)
    model = BetSizingModel(agent)

    # Example: Saving and loading model
    model.save_model('bet_sizing_model.pth')
    model.load_model('bet_sizing_model.pth')

if __name__ == '__main__':
    main()
C:\mygit\BLazy\repo\glbj\visualization.py
Language detected: python
# Import statements
import pygame
import numpy as np
from matplotlib import pyplot as plt
import random
from collections import deque
from config import Config
from game_engine import GameState
from rl_agent import BetSizingAgent

# Initialize PyGame
pygame.init()

# Constants for visualization
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (40, 120, 60)
TEXT_COLOR = (255, 255, 255)
CARD_COLOR = (255, 255, 255)
CARD_BACK_IMAGE = pygame.image.load('resources/card_back.png')

# Initialize fonts
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Visualizer")

# Sprite groups for rendering
cards_sprite_group = pygame.sprite.Group()

class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card: Card, position):
        super().__init__()
        self.image = pygame.image.load(f'resources/{card.suit.name}_{card.value.name}.png')
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Visualization:
    def __init__(self, config: Config, agent: BetSizingAgent):
        self.config = config
        self.agent = agent
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.deck = Deck()
        self.game_state = GameState(config)
        self.performance_queue = deque(maxlen=50)
        self.game_count = 0
        self.total_reward = 0
        self.performance_data = []

    def initialize_game(self):
        self.game_state.new_round()

        # Draw all cards
        for idx, hand in enumerate(self.game_state.hands):
            for card in hand.cards:
                card_sprite = CardSprite(card, (100 + idx * 150, 200))
                cards_sprite_group.add(card_sprite)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    def render_game(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Render all cards
        cards_sprite_group.draw(screen)
        
        # Render text
        score_text = FONT.render(f"Player Hand: {self.game_state.player_hand.get_value()}", True, TEXT_COLOR)
        dealer_text = FONT.render(f"Dealer Upcard: {self.game_state.dealer_hand.cards[0].value.value}", True, TEXT_COLOR)
        count_text = FONT.render(f"Running Count: {self.game_state.running_count}", True, TEXT_COLOR)
        true_count_text = FONT.render(f"True Count: {self.game_state.true_count:.2f}", True, TEXT_COLOR)
        reward_text = FONT.render(f"Total Reward: {self.total_reward}", True, TEXT_COLOR)

        self.screen.blit(score_text, (30, 30))
        self.screen.blit(dealer_text, (30, 70))
        self.screen.blit(count_text, (30, 110))
        self.screen.blit(true_count_text, (30, 150))
        self.screen.blit(reward_text, (30, 190))

        pygame.display.flip()

    def track_performance(self, reward):
        self.total_reward += reward
        self.game_count += 1
        self.performance_queue.append(reward)
        if self.game_count % 10 == 0:
            avg_performance = sum(self.performance_queue) / len(self.performance_queue)
            self.performance_data.append(avg_performance)
            self.plot_performance()

    def plot_performance(self):
        plt.clf()
        plt.plot(self.performance_data, label='Average Reward')
        plt.xlabel('Games')
        plt.ylabel('Reward')
        plt.title('Performance Tracking')
        plt.legend()
        plt.pause(0.01)

    def main_loop(self):
        while self.running:
            self.process_events()
            self.initialize_game()
            self.render_game()
            self.clock.tick(60)  # Cap at 60 FPS

if __name__ == "__main__":
    config = Config()
    agent = BetSizingAgent(config)
    visualizer = Visualization(config, agent)
    visualizer.main_loop()
C:\mygit\BLazy\repo\glbj\main.py
Language detected: python
# main.py: Main application file for the blackjack reinforcement learning system
import argparse
import os
import logging
from config import Config
from game_engine import GameState
from rl_agent import BetSizingAgent, BetSizingModel
from visualization import Visualization

# Set up logging
logging.basicConfig(level=logging.INFO)

def initialize_components(config):
    game_state = GameState(config)
    agent = BetSizingAgent(config)
    model = BetSizingModel(agent)
    visualizer = Visualization(config, agent)
    return game_state, agent, model, visualizer

def train_agent(agent, model, game_state, episodes=100):
    for episode in range(episodes):
        game_state.new_round()
        episode_rewards = 0
        
        # Main game loop for each episode
        while True:
            state = game_state.get_game_state()
            action = agent.select_action(tuple(state.values()), EPSILON)
            
            # Simulate environment step - this would normally involve game logic
            reward, done = simulate_step(game_state, action, config)
            episode_rewards += reward
            
            agent.memory.push(state, action, reward, game_state.get_game_state(), done)
            agent.optimize_model()
            
            if done:
                break
        
        logging.info(f"Episode {episode} ended with reward {episode_rewards}")
        
        if episode % 10 == 0:
            model.save_model(f'checkpoint_{episode}.pth')

def simulate_step(game_state, action, config):
    # Dummy function to simulate the environment step
    # In a real scenario, this would involve interacting with the game logic
    # Here we simulate a simple reward based on action
    if action == 0:  # Assume 0 is stand
        reward = game_state.player_hand.get_value() - game_state.dealer_hand.get_value()
    else:
        reward = -1  # Penalize for other actions
    done = True  # Assuming the game ends after one step for simplicity
    return reward, done

def play_game(agent, game_state):
    while not game_state.player_hand.get_value() > 21:
        state = game_state.get_game_state()
        action = agent.select_action(tuple(state.values()), 0.05)  # Use a small epsilon for playing
        simulate_step(game_state, action, config)
        game_state.render_game()

def evaluate_agent(agent, model, episodes=10):
    total_rewards = 0
    for _ in range(episodes):
        game_state.new_round()
        while True:
            state = game_state.get_game_state()
            action = agent.select_action(tuple(state.values()), 0.05)  # Use a small epsilon for evaluating
            reward, done = simulate_step(game_state, action, config)
            total_rewards += reward
            if done:
                break
    logging.info(f"Evaluation over {episodes} episodes with average reward: {total_rewards / episodes}")

def parse_args():
    parser = argparse.ArgumentParser(description="Run the blackjack reinforcement learning system")
    parser.add_argument("--mode", choices=["train", "play", "evaluate"], required=True, help="Mode to run the system")
    parser.add_argument("--model", type=str, help="Path to the model checkpoint for load and save operations")
    return parser.parse_args()

def main():
    args = parse_args()
    config = Config()
    game_state, agent, model, visualizer = initialize_components(config)
    
    if args.mode == "train":
        train_agent(agent, model, game_state)
    elif args.mode == "play":
        if not args.model:
            raise ValueError("Model path must be provided for play mode")
        model.load_model(args.model)
        play_game(agent, game_state)
    elif args.mode == "evaluate":
        if not args.model:
            raise ValueError("Model path must be provided for evaluate mode")
        model.load_model(args.model)
        evaluate_agent(agent, model)

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\glbj\generate_card_images.py
Language detected: python
# Import required libraries
from PIL import Image, ImageDraw, ImageFont
import os
from game_engine import Suit, Value

# Function to create a card image
def create_card_image(suit, value, font_path=None):
    # Create a new image with white background
    card_width, card_height = 100, 150
    card_image = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(card_image)

    # Load font, use default if font_path is not provided
    if font_path is None:
        font_path = os.path.join(os.getcwd(), 'arial.ttf')
    try:
        font = ImageFont.truetype(font_path, size=12)
    except IOError:
        font = ImageFont.load_default()

    # Draw the suit symbol
    if value != Value.ACE and value != Value.JACK and value != Value.QUEEN and value != Value.KING:
        draw.text((10, 10), str(value.value), fill="black", font=font)
        draw.text((80, 130), str(value.value), fill="black", font=font)
    else:
        draw.text((10, 10), value.name.capitalize(), fill="black", font=font)
        draw.text((80, 130), value.name.capitalize(), fill="black", font=font)

    # Draw suit symbol(s)
    if suit == Suit.HEARTS:
        draw.line([(20, 20), (30, 30)], fill="red", width=2)
        draw.line([(30, 20), (20, 30)], fill="red", width=2)
    if suit == Suit.DIAMONDS:
        draw.rectangle([(20, 20), (30, 30)], outline="red", width=2)
    if suit in (Suit.SPADES, Suit.CLUBS):
        draw.rectangle([(20, 130), (30, 140)], outline="black", width=2)

    # Return the created image
    return card_image

# Function to create and save card images
def generate_card_images():
    # Ensure the directory exists
    resources_dir = os.path.join(os.getcwd(), 'resources')
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    
    # Generate and save all card images
    for suit in Suit:
        for value in Value:
            img = create_card_image(suit, value, font_path='arial.ttf')
            img.save(os.path.join(resources_dir, f'{suit.name}_{value.name}.png'))

    # Generate card back image
    card_back_img = Image.new('RGB', (100, 150), color='white')
    draw = ImageDraw.Draw(card_back_img)
    back_color = (150, 150, 150)
    draw.rectangle([(10, 10), (90, 140)], outline=back_color, width=5)
    for i in range(10, 140, 30):
        draw.line([(50, i), (50, i+10)], fill=back_color, width=5)
    draw.line([(35, 65), (65, 65)], fill=back_color, width=5)
    draw.line([(65, 65), (65, 95)], fill=back_color, width=5)
    draw.line([(35, 125), (65, 125)], fill=back_color, width=5)
    card_back_img.save(os.path.join(resources_dir, 'card_back.png'))

# Entry point
if __name__ == '__main__':
    generate_card_images()
C:\mygit\BLazy\repo\glbj\requirements.txt
Language detected: plaintext
# requirements.txt

pygame==2.1.0
numpy==1.21.2
matplotlib==3.4.3
torch==1.10.0
Pillow==8.4.0
pyyaml==5.4.1
C:\mygit\BLazy\repo\glbj\README.md
Language detected: markdown
# Blackjack Reinforcement Learning (BLazy) Project

## Overview

This project focuses on implementing a Blackjack game using reinforcement learning techniques. The goal is to develop a neural network-based agent capable of making optimal betting decisions in a multi-deck Blackjack game. The project covers several aspects including game engine development, reinforcement learning, visualization, and training the agent.

## Features

- **Configurable game settings**: Easily change parameters such as initial bankroll, minimum and maximum bets, number of decks, and learning parameters.
- **Basic Strategy Implementation**: A simple decision logic based on the Blackjack basic strategy.
- **Reinforcement Learning Integration**: An advanced neural network agent trained using Q-learning.
- **Visualization**: An interactive PyGame interface to visualize the game, including card rendering and performance tracking.
- **Saving and Loading Model States**: Support for saving and loading trained models for further training or direct gameplay.

## Dependencies

- Python 3.x
- [PyTorch](https://pytorch.org/) (for machine learning tasks)
- [NumPy](https://numpy.org/) (for numerical computations)
- [Matplotlib](https://matplotlib.org/) (for plotting)
- [PyYAML](https://pyyaml.org/) (for configuration files)
- [PyGame](https://www.pygame.org/) (for visualization)
- [Pillow](https://pillow.readthedocs.io/en/stable/) (for image generation)

## Installation

To set up this project, follow these steps:

1. Clone the repository:
C:\mygit\BLazy\repo\glbj\LICENSE
Language detected: plaintext
MIT License

Copyright (c) [current_year] [Your Name or Your Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
C:\mygit\BLazy\repo\glbj\test_components.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\glbj\tests.py

import unittest
from config import Config
from game_engine import GameState, basic_strategy
from rl_agent import BetSizingAgent, BetSizingModel
from visualization import Visualization
from main import initialize_components, simulate_step, train_agent

class TestBlackjackSystem(unittest.TestCase):

    def test_configuration_loading(self):
        config = Config()
        self.assertEqual(config.initial_bankroll, 1000)
        self.assertEqual(config.min_bet, 5)
        self.assertEqual(config.max_bet, 100)
        self.assertEqual(config.num_decks, 6)
        self.assertEqual(config.learning_rate, 0.01)
        self.assertEqual(config.epsilon, 0.9)
        self.assertEqual(config.gamma, 0.95)
        print("Configuration loading test passed.")

    def test_game_engine_functionality(self):
        config = Config()
        game_state = GameState(config)
        initial_deck_cards = len(game_state.deck)
        game_state.new_round()
        self.assertTrue(len(game_state.player_hand.cards) == 2)
        self.assertTrue(len(game_state.dealer_hand.cards) == 2)
        self.assertGreater(len(game_state.deck), initial_deck_cards - 2)
        print("Game Engine functionality test passed.")

    def test_basic_strategy(self):
        state = {
            "player_hand": 15,
            "dealer_upcard": 7
        }
        config = Config()
        action = basic_strategy(state, config)
        self.assertEqual(action, 1)  # Should stand
        print("Basic strategy test passed.")

    def test_reinforcement_learning_agent(self):
        config = Config()
        agent = BetSizingAgent(config)
        state = (1000, 1.0, 20)
        action = agent.select_action(state, 0.0)
        self.assertIn(action.item(), range(config.min_bet, config.max_bet + 1))
        print("Reinforcement learning agent test passed.")

    def test_model_saving_loading(self):
        config = Config()
        agent = BetSizingAgent(config)
        model = BetSizingModel(agent)
        model.save_model('temp_model.pth')
        agent_to_compare = BetSizingAgent(config)
        model_load = BetSizingModel(agent_to_compare)
        model_load.load_model('temp_model.pth')
        for param1, param2 in zip(agent.policy_net.parameters(), agent_to_compare.policy_net.parameters()):
            self.assertTrue(torch.equal(param1.data, param2.data))
        print("Model saving and loading test passed.")

if __name__ == "__main__":
    unittest.main()
C:\mygit\BLazy\repo\glbj\.gitignore
Language detected: plaintext
# .gitignore file for Python projects

# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd
*.pyc
*.mo

# Virtual environment directories
venv/
env/
.venv/
env.bak/
pip-selfcheck.json

# Model checkpoints
*.pth
*.pt

# Generated resources
resources/

# IDE-specific files
.idea/
*.vscode/
*.sln
*.csproj
*.fsproj

# Log files
*.log

# Temporary files
*.tmp
*~
.DS_Store
