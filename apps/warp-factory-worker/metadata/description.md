# Warp Factory Worker

Self-hosted worker for **Warp Factories** — a cloud platform for running fleets of
coding agents across your software development lifecycle. The control plane (the
"factory") is hosted by Warp; this app runs the **worker** on your own
infrastructure so the actual agent tasks execute on your hardware instead of in
Warp's cloud.

This is a **headless background daemon**. It has no web UI and no port — it
connects *outbound* over a WebSocket to Warp's Automation Platform and waits for
runs to be routed to it. You manage the factory, define the runs, and watch the
results in the Warp web app; the worker is the thing that does the work.

## What you need

- A **Warp Enterprise** account (Factories / self-hosted workers are an Enterprise feature).
- A **self-hosted worker API key** (starts with `wk-`) from your Warp account.
- Outbound internet access from this box to `oz.warp.dev` (the worker dials out;
  no inbound port is opened).

Without a valid key the worker still starts and keeps retrying the connection —
you will see `Failed to connect` / auth errors in its logs until the key is valid.

## How it runs

- **Docker socket mounted** (`/var/run/docker.sock`): the worker's default backend
  is `docker`, so it spawns an isolated container per task. This is why the app runs
  as root and mounts the host socket — it needs full control of the local Docker
  daemon to create and tear down task containers.
- **`WARP_API_KEY`** is injected as an environment variable (never written to disk
  or shown in the process list).
- **`--worker-id`** is a stable identifier Warp uses to route runs to this worker.
  Keep it consistent if you re-install the app.
- **`WARP_EXTRA_ARGS`** (optional) passes any additional flags to the binary, e.g.
  `--config-file /data/worker.yaml`, `--backend direct`, `--max-concurrent-tasks 4`,
  or `-v /path/to/repo:/repo` to pre-mount a repository into task containers.

## Updating

The image is pinned to a release tag. To update, bump the tag in
`docker-compose.json` (and the reference `docker-compose.yml`) to a newer
`warpdotdev/oz-agent-worker` release, then reinstall the app.

## Links

- Source: https://github.com/warpdotdev/oz-agent-worker
- Product: https://www.warp.dev/factories
