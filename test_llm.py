#!/usr/bin/env python3
"""
Test script to debug LLM integration issues.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.llm_integration import generate_digest, generate_simple_digest
from src.config import OPENAI_API_KEY


def test_openai_client():
    """Test OpenAI client initialization."""
    print("Testing OpenAI Client Initialization")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        print(f"OpenAI API Key: {'Set' if OPENAI_API_KEY else 'Not set'}")
        
        if not OPENAI_API_KEY:
            print("No OpenAI API key found. Cannot test LLM integration.")
            return False
        
        # Test basic client initialization with custom HTTP client
        print("Initializing OpenAI client...")
        import httpx
        http_client = httpx.Client(timeout=30.0)
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=http_client
        )
        print("OpenAI client initialized successfully!")
        
        # Test a simple API call
        print("Testing simple API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, this is a test!'"}
            ],
            max_tokens=50
        )
        
        print(f"API Response: {response.choices[0].message.content}")
        print("OpenAI API test successful!")
        return True
        
    except Exception as e:
        print(f"OpenAI client error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_digest():
    """Test simple digest generation (no LLM)."""
    print("\nTesting Simple Digest Generation")
    print("=" * 50)
    
    try:
        # Create sample news data
        sample_news = [
            {
                "player_name": "Test Player",
                "team": "TEST",
                "position": "RB",
                "headline": "Test headline",
                "summary": "Test summary",
                "source": "test",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        digest = generate_simple_digest(sample_news)
        print("Simple digest generated successfully!")
        print("\nDigest preview:")
        print("-" * 30)
        print(digest[:200] + "..." if len(digest) > 200 else digest)
        return True
        
    except Exception as e:
        print(f"Simple digest error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_digest():
    """Test LLM digest generation."""
    print("\nTesting LLM Digest Generation")
    print("=" * 50)
    
    try:
        # Create sample news data
        sample_news = [
            {
                "player_name": "Taysom Hill",
                "team": "NO",
                "position": "TE",
                "headline": "Trending up: 459200 adds in last 24 hours",
                "summary": "Player is being added to 459200 rosters in the last 24 hours. Status: Active, Injury: None",
                "source": "sleeper",
                "timestamp": datetime.now().isoformat(),
                "trend_type": "add",
                "trend_count": 459200
            },
            {
                "player_name": "Justice Hill",
                "team": "BAL",
                "position": "RB",
                "headline": "Trending down: 123723 drops in last 24 hours",
                "summary": "Player is being dropped from 123723 rosters in the last 24 hours. Status: Active, Injury: None",
                "source": "sleeper",
                "timestamp": datetime.now().isoformat(),
                "trend_type": "drop",
                "trend_count": 123723
            }
        ]
        
        if not OPENAI_API_KEY:
            print("No OpenAI API key. Testing fallback to simple digest...")
            digest = generate_simple_digest(sample_news)
        else:
            print("Generating LLM-powered digest...")
            digest = generate_digest(sample_news)
        
        print("Digest generated successfully!")
        print("\nDigest preview:")
        print("-" * 30)
        print(digest[:500] + "..." if len(digest) > 500 else digest)
        return True
        
    except Exception as e:
        print(f"LLM digest error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all LLM tests."""
    print("LLM Integration Debug Test")
    print("=" * 60)
    
    tests = [
        ("OpenAI Client", test_openai_client),
        ("Simple Digest", test_simple_digest),
        ("LLM Digest", test_llm_digest)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_name}")
        print('='*60)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("All LLM tests passed!")
    else:
        print("Some LLM tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
