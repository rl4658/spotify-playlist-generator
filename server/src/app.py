from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
from dotenv import load_dotenv
import os
import openai
import string
from openai import OpenAI

app = FastAPI()

# change this later to allow only specific origins (in production)
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataModel(BaseModel):
    acousticness: str
    danceability: str
    energy: str
    instrumentalness: str
    mood_valence: str
    tempo: str
    prompt: str
    trackId: str

@app.get("/")
def index():
    return {"message": "Spotify Playlist Generator API running..."}

def playlist_generator(acousticness: str, danceability: str, energy: str, instrumentalness: str, mood_valence: str, tempo: str, prompt: str, trackId: str):
    if acousticness == '0':
        acousticness = None
    if danceability == '0':
        danceability = None
    if energy == '0':
        energy = None
    if instrumentalness == '0':
        instrumentalness = None
    if mood_valence == '0':
        mood_valence = None
    if tempo == '60':
        tempo = None
    if prompt == '':
        prompt = None
    if trackId == '':
        trackId = None

    if prompt is not None:
        promptActivate = True
    else:
        promptActivate = False
    if trackId is not None:
        inputActivate = True
    else:
        inputActivate = False

    genre_list = [
            "acoustic",
            "afrobeat",
            "alt-rock",
            "alternative",
            "ambient",
            "anime",
            "black-metal",
            "bluegrass",
            "blues",
            "bossanova",
            "brazil",
            "breakbeat",
            "british",
            "cantopop",
            "chicago-house",
            "children",
            "chill",
            "classical",
            "club",
            "comedy",
            "country",
            "dance",
            "dancehall",
            "death-metal",
            "deep-house",
            "detroit-techno",
            "disco",
            "disney",
            "drum-and-bass",
            "dub",
            "dubstep",
            "edm",
            "electro",
            "electronic",
            "emo",
            "folk",
            "forro",
            "french",
            "funk",
            "garage",
            "german",
            "gospel",
            "goth",
            "grindcore",
            "groove",
            "grunge",
            "guitar",
            "happy",
            "hard-rock",
            "hardcore",
            "hardstyle",
            "heavy-metal",
            "hip-hop",
            "holidays",
            "honky-tonk",
            "house",
            "idm",
            "indian",
            "indie",
            "indie-pop",
            "industrial",
            "iranian",
            "j-dance",
            "j-idol",
            "j-pop",
            "j-rock",
            "jazz",
            "k-pop",
            "kids",
            "latin",
            "latino",
            "malay",
            "mandopop",
            "metal",
            "metal-misc",
            "metalcore",
            "minimal-techno",
            "movies",
            "mpb",
            "new-age",
            "new-release",
            "opera",
            "pagode",
            "party",
            "philippines-opm",
            "piano",
            "pop",
            "pop-film",
            "post-dubstep",
            "power-pop",
            "progressive-house",
            "psych-rock",
            "punk",
            "punk-rock",
            "r-n-b",
            "rainy-day",
            "reggae",
            "reggaeton",
            "road-trip",
            "rock",
            "rock-n-roll",
            "rockabilly",
            "romance",
            "sad",
            "salsa",
            "samba",
            "sertanejo",
            "show-tunes",
            "singer-songwriter",
            "ska",
            "sleep",
            "songwriter",
            "soul",
            "soundtracks",
            "spanish",
            "study",
            "summer",
            "swedish",
            "synth-pop",
            "tango",
            "techno",
            "trance",
            "trip-hop",
            "turkish",
            "work-out",
            "world-music"
        ]

    genres_final = ""
    for genre in genre_list:
        genres_final += genre + "\n"
    
    load_dotenv()
    gptKey = os.getenv('openai.api_key')
    spotifyClient = os.getenv('SPOTIFY_CLIENT_ID')
    spotifySecret = os.getenv('SPOTIFY_CLIENT_SECRET')
    # Check both conditions first
    if promptActivate and inputActivate:
        openai.api_key = gptKey
        # Create a translation table to replace punctuation with None
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation from the string
        final_prompt = prompt.translate(translator)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (f"You are a playlist curator for Spotify. You are given this prompt: '{final_prompt}'. As a curator, pick the most relevant genre to this prompt ONLY FROM THIS LIST. If the genre that you pick is not in the list, choose the most similar one from the list: \n" + genres_final +
                                "\nAlso, assign values to the following track attributes: \n\n"
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. Range: 0 - 1. \n\n"
                                "Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. \n\n"
                                "Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. \n\n"
                                "Instrumentalness: Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. \n\n"
                                "Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. Range: 60 - 180. \n\n"
                                "Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). Range: 0 - 1. \n\n"
                                "Give me your response in the following format, and do not deviate from it: \n"                      
                                "Acousticness: <Acousticness Value> \n"
                                "Danceability: <Danceability Value> \n"
                                "Energy: <Energy Value> \n"
                                "Instrumentalness: <Instrumentalness Value> \n"
                                "Tempo: <Tempo Value> \n"
                                "Valence: <Valence Value>\n"
                                "Genre 1: <Genre #1> \n")
                },
            ]
        )

        response_content = str(response.choices[0].message)

        # Extracting the content from the response string
        start = response_content.find("content='") + 9
        end = response_content.find("', role='")
        actual_content = response_content[start:end]

        # Splitting the actual content by newline to get each attribute line
        attribute_lines = actual_content.split("\\n")

        # Parsing each line and filling the dictionary
        dictionary = {}
        for line in attribute_lines:
            # Splitting each line into key and value
            key_value = line.split(": ")
            if len(key_value) == 2:
                # Assigning to dictionary, converting numeric values when necessary
                key, value = key_value
                if key in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Tempo', 'Valence']:
                    try:
                        dictionary[key] = float(value) if '.' in value else int(value)
                    except ValueError:
                        dictionary[key] = value  # In case of conversion error, keep original string
                else:
                    dictionary[key] = value

        dictionary["Genre 1"] = dictionary["Genre 1"].strip()

        print(dictionary)

        if dictionary["Genre 1"] not in genre_list:
            dictionary["Genre 1"] = "Pop"

        print(dictionary)

        # Define a function to retrieve Spotify track link
        def get_spotify_link(track_id, sp):
            return sp.track(track_id)

        # Define a function to input track recommendations based on song name and artist name
        def input_track_recommendations(song_name, artist_name, sp):
            # Query Spotify API to search for the song and artist
            query = f"{song_name} {artist_name}"
            results = sp.search(q=query, type='track', limit=1)

            # Proceed if the song is found
            if results['tracks']['items']:
                input_track = results['tracks']['items'][0]
                input_genre = trackId

                # Get audio analysis for the input track
                input_audio_analysis = sp.audio_analysis(input_track['id'])
                
                # Modify tempo randomly within a range
                if tempo is not None:
                    final_tempo = int(tempo)
                else:
                    extracted_tempo = input_audio_analysis['track']['tempo'] + random.randint(-10,10)
                    tempo_factor = random.randint(-10,10)
                    input_tempo = extracted_tempo + tempo_factor
                    final_tempo = (input_tempo + dictionary["Tempo"])/2

                # Extract artist name and audio features
                input_artist = input_track['artists'][0]['name']
                input_audio_features = sp.audio_features(input_track['id'])[0]

                # Modify energy randomly within a range but ensure it stays between 0 and 1
                if energy is not None:
                    final_energy = float(energy)
                else:
                    extracted_energy = input_audio_features['energy']
                    energy_factor = random.uniform(-0.1, 0.1)
                    input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
                    final_energy = (input_energy + dictionary["Energy"])/2

                # Similar modifications for valence, danceability, acousticness, and instrumentalness
                if mood_valence is not None:
                    final_valence = float(mood_valence)
                else:
                    extracted_valence = input_audio_features['valence']
                    valence_factor = random.uniform(-0.1, 0.1)
                    input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
                    final_valence = (input_valence + dictionary["Valence"])/2
                
                if danceability is not None:
                    final_danceability = float(danceability)
                else:
                    extracted_danceability = input_audio_features['danceability']
                    danceability_factor = random.uniform(-0.1, 0.1)
                    input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
                    final_danceability = (input_danceability + dictionary["Danceability"])/2

                if acousticness is not None:
                    final_acousticness = float(acousticness)
                else:
                    extracted_acousticness = input_audio_features['acousticness']
                    acousticness_factor = random.uniform(-0.1, 0.1)
                    input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
                    final_acousticness = (input_acousticness + dictionary["Acousticness"])/2

                if instrumentalness is not None:
                    final_instrumentalness = float(instrumentalness)
                else:
                    extracted_instrumentalness = input_audio_features['instrumentalness']
                    instrumentalness_factor = random.uniform(-0.1, 0.1)
                    input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
                    final_instrumentalness = (input_instrumentalness + dictionary["Instrumentalness"])/2
                
                # Get recommendations based on the modified track features
                recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=track_num)

                # Filter out the input track from the recommendations and truncate the list
                recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]
                recommendations['tracks'] = recommendations['tracks'][:track_num - 1]

                # Add Spotify URLs to the recommendations
                recommendations['spotify_url'] = [get_spotify_link(track['id'], sp)['external_urls']['spotify'] for track in recommendations['tracks']]

                return recommendations
            
            else:
                print(f"No match found for the song '{song_name}'.")
                return None 

        # Load environment variables containing sensitive information
        load_dotenv()
        CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

        # Initialize Spotify client with credentials
        client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Define scope for playlist modification and initialize SpotifyOAuth
        scope = 'playlist-modify-public'
        username = '31vxd2rpgrlanjxy6mu5fvcexoaq'
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:3001/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = prompt
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        track_num = 50
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        track = sp.track(trackId)        
        list_of_songs = []
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        list_of_songs = []

        # Search for the track and add it to the playlist
        if artist_name:
            query = f"{track_name} {artist_name}"
        else:
            query = track_name
        result = spotifyObject.search(q=query)
        if len(result['tracks']['items']) > 0:
            list_of_songs.append(result['tracks']['items'][0]['uri'])
        else:
            print(f"No results found for '{track_name}' by '{artist_name}'")
        print(f"Added '{track_name}' by '{artist_name}' to the '{playlist_name}' playlist!")    
        
        # Generate and display recommendations based on the input track
        recommendations = input_track_recommendations(track_name, artist_name, sp)

        if recommendations is not None:
            print(f"\nTop {track_num} Recommendations:\n")
            for track in recommendations['tracks']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                list_of_songs.append(track['uri'])
                print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!")
                                
        # Add recommended tracks to the playlist
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)

        
    elif promptActivate:  # This will only be checked if the first condition is False
        load_dotenv()
        openai.api_key = os.getenv("openai.api_key") #CRAZY 
        print("\nTHIS IS THE KEY\n")
        # Create a translation table to replace punctuation with None
        translator = str.maketrans('', '', string.punctuation)
        # Remove punctuation from the string
        final_prompt = prompt.translate(translator)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (f"You are a playlist curator for Spotify. You are given this prompt: '{final_prompt}'. As a curator, pick the most relevant genre to this prompt ONLY FROM THIS LIST. If the genre that you pick is not in the list, choose the most similar one from the list: \n" + genres_final +
                                "\nAlso, assign values to the following track attributes: \n\n"
                                "Acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. Range: 0 - 1. \n\n"
                                "Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. \n\n"
                                "Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. \n\n"
                                "Instrumentalness: Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. \n\n"
                                "Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. Range: 60 - 180. \n\n"
                                "Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). Range: 0 - 1. \n\n"
                                "Give me your response in the following format, and do not deviate from it: \n"                      
                                "Acousticness: <Acousticness Value> \n"
                                "Danceability: <Danceability Value> \n"
                                "Energy: <Energy Value> \n"
                                "Instrumentalness: <Instrumentalness Value> \n"
                                "Tempo: <Tempo Value> \n"
                                "Valence: <Valence Value>\n"
                                "Genre 1: <Genre #1> \n")
                },
            ]
        )

        response_content = str(response.choices[0].message)
        print(response_content)

        # Extracting the content from the response string
        start = response_content.find("content='") + 9
        end = response_content.find("', role='")
        actual_content = response_content[start:end]

        # Splitting the actual content by newline to get each attribute line
        attribute_lines = actual_content.split("\\n")

        # Parsing each line and filling the dictionary
        dictionary = {}
        for line in attribute_lines:
            # Splitting each line into key and value
            key_value = line.split(": ")
            if len(key_value) == 2:
                # Assigning to dictionary, converting numeric values when necessary
                key, value = key_value
                if key in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Tempo', 'Valence']:
                    try:
                        dictionary[key] = float(value) if '.' in value else int(value)
                    except ValueError:
                        dictionary[key] = value  # In case of conversion error, keep original string
                else:
                    dictionary[key] = value

        dictionary["Genre 1"] = dictionary["Genre 1"].strip()

        print(dictionary)

        if dictionary["Genre 1"] not in genre_list:
            dictionary["Genre 1"] = "Pop"

        # Load environment variables containing sensitive information
        load_dotenv()
        CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

        # Initialize Spotify client with credentials
        client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Define scope for playlist modification and initialize SpotifyOAuth
        scope = 'playlist-modify-public'
        username = '31vxd2rpgrlanjxy6mu5fvcexoaq'
        list_of_songs = []
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:3001/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = prompt
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        track_num = 50
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Modify tempo randomly within a range
        if tempo is not None:
            input_tempo = int(tempo)
        else:
            extracted_tempo = dictionary['Tempo']
            tempo_factor = random.randint(-10,10)
            input_tempo = extracted_tempo + tempo_factor

        # Modify energy randomly within a range but ensure it stays between 0 and 1
        if energy is not None:
            input_energy = float(energy)
        else:
            extracted_energy = dictionary['Energy']
            energy_factor = random.uniform(-0.1, 0.1)
            input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)

        # Similar modifications for valence, danceability, acousticness, and instrumentalness
        if mood_valence is not None:
            input_valence = float(mood_valence)
        else:
            extracted_valence = dictionary['Valence']
            valence_factor = random.uniform(-0.1, 0.1)
            input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)

        if danceability is not None:
            input_danceability = float(danceability)
        else:
            extracted_danceability = dictionary['Danceability']
            danceability_factor = random.uniform(-0.1, 0.1)
            input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)

        if acousticness is not None:
            input_acousticness = float(acousticness)
        else:
            extracted_acousticness = dictionary['Acousticness']
            acousticness_factor = random.uniform(-0.1, 0.1)
            input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)

        if instrumentalness is not None:
            input_instrumentalness = float(instrumentalness)
        else:
            extracted_instrumentalness = dictionary['Instrumentalness']
            instrumentalness_factor = random.uniform(-0.1, 0.1)
            input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
            
        # Get recommendations based on the modified track features
        recommendations = sp.recommendations(seed_genres=[dictionary['Genre 1'].lower()], target_tempo=[input_tempo], target_energy=[input_energy], target_valence=[input_valence], target_danceability=[input_danceability], target_acousticness=[input_acousticness], target_instrumentalness=[input_instrumentalness], limit=track_num)

        list_of_songs = [track['uri'] for track in recommendations['tracks']]

        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)

        print("Playlist Generated!")


    elif inputActivate:  # This will only be checked if the first and second conditions are False
        # Define a function to retrieve Spotify track link
        def get_spotify_link(track_id, sp):
            return sp.track(track_id)

        # Define a function to input track recommendations based on song name and artist name
        def input_track_recommendations(song_name, artist_name, sp):
            # Query Spotify API to search for the song and artist
            query = f"{song_name} {artist_name}"
            results = sp.search(q=query, type='track', limit=1)

            # Proceed if the song is found
            if results['tracks']['items']:
                input_track = results['tracks']['items'][0]
                input_genre = input_track['artists'][0]['id']

                audio_features = sp.audio_features(trackId)[0]
                print("\nTRACK INFO\n")
                print(audio_features)
                
                # Modify tempo randomly within a range
                if tempo is not None:
                    final_tempo = int(tempo)
                else:
                    extracted_tempo = audio_features['tempo'] + random.randint(-10,10)
                    tempo_factor = random.randint(-10,10)
                    input_tempo = extracted_tempo + tempo_factor
                    final_tempo = input_tempo

                # Modify energy randomly within a range but ensure it stays between 0 and 1
                if energy is not None:
                    final_energy = float(energy)
                else:
                    extracted_energy = audio_features['energy']
                    energy_factor = random.uniform(-0.1, 0.1)
                    input_energy = round(max(0, min(1, extracted_energy + energy_factor)), 3)
                    final_energy = input_energy

                # Similar modifications for valence, danceability, acousticness, and instrumentalness
                if mood_valence is not None:
                    final_valence = float(mood_valence)
                else:
                    extracted_valence = audio_features['valence']
                    valence_factor = random.uniform(-0.1, 0.1)
                    input_valence = round(max(0, min(1, extracted_valence + valence_factor)), 3)
                    final_valence = input_valence
                
                if danceability is not None:
                    final_danceability = float(danceability)
                else:
                    extracted_danceability = audio_features['danceability']
                    danceability_factor = random.uniform(-0.1, 0.1)
                    input_danceability = round(max(0, min(1, extracted_danceability + danceability_factor)), 3)
                    final_danceability = input_danceability

                if acousticness is not None:
                    final_acousticness = float(acousticness)
                else:
                    extracted_acousticness = audio_features['acousticness']
                    acousticness_factor = random.uniform(-0.1, 0.1)
                    input_acousticness = round(max(0, min(1, extracted_acousticness + acousticness_factor)), 3)
                    final_acousticness = input_acousticness

                if instrumentalness is not None:
                    final_instrumentalness = float(instrumentalness)
                else:
                    extracted_instrumentalness = audio_features['instrumentalness']
                    instrumentalness_factor = random.uniform(-0.1, 0.1)
                    input_instrumentalness = round(max(0, min(1, extracted_instrumentalness + instrumentalness_factor)), 3)
                    final_instrumentalness = input_instrumentalness
                
                # Get recommendations based on the modified track features
                recommendations = sp.recommendations(seed_artists=[input_genre], target_tempo=[final_tempo], target_energy=[final_energy], target_valence=[final_valence], target_danceability=[final_danceability], target_acousticness=[final_acousticness], target_instrumentalness=[final_instrumentalness], limit=track_num)

                # Filter out the input track from the recommendations and truncate the list
                recommendations['tracks'] = [track for track in recommendations['tracks'] if track['id'] != input_track['id']]
                recommendations['tracks'] = recommendations['tracks'][:track_num - 1]

                explicitActivate = True
                # While loop to filter out explicit tracks
                
                # Add Spotify URLs to the recommendations
                recommendations['spotify_url'] = [get_spotify_link(track['id'], sp)['external_urls']['spotify'] for track in recommendations['tracks']]

                return recommendations
            
            else:
                print(f"No match found for the song '{song_name}'.")
                return None  

        # Load environment variables containing sensitive information
        load_dotenv()
        CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

        # Initialize Spotify client with credentials
        client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Define scope for playlist modification and initialize SpotifyOAuth
        scope = 'playlist-modify-public'
        username = '31vxd2rpgrlanjxy6mu5fvcexoaq'
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=scope, username=username, redirect_uri='http://127.0.0.1:3001/')
        access_token = sp_oauth.get_access_token(as_dict=False)
        spotifyObject = spotipy.Spotify(auth=access_token)

        # Interactively create a playlist
        playlist_name = "Input-Only Playlist"
        playlist_description = "This is your playlist, created by Spotify Playlist Generator!"
        track_num = 50
        playlist = spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Prompt user for track and artist, then search and add the track to the playlist
        track = sp.track(trackId)        
        list_of_songs = []
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        # Search for the track and add it to the playlist
        if artist_name:
            query = f"{track_name} {artist_name}"
        else:
            query = track_name
        result = spotifyObject.search(q=query)
        if len(result['tracks']['items']) > 0:
            list_of_songs.append(result['tracks']['items'][0]['uri'])
        else:
            print(f"No results found for '{track_name}' by '{artist_name}'")
        print(f"Added '{track_name}' by '{artist_name}' to the '{playlist_name}' playlist!")           
        
        # Generate and display recommendations based on the input track
        recommendations = input_track_recommendations(track_name, artist_name, sp)

        if recommendations is not None:
            print(f"\nTop {track_num} Recommendations:\n")
            for track in recommendations['tracks']:
                artists = ', '.join([artist['name'] for artist in track['artists']])
                list_of_songs.append(track['uri'])
                print(f"Added '{track['name']}' by '{artists}' to the '{playlist_name}' playlist!")
                                
        # Add recommended tracks to the playlist
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=list_of_songs)


@app.post("/post_features")
async def post_data(data: DataModel):
    
    # use the data to generate the playlist here
    playlist_generator(data.acousticness, data.danceability, data.energy, data.instrumentalness, data.mood_valence, data.tempo, data.prompt, data.trackId)
    return {"status": 200, "data": data}