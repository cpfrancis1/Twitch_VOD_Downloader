import requests
import asyncio
import aiohttp
import os
import re
from datetime import datetime, timedelta
import math


def get_m3u8_media_playlist(m3u8_url):
    response = requests.get(m3u8_url)
    if response.status_code == '200':
        return response.text
    else: 
        print(f'Failed to download m3u8 media playlist. {response.status_code}')
        print(f'Error Text. {response.text}')
        return None
    
def get_stream_duration(m3u8_media_playlist):
    segment_duration_pattern = r'#EXT-X-TWITCH-TOTAL-SECS:(\d+.+)[^\n]*'
    segment_duration = re.findall(segment_duration_pattern, m3u8_media_playlist)
    return segment_duration
    # stream_duration = r''
    # not sure if i need to pass the file for the file name

def get_segment_duration(m3u8_media_playlist):
    stream_duration_pattern = r'#EXT-X-TARGETDURATION:(\d+.+)[^\n]*'
    stream_duration = re.findall(stream_duration_pattern, m3u8_media_playlist)
    return stream_duration

def get_base_url(url):
    pattern = r'(.*/)'
    baseurl = re.findall(pattern, url)
    return baseurl

"""
- calculate the segments to be downloaded
    - start time seconds/segment duration = first segment
    - end time second/segment duration = last segment
"""
def get_segment_list(base_url, start_time_seconds, end_time_seconds, segment_duration):
    start_segment = start_time_seconds/segment_duration
    end_segment = end_time_seconds/segment_duration 
    Url_list = []
    for segment_number in range(math.floor(start_segment), math.floor(end_segment)):
        string = f"{base_url[0]}{segment_number}.ts"
        Url_list.append(string)
    return Url_list


def download_segments_from_file(segment_list, temp_dir): # Used to load from File and not url for bug fixing
    for url in segment_list:
        local_filename = os.path.join(temp_dir, url.split('/')[-1])
        with open(local_filename, 'wb') as local_segment:
            print(f"Downloading segment @: {url}")
            segment = requests.get(url)
            if segment:
                local_segment.write(segment.content)
                print(f"Downloaded segment {local_filename}")

def concat_segments(segment_list, title, temp_dir):
    """
    will need to create a video file
    for this function need to loop through the list of segments in order
    then will need to run a function that will delete the downloaded segments
    """
    output_filename = f'{title}.mp4' # later write function to sanitise title
    with open(output_filename, 'wb') as output_file:
        for url in segment_list:
            segment_path = temp_dir + "\\" + url.split('/')[-1]
            with open(segment_path, 'rb') as segment_file:
                output_file.write(segment_file.read())
    print(f"Video titled {title} successfully download!")

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

async def download_segment(url, temp_dir, semaphore):
    local_filename = os.path.join(temp_dir, url.split('/')[-1])
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(local_filename, 'wb') as local_segment:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            local_segment.write(chunk)
                    print(f"Downloaded segment {local_filename}")

async def download_segments(segment_list, temp_dir, your_bandwidth, server_bandwidth):
    # Calculate the maximum concurrent downloads based on bandwidth
    max_concurrent_downloads = min(your_bandwidth / server_bandwidth, len(segment_list))

    # Create a semaphore to limit concurrent downloads
    semaphore = asyncio.Semaphore(max_concurrent_downloads)

    tasks = []
    for url in segment_list:
        tasks.append(download_segment(url, temp_dir, semaphore))

    await asyncio.gather(*tasks)


        

