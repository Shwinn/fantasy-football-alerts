"""Tests for news filtering functionality."""

import pytest
from src.news_filter import is_fantasy_relevant, filter_relevant_news, categorize_news


def test_is_fantasy_relevant_injury():
    """Test that injury news is marked as fantasy relevant."""
    news_item = {
        "player_name": "Test Player",
        "team": "Test Team",
        "position": "RB",
        "headline": "Player injured in practice",
        "summary": "Player suffered a hamstring injury",
        "source": "test",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    assert is_fantasy_relevant(news_item) == True


def test_is_fantasy_relevant_role_change():
    """Test that role change news is marked as fantasy relevant."""
    news_item = {
        "player_name": "Test Player",
        "team": "Test Team", 
        "position": "WR",
        "headline": "Player promoted to starter",
        "summary": "Player will start this week",
        "source": "test",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    assert is_fantasy_relevant(news_item) == True


def test_is_fantasy_relevant_not_relevant():
    """Test that non-fantasy news is marked as not relevant."""
    news_item = {
        "player_name": "Test Player",
        "team": "Test Team",
        "position": "QB", 
        "headline": "Player attends charity event",
        "summary": "Player visited local hospital",
        "source": "test",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    assert is_fantasy_relevant(news_item) == False


def test_filter_relevant_news():
    """Test filtering a list of news items."""
    news_items = [
        {
            "player_name": "Player 1",
            "team": "Team 1",
            "position": "RB",
            "headline": "Player injured",
            "summary": "Hamstring injury",
            "source": "test",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "player_name": "Player 2", 
            "team": "Team 2",
            "position": "WR",
            "headline": "Player attends event",
            "summary": "Charity work",
            "source": "test",
            "timestamp": "2024-01-01T00:00:00"
        }
    ]
    
    relevant = filter_relevant_news(news_items)
    assert len(relevant) == 1
    assert relevant[0]["player_name"] == "Player 1"


def test_categorize_news():
    """Test categorizing news items."""
    news_items = [
        {
            "player_name": "Injured Player",
            "team": "Team 1",
            "position": "RB",
            "headline": "Player injured",
            "summary": "Hamstring injury",
            "source": "test",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "player_name": "Promoted Player",
            "team": "Team 2", 
            "position": "WR",
            "headline": "Player promoted to starter",
            "summary": "Will start this week",
            "source": "test",
            "timestamp": "2024-01-01T00:00:00"
        }
    ]
    
    categories = categorize_news(news_items)
    
    assert len(categories["injuries"]) == 1
    assert len(categories["role_changes"]) == 1
    assert categories["injuries"][0]["player_name"] == "Injured Player"
    assert categories["role_changes"][0]["player_name"] == "Promoted Player"
