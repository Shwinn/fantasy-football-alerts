#!/usr/bin/env python3
"""
Script to run the FantasyPros web scraper with more articles.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.web_scraper import FantasyProsScraper


def main():
    """Run the web scraper with more articles."""
    print("FantasyPros Web Scraper - Full Run")
    print("=" * 50)
    
    # Initialize scraper
    scraper = FantasyProsScraper()
    
    # Ask user how many articles to scrape
    try:
        max_articles = int(input("How many articles would you like to scrape? (default: 20): ") or "20")
    except ValueError:
        max_articles = 20
    
    print(f"\nStarting scrape for {max_articles} articles...")
    articles = scraper.scrape_fantasypros_articles(max_articles=max_articles)
    
    if articles:
        print(f"\n[SUCCESS] Successfully scraped {len(articles)} articles!")
        
        # Show summary
        summary = scraper.get_scraping_summary()
        print(f"\nScraping Summary:")
        print(f"Total articles: {summary['total_articles']}")
        
        print(f"\nArticles saved to: {scraper.articles_dir}")
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
        print("[ERROR] No articles were scraped successfully.")


if __name__ == "__main__":
    main()
