"""Configuration settings for the NFL Fantasy Waiver Digest."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
SLEEPER_BASE_URL = "https://api.sleeper.app/v1"
FANTASYPROS_BASE_URL = "https://api.fantasypros.com/v2"

# API Keys
SLEEPER_API_KEY = os.getenv("SLEEPER_API_KEY", "")  # Not required for Sleeper
FANTASYPROS_API_KEY = os.getenv("FANTASYPROS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Fantasy relevance keywords
FANTASY_KEYWORDS = [
    # Injury keywords
    "injured", "injury", "out", "questionable", "doubtful", "probable",
    "hamstring", "knee", "ankle", "concussion", "shoulder", "back",
    "limited", "full", "practice", "rehab", "recovery",
    
    # Role change keywords
    "promoted", "demoted", "starter", "backup", "depth chart", "depth",
    "snap count", "snaps", "targets", "carries", "touches",
    "breakout", "struggling", "hot streak", "cold streak",
    
    # Transaction keywords
    "signed", "released", "traded", "waived", "claimed",
    "contract", "extension", "restructure",
    
    # Performance keywords
    "breakout", "breakout game", "career high", "season high",
    "struggling", "struggles", "slumping", "slump",
    "hot", "cold", "streak", "trending"
]

# Output configuration
OUTPUT_DIR = "digests"
DIGEST_FILENAME_TEMPLATE = "daily_digest_{date}.md"

# LLM Configuration
LLM_TIMEOUT_SECONDS = 60  # 60 seconds timeout for LLM requests