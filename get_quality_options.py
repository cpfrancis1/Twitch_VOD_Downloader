import re
import requests

#Testing function used to read local file
def read_m3u8_file(filepath):
    with open(filepath, "r") as file:
        m3u8_master_playlist_content = file.read()
    return m3u8_master_playlist_content


def get_quality_options(m3u8_master_playlist_content):
    pattern = r'#EXT-X-STREAM-INF:.*VIDEO="([^"]+)".*\n(https.*)'
    quality_options = re.findall(pattern, m3u8_master_playlist_content)
    return quality_options

def select_quality_option(quality_options):
    print("Options Available: ")
    for index, option in enumerate(quality_options):
        print(f"Option Number: {index} Quality: {option[0]}")

    while True: 
        try:
            selected_option = int(input("Please Select Quality Option Number: "))
            if len(quality_options) > selected_option and 0 <= selected_option:
                break
            else: print("Invalid Option: Please enter a valid option")
        except ValueError:
            print("Invalid Input: Please enter a valid options")
    
    selected_quality = quality_options[selected_option][0]
    m3u8_url = quality_options[int(selected_option)][1]

    print("Quality Selected")
    print("Selected Quality " + selected_quality)
    print("Options URL: " + m3u8_url)
    return str(m3u8_url)

    




