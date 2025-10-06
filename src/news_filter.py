"""News filtering functions for fantasy relevance."""

from typing import List, Dict, Any
from .config import FANTASY_KEYWORDS


def is_fantasy_relevant(news_item: Dict[str, Any]) -> bool:
    """
    Check if a news item is relevant for fantasy football.
    
    Args:
        news_item: Dictionary containing news item data
        
    Returns:
        True if the news item is fantasy relevant
    """
    # Sleeper trending data is always fantasy relevant
    if news_item.get("source") == "sleeper" and "trend_type" in news_item:
        return True
    
    # Combine headline and summary for keyword checking
    text_to_check = f"{news_item.get('headline', '')} {news_item.get('summary', '')}".lower()
    
    # Check if any fantasy keywords are present
    for keyword in FANTASY_KEYWORDS:
        if keyword.lower() in text_to_check:
            return True
    
    return False


def filter_relevant_news(news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter news items to only include fantasy-relevant ones.
    
    Args:
        news_items: List of news items to filter
        
    Returns:
        List of fantasy-relevant news items
    """
    relevant_news = []
    
    for item in news_items:
        if is_fantasy_relevant(item):
            relevant_news.append(item)
    
    print(f"Filtered {len(news_items)} news items down to {len(relevant_news)} fantasy-relevant items")
    return relevant_news


def categorize_news(news_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize news items by type (injuries, role changes, etc.).
    
    Args:
        news_items: List of fantasy-relevant news items
        
    Returns:
        Dictionary with categorized news items
    """
    categories = {
        "injuries": [],
        "role_changes": [],
        "transactions": [],
        "performance": [],
        "trending_up": [],
        "trending_down": [],
        "other": []
    }
    
    injury_keywords = ["injured", "injury", "out", "questionable", "doubtful", "probable", 
                      "hamstring", "knee", "ankle", "concussion", "shoulder", "back",
                      "limited", "full", "practice", "rehab", "recovery"]
    
    role_keywords = ["promoted", "demoted", "starter", "backup", "depth chart", "depth",
                    "snap count", "snaps", "targets", "carries", "touches"]
    
    transaction_keywords = ["signed", "released", "traded", "waived", "claimed",
                           "contract", "extension", "restructure"]
    
    performance_keywords = ["breakout", "breakout game", "career high", "season high",
                           "struggling", "struggles", "slumping", "slump",
                           "hot", "cold", "streak", "trending"]
    
    for item in news_items:
        # Handle Sleeper trending data
        if item.get("source") == "sleeper" and "trend_type" in item:
            if item["trend_type"] == "add":
                categories["trending_up"].append(item)
            elif item["trend_type"] == "drop":
                categories["trending_down"].append(item)
            continue
        
        # Handle other news sources
        text = f"{item.get('headline', '')} {item.get('summary', '')}".lower()
        
        if any(keyword in text for keyword in injury_keywords):
            categories["injuries"].append(item)
        elif any(keyword in text for keyword in role_keywords):
            categories["role_changes"].append(item)
        elif any(keyword in text for keyword in transaction_keywords):
            categories["transactions"].append(item)
        elif any(keyword in text for keyword in performance_keywords):
            categories["performance"].append(item)
        else:
            categories["other"].append(item)
    
    return categories
