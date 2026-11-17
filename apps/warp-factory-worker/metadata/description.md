# Warp Factory Worker

Self-hosted worker for **Warp Factories** — a cloud platform for running fleets of
coding agents across your software development lifecycle. This app is integrated
with this box's local resources so that, as far as Warp's architecture allows, the
*work* happens on our own hardware.

## What is self-hosted, and what is not

Warp Factories splits into two halves:

- **Control plane** (factories, runs, projects, agents, secrets) — hosted by Warp
  in the cloud. This is **not publicly self-hostable**: the worker's WebSocket
  endpoint (`wss://oz.warp.dev`) is hardcoded, and the `warp-server` repository is
  private. You manage the factory and watch results in the Warp web app.
- **Execution** (the actual agent tasks) — **self-hosted on this box**. This app
  runs the `oz-agent-worker` daemon, which dials *out* to Warp and runs each task
  locally.

So "all parts self-hosted" is true for everything that *does* work (execution,
LLM, SDK, project); the one cloud-only part is the control plane that routes runs.

## What this box provides (already wired in)

The app seeds a `worker.yaml` (see `data/worker.yaml`) that the worker loads via
`--config-file /data/worker.yaml`. It configures the **Docker backend** to:

- **Use the local LLM.** Every task container gets env vars pointing the agent
  harness at the local vLLM server over the Tailscale IP
  (`http://100.103.38.100:8010`, model `fable` = Qwen3.8-27B-Uncensored-FP8).
  vLLM serves both the Anthropic (`/v1/messages`) and OpenAI
  (`/v1/chat/completions`) APIs, so Claude-Code- and Codex-style harnesses both
  route to it. Delete those `environment` entries to fall back to Warp's cloud
  models instead.
- **Mount the Android SDK** at `/opt/android-sdk` and set `ANDROID_HOME` /
  `ANDROID_SDK_ROOT`, so Gradle / Android-Gradle-Plugin builds work in-task.
- **Mount Phone-Projects** (our first project) at `/workspace/phone-projects`.

Reachability of vLLM from a task container (Docker's default bridge) is verified.

## What you need

- A **Warp Enterprise** account (Factories / self-hosted workers are Enterprise).
- A **self-hosted worker API key** (starts with `wk-`) from your Warp account.
  This is the one thing that cannot be self-hosted or generated locally — without
  a valid key the worker starts and keeps retrying the connection (you will see
  `401 Unauthorized, retrying` in its logs).
- Outbound internet access from this box to `oz.warp.dev` (the worker dials out;
  no inbound port is opened).

## Making Phone-Projects the first project

1. In the Warp web app, create (or open) a **factory** and add a **project**
   whose working directory is the mounted path **`/workspace/phone-projects`**
   (do *not* point it at a git remote — the code is already on this box and
   mounted into the task container).
2. Configure the project's **environment / agent** to use a Claude-Code or Codex
   harness. The `ANTHROPIC_*` / `OPENAI_*` env vars from `worker.yaml` already
   route it to the local vLLM model.
3. Assign the run to this worker (worker id `runtipi-worker`).

The agent then edits and builds Phone-Projects on this box, using the local model
and the local Android SDK.

## How it runs

- **Docker socket mounted** (`/var/run/docker.sock`): the Docker backend spawns an
  isolated container per task. This is why the app runs as root and mounts the
  host socket.
- **`WARP_API_KEY`** is injected as an environment variable (never in argv or on
  disk).
- **`--worker-id`** is a stable identifier Warp uses to route runs to this worker.
  Keep it consistent across reinstalls.
- **`WARP_EXTRA_ARGS`** (optional) passes additional flags, e.g.
  `--max-concurrent-tasks 4` or `-v /other/repo:/repo`.

## Alternative: the "direct" backend (fully local harness)

The Docker backend uses Warp's sidecar images for the agent harness. If you want
the harness to be the **host's own coding CLIs** instead, switch to the `direct`
backend. The **Oz CLI is already installed on this host** (`/usr/bin/oz` →
`/opt/warpdotdev/oz-stable/oz`, package `oz-stable`). Because the worker runs in a
container, mount the host CLI into it and point `oz_path` at it:

1. Add this volume to the app (via `WARP_EXTRA_ARGS`: `-v
   /opt/warpdotdev/oz-stable:/opt/oz:ro`).
2. Replace the `backend:` block in `data/worker.yaml` with:

```yaml
backend:
  direct:
    workspace_root: "/var/lib/oz/workspaces"
    oz_path: "/opt/oz/oz"
    environment:
      - name: ANDROID_HOME
        value: "/home/morteza/Android/Sdk"
      - name: ANDROID_SDK_ROOT
        value: "/home/morteza/Android/Sdk"
```

The direct backend runs tasks on the host (no per-task container), so it uses the
host CLIs, the host SDK, and the host file ownership directly.

## Updating

The image is pinned to a release tag. To update, bump the tag in
`docker-compose.json` (and the reference `docker-compose.yml`) to a newer
`warpdotdev/oz-agent-worker` release, then reinstall the app.

## Links

- Source: https://github.com/warpdotdev/oz-agent-worker
- Product: https://www.warp.dev/factories
- Self-hosting docs: https://docs.warp.dev/factories/self-hosting/
