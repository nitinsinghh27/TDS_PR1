# Quick Setup Guide

This guide will help you set up and run the LLM Code Deployment System in under 10 minutes.

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] GitHub account created
- [ ] GitHub Personal Access Token obtained
- [ ] Anthropic or OpenAI API key obtained

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
cd Project1
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "LLM Deployment System"
4. Select scopes:
   - ✅ `repo` (all sub-items)
   - ✅ `workflow`
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### 3. Get LLM API Key

**Option A: Anthropic Claude (Recommended)**
1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)

**Option B: OpenAI GPT**
1. Visit: https://platform.openai.com/
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

### 4. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

**Minimum required configuration**:
```env
STUDENT_EMAIL=your.email@example.com
STUDENT_SECRET=any-secret-phrase-you-choose
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your-github-username
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Test the Setup

```bash
# Run the server
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 6. Test with a Request

Open a new terminal and run:

```bash
curl -X POST http://localhost:5000/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "any-secret-phrase-you-choose",
    "task": "test-hello-world-123",
    "round": 1,
    "nonce": "test-nonce-001",
    "brief": "Create a simple HTML page that displays Hello World in a large, centered heading with a colorful background",
    "checks": [
      "Page has an h1 tag",
      "Page displays Hello World",
      "Page has a colorful background"
    ],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

**Replace**:
- `your.email@example.com` with your actual email
- `any-secret-phrase-you-choose` with the secret you set in `.env`

### 7. Verify Success

If successful, you'll receive:
```json
{
  "status": "success",
  "message": "Application deployed successfully",
  "repo_url": "https://github.com/username/test-hello-world-123",
  "pages_url": "https://username.github.io/test-hello-world-123/",
  "commit_sha": "..."
}
```

Check:
1. Visit the `repo_url` - you should see your new repository
2. Wait 1-2 minutes, then visit `pages_url` - you should see your app live!

## Common Setup Issues

### Issue: "No module named 'flask'"

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "GITHUB_TOKEN not configured"

**Solution**:
- Verify `.env` file exists
- Check that `GITHUB_TOKEN=...` line is present
- Ensure no extra spaces around the `=` sign
- Token should start with `ghp_`

### Issue: "Secret verification failed"

**Solution**:
- Ensure the `secret` in your request matches `STUDENT_SECRET` in `.env`
- Both must be exactly the same (case-sensitive)

### Issue: "Authentication failed" from GitHub

**Solution**:
- Generate a new GitHub token
- Ensure all required scopes are selected
- Check token hasn't expired
- Verify token is correctly copied to `.env`

### Issue: "API key invalid" from Anthropic/OpenAI

**Solution**:
- Verify API key is correctly copied
- Check you have credits/quota available
- Ensure key hasn't been revoked
- Try generating a new key

### Issue: GitHub Pages not accessible

**Solution**:
- Wait 2-5 minutes for GitHub Pages to build
- Check repository is public
- Verify GitHub Pages is enabled in repo settings
- Check repo name doesn't contain invalid characters

## Production Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set all environment variables
heroku config:set STUDENT_EMAIL=your@email.com
heroku config:set STUDENT_SECRET=your-secret
heroku config:set GITHUB_TOKEN=your-token
heroku config:set GITHUB_USERNAME=your-username
heroku config:set ANTHROPIC_API_KEY=your-key

# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

Your API will be available at: `https://your-app-name.herokuapp.com`

### Deploy to Railway

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in Settings → Variables
6. Railway will automatically deploy

### Deploy to Render

1. Go to: https://render.com/
2. Sign up
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Add environment variables
7. Click "Create Web Service"

## Next Steps

1. **Submit your API endpoint** to the Google Form provided by instructors
2. **Test with sample tasks** to ensure everything works
3. **Monitor logs** during evaluation
4. **Keep your API running** during the evaluation period
5. **Don't change your secret** after submission

## Getting Help

**Check logs**:
```bash
python app.py
# Server logs will appear here
```

**Test individual components**:
```python
# Test validator
from validator import validate_request
result = validate_request({"email": "test@test.com", ...})
print(result)

# Test secret
from validator import verify_secret
print(verify_secret("test", "test"))  # Should print True
```

**Verify environment variables**:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token:', os.getenv('GITHUB_TOKEN')[:10])"
```

## Security Reminders

- ⚠️ Never commit `.env` file
- ⚠️ Never share your GitHub token
- ⚠️ Never share your API keys
- ⚠️ Use environment variables in production
- ⚠️ Keep your secret secure

## Cost Considerations

**Anthropic Claude**:
- ~$0.003 per request for Claude 3.5 Sonnet
- ~$3 per 1000 requests
- New accounts get free credits

**OpenAI GPT-4**:
- ~$0.03 per request
- ~$30 per 1000 requests
- More expensive but widely available

**GitHub**:
- Free for public repositories
- Free GitHub Pages hosting

**Hosting**:
- Heroku: Free tier available (may sleep after 30 min)
- Railway: $5/month
- Render: Free tier available

**Recommendation**: Start with Anthropic Claude (cheaper) and Railway/Render (reliable).

## Support Resources

- **Project Docs**: See PROJECT_README.md for detailed information
- **Flask Docs**: https://flask.palletsprojects.com/
- **PyGithub Docs**: https://pygithub.readthedocs.io/
- **Anthropic Docs**: https://docs.anthropic.com/
- **OpenAI Docs**: https://platform.openai.com/docs

---

You're ready to go! Run `python app.py` and start deploying applications automatically.
