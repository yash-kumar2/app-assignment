# App Assignment

A full-stack video streaming application featuring a secure, token-based video proxy system.

## 🚀 Overview

This project demonstrates a secure video delivery architecture. The application allows authenticated users to browse a dashboard of videos and stream them via a custom secure player.

**Key Architecture:** The frontend never interacts with the video source directly. Instead, it utilizes a **Backend Proxy** pattern (Option B) where the backend strictly controls access via short-lived tokens and pipes the video stream securely to the client (Frontend loops to Backend Proxy loops to Upstream Source).

## 🛠️ Tech Stack

- **Frontend:** React Native (Expo), TypeScript, `expo-av`.
- **Backend:** Python (Flask), `requests` for proxying, `flask-jwt-extended` for auth.
- **Database:** MongoDB.

## 📦 Project Structure

```
app-assignment/
├── backend/            # Flask API & Proxy Server
│   ├── routes/         # API Endpoints (Auth, Video, Dashboard)
│   ├── utils/          # Helper functions (Token gen, upstream resolver)
│   └── ...
└── frontend/           # React Native Expo App
    ├── app/            # Expo Router screens (Video Player, Dashboard)
    ├── lib/            # API Client
    └── ...
```

## ⚡ Getting Started

### Prerequisites

- Node.js & npm
- Python 3.10+
- MongoDB (running locally or cloud URI)

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   Copy `.env.example` to `.env` and update variables (MongoDB URI, etc.).
   ```bash
   # Windows (Powershell)
   Copy-Item .env.example .env
   ```
5. Seed the database with sample videos:
   ```bash
   python seed_videos.py
   ```
6. Run the server:
   ```bash
   python -m flask run
   ```
   The API will start at `http://localhost:5000`.

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure environment:
   Copy `.env.example` to `.env` to set the API URL.
   ```bash
   # Windows (Powershell)
   Copy-Item .env.example .env
   ```
4. Run the development server:
   ```bash
   npm run web
   # Or for mobile:
   # npm run android
   # npm run ios
   ```

## 🔐 Security Features

- **JWT Authentication:** All API routes are protected.
- **Secure Video Proxy:** The `/video/<id>/stream` endpoint validates a signed, short-lived playback token. It then fetches the video bytes from the upstream source and streams them strictly to the authenticated client, creating a "walled garden" for content.
