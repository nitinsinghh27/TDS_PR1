# AI Pipeline Setup Guide

This guide is specifically for users who have an **AI Pipeline API key** from [aipipe.org](https://aipipe.org).

## Why AI Pipeline?

AI Pipeline offers several advantages:
- **Free tier**: $0.10/week free credit
- **Multiple LLM providers**: Access OpenAI, OpenRouter, and Gemini through one API
- **Simple authentication**: One token for all models
- **Browser-friendly**: Built for web applications
- **Cost-effective**: Pay-as-you-go pricing

## Quick Setup (5 minutes)

### 1. Get Your AI Pipeline Token

1. Visit [https://aipipe.org/login](https://aipipe.org/login)
2. Sign up or log in
3. Copy your API token (you should already have this!)

### 2. Install Dependencies

```bash
cd Project1

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Add your credentials to `.env`**:
```env
STUDENT_EMAIL=your.email@example.com
STUDENT_SECRET=your-chosen-secret-phrase
GITHUB_TOKEN=ghp_your_github_token
GITHUB_USERNAME=your-github-username
AIPIPE_API_KEY=your-aipipe-token-here
```

### 4. Get GitHub Token (if you don't have one)

1. Go to: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Name: "LLM Deployment"
4. Select scopes:
   - ✅ `repo` (full control)
   - ✅ `workflow`
5. Generate and copy the token

### 5. Run the Server

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5001
```

### 6. Test It!

Open a new terminal and run:

```bash
curl -X POST http://localhost:5001/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your-chosen-secret-phrase",
    "task": "test-hello-123",
    "round": 1,
    "nonce": "test-001",
    "brief": "Create a colorful Hello World page with animation",
    "checks": ["Has h1 tag", "Says Hello World"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

**Important**: Replace `your.email@example.com` and `your-chosen-secret-phrase` with the values you set in `.env`!

If successful, you'll get:
```json
{
  "status": "success",
  "repo_url": "https://github.com/username/test-hello-123",
  "pages_url": "https://username.github.io/test-hello-123/"
}
```

## AI Pipeline Models Available

The system is configured to use `anthropic/claude-3.5-sonnet` through OpenRouter (via AI Pipeline). You can change this in [code_generator.py:167](code_generator.py#L167).

**Popular models you can use**:
- `anthropic/claude-3.5-sonnet` - Best quality (recommended)
- `openai/gpt-4o` - OpenAI's latest
- `openai/gpt-4o-mini` - Faster and cheaper
- `google/gemini-pro` - Google's model
- `meta-llama/llama-3.1-70b-instruct` - Open source

To change models, edit [code_generator.py:167](code_generator.py#L167):
```python
"model": "openai/gpt-4o-mini",  # Change this line
```

## Troubleshooting

### "AI Pipeline API error: 401"
- Your `AIPIPE_API_KEY` is incorrect
- Check you copied the full token
- Try generating a new token at aipipe.org

### "AI Pipeline API error: 402"
- You've exceeded your free credits
- Add credits to your AI Pipeline account
- Or switch to a cheaper model

### "AI Pipeline API error: 429"
- Rate limited (too many requests)
- Wait a minute and try again
- AI Pipeline has rate limits on free tier

### "Package not installed" warnings
Those are just hints from your IDE. The packages will be installed when you run `pip install -r requirements.txt`.

## Cost Estimates

With AI Pipeline and Claude 3.5 Sonnet:
- **Per request**: ~$0.01 - $0.03
- **10 deployments**: ~$0.20
- **100 deployments**: ~$2.00

The free tier ($0.10/week) should be enough for testing (5-10 requests).

## Alternative: Cheaper Models

If you need to minimize costs, edit [code_generator.py:167](code_generator.py#L167) to use a cheaper model:

```python
"model": "openai/gpt-4o-mini",  # Much cheaper!
```

Or:
```python
"model": "google/gemini-flash-1.5",  # Very cheap
```

## Production Deployment

Once everything works locally, deploy to a cloud platform:

### Heroku
```bash
heroku create my-llm-deployer
heroku config:set AIPIPE_API_KEY=your-token
heroku config:set GITHUB_TOKEN=your-token
# ... set other variables
git push heroku main
```

### Railway (Recommended)
1. Push your code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Automatic deployment!

### Render
1. Create Web Service on render.com
2. Connect your GitHub repo
3. Add environment variables
4. Deploy!

## Security Note

⚠️ **Never commit `.env` file!**

The `.gitignore` is already configured to prevent this, but double-check:
```bash
git status
# Should NOT show .env file
```

## Need Help?

1. **Check logs**: The terminal running `python app.py` shows detailed logs
2. **Test individual parts**: See [PROJECT_README.md](PROJECT_README.md) for testing
3. **AI Pipeline docs**: [https://aipipe.org/](https://aipipe.org/)

## What's Next?

1. Test with different briefs
2. Try different models to compare quality/cost
3. Deploy to a cloud platform
4. Submit your API endpoint to instructors

---

**You're all set!** Your system will use AI Pipeline to generate code automatically. 🚀
