# Warp Factory Worker

Self-hosted worker for **Warp Factories** — a cloud platform for running fleets
of coding agents across your software development lifecycle. This app is
integrated with this box's local resources so that, as far as Warp's
architecture allows, the *work* happens on our own hardware.

## What is self-hosted, and what is not

Warp Factories splits into two halves:

- **Control plane** (factories, runs, projects, agents, secrets) — hosted by Warp
  in the cloud. This is **not publicly self-hostable**: the worker's WebSocket
  endpoint (`wss://oz.warp.dev`) is hardcoded, the `warp-server` repository is
  private, and setting `WARP_SERVER_ROOT_URL` does not change where the worker
  dials (verified empirically). You manage the factory and watch results in the
  Warp web app.
- **Execution** (the actual agent tasks) — **self-hosted on this box**. This app
  runs the `oz-agent-worker` daemon, which dials *out* to Warp and runs each task
  locally, using the local `oz` CLI, the local LLM, and the local Android SDK.

So "all parts self-hosted" is true for everything that *does* work (execution,
LLM, SDK, project, the agent CLI); the one cloud-only part is the control plane
that routes runs.

## Backend: `command` (most self-hosted, the default here)

The app uses the worker's **command backend**. For each task the worker hands our
operator dispatch script (`data/dispatch-oz.py`, seeded to `/data/dispatch-oz.py`)
a versioned JSON payload on stdin. The script runs the **host `oz` CLI** (mounted
at `/opt/oz/oz`) **in our local project directory** (`/workspace/phone-projects`).

Why the command backend: a Warp "project" is normally a git repo the worker
*clones* into the task workspace. The command backend lets *us* set the working
directory, so the factory's **first project is this box's
`~/projects/Phone-Projects`** — not a fresh clone. It is also the most
self-hosted path: our dispatch script, our `oz` CLI, our model, our SDK.

What the app wires in (all on this box):

- **Local LLM.** The dispatch script's environment points the agent harness at
  the local vLLM server over the Tailscale IP (`http://100.103.38.100:8010`,
  model `fable` = Qwen3.8-27B-Uncensored-FP8). vLLM serves both the Anthropic
  (`/v1/messages`) and OpenAI (`/v1/chat/completions`) APIs, so Claude-Code- and
  Codex-style harnesses both route to it. Delete those `environment` entries in
  `worker.yaml` to fall back to Warp's cloud models.
- **Android SDK** at `/opt/android-sdk` with `ANDROID_HOME` / `ANDROID_SDK_ROOT`
  set, so Gradle / Android-Gradle-Plugin builds work.
- **Phone-Projects** at `/workspace/phone-projects` (the first project).
- **The `oz` CLI** at `/opt/oz/oz` (the host's static `oz` binary, mounted
  read-only).

Reachability of vLLM from the worker container (on the runtipi network) is
verified.

## The worker image (derived, local)

The stock `warpdotdev/oz-agent-worker` image is **Alpine (musl)** and has no
`python3` or `jq`, which the dispatch script needs. This app therefore runs a
**derived image** built from the pinned release with `python3` added:

```
FROM warpdotdev/oz-agent-worker:v2026-11-12-16-17-15
USER root
RUN apk add --no-cache python3
```

built and pushed to the local registry as
`127.0.0.1:5000/oz-agent-worker-local:v2026-11-12-16-17-15`. To rebuild it after
bumping the base tag:

```
docker build -t 127.0.0.1:5000/oz-agent-worker-local:<tag> <dir-with-Dockerfile>
docker push 127.0.0.1:5000/oz-agent-worker-local:<tag>
```

The host `oz` binary is **statically linked**, so it runs inside the Alpine
worker container (verified: `oz --version` inside the container).

## What you need

- A **Warp Enterprise** account (Factories / self-hosted workers are Enterprise).
- A **self-hosted worker API key** (starts with `wk-`) from your Warp account.
  This is the one thing that cannot be self-hosted or generated locally — without
  a valid key the worker starts and keeps retrying the connection (you will see
  `401 Unauthorized, retrying` in its logs).
- Outbound internet access from this box to `oz.warp.dev` (the worker dials out;
  no inbound port is opened).

## Making Phone-Projects the first project

1. In the Warp web app, create (or open) a **factory** and add a **project**.
   Because the command backend runs the agent in `/workspace/phone-projects`, the
   agent works directly on this box's local Phone-Projects checkout.
2. Configure the project's **agent** to use a Claude-Code or Codex harness. The
   `ANTHROPIC_*` / `OPENAI_*` env vars from `worker.yaml` already route it to the
   local vLLM model.
3. Assign the run to this worker (worker id `runtipi-worker`).

The agent then edits and builds Phone-Projects on this box, using the local model
and the local Android SDK. Per-run payloads and logs land in
`${APP_DATA_DIR}/data/run-logs/` for inspection.

## How it runs

- **`WARP_API_KEY`** is injected as an environment variable (never in argv or on
  disk).
- **`--worker-id`** is a stable identifier Warp uses to route runs to this worker.
  Keep it consistent across reinstalls.
- **`WARP_EXTRA_ARGS`** (optional) passes additional flags, e.g.
  `--max-concurrent-tasks 4`.
- The app runs as root and mounts the host Docker socket (kept so the Docker
  backend can be re-enabled; the command backend does not use it).

## Alternative: the `docker` backend (per-task containers)

If you'd rather have each task run in an isolated container with Warp's sidecar
images (instead of the host `oz` CLI), switch `worker.yaml`'s `backend:` block to
`docker:` and move the Phone-Projects / SDK / LLM mounts into `docker.volumes` +
`docker.environment` (the command backend mounts them into the *worker*
container; the docker backend mounts them into each *task* container). The docker
backend's task container has `WorkingDir: /workspace`, where the `oz` agent
clones the configured repo.

## Updating

The base image is pinned to a release tag. To update, bump the tag in the
Dockerfile, rebuild + push the derived image, update `docker-compose.json` (and
the reference `docker-compose.yml`), then reinstall the app.

## Links

- Source: https://github.com/warpdotdev/oz-agent-worker
- Product: https://www.warp.dev/factories
- Self-hosting docs: https://docs.warp.dev/factories/self-hosting/
- Command backend: https://docs.warp.dev/factories/self-hosting/external-orchestrators/
