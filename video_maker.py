#!/usr/bin/env python3
"""
Video Maker
Creates short-form videos from audio and text for YouTube/TikTok
Uses PIL for text rendering to avoid ImageMagick dependency
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
)

# Video settings for social media
VIDEO_SETTINGS = {
    'youtube_shorts': {'width': 1080, 'height': 1920, 'fps': 30},  # 9:16
    'tiktok': {'width': 1080, 'height': 1920, 'fps': 30},         # 9:16
    'youtube': {'width': 1920, 'height': 1080, 'fps': 30},        # 16:9
}

def get_font_path():
    """Get available font for the system"""
    if os.name == 'nt':  # Windows
        return 'C:\\Windows\\Fonts\\arial.ttf'
    else:  # macOS/Linux
        return '/System/Library/Fonts/Arial.ttf'

def create_frame_with_text(width, height, text, bg_color=(20, 20, 40), text_color='white', font_size=50):
    """
    Create a PIL Image with text overlay
    """
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a system font
    try:
        font_path = get_font_path()
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with shadow effect
    shadow_offset = 2
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 128))
    draw.text((x, y), text, font=font, fill=text_color)
    
    return np.array(img)


def load_script(script_file='data/ai_news_audio_script.txt'):
    """
    Load the generated script
    """
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "AI Tech Bytes - Your daily AI news update!"

def create_video_from_audio(
    audio_file='data/ai_news_audio.mp3',
    output_file='output/ai_tech_bytes.mp4',
    platform='youtube_shorts'
):
    """
    Create a video with audio and text overlay using PIL for text rendering
    """
    try:
        # Load audio
        print("Loading audio file...")
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print(f"Audio duration: {duration:.2f} seconds")
        
        # Get video settings for platform
        settings = VIDEO_SETTINGS.get(platform, VIDEO_SETTINGS['youtube_shorts'])
        width = settings['width']
        height = settings['height']
        fps = settings['fps']
        
        # Create title frame
        title_text = "AI TECH BYTES"
        subtitle_text = "Daily AI News Update"
        
        # Create opening frame with title
        title_frame = create_frame_with_text(
            width, height, 
            f"{title_text}\n\n{subtitle_text}",
            bg_color=(20, 20, 40),
            text_color='cyan',
            font_size=80
        )
        
        # Create closing frame
        closing_text = "Thank you for watching!\nSubscribe for more AI news"
        closing_frame = create_frame_with_text(
            width, height,
            closing_text,
            bg_color=(30, 30, 50),
            text_color='white',
            font_size=60
        )
        
        # Create clips
        title_clip = ImageClip(title_frame).set_duration(2)
        closing_clip = ImageClip(closing_frame).set_duration(2)
        
        # Composite video with title, background, and closing
        video = concatenate_videoclips([title_clip, closing_clip])
        
        # Add audio
        video = video.set_audio(audio)
        
        # Create output directory
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write video file
        print(f"Writing video to {output_file}...")
        video.write_videofile(
            output_file,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            threads=4,
            preset='fast',
            verbose=False,
            logger=None
        )
        
        print(f"\n[OK] Video created successfully: {output_file}")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Resolution: {width}x{height}")
        print(f"  Platform: {platform}")
        
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Error creating video: {e}")
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
        print(f"[OK] Successfully created {len(videos)} video(s):")
        for video in videos:
            print(f"  - {video}")
        print(f"{'='*60}")
    else:
        print("\n[ERROR] No videos were created")
