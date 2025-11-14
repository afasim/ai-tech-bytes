#!/usr/bin/env python3
"""
Text-to-Speech Generator
Converts news text to audio using gTTS (Google Text-to-Speech)
"""

import os
import json
from gtts import gTTS
from datetime import datetime

def load_news_from_file(filename='data/today_news.json'):
    """
    Load news articles from JSON file
    Returns list of (title, description) tuples
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('articles', [])
            return [(a['title'], a['description']) for a in articles]
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return []

def create_script_from_news(news_items):
    """
    Create a narrative script from news headlines
    Returns formatted text suitable for TTS
    """
    if not news_items:
        return "No news available today."
    
    # Introduction
    script = "Welcome to AI Tech Bytes! Here are today's top AI news stories. "
    
    # Add each news item
    for i, (title, description) in enumerate(news_items, 1):
        script += f"\n\nStory {i}: {title}. "
        if description:
            # Clean up description
            desc = description.strip()
            if desc:
                script += f"{desc} "
    
    # Outro
    script += "\n\nThat's all for today's AI Tech Bytes. Stay tuned for more AI news tomorrow!"
    
    return script

def text_to_speech(text, output_file='data/ai_news_audio.mp3', lang='en', slow=False):
    """
    Convert text to speech using gTTS
    Saves audio file to specified location
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Generate TTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to file
        tts.save(output_file)
        
        print(f"Audio saved to: {output_file}")
        print(f"Duration estimate: ~{len(text.split())} words")
        
        return output_file
        
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None

def generate_audio_from_news(news_file='data/today_news.json', 
                              audio_file='data/ai_news_audio.mp3'):
    """
    Complete pipeline: Load news, create script, generate audio
    """
    print("Loading news articles...")
    news_items = load_news_from_file(news_file)
    
    if not news_items:
        print("No news items found. Using default message.")
        news_items = [("No news available", "Please check back later for updates.")]
    
    print(f"Found {len(news_items)} news items")
    
    print("\nCreating narrative script...")
    script = create_script_from_news(news_items)
    
    # Save script for reference
    script_file = audio_file.replace('.mp3', '_script.txt')
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script)
    print(f"Script saved to: {script_file}")
    
    print("\nGenerating audio...")
    result = text_to_speech(script, audio_file)
    
    return result

if __name__ == "__main__":
    print("=== AI Tech Bytes - TTS Generator ===")
    audio_path = generate_audio_from_news()
    
    if audio_path:
        print(f"\n✓ Success! Audio file created: {audio_path}")
    else:
        print("\n✗ Failed to generate audio file")
