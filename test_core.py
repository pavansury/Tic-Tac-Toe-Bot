#!/usr/bin/env python3
"""
Quick test script to verify core functionality
"""

from q_learning_agent import QLearningAgent
from game_engine import TicTacToeGame, GameTrainer

print("=" * 50)
print("RL Tic Tac Toe Bot - Test Suite")
print("=" * 50)

# Test 1: Agent Creation
print("\n[TEST 1] Creating Q-Learning Agent...")
agent = QLearningAgent(learning_rate=0.1, discount_factor=0.95, epsilon=0.2)
print(f"✓ Agent created successfully")
print(f"  - Q-Table Size: {len(agent.q_table)}")
print(f"  - Learning Rate: {agent.learning_rate}")
print(f"  - Epsilon: {agent.epsilon}")

# Test 2: Game Creation
print("\n[TEST 2] Creating Game Engine...")
game = TicTacToeGame(agent)
print(f"✓ Game created successfully")
print(f"  - Board Size: {len(game.board)}")
print(f"  - Available Moves: {game.get_available_moves()}")

# Test 3: Basic Gameplay
print("\n[TEST 3] Testing Basic Gameplay...")
game.player_move(4)  # Human plays center
print(f"✓ Human move to position 4 - Board: {game.get_board_state()}")

ai_pos = agent.select_action(game.board, training=False)
game.make_move(ai_pos, "O")
print(f"✓ AI move to position {ai_pos} - Board: {game.get_board_state()}")

# Test 4: Training
print("\n[TEST 4] Training AI for 10 episodes...")
trainer = GameTrainer(agent)
for i in range(10):
    game = TicTacToeGame(agent)
    game_over = False
    while not game_over:
        ai_move_pos = agent.select_action(game.board, training=True)
        if ai_move_pos == -1:
            break
        state = game.get_board_state()
        game.make_move(ai_move_pos, "X")
        next_state = game.get_board_state()
        game_over, winner = game.evaluate_game_state()
        agent.update_q_value(state, ai_move_pos, 1.0 if winner == "X" else 0, next_state, game_over)
        if game_over:
            break
        
        ai_move_pos = agent.select_action(game.board, training=True)
        if ai_move_pos == -1:
            break
        state = game.get_board_state()
        game.make_move(ai_move_pos, "O")
        next_state = game.get_board_state()
        game_over, winner = game.evaluate_game_state()
        agent.update_q_value(state, ai_move_pos, 1.0 if winner == "O" else 0, next_state, game_over)
    
    agent.decay_epsilon()

print(f"✓ Training completed")
print(f"  - Q-Table States: {len(agent.q_table)}")
print(f"  - Current Epsilon: {agent.epsilon:.4f}")

# Test 5: Model Save/Load
print("\n[TEST 5] Testing Model Persistence...")
import os
os.makedirs("models", exist_ok=True)
agent.save_model("models/test_model.pkl")
print(f"✓ Model saved successfully")

agent2 = QLearningAgent()
agent2.load_model("models/test_model.pkl")
print(f"✓ Model loaded successfully")
print(f"  - Loaded Q-Table Size: {len(agent2.q_table)}")

# Cleanup
os.remove("models/test_model.pkl")

print("\n" + "=" * 50)
print("All Tests Passed Successfully!")
print("=" * 50)
