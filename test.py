from download_stream import get_segment_duration, get_m3u8_media_playlist

def main():
    with open('index-dvr.m3u8', 'r') as file:
        data = file.read()
    test = get_segment_duration(data)
    print(test[0])

main()



