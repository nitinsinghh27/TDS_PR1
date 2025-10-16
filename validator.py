"""
Request validation and secret verification module
"""
import logging

logger = logging.getLogger(__name__)

def validate_request(payload):
    """
    Validate the incoming request payload structure

    Args:
        payload (dict): The JSON payload from the request

    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['email', 'secret', 'task', 'round', 'nonce', 'brief', 'evaluation_url']

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    # Validate email format
    email = payload['email']
    if '@' not in email or '.' not in email.split('@')[-1]:
        return False, "Invalid email format"

    # Validate round number
    round_num = payload['round']
    if not isinstance(round_num, int) or round_num < 1:
        return False, "Round must be a positive integer"

    # Validate task name
    task = payload['task']
    if not isinstance(task, str) or len(task) == 0:
        return False, "Task must be a non-empty string"

    # Validate nonce
    nonce = payload['nonce']
    if not isinstance(nonce, str) or len(nonce) == 0:
        return False, "Nonce must be a non-empty string"

    # Validate brief
    brief = payload['brief']
    if not isinstance(brief, str) or len(brief) == 0:
        return False, "Brief must be a non-empty string"

    # Validate evaluation_url
    evaluation_url = payload['evaluation_url']
    if not isinstance(evaluation_url, str) or not evaluation_url.startswith('http'):
        return False, "Evaluation URL must be a valid HTTP(S) URL"

    # Validate checks (optional but should be a list if present)
    if 'checks' in payload and not isinstance(payload['checks'], list):
        return False, "Checks must be a list"

    # Validate attachments (optional but should be a list if present)
    if 'attachments' in payload:
        if not isinstance(payload['attachments'], list):
            return False, "Attachments must be a list"

        for idx, attachment in enumerate(payload['attachments']):
            if not isinstance(attachment, dict):
                return False, f"Attachment {idx} must be a dictionary"
            if 'name' not in attachment or 'url' not in attachment:
                return False, f"Attachment {idx} must have 'name' and 'url' fields"

    logger.info("Request validation successful")
    return True, ""

def verify_secret(provided_secret, expected_secret):
    """
    Verify that the provided secret matches the expected secret

    Args:
        provided_secret (str): The secret from the request
        expected_secret (str): The expected secret

    Returns:
        bool: True if secrets match, False otherwise
    """
    if not expected_secret:
        logger.warning("Expected secret is not configured")
        # In development, you might want to allow requests without secret
        # return True
        # In production, always require a secret:
        return False

    if provided_secret == expected_secret:
        logger.info("Secret verification successful")
        return True

    logger.warning("Secret verification failed")
    return False
