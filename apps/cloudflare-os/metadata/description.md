# Cloudflare OS

Cloudflare OS is an "operating system" for AI productivity: an agent chat UI, sandboxed app development ("gadgets"), and a capability-based security layer ("Gatekeepers") that mediates agent and app access to external services.

This self-hosted build runs the full stack — frontend, backend, and every Gatekeeper Worker — in a single `workerd` container on port 8787, with persistent state and OAuth credentials supplied as app settings.

## Features

- **Agent chat**: converse with AI agents that can read, write, and run tools.
- **Gadgets**: agents build and run sandboxed web apps on the fly.
- **Gatekeepers**: each external service (GitHub, GitLab, Google, Linear, Notion, Spotify, Supabase, Cloudflare, …) is mediated by its own Worker, so agents and gadgets access it with scoped, revocable credentials.
- **OAuth login**: offer "Continue with …" sign-in via any configured Gatekeeper, alongside password auth.

## Prerequisites

- A reachable public origin (scheme + host) — the URL the browser actually uses. This drives every Gatekeeper's OAuth redirect URI.
- OAuth client ID/secret pairs for the services you want to enable (leave a pair empty to skip that Gatekeeper).

## Configuration

| Setting | Purpose |
| --- | --- |
| **Public Origin** | Full origin the app is served from (e.g. `https://flare.example.com`). Required. Must match the browser URL. |
| **Login Gatekeepers** | Comma-separated vendor ids to offer as login buttons (e.g. `google,github`). Empty = password-only login. |
| **`<Vendor> Client ID` / `<Vendor> Client Secret`** | OAuth credentials for that Gatekeeper. Leave both empty to leave the Gatekeeper unconfigured. |

Supported vendors: Google, GitHub, GitLab, Cloudflare, Linear, Notion, Spotify, Supabase.

## Notes

- State (accounts, workspaces, gadgets, Durable Objects) persists in the app's data directory across restarts and updates.
- The image is built from the [cloudflare/cloudflare-os](https://github.com/cloudflare/cloudflare-os) repository. This store entry references `127.0.0.1:5000/cloudflare-os:local`, a locally built image published to a **local Docker registry** on the host. Runtipi's install runs `docker compose down --rmi all` (which strips the image tag) before `up`, so the image must be re-pullable — a bare local tag would fail that pull. To set up: `docker run -d --name cfos-registry -p 127.0.0.1:5000:5000 registry:2`, then `docker tag cloudflare-os:local 127.0.0.1:5000/cloudflare-os:local && docker push 127.0.0.1:5000/cloudflare-os:local`.
