"""
LLM-based code generation module
Generates application code based on the brief and requirements
"""
import logging
import os
import base64
import requests

logger = logging.getLogger(__name__)

# Configure API clients
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
AIPIPE_API_KEY = os.environ.get('AIPIPE_API_KEY', '')

def decode_attachment(attachment):
    """
    Decode a data URI attachment

    Args:
        attachment (dict): Attachment with 'name' and 'url' fields

    Returns:
        dict: Decoded attachment with content
    """
    try:
        url = attachment['url']
        if url.startswith('data:'):
            # Parse data URI: data:mime/type;base64,content
            header, encoded = url.split(',', 1)
            mime_type = header.split(':')[1].split(';')[0]

            # Decode base64 content
            content = base64.b64decode(encoded)

            # For text files, decode to string
            if mime_type.startswith('text/') or mime_type in ['application/json', 'application/javascript']:
                content = content.decode('utf-8')

            return {
                'name': attachment['name'],
                'mime_type': mime_type,
                'content': content
            }
    except Exception as e:
        logger.error(f"Failed to decode attachment {attachment.get('name', 'unknown')}: {str(e)}")
        return None

def generate_app_code(brief, checks, attachments):
    """
    Generate application code using LLM based on the brief

    Args:
        brief (str): Description of what the app should do
        checks (list): List of validation checks
        attachments (list): List of attachments (data URIs)

    Returns:
        dict: Generated code structure with HTML, CSS, JS, and README
    """
    logger.info("Starting code generation with LLM")

    # Decode attachments
    decoded_attachments = []
    for attachment in attachments:
        decoded = decode_attachment(attachment)
        if decoded:
            decoded_attachments.append(decoded)

    # Build the prompt for the LLM
    prompt = build_generation_prompt(brief, checks, decoded_attachments)

    # Try AI Pipeline first, then Anthropic, then OpenAI as fallback
    try:
        if AIPIPE_API_KEY:
            logger.info("Using AI Pipeline for code generation")
            code = generate_with_aipipe(prompt)
        elif ANTHROPIC_API_KEY:
            logger.info("Using Anthropic Claude for code generation")
            code = generate_with_anthropic(prompt)
        elif OPENAI_API_KEY:
            logger.info("Using OpenAI for code generation")
            code = generate_with_openai(prompt)
        else:
            logger.warning("No API keys configured, using template generation")
            code = generate_template_code(brief, checks, decoded_attachments)

        return code

    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}", exc_info=True)
        # Fallback to template
        return generate_template_code(brief, checks, decoded_attachments)

def build_generation_prompt(brief, checks, attachments):
    """Build a comprehensive prompt for the LLM"""

    attachments_info = ""
    if attachments:
        attachments_info = "\n\nATTACHMENTS:\n"
        for att in attachments:
            attachments_info += f"- {att['name']} ({att['mime_type']})\n"
            if isinstance(att['content'], str) and len(att['content']) < 1000:
                attachments_info += f"  Content: {att['content'][:500]}...\n"

    checks_info = ""
    if checks:
        checks_info = "\n\nVALIDATION CHECKS:\n" + "\n".join([f"- {check}" for check in checks])

    prompt = f"""Generate a complete, production-ready single-page web application based on the following requirements:

BRIEF:
{brief}
{attachments_info}
{checks_info}

REQUIREMENTS:
1. Create a single HTML file (index.html) with embedded CSS and JavaScript
2. Use modern, semantic HTML5
3. Include responsive design (mobile-friendly)
4. Use Bootstrap 5 from CDN for styling (unless specified otherwise)
5. Write clean, well-commented JavaScript
6. Handle errors gracefully
7. Make the page professional and user-friendly
8. Ensure all validation checks can pass
9. Include proper meta tags and title

OUTPUT FORMAT:
Provide the complete code in the following structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Your complete head section -->
</head>
<body>
    <!-- Your complete body content -->
</body>
</html>
```

Also provide a comprehensive README.md explaining:
- What the application does
- How to use it
- Technical implementation details
- How it satisfies the requirements

Generate ONLY production-ready, working code. No placeholders, no TODOs."""

    return prompt

