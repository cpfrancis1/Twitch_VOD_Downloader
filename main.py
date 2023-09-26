"""
Automate extraction of VOD segments from Twitch
Extract VOD using combination of ffmpeg and youtube-dl
inputs required:
- start_time in HH:MM:SS format
- finish_time in HH:MM:SS format
- video_name
- vod_url
"""
from get_access_tokens_and_urls import get_video_id, _download_access_token, construct_cdn_url, download_m3u8_master_file, extract_twitch_vod
from get_quality_options import get_quality_options, select_quality_option
from get_stream import get_stream
import asyncio
import click
import tracemalloc
from functools import wraps

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper



async def download_video(video_url, start_time, end_time, video_title, quality):
    your_bandwidth = 50
    server_bandwidth = 5
    video_id = get_video_id(video_url)
    data = _download_access_token(str(video_id[0]))
    cdn_url = construct_cdn_url(data, str(video_id[0]))
    print("CDN_URL "+ cdn_url)

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
        with open(bulk_download) as file:
            lines = file.readlines()
        for line in lines:
            arguments = line.split(",")
            video_url = arguments[0]
            start_time = arguments[1]
            end_time = arguments[2]
            video_title = str(arguments[3]).strip()
            await download_video(video_url, start_time, end_time, video_title, quality = 1)
    else: 
        await download_video(video_url, start_time, end_time, video_title, quality = None)

# Create a synchronous entry point


if __name__ == "__main__":
    # video_url = "https://www.twitch.tv/videos/1935001103" #Enter VOD URL Here
    # start_time = "02:42:12" # Enter time in format HH:MM:SS
    # end_time = "02:44:12" # Enter time in format HH:MM:SS
    # video_title = "Mitch Jones"
    # asyncio.run(download_video(video_url, start_time, end_time, video_title))
    main()
    # main()
    

    
"""
Future improvements:
- parse the twitch vod url for the ID - completed
- add in command line options - completed
- add in function and option that will download a list of videos from a config file - completed
- Look up possibility of including quality options in the click options
- Async download of the m3u8 segment files

"""