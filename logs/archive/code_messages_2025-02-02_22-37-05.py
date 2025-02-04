C:\mygit\BLazy\repo\glbj\config.py
Language detected: python
from dataclasses import dataclass, field
from typing import Tuple, Dict, List

@dataclass
class GameConstants:
    # Screen dimensions and colors
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    BACKGROUND_COLOR: Tuple[int, int, int] = (0, 153, 51)  # Dark Green
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White

    # Card dimensions and positions
    CARD_WIDTH: int = 100
    CARD_HEIGHT: int = 150
    CARD_BACK_IMAGE: str = "images/card_back.png"
    CARD_POSITIONS: Dict[str, Tuple[int, int]] = field(default_factory=lambda: {
        'dealer_first_card_x': 100,
        'dealer_second_card_x': 200,
        'dealer_third_card_x': 300,
        'dealer_fourth_card_x': 400,
        'dealer_fifth_card_x': 500,
        'player_first_card_x': 100,
        'player_second_card_x': 200,
        'player_third_card_x': 300,
        'player_fourth_card_x': 400,
        'player_fifth_card_x': 500,
        'dealer_y': 100,
        'player_y': 400
    })

    # Game rules parameters
    DECK_COUNT: int = 6
    MIN_BET: int = 5
    MAX_BET: int = 1000
    BANKROLL: int = 5000
    CARD_VALUES: Dict[str, int] = field(default_factory=lambda: {
        'Ace': 11,  # Can also count as 1
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
        'Six': 6,
        'Seven': 7,
        'Eight': 8,
        'Nine': 9,
        'Ten': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10
    })
    
    # RL training parameters
    LEARNING_RATE: float = 0.001
    EPSILON: float = 1.0
    EPSILON_DECAY: float = 0.999
    MIN_EPSILON: float = 0.1
    GAMMA: float = 0.99
    MEMORY_SIZE: int = 1000000
    BATCH_SIZE: int = 64
    TARGET_UPDATE_FREQUENCY: int = 1000

# Example usage
if __name__ == "__main__":
    constants = GameConstants()
    print(constants)
C:\mygit\BLazy\repo\glbj\deck.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\glbj\card_deck.py
from dataclasses import dataclass, field
from random import shuffle
from typing import List, Iterator, Tuple

@dataclass
class Card:
    """
    Represents an individual playing card.
    
    Attributes:
        suit (str): The suit of the card.
        value (str): The face value of the card.
    """
    suit: str
    value: str
    
    def get_value_int(self) -> int:
        """Converts the card value string to its integer equivalent."""
        return {
            'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 
            'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 
            'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
        }.get(self.value, 0)

    def get_hi_lo_value(self) -> int:
        """Returns the Hi-Lo count value for the card."""
        if self.value in ['Ten', 'Jack', 'Queen', 'King', 'Ace']:
            return -1
        elif self.value in ['Two', 'Three', 'Four', 'Five', 'Six']:
            return 1
        return 0

