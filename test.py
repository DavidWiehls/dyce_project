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


    
liked_songs_ids = ['4MzCFFUKU88r9NdaEMtEOn',
            '4UUtMpItuASMKEqIrRPJoG',
            '01V4yWGdMatwJT66DYgB7k',
            '5BoOPZNXhYqLK5fG1EL07F',
            '2i2m3iS5nfsng9RKVY7f7x',
            '79FlK1DMiVrTtDTnbevDGN',
            '7LADc2xkZjX0vtrO3bWDbR',
            '31vMUhHsHny8fknI6O0TLd']


dyce_uri = 'spotify:artist:77s8dtx2Y0GfkwgSJDH7pc'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

results = spotify.artist_top_tracks(dyce_uri)
songs_ids = [item['id'] for item in results['tracks']]
songs_names = [item['name'] for item in results['tracks']]
songs_preview = [item['preview_url'] for item in results['tracks']]
songs_image = [item['album']['images'][0]['url'] for item in results['tracks']]
