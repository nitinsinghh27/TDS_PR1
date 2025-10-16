"""
Main API server for LLM Code Deployment System
Handles POST requests to build and deploy applications
"""
from flask import Flask, request, jsonify
import os
import logging
from datetime import datetime
from validator import validate_request, verify_secret
from code_generator import generate_app_code
from github_manager import create_and_deploy_repo
from evaluator import notify_evaluation_api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Store the secret (in production, use environment variables)
STUDENT_SECRET = os.environ.get('STUDENT_SECRET', '')
STUDENT_EMAIL = os.environ.get('STUDENT_EMAIL', '')

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'LLM Code Deployment API',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/deploy', methods=['POST'])
def deploy():
    """
    Main endpoint to receive deployment requests
    Validates request, generates code, creates repo, and notifies evaluation API
    """
    try:
        # Get JSON payload
        payload = request.get_json()

        if not payload:
            return jsonify({'error': 'No JSON payload provided'}), 400

        logger.info(f"Received deployment request for task: {payload.get('task', 'unknown')}")

        # Step 1: Validate request structure
        is_valid, error_message = validate_request(payload)
        if not is_valid:
            logger.error(f"Request validation failed: {error_message}")
            return jsonify({'error': error_message}), 400

        # Step 2: Verify secret
        if not verify_secret(payload.get('secret', ''), STUDENT_SECRET):
            logger.error("Secret verification failed")
            return jsonify({'error': 'Invalid secret'}), 403

        # Step 3: Send immediate 200 response
        logger.info("Request validated successfully")

        # Extract request details
        email = payload['email']
        task = payload['task']
        round_num = payload['round']
        nonce = payload['nonce']
        brief = payload['brief']
        checks = payload.get('checks', [])
        evaluation_url = payload['evaluation_url']
        attachments = payload.get('attachments', [])

        # Step 4: Generate app code using LLM
        logger.info("Generating application code...")
        app_code = generate_app_code(brief, checks, attachments)

        # Step 5: Create GitHub repo and deploy
        logger.info("Creating GitHub repository and deploying...")
        repo_info = create_and_deploy_repo(
            task_name=task,
            app_code=app_code,
            brief=brief,
            checks=checks
        )

        # Step 6: Notify evaluation API
        logger.info("Notifying evaluation API...")
        notify_result = notify_evaluation_api(
            evaluation_url=evaluation_url,
            email=email,
            task=task,
            round_num=round_num,
            nonce=nonce,
            repo_url=repo_info['repo_url'],
            commit_sha=repo_info['commit_sha'],
            pages_url=repo_info['pages_url']
        )

        if notify_result['success']:
            logger.info(f"Deployment completed successfully for task: {task}")
            return jsonify({
                'status': 'success',
                'message': 'Application deployed successfully',
                'repo_url': repo_info['repo_url'],
                'pages_url': repo_info['pages_url'],
                'commit_sha': repo_info['commit_sha']
            }), 200
        else:
            logger.error(f"Failed to notify evaluation API: {notify_result['error']}")
            return jsonify({
                'status': 'partial_success',
                'message': 'App deployed but evaluation notification failed',
                'repo_url': repo_info['repo_url'],
                'pages_url': repo_info['pages_url'],
                'error': notify_result['error']
            }), 200

    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not STUDENT_SECRET:
        logger.warning("STUDENT_SECRET not set in environment variables")
    if not STUDENT_EMAIL:
        logger.warning("STUDENT_EMAIL not set in environment variables")

    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
