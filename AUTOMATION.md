# AUTOMATION.md - AI Tech Bytes Deployment & Automation Guide

## Overview

This guide covers the complete setup and deployment of the **AI Tech Bytes** automated video generation pipeline using GitHub Actions, free/open-source tools, and optional cloud storage integration.

**Target:** Daily generation of 60-second AI news videos for YouTube, TikTok, and Instagram Reels, fully automated with no manual intervention.

---

## Architecture

### Pipeline Flow

```
1. News Fetching
   ├─ RSS Feeds (Free): Hacker News, Y Combinator, Reddit ML/AI
   └─ NewsAPI (Optional): Additional coverage with your API key

2. Content Processing
   ├─ Text Summarization (HuggingFace BART)
   ├─ Script Generation (900-char budget for 60-sec video)
   └─ Asset Management (JSON specs for reproducibility)

3. Media Generation
   ├─ TTS Audio (gTTS - Google Text-to-Speech)
   └─ Video Composition (MoviePy, PIL-based frames)

4. Output Formats
   ├─ YouTube Shorts (1080×1920, 9:16)
   ├─ YouTube Standard (1920×1080, 16:9)
   ├─ TikTok / Instagram Reels (1080×1920)
   └─ Asset Manifest (JSON metadata)

5. Storage & Deployment
   ├─ GitHub Commits (output/ directory)
   ├─ Optional: Google Cloud Storage
   ├─ Optional: AWS S3
   └─ Optional: Azure Blob Storage
```

### Technology Stack

| Layer | Tool | Purpose | Type |
|-------|------|---------|------|
| **News** | feedparser | Parse RSS feeds | Free |
| | NewsAPI | Fetch AI news | Paid (optional) |
| **Processing** | HuggingFace BART | Summarization | Free |
| **Voice** | gTTS | Text-to-Speech | Free |
| **Video** | MoviePy | Video composition | Free |
| | PIL/Pillow | Image generation | Free |
| **Automation** | GitHub Actions | Daily scheduling | Free (GitHub) |
| **Storage** | Git (output/) | Default storage | Free |
| | Google Cloud Storage | Optional cloud | Paid tier |

---

## Local Setup

### Prerequisites

- Python 3.10+
- FFmpeg (system-level)
- Git (for version control)
- GitHub account (for Actions automation)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-tech-bytes.git
cd ai-tech-bytes
```

### Step 2: Create Python Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key packages:**
- `feedparser>=6.0.0` - RSS feed parsing
- `transformers>=4.30.0` - HuggingFace BART summarization
- `torch>=2.0.0` - PyTorch (required by transformers)
- `gTTS>=2.5.0` - Google Text-to-Speech
- `moviepy>=1.0.3` - Video composition
- `Pillow>=10.0.0` - Image processing
- `requests>=2.31.0` - HTTP client
- `python-dotenv>=1.0.0` - Environment variable loading

### Step 4: Configure Environment Variables

Create `.env` file in project root:

```bash
# Optional: NewsAPI key (for additional news sources)
NEWS_API_KEY=your_newsapi_key_here
API_KEY=your_newsapi_key_here
```

**Get NewsAPI Key:**
1. Visit https://newsapi.org/
2. Sign up (free tier includes 100 requests/day)
3. Copy your API key
4. Paste into `.env` or GitHub Secrets

### Step 5: Test Local Pipeline

```bash
# Run full pipeline (fetch news → summarize → TTS → video)
python main.py

# Run with specific options
python main.py --use-enhanced --use-summarization

# Skip expensive steps for testing
python main.py --skip-news --skip-audio
python main.py --skip-video  # Test video composition only
```

### Expected Output

```
======================================================================
  AI Tech Bytes
======================================================================
           BYTES - Automated Video Creator
======================================================================

[2024-01-15 10:30:45] Starting pipeline...

======================================================================
STEP 1: Fetching AI News
======================================================================
[INFO] Using enhanced news fetcher (RSS + NewsAPI)
[OK] News fetched and saved: data/today_news.json

...

[OK] PIPELINE COMPLETED SUCCESSFULLY
======================================================================
[INFO] Output files:
[INFO]   - Videos: output/
[INFO]   - News: data/today_news.json
[INFO]   - Audio: data/ai_news_audio.mp3
[INFO]   - Manifest: data/asset_manifest_*.json
```

---

## GitHub Actions Automation

### Step 1: Push Repository to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-tech-bytes.git
git branch -M main
git push -u origin main
```

### Step 2: Configure GitHub Secrets

1. Go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Add `NEWS_API_KEY` (optional but recommended)
   - Name: `NEWS_API_KEY`
   - Value: Your NewsAPI key from newsapi.org

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab
2. Authorize Actions on your repository
3. Workflow file is ready: `.github/workflows/daily-video.yml`

### Step 4: Review Workflow Schedule

Edit `.github/workflows/daily-video.yml` to change execution time:

```yaml
schedule:
  # Current: 8 AM UTC (3 AM EST, 12 AM PST)
  # Adjust cron as needed:
  - cron: '0 8 * * *'    # Daily at 8 AM UTC
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 9-18 * * *' # Multiple times per day
```

