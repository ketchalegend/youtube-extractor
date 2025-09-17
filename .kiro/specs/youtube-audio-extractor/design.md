# Design Document

## Overview

The YouTube Audio Extractor is a Python-based command-line tool that leverages `yt-dlp` (a fork of youtube-dl with active maintenance) for downloading YouTube content and `ffmpeg` for audio conversion. The tool provides a simple CLI interface for extracting high-quality MP3 audio from individual videos or entire playlists.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
youtube-audio-extractor/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── extractor.py         # Core extraction logic
│   ├── converter.py         # Audio conversion utilities
│   ├── metadata.py          # Metadata handling
│   └── utils.py             # Helper functions
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
└── README.md               # Usage documentation
```

## Components and Interfaces

### CLI Interface (main.py)
- **Purpose**: Command-line argument parsing and user interaction
- **Key Functions**:
  - `parse_arguments()`: Handle CLI arguments (URL, quality, output path)
  - `main()`: Orchestrate the extraction process
  - `display_progress()`: Show download progress and status

### Audio Extractor (extractor.py)
- **Purpose**: Handle YouTube content downloading using yt-dlp
- **Key Functions**:
  - `extract_video_audio(url, options)`: Download single video audio
  - `extract_playlist_audio(url, options)`: Process entire playlists
  - `get_video_info(url)`: Retrieve video metadata
  - `sanitize_filename(title)`: Clean filenames for filesystem compatibility

### Audio Converter (converter.py)
- **Purpose**: Convert downloaded audio to MP3 format
- **Key Functions**:
  - `convert_to_mp3(input_file, output_file, quality)`: Convert audio format
  - `embed_metadata(file_path, metadata)`: Add ID3 tags to MP3 files
  - `validate_ffmpeg()`: Check ffmpeg availability

### Metadata Handler (metadata.py)
- **Purpose**: Extract and format metadata for MP3 tags
- **Key Functions**:
  - `extract_metadata(video_info)`: Parse yt-dlp video information
  - `format_metadata(metadata, playlist_info)`: Structure metadata for ID3 tags
  - `clean_metadata_text(text)`: Sanitize metadata strings

## Data Models

### VideoInfo
```python
@dataclass
class VideoInfo:
    title: str
    uploader: str
    duration: int
    upload_date: str
    url: str
    id: str
```

### PlaylistInfo
```python
@dataclass
class PlaylistInfo:
    title: str
    uploader: str
    video_count: int
    videos: List[VideoInfo]
```

### ExtractionOptions
```python
@dataclass
class ExtractionOptions:
    quality: str = "320"  # kbps
    output_dir: str = "downloads"
    format_template: str = "%(title)s.%(ext)s"
    embed_metadata: bool = True
```

## Error Handling

### Network Errors
- **Strategy**: Retry mechanism with exponential backoff
- **Implementation**: Catch `yt_dlp.DownloadError` and retry up to 3 times
- **User Feedback**: Display clear error messages with suggested actions

### File System Errors
- **Strategy**: Validate paths and permissions before processing
- **Implementation**: Check write permissions and available disk space
- **User Feedback**: Provide specific error messages for permission issues

### Conversion Errors
- **Strategy**: Graceful degradation with format fallbacks
- **Implementation**: If MP3 conversion fails, keep original format
- **User Feedback**: Warn user about format issues but continue processing

### Invalid URLs
- **Strategy**: URL validation before processing
- **Implementation**: Use yt-dlp's URL validation capabilities
- **User Feedback**: Clear error message with URL format examples

## Testing Strategy

### Unit Tests
- **extractor.py**: Mock yt-dlp responses to test extraction logic
- **converter.py**: Test audio conversion with sample files
- **metadata.py**: Validate metadata parsing and formatting
- **utils.py**: Test utility functions with various inputs

### Integration Tests
- **End-to-end**: Test complete workflow with public YouTube videos
- **Playlist handling**: Verify playlist processing with different playlist types
- **Error scenarios**: Test behavior with invalid URLs and network issues

### Manual Testing
- **Quality verification**: Listen to extracted audio for quality issues
- **Metadata validation**: Check MP3 tags in various media players
- **Cross-platform**: Test on different operating systems

## Dependencies

### Core Dependencies
- **yt-dlp**: YouTube content downloading (actively maintained youtube-dl fork)
- **ffmpeg**: Audio conversion and processing
- **mutagen**: MP3 metadata manipulation
- **click**: Command-line interface framework

### System Requirements
- **Python**: 3.8 or higher
- **ffmpeg**: Must be installed and available in PATH
- **Internet connection**: Required for YouTube access

## Configuration

### Default Settings
```python
DEFAULT_CONFIG = {
    "quality": "320",
    "output_format": "mp3",
    "output_template": "%(title)s.%(ext)s",
    "max_retries": 3,
    "timeout": 30
}
```

### CLI Options
- `--quality`: Audio quality (128, 192, 320 kbps)
- `--output`: Output directory path
- `--playlist-folder`: Create folders for playlists (default: True)
- `--metadata`: Embed metadata (default: True)
- `--verbose`: Detailed logging output