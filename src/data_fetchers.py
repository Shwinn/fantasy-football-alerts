"""Data fetching functions for Sleeper and FantasyPros APIs."""

import requests
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any
from .config import SLEEPER_BASE_URL, FANTASYPROS_BASE_URL, FANTASYPROS_API_KEY


def fetch_sleeper_news() -> List[Dict[str, Any]]:
    """
    Fetch trending players from Sleeper API.
    
    Returns:
        List of trending player data from Sleeper
    """
    try:
        print("Fetching Sleeper trending players...")
        
        # Get trending players (both adds and drops)
        trending_adds = fetch_sleeper_trending_players("add")
        trending_drops = fetch_sleeper_trending_players("drop")
        
        # Get player details for trending players
        player_details = fetch_sleeper_player_details()
        
        sleeper_news = []
        
        # Process trending adds
        for trend in trending_adds[:10]:  # Top 10 trending adds
            player_id = trend["player_id"]
            add_count = trend["count"]
            
            if player_id in player_details:
                player = player_details[player_id]
                sleeper_news.append({
                    "player_name": f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                    "team": player.get("team", "Unknown"),
                    "position": player.get("position", "Unknown"),
                    "headline": f"Trending up: {add_count} adds in last 24 hours",
                    "summary": f"Player is being added to {add_count} rosters in the last 24 hours. Status: {player.get('status', 'Unknown')}, Injury: {player.get('injury_status', 'None')}",
                    "source": "sleeper",
                    "timestamp": datetime.now().isoformat(),
                    "trend_type": "add",
                    "trend_count": add_count
                })
        
        # Process trending drops
        for trend in trending_drops[:5]:  # Top 5 trending drops
            player_id = trend["player_id"]
            drop_count = trend["count"]
            
            if player_id in player_details:
                player = player_details[player_id]
                sleeper_news.append({
                    "player_name": f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                    "team": player.get("team", "Unknown"),
                    "position": player.get("position", "Unknown"),
                    "headline": f"Trending down: {drop_count} drops in last 24 hours",
                    "summary": f"Player is being dropped from {drop_count} rosters in the last 24 hours. Status: {player.get('status', 'Unknown')}, Injury: {player.get('injury_status', 'None')}",
                    "source": "sleeper",
                    "timestamp": datetime.now().isoformat(),
                    "trend_type": "drop",
                    "trend_count": drop_count
                })
        
        print(f"Fetched {len(sleeper_news)} trending items from Sleeper")
        return sleeper_news
        
    except Exception as e:
        print(f"Error fetching Sleeper news: {e}")
        return []


