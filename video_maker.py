#!/usr/bin/env python3
"""
Video Maker
Creates short-form videos from audio and text for YouTube/TikTok
Enhanced with professional animations from video_animations module (particles, smooth transitions, dynamic effects)
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
)
import librosa # <-- Import librosa
import video_animations as va # <-- Import your animations file

# Video settings for social media
VIDEO_SETTINGS = {
    'youtube_shorts': {'width': 1080, 'height': 1920, 'fps': 24},  # 9:16
    'tiktok': {'width': 1080, 'height': 1920, 'fps': 24},          # 9:16
    'youtube': {'width': 1920, 'height': 1080, 'fps': 24},         # 16:9
}

# This function is now a helper, we will call the enhanced one
def create_frame_with_text(width, height, text, bg_color=(20, 20, 40), text_color='white', font_size=50):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font_path = va.get_font_path()
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=text_color, align="center")
    return np.array(img)


def create_animated_scene(width, height, particle_system, text, text_effect='pulse', shape='circles', progress=0.0, audio_level=0.0):
    """
    Creates a single, fully composited frame for intro/outro.
    This combines background, particles, shapes, and text.
    """
    # 1. Create animated background
    base_img = va.create_tech_background(width, height, progress, audio_level)
    
    # 2. Update and draw particle system
    particle_system.update(audio_level)
    draw = ImageDraw.Draw(base_img, 'RGBA')
    particle_system.draw(draw)
    
    # 3. Create and composite animated shapes
    shapes_img = va.create_animated_shapes(width, height, progress, shape, audio_level)
    base_img.paste(shapes_img, (0, 0), shapes_img) # Paste with alpha
    
    # 4. Create and composite animated text
    font_size = 80 if width < 1200 else 100 # Larger font for title
    text_img = va.create_animated_text(width, height, text, font_size, progress, text_effect, audio_level)
    base_img.paste(text_img, (0, 0), text_img) # Paste with alpha
    
    return np.array(base_img)

def create_animated_news_frame_enhanced(width, height, particle_system, news_title, progress=0.0, audio_level=0.0):
    """
    Enhanced animated frame with professional effects from video_animations module
    """
    # 1. Create tech background
    base_img = va.create_tech_background(width, height, progress, audio_level)
    
    # 2. Update and draw particle system
    particle_system.update(audio_level)
    draw = ImageDraw.Draw(base_img, 'RGBA')
    particle_system.draw(draw)
    
    # 3. Add animated shapes for visual interest
    shapes_img = va.create_animated_shapes(width, height, progress, 'hexagon', audio_level)
    base_img.paste(shapes_img, (0, 0), shapes_img)
    
    # 4. Add animated text overlay (wrapped)
    font_size = 45 if width < 1200 else 60
    
    # Simple word wrapping
    max_chars = 40
    words = news_title.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    wrapped_text = "\n".join(lines[:3]) # Max 3 lines
    
    text_img = va.create_animated_text(width, height, wrapped_text, font_size, progress, 'slide', audio_level)
    base_img.paste(text_img, (0, 0), text_img)
    
    return np.array(base_img)


def create_video_from_audio(
    audio_file='data/ai_news_audio.mp3',
    output_file='output/ai_tech_bytes.mp4',
    platform='youtube_shorts'
):
    """
    Create a video with audio and animated news frames that change per article
    """
    try:
        # Load audio and get settings
        print("Loading audio file...")
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print(f"Audio duration: {duration:.2f} seconds")
        
        settings = VIDEO_SETTINGS.get(platform, VIDEO_SETTINGS['youtube_shorts'])
        width, height, fps = settings['width'], settings['height'], settings['fps']

        # --- AUDIO ANALYSIS (NEW) ---
        print("Analyzing audio with Librosa...")
        y, sr = librosa.load(audio_file, sr=8000)
        # Get Root-Mean-Square (RMS) energy, a good proxy for volume
        rms = librosa.feature.rms(y=y)[0]
        # Normalize RMS to be between 0.0 and 1.0
        rms_normalized = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)
        
        # Interpolate audio data to match the number of video frames
        total_video_frames = math.ceil(duration * fps)
        # Create an array of frame indices [0, 1, 2, ..., total_video_frames-1]
        video_frame_indices = np.arange(total_video_frames)
        # Create an array of audio sample indices
        audio_sample_indices = np.linspace(0, len(rms_normalized) - 1, total_video_frames)
        # Interpolate: Map audio data to video frames
        amplitude_frames = np.interp(video_frame_indices, np.arange(len(rms_normalized)), rms_normalized)
        print(f"Analyzed audio and mapped to {len(amplitude_frames)} video frames.")
        # --- END OF AUDIO ANALYSIS ---

        # Load news items
        news_items = []
        try:
            with open('data/today_news.json', 'r', encoding='utf-8') as f:
                news_data = json.load(f)
                news_items = news_data.get('articles', [])
        except Exception as e:
            print(f"Warning: Could not load news data. Using default. Error: {e}")
        
        if not news_items:
            news_items = [{'title': 'Thanks for tuning in! No news items found.'}]

        # Durations
        intro_duration = 3.0
        outro_duration = 3.0
        content_duration = duration - intro_duration - outro_duration
        
        if content_duration < 0:
            print("Warning: Audio is very short. Adjusting scene durations.")
            intro_duration = min(1.0, duration * 0.4)
            outro_duration = min(1.0, duration * 0.4)
            content_duration = duration - intro_duration - outro_duration
            if content_duration < 0: content_duration = 0

        num_articles = len(news_items)
        duration_per_article = content_duration / num_articles if num_articles > 0 else 0

        # --- FRAME GENERATION LOOP (REFACTORED) ---
        print("Creating animated visual frames...")
        all_clips = []
        frame_counter = 0 # Global frame counter
        
        # Initialize Particle System
        particle_sys = va.ParticleSystem(width, height, num_particles=100)
        
        # 1. Create Intro Frames
        intro_frames = int(intro_duration * fps)
        for i in range(intro_frames):
            if frame_counter >= total_video_frames: break
            progress = i / (intro_frames - 1) if intro_frames > 1 else 0
            audio_level = amplitude_frames[frame_counter]
            
            frame = create_animated_scene(
                width, height, particle_sys, 
                "AI TECH BYTES\nDaily News Update", 
                text_effect='zoom', shape='lines',
                progress=progress, audio_level=audio_level
            )
            all_clips.append(ImageClip(frame).set_duration(1.0 / fps))
            frame_counter += 1

        # 2. Create News Article Frames
        for idx, news_item in enumerate(news_items):
            title = news_item.get('title', 'AI News')
            num_frames_for_article = int(duration_per_article * fps)
            
            for i in range(num_frames_for_article):
                if frame_counter >= total_video_frames: break
                progress = i / (num_frames_for_article - 1) if num_frames_for_article > 1 else 0
                audio_level = amplitude_frames[frame_counter]
                
                frame = create_animated_news_frame_enhanced(
                    width, height, particle_sys,
                    f"Story {idx + 1}: {title}",
                    progress=progress,
                    audio_level=audio_level
                )
                all_clips.append(ImageClip(frame).set_duration(1.0 / fps))
                frame_counter += 1

        # 3. Create Outro Frames
        # Fill remaining time with outro
        outro_frames = total_video_frames - frame_counter
        for i in range(outro_frames):
            if frame_counter >= total_video_frames: break
            progress = i / (outro_frames - 1) if outro_frames > 1 else 0
            audio_level = amplitude_frames[frame_counter]
            
            frame = create_animated_scene(
                width, height, particle_sys,
                "Thanks for watching!\nSubscribe for more.",
                text_effect='fade', shape='circles',
                progress=progress, audio_level=audio_level
            )
            all_clips.append(ImageClip(frame).set_duration(1.0 / fps))
            frame_counter += 1

        print(f"Generated {len(all_clips)} total frames.")
        # --- END OF FRAME GENERATION ---

        # Composite all clips
        video = concatenate_videoclips(all_clips)
        
        # Ensure video duration exactly matches audio
        video = video.set_duration(duration)
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
            preset='ultrafast'
        )

        print(f"\n[OK] Video created successfully: {output_file}")
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
    
    # Ensure data/output dirs exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # Check for dummy audio/news if they don't exist (for testing)
    if not os.path.exists('data/ai_news_audio.mp3'):
        print("Warning: 'data/ai_news_audio.mp3' not found. Please generate it first.")
        # As a fallback, we could try to create a dummy, but for now we'll just exit
        exit()
        
    if not os.path.exists('data/today_news.json'):
         print("Warning: 'data/today_news.json' not found. Creating dummy file.")
         dummy_news = {"articles": [{"title": "Dummy News: AI Takes Over"}, {"title": "Another Story: Python is Great"}]}
         with open('data/today_news.json', 'w') as f:
             json.dump(dummy_news, f)

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
