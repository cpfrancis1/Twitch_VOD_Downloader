import requests
import json

# Define the URL
url = 'https://gql.twitch.tv/gql'

# client_id = 'sw6b4v2sfjuye6s2kngy5t4fwki6v2'
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'

# Define the headers (optional)
headers = {
    'Content-Type': 'text/plain;charset=UTF-8',
    'Client-ID': client_id,  # Replace with your actual Client-ID
}

# Define the GraphQL query (ops)
ops = [
    {
        "operationName": "VideoMetadata",
        "variables": {
            "channelLogin": "",
            "videoID": "1926316965"
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "226edb3e692509f727fd56821f5653c05740242c82b0388883e0c0e75dcbf687"
            }
        }
    }
]

# Convert the ops list to JSON string
ops_json = json.dumps(ops).encode()

# Make the GET request
response = requests.post(url, headers=headers, data=ops_json)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Now 'data' contains the JSON data from the response
    # You can access specific fields within 'data' as needed
    print(json.dumps(data, indent=4))  # Print the JSON data with indentation
else:
    print(f'Failed to retrieve data. Status code: {response.text}')

# Close the response
response.close()