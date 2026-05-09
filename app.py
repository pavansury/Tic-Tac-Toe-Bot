"""
Advanced RL Tic Tac Toe Bot - Streamlit Application
Features: Training, Playing, Statistics, Model Management
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import time
import os
from q_learning_agent import QLearningAgent
from game_engine import TicTacToeGame, GameTrainer

# =====================================================
# Page Configuration
# =====================================================
st.set_page_config(
    page_title="RL Tic Tac Toe Bot",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# Custom CSS
# =====================================================
st.markdown("""
<style>
    .title-main {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .board-cell {
        width: 100%;
        padding: 20px;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        border: 2px solid #1f77b4;
        cursor: pointer;
        background-color: #f0f2f6;
        border-radius: 10px;
        transition: background-color 0.3s;
    }
    .board-cell:hover {
        background-color: #e0e2f0;
    }
    .stats-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
    }
    .win {
        color: #00cc00;
        font-weight: bold;
    }
    .loss {
        color: #ff4444;
        font-weight: bold;
    }
    .draw {
        color: #ffaa00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# Session State Management
# =====================================================
def initialize_session_state():
    """Initialize all session state variables"""
    if "ai_agent" not in st.session_state:
        st.session_state.ai_agent = QLearningAgent()
    
    if "game" not in st.session_state:
        st.session_state.game = None
    
    if "game_history" not in st.session_state:
        st.session_state.game_history = []
    
    if "model_loaded" not in st.session_state:
        st.session_state.model_loaded = False
    
    if "training_progress" not in st.session_state:
        st.session_state.training_progress = []
    
    if "human_score" not in st.session_state:
        st.session_state.human_score = {"wins": 0, "losses": 0, "draws": 0}
    
    if "ai_difficulty" not in st.session_state:
        st.session_state.ai_difficulty = "Normal"
    
    if "page" not in st.session_state:
        st.session_state.page = "🎮 Play"

initialize_session_state()

# =====================================================
# Helper Functions
# =====================================================
def load_or_create_model(model_path: str = "models/rl_model.pkl") -> bool:
    """Load existing model or create new one"""
    os.makedirs("models", exist_ok=True)
    
    if os.path.exists(model_path):
        if st.session_state.ai_agent.load_model(model_path):
            st.session_state.model_loaded = True
            return True
    
    return False

def save_model(model_path: str = "models/rl_model.pkl"):
    """Save current model"""
    os.makedirs("models", exist_ok=True)
    st.session_state.ai_agent.save_model(model_path)

def create_new_game():
    """Create a new game"""
    st.session_state.game = TicTacToeGame(st.session_state.ai_agent)

def render_board():
    """Render the game board with interactive buttons"""
    if not st.session_state.game:
        create_new_game()
    
    game = st.session_state.game
    board = game.board
    
    # Create 3x3 grid
    cols = st.columns(3)
    
    for i in range(9):
        with cols[i % 3]:
            cell_value = board[i]
            
            # Color based on content
            if cell_value == "X":
                button_color = "🔵"
                display_value = "X"
            elif cell_value == "O":
                button_color = "🔴"
                display_value = "O"
            else:
                button_color = "⬜"
                display_value = " "
            
            if st.button(f"{button_color}\n{display_value}", key=f"cell_{i}", use_container_width=True, 
                        help=f"Position {i}"):
                
                if game.board[i] == " " and not game.game_over:
                    # Human move
                    game.player_move(i)
                    st.session_state.game_history.append(f"Human: Position {i}")
                    
                    # Check game state
                    game_over, winner = game.evaluate_game_state()
                    
                    if game_over:
                        if winner == "X":
                            st.session_state.human_score["wins"] += 1
                            st.success("🎉 You Win!")
                        elif winner == "Draw":
                            st.session_state.human_score["draws"] += 1
                            st.info("🤝 Draw!")
                        else:
                            st.session_state.human_score["losses"] += 1
                            st.error("🤖 AI Wins!")
                        game.game_over = True
                        game.winner = winner
                    else:
                        # AI move
                        time.sleep(0.5)  # Brief delay for UX
                        
                        # Adjust difficulty
                        if st.session_state.ai_difficulty == "Easy":
                            st.session_state.ai_agent.epsilon = 0.5
                        elif st.session_state.ai_difficulty == "Normal":
                            st.session_state.ai_agent.epsilon = 0.1
                        else:  # Hard
                            st.session_state.ai_agent.epsilon = 0.01
                        
                        ai_pos = game.ai_move(training=False)
                        if ai_pos != -1:
                            st.session_state.game_history.append(f"AI: Position {ai_pos}")
                        
                        # Check game state again
                        game_over, winner = game.evaluate_game_state()
                        
                        if game_over:
                            if winner == "O":
                                st.session_state.human_score["losses"] += 1
                                st.error("🤖 AI Wins!")
                            elif winner == "Draw":
                                st.session_state.human_score["draws"] += 1
                                st.info("🤝 Draw!")
                            else:
                                st.session_state.human_score["wins"] += 1
                                st.success("🎉 You Win!")
                            game.game_over = True
                            game.winner = winner
                
                st.rerun()

def display_board_simple():
    """Display board without interactivity"""
    if st.session_state.game:
        board = st.session_state.game.board
        cols = st.columns(3)
        
        for i in range(9):
            with cols[i % 3]:
                if board[i] == "X":
                    st.markdown(f"### 🔵")
                elif board[i] == "O":
                    st.markdown(f"### 🔴")
                else:
                    st.markdown(f"### ⬜")

# =====================================================
# Main App Layout
# =====================================================
st.markdown("<h1 class='title-main'>🎮 RL Tic Tac Toe Bot - Advanced Edition</h1>", unsafe_allow_html=True)
st.markdown("*A self-learning AI using Q-Learning!*")

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Select Page:", 
    ["🎮 Play", "🤖 Train AI", "📊 Statistics", "⚙️ Settings"])

