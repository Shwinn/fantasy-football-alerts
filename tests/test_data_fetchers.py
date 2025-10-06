"""Tests for data fetching functionality."""

import pytest
from unittest.mock import patch, Mock
from src.data_fetchers import fetch_sleeper_news, fetch_fantasypros_news, fetch_all_news


def test_fetch_sleeper_news():
    """Test fetching Sleeper news."""
    news = fetch_sleeper_news()
    
    # Should return a list
    assert isinstance(news, list)
    
    # Should have at least one item (our placeholder)
    assert len(news) >= 1
    
    # Check structure of first item
    if news:
        item = news[0]
        assert "player_name" in item
        assert "team" in item
        assert "position" in item
        assert "headline" in item
        assert "summary" in item
        assert "source" in item
        assert "timestamp" in item
        assert item["source"] == "sleeper"


@patch('src.data_fetchers.requests.get')
def test_fetch_fantasypros_news_success(mock_get):
    """Test successful FantasyPros news fetching."""
    # Mock successful response
    mock_response = Mock()
    mock_response.json.return_value = {
        "news": [
            {
                "player_name": "Test Player",
                "team": "Test Team",
                "position": "RB",
                "headline": "Test Headline",
                "summary": "Test Summary",
                "timestamp": "2024-01-01T00:00:00"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    news = fetch_fantasypros_news()
    
    assert isinstance(news, list)
    assert len(news) == 1
    assert news[0]["player_name"] == "Test Player"
    assert news[0]["source"] == "fantasypros"


@patch('src.data_fetchers.requests.get')
def test_fetch_fantasypros_news_error(mock_get):
    """Test FantasyPros news fetching with error."""
    # Mock error response
    mock_get.side_effect = Exception("API Error")
    
    news = fetch_fantasypros_news()
    
    # Should return empty list on error
    assert isinstance(news, list)
    assert len(news) == 0


def test_fetch_all_news():
    """Test fetching from all sources."""
    news = fetch_all_news()
    
    assert isinstance(news, list)
    # Should have at least Sleeper news (our placeholder)
    assert len(news) >= 1
