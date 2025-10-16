# LLM Code Deployment System

A complete implementation of an automated code deployment system that receives application briefs, generates code using LLMs, creates GitHub repositories, and deploys to GitHub Pages.

## Overview

This system implements the complete workflow for the TDS LLM Code Deployment project:

1. **Receives POST requests** with application briefs and requirements
2. **Verifies student secrets** for authentication
3. **Generates code** using Anthropic Claude or OpenAI GPT
4. **Creates GitHub repositories** with proper structure
5. **Deploys to GitHub Pages** automatically
6. **Notifies evaluation API** with repository details
7. **Handles revision requests** (Round 2) to modify existing applications

## Project Structure

```
Project1/
├── app.py                  # Main Flask API server
├── validator.py            # Request validation and secret verification
├── code_generator.py       # LLM-based code generation
├── github_manager.py       # GitHub repository management
├── evaluator.py            # Evaluation API notification
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
├── PROJECT_README.md      # This file
└── README.md              # Original project specification
```

## Features

### Core Functionality

- **RESTful API Endpoint**: Flask-based API that accepts JSON POST requests
- **Secret Verification**: Validates student credentials against configured secrets
- **Request Validation**: Comprehensive validation of incoming requests
- **LLM Integration**: Supports both Anthropic Claude and OpenAI GPT for code generation
- **GitHub Integration**: Automated repository creation and management
- **GitHub Pages Deployment**: Automatic deployment and URL generation
- **Retry Logic**: Exponential backoff for evaluation API notifications
- **Error Handling**: Robust error handling and logging throughout

### Generated Repositories Include

- **index.html**: Complete, functional web application
- **README.md**: Professional documentation with:
  - Project summary
  - Setup instructions
  - Usage guide
  - Technical details
  - License information
- **LICENSE**: MIT License file

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git installed and configured
- GitHub account
- GitHub Personal Access Token with repo and workflow permissions
- API key for either Anthropic Claude or OpenAI GPT

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/Project1
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` with your credentials**:
   ```env
   STUDENT_EMAIL=your.email@example.com
   STUDENT_SECRET=your-secret-from-google-form
   GITHUB_TOKEN=ghp_your_github_personal_access_token
   GITHUB_USERNAME=your-github-username
   ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key
   # OR
   OPENAI_API_KEY=sk-your-openai-key
   ```

### Getting Required Credentials

#### GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (all)
   - `workflow`
   - `admin:org` → `read:org`
4. Generate and copy the token

#### Anthropic API Key

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new key

#### OpenAI API Key (Alternative)

1. Visit [platform.openai.com](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new secret key

## Usage

### Starting the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Load environment variables (if not using python-dotenv)
export $(cat .env | xargs)

# Run the server
python app.py
```

The server will start on `http://localhost:5001` by default.

### Making a Request

**Endpoint**: `POST /api/deploy`

**Request Format**:
```json
{
  "email": "student@example.com",
  "secret": "your-secret",
  "task": "task-name-12345",
  "round": 1,
  "nonce": "unique-nonce-abc123",
  "brief": "Create a web page that displays the current time and updates every second",
  "checks": [
    "Page displays current time",
    "Time updates automatically",
    "Page has a professional design"
  ],
  "evaluation_url": "https://example.com/evaluate",
  "attachments": []
}
```

**Example using curl**:
```bash
curl -X POST http://localhost:5001/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "your-secret",
    "task": "clock-app-abc123",
    "round": 1,
    "nonce": "nonce-xyz789",
    "brief": "Create a digital clock that shows current time",
    "checks": ["Displays time", "Updates every second"],
    "evaluation_url": "https://example.com/evaluate",
    "attachments": []
  }'
```

**Success Response**:
```json
{
  "status": "success",
  "message": "Application deployed successfully",
  "repo_url": "https://github.com/username/clock-app-abc123",
  "pages_url": "https://username.github.io/clock-app-abc123/",
  "commit_sha": "abc123def456..."
}
```

### Round 2 (Revision) Requests

Round 2 requests work identically but with `"round": 2` and typically include modifications to the existing brief:

```json
{
  "email": "student@example.com",
  "secret": "your-secret",
  "task": "clock-app-abc123",
  "round": 2,
  "nonce": "nonce-round2-xyz",
  "brief": "Update the clock to also show the date and add a timezone selector",
  "checks": [
    "Shows time and date",
    "Has timezone selector",
    "Updates in selected timezone"
  ],
  "evaluation_url": "https://example.com/evaluate",
  "attachments": []
}
```

## Deployment

### Local Development

Follow the setup instructions above and run locally for development and testing.

### Cloud Deployment Options

#### 1. Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set STUDENT_EMAIL=your@email.com
heroku config:set STUDENT_SECRET=your-secret
heroku config:set GITHUB_TOKEN=your-token
heroku config:set GITHUB_USERNAME=your-username
heroku config:set ANTHROPIC_API_KEY=your-key

