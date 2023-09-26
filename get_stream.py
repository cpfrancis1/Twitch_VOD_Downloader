from download_stream import get_segment_duration, get_stream_duration, get_m3u8_media_playlist, time_to_seconds, get_segment_list, get_base_url, download_segments, concat_segments
import tempfile
import asyncio
import time
import datetime
import requests
 # Enter time in format HH:MM:SS

async def get_stream(url, start_time, end_time, title, your_bandwidth, server_bandwidth):
    
    # with open(url.reponse, 'r') as file:
    #     data = file.read()
    data = requests.get(url)
    segment_duration = float(get_segment_duration(data.text)[0])
    stream_duration = float(get_stream_duration(data.text)[0])
    print(segment_duration)
    print(stream_duration)
    start_time_seconds = time_to_seconds(start_time)
    end_time_seconds = time_to_seconds(end_time)
    if end_time_seconds < stream_duration:
        baseurl = get_base_url(url)
        segment_list = get_segment_list(baseurl, start_time_seconds, end_time_seconds, segment_duration)
        temp_dir = tempfile.mkdtemp()
        start_time = time.time()
        await download_segments(segment_list, temp_dir, your_bandwidth, server_bandwidth)
        concat_segments(segment_list, title, temp_dir)
        run_time = time.time()-start_time
        print(f"Download took {run_time} to run")

async def main(): 
    await get_stream(url = "https://d2nvs31859zcd8.cloudfront.net/b33027d6a89a4d43f4fe_chickchau_42747680699_1694562385/chunked/index-dvr.m3u8",
        start_time = "05:42:12", # Enter time in format HH:MM:SS
        end_time = "05:55:12",
        title = "Test Concat", your_bandwidth = 50, server_bandwidth = 5)
    
if __name__ == "__main__":
    asyncio.run(main())



