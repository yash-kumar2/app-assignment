## Backend Video API (Flask + MongoDB)

This is a production-style Flask REST API powering a React Native video app.
The mobile client is a **thin viewer** – all business logic (auth, video
selection, playback, analytics) lives in this backend.

YouTube is treated as a **private implementation detail**: the client never
sees YouTube URLs or IDs and can only interact through opaque backend tokens.

---

### Features

- **JWT auth** with access + refresh tokens
- **bcrypt password hashing** (via Werkzeug)
- **Rate-limited login** endpoint
- **Dashboard API** returning exactly 2 active videos
- **Playback tokens** (short-lived, video-specific JWTs)
- **Masked stream URLs** that never leak YouTube IDs
- **Watch analytics** for progress / engagement tracking
- Health check endpoint

---

### Project Layout

```text
backend/
  app.py
  config.py
  extensions/
    db.py
    jwt.py
  middleware/
    auth.py
  models/
    user.py
    video.py
  routes/
    auth.py
    dashboard.py
    video.py
  utils/
    token.py
    youtube.py
  seed_videos.py
  requirements.txt
  .env.example
  README.md
```

---

### Setup

1. **Create virtualenv & install deps**

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # on Windows
pip install -r requirements.txt
```

2. **Configure environment**

```bash
cp .env.example .env   # then edit secrets as needed
```

3. **Run MongoDB**

Make sure MongoDB is running locally (default URI in `.env.example` is
`mongodb://localhost:27017/video_app`).

4. **Seed videos**

```bash
python seed_videos.py
```

5. **Run the API**

```bash
python app.py
```

The API will be available at `http://localhost:5000/api`.

---

### Key Endpoints

Base URL: `/api`

- **Health**: `GET /api/health`

#### Auth

- **Signup**: `POST /api/auth/signup`
- **Login** (rate limited): `POST /api/auth/login`
- **Current user**: `GET /api/auth/me`
- **Refresh access token**: `POST /api/auth/refresh`
- **Logout (mock)**: `POST /api/auth/logout`

All protected routes require:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Dashboard

- **Dashboard**: `GET /api/dashboard`

Returns exactly 2 active videos with:

```json
{
  "videos": [
    {
      "id": "video_id",
      "title": "How Startups Fail",
      "description": "Lessons from real founders",
      "thumbnail_url": "https://..."
    }
  ]
}
```

#### Playback Flow

1. **Generate playback token** (client cannot see YouTube IDs):

- `POST /api/video/{video_id}/play`

Response:

```json
{
  "video_id": "video_id",
  "playback_token": "signed_token",
  "expires_in": 300
}
```

2. **Stream video**:

- `GET /api/video/{video_id}/stream?token=...`

Response:

```json
{
  "stream_url": "https://player.example.com/embed/secure"
}
```

The actual YouTube ID **never** appears in any response – it is only resolved
inside `utils/youtube.py`.

#### Analytics

- **Watch events**:

`POST /api/video/{video_id}/watch`

```json
{
  "event": "progress",
  "timestamp": 120
}
```

These are stored in a `watch_events` collection for later analysis.

---

### Security Notes

- Passwords are stored **only** as salted hashes (Werkzeug).
- JWT access tokens have limited expiry; refresh tokens are separate.
- Playback tokens are short-lived (≤ 5 minutes), video-specific, and signed.
- Login is rate limited via `Flask-Limiter`.
- All YouTube-specific logic is abstracted behind `utils/youtube.py`.

