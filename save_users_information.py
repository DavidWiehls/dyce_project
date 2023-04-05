from flask import Flask, render_template, request, url_for, session, redirect
import spotipy, os
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import time, os

##ALL FIREBASE IMPORTS
##pip install firebase-admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
client_id ='0f7f7d560565409dbb51cc813b995805'
client_secret = '12fcddfc70c344c8b394de5f970329fc'
redirect_url_account = 'https://dyce-36wcmmtu3q-ey.a.run.app/redirect'
#redirect_url_account = 'http://127.0.0.1:8080/redirect'

# Scope for requests
scopes = [
#   'ugc-image-upload',
#   'user-read-playback-state',
   'user-modify-playback-state',
#   'user-read-currently-playing',
#   'streaming',
#   'app-remote-control',
   'user-read-email',
   'user-read-private',
#   'playlist-read-collaborative',
#   'playlist-modify-public',
#   'playlist-read-private',
   'playlist-modify-private',
   'user-library-modify',
#   'user-library-read'
#   'user-top-read',
#   'user-read-playback-position',
#   'user-read-recently-played',
#   'user-follow-read',
#   'user-follow-modify'
 ]

# pylint: disable=C0103
app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['SESSION_COOKIE_NAME'] = 'Dyce Fan Club'
#app.config["CACHE_TYPE"] = "null"
#TOKEN_INFO = "token_info"
user_id = ""

@app.route('/welcome', methods=['Get', 'Post'])
def welcome():
    return render_template('Welcome.html')

@app.route('/', methods=['Get', 'Post'])
def login():
    session.clear()
    try:
        os.remove('.cache')
    except:
        pass
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri= redirect_url_account, ##Change for deployment to redirect_url_account
        scope=scopes)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    load_token_and_email(sp_oauth)
    try:
        os.remove('.cache')
    except:
        pass
    return render_template('Thanks_Page.html')

def load_token_and_email(sp_oauth):
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    user_email=sp.me()['email']
    user_name=sp.me()['display_name']
    user_id=sp.me()['id']
    user_country=sp.me()['country']

    doc_ref = db.collection(u'Users').document(user_id)
    doc_ref.set({'access_token': access_token,
                'refresh_token': refresh_token,
                'user_email': user_email,
                'user_name':user_name,
                'user_country':user_country})
    sp.current_user_saved_tracks_add(tracks=songs_ids)

@app.route('/add_to_queue')
def add_to_queue():
    return render_template('add_to_queue_Page.html', songs_names=songs_names, songs_images=songs_images, length=length)


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
dyce_uri = 'spotify:artist:77s8dtx2Y0GfkwgSJDH7pc'
results = spotify.artist_top_tracks(dyce_uri)
songs_ids = [item['id'] for item in results['tracks']]
songs_names = [item['name'] for item in results['tracks']]
songs_previews = [item['preview_url'] for item in results['tracks']]
songs_images = [item['album']['images'][0]['url'] for item in results['tracks']]
length = len(songs_ids)


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')