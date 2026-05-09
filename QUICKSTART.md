# 🎮 Quick Start Guide

## Local Installation (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/pavansury/Tic-Tac-Toe-Bot.git
cd Tic-Tac-Toe-Bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run app.py
```

### 4. Open Browser
```
http://localhost:8501
```

## First Time Using the App

### Getting Started
1. **Open the "Play" page** - This is the main gameplay interface
2. **Select difficulty** - Try "Easy" first to test
3. **Play a game** - Click on empty cells to make your move (X)
4. **Watch AI play** - AI automatically responds with O
5. **Check your score** - See wins/losses in the sidebar

### No Trained AI?
⚠️ If AI plays randomly at first:
1. Go to **"Train AI"** page
2. Click "Start Training"
3. Wait 2-3 minutes for training (1000 episodes)
4. Go back to **Play** and enjoy improved AI!

## Understanding the Screens

### 🎮 Play Page
- **Board**: Click cells to play
- **Difficulty**: 3 levels (Easy/Normal/Hard)
- **Score Card**: Track your wins/losses
- **Game Info**: Shows AI status

### 🤖 Train AI Page
- **Episodes**: How many training games (default: 1000)
- **Learning Rate**: How fast AI learns
- **Other Parameters**: For advanced users
- **Progress Bar**: Shows training status
- **Learning Chart**: Visualizes progress

### 📊 Statistics Page
- **Q-Table Size**: Number of learned positions
- **Player Performance**: Your win rate
- **Game History**: Recent moves
- **Charts**: Visual win/loss data

### ⚙️ Settings Page
- **Save Model**: Backup trained AI
- **Load Model**: Restore previous AI
- **Reset Everything**: Start fresh
- **Model Info**: Technical details

## Pro Tips

1. **Better AI**: Train with 5000+ episodes for excellent play
2. **Save Models**: Use Settings to backup your trained AI
3. **Understand RL**: Check README.md for Q-Learning info
4. **Test Easy Mode**: Best for learning the app
5. **Share URL**: Deployed version is shareable

## Common Issues

**Q: AI plays randomly?**
- A: Train it first in "Train AI" page

**Q: Training is slow?**
- A: It's normal! 1000 episodes ≈ 2 minutes

**Q: Want to see model improve?**
- A: Check Stats page during/after training

**Q: How to reset everything?**
- A: Settings page → "Reset Everything" button

## Keyboard Shortcuts
- No keyboard shortcuts - click-based interface
- Mobile friendly! ✓

## Next Steps

1. ✅ Play a few games
2. ✅ Train the AI
3. ✅ Check statistics
4. ✅ Read README.md for technical details
5. ✅ Deploy on Streamlit Cloud (optional)

## Deploy Online (FREE!)

Want to share your app online?

```bash
# 1. Push to GitHub
git add -A
git commit -m "Update AI model"
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app"
# 4. Select repo, branch, and app.py
# 5. Deploy!

# Your live URL: https://rl-tic-tac-toe-bot.streamlit.app
```

See `DEPLOYMENT.md` for detailed instructions.

## Support

- 📖 [Full Documentation](README.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)
- 🐛 [Report Issues](https://github.com/pavansury/Tic-Tac-Toe-Bot/issues)

---

**Enjoy playing against the self-learning AI! 🤖**
