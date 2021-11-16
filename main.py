import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID="your client id"
CLIENT_SECRET="your client secret"

date=input("what year you would like to travel to in YYY-MM-DD format")
year=date.split("-")[0]

url=f"https://www.billboard.com/charts/hot-100/{date}"

response=requests.get(url)
website=response.text

soup=BeautifulSoup(website,"html.parser")


songs=soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")


songs_name=[song.getText() for song in songs]
print(songs_name)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://127.0.0.1:5500/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]


song_uris = []

for song in songs_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


#playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)