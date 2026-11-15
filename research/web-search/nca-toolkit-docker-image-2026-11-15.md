# NCA Toolkit — Correct Docker Image Research

Date: 2026-11-15
Task: Find the correct, real, publicly-pullable Docker image for the RunTipi appstore app
`nca-toolkit`, which references `nca/nca-toolkit:latest` (404 on Docker Hub).

## Executive Summary

The appstore app "nca-toolkit" is **NOT** the Nintendo Switch NSP/NCA toolkit. It is the
**No-Code Architects Toolkit** (NCA = "No-Code Architects") — a real, self-hostable,
publicly-pullable Python/Flask media-processing API. The correct image is
`stephengpope/no-code-architects-toolkit` (282,264 pulls, active). The Nintendo NSP/NCA
tools are all CLI/GUI utilities with no real Docker web image. Note: the appstore entry's
port (8000), health path (/health), and PUID/PGID env vars do NOT match the real app —
the real app listens on **8080**, has no `/health` route (closest is `/v1/toolkit/test`),
and uses a fixed `appuser` (no PUID/PGID).

## Verified Facts

### 1. The 404 image is genuinely absent
- `nca/nca-toolkit` → Docker Hub API returns `{"message":"object not found"}`.
- Docker Hub search for "nca-toolkit" returns only 0-star personal/CI images
  (xiangyugongzuoliu, omar3leafi, macdesire, joec05, kojide, frankroron, gromeron,
  frkoom, srajeevan0227, juanzuluaga91) — none canonical.

### 2. The correct image: `stephengpope/no-code-architects-toolkit`
- Docker Hub: https://hub.docker.com/r/stephengpope/no-code-architects-toolkit
  - status: active, is_private: false
  - pull_count: 282,264, star_count: 11
  - date_registered: 2024-08-02, last_updated: 2026-01-02
  - description: "The NCA Toolkit API eliminates monthly subscription fees by
    consolidating common API functionalities into a single FREE API... media processing,
    video editing and captioning, image transformations, cloud storage, Python code execution."
- GitHub: https://github.com/stephengpope/no-code-architects-toolkit
  - 2,355 stars, pushed_at 2026-01-02, default_branch main
  - homepage: https://skool.com/no-code-architects
  - "built in Python using Flask"

### 3. Listening port = 8080 (NOT 8000)
Verified from the Dockerfile (raw.githubusercontent.com/.../main/Dockerfile):
- `EXPOSE 8080`
- gunicorn entrypoint: `gunicorn --bind 0.0.0.0:8080 ...`
- app.py `__main__`: `app.run(host='0.0.0.0', port=8080)`
- README: `docker run -d -p 8080:8080 ...`

### 4. Health endpoint
- There is NO `/health` route. All routes are under `/v1/...` (audio, code, ffmpeg, image,
  media, s3, toolkit, video).
- Closest to a health check: `GET /v1/toolkit/test` (docs/toolkit/test.md) — "designed to
  test the API setup. It creates a temporary file, uploads it to cloud storage, and then
  returns the upload URL." Requires `x-api-key` header.
- So an appstore healthcheck on `/health` will 404; use `/v1/toolkit/test` (with an API key)
  or a TCP/200 probe on 8080.

### 5. PUID/PGID
- NOT used. The Dockerfile creates a fixed user: `RUN useradd -m appuser` then
  `USER appuser`. `.env.example` has no PUID/PGID entries. So PUID/PGID env vars in the
  appstore entry are inert (harmless but ignored).

### 6. Stable tag to pin
Docker Hub tags (clean version tags): v1.0.1 … v1.0.17, then 1.0.18, 1.0.19, 1.1.0, 1.1.1,
1.1.2, 1.1.3. Variant/suffixed tags: 1.1.3-gdrive, 1.1.4-do, 1.1.4-nvidia (no clean 1.1.4).
- **Best clean version tag to pin: `1.1.3`**
  - digest sha256:985d2cc8ea4fd3cd6e1adcaf0761f9b549d6760817aac426c7e5934775f46c9c
  - last_updated 2024-09-18, full_size ~8.0 GB
- CAVEAT: `latest` was last updated **2025-11-12** (digest sha256:4b4e8702f9e4538280cabe32e850965cb988923aad8731c721d7922abbae3b6f),
  which is NEWER than `1.1.3` (2024-09-18). The maintainer has been pushing to `latest`
  without bumping clean version tags, so `1.1.3` is the newest *labeled* version but is
  ~14 months behind `latest`. If recency matters more than a stable label, pin by digest of
  `latest`.

### 7. Volumes (from docker-compose.yml)
- `storage:/var/www/html/storage/app`
- `logs:/var/www/html/storage/logs`
- Heavy env requirements (cloud storage): S3_ENDPOINT_URL, GDrive, GCS, Dropbox, etc.
  (see .env.example). It is a media API, not a simple stateless web app — it needs cloud
  storage credentials to be fully functional.

