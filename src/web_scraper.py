"""Web scraper for FantasyPros articles."""

import requests
import time
import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class FantasyProsScraper:
    """Web scraper for FantasyPros NFL content."""
    
    def __init__(self, base_url: str = "https://www.fantasypros.com/nfl/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.articles_dir = "scraped_articles"
        self.scraped_urls_file = "scraped_urls.json"
        self.section_mapping = {
            "https://www.fantasypros.com/nfl/": "main",
            "https://www.fantasypros.com/nfl/news/": "news",
            "https://www.fantasypros.com/nfl/advice/": "advice",
            "https://www.fantasypros.com/nfl/articles/": "articles",
        }
        self._ensure_articles_dir()
        self._load_scraped_urls()
    
    def _ensure_articles_dir(self):
        """Create articles directory if it doesn't exist."""
        if not os.path.exists(self.articles_dir):
            os.makedirs(self.articles_dir)
            print(f"Created directory: {self.articles_dir}")
    
    def _load_scraped_urls(self):
        """Load previously scraped URLs from file."""
        self.scraped_urls = set()
        if os.path.exists(self.scraped_urls_file):
            try:
                with open(self.scraped_urls_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scraped_urls = set(data.get('urls', []))
                print(f"Loaded {len(self.scraped_urls)} previously scraped URLs")
            except Exception as e:
                print(f"Error loading scraped URLs: {e}")
                self.scraped_urls = set()
        else:
            print("No previous scraped URLs found, starting fresh")
    
    def _save_scraped_urls(self):
        """Save scraped URLs to file."""
        try:
            data = {
                'urls': list(self.scraped_urls),
                'last_updated': datetime.now().isoformat(),
                'total_urls': len(self.scraped_urls)
            }
            with open(self.scraped_urls_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving scraped URLs: {e}")
    
    def _is_url_scraped(self, url: str) -> bool:
        """Check if a URL has already been scraped."""
        return url in self.scraped_urls
    
    def _mark_url_scraped(self, url: str):
        """Mark a URL as scraped."""
        self.scraped_urls.add(url)
    
    def _setup_selenium_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def get_page_links(self, url: str) -> List[str]:
        """Extract all article links from a FantasyPros page."""
        try:
            print(f"Fetching links from: {url}")
            
            # Try with requests first
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            print(f"Response status: {response.status_code}")
            print(f"Content length: {len(response.content)}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Print some basic info about the page
            title = soup.find('title')
            print(f"Page title: {title.get_text() if title else 'No title found'}")
            
            # Look for all links first
            all_links = soup.find_all('a', href=True)
            print(f"Total links found: {len(all_links)}")
            
            links = self._extract_links_from_soup(soup, url)
            
            if not links:
                print("No article links found with requests, trying alternative selectors...")
                links = self._extract_links_alternative(soup, url)
            
            print(f"Found {len(links)} potential article links")
            return links
            
        except Exception as e:
            print(f"Error fetching links from {url}: {e}")
            return []
    
    def _extract_links_from_soup(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract article links from BeautifulSoup object."""
        links = []
        
        # Look for common article link patterns
        link_selectors = [
            'a[href*="/news/"]',
            'a[href*="/articles/"]',
            'a[href*="/analysis/"]',
            'a[href*="/rankings/"]',
            'a[href*="/advice/"]',
            'a[href*="/waiver-wire/"]',
            'a[href*="/start-sit/"]',
            'a[href*="/sleepers/"]',
            'a[href*="/busts/"]',
            'a[href*="/injury/"]',
            'a[href*="/trade/"]',
            'a[href*="/draft/"]',
            'a[href*="/lineup/"]',
            'a[href*="/projections/"]',
            'a[href*="/consensus/"]',
            # Date-based article patterns (e.g., /2025/10/article-name/)
            'a[href*="/2025/"]',
            'a[href*="/2024/"]',
            'a[href*="/2023/"]'
        ]
        
        for selector in link_selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if self._is_valid_article_url(full_url):
                        links.append(full_url)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(links))
    
    def _extract_links_alternative(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Alternative method to extract links using broader selectors."""
        links = []
        
        # Get all links and filter manually
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                
                # Check if it's a FantasyPros article
                if ('fantasypros.com' in full_url and 
                    any(keyword in full_url.lower() for keyword in [
                        'news', 'article', 'analysis', 'rankings', 'advice', 
                        'waiver', 'start-sit', 'sleeper', 'bust', 'injury',
                        'trade', 'draft', 'lineup', 'projection', 'consensus'
                    ]) and
                    not any(skip in full_url.lower() for skip in [
                        'api', 'static', 'css', 'js', 'image', 'font', 'ad',
                        'tracking', 'login', 'register', 'subscribe', 'premium'
                    ])):
                    links.append(full_url)
        
        print(f"Alternative method found {len(links)} links")
        return list(dict.fromkeys(links))
    
    def _is_valid_article_url(self, url: str) -> bool:
        """Check if URL is a valid article URL."""
        if not url or not isinstance(url, str):
            return False
        
        # Must be from fantasypros.com
        if 'fantasypros.com' not in url:
            return False
        
        # Skip certain patterns
        skip_patterns = [
            '/api/',
            '/static/',
            '/css/',
            '/js/',
            '/images/',
            '/fonts/',
            '/ads/',
            '/tracking/',
            'javascript:',
            'mailto:',
            'tel:',
            '#',
            '?utm_',
            '/login',
            '/register',
            '/subscribe',
            '/premium',
            '?page=',  # Skip pagination URLs
            '?sort=',
            '?filter=',
            '?category=',
            '?tag=',
            '?search=',
            '?year=',
            '?month=',
            '?author='
        ]
        
        for pattern in skip_patterns:
            if pattern in url.lower():
                return False
        
        # Must have meaningful content path
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if len(path.split('/')) < 2:  # At least 2 path segments
            return False
        
        # Must be an actual article, not a listing page
        # Look for specific article indicators in the URL
        article_indicators = [
            '/news/',
            '/articles/',
            '/analysis/',
            '/rankings/',
            '/advice/',
            '/waiver-wire/',
            '/start-sit/',
            '/sleepers/',
            '/busts/',
            '/injury/',
            '/trade/',
            '/draft/',
            '/lineup/',
            '/projections/',
            '/consensus/',
            '/correspondents/',
            # Date-based article patterns (e.g., /2025/10/article-name/)
            '/2025/',
            '/2024/',
            '/2023/'
        ]
        
        # Check if URL contains any article indicators
        has_article_indicator = any(indicator in url for indicator in article_indicators)
        if not has_article_indicator:
            return False
        
        # Additional check: must not be just a section listing page
        # e.g., /nfl/articles/ should be excluded, but /nfl/articles/some-article should be included
        if url.endswith('/articles/') or url.endswith('/news/') or url.endswith('/rankings/'):
            return False
        
        return True
    
    def _get_links_with_selenium(self, url: str) -> List[str]:
        """Use Selenium to get links from JavaScript-heavy pages."""
        driver = None
        try:
            driver = self._setup_selenium_driver()
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Get all links
            links = []
            link_elements = driver.find_elements(By.TAG_NAME, "a")
            
            for element in link_elements:
                href = element.get_attribute("href")
                if href and self._is_valid_article_url(href):
                    links.append(href)
            
            return list(dict.fromkeys(links))
            
        except Exception as e:
            print(f"Error with Selenium scraping: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def scrape_article(self, url: str, source_url: str = None) -> Optional[Dict[str, Any]]:
        """Scrape content from a single article URL."""
        try:
            print(f"Scraping article: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article content
            article_data = {
                'url': url,
                'title': self._extract_title(soup),
                'author': self._extract_author(soup),
                'date': self._extract_date(soup),
                'content': self._extract_content(soup),
                'tags': self._extract_tags(soup),
                'scraped_at': datetime.now().isoformat(),
                'source_url': source_url
            }
            
            # Save to file
            filename = self._save_article_to_file(article_data, source_url)
            article_data['filename'] = filename
            
            return article_data
            
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        title_selectors = [
            'h1.article-title',
            'h1.entry-title',
            'h1.post-title',
            'h1[class*="title"]',
            'title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "No title found"
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract article author."""
        author_selectors = [
            '.author-name',
            '.byline',
            '.article-author',
            '[class*="author"]',
            'meta[name="author"]'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '').strip()
                return element.get_text().strip()
        
        return "Unknown author"
    
    def _extract_date(self, soup: BeautifulSoup) -> str:
        """Extract article publication date."""
        date_selectors = [
            '.article-date',
            '.published-date',
            '.post-date',
            '[class*="date"]',
            'time[datetime]',
            'meta[property="article:published_time"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '').strip()
                if element.name == 'time':
                    return element.get('datetime', element.get_text()).strip()
                return element.get_text().strip()
        
        return datetime.now().strftime("%Y-%m-%d")
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content."""
        content_selectors = [
            '.article-content',
            '.entry-content',
            '.post-content',
            '.main-content',
            '.content',
            'article',
            '.article-body',
            '[class*="content"]'
        ]
        
        # First try to find a single main content element
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                # Remove script and style elements
                for script in element(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                
                # Get text content
                content = element.get_text(separator='\n', strip=True)
                if len(content) > 100:  # Only return if substantial content
                    return content
        
        # If no single element found, try to combine multiple .content elements
        # This handles FantasyPros' structure where news items are in multiple .content divs
        content_elements = soup.select('.content')
        if content_elements:
            combined_content = []
            for element in content_elements:
                # Remove script and style elements
                for script in element(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                
                text = element.get_text(separator='\n', strip=True)
                if text and len(text) > 50:  # Only include substantial content
                    combined_content.append(text)
            
            if combined_content:
                return '\n\n'.join(combined_content)
        
        return "No content found"
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract article tags."""
        tag_selectors = [
            '.tags a',
            '.tag-list a',
            '.article-tags a',
            '[class*="tag"] a'
        ]
        
        tags = []
        for selector in tag_selectors:
            elements = soup.select(selector)
            for element in elements:
                tag = element.get_text().strip()
                if tag:
                    tags.append(tag)
        
        return list(set(tags))  # Remove duplicates
    
    def _save_article_to_file(self, article_data: Dict[str, Any], source_url: str = None) -> str:
        """Save article data to a text file organized by section and date."""
        try:
            # Determine section from article URL first, then source URL
            section = "unknown"
            article_url = article_data.get('url', '')
            
            # First check the article URL for better categorization
            if '/news/' in article_url:
                section = "news"
            elif '/rankings/' in article_url:
                section = "rankings"
            elif '/advice/' in article_url:
                section = "advice"
            elif '/articles/' in article_url:
                section = "articles"
            elif source_url:
                # Fall back to source URL matching
                best_match = None
                best_match_length = 0
                for url_pattern, section_name in self.section_mapping.items():
                    if source_url.startswith(url_pattern) and len(url_pattern) > best_match_length:
                        best_match = section_name
                        best_match_length = len(url_pattern)
                
                if best_match:
                    section = best_match
            
            # Get date for folder organization
            article_date = article_data.get('date', datetime.now().strftime("%Y-%m-%d"))
            if isinstance(article_date, str):
                try:
                    # Try to parse the date to ensure it's valid
                    parsed_date = datetime.strptime(article_date, "%Y-%m-%d")
                    date_folder = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    # If date parsing fails, use today's date
                    date_folder = datetime.now().strftime("%Y-%m-%d")
            else:
                date_folder = datetime.now().strftime("%Y-%m-%d")
            
            # Create directory structure: scraped_articles/section/date/
            section_dir = os.path.join(self.articles_dir, section)
            date_dir = os.path.join(section_dir, date_folder)
            
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)
                print(f"Created directory: {date_dir}")
            
            # Create safe filename from title
            title = article_data.get('title', 'untitled')
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            safe_title = safe_title[:50]  # Limit length
            
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{safe_title}_{timestamp}.txt"
            filepath = os.path.join(date_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {article_data.get('title', 'N/A')}\n")
                f.write(f"Author: {article_data.get('author', 'N/A')}\n")
                f.write(f"Date: {article_data.get('date', 'N/A')}\n")
                f.write(f"URL: {article_data.get('url', 'N/A')}\n")
                f.write(f"Section: {section}\n")
                f.write(f"Source URL: {source_url or 'N/A'}\n")
                f.write(f"Tags: {', '.join(article_data.get('tags', []))}\n")
                f.write(f"Scraped: {article_data.get('scraped_at', 'N/A')}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(article_data.get('content', 'No content available'))
            
            print(f"Saved article: {section}/{date_folder}/{filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving article: {e}")
            return "error_saving.txt"
    
    def scrape_fantasypros_articles(self, max_articles: int = 50) -> List[Dict[str, Any]]:
        """Main method to scrape FantasyPros articles."""
        print(f"Starting FantasyPros scraping (max {max_articles} articles)...")
        
        # Try multiple FantasyPros sections to find articles
        urls_to_check = [
            "https://www.fantasypros.com/nfl/",
            "https://www.fantasypros.com/nfl/news/",
            "https://www.fantasypros.com/nfl/articles/",
        ]
        
        all_links = []
        
        for url in urls_to_check:
            print(f"\nChecking: {url}")
            links = self.get_page_links(url)
            # Store links with their source URL for section tracking
            for link in links:
                all_links.append((link, url))  # (article_url, source_url)
            print(f"Found {len(links)} links from this page")
            
            # If we found some links, we can stop checking more pages
            if len(all_links) >= max_articles * 2:  # Get more than needed for variety
                break
        
        # Remove duplicates while preserving source URL
        unique_links = []
        seen_urls = set()
        for article_url, source_url in all_links:
            if article_url not in seen_urls:
                unique_links.append((article_url, source_url))
                seen_urls.add(article_url)
        
        if not unique_links:
            print("No article links found from any FantasyPros pages!")
            return []
        
        print(f"\nFound {len(unique_links)} total unique articles across all pages")
        
        # Limit number of articles to scrape
        links_to_scrape = unique_links[:max_articles]
        
        scraped_articles = []
        failed_count = 0
        
        for i, (article_url, source_url) in enumerate(links_to_scrape, 1):
            print(f"\nScraping article {i}/{len(links_to_scrape)}")
            print(f"From section: {self.section_mapping.get(source_url, 'unknown')}")
            
            # Check if URL has already been scraped
            if self._is_url_scraped(article_url):
                print(f"[SKIPPED] Already scraped: {article_url}")
                continue
            
            article_data = self.scrape_article(article_url, source_url)
            
            if article_data:
                # Mark URL as scraped
                self._mark_url_scraped(article_url)
                
                # Add source URL to article data for section tracking
                article_data['source_url'] = source_url
                scraped_articles.append(article_data)
                print(f"[SUCCESS] Successfully scraped: {article_data.get('title', 'Unknown')[:50]}...")
            else:
                failed_count += 1
                print(f"[FAILED] Failed to scrape: {article_url}")
            
            # Be respectful - add delay between requests
            time.sleep(1)
        
        print(f"\nScraping complete!")
        print(f"Successfully scraped: {len(scraped_articles)} articles")
        print(f"Failed: {failed_count} articles")
        print(f"Articles saved to: {self.articles_dir}")
        
        # Save updated scraped URLs
        self._save_scraped_urls()
        print(f"Updated scraped URLs tracking: {len(self.scraped_urls)} total URLs")
        
        return scraped_articles
    
    def get_scraping_summary(self) -> Dict[str, Any]:
        """Get summary of scraped articles organized by section and date."""
        if not os.path.exists(self.articles_dir):
            return {"total_articles": 0, "articles": [], "sections": {}}
        
        articles = []
        sections = {}
        
        # Walk through the directory structure
        for root, dirs, files in os.walk(self.articles_dir):
            for filename in files:
                if filename.endswith('.txt'):
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract basic info from file
                            lines = content.split('\n')
                            title = lines[0].replace('Title: ', '') if lines else 'Unknown'
                            author = lines[1].replace('Author: ', '') if len(lines) > 1 else 'Unknown'
                            section = lines[4].replace('Section: ', '') if len(lines) > 4 else 'unknown'
                            date = lines[2].replace('Date: ', '') if len(lines) > 2 else 'Unknown'
                            
                            # Get relative path for better organization
                            rel_path = os.path.relpath(filepath, self.articles_dir)
                            
                            article_info = {
                                'filename': filename,
                                'title': title,
                                'author': author,
                                'section': section,
                                'date': date,
                                'path': rel_path
                            }
                            articles.append(article_info)
                            
                            # Count by section
                            if section not in sections:
                                sections[section] = 0
                            sections[section] += 1
                            
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
        
        return {
            "total_articles": len(articles),
            "articles": articles,
            "sections": sections
        }
    
    def get_deduplication_stats(self) -> Dict[str, Any]:
        """Get statistics about the deduplication system."""
        return {
            "total_scraped_urls": len(self.scraped_urls),
            "scraped_urls_file": self.scraped_urls_file,
            "file_exists": os.path.exists(self.scraped_urls_file)
        }
    
    def clear_scraped_urls(self):
        """Clear all scraped URL tracking (use with caution)."""
        self.scraped_urls.clear()
        if os.path.exists(self.scraped_urls_file):
            os.remove(self.scraped_urls_file)
        print("Cleared all scraped URL tracking")
    
    def clean_old_urls(self, days_old: int = 30):
        """Clean URLs older than specified days (placeholder for future enhancement)."""
        # This could be enhanced to clean old URLs based on timestamps
        # For now, we'll keep all URLs to avoid re-scraping
        print(f"URL cleaning not implemented yet - keeping all {len(self.scraped_urls)} URLs")
