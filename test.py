from download_stream import get_segment_duration, get_stream_duration, get_m3u8_media_playlist, time_to_seconds, get_chunk_list, get_base_url, download_chunks, concat_segments
import tempfile
 # Enter time in format HH:MM:SS

def main():
    url = "https://d1m7jfoe9zdc1j.cloudfront.net/ac905f0ca491b7eea5a6_chickchau_41847695977_1694646588/chunked/index-dvr.m3u8"
    start_time = "05:42:12" # Enter time in format HH:MM:SS
    end_time = "05:44:12"
    title = "Test Concat"
    with open('index-dvr.m3u8', 'r') as file:
        data = file.read()
    segment_duration = get_segment_duration(data)
    stream_duration = get_stream_duration(data)
    print(segment_duration)
    print(stream_duration)
    start_time_seconds = time_to_seconds(start_time)
    end_time_seconds = time_to_seconds(end_time)
    if time_to_seconds(end_time) < stream_duration:
        baseurl = get_base_url(url)
        chunk_list = get_chunk_list(baseurl, start_time_seconds, end_time_seconds, segment_duration)
        temp_dir = tempfile.mkdtemp()
        download_chunks(chunk_list, temp_dir)
        concat_segments()



    

main()



