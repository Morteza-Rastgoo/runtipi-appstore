# Agent notes — Morteza-Rastgoo/runtipi-appstore

Personal Runtipi appstore. Each app lives in `apps/<app-id>/` with `config.json`
(version, form fields, port), `docker-compose.yml`, and `metadata/` (description.md, logo).

## Two copies of this repo — do not confuse them

- **This repo** (`/mnt/SSD-Storage/home/morteza/runtipi/repos/morteza-rastgoo`, git,
  remote `Morteza-Rastgoo/runtipi-appstore`) is the **source of truth**.
- **Runtipi's runtime checkout** (`/mnt/SSD-Storage/home/morteza/runtipi/apps/morteza-rastgoo/`)
  is a **separate, Runtipi-managed copy** of the installed apps. It can be **stale** — e.g. it
  showed `cloudflare-os` at `1.0.0` while this repo was already at `1.0.1`. **Read versions and
  config from THIS repo, not the runtime checkout.**

## Updating an app (the flow that actually sticks)

1. Change the app's files here under `apps/<app-id>/`.
2. **Bump `config.json` → `version`** (and `updated_at`) so Runtipi sees a new version.
3. **Commit AND push.** Runtipi pulls this repo — an unpushed change is invisible and reverts on
   the next pull. Verify: `git rev-parse HEAD` == `git rev-parse @{u}`.
4. For apps that ship a locally built image (e.g. `cloudflare-os` → `127.0.0.1:5000/cloudflare-os:local`),
   the image must be **rebuilt and pushed to the local registry** separately — the repo change does
   not rebuild it. Runtipi's install runs `docker compose down --rmi all` before `up`, so the image
   tag must be re-pullable from `127.0.0.1:5000` (a bare local tag fails that pull). See
   `apps/cloudflare-os/metadata/description.md`.

## Verifying a deployed app is on the new build

- The app is a code-split SPA: the served `index.html` → entry `index-*.js` → lazy route chunks.
  **Confirm the specific chunk the browser loads contains the change** (or that the asset returns
  200) — grepping only the entry bundle or a `dist/` file is a false negative.
- `docker inspect --format='{{.State.Health.Status}}' <container>` + a health probe, and confirm the
  container's image id matches the one you just pushed.
