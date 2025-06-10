# Spotify Playlist Generator

The **Spotify Playlist Generator** is a full-stack application that leverages AI and the Spotify API to create personalized playlists based on user prompts and audio feature sliders. With a React.js frontend and a FastAPI backend, users can fine-tune attributes like danceability, energy, and tempo, or start with a specific track seed.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
  - [Backend (Server)](#backend-server)
  - [Frontend (Client)](#frontend-client)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Contact](#contact)

---

## Features

- **AI-Powered Playlist Curation**: Uses OpenAI GPT-4 to suggest audio feature targets and genres from user prompts.
- **Audio Feature Sliders**: Fine-tune attributes like acousticness, danceability, energy, instrumentalness, valence, and tempo.
- **Track Seed Search**: Optionally seed playlist generation with a specific Spotify track.
- **Dynamic Recommendations**: Fetches recommendations via Spotify's Web API.
- **Interactive UI**: Responsive React frontend with real-time previews of selected tracks.

---

## Prerequisites

- **Node.js** (v16+)
- **npm** (v8+)
- **Python** (3.9+)
- **pip** (Python package manager)
- A **Spotify Developer** account (Client ID & Client Secret)
- An **OpenAI** API key

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spotify-playlist-generator.git
   cd spotify-playlist-generator
   ```

2. **Setup the Backend**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install fastapi "uvicorn[standard]" python-dotenv spotipy openai pydantic
   ```

3. **Setup the Frontend**
   ```bash
   cd ../client
   npm install
   ```

---

## Environment Variables

Create a `.env` file in the **server** root (`/server`) with the following variables:

```dotenv
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key
```

Ensure these values are kept secure and never committed to version control.

---

## Running the Application

### Backend (Server)

1. Activate your virtual environment:
   ```bash
   cd server
   source venv/bin/activate
   ```
2. Start the FastAPI server:
   ```bash
   npm run dev       # or: uvicorn src.app:app --reload --port 8080
   ```
3. The API will be available at: `http://localhost:8080`

### Frontend (Client)

1. In a separate terminal:
   ```bash
   cd client
   npm start
   ```
2. Open your browser and navigate to: `http://localhost:3000`

---

## Project Structure

```
spotify-playlist-generator/
├── client/          # React frontend
│   ├── public/      # Static assets and HTML template
│   └── src/         # React components, CSS, and entry point
├── server/          # FastAPI backend
│   └── src/app.py   # API routes and playlist logic
├── .gitignore
├── LICENSE          # MIT License
└── README.md        # Project documentation
```

---

## Technologies Used

- **Frontend**: React.js, React Router, CSS3
- **Backend**: Python, FastAPI, Uvicorn
- **AI**: OpenAI GPT-4 API
- **Music API**: Spotify Web API via `spotipy`
- **Environment Management**: `python-dotenv`

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

Created by **Richard Augustine**.

For questions or feedback, please open an issue or reach out at `your.email@example.com`.
