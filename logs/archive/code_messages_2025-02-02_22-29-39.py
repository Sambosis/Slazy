C:\mygit\BLazy\repo\glbj\config.py
Language detected: python
from dataclasses import dataclass
import os

# Game Constants
DECK_RULES = {
    "number_of_decks": 6,
    "reshuffle_after_hand": True,
}

BETTING_LIMITS = {
    "min_bet": 5,
    "max_bet": 1000,
}

PAYOUTS = {
    "natural_blackjack": 1.5,
    "blackjack": 1.2,
}

# Training Parameters
LEARNING_RATE = 0.01
EPSILON = 0.1
GAMMA = 0.99

# Visualization Parameters
COLORS = {
    "background": "#000000",
    "text": "#FFFFFF",
    "card": "#FFFFFF",
    "button": "#808080",
}

SCREEN_DIMENSIONS = {
    "width": 800,
    "height": 600,
}

@dataclass
class Configuration:
    number_of_decks: int = DECK_RULES["number_of_decks"]
    reshuffle_after_hand: bool = DECK_RULES["reshuffle_after_hand"]
    
    min_bet: int = BETTING_LIMITS["min_bet"]
    max_bet: int = BETTING_LIMITS["max_bet"]
    
    natural_blackjack_payout: float = PAYOUTS["natural_blackjack"]
    blackjack_payout: float = PAYOUTS["blackjack"]
    
    learning_rate: float = LEARNING_RATE
    epsilon: float = EPSILON
    gamma: float = GAMMA
    
    background_color: str = COLORS["background"]
    text_color: str = COLORS["text"]
    card_color: str = COLORS["card"]
    button_color: str = COLORS["button"]
    
    screen_width: int = SCREEN_DIMENSIONS["width"]
    screen_height: int = SCREEN_DIMENSIONS["height"]

    @classmethod
    def from_env(cls):
        return cls(
            number_of_decks=int(os.getenv("NUMBER_OF_DECKS", cls.number_of_decks)),
            reshuffle_after_hand=bool(os.getenv("RESHUFFLE_AFTER_HAND", cls.reshuffle_after_hand)),
            min_bet=int(os.getenv("MIN_BET", cls.min_bet)),
            max_bet=int(os.getenv("MAX_BET", cls.max_bet)),
            natural_blackjack_payout=float(os.getenv("NATURAL_BLACKJACK_PAYOUT", cls.natural_blackjack_payout)),
            blackjack_payout=float(os.getenv("BLACKJACK_PAYOUT", cls.blackjack_payout)),
            learning_rate=float(os.getenv("LEARNING_RATE", cls.learning_rate)),
            epsilon=float(os.getenv("EPSILON", cls.epsilon)),
            gamma=float(os.getenv("GAMMA", cls.gamma)),
            background_color=os.getenv("BACKGROUND_COLOR", cls.background_color),
            text_color=os.getenv("TEXT_COLOR", cls.text_color),
            card_color=os.getenv("CARD_COLOR", cls.card_color),
            button_color=os.getenv("BUTTON_COLOR", cls.button_color),
            screen_width=int(os.getenv("SCREEN_WIDTH", cls.screen_width)),
            screen_height=int(os.getenv("SCREEN_HEIGHT", cls.screen_height)),
        )

# Example Usage
config = Configuration.from_env()
print(config)
C:\mygit\BLazy\repo\glbj\deck.py
Language detected: python
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random
from config import Configuration

# Define the suit and rank constants
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

