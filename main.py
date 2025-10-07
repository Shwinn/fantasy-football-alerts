#!/usr/bin/env python3
"""
NFL Fantasy Waiver Digest - Main Script

This script aggregates NFL news from Sleeper and FantasyPros,
filters for fantasy-relevant items, and generates a daily digest.

Usage:
    python main.py                    # Use LLM if API key available, otherwise simple digest
    python main.py --no-llm          # Force simple digest (no LLM API calls)
    python main.py --help            # Show this help message
"""

import sys
import os
import argparse
from datetime import datetime

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetchers import fetch_all_news
from src.news_filter import filter_relevant_news, categorize_news
from src.llm_integration import generate_digest, generate_simple_digest
from src.digest_formatter import write_digest
from src.config import OPENAI_API_KEY


def main():
    """Main function to run the fantasy digest generation with web scraping."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate NFL Fantasy Waiver Digest with web scraping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Use LLM if API key available, otherwise simple digest
  python main.py --no-llm          # Force simple digest (no LLM API calls)
  python main.py --help            # Show this help message
        """
    )
    
    parser.add_argument(
        '--no-llm', 
        action='store_true', 
        help='Force simple digest generation without LLM API calls (saves API costs)'
    )
    
    args = parser.parse_args()
    
    print("NFL Fantasy Waiver Digest Generator (with Web Scraping)")
    print("=" * 60)
    
    # Determine whether to use LLM
    use_llm = OPENAI_API_KEY and not args.no_llm
    
    if args.no_llm:
        print("Mode: Simple digest (LLM disabled by --no-llm flag)")
    elif not OPENAI_API_KEY:
        print("Mode: Simple digest (no OpenAI API key found)")
        print("   To get LLM-powered insights, add your OpenAI API key to the .env file.")
    else:
        print("Mode: LLM-powered digest")
    
    print()
    
    try:
        # Step 1: Fetch news from all sources (including web scraping)
        print("Fetching news from all sources (including FantasyPros web scraping)...")
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
        if use_llm:
            print("  Using LLM for enhanced insights...")
            digest_content = generate_digest(relevant_news)
        else:
            print("  Using simple digest format...")
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
