"""
Improvements: 
- error handling, need to check that segment has download correctly, if not need to redownload the segment, and overwrite existing segment file
- need to have option to set the bandwith cap, for example, if you only have 50megabits/s down, no points trying to a sync more than 50 megabits/s of video at once
- parse the file for the segment durations
- make sure to clean up files after stitching together
- host this library on github
- Write seperate program that will add an intro and outro video automatically
- Monitoring and Logging:
- options to choose output format

Terms: 
HLS = HTTP Live streeaming
m3u8 = HLS file format
m3u8 media playlist = file containing the list of segments for a stream, and meta information about the segment durations 
m3u8 master playlist = unline the media file, this file does not contain URLs for the video content directly, however it contains links to variour media playlists, there may be various media playlist depending on the resolution and fps etc

- psuedo code
- get the m3u8 file
- Parse the file for the segment duration
- Parse the file for the stream length 
- check if the segment finish time is less than the stream length
- convert the start and finish time to second
- calculate the segments to be downloaded
    - start time seconds/segment duration = first segment
    - end time second/segment duration = last segment
- create a list of all the segment URLs to download
- download the segments, name the segments in order
- for the first and last segments, make sure that they are trimmed down to the specific time, not just the nearest segment duration 
- stich the segments together
- name the file after the filename

After this code is written implement asynconous download

Libaries needed:
Need library to download video - is requests library conventional for this type of thing?
Use regular expression to parse the m3u8 media playlist



IMPORTANT: Connect this repo to GIT, and make sure to connect all your projects to a git repo moving forward
"""

import requests
import asyncio
import aiohttp
import subprocess
import os
import re
import tempfile
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
        print(f"{base_url[0]}{segment_number}.ts")
        Url_list.append(string)
    return Url_list


# def download_segments(segment_list, temp_dir):
#     for url in segment_list:
#         local_filename = os.path.join(temp_dir, url.split('/')[-1])
#         with open(local_filename, 'wb') as local_segment:
#             print(f"Downloading segment @: {url}")
#             segment = requests.get(url)
#             if segment:
#                 local_segment.write(segment.content)
#                 print(f"Downloaded segment {local_filename}")

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
    print("script succesfully run")

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

async def download_segment(url, temp_dir, semaphore):
    local_filename = os.path.join(temp_dir, url.split('/')[-1])
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(response.status)
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
        print(url)
        tasks.append(download_segment(url, temp_dir, semaphore))

    await asyncio.gather(*tasks)


        

