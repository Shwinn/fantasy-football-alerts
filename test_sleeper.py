#!/usr/bin/env python3
"""
Test script to see actual Sleeper trending data.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetchers import fetch_sleeper_news
from src.news_filter import filter_relevant_news, categorize_news
from src.llm_integration import generate_simple_digest
from src.digest_formatter import write_digest


def main():
    """Test the Sleeper API with real data."""
    print("Testing Sleeper API with Real Data")
    print("=" * 50)
    
    try:
        # Fetch real Sleeper data
        print("Fetching real Sleeper trending data...")
        sleeper_news = fetch_sleeper_news()
        
        if not sleeper_news:
            print("No Sleeper data found.")
            return
        
        print(f"Found {len(sleeper_news)} trending items from Sleeper")
        
        # Show first few items
        print("\nFirst 5 trending items:")
        for i, item in enumerate(sleeper_news[:5]):
            print(f"{i+1}. {item['player_name']} ({item['team']}) - {item['headline']}")
            print(f"   Trend: {item.get('trend_type', 'unknown')} - {item.get('trend_count', 0)} count")
            print(f"   Summary: {item['summary']}")
            print()
        
        # Filter and categorize
        print("Filtering and categorizing...")
        relevant_news = filter_relevant_news(sleeper_news)
        categories = categorize_news(relevant_news)
        
        print("Categories:")
        for category, items in categories.items():
            if items:
                print(f"  {category}: {len(items)} items")
        
        # Generate simple digest
        print("\nGenerating digest...")
        digest_content = generate_simple_digest(relevant_news)
        
        # Write digest
        print("Writing digest...")
        filepath = write_digest(digest_content)
        
        if filepath:
            print(f"Digest written to: {filepath}")
            print("\n" + "="*60)
            print("DIGEST PREVIEW:")
            print("="*60)
            print(digest_content)
        else:
            print("Failed to write digest file.")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