@dataclass
class Card:
    suit: str
    rank: str
    value: int

    def __post_init__(self):
        if self.rank == 'Ace':
            self.value = 11  # Default value for Ace is 11
        else:
            self.value = VALUES[self.rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

@dataclass
class Deck:
    number_of_decks: int
    reshuffle_after_hand: bool
    cards: List[Card] = None

    def __post_init__(self):
        self.cards = self.build_deck()
        self.count = 0
        self.shuffle()

    def build_deck(self) -> List[Card]:
        """Build a full deck of cards based on the number_of_decks."""
        full_deck = []
        for _ in range(self.number_of_decks):
            for suit in SUITS:
                for rank in RANKS:
                    full_deck.append(Card(suit, rank, 0))
        return full_deck

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        self.count = self.calculate_true_count()

    def calculate_true_count(self) -> float:
        """Calculate the true count for counting cards."""
        deck_count = len(self.cards)
        true_count = self.count / (deck_count / 52)
        return true_count

    def draw_card(self) -> Card:
        """Draw a card from the deck."""
        return self.cards.pop()

def calculate_hand_value(hand: List[Card]) -> int:
    """Calculate the total value of a hand."""
    total_value = sum(card.value for card in hand)
    
    # Handle Aces
    num_aces = sum(1 for card in hand if card.rank == 'Ace')
    while total_value > 21 and num_aces:
        total_value -= 10
        num_aces -= 1
    
    return total_value

def has_blackjack(hand: List[Card]) -> bool:
    """Check if the hand has a blackjack."""
    return len(hand) == 2 and calculate_hand_value(hand) == 21

# Example Usage
config = Configuration.from_env()
deck = Deck(number_of_decks=config.number_of_decks, reshuffle_after_hand=config.reshuffle_after_hand)
print(deck)
C:\mygit\BLazy\repo\glbj\agent.py
Language detected: python
import numpy as np
import torch
import torch.nn as nn
import random
from typing import List, Tuple, Dict
import json
import os
from config import Configuration

@dataclass
class State:
    bankroll: float
    true_count: float
    betting_history: List[float]

class QLearningAgent:
    def __init__(self, config: Configuration):
        self.config = config
        self.state_space = self._state_space(config.screen_width, config.screen_height)
        self.action_space = self._action_space(config.min_bet, config.max_bet)
        self.q_table = self._initialize_q_table()
        self.epsilon = config.epsilon
        self.gamma = config.gamma
        self.learning_rate = config.learning_rate
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _state_space(self, screen_width: int, screen_height: int) -> List[Tuple[int, int]]:
        states = []
        for x in range(0, screen_width + 1, 10):
            for y in range(0, screen_height + 1, 10):
                states.append((x, y))
        return states

    def _action_space(self, min_bet: int, max_bet: int) -> List[int]:
        actions = []
        current_bet = min_bet
        while current_bet <= max_bet:
            actions.append(current_bet)
            current_bet *= 2
        return actions

    def _initialize_q_table(self) -> Dict[Tuple[int, int], Dict[int, float]]:
        q_table = {}
        for state in self.state_space:
            q_table[state] = {action: 0.0 for action in self.action_space}
        return q_table

    def choose_action(self, state: State) -> int:
        state_key = (int(state.bankroll), int(state.true_count))
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.action_space)
        else:
            q_values = self.q_table.get(state_key, {})
            return max(q_values.keys(), key=lambda x: q_values[x])

    def update_q_table(self, old_state: State, action: int, reward: float, new_state: State):
        old_state_key = (int(old_state.bankroll), int(old_state.true_count))
        new_state_key = (int(new_state.bankroll), int(new_state.true_count))

        old_q_value = self.q_table[old_state_key][action]
        next_max = max(self.q_table[new_state_key].values())

        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * (reward + self.gamma * next_max)
        self.q_table[old_state_key][action] = new_q_value

    def save_model(self, file_name: str):
        with open(file_name, 'w') as f:
            json.dump(self.q_table, f)

    def load_model(self, file_name: str):
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                self.q_table = json.load(f)

# Example Usage
config = Configuration.from_env()
agent = QLearningAgent(config)
state = State(bankroll=1000, true_count=-1, betting_history=[5, 10])
action = agent.choose_action(state)
agent.update_q_table(state, action, reward=100, new_state=state)
print(agent.q_table)
C:\mygit\BLazy\repo\glbj\visualization.py
Language detected: python
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from typing import List, Tuple, Dict
from config import Configuration
from deck import Card, calculate_hand_value
import io
from PIL import Image

# Initialize configuration
config = Configuration.from_env()

class GameVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def render_card(self, card: Card, position: Tuple[int, int]):
        # Dummy implementation for rendering a card at the given position
        pygame.draw.rect(self.screen, Config.COLORS['card'], (*position, 100, 150))
        text_surface = self.font.render(f"{card.rank} of {card.suit}", True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def render_chips(self, amount: float, position: Tuple[int, int]):
        # Dummy implementation for rendering chips (could be a simple rectangle with amount text)
        pygame.draw.rect(self.screen, (192, 192, 192), (*position, 50, 25))
        text_surface = self.font.render(f"${amount:.2f}", True, (0, 0, 0))
        self.screen.blit(text_surface, position)

    def render_stats(self, stats: Dict[str, any]):
        # Dummy implementation for rendering the given statistics as text
        for i, (key, value) in enumerate(stats.items()):
            stat_text = f"{key}: {value}"
            text_surface = self.font.render(stat_text, True, config.COLORS['text'])
            self.screen.blit(text_surface, (10, 10 + i * 30))

    def handle_animation(self):
        # Dummy implementation for handling animation (could involve moving cards across the screen)
        pass

class StatsDisplay:
    def __init__(self, bankroll_history, win_loss_ratio):
        self.bankroll_history = bankroll_history
        self.win_loss_ratio = win_loss_ratio
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasAgg(self.fig)
        
        # Plot bankroll history
        self.ax.plot(bankroll_history, label='Bankroll')
        self.ax.legend()
        self.canvas.draw()
        
        # Convert figure to image
        img = np.frombuffer(self.canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(self.canvas.figure.bbox.bounds[3], self.canvas.figure.bbox.bounds[2], 4)
        self.img = Image.fromarray(img)
    
    def update_plot(self, new_bankroll, win_loss_ratio):
        self.bankroll_history.append(new_bankroll)
        self.win_loss_ratio = win_loss_ratio
        
        self.ax.clear()
        self.ax.plot(self.bankroll_history, label='Bankroll')
        self.ax.legend()
        self.canvas.draw()
        
        # Convert figure to image
        img = np.frombuffer(self.canvas.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(self.canvas.figure.bbox.bounds[3], self.canvas.figure.bbox.bounds[2], 4)
        self.img = Image.fromarray(img)
    
    def get_surface(self):
        # Convert PIL image to Pygame surface
        mode = self.img.mode
        size = self.img.size
        data = self.img.tobytes()
        pygame_img = pygame.image.frombuffer(data, size, mode)
        return pygame_img

# Helper Functions

def mpl_figure_to_surface(fig):
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    img = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    img = img.reshape(canvas.figure.bbox.bounds[3], canvas.figure.bbox.bounds[2], 4)
    return pygame.image.frombuffer(img, (canvas.figure.bbox.bounds[2], canvas.figure.bbox.bounds[3]), 'RGBA')

color_convert = {
    'RGB': '(255, 255, 255)',
    'RGBA': '(255, 255, 255, 255)',
}

def convert_color(color_str: str) -> Tuple[int]:
    # Example conversion for RGB or RGBA strings
    return eval(color_convert[color_str[:3]])

def screen_update(screen: pygame.Surface, surf: pygame.Surface, pos: Tuple[int]):
    screen.blit(surf, pos)
    pygame.display.flip()

# Example Usage
pygame.init()
screen = pygame.display.set_mode((config.screen_width, config.screen_height))
visualizer = GameVisualizer(screen)

bankroll_history = [1000]
win_loss_ratio = [0.5]

stats_display = StatsDisplay(bankroll_history, win_loss_ratio)
pygame.display.flip()

# Simulate game actions for demonstration
bankroll_history.append(1050)
win_loss_ratio[0] = 0.7
stats_display.update_plot(bankroll_history[-1], win_loss_ratio[0])
pygame_screen = screen_update(screen, stats_display.get_surface(), (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    visualizer.handle_animation()
    pygame.display.flip()
pygame.quit()
C:\mygit\BLazy\repo\glbj\game.py
Language detected: python
import pygame
from typing import List, Tuple, Dict
from config import Configuration
from deck import Card, Deck, calculate_hand_value, has_blackjack
from agent import QLearningAgent, State
from visualization import GameVisualizer, StatsDisplay
import numpy as np
import json
import os

class BlackjackGame:
    def __init__(self, config: Configuration, training_mode=True):
        self.config = config
        self.training_mode = training_mode
        self.deck = Deck(number_of_decks=config.number_of_decks, reshuffle_after_hand=config.reshuffle_after_hand)
        self.player_hand = []
        self.dealer_hand = []
        self.player_bankroll = self.config.min_bet
        self.running_statistics = {'games_played': 0, 'player_wins': 0, 'ties': 0, 'dealer_wins': 0}
        self.agent = QLearningAgent(config)
        self.game_visualizer = GameVisualizer(pygame.display.get_surface())
        self.stats_display = StatsDisplay([self.player_bankroll], self.agent.epsilon)
        self.training_episodes = 0

        if self.training_mode:
            self.load_model()
        else:
            self.load_stats()

    def reset_board(self):
        self.dealer_hand = []
        self.player_hand = []
        self.deck = Deck(number_of_decks=self.config.number_of_decks, reshuffle_after_hand=self.config.reshuffle_after_hand)
        self.update_statistics(self.running_statistics)

    def deal_cards(self):
        self.dealer_hand.append(self.deck.draw_card())
        self.dealer_hand.append(self.deck.draw_card())
        self.player_hand.append(self.deck.draw_card())
        self.player_hand.append(self.deck.draw_card())

    def process_player_decision(self, decision: str, state: State):
        if decision == "hit":
            self.player_hand.append(self.deck.draw_card())
            if calculate_hand_value(self.player_hand) > 21:
                self.end_game("dealer")
        elif decision == "stand":
            self.process_dealer_actions(state)

    def process_dealer_actions(self, state: State):
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw_card())
        self.compare_hands(state)

    def compare_hands(self, state: State):
        player_score = calculate_hand_value(self.player_hand)
        dealer_score = calculate_hand_value(self.dealer_hand)

        if player_score > dealer_score or dealer_score > 21:
            reward = self.config.max_bet
            self.running_statistics['player_wins'] += 1
        elif player_score == dealer_score:
            reward = 0
            self.running_statistics['ties'] += 1
        else:
            reward = -self.config.max_bet
            self.running_statistics['dealer_wins'] += 1

        self.agent.update_q_table(state, decision_index, reward, state)
        self.end_game(reward=reward)

    def end_game(self, result=""):
        self.running_statistics['games_played'] += 1

        if result == "dealer":
            self.player_bankroll -= self.config.max_bet
        elif result.startswith("-"):
            self.player_bankroll += float(result.split(":")[1])

        self.reset_board()
        self.save_model()
        self.save_stats()

    def train_agent(self, episodes):
        self.training_episodes = episodes
        for _ in range(episodes):
            state = State(bankroll=self.player_bankroll, true_count=self.deck.calculate_true_count(), betting_history=[])
            action = self.agent.choose_action(state)
            outcome = self.simulate_game(action, state)
            self.agent.update_q_table(state, action, outcome, State(bankroll=self.player_bankroll, true_count=self.deck.calculate_true_count(), betting_history=[]))
    
    def simulate_game(self, action, state):
        # This function should simulate a game with the given action, and return the outcome
        pass

    def load_stats(self):
        if os.path.exists("stats.json"):
            with open("stats.json", 'r') as f:
                self.running_statistics = json.load(f)

    def save_stats(self):
        with open("stats.json", 'w') as f:
            json.dump(self.running_statistics, f)

    def load_model(self):
        self.agent.load_model('q_table.json')

    def save_model(self):
        self.agent.save_model('q_table.json')

def main(training_mode=True):
    pygame.init()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Blackjack Game")

    game_config = Configuration.from_env()
    blackjack_game = BlackjackGame(game_config, training_mode)

    running = True
    episode = 0
    step = 0

    while running:
        screen.fill(convert_color(game_config.colors['background']))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if training_mode and episode < blackjack_game.training_episodes:
            if step % 10 == 0:
                blackjack_game.train_agent(10)

        state = State(bankroll=blackjack_game.player_bankroll, true_count=blackjack_game.deck.calculate_true_count(), betting_history=[])
        action = blackjack_game.agent.choose_action(state)

        if not action and step % 50 != 0:
            continue

        if not training_mode:
            print(f"Player's Bankroll: ${blackjack_game.player_bankroll}")
            print(f"True Count: {blackjack_game.deck.calculate_true_count()}")

        # Deal initial cards
        blackjack_game.deal_cards()

        # Process player and dealer actions
        blackjack_game.process_player_decision(action, state)
        blackjack_game.process_dealer_actions(state)

        # Render game elements
        for card in blackjack_game.dealer_hand:
            blackjack_game.game_visualizer.render_card(card, (random.randint(config.screen_width//4, 3*config.screen_width // 4), config.screen_height // 2))
        for card in blackjack_game.player_hand:
            blackjack_game.game_visualizer.render_card(card, (random.randint(config.screen_width//4, 3*config.screen_width // 4), config.screen_height // 4))

        # Update stats display
        blackjack_game.stats_display.update_plot(blackjack_game.player_bankroll, blackjack_game.agent.epsilon)
        screen.blit(blackjack_game.stats_display.get_surface(), (0, config.screen_height//2))

        pygame.display.flip()
        clock.tick(30)

        if step % 1000 == 0 and step != 0:
            episode += 1
        step += 1

    pygame.quit()

if __name__ == "__main__":
    main(training_mode=False)
