"""
Automate extraction of VOD segments from Twitch
Extract VOD using combination of ffmpeg and youtube-dl
inputs required:
- start_time in HH:MM:SS format
- finish_time in HH:MM:SS format
- video_name
- vod_url

Terms: 
HLS = HTTP Live streaming
m3u8 = HLS file format
m3u8 media playlist = file containing the list of segments for a stream, and meta information about the segment durations 
m3u8 master playlist = unlike the media file, this file does not contain URLs for the video content directly, however it contains links to various media playlists, there may be various media playlist depending on the resolution and fps etc
"""
"""
Improvements: 
- error handling, need to check that segment has download correctly, if not need to retry the download. If the download fails then need to break the program
- config file for bandwidth settings
- host this library on github
- Write seperate program that will add an intro and outro video automatically
- Logging?
- Options to choose outputformat
- Create readme file
"""
from get_access_tokens_and_urls import get_video_id, _download_access_token, construct_cdn_url, download_m3u8_master_file
from get_quality_options import get_quality_options, select_quality_option
from get_stream import get_stream
from functools import wraps
import asyncio
import click
import time
import random
import os

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

def generate_unique_directory_name():
    # Generate a unique directory name based on the current timestamp and a random string
    timestamp = time.strftime("%d%m%Y-%H%M")
    random_string = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    directory_name = f"./data/Bulk Downloads/Twitch Bulk Download {timestamp}-{random_string}"
    return directory_name

async def download_video(video_url, start_time, end_time, video_title, quality):
    your_bandwidth = 50
    server_bandwidth = 5
    video_id = get_video_id(video_url)
    data = _download_access_token(str(video_id[0]))
    cdn_url = construct_cdn_url(data, str(video_id[0]))
    if cdn_url:
        m3u8_master_content = download_m3u8_master_file(cdn_url)
    else:
        print("Failed to construct CDN URL.")

    quality_options = get_quality_options(m3u8_master_content)
    m3u8_media_playlist_url = select_quality_option(quality_options, quality)
    
    await get_stream(m3u8_media_playlist_url,start_time, end_time, video_title, your_bandwidth, server_bandwidth)
    


@click.command()
@click.option("--video-url", help="Video URL")
@click.option("--start-time", help="Start time")
@click.option("--end-time", help="End time")
@click.option("--video-title", help="Video title")
@click.option("--bulk-download", type=click.Path(exists=True), help="File Path of bulk download file")
@coro  # Use the coro decorator
async def main(bulk_download, video_url, start_time, end_time, video_title):
    if bulk_download:
        download_start_time = time.time()
        
        with open(bulk_download) as file:
            lines = file.readlines()
        # Remove trailing empty lines
        while lines and lines[-1].strip() == "":
            lines.pop()

        directory_name = generate_unique_directory_name()
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        os.chdir(directory_name)
        
        for line in lines:
            arguments = line.split(",")
            video_url = arguments[0]
            start_time = arguments[1]
            end_time = arguments[2]
            video_title = str(arguments[3]).strip()
            await download_video(video_url, start_time, end_time, video_title, quality = 1)
        total_time = time.time() - download_start_time
        print(f"Total time for Entire Bulk Download: {str(round(total_time/60, 2))} minutes")
    else: 
        await download_video(video_url, start_time, end_time, video_title, quality = None)



if __name__ == "__main__":
    main()
    

    
"""
Future improvements:
- parse the twitch vod url for the ID - completed
- add in command line options - completed
- add in function and option that will download a list of videos from a config file - completed
- Look up possibility of including quality options in the click options - Not sure how to achieve this
- Async download of the m3u8 segment files - Completed

"""