## Nintendo NSP/NCA toolkit (the caller's hypothesis) — ruled out
- The Nintendo "NCA/NSP toolkit" is a family of CLI/GUI file tools, none a port-8000 web
  service with /health:
  - jakcron/nstool — "General purpose read/extract tool for Nintendo Switch file formats"
    (NCA/NSP/XCI/ROMFS). CLI. https://github.com/jakcron/nstool
  - KillzXGaming/Switch-Toolbox — "A tool to edit many formats of Nintendo Switch, 3DS and
    Wii U." CLI/GUI. https://github.com/KillzXGaming/Switch-Toolbox
  - RinoWu96/NX-Toolkit — "Dark Chinese/English GUI for Nintendo Switch file tools:
    XCI/NSP/NSZ/XCZ converter." Desktop GUI.
- Docker Hub search "nsp" / "nintendo switch" returns only 0-star unrelated or junk images
  (quadric/nsp, delfus77/switch-library-manager-web, etc.). No real, maintained Docker web
  image for a Nintendo NSP/NCA toolkit exists.

## Report for the image

- **Exact correct image reference:** `stephengpope/no-code-architects-toolkit`
- **Best stable tag to pin:** `1.1.3` (newest clean version label; digest
  sha256:985d2cc8ea4fd3cd6e1adcaf0761f9b549d6760817aac426c7e5934775f46c9c). Note `latest`
  is actually newer (2025-11-12) — pin by digest if you want current behavior.
- **Container's actual listening port:** `8080` (not 8000)
- **1-line note:** Real, self-hostable web service (Flask media-processing API) — it fits a
  web app, but the appstore's port 8000 / /health / PUID/PGID are all wrong and need
  correcting to 8080 / `/v1/toolkit/test` / (no PUID/PGID, fixed appuser).
- **Confidence:** HIGH — verified directly from Docker Hub API, the GitHub repo's
  Dockerfile/app.py/README, and the docs.

## Sources and References
1. https://hub.docker.com/r/stephengpope/no-code-architects-toolkit — Docker Hub image
   (282,264 pulls, active). Verified via hub.docker.com/v2/repositories API.
2. https://github.com/stephengpope/no-code-architects-toolkit — source repo (2,355 stars).
3. https://raw.githubusercontent.com/stephengpope/no-code-architects-toolkit/main/Dockerfile
   — EXPOSE 8080, gunicorn bind 0.0.0.0:8080, fixed `appuser`.
4. https://raw.githubusercontent.com/stephengpope/no-code-architects-toolkit/main/app.py
   — app.run(port=8080), blueprint registration, no /health route.
5. https://raw.githubusercontent.com/stephengpope/no-code-architects-toolkit/main/README.md
   — `docker run -d -p 8080:8080`, /v1/... endpoint list.
6. https://raw.githubusercontent.com/stephengpope/no-code-architects-toolkit/main/docs/toolkit/test.md
   — /v1/toolkit/test health-like endpoint (requires x-api-key).
7. https://hub.docker.com/v2/repositories/stephengpope/no-code-architects-toolkit/tags/1.1.3
   — tag 1.1.3 digest + date.
8. https://github.com/jakcron/nstool — Nintendo NSP/NCA CLI tool (ruled out as the target).
9. https://github.com/KillzXGaming/Switch-Toolbox — Nintendo Switch file editor (ruled out).
10. https://huggingface.co/spaces/jananath/nca-toolkit — a HF Space also named "NCA Toolkit"
    (community, secondary).

## Recommendations
1. Change the appstore image from `nca/nca-toolkit:latest` to
   `stephengpope/no-code-architects-toolkit:1.1.3` (or pin `latest` by digest for recency).
2. Change the container port from 8000 to **8080**.
3. Change the healthcheck from `/health` to `GET /v1/toolkit/test` (supply an `x-api-key`),
   or use a plain TCP/HTTP 200 probe on 8080.
4. Drop the PUID/PGID env vars (inert) or keep them harmlessly; the app runs as `appuser`.
5. Budget for the heavy env: this is a media API that wants S3/GDrive/GCS/Dropbox
   credentials to be fully useful, and the image is ~8 GB. If the RunTipi slot is meant to
   be a lightweight "Nintendo NSP/NCA" utility, this app is a mismatch — there is no real
   Docker web image for the Nintendo toolkit, so it would need to be dropped or replaced
   with a CLI-in-a-container build.

## Additional Notes
- The name collision is the root confusion: "NCA Toolkit" (No-Code Architects) vs. "NCA"
  (Nintendo Content Archive). The appstore entry's web-app shape (port + health + env)
  matches the No-Code Architects Toolkit, not the Nintendo CLI family.
- `latest` (2025-11-12) vs `1.1.3` (2024-09-18) gap means version labels are stale; if you
  must pin a version and want current features, prefer digest-pinning `latest`.
