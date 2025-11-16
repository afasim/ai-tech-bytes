#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced News Fetcher
Fetches AI news from free RSS feeds and public APIs (no premium required)
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Free RSS feeds for AI/Tech news (no API key required)
FREE_RSS_FEEDS = {
    'ycombinator': 'https://news.ycombinator.com/rss',
    'hackernews': 'https://news.ycombinator.com/rss',
    'reddit_ml': 'https://www.reddit.com/r/MachineLearning/.rss',
    'reddit_ai': 'https://www.reddit.com/r/artificial/.rss',
}

NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
NEWS_API_URL = 'https://newsapi.org/v2/everything'


def parse_rss_feed(feed_url, search_terms=['AI', 'machine learning', 'artificial intelligence']):
    """
    Parse RSS feed and extract AI-related articles
    Returns list of (title, description, source) tuples
    """
    try:
        import feedparser
    except ImportError:
        print("[WARNING] feedparser not installed. Skipping RSS feeds. Install with: pip install feedparser")
        return []
    
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:5]:  # Get top 5 from each feed
            title = entry.get('title', '')
            description = entry.get('summary', '') or entry.get('description', '')
            
            # Filter for AI-related content
            content_lower = (title + ' ' + description).lower()
            if any(term.lower() in content_lower for term in search_terms):
                articles.append({
                    'title': title,
                    'description': description[:200],  # Limit description length
                    'source': feed.feed.get('title', 'RSS Feed'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', datetime.now().isoformat())
                })
        
        return articles
    except Exception as e:
        print("[WARNING] Error parsing RSS feed {}: {}".format(feed_url, e))
        return []


def fetch_from_free_rss():
    """
    Fetch AI news from free RSS feeds
    Returns list of article dicts
    """
    print("[INFO] Fetching from free RSS feeds...")
    all_articles = []
    
    for source_name, feed_url in FREE_RSS_FEEDS.items():
        print("[INFO] Parsing {}...".format(source_name))
        articles = parse_rss_feed(feed_url)
        all_articles.extend(articles)
    
    return all_articles


def fetch_from_newsapi(num_articles=3):
    """
    Fetch from NewsAPI (if key available)
    Returns list of article dicts
    """
    if not NEWS_API_KEY:
        print("[WARNING] NEWS_API_KEY not set. Skipping NewsAPI.")
        return []
    
    print("[INFO] Fetching from NewsAPI...")
    try:
        params = {
            'q': 'artificial intelligence OR machine learning OR AI OR ChatGPT OR neural network',
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': num_articles,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for article in data.get('articles', []):
            articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', '')[:200],
                'source': article.get('source', {}).get('name', 'NewsAPI'),
                'link': article.get('url', ''),
                'published': article.get('publishedAt', datetime.now().isoformat())
            })
        
        return articles
    except Exception as e:
        print("[WARNING] Error fetching from NewsAPI: {}".format(e))
        return []


def fetch_ai_news(num_articles=5, use_rss=True, use_api=True):
    """
    Fetch AI news from multiple free sources
    
    Args:
        num_articles: Number of articles to fetch
        use_rss: Whether to fetch from RSS feeds
        use_api: Whether to fetch from NewsAPI (if key available)
    
    Returns:
        List of article dicts, sorted by date
    """
    all_articles = []
    
    if use_rss:
        rss_articles = fetch_from_free_rss()
        all_articles.extend(rss_articles)
    
    if use_api:
        api_articles = fetch_from_newsapi(num_articles)
        all_articles.extend(api_articles)
    
    if not all_articles:
        print("[WARNING] No articles fetched. Using sample data.")
        return get_sample_news()
    
    # Deduplicate by title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title = article['title']
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    
    # Sort by date (newest first) and return top N
    try:
        unique_articles.sort(
            key=lambda x: x.get('published', ''),
            reverse=True
        )
    except:
        pass  # If sorting fails, keep original order
    
    return unique_articles[:num_articles]


def get_sample_news():
    """Fallback sample news for testing"""
    return [
        {
            "title": "OpenAI Announces GPT-4 Turbo with 128K Context Window",
            "description": "OpenAI releases GPT-4 Turbo, doubling the context window to 128K tokens and reducing API costs.",
            "source": "Sample",
            "link": "",
            "published": datetime.now().isoformat()
        },
        {
            "title": "Google DeepMind Releases AlphaFold3 for Protein Prediction",
            "description": "DeepMind releases AlphaFold3, predicting not just protein structures but also molecular interactions.",
            "source": "Sample",
            "link": "",
            "published": datetime.now().isoformat()
        },
        {
            "title": "Meta Open-Sources Llama 2 AI Model",
            "description": "Meta releases Llama 2, an open-source large language model, for research and commercial use.",
            "source": "Sample",
            "link": "",
            "published": datetime.now().isoformat()
        },
        {
            "title": "Anthropic Raises $5B for Constitutional AI Research",
            "description": "Anthropic secures $5 billion in funding to advance safe and beneficial AI research.",
            "source": "Sample",
            "link": "",
            "published": datetime.now().isoformat()
        },
        {
            "title": "Microsoft Integrates GPT-4 into Windows 11 Copilot",
            "description": "Microsoft brings advanced AI capabilities to Windows 11 with GPT-4 integration.",
            "source": "Sample",
            "link": "",
            "published": datetime.now().isoformat()
        }
    ]


def save_news_to_file(news_items, filename='data/today_news.json'):
    """
    Save news items to JSON file
    """
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
    news_data = {
        'date': datetime.now().isoformat(),
        'num_articles': len(news_items),
        'articles': news_items
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    
    print("[OK] Saved {} articles to {}".format(len(news_items), filename))
    return filename


if __name__ == "__main__":
    print("=== AI Tech Bytes - Enhanced News Fetcher ===\n")
    
    news = fetch_ai_news(num_articles=5)
    
    if news:
        print("\n[OK] Found {} articles:".format(len(news)))
        for i, article in enumerate(news, 1):
            print("\n{:2d}. {}".format(i, article['title']))
            print("    Source: {}".format(article.get('source', 'Unknown')))
            print("    {}...".format(article['description'][:80]))
        
        save_news_to_file(news)
    else:
        print("[ERROR] No news articles found.")
