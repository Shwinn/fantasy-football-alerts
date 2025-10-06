#!/usr/bin/env python3
"""
Test script to run the fantasy digest without API keys.
This will test the basic functionality with sample data.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.news_filter import filter_relevant_news, categorize_news
from src.llm_integration import generate_simple_digest
from src.digest_formatter import write_digest


def create_sample_news():
    """Create sample news data for testing."""
    return [
        {
            "player_name": "Justin Jefferson",
            "team": "MIN",
            "position": "WR",
            "headline": "Justin Jefferson injured in practice",
            "summary": "Star receiver suffered a hamstring injury during practice and is questionable for Sunday's game.",
            "source": "sleeper",
            "timestamp": datetime.now().isoformat()
        },
        {
            "player_name": "Tyjae Spears",
            "team": "TEN", 
            "position": "RB",
            "headline": "Tyjae Spears sees increased snaps",
            "summary": "With Derrick Henry limited, Spears saw 60% more snaps in practice and could be in line for more touches.",
            "source": "fantasypros",
            "timestamp": datetime.now().isoformat()
        },
        {
            "player_name": "Josh Downs",
            "team": "IND",
            "position": "WR", 
            "headline": "Josh Downs target share climbing",
            "summary": "The rookie receiver has seen his target share increase to 18% over the last three games, making him a solid PPR option.",
            "source": "fantasypros",
            "timestamp": datetime.now().isoformat()
        },
        {
            "player_name": "Saquon Barkley",
            "team": "NYG",
            "position": "RB",
            "headline": "Saquon Barkley limited in practice",
            "summary": "Barkley was limited in practice due to an ankle injury and is trending toward questionable for Sunday.",
            "source": "sleeper",
            "timestamp": datetime.now().isoformat()
        },
        {
            "player_name": "Random Player",
            "team": "RAND",
            "position": "QB",
            "headline": "Player attends charity event",
            "summary": "Player visited local hospital to meet with children.",
            "source": "sleeper",
            "timestamp": datetime.now().isoformat()
        }
    ]


def main():
    """Test the fantasy digest with sample data."""
    print("Testing NFL Fantasy Waiver Digest with Sample Data")
    print("=" * 60)
    
    try:
        # Create sample news
        print("Creating sample news data...")
        sample_news = create_sample_news()
        print(f"Created {len(sample_news)} sample news items")
        
        # Filter for fantasy relevance
        print("Filtering for fantasy-relevant news...")
        relevant_news = filter_relevant_news(sample_news)
        print(f"Found {len(relevant_news)} fantasy-relevant items")
        
        # Categorize news
        print("Categorizing news...")
        categories = categorize_news(relevant_news)
        for category, items in categories.items():
            if items:
                print(f"  {category}: {len(items)} items")
        
        # Generate simple digest
        print("Generating digest...")
        digest_content = generate_simple_digest(relevant_news)
        
        # Write digest
        print("Writing digest to file...")
        filepath = write_digest(digest_content)
        
        if filepath:
            print(f"Test completed successfully!")
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
