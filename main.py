#!/usr/bin/env python3
"""
AI Tech Bytes - Main Orchestrator
Automated pipeline: Fetch AI news -> Generate TTS -> Create Video -> Upload
"""

import os
import sys
import argparse
from datetime import datetime

# Import modules
from news_fetcher import fetch_ai_news, save_news_to_file
from tts_generator import generate_audio_from_news
from video_maker import create_multiple_formats

def print_banner():
    """Print application banner"""
    print("="*70)
    print("  █████╗ ██╗    ████████╗███████╗ ██████╗██╗  ██╗")
    print(" ██╔══██╗██║    ╚══██╔══╝██╔════╝██╔════╝██║  ██║")
    print(" ███████║██║       ██║   █████╗  ██║     ███████║")
    print(" ██╔══██║██║       ██║   ██╔══╝  ██║     ██╔══██║")
    print(" ██║  ██║██║       ██║   ███████╗╚██████╗██║  ██║")
    print(" ╚═╝  ╚═╝╚═╝       ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝")
    print("")
    print("           BYTES - Automated Video Creator")
    print("="*70)
    print()

def run_pipeline(skip_news=False, skip_audio=False, skip_video=False):
    """
    Run the complete pipeline
    """
    print_banner()
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting pipeline...\n")
    
    # Step 1: Fetch AI News
    if not skip_news:
        print("\n" + "="*70)
        print("STEP 1: Fetching AI News")
        print("="*70)
        try:
            news_items = fetch_ai_news(num_articles=3)
            if news_items:
                news_file = save_news_to_file(news_items)
                print(f"✓ News fetched and saved: {news_file}")
            else:
                print("✗ No news items fetched. Using fallback.")
        except Exception as e:
            print(f"✗ Error fetching news: {e}")
            return False
    else:
        print("\n⏩ Skipping news fetch (using existing data)")
    
    # Step 2: Generate TTS Audio
    if not skip_audio:
        print("\n" + "="*70)
        print("STEP 2: Generating Text-to-Speech Audio")
        print("="*70)
        try:
            audio_file = generate_audio_from_news()
            if audio_file:
                print(f"✓ Audio generated: {audio_file}")
            else:
                print("✗ Audio generation failed")
                return False
        except Exception as e:
            print(f"✗ Error generating audio: {e}")
            return False
    else:
        print("\n⏩ Skipping audio generation (using existing audio)")
    
    # Step 3: Create Videos
    if not skip_video:
        print("\n" + "="*70)
        print("STEP 3: Creating Videos for Multiple Platforms")
        print("="*70)
        try:
            videos = create_multiple_formats()
            if videos:
                print(f"\n✓ Created {len(videos)} video(s)")
                for video in videos:
                    print(f"  - {video}")
            else:
                print("✗ Video creation failed")
                return False
        except Exception as e:
            print(f"✗ Error creating videos: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n⏩ Skipping video creation (using existing videos)")
    
    # Step 4: Upload (placeholder for future implementation)
    print("\n" + "="*70)
    print("STEP 4: Upload to Social Media (Manual)")
    print("="*70)
    print("ℹ️  YouTube/TikTok upload requires OAuth setup.")
    print("ℹ️  Videos are ready in the 'output/' directory.")
    print("ℹ️  Manual upload or configure YouTube Data API for automation.")
    
    # Summary
    print("\n" + "="*70)
    print("✓ PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Done!\n")
    
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
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
