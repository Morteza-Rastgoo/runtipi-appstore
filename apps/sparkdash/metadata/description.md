# sparkDash

Real-time web dashboard for one or more **NVIDIA DGX Spark (GB10)** machines — and any Linux, macOS, or Windows unit with an NVIDIA GPU. Streams GPU, CPU, unified memory, storage, network, and local LLM metrics in a single browser window. Add, edit, reorder, or remove units from the UI without restarts.

- **Local unit**: add the host itself with "This host (local collectors — no SSH for metrics)".
- **Remote units**: monitored over SSH (GPU via `nvidia-smi`, plus CPU/memory/storage/network).
- **Local LLM metrics**: probes local inference servers (vLLM, llama.cpp server, etc.) for token rates and KV-cache fill.
- **Extras**: quality/decode bench, fleet token + energy history, alerts (ntfy and more), Prometheus `/metrics` export, mobile PWA, kiosk mode, Home Assistant integration.

## Image

Upstream publishes `ghcr.io/miaai-lab/sparkdash` per release tag, but the publish workflow was added **after v2.32.0**, so no release has a published image yet (`docker pull` answers `denied` until a newer release ships). This app therefore uses an image **built from source** (v2.32.0, `main`) and served from the local registry:

```
127.0.0.1:5000/sparkdash:local   (also tagged :2.32.0)
```

Rebuild + republish after an upstream update:

```bash
git clone --depth 1 --branch main https://github.com/MiaAI-Lab/sparkDash /tmp/sparkdash-src
docker build -t 127.0.0.1:5000/sparkdash:local -t 127.0.0.1:5000/sparkdash:<version> /tmp/sparkdash-src
docker push 127.0.0.1:5000/sparkdash:local
docker push 127.0.0.1:5000/sparkdash:<version>
```

Once upstream publishes a release image, swap the `image` to `ghcr.io/miaai-lab/sparkdash:<version>` and drop the local build.

## How it runs

The container needs host access to read metrics, so it runs with:

- `privileged: true` + `pid: host` — `nsenter` into the host PID namespace and `nvidia-smi` compute-apps.
- Read-only host mounts: `/proc`, `/sys`, `/`, `/usr/bin/nvidia-smi`, and the host's `libnvidia-ml.so.1` (x86_64 path; on an arm64 Spark use `/usr/lib/aarch64-linux-gnu/libnvidia-ml.so.1`).
- `${APP_DATA_DIR}/config:/app/config` — persistent `sparks.json` + encrypted secrets.

Unlike the upstream compose (which uses `network_mode: host`), this app joins the RunTipi bridge network so Traefik can route it. Consequence: LLM servers on the host that bind to **127.0.0.1** are not reachable by their loopback address from inside the container — target them as `http://host.docker.internal:<port>` instead (mapped to the host gateway).

## Access

- Behind the Runtipi login (forward auth) on its own subdomain.
- Noindex: responses carry `X-Robots-Tag: noindex, nofollow`.
- Optional second gate: set the **Dashboard Access Token** form field (`SPARKDASH_TOKEN`). When set, the dashboard itself asks for the token in the browser.
