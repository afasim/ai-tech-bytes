#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Tech Bytes - Main Orchestrator
Automated pipeline: Fetch AI news -> Summarize -> Generate TTS -> Create Video -> Save Assets
"""

import os
import sys
import argparse
from datetime import datetime
import json

# Fix Unicode issues on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import modules
from news_fetcher import fetch_ai_news, save_news_to_file
try:
    from enhanced_news_fetcher import fetch_ai_news as fetch_ai_news_enhanced
except ImportError:
    fetch_ai_news_enhanced = None

try:
    from text_summarizer import create_video_script
except ImportError:
    create_video_script = None

from tts_generator import generate_audio_from_news
from video_maker import create_multiple_formats

try:
    from asset_manager import AssetManager, create_complete_asset_manifest
except ImportError:
    AssetManager = None

def print_banner():
    """Print application banner"""
    print("="*70)
    print("  AI Tech Bytes")
    print("="*70)
    print("           BYTES - Automated Video Creator")
    print("="*70)
    print()

def run_pipeline(skip_news=False, skip_audio=False, skip_video=False, use_enhanced=True, use_summarization=True):
    """
    Run the complete pipeline
    """
    print_banner()
    
    print("[{}] Starting pipeline...\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Initialize asset manager
    asset_manager = None
    if AssetManager:
        asset_manager = AssetManager()
    
    news_items = []
    
    # Step 1: Fetch AI News
    if not skip_news:
        print("\n" + "="*70)
        print("STEP 1: Fetching AI News")
        print("="*70)
        try:
            if use_enhanced and fetch_ai_news_enhanced:
                print("[INFO] Using enhanced news fetcher (RSS + NewsAPI)")
                news_items = fetch_ai_news_enhanced(num_articles=3, use_rss=True, use_api=True)
            else:
                print("[INFO] Using standard NewsAPI fetcher")
                news_items = fetch_ai_news(num_articles=3)
            
            if news_items:
                news_file = save_news_to_file(news_items)
                print("[OK] News fetched and saved: {}".format(news_file))
                if asset_manager:
                    asset_manager.add_asset('news', news_file, 'Fetched AI news articles', 
                        source='Enhanced RSS+API' if use_enhanced else 'NewsAPI')
            else:
                print("[WARNING] No news items fetched. Using fallback.")
        except Exception as e:
            print("[ERROR] Error fetching news: {}".format(e))
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n[SKIP] Skipping news fetch (using existing data)")
        # Load existing news
        if os.path.exists('data/today_news.json'):
            with open('data/today_news.json', 'r', encoding='utf-8') as f:
                news_items = json.load(f)
                print("[OK] Loaded existing news: {} articles".format(len(news_items)))

    if asset_manager:
        asset_manager.add_workflow_step('News Fetching', 'fetch', 'completed',
            {'articles_count': len(news_items), 'use_enhanced': use_enhanced})
    
    # Step 1.5: Summarize and Generate Script
    script = None
    if use_summarization and create_video_script and not skip_audio:
        print("\n" + "="*70)
        print("STEP 1.5: Summarizing and Generating Video Script")
        print("="*70)
        try:
            print("[INFO] Generating script optimized for 60-second video (~900 chars)")
            script = create_video_script(news_items, max_total_chars=900)
            script_file = 'data/ai_news_audio_script.txt'
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script)
            print("[OK] Script generated: {} characters".format(len(script)))
            print("[OK] Saved to: {}".format(script_file))
            if asset_manager:
                asset_manager.add_asset('script', script_file, 'Generated video script',
                    source='HuggingFace BART summarization', 
                    metadata={'character_count': len(script), 'articles': len(news_items)})
        except Exception as e:
            print("[WARNING] Summarization failed, using standard script: {}".format(e))
            script = None

    if asset_manager:
        asset_manager.add_workflow_step('Text Summarization', 'summarize', 'completed',
            {'engine': 'HuggingFace BART' if use_summarization else 'basic', 'target_chars': 900})
    
    # Step 2: Generate TTS Audio
    if not skip_audio:
        print("\n" + "="*70)
        print("STEP 2: Generating Text-to-Speech Audio")
        print("="*70)
        try:
            audio_file = generate_audio_from_news()
            if audio_file:
                print("[OK] Audio generated: {}".format(audio_file))
                if asset_manager:
                    asset_manager.add_asset('audio', audio_file, 'TTS audio for video',
                        source='gTTS (Google Text-to-Speech)')
            else:
                print("[ERROR] Audio generation failed")
                return False
        except Exception as e:
            print("[ERROR] Error generating audio: {}".format(e))
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n[SKIP] Skipping audio generation (using existing audio)")

    if asset_manager:
        asset_manager.add_workflow_step('Audio Generation', 'generate', 'completed',
            {'engine': 'gTTS', 'language': 'en'})
    
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
                    if asset_manager:
                        asset_manager.add_asset('video', video, 'Generated video file',
                            source='MoviePy composition')
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

    if asset_manager:
        asset_manager.add_workflow_step('Video Composition', 'compose', 'completed',
            {'formats': 2, 'codec': 'h264'})
    
    # Step 4: Upload (placeholder for future implementation)
    print("\n" + "="*70)
    print("STEP 4: Upload to Social Media (Manual)")
    print("="*70)
    print("[INFO] YouTube/TikTok upload requires OAuth setup.")
    print("[INFO] Videos are ready in the 'output/' directory.")
    print("[INFO] Manual upload or configure YouTube Data API for automation.")
    
    # Step 5: Save Asset Manifest
    if asset_manager:
        print("\n" + "="*70)
        print("STEP 5: Saving Asset Manifest")
        print("="*70)
        try:
            manifest_file = asset_manager.save_manifest()
            print("[OK] Asset manifest saved: {}".format(manifest_file))
        except Exception as e:
            print("[WARNING] Asset manifest save skipped: {}".format(e))
    
    # Summary
    print("\n" + "="*70)
    print("[OK] PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print("[INFO] Output files:")
    print("[INFO]   - Videos: output/")
    print("[INFO]   - News: data/today_news.json")
    print("[INFO]   - Audio: data/ai_news_audio.mp3")
    print("[INFO]   - Manifest: data/asset_manifest_*.json")
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
        '--use-enhanced',
        action='store_true',
        default=True,
        help='Use enhanced news fetcher with RSS feeds'
    )
    parser.add_argument(
        '--use-summarization',
        action='store_true',
        default=True,
        help='Use HuggingFace summarization for 60-sec optimization'
    )
    parser.add_argument(
        '--target-duration',
        type=int,
        default=60,
        help='Target video duration in seconds'
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
