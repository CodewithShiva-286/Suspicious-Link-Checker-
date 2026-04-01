# Deploying to Vercel

This repository is set up so **Vercel hosts the React (Vite) frontend**. The **FastAPI backend** (MongoDB, external APIs) should run on a platform that supports long-lived Python processes and your database (for example Railway, Render, Fly.io, or a VPS).

## 1. Deploy the frontend on Vercel

1. Import the Git repository in [Vercel](https://vercel.com).
2. Leave the project **root** as the repository root (no “Root Directory” change required). The root `vercel.json` builds `frontend/` and publishes `frontend/dist`.
3. Add this **environment variable** in the Vercel project (Settings → Environment Variables):

   | Name | Value | Environments |
   |------|--------|----------------|
   | `VITE_API_BASE_URL` | `https://your-api-host.example.com/api/v1` | Production (and Preview if the API supports preview URLs) |

   Use the **public base URL of your deployed API**, including the `/api/v1` prefix (same as `API_PREFIX` on the backend).

4. Deploy. The site will call `VITE_API_BASE_URL` at build time (embedded in the bundle), so change it when the API URL changes and redeploy.

## 2. Run the API elsewhere

1. Deploy the `backend/` app (for example `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
2. Use **MongoDB Atlas** (or another reachable MongoDB) and set `MONGODB_URI` on the API host.
3. Set API keys (`GOOGLE_SAFE_BROWSING_API_KEY`, `VIRUSTOTAL_API_KEY`, etc.) on the API host.
4. **CORS:** Point the browser origin at your Vercel app:

   ```env
   FRONTEND_ORIGIN=https://your-app.vercel.app
   CORS_ORIGINS=https://your-app.vercel.app
   ```

   For **Vercel preview** deployments (per-branch URLs), either list each origin in `CORS_ORIGINS` (comma-separated) or add:

   ```env
   CORS_ORIGIN_REGEX=https://.*\.vercel\.app
   ```

   Review whether that regex matches only hosts you trust.

## 3. Local check (production build)

```bash
cd frontend
npm ci
set VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
npm run build
npm run preview
```

On Windows PowerShell, use `$env:VITE_API_BASE_URL="..."` instead of `set`.

## Why not the API on Vercel?

Vercel serverless functions are a poor fit for this FastAPI app as written: Motor/MongoDB connection lifecycle, scan duration, and cold starts are easier to handle on a container or VM-style host. The setup above is the standard split: **static site on Vercel**, **API + DB elsewhere**.
