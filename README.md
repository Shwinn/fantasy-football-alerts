# NFL Fantasy Waiver Digest

A Python script that aggregates NFL news from Sleeper and FantasyPros, filters for fantasy-relevant items, and generates daily digests with LLM-powered insights.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

3. Run the script:
```bash
python main.py
```

## API Keys Required

- **Sleeper API**: Free, no key required
- **FantasyPros API**: Free tier available
- **OpenAI API**: Pay-per-use

See the setup guide for detailed instructions on obtaining these keys.