# Deploy
git push heroku main
```

#### 2. Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in the Railway dashboard
3. Deploy automatically on push

#### 3. Render

1. Create a new Web Service
2. Connect your repository
3. Set environment variables
4. Deploy

#### 4. Google Cloud Run

```bash
# Build and deploy
gcloud run deploy llm-deployment \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Important Deployment Notes

- Always use HTTPS in production
- Keep your `.env` file secure and never commit it
- Use environment variables for all sensitive data
- Monitor API usage and costs for LLM services
- Set up logging and monitoring
- Consider rate limiting for the API endpoint

## Code Explanation

### app.py
Main Flask application that:
- Defines the `/api/deploy` endpoint
- Orchestrates the entire deployment workflow
- Handles errors and returns appropriate responses
- Provides health check endpoint at `/`

### validator.py
Handles all validation logic:
- Validates JSON structure and required fields
- Verifies email format
- Checks secret authentication
- Validates attachments format

### code_generator.py
Generates application code using LLMs:
- Supports Anthropic Claude and OpenAI GPT
- Decodes base64-encoded attachments
- Builds comprehensive prompts for code generation
- Parses LLM responses to extract HTML and README
- Provides template fallback when LLM unavailable

### github_manager.py
Manages GitHub operations:
- Creates public repositories
- Sanitizes repository names
- Pushes code, README, and LICENSE files
- Enables GitHub Pages
- Returns repository metadata

### evaluator.py
Handles evaluation API notifications:
- Sends POST requests with repo details
- Implements exponential backoff retry logic
- Handles timeouts and errors gracefully
- Ensures evaluation API receives notifications

## Technical Details

### Technology Stack

- **Backend**: Python 3.8+, Flask 3.0
- **GitHub API**: PyGithub 2.1
- **LLM APIs**: Anthropic SDK, OpenAI SDK
- **HTTP Client**: Requests library
- **Version Control**: Git

### API Design

The API follows REST principles:
- Uses appropriate HTTP methods (POST)
- Returns proper status codes
- Uses JSON for request/response
- Includes descriptive error messages

### Security Considerations

1. **Secret Verification**: All requests must include valid secret
2. **Environment Variables**: Sensitive data stored securely
3. **Public Repositories**: Generated repos are public (as required)
4. **No Secrets in Git**: `.gitignore` prevents committing sensitive files
5. **Token Scoping**: GitHub token has minimal required permissions

### Error Handling

The system handles various error scenarios:
- Invalid request format → 400 Bad Request
- Invalid secret → 403 Forbidden
- LLM API failures → Falls back to template
- GitHub API errors → Detailed logging
- Evaluation API failures → Retry with backoff
- Internal errors → 500 Internal Server Error

### Logging

Comprehensive logging throughout:
- Request receipt and validation
- Code generation progress
- GitHub operations
- Evaluation notifications
- Error details with stack traces

## Testing

### Manual Testing

Test with a sample request:

```bash
python -c "
import requests
import json

response = requests.post(
    'http://localhost:5001/api/deploy',
    json={
        'email': 'test@example.com',
        'secret': 'test-secret',
        'task': 'test-task-001',
        'round': 1,
        'nonce': 'test-nonce-123',
        'brief': 'Create a hello world page',
        'checks': ['Has h1 tag', 'Says hello'],
        'evaluation_url': 'https://httpbin.org/post',
        'attachments': []
    }
)

print(json.dumps(response.json(), indent=2))
"
```

### Health Check

```bash
curl http://localhost:5001/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "LLM Code Deployment API",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Troubleshooting

### Common Issues

1. **"GITHUB_TOKEN not configured"**
   - Ensure `.env` file exists and contains `GITHUB_TOKEN`
   - Verify token has correct permissions

2. **"Secret verification failed"**
   - Check `STUDENT_SECRET` in `.env` matches request
   - Ensure secret is not empty

3. **"Failed to enable GitHub Pages"**
   - Check repository exists
   - Verify repository is public
   - Wait a few minutes and check manually

4. **"LLM generation failed"**
   - Verify API key is valid
   - Check API quota/credits
   - System will fall back to template code

5. **"Import error: No module named 'flask'"**
   - Activate virtual environment
   - Run `pip install -r requirements.txt`

## License

MIT License - See generated repositories for full license text.

## Contributing

This is a project assignment. Modifications should align with project requirements.

## Support

For issues related to:
- **Project requirements**: Refer to README.md
- **Technical issues**: Check logs and error messages
- **API issues**: Verify credentials and quotas
- **GitHub issues**: Check token permissions

## Acknowledgments

Built for the TDS (Tools in Data Science) course project on LLM-based automated code deployment.

---

Generated: 2025-01-16