@dataclass
class Deck:
    """
    Represents a collection of cards.
    
    Attributes:
        num_decks (int): Number of decks used in the game.
    """
    num_decks: int = 6
    cards: List[Card] = field(init=False)
    
    def __post_init__(self):
        """Initialize the deck with multiple decks of cards and shuffle them."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
                  'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, value) for _ in range(self.num_decks) for suit in suits for value in values]
        shuffle(self.cards)
    
    def deal_one(self) -> Card:
        """Deal one card from the deck."""
        return self.cards.pop(0)
    
    def __iter__(self) -> Iterator[Card]:
        """Iterator for the deck."""
        return iter(self.cards)
    
    def count_running(self, card: Card) -> int:
        """Calculate the running count based on a given card using the Hi-Lo strategy."""
        return self.count_running_helper() + card.get_hi_lo_value()
        
    def count_running_helper(self) -> int:
        """Helper method for running count."""
        return sum(card.get_hi_lo_value() for card in self.cards)
    
    def get_true_count(self, remaining_cards: int) -> float:
        """Calculate the true count based on the current running count and the number of remaining cards."""
        deck_penetration = remaining_cards / (52 * self.num_decks)
        return self.count_running_helper() / ((52 * self.num_decks - remaining_cards) / 52)
    
# Example Usage
if __name__ == "__main__":
    deck = Deck()
    print(f"Remaining Cards: {len(deck.cards)}")
    card = deck.deal_one()
    print(f"Dealt Card: {card}")
    running_count = deck.count_running(card)
    print(f"Running Count: {running_count}")
    true_count = deck.get_true_count(len(deck.cards))
    print(f"True Count: {true_count}")
C:\mygit\BLazy\repo\glbj\agent.py
Language detected: python
# Import necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque, namedtuple
import random

# Define device for tensor computations (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define named tuple for storing state transitions
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

# Define the neural network for Q-value approximation
class QNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Define the RL agent class
class QLearningAgent:
    def __init__(self, input_size, output_size, memory_size=1000000, batch_size=64, gamma=0.99, lr=0.001, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.999):
        self.output_size = output_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.memory = deque(maxlen=memory_size)
        self.policy_net = QNetwork(input_size, output_size).to(device)
        self.target_net = QNetwork(input_size, output_size).to(device)
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def select_action(self, state, steps_done):
        sample = random.random()
        eps_threshold = self.epsilon * (self.epsilon_decay ** steps_done)
        if sample > eps_threshold:
            with torch.no_grad():
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.output_size)]], dtype=torch.long)

    def remember(self, state, action, next_state, reward):
        self.memory.append(Transition(state, action, next_state, reward))

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        batch = Transition(*zip(*minibatch))

        # Compute a mask of non-final states and concatenate the batch elements
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Estimate Q-values using the policy network and compute expected Q-values
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)
        next_state_values = torch.zeros(self.batch_size, device=device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save_model(self, filename):
        torch.save(self.policy_net.state_dict(), filename)

    def load_model(self, filename):
        self.policy_net.load_state_dict(torch.load(filename))
        self.policy_net.eval()

# Example of how to use the agent
if __name__ == '__main__':
    agent = QLearningAgent(input_size=128, output_size=64)
    state = torch.tensor([np.random.rand(1, 128)], dtype=torch.float, device=device)
    action = agent.select_action(state, steps_done=0)
    print(action)
C:\mygit\BLazy\repo\glbj\game_engine.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\glbj\blackjack_game.py

import random
from typing import List, Tuple, Optional

from .config import GameConstants
from .deck import Deck
from .card_deck import Card

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
        self.bet_amount: int = 0
        self.status: str = "active"
    
    def add_card(self, card: Card) -> None:
        self.cards.append(card)
    
    def clear_hand(self) -> None:
        self.cards = []

    def get_value(self) -> int:
        value = 0
        ace_count = 0
        for card in self.cards:
            value += card.get_value_int()
            if card.value == 'Ace':
                ace_count += 1
        
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        
        return value

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21

    def is_soft(self) -> bool:
        return 'Ace' in [card.value for card in self.cards]

class BlackjackGame:
    def __init__(self):
        self.constants = GameConstants()
        self.deck = Deck(self.constants.DECK_COUNT)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.payout_ratio = 3/2
        self.bankroll = self.constants.BANKROLL
        self.round_number = 0
        self.previous_bet = None
        self.game_stats = {'rounds_played': 0, 'wins': 0, 'losses': 0, 'ties': 0}
    
    def initialize_hands(self):
        self.player_hand.clear_hand()
        self.dealer_hand.clear_hand()
        self.player_hand.add_card(self.deck.deal_one())
        self.player_hand.add_card(self.deck.deal_one())
        self.dealer_hand.add_card(self.deck.deal_one())
        self.dealer_hand.add_card(self.deck.deal_one())

    def bet(self, amount):
        if amount > self.bankroll:
            raise ValueError("Insufficient funds")
        self.player_hand.bet_amount = amount
        self.bankroll -= amount

    def play_player_turn(self):
        while True:
            player_input = input("Press H to hit, S to stand, D to double down: ").upper()
            if player_input == 'H':
                self.player_hand.add_card(self.deck.deal_one())
                if self.player_hand.get_value() > 21:
                    return "bust"
            elif player_input == 'S':
                return "stand"
            elif player_input == 'D':
                if len(self.player_hand.cards) != 2:
                    print("Can only double down on first two cards.")
                    continue
                self.bet(self.player_hand.bet_amount)
                self.player_hand.add_card(self.deck.deal_one())
                return "stand"

    def dealer_play(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal_one())
        
        if self.dealer_hand.get_value() > 21:
            return "bust"
        return "stand"

    def evaluate_game(self):
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if player_value == dealer_value:
            self.player_hand.status = "push"
            self.bankroll += self.player_hand.bet_amount
            self.game_stats['ties'] += 1
        elif player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
            self.player_hand.status = "lose"
            self.game_stats['losses'] += 1
        else:
            self.player_hand.status = "win"
            self.game_stats['wins'] += 1
            self.bankroll += self.player_hand.bet_amount * 2

    def play_round(self):
        self.initialize_hands()
        self.round_number += 1
        self.bet(self.previous_bet if self.previous_bet else self.constants.MIN_BET)
        result = self.play_player_turn()
        
        if result == "bust":
            self.player_hand.status = "lose"
            self.game_stats['losses'] += 1
            return

        self.status = self.dealer_play()

        if self.status == "bust":
            self.player_hand.status = "win"
            self.bankroll += self.player_hand.bet_amount * 2
            self.game_stats['wins'] += 1
        else:
            self.evaluate_game()
        self.game_stats['rounds_played'] += 1
    
    def save_game_state(self, filename):
        game_state = {
            'deck': list(self.deck.cards),
            'player_hand': self.player_hand.__dict__,
            'dealer_hand': self.dealer_hand.__dict__,
            'bankroll': self.bankroll,
            'game_stats': self.game_stats,
            'round_number': self.round_number
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self, filename):
        with open(filename, 'r') as f:
            game_state = json.load(f)
        self.deck.cards = [Card(**c) for c in game_state['deck']]
        self.player_hand.__dict__.update(game_state['player_hand'])
        self.dealer_hand.__dict__.update(game_state['dealer_hand'])
        self.bankroll = game_state['bankroll']
        self.game_stats.update(game_state['game_stats'])
        self.round_number = game_state['round_number']
C:\mygit\BLazy\repo\glbj\visualizer.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\glbj\visualizer.py
import pygame
import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict
from .config import GameConstants
from .blackjack_game import BlackjackGame, Hand

# Initialize Pygame
pygame.init()

# Constants for display
SCREEN_WIDTH = GameConstants.SCREEN_WIDTH
SCREEN_HEIGHT = GameConstants.SCREEN_HEIGHT
BACKGROUND_COLOR = GameConstants.BACKGROUND_COLOR
TEXT_COLOR = GameConstants.TEXT_COLOR
CARD_WIDTH = GameConstants.CARD_WIDTH
CARD_HEIGHT = GameConstants.CARD_HEIGHT

@dataclass
class GameVisualizer:
    screen: pygame.Surface
    constants: GameConstants
    game: BlackjackGame
    
    def __post_init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.reset()
    
    def reset(self):
        self.screen.fill(self.constants.BACKGROUND_COLOR)
        self.draw_table()
    
    def draw_table(self):
        pygame.draw.rect(self.screen, (0, 51, 0), (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
        self.draw_cards()
    
    def draw_cards(self):
        player = self.game.player_hand.cards
        dealer = self.game.dealer_hand.cards

        for i, card in enumerate(player):
            img = pygame.image.load(self.constants.CARD_BACK_IMAGE if i == 0 and self.game.dealer_hand.is_blackjack() else "images/card_" + card.suit.lower() + "_" + card.value.lower() + ".png")
            self.screen.blit(img, (self.constants.CARD_POSITIONS[f'player_first_card_x'] + (i * CARD_WIDTH), self.constants.CARD_POSITIONS['player_y']))

        for i, card in enumerate(dealer):
            img = pygame.image.load(self.constants.CARD_BACK_IMAGE if i == 0 and not self.game.player_hand.is_blackjack() else "images/card_" + card.suit.lower() + "_" + card.value.lower() + ".png")
            self.screen.blit(img, (self.constants.CARD_POSITIONS[f'dealer_first_card_x'] + (i * CARD_WIDTH), self.constants.CARD_POSITIONS['dealer_y']))
    
    def draw_text(self, text: str, position: Tuple[int, int]):
        rendered_text = self.font.render(text, True, self.constants.TEXT_COLOR)
        self.screen.blit(rendered_text, position)
    
    def show_statistics(self):
        stats = [
            f"Bankroll: ${self.game.bankroll}",
            f"Wins: {self.game.game_stats['wins']}",
            f"Losses: {self.game.game_stats['losses']}",
            f"Ties: {self.game.game_stats['ties']}",
            f"Running Count: {self.game.deck.count_running_helper()}",
            f"True Count: {self.game.deck.get_true_count(len(self.game.deck.cards))}",
            f"Avg Bet Size: ${sum([h.bet_amount for h in [self.game.player_hand]]) / max(len(self.game.player_hand.cards), 1)}",
            f"Max Drawdown: TBD"
        ]
        y_offset = 20
        for i, stat in enumerate(stats):
            self.draw_text(stat, (50, y_offset + i*50))
    
    def draw_training_progress(self):
        # For simplicity, we'll just draw a placeholder for the learning curve
        learning_curve = [0.5] * 50  # Mocked learning curve
        for i, value in enumerate(learning_curve):
            color = (255, 0, 0) if value == 0 else (0, 255, 0)
            pygame.draw.line(self.screen, color, (100 + i * 20, 400), (100 + i * 20, 400 - value * 200))
        
        self.draw_text(f"Epsilon: {self.game.agent.epsilon}", (50, 550))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_screen(self):
        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_constants = GameConstants()
    game = BlackjackGame()
    visualizer = GameVisualizer(screen, game_constants, game)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        visualizer.reset()
        visualizer.draw_cards()
        visualizer.show_statistics()
        visualizer.draw_training_progress()
        visualizer.handle_events()
        visualizer.update_screen()
        clock.tick(60)

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\glbj\main.py
Language detected: python
# filepath: C:\mygit\BLazy\repo\glbj\main.py

import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict

from .config import GameConstants
from .deck import Deck
from .card_deck import Card, Deck as CardDeck
from .game_engine import BlackjackGame
from .agent import QLearningAgent
from .visualizer import GameVisualizer, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class Trainer:
    game_constants: GameConstants
    blackjack_game: BlackjackGame
    visualizer: GameVisualizer
    training_agent: QLearningAgent
    training_mode: bool = True

    def init_components(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visualizer = GameVisualizer(self.screen, self.game_constants, self.blackjack_game)
        self.training_agent = QLearningAgent(
            input_size=128, output_size=64,
            memory_size=self.game_constants.MEMORY_SIZE,
            batch_size=self.game_constants.BATCH_SIZE,
            gamma=self.game_constants.GAMMA,
            lr=self.game_constants.LEARNING_RATE,
            epsilon=self.game_constants.EPSILON,
            epsilon_min=self.game_constants.MIN_EPSILON,
            epsilon_decay=self.game_constants.EPSILON_DECAY
        )

    def run_game_loop(self):
        running = True
        while running:
            self.visualizer.reset()
            
            if self.training_mode:
                for _ in range(self.game_constants.TARGET_UPDATE_FREQUENCY):
                    self.blackjack_game.play_round()
                    self.training_agent.remember(
                        self.preprocess_state(self.blackjack_game.player_hand.cards), 
                        torch.tensor([[self.blackjack_game.player_hand.status == 'win']], dtype=torch.float32),
                        self.preprocess_state(self.blackjack_game.dealer_hand.cards), 
                        torch.tensor([[self.blackjack_game.player_hand.bet_amount]])
                    )
                    if len(self.training_agent.memory) > self.game_constants.BATCH_SIZE:
                        self.training_agent.train()

                self.training_agent.update_target_network()
            else:
                self.blackjack_game.play_round()
            
            self.visualizer.draw_cards()
            self.visualizer.show_statistics()
            self.visualizer.handle_events()
            self.visualizer.update_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.training_mode = not self.training_mode

    def preprocess_state(self, cards_list):
        return torch.tensor([card.get_value_int() for card in cards_list], dtype=torch.float32).unsqueeze(0)

def main():
    game_constants = GameConstants()
    blackjack_game = BlackjackGame()
    trainer = Trainer(game_constants, blackjack_game, None, None)
    trainer.init_components()
    trainer.run_game_loop()

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\glbj\requirements.txt
Language detected: txt
pygame==2.1.0
torch==1.10.0
numpy==1.21.2
matplotlib==3.4.3
