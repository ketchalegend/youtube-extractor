"""Setup configuration for YouTube Audio Extractor."""

from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="youtube-audio-extractor",
    version="1.0.0",
    author="YouTube Audio Extractor",
    description="Extract audio from YouTube videos and playlists, convert to MP3 format",
    long_description="A command-line tool that extracts audio from YouTube videos and playlists, converting them to MP3 format for use on devices like iPods.",
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "youtube-audio-extractor=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Internet :: WWW/HTTP",
    ],
)