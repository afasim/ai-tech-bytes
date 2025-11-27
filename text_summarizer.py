#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Summarizer
Summarizes news articles into concise scripts using HuggingFace transformers
"""

import json
import os
from datetime import datetime

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("[WARNING] HuggingFace transformers not installed. Using fallback summarization.")


def summarize_text_huggingface(text, max_length=150, min_length=50):
    """
    Summarize text using HuggingFace transformers
    Returns a concise summary (~900 characters for 3-5 articles)
    """
    if not HAS_TRANSFORMERS:
        return text[:900]  # Fallback: truncate to 900 chars
    
    try:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
        
        # Split into sentences if text is too long
        words = text.split()
        if len(words) > 512:  # Model token limit
            text = ' '.join(words[:512])
        
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print("[WARNING] HuggingFace summarization failed: {}. Using fallback.".format(e))
        return text[:900]


def summarize_article(title, description, max_chars=300):
    """
    Summarize a single article
    Returns title + concise summary
    """
    combined_text = "{}. {}".format(title, description) if description else title
    
    if len(combined_text) <= max_chars:
        return combined_text
    
    # If HuggingFace is available, use it; otherwise simple truncation
    if HAS_TRANSFORMERS:
        try:
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
            summary = summarizer(combined_text[:512], max_length=100, min_length=30, do_sample=False)
            return "{}. {}".format(title, summary[0]['summary_text'])
        except:
            return combined_text[:max_chars]
    else:
        return combined_text[:max_chars]


def create_video_script(news_items, max_total_chars=900):
    """
    Create a concise video script from news articles
    Optimized for ~60-second narration
    
    Args:
        news_items: List of dicts with 'title' and 'description'
        max_total_chars: Target character length (default 900 for ~60 sec)
    
    Returns:
        Formatted script as string
    """
    if not news_items:
        return "Welcome to AI Tech Bytes. No AI news available today. Check back tomorrow for updates."
    
    script_parts = ["Welcome to AI Tech Bytes. Here are today's top AI stories."]
    current_length = len(script_parts[0])
    
    for i, item in enumerate(news_items, 1):
        title = item.get('title', 'AI News')
        description = item.get('description', '')
        
        # Summarize each article to fit in the 900-char budget
        chars_per_article = (max_total_chars - current_length) // (len(news_items) - i + 1)
        
        article_text = summarize_article(title, description, max_chars=int(chars_per_article * 0.9))
        
        story_line = "\nStory {}: {}".format(i, article_text)
        
        if current_length + len(story_line) <= max_total_chars:
            script_parts.append(story_line)
            current_length += len(story_line)
        else:
            break
    
    # Add outro
    outro = "\nThat's all for today's AI Tech Bytes. Like and subscribe for daily AI news updates!"
    if current_length + len(outro) <= max_total_chars:
        script_parts.append(outro)
    
    script = ''.join(script_parts)
    
    print("[INFO] Generated script: {} characters (~{} seconds narration)".format(
        len(script), int(len(script) / 15)))  # Rough estimate: 15 chars per second
    
    return script


def save_script(script, filename='data/video_script.txt'):
    """
    Save the video script to a file
    """
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print("[OK] Script saved to: {}".format(filename))
    return filename


if __name__ == "__main__":
    print("=== AI Tech Bytes - Text Summarizer ===\n")
    
    # Example usage
    sample_news = [
        {
            "title": "OpenAI Releases GPT-4 Turbo with Vision Capabilities",
            "description": "OpenAI unveiled GPT-4 Turbo, featuring enhanced vision understanding, extended context window, and lower API costs for developers worldwide."
        },
        {
            "title": "Google DeepMind Announces Breakthrough in Protein Folding",
            "description": "DeepMind released AlphaFold3, predicting protein structures and molecular interactions with unprecedented accuracy, revolutionizing drug discovery."
        },
        {
            "title": "Meta Open-Sources Llama 2 AI Model for Researchers",
            "description": "Meta released Llama 2, an open-source large language model, enabling researchers and developers to build and customize AI applications freely."
        }
    ]
    
    script = create_video_script(sample_news)
    print("\nGenerated Script:")
    print("-" * 60)
    print(script)
    print("-" * 60)
    
    save_script(script)
