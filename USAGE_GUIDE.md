# Fantasy Football Alerts - Usage Guide

## Main Scripts

### `main.py` - Complete Digest Generation
The main entry point that generates a complete fantasy football digest using all available sources.

```bash
python main.py                    # Use LLM if API key available, otherwise simple digest
python main.py --no-llm          # Force simple digest (no LLM API calls)
python main.py --help            # Show help message
```

**What it does:**
- Fetches news from Sleeper API and FantasyPros (via web scraping)
- Filters for fantasy-relevant content
- Generates a digest with LLM insights (if OpenAI API key is configured)
- Saves digest to `digests/` folder

**Command-line options:**
- `--no-llm`: Force simple digest generation without LLM API calls (saves API costs)
- `--help`: Show detailed help message with usage examples

### `run_scraper.py` - Web Scraping Only
Runs only the FantasyPros web scraper to collect articles.

```bash
python run_scraper.py
```

**What it does:**
- Scrapes articles from multiple FantasyPros sections
- Organizes articles by section and date
- Saves articles to `scraped_articles/` folder
- Interactive - asks how many articles to scrape

### `test_scraper.py` - Quick Test
Quick test of the web scraper with 5 articles.

```bash
python test_scraper.py
```

**What it does:**
- Tests the web scraper with a small number of articles
- Shows organization by section and date
- Good for testing functionality

### `browse_articles.py` - Article Browser
Browse and search through scraped articles.

```bash
python browse_articles.py
python browse_articles.py "Xavier Worthy"  # Search for specific content
```

**What it does:**
- Shows all scraped articles organized by section and date
- Search functionality for finding specific articles
- Displays article metadata and file paths

### `cleanup_duplicates.py` - Duplicate Cleanup
Clean up duplicate articles created before the deduplication system.

```bash
python cleanup_duplicates.py           # Dry run - show what would be deleted
python cleanup_duplicates.py --execute # Actually delete duplicate files
```

**What it does:**
- Scans all articles for duplicates based on content and title
- Shows detailed analysis of duplicate files
- Safely removes duplicates while keeping the newest version
- Dry run mode shows what would be deleted without actually deleting

## File Organization

### Scraped Articles
```
scraped_articles/
├── news/2025-10-06/
├── rankings/2025-10-06/
├── advice/2025-10-06/
└── ...
```

### Digests
```
digests/
├── daily_digest_20251005.md
├── daily_digest_20251006.md
└── ...
```

### Deduplication Tracking
```
scraped_urls.json    # Tracks previously scraped URLs to prevent duplicates
```

## Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

## Typical Workflow

1. **Daily Digest Generation:**
   ```bash
   python main.py                    # With LLM (if API key available)
   python main.py --no-llm          # Simple format (no API costs)
   ```

2. **Browse Recent Articles:**
   ```bash
   python browse_articles.py
   ```

3. **Search for Specific Content:**
   ```bash
   python browse_articles.py "injury"
   ```

4. **Test Scraper:**
   ```bash
   python test_scraper.py
   ```

5. **Clean Up Duplicates:**
   ```bash
   python cleanup_duplicates.py
   ```

## Cost Management

### LLM API Costs
- **With LLM**: Uses OpenAI API for enhanced insights (costs money)
- **Without LLM**: Uses simple digest format (free)
- **Default behavior**: Uses LLM if API key is available, otherwise falls back to simple format
- **Force simple mode**: Use `--no-llm` flag to avoid API costs during testing

### Deduplication System
The system automatically prevents scraping the same articles multiple times:

- **URL Tracking**: All scraped URLs are stored in `scraped_urls.json`
- **Automatic Skipping**: Previously scraped articles are automatically skipped
- **Persistent Storage**: URL tracking persists between runs
- **Automatic Operation**: No manual management needed

### Benefits:
- **Efficiency**: No wasted time re-scraping the same content
- **Storage**: Prevents duplicate files
- **Bandwidth**: Reduces unnecessary network requests
- **Reliability**: Safe to run multiple times without issues

## Notes

- The web scraper is automatically integrated into the main digest generation
- Articles are organized by section (news, rankings, advice, etc.) and date
- All scripts include error handling and progress reporting
- The system respects rate limits and includes delays between requests
- **Deduplication is automatic** - no configuration needed
