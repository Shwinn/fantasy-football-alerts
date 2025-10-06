#!/usr/bin/env python3
"""
NFL Fantasy Waiver Digest - Main Script

This script aggregates NFL news from Sleeper and FantasyPros,
filters for fantasy-relevant items, and generates a daily digest.
"""

import sys
import os
from datetime import datetime

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetchers import fetch_all_news
from src.news_filter import filter_relevant_news, categorize_news
from src.llm_integration import generate_digest, generate_simple_digest
from src.digest_formatter import write_digest
from src.config import OPENAI_API_KEY


def main():
    """Main function to run the fantasy digest generation."""
    print("NFL Fantasy Waiver Digest Generator")
    print("=" * 50)
    
    # Check if OpenAI API key is configured
    if not OPENAI_API_KEY:
        print("Warning: OpenAI API key not found. Will generate simple digest without LLM insights.")
        print("   To get LLM-powered insights, add your OpenAI API key to the .env file.")
        print()
    
    try:
        # Step 1: Fetch news from all sources
        print("Fetching news from all sources...")
        all_news = fetch_all_news()
        
        if not all_news:
            print("No news items found. Exiting.")
            return
        
        # Step 2: Filter for fantasy relevance
        print("Filtering for fantasy-relevant news...")
        relevant_news = filter_relevant_news(all_news)
        
        if not relevant_news:
            print("No fantasy-relevant news found. Exiting.")
            return
        
        # Step 3: Generate digest
        print("Generating digest...")
        if OPENAI_API_KEY:
            digest_content = generate_digest(relevant_news)
        else:
            digest_content = generate_simple_digest(relevant_news)
        
        # Step 4: Write digest to file
        print("Writing digest to file...")
        filepath = write_digest(digest_content)
        
        if filepath:
            print(f"Digest successfully generated: {filepath}")
        else:
            print("Failed to write digest file.")
            
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