**Cron format:** `minute hour day month day-of-week`

### Step 5: Manual Test

1. Go to **Actions** tab
2. Select **Daily AI Tech Bytes Video Generation**
3. Click **Run workflow**
4. Monitor execution in real-time

### Workflow Features

✅ **Automated Daily Execution** - Runs on schedule (configurable)
✅ **Manual Trigger** - Run on-demand via Actions tab
✅ **Error Handling** - Graceful failures with logging
✅ **Artifact Storage** - 30-day retention of outputs
✅ **Git Integration** - Auto-commits generated videos
✅ **Notifications** - Email on failure (optional)
✅ **Validation** - Post-generation video format checks

---

## Asset Management

### Asset Manifest Structure

Generated automatically in `data/asset_manifest_YYYY-MM-DD.json`:

```json
{
  "project": "AI Tech Bytes",
  "date": "2024-01-15",
  "version": "2.0",
  "generated": "2024-01-15T10:30:45.123456",
  "assets": [
    {
      "type": "news",
      "filename": "data/today_news.json",
      "description": "Fetched AI news articles",
      "source": "Enhanced RSS+API",
      "file_size_bytes": 15234,
      "md5_hash": "a3f4b9c2e1d8f5a6b7c9d0e1f2a3b4c5",
      "created": "2024-01-15T10:30:45.123456",
      "metadata": {"articles_count": 3}
    }
  ],
  "workflow_steps": [
    {
      "name": "News Fetching",
      "type": "fetch",
      "status": "completed",
      "timestamp": "2024-01-15T10:30:45.123456",
      "details": {"articles_count": 3, "use_enhanced": true}
    }
  ]
}
```

### Asset Specification

Generated in `data/asset_spec_*.json`:

```json
{
  "id": "ai_tech_bytes_20240115_103045",
  "date": "2024-01-15",
  "content": {
    "news_count": 3,
    "articles": [
      {"order": 1, "title": "...", "source": "...", "character_count": 245}
    ],
    "script": {
      "total_characters": 892,
      "estimated_words": 156,
      "estimated_duration_seconds": 62.4
    }
  },
  "audio": {
    "duration_seconds": 62.4,
    "format": "mp3",
    "sample_rate": 44100,
    "bitrate": "128k",
    "voice_engine": "gTTS"
  },
  "video": {
    "formats": [
      {
        "name": "YouTube Shorts",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "fps": 30,
        "codec": "h264"
      }
    ]
  },
  "optimization": {
    "target_duration_seconds": 60,
    "target_character_count": 900,
    "ai_summarization": true,
    "animated_visuals": true
  },
  "delivery": {
    "platforms": ["YouTube", "TikTok", "YouTube Shorts"],
    "file_format": "mp4",
    "color_profile": "sRGB",
    "subtitles": "Available"
  }
}
```

### Usage

```python
from asset_manager import AssetManager, create_complete_asset_manifest

# Create manifest
manager = AssetManager()
manager.add_asset('video', 'output/video.mp4', 'Generated video')
manager.save_manifest('data/manifest.json')

# Generate spec
manager, spec = create_complete_asset_manifest(news_items, script, audio_duration)
manager.save_asset_spec(spec)
```

---

## Cloud Storage Integration (Optional)

### Google Cloud Storage

#### Setup

1. **Create GCP Project:**
   - Go to https://console.cloud.google.com/
   - Create new project
   - Enable Cloud Storage API

2. **Create Service Account:**
   - IAM & Admin → Service Accounts
   - Create service account
   - Grant role: `Storage Object Creator`
   - Create JSON key

3. **Add to GitHub Secrets:**
   - Copy JSON key content
   - Settings → Secrets → `GCP_SERVICE_ACCOUNT_KEY`

#### Workflow Integration

Edit `.github/workflows/daily-video.yml`:

```yaml
upload-to-cloud:
  runs-on: ubuntu-latest
  needs: validate-video
  
  steps:
    - name: Setup Google Cloud
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}
    
    - name: Upload Videos
      run: |
        gsutil -m cp -r output/* gs://ai-tech-bytes/$(date +%Y-%m-%d)/
```

### AWS S3

#### Setup

1. **Create S3 Bucket:**
   - AWS Console → S3
   - Create bucket (e.g., `ai-tech-bytes-videos`)

2. **Create IAM User:**
   - IAM → Users
   - Attach `AmazonS3FullAccess` policy
   - Create access key

3. **Add to GitHub Secrets:**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_BUCKET_NAME`

#### Workflow Integration

```yaml
upload-to-s3:
  runs-on: ubuntu-latest
  needs: validate-video
  
  steps:
    - name: Upload to S3
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        aws s3 sync output/ s3://${{ secrets.AWS_BUCKET_NAME }}/$(date +%Y-%m-%d)/
```

---

## Monitoring & Logging

### GitHub Actions Logs

1. Go to **Actions** tab
2. Click on workflow run
3. View step-by-step execution logs
4. Check artifacts after completion

### Local Logs

```bash
# View pipeline output
python main.py 2>&1 | tee pipeline.log

