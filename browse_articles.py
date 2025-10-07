#!/usr/bin/env python3
"""
Utility script to browse and search through scraped articles.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.web_scraper import FantasyProsScraper


def browse_articles():
    """Browse articles by section and date."""
    scraper = FantasyProsScraper()
    summary = scraper.get_scraping_summary()
    
    print("FantasyPros Articles Browser")
    print("=" * 40)
    print(f"Total articles: {summary['total_articles']}")
    
    if summary['total_articles'] == 0:
        print("No articles found. Run the scraper first!")
        return
    
    print(f"\nArticles by section:")
    for section, count in summary['sections'].items():
        print(f"  {section}: {count} articles")
    
    print(f"\nRecent articles (last 20):")
    recent_articles = summary['articles'][-20:]
    for i, article in enumerate(recent_articles, 1):
        print(f"{i:2d}. [{article['section']}] {article['title']} ({article['date']})")
        print(f"     Path: {article['path']}")
    
    # Group by date
    print(f"\nArticles by date:")
    articles_by_date = {}
    for article in summary['articles']:
        date = article['date']
        if date not in articles_by_date:
            articles_by_date[date] = []
        articles_by_date[date].append(article)
    
    for date in sorted(articles_by_date.keys(), reverse=True):
        print(f"\n{date}:")
        for article in articles_by_date[date]:
            print(f"  - [{article['section']}] {article['title']}")


def search_articles(search_term: str):
    """Search articles by title or content."""
    scraper = FantasyProsScraper()
    summary = scraper.get_scraping_summary()
    
    print(f"Searching for: '{search_term}'")
    print("=" * 40)
    
    matches = []
    for article in summary['articles']:
        if (search_term.lower() in article['title'].lower() or 
            search_term.lower() in article.get('author', '').lower()):
            matches.append(article)
    
    if matches:
        print(f"Found {len(matches)} matches:")
        for i, article in enumerate(matches, 1):
            print(f"{i:2d}. [{article['section']}] {article['title']} ({article['date']})")
            print(f"     Author: {article['author']}")
            print(f"     Path: {article['path']}")
    else:
        print("No matches found.")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
        search_articles(search_term)
    else:
        browse_articles()


if __name__ == "__main__":
    main()