def fetch_sleeper_trending_players(trend_type: str) -> List[Dict[str, Any]]:
    """
    Fetch trending players from Sleeper API.
    
    Args:
        trend_type: Either "add" or "drop"
        
    Returns:
        List of trending player data
    """
    try:
        url = f"{SLEEPER_BASE_URL}/players/nfl/trending/{trend_type}"
        params = {
            "lookback_hours": 24,
            "limit": 25
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        print(f"Error fetching Sleeper trending {trend_type}: {e}")
        return []


def fetch_sleeper_player_details() -> Dict[str, Any]:
    """
    Fetch all player details from Sleeper API.
    This is cached to avoid repeated calls to the large endpoint.
    
    Returns:
        Dictionary mapping player_id to player details
    """
    try:
        # Check if we have cached player data
        cache_file = "sleeper_players_cache.json"
        cache_time = 24 * 60 * 60  # 24 hours in seconds
        
        if os.path.exists(cache_file):
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age < cache_time:
                print("Using cached Sleeper player data...")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        print("Fetching fresh Sleeper player data...")
        url = f"{SLEEPER_BASE_URL}/players/nfl"
        
        response = requests.get(url)
        response.raise_for_status()
        
        player_data = response.json()
        
        # Cache the data
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(player_data, f, indent=2)
        
        print(f"Cached {len(player_data)} players")
        return player_data
        
    except Exception as e:
        print(f"Error fetching Sleeper player details: {e}")
        return {}


def fetch_fantasypros_news() -> List[Dict[str, Any]]:
    """
    Fetch NFL news from FantasyPros using web scraping.
    
    Returns:
        List of news items from FantasyPros
    """
    try:
        print("Fetching FantasyPros news via web scraping...")
        
        # Import web scraper
        from .web_scraper import FantasyProsScraper
        
        # Initialize scraper
        scraper = FantasyProsScraper()
        
        # First try to scrape new articles
        articles = scraper.scrape_fantasypros_articles(max_articles=1000)
        
        # If no new articles were scraped, load existing articles from files
        if not articles:
            print("No new articles scraped, loading existing articles...")
            articles = load_existing_scraped_articles()
        
        # Transform articles to our format
        fantasypros_news = []
        for article in articles:
            # Extract player names from title and content
            player_name = extract_player_name_from_article(article)
            
            # Use raw content directly
            summary = article.get("content", "")
            if not summary:
                # Fallback to truncated content
                summary = article.get("content", "")[:500] + "..." if len(article.get("content", "")) > 500 else article.get("content", "")
            
            fantasypros_news.append({
                "player_name": player_name,
                "team": "Unknown",  # Could be enhanced to extract from content
                "position": "Unknown",  # Could be enhanced to extract from content
                "headline": article.get("title", ""),
                "summary": summary,
                "source": "fantasypros_scraped",
                "timestamp": article.get("scraped_at", datetime.now().isoformat()),
                "url": article.get("url", ""),
                "author": article.get("author", "Unknown"),
                "content_length": len(article.get("content", ""))
            })
        
        print(f"Fetched {len(fantasypros_news)} items from FantasyPros via scraping")
        return fantasypros_news
        
    except Exception as e:
        print(f"Error fetching FantasyPros news via scraping: {e}")
        return []


def load_existing_scraped_articles() -> List[Dict[str, Any]]:
    """
    Load existing scraped articles from the filesystem.
    
    Returns:
        List of article dictionaries
    """
    import os
    import glob
    
    articles = []
    articles_dir = "scraped_articles"
    
    if not os.path.exists(articles_dir):
        return articles
    
    # Find all .txt files in the scraped_articles directory
    pattern = os.path.join(articles_dir, "**", "*.txt")
    txt_files = glob.glob(pattern, recursive=True)
    
    print(f"Found {len(txt_files)} existing article files")
    
    for filepath in txt_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the article file format
            lines = content.split('\n')
            if len(lines) < 8:
                continue
                
            # Extract metadata
            title = lines[0].replace('Title: ', '').strip()
            author = lines[1].replace('Author: ', '').strip()
            date = lines[2].replace('Date: ', '').strip()
            url = lines[3].replace('URL: ', '').strip()
            section = lines[4].replace('Section: ', '').strip()
            source_url = lines[5].replace('Source URL: ', '').strip()
            tags = lines[6].replace('Tags: ', '').strip()
            scraped_at = lines[7].replace('Scraped: ', '').strip()
            
            # Find content start (after the separator)
            content_start = content.find('==================================================')
            if content_start != -1:
                article_content = content[content_start + 52:].strip()  # Skip separator
            else:
                article_content = content
            
            # Only include articles with substantial content
            if len(article_content) > 100:
                articles.append({
                    'title': title,
                    'author': author,
                    'date': date,
                    'url': url,
                    'section': section,
                    'source_url': source_url,
                    'tags': tags.split(', ') if tags else [],
                    'content': article_content,
                    'scraped_at': scraped_at
                })
                
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue
    
    print(f"Loaded {len(articles)} existing articles")
    return articles


def extract_player_name_from_article(article: Dict[str, Any]) -> str:
    """
    Extract player name from article title and content.
    This is a simple implementation - could be enhanced with NLP.
    """
    title = article.get("title", "").lower()
    content = article.get("content", "").lower()
    
    # Common NFL player name patterns (simplified)
    # This could be enhanced with a comprehensive player database
    common_players = [
        "mahomes", "allen", "josh allen", "brady", "rodgers", "aaron rodgers",
        "mccaffrey", "cmc", "henry", "derrick henry", "cook", "dalvin cook",
        "adams", "davante adams", "hill", "tyreek hill", "kelce", "travis kelce",
        "kupp", "cooper kupp", "jefferson", "justin jefferson", "chase", "ja'marr chase"
    ]
    
    for player in common_players:
        if player in title or player in content:
            return player.title()
    
    return "Unknown"


def fetch_all_news() -> List[Dict[str, Any]]:
    """
    Fetch news from all sources and combine them.
    
    Returns:
        Combined list of news items from all sources
    """
    all_news = []
    
    # Fetch from Sleeper
    sleeper_news = fetch_sleeper_news()
    all_news.extend(sleeper_news)
    
    # Fetch from FantasyPros
    fantasypros_news = fetch_fantasypros_news()
    all_news.extend(fantasypros_news)
    
    print(f"Total news items fetched: {len(all_news)}")
    return all_news
