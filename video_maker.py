#!/usr/bin/env python3
"""
Video Maker
Creates short-form videos from audio and text for YouTube/TikTok
"""

import os
import json
from moviepy.editor import (
    AudioFileClip, TextClip, CompositeVideoClip, 
    ColorClip, concatenate_videoclips
)
from moviepy.video.fx import fadein, fadeout

# Video settings for social media
VIDEO_SETTINGS = {
    'youtube_shorts': {'width': 1080, 'height': 1920, 'fps': 30},  # 9:16
    'tiktok': {'width': 1080, 'height': 1920, 'fps': 30},         # 9:16
    'youtube': {'width': 1920, 'height': 1080, 'fps': 30},        # 16:9
}

def load_script(script_file='data/ai_news_audio_script.txt'):
    """
    Load the generated script
    """
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "AI Tech Bytes - Your daily AI news update!"

def create_text_clip(text, duration, video_size=(1080, 1920)):
    """
    Create a text clip with styling
    """
    txt_clip = TextClip(
        text,
        fontsize=70,
        color='white',
        font='Arial-Bold',
        size=video_size,
        method='caption',
        align='center'
    ).set_duration(duration)
    
    return txt_clip

def create_video_from_audio(
    audio_file='data/ai_news_audio.mp3',
    output_file='output/ai_tech_bytes.mp4',
    platform='youtube_shorts'
):
    """
    Create a video with audio and text overlay
    """
    try:
        # Load audio
        print("Loading audio file...")
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print(f"Audio duration: {duration:.2f} seconds")
        
        # Get video settings for platform
        settings = VIDEO_SETTINGS.get(platform, VIDEO_SETTINGS['youtube_shorts'])
        video_size = (settings['width'], settings['height'])
        
        # Create background
        print("Creating video background...")
        background = ColorClip(
            size=video_size,
            color=(20, 20, 40),  # Dark blue background
            duration=duration
        )
        
        # Create title
        title_text = "AI TECH BYTES"
        title_clip = TextClip(
            title_text,
            fontsize=90,
            color='cyan',
            font='Arial-Bold',
            size=video_size,
            method='caption',
            align='center'
        ).set_position(('center', 100)).set_duration(duration)
        
        # Create subtitle (static for now - could be made dynamic)
        subtitle_text = "Daily AI News Update"
        subtitle_clip = TextClip(
            subtitle_text,
            fontsize=50,
            color='white',
            font='Arial',
            size=(video_size[0] - 100, None),
            method='caption',
            align='center'
        ).set_position(('center', 'center')).set_duration(duration)
        
        # Composite video
        print("Compositing video layers...")
        video = CompositeVideoClip([
            background,
            title_clip,
            subtitle_clip
        ])
        
        # Add audio
        video = video.set_audio(audio)
        
        # Create output directory
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write video file
        print(f"Writing video to {output_file}...")
        video.write_videofile(
            output_file,
            fps=settings['fps'],
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            threads=4,
            preset='medium'
        )
        
        print(f"\n✓ Video created successfully: {output_file}")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Resolution: {video_size[0]}x{video_size[1]}")
        print(f"  Platform: {platform}")
        
        return output_file
        
    except Exception as e:
        print(f"Error creating video: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_multiple_formats(audio_file='data/ai_news_audio.mp3'):
    """
    Create videos in multiple formats for different platforms
    """
    platforms = ['youtube_shorts', 'youtube']
    created_videos = []
    
    for platform in platforms:
        output_file = f'output/ai_tech_bytes_{platform}.mp4'
        print(f"\n{'='*60}")
        print(f"Creating video for {platform}...")
        print(f"{'='*60}")
        
        result = create_video_from_audio(
            audio_file=audio_file,
            output_file=output_file,
            platform=platform
        )
        
        if result:
            created_videos.append(result)
    
    return created_videos

if __name__ == "__main__":
    print("=== AI Tech Bytes - Video Maker ===")
    print("\nCreating videos for multiple platforms...\n")
    
    videos = create_multiple_formats()
    
    if videos:
        print(f"\n\n{'='*60}")
        print(f"✓ Successfully created {len(videos)} video(s):")
        for video in videos:
            print(f"  - {video}")
        print(f"{'='*60}")
    else:
        print("\n✗ No videos were created")
