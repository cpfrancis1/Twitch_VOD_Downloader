import requests
import json
import ffmpeg # install "ffmpeg-python" not "ffmpeg"
import re


def get_video_id(video_url):
    pattern = r"videos\/(\d+)[^\/]*"
    video_id = re.findall(pattern, video_url)
    return video_id

def _download_access_token(video_id):
    # Define 
    token_kind = "video"  
    param_name = "id"  
    url = 'https://gql.twitch.tv/gql'
    client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

    # Define the headers 
    headers = {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-ID': client_id, 
    }

    method = '%sPlaybackAccessToken' % token_kind
    ops = {
        'query': '''{
          %s(
            %s: "%s",
            params: {
              platform: "web",
              playerBackend: "mediaplayer",
              playerType: "site"
            }
          )
          {
            value
            signature
          }
        }''' % (method, param_name, video_id),
    }
    # Convert the ops dictionary to JSON string
    ops_json = json.dumps(ops).encode()

    # Make the POST request
    response = requests.post(url, headers=headers, data=ops_json)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
        print(f'Error Text: {response.text}')

def construct_cdn_url(response_json, vod_id):
    try:
        # Extract the required data from the JSON response
        access_token_data = response_json.get("data", {}).get("videoPlaybackAccessToken", {})
        value = access_token_data.get("value", {})
        signature = access_token_data.get("signature", "")

        # Sanitise the nauth
        nauth = json.dumps(value).replace('\\', '').strip('"')

        # Construct the URL
        cdn_url = f"https://usher.ttvnw.net/vod/{vod_id}.m3u8?allow_source=true&allow_audio_only=true&allow_spectre=true&player=twitchweb&playlist_include_framerate=true&nauth={nauth}&nauthsig={signature}"

        return cdn_url
    except Exception as e:
        print(f"Error constructing CDN URL: {str(e)}")
        return None

def download_m3u8_master_file(cdn_url):
    try:
        response = requests.get(cdn_url)
        if response.status_code == 200:
            return response.text
        else:
            print(f'Failed to download M3U8 file. Status code: {response.status_code}')
            print(f'Error Text: {response.text}')
            return None
    except Exception as e:
        print(f'Error downloading M3U8 file: {str(e)}')
        return None
    
def extract_twitch_vod(hls_m3u8_url,start_time, finish_time, video_name):
    print("Hls m3u8 url: " + hls_m3u8_url)
    print("Start Time: " + start_time)
    print("End Time: " + finish_time)
    print("Video Title: " + video_name)
    stream = ffmpeg.input(hls_m3u8_url, ss=start_time, to=finish_time)
    stream = ffmpeg.output(stream, f"{video_name}.mp4")
    ffmpeg.run(stream, overwrite_output=True)
    print("video successfully extracted")





