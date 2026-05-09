"""
Tic Tac Toe Game Engine
Handles game logic, board management, and winner detection
"""

from typing import List, Tuple, Optional
from q_learning_agent import QLearningAgent


class TicTacToeGame:
    """Tic Tac Toe Game Engine"""
    
    WIN_CONDITIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    
    def __init__(self, ai_agent: Optional[QLearningAgent] = None):
        """
        Initialize game
        
        Args:
            ai_agent: QLearningAgent for AI player (optional)
        """
        self.board: List[str] = [" "] * 9
        self.ai_agent = ai_agent
        self.move_history: List[Tuple[int, str]] = []
        self.game_over = False
        self.winner = None  # "X", "O", "Draw", or None
    
    def reset(self) -> None:
        """Reset board and game state"""
        self.board = [" "] * 9
        self.move_history = []
        self.game_over = False
        self.winner = None
    
    def is_valid_move(self, position: int) -> bool:
        """Check if move is valid"""
        return 0 <= position < 9 and self.board[position] == " "
    
    def make_move(self, position: int, player: str) -> bool:
        """
        Make a move on the board
        
        Args:
            position: Position to place (0-8)
            player: "X" or "O"
        
        Returns:
            True if move was successful, False otherwise
        """
        if not self.is_valid_move(position):
            return False
        
        self.board[position] = player
        self.move_history.append((position, player))
        return True
    
    def check_winner(self, player: Optional[str] = None) -> bool:
        """
        Check if a player has won
        
        Args:
            player: "X" or "O", or None to check all players
        
        Returns:
            True if player(s) has won
        """
        players = [player] if player else ["X", "O"]
        
        for p in players:
            for condition in self.WIN_CONDITIONS:
                if all(self.board[i] == p for i in condition):
                    return True
        
        return False
    
    def is_board_full(self) -> bool:
        """Check if board is full"""
        return " " not in self.board
    
    def get_available_moves(self) -> List[int]:
        """Get list of available positions"""
        return [i for i, cell in enumerate(self.board) if cell == " "]
    
    def get_board_copy(self) -> List[str]:
        """Get a copy of the current board"""
        return self.board.copy()
    
    def evaluate_game_state(self) -> Tuple[bool, Optional[str]]:
        """
        Evaluate current game state
        
        Returns:
            Tuple of (game_over, winner)
            winner: "X", "O", "Draw", or None
        """
        # Check for winner
        if self.check_winner("X"):
            return True, "X"
        elif self.check_winner("O"):
            return True, "O"
        elif self.is_board_full():
            return True, "Draw"
        
        return False, None
    
    def ai_move(self, training: bool = True) -> int:
        """
        Make AI move
        
        Args:
            training: If True, use training mode for Q-Learning
        
        Returns:
            Position where AI moved
        """
        if not self.ai_agent:
            raise ValueError("No AI agent available")
        
        position = self.ai_agent.select_action(self.board, training=training)
        
        if position != -1 and self.make_move(position, "O"):
            return position
        
        return -1
    
    def player_move(self, position: int) -> bool:
        """Make human player move"""
        return self.make_move(position, "X")
    
    def print_board(self) -> str:
        """Return string representation of board"""
        board_str = "   0   1   2\n"
        for i in range(3):
            row = i * 3
            board_str += f"{i}  {self.board[row]} | {self.board[row+1]} | {self.board[row+2]}\n"
            if i < 2:
                board_str += "  -----------\n"
        return board_str
    
    def get_board_state(self) -> str:
        """Get hashable board state"""
        return "".join(self.board)


class GameTrainer:
    """Trainer for AI agent using self-play"""
    
    def __init__(self, ai_agent: QLearningAgent):
        """
        Initialize trainer
        
        Args:
            ai_agent: QLearningAgent to train
        """
        self.ai_agent = ai_agent
    
    def train(self, episodes: int, log_interval: int = 100) -> List[dict]:
        """
        Train AI agent through self-play
        
        Args:
            episodes: Number of training episodes
            log_interval: Log stats every N episodes
        
        Returns:
            List of training logs
        """
        logs = []
        
        for episode in range(episodes):
            game = TicTacToeGame(self.ai_agent)
            game_over = False
            
            while not game_over:
                # AI as first player (X)
                ai_move_pos = self.ai_agent.select_action(game.board, training=True)
                if ai_move_pos == -1:
                    game_over = True
                    break
                
                state = game.get_board_state()
                game.make_move(ai_move_pos, "X")
                next_state = game.get_board_state()
                
                game_over, winner = game.evaluate_game_state()
                
                if winner == "X":
                    self.ai_agent.update_q_value(state, ai_move_pos, 1.0, next_state, True)
                elif winner == "Draw":
                    self.ai_agent.update_q_value(state, ai_move_pos, 0.5, next_state, True)
                else:
                    self.ai_agent.update_q_value(state, ai_move_pos, 0, next_state, False)
                
                if game_over:
                    break
                
                # AI as second player (O)
                ai_move_pos = self.ai_agent.select_action(game.board, training=True)
                if ai_move_pos == -1:
                    game_over = True
                    break
                
                state = game.get_board_state()
                game.make_move(ai_move_pos, "O")
                next_state = game.get_board_state()
                
                game_over, winner = game.evaluate_game_state()
                
                if winner == "O":
                    self.ai_agent.update_q_value(state, ai_move_pos, 1.0, next_state, True)
                elif winner == "Draw":
                    self.ai_agent.update_q_value(state, ai_move_pos, 0.5, next_state, True)
                else:
                    self.ai_agent.update_q_value(state, ai_move_pos, 0, next_state, False)
            
            self.ai_agent.decay_epsilon()
            
            # Logging
            if (episode + 1) % log_interval == 0:
                logs.append({
                    "episode": episode + 1,
                    "q_table_size": len(self.ai_agent.q_table),
                    "epsilon": self.ai_agent.epsilon
                })
        
        return logs
    
    def evaluate_vs_random(self, episodes: int = 100) -> dict:
        """
        Evaluate AI against random player
        
        Args:
            episodes: Number of evaluation games
        
        Returns:
            Statistics dictionary
        """
        stats = {"wins": 0, "losses": 0, "draws": 0}
        
        for _ in range(episodes):
            game = TicTacToeGame(self.ai_agent)
            
            while True:
                # AI move
                ai_pos = self.ai_agent.select_action(game.board, training=False)
                if ai_pos != -1:
                    game.make_move(ai_pos, "X")
                
                game_over, winner = game.evaluate_game_state()
                if game_over:
                    if winner == "X":
                        stats["wins"] += 1
                    elif winner == "Draw":
                        stats["draws"] += 1
                    else:
                        stats["losses"] += 1
                    break
                
                # Random move
                available = game.get_available_moves()
                if available:
                    import random
                    random_pos = random.choice(available)
                    game.make_move(random_pos, "O")
                
                game_over, winner = game.evaluate_game_state()
                if game_over:
                    if winner == "O":
                        stats["losses"] += 1
                    elif winner == "Draw":
                        stats["draws"] += 1
                    else:
                        stats["wins"] += 1
                    break
        
        return stats
