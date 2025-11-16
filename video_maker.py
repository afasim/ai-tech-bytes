#!/usr/bin/env python3
"""
Video Maker
Creates short-form videos from audio and text for YouTube/TikTok
Enhanced with professional animations from video_animations module (particles, smooth transitions, dynamic effects)"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import video_animations as va
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

def create_animated_gradient(width, height, color1=(20, 20, 40), color2=(40, 40, 80)):
    """Create a gradient background"""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        # Interpolate between two colors
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    return np.array(img)

def create_frame_with_text(width, height, text, bg_color=(20, 20, 40), text_color='white', font_size=50, add_decorations=True):
    """
    Create a PIL Image with text overlay and visual decorations
    """
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add decorative elements
    if add_decorations:
        # Top accent line
        draw.rectangle([(0, 0), (width, 10)], fill=(0, 150, 255))
        # Bottom accent line
        draw.rectangle([(0, height-10), (width, height)], fill=(0, 150, 255))
        # Side accents
        draw.rectangle([(0, 0), (10, height)], fill=(100, 100, 200))
        draw.rectangle([(width-10, 0), (width, height)], fill=(100, 100, 200))
    
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

def create_ai_icon_frame(width, height, text=""):
    """Create a frame with AI-themed visual elements"""
    img = Image.new('RGB', (width, height), color=(15, 15, 35))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw circular elements (representing AI/neural networks)
    center_x, center_y = width // 2, height // 2
    colors = [(0, 150, 255), (100, 200, 255), (150, 100, 255), (200, 100, 255)]
    
    # Draw concentric circles
    for i, color in enumerate(colors):
        radius = 200 - (i * 40)
        if radius > 0:
            bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
            draw.ellipse(bbox, outline=color, width=3)
    
    # Draw connecting nodes
    node_positions = [
        (center_x - 150, center_y - 150),
        (center_x + 150, center_y - 150),
        (center_x - 150, center_y + 150),
        (center_x + 150, center_y + 150),
        (center_x, center_y)
    ]
    
    for pos in node_positions:
        draw.ellipse(
            [pos[0] - 20, pos[1] - 20, pos[0] + 20, pos[1] + 20],
            fill=(0, 200, 255)
        )
    
    # Draw connecting lines
    for i in range(len(node_positions) - 1):
        draw.line([node_positions[i], node_positions[-1]], fill=(0, 150, 255), width=2)
    
    # Add text if provided
    if text:
        try:
            font_path = get_font_path()
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 60)
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 150
        
        draw.text((x, y), text, font=font, fill=(0, 200, 255))
    
    return np.array(img)

def create_animated_news_frame_enhanced(width, height, news_title, progress=0.5):
    """
    Enhanced animated frame with professional effects from video_animations module
    """
    # Create tech background with animated grid
    base_img = va.create_tech_background(width, height, progress)
    
    # Convert to PIL for compositing
    img = Image.fromarray(base_img.astype('uint8'), 'RGB')
    
    # Add animated text overlay
    text_img = va.create_animated_text(
        width, height, 
        f"Story: {news_title}",
        font_size=45, 
        progress=progress, 
        effect='slide'
    )
    img.paste(text_img, (0, 0), text_img)
    
    # Add animated shapes for visual interest
    shapes_img = va.create_animated_shapes(
        width, height, 
        progress=progress, 
        shape_type='circles'
    )
    img.paste(shapes_img, (0, 0), shapes_img)
    
    return np.array(img)

def create_animated_news_frame(width, height, news_title, progress=0.5):
    """
    Create an animated frame for displaying news article.
    progress: 0.0 to 1.0 indicating how far through this article we are
    """
    img = Image.new('RGB', (width, height), color=(20, 20, 50))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Create animated background with gradient based on progress
    color_start = (20, 20, 50)
    color_mid = (40, 60, 100)
    color_end = (60, 100, 150)
    
    # Interpolate color based on progress
    if progress < 0.5:
        ratio = progress * 2
        r = int(color_start[0] + (color_mid[0] - color_start[0]) * ratio)
        g = int(color_start[1] + (color_mid[1] - color_start[1]) * ratio)
        b = int(color_start[2] + (color_mid[2] - color_start[2]) * ratio)
    else:
        ratio = (progress - 0.5) * 2
        r = int(color_mid[0] + (color_end[0] - color_mid[0]) * ratio)
        g = int(color_mid[1] + (color_end[1] - color_mid[1]) * ratio)
        b = int(color_mid[2] + (color_end[2] - color_mid[2]) * ratio)
    
    bg_color = (r, g, b)
    
    # Fill background
    draw.rectangle([(0, 0), (width, height)], fill=bg_color)
    
    # Draw animated accent bar
    accent_height = 5
    accent_width = int(width * progress)
    draw.rectangle([(0, 0), (accent_width, accent_height)], fill=(0, 200, 255))
    
    # Draw animated circles (pulse effect based on progress)
    center_x, center_y = width // 2, height // 3
    pulse_radius = int(50 + 30 * np.sin(progress * np.pi))
    draw.ellipse(
        [center_x - pulse_radius, center_y - pulse_radius, 
         center_x + pulse_radius, center_y + pulse_radius],
        outline=(0, 200, 255),
        width=3
    )
    
    # Draw multiple pulsing rings
    for i in range(2):
        ring_radius = int(80 + 40 * np.sin(progress * np.pi - i * 0.5))
        if ring_radius > 0:
            draw.ellipse(
                [center_x - ring_radius, center_y - ring_radius,
                 center_x + ring_radius, center_y + ring_radius],
                outline=(100, 150, 255),
                width=2
            )
    
    # Draw animated bars (moving left to right)
    bar_height = 20
    bar_y = height // 2
    for i in range(5):
        bar_x = int((progress * width + i * width / 5) % width)
        draw.rectangle([(bar_x, bar_y), (bar_x + 100, bar_y + bar_height)], 
                      fill=(0, 150, 200))
    
    # Add news title with word wrapping
    try:
        font_path = get_font_path()
        if os.path.exists(font_path):
            title_font = ImageFont.truetype(font_path, 50)
            text_font = ImageFont.truetype(font_path, 35)
        else:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
    except Exception:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Wrap title text if too long
    title = "BREAKING NEWS"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, height * 0.6), title, font=title_font, fill=(0, 255, 200))
    
    # Wrap and display news article title
    max_chars = 40 if width < 1200 else 50
    if len(news_title) > max_chars:
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
        news_text = "\n".join(lines[:3])  # Max 3 lines
    else:
        news_text = news_title
    
    news_y = height * 0.75
    draw.text((40, int(news_y)), news_text, font=text_font, fill=(200, 200, 255))
    
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
    Create a video with audio and animated news frames that change per article
    """
    try:
        # Load audio and news data
        print("Loading audio file...")
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print("Audio duration: {:.2f} seconds".format(duration))
        
        # Load news items to display
        try:
            with open('data/today_news.json', 'r', encoding='utf-8') as f:
                news_data = json.load(f)
                news_items = news_data.get('articles', [])
        except:
            news_items = []
        
        # Get video settings for platform
        settings = VIDEO_SETTINGS.get(platform, VIDEO_SETTINGS['youtube_shorts'])
        width = settings['width']
        height = settings['height']
        fps = settings['fps']
        
        print("Creating animated visual frames for {} news items...".format(len(news_items)))
        
        # Create opening frame
        title_text = "AI TECH BYTES"
        subtitle_text = "Daily AI News Update"
        opening_frame = create_frame_with_text(
            width, height, 
            "{}\n\n{}".format(title_text, subtitle_text),
            bg_color=(20, 20, 40),
            text_color='cyan',
            font_size=80,
            add_decorations=True
        )
        opening_clip = ImageClip(opening_frame).set_duration(3)
        
        # Calculate duration per article
        num_articles = len(news_items)
        content_duration = duration - 3 - 2  # Minus opening and closing
        duration_per_article = content_duration / num_articles if num_articles > 0 else content_duration
        
        # Create animated frames for each news article
        all_clips = [opening_clip]
        
        for idx, news_item in enumerate(news_items):
            title = news_item.get('title', 'AI News')
            
            # Create multiple frames with animation for this article
            num_frames = max(int(duration_per_article * fps / 10), 3)  # Create frame every 1/10th second
            
            for frame_num in range(num_frames):
                progress = frame_num / (num_frames - 1) if num_frames > 1 else 0.5
                
                animated_frame = create_animated_news_frame_enhanced(
                    width, height, 
                    "Story {}: {}".format(idx + 1, title),
                    progress=progress
                )
                
                frame_clip = ImageClip(animated_frame).set_duration(1.0 / fps * 10)
                all_clips.append(frame_clip)
        
        # Create closing frame
        closing_text = "Thank you for watching!\nSubscribe for more AI news"
        closing_frame = create_frame_with_text(
            width, height,
            closing_text,
            bg_color=(30, 30, 50),
            text_color='white',
            font_size=60,
            add_decorations=True
        )
        closing_clip = ImageClip(closing_frame).set_duration(2)
        all_clips.append(closing_clip)
        
        # Composite all clips
        print("Compositing video with {} clips...".format(len(all_clips)))
        video = concatenate_videoclips(all_clips)
        
        # Add audio
        video = video.set_audio(audio)
        
        # Create output directory
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write video file
        print("Writing video to {}...".format(output_file))
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
        
        print("\n[OK] Video created successfully: {}".format(output_file))
        print("  Duration: {:.2f}s".format(duration))
        print("  Resolution: {}x{}".format(width, height))
        print("  Platform: {}".format(platform))
        
        return output_file
        
    except Exception as e:
        print("[ERROR] Error creating video: {}".format(e))
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
