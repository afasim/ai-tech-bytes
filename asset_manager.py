#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asset Manager
Generates JSON specifications for all video assets and components
Used for tracking, reproducibility, and cloud deployment
"""

import os
import json
from datetime import datetime
import hashlib


class AssetManager:
    """Manages video asset metadata and specifications"""
    
    def __init__(self, project_name="AI Tech Bytes", date_str=None):
        self.project_name = project_name
        self.date_str = date_str or datetime.now().strftime('%Y-%m-%d')
        self.assets = {}
        self.manifest = {
            'project': project_name,
            'date': self.date_str,
            'version': '2.0',
            'generated': datetime.now().isoformat(),
            'assets': [],
            'workflow_steps': []
        }
    
    def add_asset(self, asset_type, filename, description, source=None, metadata=None):
        """
        Add an asset to the manifest
        
        Args:
            asset_type: 'news', 'script', 'audio', 'video', 'image', 'metadata'
            filename: Path to the asset file
            description: Human-readable description
            source: Where the asset came from (API, RSS, etc.)
            metadata: Additional metadata dict
        """
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            with open(filename, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
        else:
            file_size = 0
            file_hash = None
        
        asset = {
            'type': asset_type,
            'filename': filename,
            'description': description,
            'source': source,
            'file_size_bytes': file_size,
            'md5_hash': file_hash,
            'created': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.manifest['assets'].append(asset)
        print("[OK] Added asset: {} ({})".format(filename, asset_type))
        
        return asset
    
    def add_workflow_step(self, step_name, step_type, status, details=None):
        """
        Add a workflow step to the manifest
        
        Args:
            step_name: Name of the step (e.g., 'News Fetching')
            step_type: Type (fetch, summarize, generate, compose, export)
            status: 'pending', 'in_progress', 'completed', 'failed'
            details: Optional details dict
        """
        step = {
            'name': step_name,
            'type': step_type,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        self.manifest['workflow_steps'].append(step)
        return step
    
    def generate_asset_spec(self, news_items, script_text, audio_duration, video_info):
        """
        Generate a complete asset specification
        
        Args:
            news_items: List of news article dicts
            script_text: Generated video script
            audio_duration: Duration in seconds
            video_info: Dict with video properties
        
        Returns:
            Complete asset spec as dict
        """
        spec = {
            'id': "{}_{}_{}".format(
                self.project_name.replace(' ', '_').lower(),
                self.date_str.replace('-', ''),
                datetime.now().strftime('%H%M%S')
            ),
            'date': self.date_str,
            'content': {
                'news_count': len(news_items),
                'articles': [
                    {
                        'order': i + 1,
                        'title': item.get('title', ''),
                        'source': item.get('source', ''),
                        'character_count': len(item.get('description', ''))
                    }
                    for i, item in enumerate(news_items)
                ],
                'script': {
                    'total_characters': len(script_text),
                    'estimated_words': len(script_text.split()),
                    'estimated_duration_seconds': len(script_text.split()) / 2.5  # ~2.5 words/sec
                }
            },
            'audio': {
                'duration_seconds': audio_duration,
                'format': 'mp3',
                'sample_rate': 44100,
                'bitrate': '128k',
                'voice_engine': 'gTTS'
            },
            'video': video_info or {
                'formats': [
                    {
                        'name': 'YouTube Shorts',
                        'resolution': '1080x1920',
                        'aspect_ratio': '9:16',
                        'fps': 30,
                        'codec': 'h264',
                        'duration_seconds': audio_duration
                    },
                    {
                        'name': 'YouTube Standard',
                        'resolution': '1920x1080',
                        'aspect_ratio': '16:9',
                        'fps': 30,
                        'codec': 'h264',
                        'duration_seconds': audio_duration
                    }
                ]
            },
            'optimization': {
                'target_duration_seconds': 60,
                'target_character_count': 900,
                'ai_summarization': True,
                'animated_visuals': True,
                'text_overlay_accessibility': True
            },
            'delivery': {
                'platforms': ['YouTube', 'TikTok', 'YouTube Shorts', 'Instagram Reels'],
                'file_format': 'mp4',
                'color_profile': 'sRGB',
                'subtitles': 'Available'
            }
        }
        
        return spec
    
    def save_manifest(self, filename=None):
        """
        Save the asset manifest to JSON file
        """
        if filename is None:
            filename = "data/asset_manifest_{}.json".format(self.date_str)
        
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)
        
        print("[OK] Manifest saved to: {}".format(filename))
        return filename
    
    def save_asset_spec(self, spec, filename=None):
        """
        Save asset specification to JSON file
        """
        if filename is None:
            filename = "data/asset_spec_{}.json".format(spec.get('id', 'unknown'))
        
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        
        print("[OK] Asset spec saved to: {}".format(filename))
        return filename


def create_complete_asset_manifest(news_items, script_text, audio_duration):
    """
    Convenience function to create a complete asset manifest
    """
    manager = AssetManager()
    
    # Add workflow steps
    manager.add_workflow_step('News Fetching', 'fetch', 'completed',
        {'articles_count': len(news_items), 'sources': ['NewsAPI', 'RSS Feeds']})
    manager.add_workflow_step('Text Summarization', 'summarize', 'completed',
        {'engine': 'HuggingFace BART', 'target_length': 900})
    manager.add_workflow_step('Audio Generation', 'generate', 'completed',
        {'engine': 'gTTS', 'duration': audio_duration})
    manager.add_workflow_step('Video Composition', 'compose', 'completed',
        {'formats': 2, 'resolution_1': '1080x1920', 'resolution_2': '1920x1080'})
    
    # Generate spec
    video_info = {
        'formats': [
            {
                'name': 'YouTube Shorts',
                'resolution': '1080x1920',
                'aspect_ratio': '9:16',
                'fps': 30,
                'duration': audio_duration
            },
            {
                'name': 'YouTube Standard',
                'resolution': '1920x1080',
                'aspect_ratio': '16:9',
                'fps': 30,
                'duration': audio_duration
            }
        ]
    }
    
    spec = manager.generate_asset_spec(news_items, script_text, audio_duration, video_info)
    
    return manager, spec


if __name__ == "__main__":
    print("=== AI Tech Bytes - Asset Manager ===\n")
    
    # Example usage
    sample_news = [
        {"title": "Article 1", "source": "NewsAPI", "description": "Description 1"},
        {"title": "Article 2", "source": "RSS Feed", "description": "Description 2"},
    ]
    
    sample_script = "Welcome to AI Tech Bytes. Today's top stories..."
    sample_duration = 42.5
    
    manager, spec = create_complete_asset_manifest(sample_news, sample_script, sample_duration)
    
    print("\nAsset Specification:")
    print(json.dumps(spec, indent=2))
    
    manager.save_manifest()
    manager.save_asset_spec(spec)
