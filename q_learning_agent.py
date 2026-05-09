"""
Q-Learning Agent for Tic Tac Toe
Implements reinforcement learning for game strategy improvement
"""

import numpy as np
import pickle
import os
from typing import Dict, List, Tuple


class QLearningAgent:
    """Q-Learning Agent for Tic Tac Toe"""
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95, 
                 epsilon: float = 0.1, epsilon_decay: float = 0.995):
        """
        Initialize Q-Learning Agent
        
        Args:
            learning_rate: How much new info overrides old info (alpha)
            discount_factor: Importance of future rewards (gamma)
            epsilon: Exploration rate (0-1)
            epsilon_decay: Rate at which epsilon decreases
        """
        self.q_table: Dict[str, np.ndarray] = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.initial_epsilon = epsilon
        self.training_stats = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "episodes": []
        }
    
    def state_to_key(self, board: List[str]) -> str:
        """Convert board state to hashable key"""
        return "".join(board)
    
    def get_available_moves(self, board: List[str]) -> List[int]:
        """Get list of available moves"""
        return [i for i, cell in enumerate(board) if cell == " "]
    
    def initialize_q_values(self, state: str) -> None:
        """Initialize Q-values for new state"""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)
    
    def select_action(self, board: List[str], training: bool = True) -> int:
        """
        Select action using epsilon-greedy strategy
        
        Args:
            board: Current board state
            training: If True, use exploration; if False, pure exploitation
        
        Returns:
            Position to place the move
        """
        available_moves = self.get_available_moves(board)
        
        if not available_moves:
            return -1
        
        state = self.state_to_key(board)
        self.initialize_q_values(state)
        
        # Epsilon-greedy selection
        if training and np.random.random() < self.epsilon:
            # Exploration: random move
            return np.random.choice(available_moves)
        else:
            # Exploitation: best move
            q_values = self.q_table[state].copy()
            # Set unavailable moves to very low value
            for i in range(9):
                if i not in available_moves:
                    q_values[i] = -np.inf
            
            best_move = np.argmax(q_values)
            # If all values are -inf, return random move
            if np.isinf(q_values[best_move]):
                return np.random.choice(available_moves)
            return best_move
    
    def update_q_value(self, state: str, action: int, reward: float, 
                      next_state: str, game_over: bool = False) -> None:
        """
        Update Q-value using Q-Learning formula
        Q(s,a) = Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
            game_over: Whether game has ended
        """
        self.initialize_q_values(state)
        self.initialize_q_values(next_state)
        
        current_q = self.q_table[state][action]
        
        if game_over:
            max_next_q = 0
        else:
            max_next_q = np.max(self.q_table[next_state])
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def save_model(self, filepath: str) -> None:
        """Save trained model to file"""
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump({
                "q_table": self.q_table,
                "stats": self.training_stats,
                "epsilon": self.epsilon
            }, f)
    
    def load_model(self, filepath: str) -> bool:
        """Load trained model from file"""
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, "rb") as f:
                data = pickle.load(f)
                self.q_table = data.get("q_table", {})
                self.training_stats = data.get("stats", self.training_stats)
                self.epsilon = data.get("epsilon", self.initial_epsilon)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def decay_epsilon(self) -> None:
        """Decay exploration rate"""
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, 0.01)  # Minimum exploration rate
    
    def reset_epsilon(self) -> None:
        """Reset epsilon to initial value"""
        self.epsilon = self.initial_epsilon
    
    def get_model_stats(self) -> Dict:
        """Get training statistics"""
        return self.training_stats.copy()
