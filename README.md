# 🤖 AI Tech Bytes

**Automated AI Tech Byte video creator** - Fetches AI news, generates TTS audio, creates videos, and posts to YouTube/TikTok.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Overview

AI Tech Bytes is an end-to-end automated system for creating daily AI news video content. The pipeline fetches the latest AI news from various sources, converts it to speech using Google TTS, creates engaging short-form videos, and prepares them for upload to social media platforms.

### Features

- ✅ **Automated News Fetching**: Pulls latest AI news from NewsAPI
- ✅ **Text-to-Speech**: Converts news articles into natural-sounding narration using gTTS
- ✅ **Video Generation**: Creates professional videos with text overlays and branding
- ✅ **Multi-Platform Support**: Generates videos in formats for YouTube Shorts, TikTok, and standard YouTube
- ✅ **Customizable**: Easy to modify scripts, styling, and content sources
- ✅ **Free Tools**: Uses only free and open-source libraries

## 📋 Prerequisites

- Python 3.8 or higher
- FFmpeg (required for video processing)
- NewsAPI key (free tier available)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/afasim/ai-tech-bytes.git
cd ai-tech-bytes
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### 4. Set Up API Keys

Create a `.env` file in the project root:

```bash
NEWS_API_KEY=your_newsapi_key_here
```

Get your free NewsAPI key at: [newsapi.org](https://newsapi.org/)

### 5. Run the Pipeline

```bash
python main.py
```

This will:
1. Fetch the latest AI news
2. Generate TTS audio
3. Create videos for multiple platforms
4. Save output to the `output/` directory

## 📁 Project Structure

```
ai-tech-bytes/
│
├── main.py                 # Main orchestrator script
├── news_fetcher.py         # Fetches AI news from APIs
├── tts_generator.py        # Converts text to speech
├── video_maker.py          # Creates videos with overlays
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── README.md              # This file
│
├── data/                  # Generated data (news, audio, scripts)
│   ├── today_news.json
│   ├── ai_news_audio.mp3
│   └── ai_news_audio_script.txt
│
└── output/                # Final video outputs
    ├── ai_tech_bytes_youtube_shorts.mp4
    └── ai_tech_bytes_youtube.mp4
```

## 🎬 Usage

### Basic Usage

```bash
python main.py
```

### Skip Specific Steps

```bash
# Skip news fetching (use existing data)
python main.py --skip-news

# Skip audio generation (use existing audio)
python main.py --skip-audio

# Skip video creation (use existing videos)
python main.py --skip-video
```

### Run Individual Components

```bash
# Just fetch news
python news_fetcher.py

# Just generate audio
python tts_generator.py

# Just create videos
python video_maker.py
```

## ⚙️ Configuration

### News Sources

Edit `news_fetcher.py` to customize:
- Number of articles fetched
- Search queries
- News sources

### Video Styling

Edit `video_maker.py` to customize:
- Video dimensions
- Background colors
- Text fonts and sizes
- Title and branding

### Audio Settings

Edit `tts_generator.py` to customize:
- Speech language
- Speech speed
- Intro/outro messages

## 🤖 Automation with GitHub Actions

For daily automated runs, you can set up GitHub Actions:

1. Create `.github/workflows/daily-video.yml`
2. Add your NEWS_API_KEY to GitHub Secrets
3. Configure the workflow to run daily

## 📤 Uploading to Social Media

### YouTube Upload

For automated YouTube uploads:
1. Set up YouTube Data API v3
2. Create OAuth 2.0 credentials
3. Use `google-api-python-client` library

### TikTok Upload

TikTok API access is limited. Options:
- Manual upload (recommended)
- Use unofficial API wrappers (use with caution)

## 🛠️ Tech Stack

- **Python 3.8+**: Core language
- **NewsAPI**: News aggregation
- **gTTS**: Google Text-to-Speech
- **MoviePy**: Video editing and composition
- **FFmpeg**: Video encoding
- **Pillow**: Image processing

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Created by [@afasim](https://github.com/afasim)

## 🙏 Acknowledgments

- NewsAPI for news aggregation
- Google for TTS services
- MoviePy community for video processing tools

---

**Happy Creating! 🎥✨**
