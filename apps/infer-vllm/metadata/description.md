# Infer: vLLM (official)

Stock vLLM v0.33.0 (CUDA 13, sm_120). Mirrors the host vllm-flagship flags: prefix caching, chunked prefill, fp8 KV, priority scheduling, qwen3_coder tools. KV offload uses the native OffloadingConnector (--kv-offloading-size). Spec decode uses the model's native MTP head. Metrics: /metrics. Anthropic API: /v1/messages.

## Notes

- The API listens on `127.0.0.1` only. Put a reverse proxy or LiteLLM in front of it.
- Set **Models directory (host)** to the folder with your weights, then set
  **Model path** to a folder inside it.
- The app never restarts on its own (`restart: "no"`), so it does not fight
  another engine for the GPU after a reboot.
- It uses the NVIDIA runtime. NVIDIA MPS settings are optional.
