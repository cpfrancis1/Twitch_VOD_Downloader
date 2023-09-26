from youtube_dl import YoutubeDL
from youtube_dl.extractor.twitch import TwitchVodIE
import json

# Create a YoutubeDL instance with appropriate options
ydl_opts = {
    'quiet': True,  # Suppress output
    'cookiefile': 'cookies.txt',  # Provide a cookie file if needed
}

ydl = YoutubeDL(ydl_opts)

# Instantiate the TwitchVodIE class
ie = TwitchVodIE(ydl)

# Replace 'YOUR_VOD_URL' with the URL of the Twitch VOD you want to extract info from
vod_url = 'https://www.twitch.tv/videos/1926316965'

# Call the _real_extract function to extract video information
video_info = ie._real_extract(vod_url)

# Now, 'video_info' contains information about the Twitch VOD
# print(json.dumps(video_info, indent= 4))