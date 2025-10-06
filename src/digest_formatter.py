"""Digest formatting and file writing functions."""

import os
from datetime import datetime
from typing import List, Dict, Any
from .config import OUTPUT_DIR, DIGEST_FILENAME_TEMPLATE


def ensure_output_directory():
    """Ensure the output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")


def write_digest(digest_content: str) -> str:
    """
    Write the digest content to a markdown file.
    
    Args:
        digest_content: The digest content as a string
        
    Returns:
        Path to the written file
    """
    ensure_output_directory()
    
    # Generate filename with today's date
    today = datetime.now()
    filename = DIGEST_FILENAME_TEMPLATE.format(date=today.strftime("%Y%m%d"))
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(digest_content)
        
        print(f"Digest written to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error writing digest: {e}")
        return ""


def format_news_summary(news_items: List[Dict[str, Any]]) -> str:
    """
    Format a simple summary of news items.
    
    Args:
        news_items: List of news items to summarize
        
    Returns:
        Formatted summary string
    """
    if not news_items:
        return "No news items to summarize."
    
    summary = f"Found {len(news_items)} fantasy-relevant news items:\n\n"
    
    for i, item in enumerate(news_items, 1):
        summary += f"{i}. **{item.get('player_name', 'Unknown')}** ({item.get('team', 'Unknown')}) - {item.get('headline', 'No headline')}\n"
        if item.get('summary'):
            summary += f"   *{item.get('summary')}*\n"
        summary += f"   *Source: {item.get('source', 'Unknown')}*\n\n"
    
    return summary
