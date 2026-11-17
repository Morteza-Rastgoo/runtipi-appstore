# Infer: GPUStack (control plane)

GPUStack v2.3.1 server with the embedded worker. You deploy models from the web UI (admin / the generated password in the app settings). The worker starts each model as a separate runner container (vLLM, SGLang, ...) through the Docker socket. Built-in Prometheus + Grafana dashboards and an OpenAI-compatible gateway. Caution: the runner containers that GPUStack creates do not join the host NVIDIA MPS daemon (no uid 1000, no /tmp/nvidia-mps), so on this Exclusive_Process GPU they can only start while the host vLLM and its MPS daemon are stopped. The data dir uses the same path inside and outside the container so runner containers can mount model files from it.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
