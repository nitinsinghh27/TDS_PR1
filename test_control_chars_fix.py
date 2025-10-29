#!/usr/bin/env python3
"""
Test script to demonstrate the control character sanitization fix
This proves the bug has been resolved and the system now handles
briefs with newlines, tabs, and other control characters.
"""

import sys
from github_manager import sanitize_description

def test_control_characters():
    """Test that control characters are properly sanitized"""

    test_cases = [
        {
            "name": "Newlines in brief",
            "input": "Create a captcha solver\nthat handles URL parameters\nand displays results",
            "should_not_contain": ["\n"]
        },
        {
            "name": "Tabs in brief",
            "input": "Display\tdata\tfrom\tCSV\tfile",
            "should_not_contain": ["\t"]
        },
        {
            "name": "Multiple control characters",
            "input": "Line 1\nLine 2\r\nLine 3\tTabbed\x00Null",
            "should_not_contain": ["\n", "\r", "\t", "\x00"]
        },
        {
            "name": "Form feed and vertical tab",
            "input": "Text with\fform feed\vand vertical tab",
            "should_not_contain": ["\f", "\v"]
        },
        {
            "name": "Escape and backspace",
            "input": "Text\x1bwith\x08escape",
            "should_not_contain": ["\x1b", "\x08"]
        }
    ]

    print("Testing Control Character Sanitization")
    print("=" * 60)

    all_passed = True

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Input (repr): {repr(test['input'])}")

        # Sanitize the description
        result = sanitize_description(test['input'])
        print(f"Output (repr): {repr(result)}")

        # Check that control characters were removed
        passed = True
        for bad_char in test['should_not_contain']:
            if bad_char in result:
                print(f"  FAILED: Still contains {repr(bad_char)}")
                passed = False
                all_passed = False

        if passed:
            print(f"  PASSED: All control characters removed")

    print("\n" + "=" * 60)

    # Test with the actual GitHub API format
    print("\nTest with GitHub API description format:")
    brief_with_newlines = """Create a web application that:
- Fetches data from an API
- Displays it in a table
- Allows filtering by category"""

    description = f"Auto-generated application: {brief_with_newlines[:100]}"
    print(f"Before: {repr(description)}")

    sanitized = sanitize_description(description)
    print(f"After: {repr(sanitized)}")

    if "\n" not in sanitized and "\r" not in sanitized and "\t" not in sanitized:
        print("PASSED: Ready for GitHub API")
    else:
        print("FAILED: Still contains control characters")
        all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("\nALL TESTS PASSED!")
        print("The fix successfully handles control characters in briefs.")
        return 0
    else:
        print("\nSOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(test_control_characters())