def generate_with_aipipe(prompt):
    """Generate code using AI Pipeline (supports OpenAI, OpenRouter, Gemini)"""
    try:
        # AI Pipeline supports multiple providers
        # Using OpenRouter with a good model
        api_url = "https://aipipe.org/openrouter/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {AIPIPE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "anthropic/claude-3.5-sonnet",  # Good balance of quality and cost
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert web developer who creates clean, production-ready code."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }

        logger.info(f"Calling AI Pipeline API: {api_url}")
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)

        if response.status_code != 200:
            logger.error(f"AI Pipeline API returned status {response.status_code}: {response.text}")
            raise Exception(f"AI Pipeline API error: {response.status_code} - {response.text}")

        result = response.json()
        response_text = result['choices'][0]['message']['content']

        logger.info("Successfully generated code with AI Pipeline")

        # Parse the response to extract HTML and README
        return parse_llm_response(response_text)

    except Exception as e:
        logger.error(f"AI Pipeline API error: {str(e)}")
        raise

def generate_with_anthropic(prompt):
    """Generate code using Anthropic Claude"""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Parse the response to extract HTML and README
        return parse_llm_response(response_text)

    except Exception as e:
        logger.error(f"Anthropic API error: {str(e)}")
        raise

def generate_with_openai(prompt):
    """Generate code using OpenAI GPT"""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert web developer who creates clean, production-ready code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7
        )

        response_text = response.choices[0].message.content

        # Parse the response to extract HTML and README
        return parse_llm_response(response_text)

    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise

def parse_llm_response(response_text):
    """
    Parse LLM response to extract code files

    Args:
        response_text (str): Raw response from LLM

    Returns:
        dict: Parsed code structure
    """
    # Extract HTML code
    html_code = ""
    if "```html" in response_text:
        start = response_text.find("```html") + 7
        end = response_text.find("```", start)
        html_code = response_text[start:end].strip()
    elif "<!DOCTYPE html>" in response_text:
        start = response_text.find("<!DOCTYPE html>")
        # Find the closing </html>
        end = response_text.find("</html>", start) + 7
        html_code = response_text[start:end].strip()

    # Extract README
    readme_content = ""
    if "README" in response_text or "readme" in response_text:
        # Try to find markdown section
        if "```markdown" in response_text or "```md" in response_text:
            marker = "```markdown" if "```markdown" in response_text else "```md"
            start = response_text.find(marker) + len(marker)
            end = response_text.find("```", start)
            readme_content = response_text[start:end].strip()

    return {
        'index.html': html_code,
        'README.md': readme_content
    }

def generate_template_code(brief, checks, attachments):
    """
    Generate basic template code when LLM is not available

    Args:
        brief (str): Description of the app
        checks (list): Validation checks
        attachments (list): Decoded attachments

    Returns:
        dict: Basic code structure
    """
    logger.info("Generating template code")

    # Create a basic HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Application</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-top: 50px;
        }}
        .app-title {{
            color: #667eea;
            margin-bottom: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="app-title">Generated Application</h1>
        <div class="alert alert-info">
            <h5>Brief:</h5>
            <p>{brief}</p>
        </div>

        <div id="app-content">
            <p class="text-muted">Application implementation goes here.</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Application logic
        console.log('Application initialized');
    </script>
</body>
</html>"""

    readme_template = f"""# Generated Application

## Overview
This application was automatically generated based on the following brief:

{brief}

## Requirements
{chr(10).join(['- ' + check for check in checks]) if checks else 'No specific checks provided.'}

## Usage
1. Open `index.html` in a web browser
2. The application will load and execute automatically

## Technical Details
- Built with HTML5, CSS3, and JavaScript
- Uses Bootstrap 5 for styling
- Responsive design for all devices

## License
MIT License
"""

    return {
        'index.html': html_template,
        'README.md': readme_template
    }
