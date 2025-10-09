"""LLM integration for generating fantasy insights and recommendations."""

import json
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
from .config import OPENAI_API_KEY, LLM_TIMEOUT_SECONDS


def generate_digest(news_items: List[Dict[str, Any]]) -> str:
    """
    Generate a fantasy digest using OpenAI's API.
    
    Args:
        news_items: List of fantasy-relevant news items (already filtered to today's date)
        
    Returns:
        Generated digest as markdown string
    """
    try:
        # Create a custom HTTP client to avoid proxy conflicts
        import httpx
        
        # Create a clean HTTP client without proxy settings
        http_client = httpx.Client(timeout=LLM_TIMEOUT_SECONDS)
        
        # Initialize OpenAI client with custom HTTP client
        client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
        
        # Prepare the news items for the LLM
        news_json = json.dumps(news_items, indent=2)
        
        system_prompt = """You are an expert fantasy football analyst. Summarize today's NFL player news to identify potential waiver pickups and role changes.

Focus on:
1. Key injuries and their fantasy impact
2. Role changes and depth chart movements  
3. Performance trends and breakout candidates
4. Specific waiver wire recommendations with reasoning
5. Players to consider dropping

Be concise but informative. Use emojis to make it engaging."""
        
        user_prompt = f"""Here are today's news items (JSON):

{news_json}

Please:
1. Summarize key takeaways (Injuries, Role Changes, Emerging Players).
2. Suggest 3–5 waiver pickups with reasoning.
3. Mention any players to consider dropping.
4. Output in Markdown format with clear sections.
5. Include the date in the title (use today's date)."""
        
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating digest with LLM: {e}")
        # If it's a quota error, fall back to simple digest
        if "quota" in str(e).lower() or "429" in str(e):
            print("OpenAI quota exceeded. Falling back to simple digest...")
            return generate_simple_digest(news_items)
        # If it's a timeout error, fall back to simple digest
        elif "timeout" in str(e).lower() or "timed out" in str(e).lower():
            print(f"LLM request timed out after {LLM_TIMEOUT_SECONDS} seconds. Falling back to simple digest...")
            return generate_simple_digest(news_items)
        return f"# Error Generating Digest\n\nThere was an error generating the digest: {e}"


def generate_simple_digest(news_items: List[Dict[str, Any]]) -> str:
    """
    Generate a simple digest without LLM (fallback).
    
    Args:
        news_items: List of fantasy-relevant news items (already filtered to today's date)
        
    Returns:
        Simple digest as markdown string
    """
    date_str = datetime.now().strftime("%B %d, %Y")
    
    digest = f"# NFL Daily Fantasy Digest — {date_str}\n\n"
    
    if not news_items:
        digest += "No fantasy-relevant news found today.\n"
        return digest
    
    # Group by source and trend type
    sleeper_adds = [item for item in news_items if item.get("source") == "sleeper" and item.get("trend_type") == "add"]
    sleeper_drops = [item for item in news_items if item.get("source") == "sleeper" and item.get("trend_type") == "drop"]
    other_sleeper = [item for item in news_items if item.get("source") == "sleeper" and "trend_type" not in item]
    fantasypros_items = [item for item in news_items if item.get("source") == "fantasypros_scraped"]
    
    if sleeper_adds:
        digest += "## Trending Up (Sleeper)\n\n"
        for item in sleeper_adds:
            trend_count = item.get("trend_count", 0)
            digest += f"- **{item.get('player_name', 'Unknown')}** ({item.get('team', 'Unknown')}) - {trend_count} adds in 24h\n"
        digest += "\n"
    
    if sleeper_drops:
        digest += "## Trending Down (Sleeper)\n\n"
        for item in sleeper_drops:
            trend_count = item.get("trend_count", 0)
            digest += f"- **{item.get('player_name', 'Unknown')}** ({item.get('team', 'Unknown')}) - {trend_count} drops in 24h\n"
        digest += "\n"
    
    if other_sleeper:
        digest += "## Other Sleeper News\n\n"
        for item in other_sleeper:
            digest += f"- **{item.get('player_name', 'Unknown')}** ({item.get('team', 'Unknown')}) - {item.get('headline', 'No headline')}\n"
        digest += "\n"
    
    if fantasypros_items:
        digest += "## FantasyPros News\n\n"
        for item in fantasypros_items:
            # Show processed summary if available, otherwise headline
            content = item.get('summary', item.get('headline', 'No headline'))
            # Truncate very long summaries
            if len(content) > 200:
                content = content[:200] + "..."
            digest += f"- **{item.get('player_name', 'Unknown')}** ({item.get('team', 'Unknown')}) - {content}\n"
        digest += "\n"
    
    digest += "*(Data aggregated from Sleeper + FantasyPros)*\n"
    
    return digest
