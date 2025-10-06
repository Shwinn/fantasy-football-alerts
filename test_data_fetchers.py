#!/usr/bin/env python3
"""
Isolated testing script for data fetching functions.
This allows you to test each API integration separately.
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetchers import (
    fetch_sleeper_news,
    fetch_sleeper_trending_players,
    fetch_sleeper_player_details,
    fetch_fantasypros_news,
    fetch_all_news
)


def test_sleeper_trending_adds():
    """Test fetching trending adds from Sleeper."""
    print("=" * 60)
    print("TESTING: Sleeper Trending Adds")
    print("=" * 60)
    
    try:
        trending_adds = fetch_sleeper_trending_players("add")
        
        if not trending_adds:
            print("No trending adds found")
            return False
        
        print(f"Found {len(trending_adds)} trending adds")
        print("\nTop 5 trending adds:")
        for i, trend in enumerate(trending_adds[:5]):
            print(f"  {i+1}. Player ID: {trend['player_id']} - Count: {trend['count']}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_sleeper_trending_drops():
    """Test fetching trending drops from Sleeper."""
    print("\n" + "=" * 60)
    print("TESTING: Sleeper Trending Drops")
    print("=" * 60)
    
    try:
        trending_drops = fetch_sleeper_trending_players("drop")
        
        if not trending_drops:
            print("No trending drops found")
            return False
        
        print(f"Found {len(trending_drops)} trending drops")
        print("\nTop 5 trending drops:")
        for i, trend in enumerate(trending_drops[:5]):
            print(f"  {i+1}. Player ID: {trend['player_id']} - Count: {trend['count']}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_sleeper_player_details():
    """Test fetching player details from Sleeper."""
    print("\n" + "=" * 60)
    print("TESTING: Sleeper Player Details")
    print("=" * 60)
    
    try:
        player_details = fetch_sleeper_player_details()
        
        if not player_details:
            print("No player details found")
            return False
        
        print(f"Found {len(player_details)} players")
        
        # Show sample player details
        sample_player_id = list(player_details.keys())[0]
        sample_player = player_details[sample_player_id]
        
        print(f"\nSample player (ID: {sample_player_id}):")
        print(f"  Name: {sample_player.get('first_name', '')} {sample_player.get('last_name', '')}")
        print(f"  Team: {sample_player.get('team', 'Unknown')}")
        print(f"  Position: {sample_player.get('position', 'Unknown')}")
        print(f"  Status: {sample_player.get('status', 'Unknown')}")
        print(f"  Injury: {sample_player.get('injury_status', 'None')}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_sleeper_news():
    """Test the complete Sleeper news fetching."""
    print("\n" + "=" * 60)
    print("TESTING: Complete Sleeper News")
    print("=" * 60)
    
    try:
        sleeper_news = fetch_sleeper_news()
        
        if not sleeper_news:
            print("No Sleeper news found")
            return False
        
        print(f"Found {len(sleeper_news)} Sleeper news items")
        
        # Show breakdown by trend type
        adds = [item for item in sleeper_news if item.get('trend_type') == 'add']
        drops = [item for item in sleeper_news if item.get('trend_type') == 'drop']
        
        print(f"  - Trending up: {len(adds)} items")
        print(f"  - Trending down: {len(drops)} items")
        
        print("\nTop 3 trending up:")
        for i, item in enumerate(adds[:3]):
            print(f"  {i+1}. {item['player_name']} ({item['team']}) - {item['trend_count']} adds")
        
        print("\nTop 3 trending down:")
        for i, item in enumerate(drops[:3]):
            print(f"  {i+1}. {item['player_name']} ({item['team']}) - {item['trend_count']} drops")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_fantasypros_news():
    """Test FantasyPros news fetching."""
    print("\n" + "=" * 60)
    print("TESTING: FantasyPros News")
    print("=" * 60)
    
    try:
        fantasypros_news = fetch_fantasypros_news()
        
        if not fantasypros_news:
            print("No FantasyPros news found (this is expected if no API key)")
            return True  # Not an error, just no data
        
        print(f"Found {len(fantasypros_news)} FantasyPros news items")
        
        print("\nFirst 3 FantasyPros items:")
        for i, item in enumerate(fantasypros_news[:3]):
            print(f"  {i+1}. {item['player_name']} ({item['team']}) - {item['headline']}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_all_news():
    """Test fetching from all sources."""
    print("\n" + "=" * 60)
    print("TESTING: All News Sources")
    print("=" * 60)
    
    try:
        all_news = fetch_all_news()
        
        if not all_news:
            print("No news from any source")
            return False
        
        print(f"Found {len(all_news)} total news items")
        
        # Group by source
        sleeper_items = [item for item in all_news if item.get('source') == 'sleeper']
        fantasypros_items = [item for item in all_news if item.get('source') == 'fantasypros']
        
        print(f"  - Sleeper: {len(sleeper_items)} items")
        print(f"  - FantasyPros: {len(fantasypros_items)} items")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_api_connectivity():
    """Test basic API connectivity."""
    print("\n" + "=" * 60)
    print("TESTING: API Connectivity")
    print("=" * 60)
    
    import requests
    
    # Test Sleeper API
    try:
        response = requests.get("https://api.sleeper.app/v1/players/nfl/trending/add?limit=1", timeout=10)
        if response.status_code == 200:
            print("Sleeper API: Connected")
        else:
            print(f"Sleeper API: Status {response.status_code}")
    except Exception as e:
        print(f"Sleeper API Error: {e}")
    
    # Test FantasyPros API
    try:
        response = requests.get("https://api.fantasypros.com/v2/news", timeout=10)
        if response.status_code == 200:
            print("FantasyPros API: Connected")
        elif response.status_code == 403:
            print("FantasyPros API: Requires API key")
        else:
            print(f"FantasyPros API: Status {response.status_code}")
    except Exception as e:
        print(f"FantasyPros API Error: {e}")


def run_specific_test(test_name):
    """Run a specific test by name."""
    tests = {
        "trending_adds": test_sleeper_trending_adds,
        "trending_drops": test_sleeper_trending_drops,
        "player_details": test_sleeper_player_details,
        "sleeper_news": test_sleeper_news,
        "fantasypros": test_fantasypros_news,
        "all_news": test_all_news,
        "connectivity": test_api_connectivity
    }
    
    if test_name in tests:
        return tests[test_name]()
    else:
        print(f"Unknown test: {test_name}")
        print(f"Available tests: {', '.join(tests.keys())}")
        return False


def main():
    """Main test runner."""
    print("Data Fetchers Isolation Test Suite")
    print("=" * 60)
    
    # Check if specific test requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
        success = run_specific_test(test_name)
        exit(0 if success else 1)
    
    # Run all tests
    tests = [
        ("API Connectivity", test_api_connectivity),
        ("Sleeper Trending Adds", test_sleeper_trending_adds),
        ("Sleeper Trending Drops", test_sleeper_trending_drops),
        ("Sleeper Player Details", test_sleeper_player_details),
        ("Complete Sleeper News", test_sleeper_news),
        ("FantasyPros News", test_fantasypros_news),
        ("All News Sources", test_all_news)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_name}")
        print('='*60)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
