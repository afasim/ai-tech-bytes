#!/usr/bin/env python3
"""
AI News Fetcher
Fetches latest AI news headlines from various sources
"""

import os
import json
import requests
from datetime import datetime

# Configure news sources
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')  # Get from GitHub Secrets
NEWS_API_URL = 'https://newsapi.org/v2/everything'

def fetch_ai_news(num_articles=3):
    """
    Fetch top AI news articles
    Returns list of (title, description) tuples
    """
    try:
        params = {
            'q': 'artificial intelligence OR machine learning OR AI OR OpenAI OR ChatGPT',
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': num_articles,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('articles', [])
        
        news_items = []
        for article in articles:
            title = article.get('title', 'No title')
            description = article.get('description', '')
            news_items.append((title, description))
        
        return news_items
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        # Fallback to sample news if API fails
        return get_sample_news()

def get_sample_news():
    """Fallback sample news for testing"""
    return [
        ("AI Breakthrough: New Model Achieves Human-Level Performance", 
         "Researchers announce major advancement in artificial intelligence capabilities."),
        ("Tech Giants Invest Billions in AI Development", 
         "Major technology companies continue to expand their AI research and development teams."),
        ("AI Ethics: New Guidelines Released for Responsible Development", 
         "Industry leaders collaborate on comprehensive framework for ethical AI deployment.")
    ]

def save_news_to_file(news_items, filename='data/today_news.json'):
    """
    Save news items to JSON file
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    news_data = {
        'date': datetime.now().isoformat(),
        'articles': [{'title': title, 'description': desc} for title, desc in news_items]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(news_items)} news articles to {filename}")
    return filename

if __name__ == "__main__":
    print("Fetching AI news...")
    news = fetch_ai_news(num_articles=3)
    
    if news:
        print(f"\nFound {len(news)} articles:")
        for i, (title, desc) in enumerate(news, 1):
            print(f"\n{i}. {title}")
            print(f"   {desc[:100]}..." if len(desc) > 100 else f"   {desc}")
        
        # Save to file
        save_news_to_file(news)
    else:
        print("No news articles found.")
