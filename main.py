#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Tech Bytes - Main Orchestrator
Automated pipeline: Fetch AI news -> Generate TTS -> Create Video -> Upload
"""

import os
import sys
import argparse
from datetime import datetime

# Fix Unicode issues on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import modules
from news_fetcher import fetch_ai_news, save_news_to_file
from tts_generator import generate_audio_from_news
from video_maker import create_multiple_formats

def print_banner():
    """Print application banner"""
    print("="*70)
    print("  AI Tech Bytes")
    print("="*70)
    print("           BYTES - Automated Video Creator")
    print("="*70)
    print()

def run_pipeline(skip_news=False, skip_audio=False, skip_video=False):
    """
    Run the complete pipeline
    """
    print_banner()
    
    print("[{}] Starting pipeline...\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Step 1: Fetch AI News
    if not skip_news:
        print("\n" + "="*70)
        print("STEP 1: Fetching AI News")
        print("="*70)
        try:
            news_items = fetch_ai_news(num_articles=3)
            if news_items:
                news_file = save_news_to_file(news_items)
                print("[OK] News fetched and saved: {}".format(news_file))
            else:
                print("[WARNING] No news items fetched. Using fallback.")
        except Exception as e:
            print("[ERROR] Error fetching news: {}".format(e))
            return False
    else:
        print("\n[SKIP] Skipping news fetch (using existing data)")
    
    # Step 2: Generate TTS Audio
    if not skip_audio:
        print("\n" + "="*70)
        print("STEP 2: Generating Text-to-Speech Audio")
        print("="*70)
        try:
            audio_file = generate_audio_from_news()
            if audio_file:
                print("[OK] Audio generated: {}".format(audio_file))
            else:
                print("[ERROR] Audio generation failed")
                return False
        except Exception as e:
            print("[ERROR] Error generating audio: {}".format(e))
            return False
    else:
        print("\n[SKIP] Skipping audio generation (using existing audio)")
    
    # Step 3: Create Videos
    if not skip_video:
        print("\n" + "="*70)
        print("STEP 3: Creating Videos for Multiple Platforms")
        print("="*70)
        try:
            videos = create_multiple_formats()
            if videos:
                print("\n[OK] Created {} video(s)".format(len(videos)))
                for video in videos:
                    print("  - {}".format(video))
            else:
                print("[ERROR] Video creation failed")
                return False
        except Exception as e:
            print("[ERROR] Error creating videos: {}".format(e))
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n[SKIP] Skipping video creation (using existing videos)")
    
    # Step 4: Upload (placeholder for future implementation)
    print("\n" + "="*70)
    print("STEP 4: Upload to Social Media (Manual)")
    print("="*70)
    print("[INFO] YouTube/TikTok upload requires OAuth setup.")
    print("[INFO] Videos are ready in the 'output/' directory.")
    print("[INFO] Manual upload or configure YouTube Data API for automation.")
    
    # Summary
    print("\n" + "="*70)
    print("[OK] PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print("[{}] Done!\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='AI Tech Bytes - Automated video creator for AI news'
    )
    parser.add_argument(
        '--skip-news',
        action='store_true',
        help='Skip news fetching (use existing data)'
    )
    parser.add_argument(
        '--skip-audio',
        action='store_true',
        help='Skip audio generation (use existing audio)'
    )
    parser.add_argument(
        '--skip-video',
        action='store_true',
        help='Skip video creation (use existing videos)'
    )
    
    args = parser.parse_args()
    
    try:
        success = run_pipeline(
            skip_news=args.skip_news,
            skip_audio=args.skip_audio,
            skip_video=args.skip_video
        )
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n[WARNING] Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n\n[ERROR] Fatal error: {}".format(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
