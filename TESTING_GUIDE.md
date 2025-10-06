# Testing Guide for Data Fetchers

This guide shows you how to test and verify the data fetching functions in isolation.

## 🧪 Available Test Scripts

### 1. `test_data_fetchers.py` - Main Data Fetcher Tests
Comprehensive test suite for all data fetching functions.

**Run all tests:**
```bash
python test_data_fetchers.py
```

**Run specific test:**
```bash
python test_data_fetchers.py trending_adds
python test_data_fetchers.py trending_drops
python test_data_fetchers.py player_details
python test_data_fetchers.py sleeper_news
python test_data_fetchers.py fantasypros
python test_data_fetchers.py all_news
python test_data_fetchers.py connectivity
```

### 2. `test_config.py` - Configuration Test
Tests your configuration and environment setup.

```bash
python test_config.py
```

### 3. `test_sleeper.py` - Sleeper-Specific Test
Tests the complete Sleeper integration with real data.

```bash
python test_sleeper.py
```

### 4. `test_run.py` - Sample Data Test
Tests the complete pipeline with sample data.

```bash
python test_run.py
```

## 📊 Test Results Explained

### ✅ **PASS** - Test Successful
- Function works correctly
- Data is being fetched properly
- No errors encountered

### ❌ **FAIL** - Test Failed
- Function encountered an error
- API might be down or rate-limited
- Configuration issue

### ⚠️ **Expected Behavior**
- **FantasyPros 403 Error**: Normal if no API key
- **No FantasyPros Data**: Expected without API key
- **API Connectivity "FAIL"**: Just means one API failed, not critical

## 🔍 What Each Test Does

### **API Connectivity Test**
- Tests basic connection to Sleeper and FantasyPros APIs
- Verifies endpoints are reachable
- Shows HTTP status codes

### **Sleeper Trending Adds Test**
- Fetches top 25 trending players being added
- Shows player IDs and add counts
- Verifies API response format

### **Sleeper Trending Drops Test**
- Fetches top 25 trending players being dropped
- Shows player IDs and drop counts
- Verifies API response format

### **Sleeper Player Details Test**
- Fetches all player information (11,400+ players)
- Uses caching to avoid repeated large downloads
- Shows sample player data

### **Complete Sleeper News Test**
- Combines trending data with player details
- Creates formatted news items
- Shows trending up vs trending down breakdown

### **FantasyPros News Test**
- Tests FantasyPros API integration
- Expected to fail without API key (403 error)
- Shows proper error handling

### **All News Sources Test**
- Tests the complete data fetching pipeline
- Combines all sources
- Shows total counts by source

## 🐛 Troubleshooting

### **Sleeper API Issues**
- Check internet connection
- Verify Sleeper API is not down
- Check for rate limiting (1000 calls/minute limit)

### **FantasyPros API Issues**
- 403 error is normal without API key
- Get API key from FantasyPros website
- Add key to `.env` file

### **OpenAI API Issues**
- Get API key from OpenAI platform
- Add key to `.env` file
- Ensure account has credits

### **Configuration Issues**
- Run `python test_config.py` to check setup
- Verify `.env` file exists and has correct format
- Check API keys are properly set

## 📈 Understanding the Data

### **Trending Adds**
- Players being added to fantasy rosters
- High counts indicate popular pickups
- Good source for waiver wire targets

### **Trending Drops**
- Players being dropped from rosters
- High counts indicate players to avoid
- Useful for identifying drop candidates

### **Player Details**
- Complete player information
- Names, teams, positions, injury status
- Used to enrich trending data

## 🚀 Next Steps

1. **Run all tests** to verify everything works
2. **Get API keys** for full functionality
3. **Test specific functions** when debugging
4. **Check configuration** if tests fail
5. **Use real data** once everything passes

The test suite gives you complete visibility into what's working and what needs attention!
