# spotify-playlist-generator
The Spotify Playlist Generator focuses on delivering a truly personalized music discovery experience by using AI to create playlists that uniquely incorporates a user’s real-time mood, preferences, and situational needs.

Change the directory to /spotify-playlist-generator and run npm i to install required packages. 

To run, make the following pip install statement:
pip install fastapi "uvicorn[standard]" python-dotenv openai spotipy pydantic

Then in 2 separate terminals, change directories to /spotify-playlist-generator/client and /spotify-playlist-generator/server/src and run npm start and npm run dev to start the client and the server.