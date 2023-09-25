"""
Automate extraction of VOD segments from Twitch
Extract VOD using combination of ffmpeg and youtube-dl
inputs required:
- start_time in HH:MM:SS format
- finish_time in HH:MM:SS format
- video_name
- vod_url
"""
import click
from get_access_tokens_and_urls import get_video_id, _download_access_token, construct_cdn_url, download_m3u8_master_file, extract_twitch_vod
from get_quality_options import get_quality_options, select_quality_option

def download_video(video_url, start_time, end_time, video_title):
    
    video_id = get_video_id(video_url)
    data = _download_access_token(str(video_id[0]))
    cdn_url = construct_cdn_url(data, str(video_id[0]))

    if cdn_url:
        m3u8_master_content = download_m3u8_master_file(cdn_url)
    else:
        print("Failed to construct CDN URL.")
    quality_options = get_quality_options(m3u8_master_content)
    m3u8_media_playlist_url = select_quality_option(quality_options)
    extract_twitch_vod(m3u8_media_playlist_url,start_time, end_time, video_title)


@click.command()
@click.option("--video-url", help="Video URL")
@click.option("--start-time", help="Start time")
@click.option("--end-time", help="End time")
@click.option("--video-title", help="Video title")
@click.option("--bulk-download", type=click.Path(exists=True), help="File Path of bulk download file")
def main(bulk_download, video_url, start_time, end_time, video_title):
    if bulk_download:
        with open(bulk_download) as file:
            lines = file.readlines()
        for line in lines:
            arguments = line.split(",")
            video_url = arguments[0]
            start_time = arguments[1]
            end_time = arguments[2]
            video_title = str(arguments[3]).strip()
            download_video(video_url, start_time, end_time, video_title)
    else: 
        download_video(video_url, start_time, end_time, video_title)


if __name__ == "__main__":
    video_url = "https://www.twitch.tv/videos/1924002230" #Enter VOD URL Here
    start_time = "09:42:12" # Enter time in format HH:MM:SS
    end_time = "09:44:12" # Enter time in format HH:MM:SS
    video_title = "EPIC RBGS"
    download_video(video_url, start_time, end_time, video_title)
    # main()
    

    
"""
Future improvements:
- parse the twitch vod url for the ID - completed
- add in command line options - completed
- add in function and option that will download a list of videos from a config file - completed
- Look up possibility of including quality options in the click options
- Async download of the m3u8 segment files

"""