# OpenHands Agent Canvas

A **fully self-hosted control plane** for running fleets of coding agents across
your software development lifecycle. This is the self-hosted alternative to
**Warp Factories**: where Warp keeps the control plane (factories, runs, projects,
agents, transcripts) in its cloud, here **every part runs on this box** — the
control plane, the agent execution, the LLM, the Android SDK, and the project.
No cloud, no subscription, MIT-licensed.

## Why this app

Warp Factories splits into a cloud control plane (not self-hostable — the worker
dials out to `wss://oz.warp.dev`, and self-hosting the worker requires an
Enterprise plan) and a self-hosted worker. **OpenHands Agent Canvas removes the
cloud entirely**: it is the control plane *and* the execution host, and it is
model-agnostic, so the agent runs against the box's local LLM.

The `warp-factory-worker` app in this store is the Warp-specific path (needs a
Warp Enterprise `wk-` key). This app is the **free, 100% self-hosted** path.

## What is wired to this box

Everything the agent needs is local:

- **Control plane** — conversations, runs, transcripts, automations and
  workspaces are stored on this box under `~/.openhands` and served by the
  container. The UI is at the root of the subdomain, behind the RunTipi login.
- **Local LLM** — the agent is configured (in `~/.openhands/settings.json` and
  the `qwen3.6-local` LLM profile) to call the box's vLLM server over the
  Tailscale IP: model `openai/fable` at `http://100.103.38.100:8010/v1`
  (Qwen3.8-27B-Uncensored-FP8, a reasoning model). No external API, no key.
- **First project** — the agent's workspace is `~/projects`, so
  **Phone-Projects** is reachable at `/projects/Phone-Projects`. Point a
  conversation's working directory there and the agent edits and builds it
  directly (no clone).
- **Android SDK** — mounted at `/opt/android-sdk` so Gradle /
  Android-Gradle-Plugin builds work.

## How it runs

- The container runs as **uid 1000** (the host user), so files the agent writes
  to the project and the SDK are owned by you, not root. The image's default
  user (uid 10001) cannot write to the uid-1000 host directories.
- **Persistence** is the shared `~/.openhands` directory (settings, LLM
  profiles, skills, conversations). Reusing it keeps the RunTipi app, the
  `agent-canvas` CLI and the OpenHands skills on a single source of truth.
- The UI is served at the `/canvas` base path (the image's self-consistent
  default). The subdomain root `/` 308-redirects to `/canvas/`, so opening the
  bare subdomain lands you in the app.

## Using it

1. Open the app's subdomain (behind the RunTipi login).
2. Start a conversation and set its **working directory** to
   `/projects/Phone-Projects` (or any project under `/projects`).
3. Give the agent a task. It runs on the local model, edits the local project,
   and can run Gradle/Android builds against the local SDK. The transcript is
   kept on this box.

## Updating

The image is pinned to a release tag (`1.41.0`). To update, bump the tag in
`docker-compose.json` and the reference `docker-compose.yml`, then reinstall the
app.

## Links

- Product: https://www.openhands.dev/
- Source: https://github.com/OpenHands/OpenHands
- Agent Canvas: https://docs.all-hands.dev/
