#!/usr/bin/env python3
"""
Enhanced Video Animations
Professional-grade animation effects for AI news videos
Uses PIL, NumPy for particle systems, smooth transitions, and dynamic effects
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

class ParticleSystem:
    """Dynamic particle system for animated backgrounds"""
    
    def __init__(self, width, height, num_particles=50):
        self.width = width
        self.height = height
        self.particles = []
        for _ in range(num_particles):
            self.particles.append({
                'x': random.uniform(0, width),
                'y': random.uniform(0, height),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'size': random.randint(2, 8),
                'color': (random.randint(100, 255), random.randint(100, 255), 255),
                'alpha': random.randint(100, 255)
            })
    
    def update(self):
        """Update particle positions"""
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around screen
            if p['x'] < 0: p['x'] = self.width
            if p['x'] > self.width: p['x'] = 0
            if p['y'] < 0: p['y'] = self.height
            if p['y'] > self.height: p['y'] = 0
    
    def draw(self, draw):
        """Draw particles on image"""
        for p in self.particles:
            x, y = int(p['x']), int(p['y'])
            size = p['size']
            color = p['color']
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

def create_gradient_background(width, height, colors, direction='vertical', progress=0.0):
    """
    Create animated gradient background
    direction: 'vertical', 'horizontal', 'radial', 'diagonal'
    progress: 0.0-1.0 for animation
    """
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    # Animate color shift based on progress
    shift = int(progress * 100)
    
    for y in range(height):
        for x in range(width):
            if direction == 'vertical':
                ratio = (y + shift) % height / height
            elif direction == 'horizontal':
                ratio = (x + shift) % width / width
            elif direction == 'diagonal':
                ratio = ((x + y + shift) % (width + height)) / (width + height)
            else:  # radial
                dx = x - width/2
                dy = y - height/2
                ratio = (math.sqrt(dx*dx + dy*dy) + shift) % (width/2) / (width/2)
            
            # Interpolate between colors
            color_index = ratio * (len(colors) - 1)
            idx1 = int(color_index)
            idx2 = min(idx1 + 1, len(colors) - 1)
            local_ratio = color_index - idx1
            
            c1, c2 = colors[idx1], colors[idx2]
            r = int(c1[0] + (c2[0] - c1[0]) * local_ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * local_ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * local_ratio)
            
            pixels[x, y] = (r, g, b)
    
    return img

def create_animated_text(width, height, text, font_size=60, progress=0.0, effect='slide'):
    """
    Create animated text with various effects
    effect: 'slide', 'zoom', 'fade', 'wave'
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    try:
        if os.name == 'nt':
            font = ImageFont.truetype('C:\\Windows\\Fonts\\arial.ttf', font_size)
        else:
            font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if effect == 'slide':
        # Slide in from left
        x = int(-text_width + (width + text_width) * progress)
        y = (height - text_height) // 2
    elif effect == 'zoom':
        # Zoom in effect
        scale = 0.1 + 0.9 * progress
        temp_font_size = int(font_size * scale)
        try:
            if os.name == 'nt':
                font = ImageFont.truetype('C:\\Windows\\Fonts\\arial.ttf', temp_font_size)
            else:
                font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', temp_font_size)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    elif effect == 'wave':
        # Wave effect - draw character by character
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        for i, char in enumerate(text):
            char_y = y + int(10 * math.sin(progress * math.pi * 2 + i * 0.5))
            draw.text((x, char_y), char, font=font, fill=(255, 255, 255, 255))
            char_bbox = draw.textbbox((0, 0), char, font=font)
            x += char_bbox[2] - char_bbox[0]
        return img
    else:  # fade
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        alpha = int(255 * progress)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))
        return img
    
    # Draw text with glow effect
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=(0, 100, 255, 100))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    return img

def create_animated_shapes(width, height, progress=0.0, shape_type='hexagon'):
    """
    Create animated geometric shapes
    shape_type: 'hexagon', 'circles', 'lines', 'grid'
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = width // 2, height // 2
    
    if shape_type == 'hexagon':
        # Rotating hexagons
        for i in range(3):
            radius = 100 + i * 60
            angle_offset = progress * 360 + i * 20
            points = []
            for j in range(6):
                angle = math.radians(angle_offset + j * 60)
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                points.append((x, y))
            draw.polygon(points, outline=(0, 150 + i*30, 255), width=3)
    
    elif shape_type == 'circles':
        # Pulsing concentric circles
        for i in range(5):
            radius_base = 50 + i * 40
            pulse = 10 * math.sin(progress * math.pi * 2 - i * 0.3)
            radius = int(radius_base + pulse)
            alpha = int(255 - i * 40)
            draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius],
                        outline=(100, 200, 255), width=2)
    
    elif shape_type == 'lines':
        # Animated connection lines
        num_points = 8
        points = []
        for i in range(num_points):
            angle = math.radians(i * 360 / num_points + progress * 180)
            radius = 150
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((int(x), int(y)))
        
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                draw.line([points[i], points[j]], fill=(0, 150, 255), width=1)
    
    return img

def apply_transition(img1, img2, progress, transition_type='fade'):
    """
    Apply transition between two images
    transition_type: 'fade', 'slide', 'wipe', 'dissolve'
    """
    if transition_type == 'fade':
        # Simple crossfade
        return Image.blend(img1.convert('RGBA'), img2.convert('RGBA'), progress)
    
    elif transition_type == 'slide':
        # Slide transition
        result = img1.copy()
        width = img1.width
        offset = int(width * progress)
        result.paste(img2.crop((0, 0, offset, img2.height)), (0, 0))
        return result
    
    elif transition_type == 'wipe':
        # Wipe from left to right
        result = img1.copy()
        width = int(img1.width * progress)
        if width > 0:
            result.paste(img2.crop((0, 0, width, img2.height)), (0, 0))
        return result
    
    return img1

def create_tech_background(width, height, progress=0.0):
    """
    Create animated tech-themed background with grid and particles
    """
    # Create base gradient
    colors = [(10, 10, 30), (30, 30, 60), (20, 40, 80), (10, 10, 30)]
    img = create_gradient_background(width, height, colors, 'radial', progress)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw animated grid
    grid_spacing = 50
    offset = int(progress * grid_spacing)
    for x in range(-grid_spacing + offset, width + grid_spacing, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(30, 50, 100, 50), width=1)
    for y in range(-grid_spacing + offset, height + grid_spacing, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(30, 50, 100, 50), width=1)
    
    # Add glowing dots at intersections
    for x in range(-grid_spacing + offset, width + grid_spacing, grid_spacing):
        for y in range(-grid_spacing + offset, height + grid_spacing, grid_spacing):
            if random.random() > 0.7:
                intensity = int(100 + 155 * (0.5 + 0.5 * math.sin(progress * math.pi * 4)))
                draw.ellipse([x-3, y-3, x+3, y+3], fill=(0, intensity, 255, 200))
    
    return img

import os  # Import at top of actual use
