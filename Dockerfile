# syntax=docker/dockerfile:1

# ---------- Stage 1: build the React frontend ----------
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# -> produces /app/frontend/dist


# ---------- Stage 2: Python backend + built frontend ----------
FROM python:3.12-slim AS runtime
WORKDIR /app

# libmagic1 enables full MIME-type detection (backend/static_analysis/file_identifier.py
# falls back to a built-in magic-byte table if this is ever unavailable, so it's not
# required — just better accuracy when present).
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

RUN mkdir -p uploads reports logs

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Render/Railway/Fly all inject $PORT — default to 8000 for local `docker run`.
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
