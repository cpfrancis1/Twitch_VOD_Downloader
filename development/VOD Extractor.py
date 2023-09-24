

import ffmpeg
import youtube_dl
import json


def main(start_time, finish_time, video_name, vod_url):

    ydl_opts = {
    "format": "best",
    "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # info_dict = ydl.extract_info(vod_url, download=False)
        info_dict = ydl._real_extract(vod_url, download=False)
        video_url = info_dict["url"]
        print(json.dumps(info_dict, indent=4, sort_keys = True))
        print("VOD URL: " + video_url)
        with open('vod_info.json', 'w') as f:
            json.dump(info_dict, f, indent=4)
    video_url = vod_url
    # stream = ffmpeg.input(video_url, ss=start_time, to=finish_time)
    # stream = ffmpeg.output(stream, f"{video_name}.mp4")
    # ffmpeg.run(stream, overwrite_output=True)
    

if __name__ == "__main__":
    # start_time = "08:19:21" #set start time here
    start_time = "02:19:21" #set start time here
    # finish_time = "08:21:34" #set finish time here
    finish_time = "02:21:34" #set finish time here
    video_name = "test"
    vod_url = "https://www.twitch.tv/videos/1926316965"
    # vod_url = "https://d2nvs31859zcd8.cloudfront.net/15db4e4c1695c80ae6ac_chickchau_42774743419_1694978042/chunked/index-dvr.m3u8"
    

    main(start_time, finish_time, video_name, vod_url)


"""
vodid

def download_info(vodid){
    

}




"""