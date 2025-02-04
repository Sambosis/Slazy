C:\mygit\BLazy\repo\glbj\config.py
Language detected: python
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class Config:
    """
    Configuration class for the Blackjack game and reinforcement learning parameters.
    
    Attributes:
        game_settings: A dictionary containing game settings such as initial bankroll, betting limits, number of decks, etc.
        display_settings: A dictionary containing display settings like screen dimensions, colors, FPS, etc.
        training_parameters: A dictionary containing training parameters such as learning rate, epsilon, gamma, etc.
        model_paths: A dictionary containing paths for saving/loading models.
    """
    
    game_settings: Dict[str, Any] = field(default_factory=lambda: {
        'initial_bankroll': 1000,
        'min_bet': 5,
        'max_bet': 100,
        'num_decks': 6
    })
    display_settings: Dict[str, Any] = field(default_factory=lambda: {
        'screen_width': 800,
        'screen_height': 600,
        'background_color': (0, 0, 0),
        'fps': 30
    })
    training_parameters: Dict[str, Any] = field(default_factory=lambda: {
        'learning_rate': 0.01,
        'epsilon': 1.0,
        'gamma': 0.99
    })
    model_paths: Dict[str, str] = field(default_factory=lambda: {
        'save_model_path': 'models/blackjack_model.pth',
        'load_model_path': 'models/blackjack_model.pth'
    })

# Example access:
# config = Config()
# print(config.game_settings['initial_bankroll'])
# print(config.display_settings['screen_width'])
# print(config.training_parameters['learning_rate'])
# print(config.model_paths['save_model_path'])
