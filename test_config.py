#!/usr/bin/env python3
"""
Test configuration and environment setup.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import (
    SLEEPER_BASE_URL,
    FANTASYPROS_BASE_URL,
    FANTASYPROS_API_KEY,
    OPENAI_API_KEY,
    FANTASY_KEYWORDS
)


def test_config():
    """Test configuration values."""
    print("Configuration Test")
    print("=" * 40)
    
    print(f"Sleeper Base URL: {SLEEPER_BASE_URL}")
    print(f"FantasyPros Base URL: {FANTASYPROS_BASE_URL}")
    print(f"FantasyPros API Key: {'Set' if FANTASYPROS_API_KEY else 'Not set'}")
    print(f"OpenAI API Key: {'Set' if OPENAI_API_KEY else 'Not set'}")
    print(f"Fantasy Keywords: {len(FANTASY_KEYWORDS)} keywords loaded")
    
    print(f"\nFirst 10 keywords: {FANTASY_KEYWORDS[:10]}")
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"\n.env file found")
        with open(env_file, 'r') as f:
            lines = f.readlines()
            print(f"   {len(lines)} lines in .env file")
    else:
        print(f"\n.env file not found")
        print("   Create one from env_example.txt if you want to set API keys")


if __name__ == "__main__":
    test_config()
