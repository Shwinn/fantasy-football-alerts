# 🏈 NFL Fantasy Waiver Digest — MVP PRD (Developer Spec)

## 1. Overview
**Goal:**  
Build a Python script that runs daily, aggregates NFL news from Sleeper and FantasyPros, filters for fantasy-relevant items (injuries, role changes, trades, depth chart shifts), and summarizes them into a Markdown digest with LLM-generated insights and pickup recommendations.

**Key Deliverable:**  
A Markdown file: `digests/daily_digest_YYYYMMDD.md` containing:
- A concise summary of the day’s notable NFL player news
- Categorized sections (e.g., Injuries, Role Changes, Potential Pickups)
- Suggested actionable pickups or watchlist players

---

## 2. Architecture Overview
(Diagram omitted for brevity, includes Sleeper + FantasyPros → Aggregator → LLM → Markdown Output)

---

## 3. Functional Requirements
**Scheduler:** Runs daily at fixed time.  
**Data Fetcher:** Pulls raw NFL news data from Sleeper and FantasyPros.  
**Normalizer:** Standardizes data.  
**Relevance Filter:** Filters for fantasy context (injury, out, promoted, etc.).  
**LLM Summarizer:** Summarizes and generates insights using OpenAI API.  
**Markdown Formatter:** Creates formatted digest.  
**File Writer:** Saves to `digests/daily_digest_YYYYMMDD.md`.

---

## 4. Data Schema
**Unified NewsItem (Python dict):**
```python
{
  "player_name": str,
  "team": str,
  "position": str,
  "headline": str,
  "summary": str,
  "source": str,      # sleeper | fantasypros
  "timestamp": str
}
```

---

## 5. Example LLM Prompt Template
```
SYSTEM:
You are an expert fantasy football analyst. Summarize today's NFL player news to identify potential waiver pickups and role changes.

USER:
Here are today's news items (JSON):

{{news_items_json}}

Please:
1. Summarize key takeaways (Injuries, Role Changes, Emerging Players).
2. Suggest 3–5 waiver pickups with reasoning.
3. Output in Markdown.
```

---

## 6. Example Output Format
```markdown
# 🏈 NFL Daily Fantasy Digest — Oct 5, 2025

### 🔥 Key Injuries
- Justin Jefferson (MIN) – Hamstring injury, expected to miss multiple weeks.
- Saquon Barkley (NYG) – Limited in practice; trending toward questionable.

### 📈 Role Changes
- Tyjae Spears (TEN) saw increased snaps with Henry limited — worth monitoring.

### 💎 Waiver Pickups / Watchlist
1. Tyjae Spears (TEN) – RB usage up 60%, must-stash if Henry misses time.
2. Josh Downs (IND) – Target share climbing; great PPR depth.

*(Data aggregated from Sleeper + FantasyPros)*
```

---

## 7. Implementation Details
Functions:
- `fetch_sleeper_news()`  
- `fetch_fantasypros_news()`  
- `filter_relevant_news()`  
- `generate_digest()`  
- `write_digest()`  
- `main()`  

Each includes example Python snippets for fetching, filtering, summarizing, and writing output.

---

## 8. MVP Flow Summary
**Main flow:**
1. Fetch Sleeper + FantasyPros news  
2. Combine and filter relevant items  
3. Send to LLM for digest generation  
4. Write Markdown file to `/digests`

---

## 9. Future Roadmap
- **v1.1:** Add Reddit/Twitter sources  
- **v1.2:** Add RAG for multi-day context  
- **v1.3:** Integrate with ESPN/Yahoo teams  
- **v1.4:** Deliver via Email/Discord  
- **v1.5:** Add trend analysis (e.g., snap count risers)
