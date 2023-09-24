"""
Improvements: 
- error handling, need to check that chunk has download correctly, if not need to redownload the chunk, and overwrite existing chunk file
- need to have option to set the bandwith cap, for example, if you only have 50megabits/s down, no points trying to a sync more than 50 megabits/s of video at once
- parse the file for the chunk durations
- make sure to clean up files after stitching together
- host this library on github
- Write seperate program that will add an intro and outro video automatically

IMPORTANT: Connect this repo to GIT, and make sure to connect all your projects to a git repo moving forward
"""

import asyncio
import aiohttp
import subprocess
import os
from datetime import datetime, timedelta

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

async def download_chunk(session, chunk_url, output_file):
    async with session.get(chunk_url) as response:
        if response.status == 200:
            chunk_data = await response.read()
            with open(output_file, 'wb') as f:
                f.write(chunk_data)
        else:
            print(f"Failed to download chunk: {chunk_url}")

async def download_m3u8_video(m3u8_url, output_folder, start_time, end_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(m3u8_url) as response:
            if response.status == 200:
                m3u8_content = await response.text()
                lines = m3u8_content.split('\n')
                chunk_urls = []
                for line in lines:
                    if line.startswith('http'):
                        chunk_urls.append(line.strip())
                chunks_to_download = []

                # Calculate the start and end chunk indices based on start and end times
                start_seconds = time_to_seconds(start_time)
                end_seconds = time_to_seconds(end_time)
                chunk_duration = 10  # Adjust this value based on your M3U8 playlist

                for i, chunk_url in enumerate(chunk_urls):
                    chunk_start_time = i * chunk_duration
                    chunk_end_time = (i + 1) * chunk_duration
                    if chunk_start_time >= end_seconds:
                        break
                    if chunk_end_time >= start_seconds:
                        chunks_to_download.append((chunk_url, f"{output_folder}/chunk_{i}.ts"))

                # Download the selected chunks asynchronously
                tasks = [download_chunk(session, url, output_file) for url, output_file in chunks_to_download]
                await asyncio.gather(*tasks, return_exceptions=True)
            else:
                print("Failed to fetch M3U8 playlist")

async def main():
    m3u8_url = 'https://example.com/video.m3u8'
    output_folder = 'output_folder'
    start_time = '00:01:30'  # Example start time
    end_time = '00:02:30'    # Example end time
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    await download_m3u8_video(m3u8_url, output_folder, start_time, end_time)

if __name__ == '__main__':
    asyncio.run(main())


import subprocess

def concatenate_video_chunks(output_folder, output_video_file):
    # Generate a list of input files (video chunks)
    input_files = [f"{output_folder}/chunk_{i}.ts" for i in range(len(os.listdir(output_folder)))]

    # Use ffmpeg to concatenate the video chunks into a single file
    cmd = ["ffmpeg", "-i", "concat:" + "|".join(input_files), "-c", "copy", output_video_file]

    # Run the ffmpeg command
    subprocess.run(cmd)

async def main():
    m3u8_url = 'https://example.com/video.m3u8'
    output_folder = 'output_folder'
    output_video_file = 'output_video.mp4'

    # ... (previous code to download chunks)

    # Concatenate the downloaded video chunks into a single video file
    concatenate_video_chunks(output_folder, output_video_file)

if __name__ == '__main__':
    asyncio.run(main())

