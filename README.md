# Twitch VOD Downloader

## Introduction

The Twitch VOD Downloader is a tool designed to simplify the process of downloading source-quality VODs from Twitchtv. Whether you're a video editor working with Twitch streams or simply someone who wants to capture specific segments without downloading the entire video, this program has you covered.

## Features

- Download Twitch VODs in their source quality.
- Specify precise start and end times for segment downloads.
- Easily bulk download multiple segments from a file.

## Usage Example
Here are some examples of how to use the program:

### Download a single VOD segment
```bash
twitch-vod-downloader --video-url <VOD_URL> --start-time 00:05:00 --end-time 00:10:00 --video-title "MyVideo"
```
### Bulk download VOD segments from a file
```bash
twitch-vod-downloader --bulk-download bulk_download_list.txt
```
## Bulk Import Format

To streamline the process of downloading multiple VOD segments, you can use a bulk import text file. The bulk import file should follow a specific format, allowing you to specify the VODs you want to download.

The bulk import file consists of multiple lines, where each line represents a separate VOD download request. Each line should contain the following comma-separated fields:

```
"https://www.twitch.tv/videos/<VOD_ID>",00:05:00,00:10:00,MyVideo
"https://www.twitch.tv/videos/<VOD_ID>",02:42:12,02:44:12,MyVideo 2
"https://www.twitch.tv/videos/<VOD_ID>",01:42:12,01:44:12,MyVideo 3
"https://www.twitch.tv/videos/<VOD_ID>",00:42:12,00:44:12,MyVideo 4
```

## How It Works

The Twitch VOD Downloader is designed to efficiently download VOD segments from Twitch using HLS (HTTP Live Streaming) technology. 

### Process Overview

1. **Obtaining HLS Streams**:
   - The script initiates a POST request to Twitch's QGL server, which returns a signature and nauth objects.
   - These obtained signatures and objects are then used to construct a URL to access the m3u8_master_playlist.

2. **Selecting Media Playlist**:
   - From the m3u8_master_playlist, users can choose one of the available m3u8_media_playlist options, which differ based on resolution, FPS, etc.

3. **Segment Downloads**:
   - Using the selected media playlist, the script constructs URLs to obtain individual video segments.
   - Downloading video segments asynchronously is implemented to maximize available bandwidth, resulting in significantly faster downloads.

4. **Command-Line Options**:
   - The `click` library is employed for straightforward inclusion of command-line options, making it user-friendly for customizing download parameters.

### Skills and Knowledge Applied

- **HLS Understanding**: To build this script I gained knowledge of HLS and how Twitch uses it for streaming content.

- **HTTP Requests**: Skills in making HTTP requests are vital for interacting with Twitch servers to obtain HLS streams.

- **Parsing m3u8 Files**: Understanding the structure of m3u8 playlist files is essential for extracting segment information.

- **URL Construction**: Constructing URLs to access m3u8 files and video segments is a key part of the process.

- **Asynchronous Download**: The script employs asynchronous programming (using asyncio) to optimize download speed and bandwidth utilisation.

- **Bandwidth Management**: Efficiently managing available bandwidth contributes to faster downloads.

- **Command-Line Interface**: The use of the `click` library simplifies customisation and user interaction through command-line arguments.

Understanding these aspects helps you appreciate the technical depth of the Twitch VOD Downloader and its capabilities in automating the retrieval of VOD segments from Twitch streams.


## Key Terms

To better understand how the Twitch VOD Downloader works, it's essential to familiarize yourself with some key terms related to video streaming and the HLS (HTTP Live Streaming) format:

### HLS (HTTP Live Streaming)

**HLS**, short for **HTTP Live Streaming**, is a widely-used streaming protocol developed by Apple. It's designed for delivering audio and video content over the internet, providing adaptive streaming capabilities. HLS works by breaking multimedia content into smaller chunks or segments, making it suitable for streaming across varying network conditions.

### m3u8

**m3u8** is the file format used for HLS streaming playlists. These playlists are essential components of HLS streaming and serve as guides for the media player to fetch video and audio segments in the correct order. The **m3u8** file contains information about the available video segments, their URLs, and additional metadata required for playback.

### m3u8 Media Playlist

An **m3u8 Media Playlist** is a specific type of HLS playlist file. It serves as a container for a list of video and audio segments for a particular stream. In addition to segment URLs, it includes critical metadata such as segment duration, stream resolution, and other attributes. Media playlists are used to organise and manage the segments of a single stream.

### m3u8 Master Playlist

In contrast to the **m3u8 Media Playlist**, the **m3u8 Master Playlist** doesn't contain URLs for video content directly. Instead, it acts as a high-level playlist that provides links to various media playlists. These media playlists may differ based on factors like resolution, frame rate (FPS), and bit rate. The master playlist enables adaptive streaming clients to select the appropriate media playlist based on the viewer's device capabilities and network conditions.

## Future Improvements
- Config file - read user bandwidth setting from a config file
- Parse m3u8 media playlist to obtain the server bandwidth
- Implement more robust error handling
- Implement quality option as input before running program

