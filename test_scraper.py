#!/usr/bin/env python3
"""
Test script for FantasyPros web scraper.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.web_scraper import FantasyProsScraper


def main():
    """Test the web scraper."""
    print("FantasyPros Web Scraper Test")
    print("=" * 40)
    
    # Initialize scraper
    scraper = FantasyProsScraper()
    
    # Test with a small number of articles first
    print("Starting test scrape (max 5 articles)...")
    articles = scraper.scrape_fantasypros_articles(max_articles=5)
    
    if articles:
        print(f"\nSuccessfully scraped {len(articles)} articles!")
        
        # Show summary
        summary = scraper.get_scraping_summary()
        print(f"\nScraping Summary:")
        print(f"Total articles: {summary['total_articles']}")
        
        print(f"\nArticles by section:")
        for section, count in summary['sections'].items():
            print(f"  {section}: {count} articles")
        
        print(f"\nRecent articles:")
        for article in summary['articles'][-10:]:  # Show last 10
            print(f"- [{article['section']}] {article['title']} ({article['date']})")
        
        # Show deduplication stats
        dedup_stats = scraper.get_deduplication_stats()
        print(f"\nDeduplication Stats:")
        print(f"  Total tracked URLs: {dedup_stats['total_scraped_urls']}")
        print(f"  Tracking file: {dedup_stats['scraped_urls_file']}")
    else:
        print("No articles were scraped successfully.")


if __name__ == "__main__":
    main()
