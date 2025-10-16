"""
Evaluation API notification module
Sends repository details to the evaluation endpoint
"""
import logging
import requests
import time

logger = logging.getLogger(__name__)

MAX_RETRIES = 5
RETRY_DELAYS = [1, 2, 4, 8, 16]  # Exponential backoff in seconds

def notify_evaluation_api(evaluation_url, email, task, round_num, nonce, repo_url, commit_sha, pages_url):
    """
    Send repository details to the evaluation API with retry logic

    Args:
        evaluation_url (str): URL to send the notification to
        email (str): Student email
        task (str): Task identifier
        round_num (int): Round number
        nonce (str): Unique nonce from the request
        repo_url (str): GitHub repository URL
        commit_sha (str): Commit SHA
        pages_url (str): GitHub Pages URL

    Returns:
        dict: Result with 'success' boolean and optional 'error' message
    """
    payload = {
        "email": email,
        "task": task,
        "round": round_num,
        "nonce": nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }

    headers = {
        "Content-Type": "application/json"
    }

    logger.info(f"Notifying evaluation API: {evaluation_url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                evaluation_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                logger.info(f"Successfully notified evaluation API (attempt {attempt + 1})")
                return {
                    'success': True,
                    'response': response.json() if response.content else {}
                }
            else:
                logger.warning(
                    f"Evaluation API returned status {response.status_code} "
                    f"(attempt {attempt + 1}/{MAX_RETRIES}): {response.text}"
                )

                # If we haven't exhausted retries, wait and try again
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[attempt]
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    return {
                        'success': False,
                        'error': f"Evaluation API returned status {response.status_code}: {response.text}"
                    }

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return {
                    'success': False,
                    'error': "Request timeout after multiple retries"
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return {
                    'success': False,
                    'error': f"Request failed: {str(e)}"
                }

        except Exception as e:
            logger.error(f"Unexpected error (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[attempt]
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return {
                    'success': False,
                    'error': f"Unexpected error: {str(e)}"
                }

    return {
        'success': False,
        'error': "Failed after maximum retries"
    }

def verify_evaluation_response(response):
    """
    Verify that the evaluation API response is valid

    Args:
        response: requests.Response object

    Returns:
        bool: True if response is valid
    """
    if response.status_code != 200:
        return False

    # Check if response has JSON content
    try:
        response.json()
        return True
    except ValueError:
        # Empty response is also acceptable
        return True
