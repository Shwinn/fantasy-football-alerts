#!/usr/bin/env python3
"""
Isolated test for OpenAI client without any other imports.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def test_openai_isolated():
    """Test OpenAI client in complete isolation."""
    print("Testing OpenAI Client in Complete Isolation")
    print("=" * 50)
    
    if not OPENAI_API_KEY:
        print("No OpenAI API key found.")
        return False
    
    try:
        # Import only what we need
        from openai import OpenAI
        
        print("OpenAI imported successfully")
        
        # Try different initialization methods
        print("\nMethod 1: Basic initialization")
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            print("Basic initialization: SUCCESS")
        except Exception as e:
            print(f"Basic initialization: FAILED - {e}")
        
        print("\nMethod 2: With explicit timeout")
        try:
            client = OpenAI(api_key=OPENAI_API_KEY, timeout=30.0)
            print("Timeout initialization: SUCCESS")
        except Exception as e:
            print(f"Timeout initialization: FAILED - {e}")
        
        print("\nMethod 3: With custom HTTP client")
        try:
            import httpx
            http_client = httpx.Client(timeout=30.0)
            client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
            print("Custom HTTP client: SUCCESS")
        except Exception as e:
            print(f"Custom HTTP client: FAILED - {e}")
        
        print("\nMethod 4: Check environment variables")
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        for var in proxy_vars:
            value = os.environ.get(var, 'Not set')
            print(f"  {var}: {value}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_openai_isolated()
