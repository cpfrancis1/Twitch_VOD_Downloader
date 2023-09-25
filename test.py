from download_stream import get_segment_duration, get_stream_duration, get_m3u8_media_playlist, time_to_seconds, get_segment_list, get_base_url, download_segments, concat_segments
import tempfile
 # Enter time in format HH:MM:SS

def main():
    url = "https://d2nvs31859zcd8.cloudfront.net/b33027d6a89a4d43f4fe_chickchau_42747680699_1694562385/160p30/index-dvr.m3u8"
    start_time = "05:42:12" # Enter time in format HH:MM:SS
    end_time = "05:44:12"
    title = "Test Concat"
    with open('index-dvr.m3u8', 'r') as file:
        data = file.read()
    segment_duration = float(get_segment_duration(data)[0])
    stream_duration = float(get_stream_duration(data)[0])
    print(segment_duration)
    print(stream_duration)
    start_time_seconds = time_to_seconds(start_time)
    end_time_seconds = time_to_seconds(end_time)
    if end_time_seconds < stream_duration:
        baseurl = get_base_url(url)
        segment_list = get_segment_list(baseurl, start_time_seconds, end_time_seconds, segment_duration)
        temp_dir = tempfile.mkdtemp()
        download_segments(segment_list, temp_dir)
        concat_segments(segment_list, title, temp_dir)




    

main()



