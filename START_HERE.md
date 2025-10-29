# 🚀 START HERE - LLM Code Deployment System

Welcome! This is your complete LLM Code Deployment System for the TDS project.

## 📋 What You Have

A fully functional system that:
1. ✅ Receives POST requests with app briefs
2. ✅ Verifies your secret for authentication
3. ✅ Generates code using AI (via AI Pipeline)
4. ✅ Creates GitHub repositories automatically
5. ✅ Deploys to GitHub Pages
6. ✅ Notifies evaluation API with results
7. ✅ Handles Round 2 revision requests

## 📁 Project Files

```
Project1/
├── 📘 START_HERE.md          ← You are here!
├── 📘 AIPIPE_SETUP.md         ← Quick setup for AI Pipeline users (RECOMMENDED)
├── 📘 SETUP_GUIDE.md          ← Detailed setup guide
├── 📘 PROJECT_README.md       ← Complete technical documentation
├── 📘 README.md               ← Original project specification
│
├── 🐍 app.py                  ← Main Flask API server
├── 🐍 validator.py            ← Request validation
├── 🐍 code_generator.py       ← LLM code generation (with AI Pipeline support!)
├── 🐍 github_manager.py       ← GitHub operations
├── 🐍 evaluator.py            ← Evaluation API notifications
├── 🐍 test_api.py             ← Test script
│
├── ⚙️  .env.example            ← Environment config template
├── ⚙️  .gitignore              ← Git ignore rules
├── ⚙️  requirements.txt        ← Python dependencies
├── ⚙️  Procfile                ← Heroku deployment config
├── ⚙️  runtime.txt             ← Python version
└── 🔧 run.sh                  ← Quick start script
```

## 🎯 Quick Start (Choose Your Path)

### Path 1: AI Pipeline User (RECOMMENDED FOR YOU!)

Since you have an AI Pipeline key, follow this path:

1. **Read the AI Pipeline Setup Guide**
   ```bash
   # Open this file:
   cat AIPIPE_SETUP.md
   ```
   Or read: [AIPIPE_SETUP.md](AIPIPE_SETUP.md)

2. **It will take just 5 minutes!**

### Path 2: Using Anthropic or OpenAI

If you have Anthropic Claude or OpenAI API keys instead:

1. **Read the General Setup Guide**
   ```bash
   cat SETUP_GUIDE.md
   ```
   Or read: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🏃 Super Quick Start (TL;DR)

```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your credentials

# 3. Run
python app.py

# 4. Test (in another terminal)
python test_api.py
```

## ✅ What You Need

Before starting, make sure you have:

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] GitHub account
- [ ] GitHub Personal Access Token ([Get one](https://github.com/settings/tokens))
- [ ] AI Pipeline API key (you already have this!)

## 📚 Documentation Guide

**Start here first:**
1. [AIPIPE_SETUP.md](AIPIPE_SETUP.md) - Quick setup for AI Pipeline (5 min read)

**Then if needed:**
2. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup guide (10 min read)
3. [PROJECT_README.md](PROJECT_README.md) - Complete technical docs (30 min read)
4. [README.md](README.md) - Original project specification

## 🎓 How It Works

```
1. Instructor sends POST request
         ↓
2. Your API validates secret
         ↓
3. AI Pipeline generates code
         ↓
4. GitHub repo created & deployed
         ↓
5. Evaluation API notified
         ↓
6. Done! ✅
```

## 🧪 Testing

After setup, test your system:

```bash
# Method 1: Use the test script
python test_api.py

# Method 2: Manual curl
curl -X POST http://localhost:5001/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "secret": "your-secret",
    "task": "test-123",
    "round": 1,
    "nonce": "test",
    "brief": "Create a hello world page",
    "checks": [],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

## 🚨 Common Issues

### "No module named 'flask'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "GITHUB_TOKEN not configured"
Edit `.env` file and add your GitHub token

### "Secret verification failed"
Make sure the `secret` in your request matches `STUDENT_SECRET` in `.env`

### "AI Pipeline API error"
- Check your `AIPIPE_API_KEY` is correct
- Verify you have credits at aipipe.org

## 💰 Cost Estimate

With AI Pipeline (Claude 3.5 Sonnet):
- **Testing (10 requests)**: ~$0.20
- **Project completion**: ~$1-2
- **Free tier**: $0.10/week (enough for initial testing)

## 🌐 Deployment

Once it works locally, deploy to the cloud:

**Railway (Easiest)**
1. Push to GitHub
2. Connect Railway
3. Add env variables
4. Deploy!

**Heroku**
```bash
heroku create
heroku config:set AIPIPE_API_KEY=...
git push heroku main
```

## 📞 Getting Help

1. **Check logs**: Look at terminal output when running `python app.py`
2. **Read docs**: Each MD file has detailed troubleshooting
3. **Test components**: Use `test_api.py` to verify setup

## 🎯 Next Steps

1. ✅ Read [AIPIPE_SETUP.md](AIPIPE_SETUP.md) (5 minutes)
2. ✅ Follow setup instructions
3. ✅ Test locally with `test_api.py`
4. ✅ Deploy to cloud platform
5. ✅ Submit your API endpoint to instructors
6. ✅ Wait for evaluation requests!

## 🔒 Security Reminders

- ⚠️ Never commit `.env` file
- ⚠️ Never share your API keys
- ⚠️ Keep your GitHub token secure
- ⚠️ The `.gitignore` is already configured

## ✨ Features

- **AI Pipeline Integration**: Use your existing API key!
- **Multiple LLM Support**: Works with Claude, GPT, Gemini
- **Auto GitHub Deployment**: Creates repos and enables Pages
- **Retry Logic**: Handles evaluation API failures
- **Professional Output**: Generated repos include README and LICENSE
- **Error Handling**: Robust logging and fallbacks
- **Template Fallback**: Works even without LLM APIs

## 📊 System Architecture

```
Flask API Server (app.py)
    ↓
Request Validator (validator.py)
    ↓
Code Generator (code_generator.py) → AI Pipeline
    ↓
GitHub Manager (github_manager.py) → GitHub API
    ↓
Evaluator (evaluator.py) → Evaluation API
```

## 🎉 You're Ready!

Everything is set up and ready to go. Just follow the [AIPIPE_SETUP.md](AIPIPE_SETUP.md) guide and you'll be deploying applications in 5 minutes!

Good luck with your project! 🚀

---

**Created**: 2025-01-16
**For**: TDS LLM Code Deployment Project
**Using**: AI Pipeline + GitHub Pages
