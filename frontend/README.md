# Enterprise Knowledge Agent – Frontend

React (Vite + TypeScript) UI for the Enterprise Knowledge Agent: login, chat with SQL/vector results, and PDF upload.

## Features

- **Auth:** Login with company email; token stored in `localStorage` and sent as `Authorization: Bearer <token>`.
- **Chat sidebar:** Session info, role, sign out, clear session.
- **Message bubbles:** Markdown and tables (SQL results) rendered via `react-markdown` + `remark-gfm`.
- **Upload portal:** Drag-and-drop PDF to `/api/v1/upload` (Admin/HR only).

## Run locally (no Docker)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. Set `VITE_API_URL` if the backend is not at http://localhost:8000 (e.g. in `.env`: `VITE_API_URL=http://localhost:8000`).

## Run with Docker

From repo root:

```bash
docker compose up -d
```

- Frontend: http://localhost:3000  
- Backend API: http://localhost:8000  

The frontend is built with `VITE_API_URL=http://localhost:8000` so the browser calls the backend on port 8000.

## Login page background

To use your own image (e.g. the KnowledgeVolt architecture diagram) as the sign-in background, place it in the frontend as:

- **Path:** `frontend/public/login-bg.png`

It will be served at `/login-bg.png` and used as the full-page background behind the sign-in form (with a dark overlay for readability).

## Test login

Sign in with **email only** (no password). Seeded users (see `backend/app/db/seed.py`): e.g. `user0@enterprise.com` … `user4@enterprise.com`.
