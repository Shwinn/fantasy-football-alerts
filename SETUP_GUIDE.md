# NFL Fantasy Waiver Digest - Setup Guide

## 🎯 What You Have

Your NFL Fantasy Waiver Digest application is ready! Here's what's been built:

### ✅ Core Features
- **Data Fetching**: Pulls news from Sleeper and FantasyPros APIs
- **Smart Filtering**: Identifies fantasy-relevant news using keyword matching
- **LLM Integration**: Uses OpenAI to generate intelligent insights and recommendations
- **Markdown Output**: Creates formatted daily digests
- **Testing**: Comprehensive unit tests included

### 📁 Project Structure
```
fantasy-football-alerts/
├── src/                    # Source code
│   ├── config.py          # Configuration and API keys
│   ├── data_fetchers.py   # API data fetching
│   ├── news_filter.py     # Fantasy relevance filtering
│   ├── llm_integration.py # OpenAI integration
│   └── digest_formatter.py # Markdown output
├── tests/                 # Unit tests
├── digests/              # Generated digest files
├── main.py               # Main script
├── test_run.py           # Test with sample data
└── requirements.txt      # Dependencies
```

## 🚀 Getting Started

### 1. Test the Basic Functionality
```bash
python test_run.py
```
This will run the app with sample data and generate a test digest.

### 2. Get Your API Keys

#### **Sleeper API** ✅ (Already Working!)
- **Status**: Free, no key needed
- **Action**: None required

#### **FantasyPros API**
1. Go to https://www.fantasypros.com/
2. Create a free account
3. Look for API access in their tools/developer section
4. Request an API key
5. Add it to your `.env` file

#### **OpenAI API** (Most Important for LLM Features)
1. Go to https://platform.openai.com/
2. Sign up for an account
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add $5-10 credits to your account

### 3. Configure API Keys
1. Copy `env_example.txt` to `.env`
2. Add your API keys:
```bash
cp env_example.txt .env
```
3. Edit `.env` and add your keys:
```
SLEEPER_API_KEY=your_sleeper_api_key_here
FANTASYPROS_API_KEY=your_fantasypros_api_key_here
OPENAI_API_KEY=sk-your-openai-key-here
```

### 4. Run the Full Application
```bash
python main.py
```

## 🧪 Testing

Run the unit tests:
```bash
python -m pytest tests/ -v
```

## 📊 How It Works

1. **Fetch News**: Pulls data from Sleeper and FantasyPros
2. **Filter**: Identifies fantasy-relevant items using keywords
3. **Categorize**: Groups news by type (injuries, role changes, etc.)
4. **Generate**: Uses OpenAI to create insights and recommendations
5. **Output**: Saves formatted digest to `digests/daily_digest_YYYYMMDD.md`

## 🔧 Customization

### Add More Keywords
Edit `src/config.py` and add keywords to `FANTASY_KEYWORDS`:
```python
FANTASY_KEYWORDS = [
    "injured", "injury", "out", "questionable",
    # Add your keywords here
    "your_keyword_here"
]
```

### Modify LLM Prompts
Edit `src/llm_integration.py` to change how the AI analyzes news.

### Add More Data Sources
Extend `src/data_fetchers.py` to include other news sources.

## 🐛 Troubleshooting

### Unicode Errors on Windows
The app is configured to work on Windows without Unicode issues.

### API Errors
- Check your API keys are correct
- Ensure you have credits in your OpenAI account
- Check if APIs are down

### No News Found
- Verify API keys are working
- Check if there's actually fantasy-relevant news today
- Try the test script first: `python test_run.py`

## 📈 Next Steps

Once you have your API keys:
1. Run `python main.py` to generate your first real digest
2. Check the `digests/` folder for your daily digest
3. Customize keywords and prompts based on your needs
4. Consider setting up a cron job for daily automation

## 🆘 Need Help?

The app includes comprehensive error handling and will tell you what's wrong. Check the console output for specific error messages.

Happy fantasy footballing! 🏈