# Check video generation logs
tail -f data/asset_manifest_*.json | jq '.'
```

### Email Notifications

GitHub automatically sends notifications on workflow failure.

Configure at: **Settings → Notifications → GitHub Actions**

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'transformers'"

**Solution:**
```bash
pip install transformers torch
```

### Issue: "FFmpeg not found"

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Solution (macOS):**
```bash
brew install ffmpeg
```

**Solution (Windows):**
```powershell
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

### Issue: "gTTS network timeout"

**Solution:** gTTS requires internet. Check connectivity or wait for retry.

### Issue: GitHub Actions workflow not running

**Solution:**
1. Verify `.github/workflows/daily-video.yml` exists
2. Check workflow syntax: `github.com/actions/workflow-syntax`
3. Enable Actions: Settings → Actions → Allow all actions

### Issue: NewsAPI quota exceeded

**Solution:**
- Free tier: 100 requests/day
- Switch to RSS-only: `--use-enhanced` (uses RSS feeds)
- Or upgrade to paid plan

### Issue: Videos not generated

**Solution:**
```bash
# Test locally first
python main.py --skip-news --skip-audio  # Test video composition

# Check if audio exists
ls -la data/ai_news_audio.mp3

# Check ffmpeg
ffmpeg -version
```

---

## Best Practices

### 1. Backup & Version Control
```bash
# Commit changes regularly
git add .
git commit -m "Update pipeline configuration"
git push origin main
```

### 2. Monitor Asset Storage
```bash
# Check output directory size
du -sh output/
git gc  # Clean up git history
```

### 3. News Source Optimization
- **RSS Feeds:** Fast, free, but limited selection
- **NewsAPI:** Comprehensive but rate-limited
- **Recommendation:** Use both for best coverage

### 4. Script Length Validation
- Target: 900 characters (≈60 seconds)
- Actual: Check `data/asset_spec_*.json` for duration
- Adjust with `text_summarizer.py` parameters

### 5. Regular Testing
```bash
# Monthly: Full pipeline test
python main.py

# Weekly: Validate video composition
python main.py --skip-news --skip-audio
```

---

## Performance Optimization

### Caching Dependencies

GitHub Actions caches pip packages by default. No action needed.

### Parallel Processing

Current workflow runs sequentially. For faster generation:

```yaml
# In daily-video.yml, add parallel matrix
strategy:
  matrix:
    format: ['shorts', 'standard']
  max-parallel: 2
```

### Reduce Model Size

For faster summarization on limited resources:

```python
# In text_summarizer.py, change model
model_name = "facebook/bart-large-cnn"      # Large (1.6GB)
model_name = "facebook/bart-base-cnn"       # Small (500MB)
model_name = "sshleifer/distilbart-cnn-6-6" # Tiny (300MB)
```

---

## Customization

### Change Video Output Dimensions

Edit `video_maker.py`:
```python
# Line with: width, height = ...
width, height = 720, 1280  # Change from 1080, 1920
```

### Change Daily Schedule

Edit `.github/workflows/daily-video.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1-5'  # Weekdays at 9 AM
  - cron: '0 12 * * *'   # Daily at noon
```

### Add Custom News Sources

Edit `enhanced_news_fetcher.py`:
```python
FREE_RSS_FEEDS = {
    'your_feed_name': 'https://your-rss-feed-url.com/feed.xml',
    # ... existing feeds
}
```

### Modify Script Format

Edit `text_summarizer.py`:
```python
def create_video_script(news_items, max_total_chars=1200):  # Increase budget
    # Adjust script generation logic
```

---

## Security Considerations

### Secrets Management

✅ **Good:** Use GitHub Secrets for API keys
```yaml
env:
  NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
```

❌ **Bad:** Hardcode keys in code or workflow files

### Rate Limiting

- **gTTS:** No official rate limit, but reasonable usage expected
- **NewsAPI:** Free tier = 100 requests/day
- **RSS Feeds:** Respect robots.txt; no rate limit

### Data Privacy

- Videos are stored in `output/` (public if repo is public)
- News data in `data/` (may contain URLs/attribution)
- Consider private repository if dealing with sensitive content

---

## Future Enhancements

- [ ] YouTube Data API integration for auto-upload
- [ ] TikTok/Instagram API integration
- [ ] Email notification with video summary
- [ ] Web dashboard for monitoring past videos
- [ ] A/B testing of different script formats
- [ ] Multi-language support (FR, ES, DE, etc.)
- [ ] Custom background music/overlay
- [ ] Subtitle generation (accessibility)

---

## Support & Contributing

**Issues?** Open an issue on GitHub: `https://github.com/YOUR_USERNAME/ai-tech-bytes/issues`

**Want to contribute?** Fork, make changes, submit PR.

**Questions?** Check README.md and code comments.

---

## License

MIT License - Free for personal and commercial use.

---

**Last Updated:** 2024-01-15
**Version:** 2.0 (Multi-source, Summarization, Full Automation)
