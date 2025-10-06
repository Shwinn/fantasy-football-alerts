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
    Fetch NFL news from FantasyPros API.
    
    Returns:
        List of news items from FantasyPros
    """
    try:
        print("Fetching FantasyPros news...")
        
        # FantasyPros API endpoint for news
        url = f"{FANTASYPROS_BASE_URL}/news"
        
        headers = {
            "x-api-key": FANTASYPROS_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Transform FantasyPros data to our format
        fantasypros_news = []
        for item in data.get("news", []):
            fantasypros_news.append({
                "player_name": item.get("player_name", "Unknown"),
                "team": item.get("team", "Unknown"),
                "position": item.get("position", "Unknown"),
                "headline": item.get("headline", ""),
                "summary": item.get("summary", ""),
                "source": "fantasypros",
                "timestamp": item.get("timestamp", datetime.now().isoformat())
            })
        
        print(f"Fetched {len(fantasypros_news)} items from FantasyPros")
        return fantasypros_news
        
    except Exception as e:
        print(f"Error fetching FantasyPros news: {e}")
        return []


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
