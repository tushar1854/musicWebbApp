import requests


def get_spotify_token(client_id, client_secret):
    # Get Spotify access token
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(token_url, headers=headers, data=data)
    token = response.json().get('access_token')
    return token


def search_spotify_track(query, token):
    # Search for a track on Spotify
    search_url = f"https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'q': query,
        'type': 'track',
    }
    response = requests.get(search_url, headers=headers, params=params)
    track_data = response.json().get('tracks', {}).get('items', [])
    if track_data:
        return track_data[0]['external_urls']['spotify']
    else:
        return None


# Replace these with your own Spotify API credentials
# client_id = 'your_client_id'
# client_secret = 'your_client_secret'
client_id = 'c8500a3536794491ad7987729b8b5dc0'
client_secret = '59cf177d543c49929c094ec1393c047e'
# Replace this with your search query
search_query = 'Despacito'

# Get Spotify access token
token = get_spotify_token(client_id, client_secret)

if token:
    # Search for the track and print the URL
    track_url = search_spotify_track(search_query, token)
    if track_url:
        print(f"Spotify URL for '{search_query}': {track_url}")
    else:
        print(f"No track found for '{search_query}' on Spotify.")
else:
    print("Failed to obtain Spotify access token.")
