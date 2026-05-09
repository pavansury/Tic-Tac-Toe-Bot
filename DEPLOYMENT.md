# 🚀 Streamlit Cloud Deployment Guide

## Step-by-Step Deployment Instructions

### Prerequisites
- GitHub account with your repository
- Streamlit Community Cloud account (free)

### Deployment Steps

#### 1. Create Streamlit Cloud Account
1. Go to [Streamlit Community Cloud](https://share.streamlit.io)
2. Click "Sign up with GitHub"
3. Authorize Streamlit to access your GitHub account
4. Click "Continue"

#### 2. Deploy Your App
1. In Streamlit Cloud dashboard, click "New app"
2. **Repository**: Select `pavansury/Tic-Tac-Toe-Bot`
3. **Branch**: Select `main`
4. **Main file path**: Type `app.py`
5. Click "Deploy"

#### 3. Initial Deployment
- First deployment takes 2-3 minutes
- You'll see deployment logs in real-time
- Status shows "Running" when complete
- Your app URL will be like: `https://rl-tic-tac-toe-bot.streamlit.app`

#### 4. Optional Configuration

Create `streamlit/config.toml` in your repository:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e0e2f0"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"

[client]
showErrorDetails = true

[server]
maxUploadSize = 200
enableXsrfProtection = true
runOnSave = true
```

#### 5. Add GitHub Secrets (Optional)
If you add API keys or secrets:

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Create new repository secret
4. In Streamlit Cloud settings, link GitHub secret

### Troubleshooting Deployment

**Issue**: App shows blank page
- **Solution**: Check deployment logs for errors
- Try restarting the app (Manage app → Reboot app)

**Issue**: Import errors
- **Solution**: Update `requirements.txt` and redeploy
- Check Python version compatibility

**Issue**: Slow training on cloud
- **Solution**: Reduce default training episodes
- Consider splitting training and play modes

**Issue**: Model file not saving
- **Solution**: Streamlit Cloud uses temporary storage
- Models persist during session but clear on redeploy
- Implement database storage for permanent models

### Monitoring Your Deployment

1. **Access Logs**: Dashboard → Settings → View logs
2. **Metrics**: Monitor CPU, memory, and execution time
3. **Errors**: Real-time error tracking
4. **Usage**: View visitor stats

### Advanced Configuration

#### Setting Up Custom Domain
1. Streamlit Cloud dashboard → App settings
2. Custom domains → Add your domain
3. Add CNAME record to DNS provider
4. Wait for verification (usually 5-10 minutes)

#### Environment Variables
Create `.streamlit/secrets.toml` for local development:

```toml
[database]
api_key = "your-key-here"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["database"]["api_key"]
```

#### GitHub Sync
- Deployment auto-updates when you push to `main`
- Redeploy manually if needed
- All changes push automatically

### Performance Optimization

1. **Reduce reload time**:
```python
@st.cache_resource
def load_model():
    agent = QLearningAgent()
    agent.load_model("models/rl_model.pkl")
    return agent
```

2. **Optimize training**:
- Default 1000 episodes (changeable by users)
- Show progress bar
- Cache training results

3. **Memory management**:
- Don't store massive datasets
- Clear temporary files
- Use session state efficiently

### URL Sharing

Your live app URL:
```
https://rl-tic-tac-toe-bot.streamlit.app
```

Share this link directly! Anyone can use your app.

### Redeploy App

To redeploy after code changes:
```bash
cd /workspaces/Tic-Tac-Toe-Bot
git add -A
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud auto-detects changes and redeploys (takes 1-2 minutes).

### Manage App

In Streamlit Cloud dashboard:
- **Reboot**: Restart app if frozen
- **Delete**: Remove app
- **Rename**: Change app name
- **Settings**: Manage configuration
- **Logs**: View deployment logs

### Support & Resources

- [Streamlit Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [GitHub Issues](https://github.com/pavansury/Tic-Tac-Toe-Bot/issues)
- [Streamlit Community](https://discuss.streamlit.io)

---

Your app is now live! 🎉
