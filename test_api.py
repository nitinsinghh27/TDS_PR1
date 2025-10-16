"""
Simple test script for the LLM Code Deployment API
Run this to verify your setup is working correctly
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get('http://localhost:5001/')
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def test_deployment():
    """Test the deployment endpoint"""
    print("\nTesting deployment endpoint...")

    # Get credentials from environment
    email = os.getenv('STUDENT_EMAIL', 'test@example.com')
    secret = os.getenv('STUDENT_SECRET', 'test-secret')

    # Create test request with unique task name
    import time
    timestamp = int(time.time())

    payload = {
        "email": email,
        "secret": secret,
        "task": f"test-clock-app-{timestamp}",
        "round": 1,
        "nonce": "test-nonce-12345",
        "brief": "Create a simple digital clock that displays the current time and updates every second. Use a clean, modern design with a dark background.",
        "checks": [
            "Page has a title",
            "Clock displays current time",
            "Time updates automatically",
            "Has a dark background",
            "Design is centered and clean"
        ],
        "evaluation_url": "https://httpbin.org/post",
        "attachments": []
    }

    print(f"Sending request for task: {payload['task']}")

    try:
        response = requests.post(
            'http://localhost:5001/api/deploy',
            json=payload,
            timeout=300  # 5 minutes timeout
        )

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Deployment successful!")
            print(f"   Repository: {result.get('repo_url', 'N/A')}")
            print(f"   GitHub Pages: {result.get('pages_url', 'N/A')}")
            print(f"   Commit SHA: {result.get('commit_sha', 'N/A')}")
            print("\n   Wait 1-2 minutes, then visit the GitHub Pages URL to see your app!")
            return True
        else:
            print(f"❌ Deployment failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out (this might be normal for first-time setup)")
        print("   Check the server logs for progress")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        return False

def test_invalid_secret():
    """Test with an invalid secret"""
    print("\nTesting invalid secret handling...")

    payload = {
        "email": "test@example.com",
        "secret": "wrong-secret",
        "task": "test-task",
        "round": 1,
        "nonce": "test-nonce",
        "brief": "Test",
        "checks": [],
        "evaluation_url": "https://httpbin.org/post",
        "attachments": []
    }

    try:
        response = requests.post(
            'http://localhost:5001/api/deploy',
            json=payload,
            timeout=10
        )

        if response.status_code == 403:
            print("✅ Invalid secret correctly rejected")
            return True
        else:
            print(f"❌ Expected status 403, got {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_missing_fields():
    """Test with missing required fields"""
    print("\nTesting missing fields handling...")

    payload = {
        "email": "test@example.com",
        "secret": "test"
    }

    try:
        response = requests.post(
            'http://localhost:5001/api/deploy',
            json=payload,
            timeout=10
        )

        if response.status_code == 400:
            print("✅ Missing fields correctly rejected")
            return True
        else:
            print(f"❌ Expected status 400, got {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("LLM Code Deployment API - Test Suite")
    print("=" * 60)

    # Check environment
    email = os.getenv('STUDENT_EMAIL')
    secret = os.getenv('STUDENT_SECRET')
    github_token = os.getenv('GITHUB_TOKEN')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    aipipe_key = os.getenv('AIPIPE_API_KEY')

    print("\nEnvironment Check:")
    print(f"   STUDENT_EMAIL: {'✅ Set' if email else '❌ Not set'}")
    print(f"   STUDENT_SECRET: {'✅ Set' if secret else '❌ Not set'}")
    print(f"   GITHUB_TOKEN: {'✅ Set' if github_token else '❌ Not set'}")
    print(f"   ANTHROPIC_API_KEY: {'✅ Set' if anthropic_key else '⚠️  Not set'}")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key else '⚠️  Not set'}")
    print(f"   AIPIPE_API_KEY: {'✅ Set' if aipipe_key else '⚠️  Not set'}")

    if not (anthropic_key or openai_key or aipipe_key):
        print("\n⚠️  Warning: No LLM API key configured. Will use template generation.")
    elif aipipe_key:
        print("\n✅ Using AI Pipeline for code generation.")
    
    print("\nStarting tests...")
    print("-" * 60)

    results = {
        'health': test_health_check(),
        'invalid_secret': test_invalid_secret(),
        'missing_fields': test_missing_fields(),
    }

    # Only run full deployment test if basic tests pass
    if results['health']:
        print("\n⚠️  Running full deployment test (this may take 1-2 minutes)...")
        results['deployment'] = test_deployment()
    else:
        print("\n⚠️  Skipping deployment test - server not responding")
        results['deployment'] = False

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    total = len(results)
    passed = sum(results.values())

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your API is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == '__main__':
    main()
