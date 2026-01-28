## Frontend (React Native + Expo Router)

This is a **thin React Native client** that only talks to the Flask backend
via HTTP APIs. It contains **no business logic** and knows nothing about
YouTube – it only renders what the backend returns.

---

### Requirements

- Node.js and npm
- Expo CLI (`npx expo`)
- The backend running at `http://localhost:5000/api` (or your own URL)

---

### Setup

1. Install dependencies

```bash
cd frontend
npm install
```

2. Configure API URL

```bash
cp .env.example .env
```

Edit `.env` and set:

```bash
EXPO_PUBLIC_API_URL=http://localhost:5000/api
```

3. Start the app

```bash
npm start
```

Then open on an emulator or a device using Expo Go.

---

### Screens & Flows

- **Signup (`/signup`)**
  - Fields: name, email, password
  - Calls `POST /auth/signup`
  - On success → navigate to Login

- **Login (`/login`)**
  - Fields: email, password
  - Calls `POST /auth/login`
  - On success:
    - Stores `access_token` + `refresh_token` using `expo-secure-store`
    - Navigates to main tabs (`/(tabs)`)

- **Dashboard (`/(tabs)/index`)**
  - Calls `GET /dashboard` with `Authorization: Bearer <access_token>`
  - Renders exactly the 2 videos from backend:
    - Thumbnail
    - Title
    - Description
  - Tap a tile → `/video/[id]`

- **Video Player (`/video/[id]`)**
  - Flow:
    1. `POST /video/{id}/play` to get playback token
    2. `GET /video/{id}/stream?token=...` to get `stream_url`
  - Renders video using `expo-av` `Video` component
  - Controls:
    - Play / Pause
    - Mute / Unmute
    - Seek +10s
  - Treats `stream_url` as opaque (no inspection or logic based on URL)

- **Settings (`/(tabs)/settings`)**
  - Calls `GET /auth/me` to show name and email
  - Logout button:
    - Calls `POST /auth/logout`
    - Clears tokens from secure storage
    - Navigates back to `/login`

---

### Token Handling

- Tokens are stored in **secure storage** via `expo-secure-store`.
- All authenticated requests use:

```http
Authorization: Bearer <access_token>
```

- If a request returns **401 Unauthorized**:
  - The app calls `POST /auth/refresh` with the stored `refresh_token`
  - If successful, it saves the new `access_token` and retries the original
    request **once**
  - If refresh fails, it clears tokens and the next actions will behave as
    unauthenticated (you should re-login)

All of this logic lives in `lib/api.ts` so that screens only describe UI and
which endpoints to call, without any business logic or YouTube knowledge.

# Welcome to your Expo app 👋

This is an [Expo](https://expo.dev) project created with [`create-expo-app`](https://www.npmjs.com/package/create-expo-app).

## Get started

1. Install dependencies

   ```bash
   npm install
   ```

2. Start the app

   ```bash
   npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.