# =====================================================
# PAGE 1: PLAY
# =====================================================
if page == "🎮 Play":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Play Against AI")
        
        if not load_or_create_model():
            st.warning("⚠️ No trained model found. AI will play with initial knowledge.")
            st.info("💡 Tip: Train the AI first in the 'Train AI' section for better performance!")
        else:
            st.success("✅ Trained model loaded successfully!")
        
        # Difficulty selector
        difficulty = st.select_slider(
            "🎯 AI Difficulty Level",
            options=["Easy", "Normal", "Hard"],
            value="Normal"
        )
        st.session_state.ai_difficulty = difficulty
        
        # Game status
        if st.session_state.game is None or st.session_state.game.game_over:
            if st.button("🆕 New Game", key="new_game_btn", use_container_width=True):
                create_new_game()
                st.rerun()
        
        st.markdown("---")
        
        # Render board
        st.markdown("### Your Move (X) vs AI (O)")
        render_board()
        
        # Reset button
        if st.session_state.game and st.session_state.game.game_over:
            if st.button("🔄 Play Again", key="play_again_btn", use_container_width=True):
                create_new_game()
                st.rerun()
    
    with col2:
        st.header("📈 Score")
        score = st.session_state.human_score
        
        st.markdown(f"""
        <div class='stats-card'>
            <div class='win'>Wins: {score['wins']}</div>
            <div class='loss'>Losses: {score['losses']}</div>
            <div class='draw'>Draws: {score['draws']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        total = score['wins'] + score['losses'] + score['draws']
        if total > 0:
            win_rate = (score['wins'] / total) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        st.markdown("---")
        st.subheader("Game Info")
        st.write(f"**Difficulty:** {difficulty}")
        st.write(f"**Model Status:** {'✅ Loaded' if st.session_state.model_loaded else '❌ Not Loaded'}")
        st.write(f"**Q-Table Size:** {len(st.session_state.ai_agent.q_table)}")
        st.write(f"**Exploration Rate:** {st.session_state.ai_agent.epsilon:.4f}")

# =====================================================
# PAGE 2: TRAIN AI
# =====================================================
elif page == "🤖 Train AI":
    st.header("🤖 Train AI Using Reinforcement Learning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Training Configuration")
        
        # Training parameters
        episodes = st.slider("Number of Episodes", min_value=100, max_value=10000, 
                            value=1000, step=100)
        learning_rate = st.slider("Learning Rate (α)", min_value=0.01, max_value=1.0, 
                                  value=0.1, step=0.01)
        discount_factor = st.slider("Discount Factor (γ)", min_value=0.5, max_value=1.0, 
                                    value=0.95, step=0.05)
        epsilon_start = st.slider("Initial Exploration Rate (ε)", min_value=0.01, max_value=1.0, 
                                  value=0.2, step=0.05)
        epsilon_decay = st.slider("Exploration Decay Rate", min_value=0.9, max_value=0.999, 
                                  value=0.995, step=0.001)
        
        st.markdown("---")
        
        if st.button("🚀 Start Training", use_container_width=True, key="train_btn"):
            # Create new agent with custom parameters
            st.session_state.ai_agent = QLearningAgent(
                learning_rate=learning_rate,
                discount_factor=discount_factor,
                epsilon=epsilon_start,
                epsilon_decay=epsilon_decay
            )
            
            trainer = GameTrainer(st.session_state.ai_agent)
            
            # Training progress
            progress_bar = st.progress(0)
            progress_text = st.empty()
            chart_data = st.empty()
            
            training_data = []
            
            with st.spinner("🎮 Training in progress..."):
                for episode in range(episodes):
                    # Train
                    game = TicTacToeGame(st.session_state.ai_agent)
                    game_over = False
                    
                    while not game_over:
                        # AI as X
                        ai_move_pos = st.session_state.ai_agent.select_action(game.board, training=True)
                        if ai_move_pos == -1:
                            game_over = True
                            break
                        
                        state = game.get_board_state()
                        game.make_move(ai_move_pos, "X")
                        next_state = game.get_board_state()
                        
                        game_over, winner = game.evaluate_game_state()
                        
                        if winner == "X":
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 1.0, next_state, True)
                        elif winner == "Draw":
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 0.5, next_state, True)
                        else:
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 0, next_state, False)
                        
                        if game_over:
                            break
                        
                        # AI as O
                        ai_move_pos = st.session_state.ai_agent.select_action(game.board, training=True)
                        if ai_move_pos == -1:
                            game_over = True
                            break
                        
                        state = game.get_board_state()
                        game.make_move(ai_move_pos, "O")
                        next_state = game.get_board_state()
                        
                        game_over, winner = game.evaluate_game_state()
                        
                        if winner == "O":
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 1.0, next_state, True)
                        elif winner == "Draw":
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 0.5, next_state, True)
                        else:
                            st.session_state.ai_agent.update_q_value(state, ai_move_pos, 0, next_state, False)
                    
                    st.session_state.ai_agent.decay_epsilon()
                    
                    training_data.append({
                        "episode": episode + 1,
                        "q_table_size": len(st.session_state.ai_agent.q_table),
                        "epsilon": st.session_state.ai_agent.epsilon
                    })
                    
                    # Update progress
                    progress = (episode + 1) / episodes
                    progress_bar.progress(progress)
                    progress_text.text(f"Episode: {episode + 1} / {episodes} | Q-Table: {len(st.session_state.ai_agent.q_table)} states | ε: {st.session_state.ai_agent.epsilon:.4f}")
                    
                    # Update chart periodically
                    if (episode + 1) % 50 == 0:
                        df = pd.DataFrame(training_data)
                        with chart_data:
                            st.line_chart(df.set_index('episode')[['q_table_size']])
            
            # Save model
            save_model()
            st.session_state.model_loaded = True
            
            st.success("✅ Training Complete!")
            st.balloons()
    
    with col2:
        st.subheader("ℹ️ Training Info")
        st.info("""
        **Q-Learning Parameters:**
        - **α (Learning Rate):** How fast the model learns
        - **γ (Discount Factor):** Importance of future rewards
        - **ε (Exploration Rate):** Probability of random moves
        - **Decay:** How fast ε decreases
        """)
        
        st.markdown("---")
        st.subheader("📌 Tips")
        st.write("""
        - More episodes = Better AI (but slower training)
        - Start with 1000 episodes for quick training
        - Use 5000+ for production-quality AI
        - Higher exploration rate = More learning, but slower convergence
        """)

# =====================================================
# PAGE 3: STATISTICS
# =====================================================
elif page == "📊 Statistics":
    st.header("📊 AI Model Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Q-Table States", len(st.session_state.ai_agent.q_table))
    
    with col2:
        st.metric("Current ε", f"{st.session_state.ai_agent.epsilon:.4f}")
    
    with col3:
        st.metric("Learning Rate", f"{st.session_state.ai_agent.learning_rate:.4f}")
    
    st.markdown("---")
    
    # Player Statistics
    st.subheader("📈 Player Performance")
    score = st.session_state.human_score
    total_games = score['wins'] + score['losses'] + score['draws']
    
    if total_games > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Games", total_games)
        
        with col2:
            st.metric("Wins", score['wins'], delta=f"{(score['wins']/total_games)*100:.1f}%")
        
        with col3:
            st.metric("Losses", score['losses'], delta=f"-{(score['losses']/total_games)*100:.1f}%")
        
        with col4:
            st.metric("Draws", score['draws'], delta=f"{(score['draws']/total_games)*100:.1f}%")
        
        # Chart
        chart_data = pd.DataFrame({
            'Result': ['Wins', 'Losses', 'Draws'],
            'Count': [score['wins'], score['losses'], score['draws']]
        })
        
        st.bar_chart(chart_data.set_index('Result'))
    else:
        st.info("Play some games to see statistics!")
    
    st.markdown("---")
    
    # Game History
    st.subheader("🎮 Game History")
    if st.session_state.game_history:
        for i, move in enumerate(st.session_state.game_history[-20:], 1):
            st.write(f"{i}. {move}")
    else:
        st.info("No game history yet.")

# =====================================================
# PAGE 4: SETTINGS
# =====================================================
elif page == "⚙️ Settings":
    st.header("⚙️ Settings & Model Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💾 Model Management")
        
        if st.button("💾 Save Current Model", use_container_width=True):
            save_model()
            st.success("✅ Model saved successfully!")
        
        if st.button("📂 Load Model", use_container_width=True):
            if load_or_create_model():
                st.success("✅ Model loaded successfully!")
            else:
                st.error("❌ No saved model found!")
        
        if st.button("🗑️ Reset Everything", use_container_width=True):
            st.session_state.ai_agent = QLearningAgent()
            st.session_state.game = None
            st.session_state.game_history = []
            st.session_state.human_score = {"wins": 0, "losses": 0, "draws": 0}
            st.session_state.model_loaded = False
            st.success("✅ Everything reset!")
            st.rerun()
    
    with col2:
        st.subheader("📊 Model Information")
        
        st.write(f"**Q-Table States:** {len(st.session_state.ai_agent.q_table)}")
        st.write(f"**Current Epsilon:** {st.session_state.ai_agent.epsilon:.6f}")
        st.write(f"**Learning Rate:** {st.session_state.ai_agent.learning_rate:.4f}")
        st.write(f"**Discount Factor:** {st.session_state.ai_agent.discount_factor:.2f}")
        st.write(f"**Model Status:** {'✅ Loaded' if st.session_state.model_loaded else '❌ Not Loaded'}")
    
    st.markdown("---")
    
    st.subheader("📚 About This Project")
    st.markdown("""
    ### RL Tic Tac Toe Bot - Advanced Edition
    
    This application demonstrates **Reinforcement Learning** using Q-Learning algorithm.
    
    **Key Features:**
    - 🤖 Q-Learning based AI agent
    - 🎮 Interactive gameplay
    - 🏋️ AI training functionality
    - 📊 Comprehensive statistics
    - 💾 Model persistence
    - 🎯 Adjustable difficulty levels
    
    **How Q-Learning Works:**
    1. AI learns by playing many games
    2. Each move/outcome updates Q-values
    3. Over time, AI discovers best moves
    4. Epsilon-greedy strategy balances exploration vs exploitation
    
    **Technologies:**
    - Python 3
    - Streamlit
    - NumPy
    - Pickle
    """)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    <p>🎮 RL Tic Tac Toe Bot v2.0 | Powered by Streamlit & Reinforcement Learning</p>
</div>
""", unsafe_allow_html=True)

# Load model on startup
load_or_create_model()
